"""Stats on why trades win or lose, forecast accuracy, and rule-change suggestions."""
import datetime as dt
import statistics as st
from collections import defaultdict

from . import config as C


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _bucket_edge(e):
    return "8-12c" if e < 0.12 else "12-20c" if e < 0.20 else "20c+"


def _bucket_price(p):
    return "5-25c" if p < 0.25 else "25-50c" if p < 0.50 else "50-75c" if p < 0.75 else "75-90c"


def _bucket_dist(r):
    try:
        z = abs(float(r["distance"])) / float(r["sigma"])
    except (TypeError, ValueError, ZeroDivisionError):
        return "n/a"
    return "within 0.5 sigma of forecast" if z <= 0.5 else "0.5-1.5 sigma" if z <= 1.5 else "1.5+ sigma"


def summarize(rows):
    n = len(rows)
    if not n:
        return {"n": 0}
    wins = sum(r["won"] == "1" for r in rows)
    pnl = sum(float(r["pnl"]) for r in rows)
    cost = sum(float(r["cost"]) for r in rows)
    fees = sum(float(r["fee"]) for r in rows)
    brier_model = st.mean((float(r["model_p"]) - (r["won"] == "1")) ** 2 for r in rows)
    brier_market = st.mean((float(r["price"]) - (r["won"] == "1")) ** 2 for r in rows)
    return {
        "n": n, "wins": wins, "win_rate": round(wins / n, 3), "pnl": round(pnl, 2),
        "roi": round(pnl / cost, 3) if cost else 0, "fees": round(fees, 2),
        "avg_edge": round(st.mean(float(r["edge"]) for r in rows), 3),
        "avg_model_p": round(st.mean(float(r["model_p"]) for r in rows), 3),
        "brier_model": round(brier_model, 4), "brier_market": round(brier_market, 4),
    }


def breakdowns(settled):
    keys = {
        "city": lambda r: r["city"],
        "side": lambda r: r["side"].upper(),
        "edge": lambda r: _bucket_edge(float(r["edge"])),
        "price": lambda r: _bucket_price(float(r["price"])),
        "days_ahead": lambda r: f"{r['lead_days']} day(s)" if r.get("unit") == "F" else (
            "under 6h" if float(r["lead_hours"]) < 6 else "6-24h" if float(r["lead_hours"]) < 24 else "1 day+"),
        "bracket_distance": _bucket_dist,
        "bracket_type": lambda r: r["strike_type"],
        "cause": lambda r: r.get("cause") or "unknown",
        "version": lambda r: r["strategy_version"],
    }
    out = {}
    for name, fn in keys.items():
        groups = defaultdict(list)
        for r in settled:
            groups[fn(r)].append(r)
        out[name] = {k: summarize(v) for k, v in sorted(groups.items())}
    return out


def calibration(settled):
    """Does 'model says 60%' actually win 60% of the time?"""
    groups = defaultdict(list)
    for r in settled:
        p = float(r["model_p"])
        groups[min(int(p * 10), 9)].append(r)
    rows = []
    for b, rs in sorted(groups.items()):
        rows.append({"bucket": f"{b*10}-{b*10+10}%", "n": len(rs),
                     "predicted": round(st.mean(float(r["model_p"]) for r in rs), 3),
                     "actual": round(sum(r["won"] == "1" for r in rs) / len(rs), 3)})
    return rows


def forecast_accuracy(forecasts, actuals, book):
    """NWS error (actual - forecast) per city and days ahead, using the last forecast of each day."""
    if book["kind"] != "weather":
        return []
    act = {(a["series"], a["target_date"]): float(a["actual"]) for a in actuals}
    last = {}
    for f in forecasts:
        if f["forecast"] in ("", None):
            continue
        last[(f["series"], f["target_date"], f["lead_days"])] = float(f["forecast"])
    errs = defaultdict(list)
    for (s, d, lead), fc in last.items():
        if (s, d) in act:
            errs[(s, int(lead))].append(act[(s, d)] - fc)
    out = []
    for (s, lead), es in sorted(errs.items()):
        city = C.STATIONS.get(book["series"].get(s, ""), {}).get("city", s)
        out.append({"series": s, "city": city, "days_ahead": lead,
                    "n": len(es), "bias": round(st.mean(es), 2),
                    "mae": round(st.mean(abs(e) for e in es), 2),
                    "stdev": round(st.pstdev(es), 2) if len(es) > 1 else None,
                    "sigma_used": book["sigma_by_lead_days"].get(lead)})
    return out


def suggestions(settled, bd, acc):
    """Ranked ideas for the NEXT single rule change. Nothing changes automatically."""
    s = []
    if len(settled) < 20:
        s.append({"priority": 0, "text": f"Only {len(settled)} settled trades. Wait for 20+ before changing any rule."})
    for a in acc:
        if a["n"] >= 7 and abs(a["bias"]) >= 1.0:
            s.append({"priority": 2, "text": f"NWS runs {'cold' if a['bias'] > 0 else 'warm'} in {a['city']} "
                      f"({a['days_ahead']} day(s) ahead, avg error {a['bias']:+.1f}F over {a['n']} days). "
                      f"Try bias['{a['series']}'] = {a['bias']:+.1f} in this book's config."})
        if a["n"] >= 10 and a["stdev"] and a["sigma_used"] and abs(a["stdev"] - a["sigma_used"]) >= 0.5:
            s.append({"priority": 1, "text": f"Measured forecast spread in {a['city']} ({a['days_ahead']} day(s) ahead) "
                      f"is {a['stdev']}F but the model assumes {a['sigma_used']}F."})
    if len(settled) >= 20:
        tot = summarize(settled)
        if tot["brier_model"] > tot["brier_market"]:
            s.append({"priority": 3, "text": f"Market prices beat the model (Brier {tot['brier_market']} vs {tot['brier_model']}). "
                      f"Raise MIN_EDGE or tighten sigma before trusting it."})
        for dim in ("city", "edge", "price", "days_ahead", "bracket_distance", "side"):
            for k, v in bd.get(dim, {}).items():
                if v["n"] >= 8 and v["roi"] <= -0.25:
                    s.append({"priority": 2, "text": f"{dim} = {k} is losing badly ({v['n']} trades, ROI {v['roi']:.0%}). Consider excluding it."})
    return sorted(s, key=lambda x: -x["priority"])


def bankroll_curve(settled, start):
    bank, pts = start, []
    for r in sorted(settled, key=lambda r: r["closed_at"]):
        bank += float(r["pnl"])
        pts.append({"t": r["closed_at"], "bankroll": round(bank, 2)})
    return pts


def build(book_id, trades, forecasts, actuals, now):
    book = C.BOOKS[book_id]
    settled = [t for t in trades if t["status"] == "settled"]
    open_ = [t for t in trades if t["status"] == "open"]
    bd = breakdowns(settled)
    acc = forecast_accuracy(forecasts, actuals, book)
    return {
        "book": book_id, "name": book["name"], "short": book["short"], "kind": book["kind"],
        "unit": book["unit"], "starting_bankroll": book["bankroll"],
        "generated_at": now.isoformat(timespec="minutes"),
        "strategy_version": book["version"],
        "rules": C.rules(book_id),
        "model": {k: book[k] for k in ("sigma_by_lead_days", "bias", "fallback_vol", "asset",
                                       "fade_min_yes", "fade_max_yes") if k in book},
        "markets": list(book["series"]),
        "bankroll": round(book["bankroll"] + sum(float(t["pnl"]) for t in settled), 2),
        "open_exposure": round(sum(float(t["cost"]) for t in open_), 2),
        "totals": summarize(settled),
        "open_count": len(open_),
        "breakdowns": bd,
        "calibration": calibration(settled),
        "forecast_accuracy": acc,
        "suggestions": suggestions(settled, bd, acc),
        "bankroll_curve": bankroll_curve(settled, book["bankroll"]),
    }


def week_bounds(day: dt.date):
    start = day - dt.timedelta(days=day.weekday())
    return start, start + dt.timedelta(days=6)
