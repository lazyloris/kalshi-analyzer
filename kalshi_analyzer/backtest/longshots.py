"""Two Kalshi-only candidates from the 2026-11-17 Fable review (project note kalshi/review-2026-11-17.md).
python -m kalshi_analyzer.backtest.longshots [fills|rain|all] [--budget 240]

fills (candidate 1): sell temperature long shots with a resting order the evening before.
  Rule, fixed before looking: at 8pm ET the evening before the target day, for every daily high/low
  range whose YES ask is 2-12c with a spread <= 3c, post a sell of YES at that ask (= buy NO at
  1 - ask). $10 per order, at most 2 ranges per city per day (the two highest asks). Hold to settlement.
  Fill, fixed before looking: we're last in line. Count taker-YES trades at or above our price
  after we post; our order fills once that count passes Q = 2,000 contracts (500 and 5,000 also shown).
  All-or-nothing. Orders posted later don't count.
  Mirror: P&L of every taker-YES buy at <= 12c placed 18h+ before close (their loss = sellers' gain).
  Pass: at Q=2,000, >= +1.0%/$ after fees, positive in the older and newer years, city-day t >= 3.5,
  and >= 30% of orders filled.
rain (candidate 2): KXRAIN, 24h before close, mid = (bid+ask)/2, spread <= 6c.
  NO at 1 - bid if 5c <= mid < 45c; YES at the ask if 85c <= mid < 97c. Taker fee, $10, hold.
  Pass: >= 120 days, >= +3%/$, both legs positive, both halves positive, 3 of 4 seasons if a year
  exists, day-level t >= 3.5. Spread <= 2c subset reported separately.
Read-only, paper research.
"""
import argparse
import datetime as dt
import json
import math
import statistics
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from zoneinfo import ZoneInfo

from .. import config as C
from ..http import get_json
from ..model import taker_fee
from . import data as D
from . import engine as E
from . import fav_extra as F

CUT = "2026-03-13"
ET = ZoneInfo("America/New_York")
SERIES = {**C.BOOKS["weather_high"]["series"], **C.BOOKS["weather_low"]["series"]}
ASK_LO, ASK_HI, MAX_SPREAD, PER_CITY_DAY, STAKE = 0.02, 0.12, 0.03, 2, 10.0
QS = (2000, 500, 5000)
OUT_MD = C.ROOT / "reports" / "longshots.md"
OUT_JSON = C.DASHBOARD_DATA / "longshots.json"
MONTHS = {m: i + 1 for i, m in enumerate(["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"])}


def target_day(event):
    s = event.split("-")[1][:7]                       # e.g. 26NOV17
    return dt.date(2000 + int(s[:2]), MONTHS[s[2:5]], int(s[5:7]))


def maker_fee(n, p, fee_type):
    # "quadratic" = taker-only fees; anything else, charge Kalshi's maker rate to be safe
    return 0.0 if fee_type == "quadratic" else math.ceil(0.0175 * n * p * (1 - p) * 100 - 1e-9) / 100


def fee_types():
    out = {}
    for s in SERIES:
        try:
            out[s] = (get_json(f"{C.KALSHI_API}/series/{s}", {}).get("series") or {}).get("fee_type") or "unknown"
        except Exception as e:
            D.log(f"fee type {s}: {e}")
            out[s] = "unknown"
    return out


def orders(series, data, entry_fn):
    """Orders a rule would post: one per qualifying range, max 2 per city-day (highest asks)."""
    by_event = defaultdict(list)
    for t, cs in data["candles"].items():
        m = data["markets"].get(t)
        if not m or m["result"] not in ("yes", "no") or not m.get("close_time"):
            continue
        close = F._ts(m["close_time"])
        entry = entry_fn(m, close)
        if entry is None or entry >= close:
            continue
        q = E.quote(cs, entry, max_age_h=1)
        if not q or q[0] <= 0 or not (ASK_LO <= q[1] <= ASK_HI) or q[1] - q[0] > MAX_SPREAD:
            continue
        by_event[m["event_ticker"]].append({"series": series, "ticker": t, "event": m["event_ticker"], "entry": entry,
                                             "close": close, "ask": q[1], "won_yes": m["result"] == "yes",
                                             "source": m["source"], "day": target_day(m["event_ticker"]).isoformat()})
    out = []
    for ev, rows in by_event.items():
        out += sorted(rows, key=lambda r: -r["ask"])[:PER_CITY_DAY]
    return out


def entry_8pm(m, close):
    d = target_day(m["event_ticker"]) - dt.timedelta(days=1)
    return int(dt.datetime(d.year, d.month, d.day, 20, tzinfo=ET).timestamp())


def entry_24h(m, close):
    return close - 24 * 3600


def fetch_trades(cands, budget_min, workers=6):
    cache = D._load("trades_longshots", {})
    deadline = time.time() + budget_min * 60
    todo = sorted({(c["ticker"], c["close"], c["source"]) for c in cands if c["ticker"] not in cache})
    D.log(f"{len(todo)} markets need trades ({len(cache)} cached)")

    def job(x):
        t, close, src = x
        return t, F.market_trades(t, close - 40 * 3600, close, src == "historical")

    with ThreadPoolExecutor(workers) as ex:
        for i in range(0, len(todo), 300):
            if time.time() > deadline:
                D.log("  trade budget used up; the next run continues")
                break
            for t, rows in ex.map(job, todo[i:i + 300]):
                cache[t] = rows
            D._save("trades_longshots", cache)
            D.log(f"  trades {min(i + 300, len(todo))}/{len(todo)}")
    D._save("trades_longshots", cache)
    return cache, max(0, len(todo) - sum(1 for t, _, _ in todo if t in cache))


def simulate(cands, trades, q, fees):
    rows = []
    for c in cands:
        tr = trades.get(c["ticker"])
        if tr is None:
            continue
        cum, filled = 0.0, False
        for ts, p, n, side in tr:
            if ts > c["entry"] and ts <= c["close"] and side == "yes" and p >= c["ask"] - 1e-9:
                cum += n
                if cum > q:
                    filled = True
                    break
        price = 1 - c["ask"]
        k = math.floor(STAKE / price)
        cost = k * price + maker_fee(k, price, fees.get(c["series"], "unknown"))
        pnl = ((0 if c["won_yes"] else k) - cost) if filled else 0.0
        rows.append({**c, "filled": filled, "cost": cost if filled else 0.0, "pnl": round(pnl, 4)})
    return rows


def _t(vals):
    sd = statistics.stdev(vals) if len(vals) > 1 else 0
    return round(statistics.fmean(vals) / sd * math.sqrt(len(vals)), 2) if sd else None


def summarize(rows, date_key="day"):
    f = [r for r in rows if r.get("filled", True)]
    if not f:
        return {"orders": len(rows), "filled": 0}
    staked = sum(r["cost"] for r in f)
    cityday, day = defaultdict(float), defaultdict(float)
    for r in f:
        cityday[(r["series"], r[date_key])] += r["pnl"]
        day[r[date_key]] += r["pnl"]
    roi = lambda rs: round(sum(r["pnl"] for r in rs) / s, 4) if (s := sum(r["cost"] for r in rs)) else None
    run = pk = dd = 0.0
    for d in sorted(day):
        run += day[d]; pk = max(pk, run); dd = max(dd, pk - run)
    return {"orders": len(rows), "filled": len(f), "fill_rate": round(len(f) / len(rows), 3),
            "win_rate": round(statistics.fmean(r["pnl"] > 0 for r in f), 3), "pnl": round(sum(r["pnl"] for r in f), 2),
            "roi": round(sum(r["pnl"] for r in f) / staked, 4), "t_cityday": _t(list(cityday.values())),
            "t_day": _t(list(day.values())), "days": len(day), "losing_days": sum(v < 0 for v in day.values()),
            "worst_day": round(min(day.values()), 2), "max_drawdown": round(dd, 2),
            "roi_older": roi([r for r in f if r[date_key] < CUT]), "roi_newer": roi([r for r in f if r[date_key] >= CUT])}


def mirror(cands, trades):
    out = {"older": [0.0, 0.0], "newer": [0.0, 0.0]}
    seen = set()
    for c in cands:
        if c["ticker"] in seen or c["ticker"] not in trades:
            continue
        seen.add(c["ticker"])
        k = "older" if c["day"] < CUT else "newer"
        for ts, p, n, side in trades[c["ticker"]]:
            if side == "yes" and p <= 0.12 and ts <= c["close"] - 18 * 3600:
                out[k][0] += n * ((1.0 if c["won_yes"] else 0.0) - p)
                out[k][1] += n * p
    return {k: {"buyers_pnl": round(v[0], 2), "buyers_spent": round(v[1], 2), "buyers_roi": round(v[0] / v[1], 4) if v[1] else None}
            for k, v in out.items()}


def fills(budget_min=240):
    fees = fee_types()
    D.log(f"fee types: {fees}")
    main, ctx = [], []
    for s in SERIES:
        data = D._load(f"kalshi_{s}", None)
        if not data:
            D.log(f"{s}: no candle cache")
            continue
        main += orders(s, data, entry_8pm)
        ctx += orders(s, data, entry_24h)
    D.log(f"orders: {len(main)} at 8pm ET, {len(ctx)} at 24h")
    trades, missing = fetch_trades(main + ctx, budget_min)
    res = {"fee_types": fees, "missing_markets": missing,
           "main": {str(q): summarize(simulate(main, trades, q, fees)) for q in QS},
           "context_24h": {str(q): summarize(simulate(ctx, trades, q, fees)) for q in QS},
           "mirror": mirror(main, trades)}
    m = res["main"]["2000"]
    res["pass"] = bool(m.get("filled") and (m["roi"] or 0) >= 0.01 and (m["roi_older"] or 0) > 0 and (m["roi_newer"] or 0) > 0
                       and (m["t_cityday"] or 0) >= 3.5 and m["fill_rate"] >= 0.30)
    return res


# ---------------------------------------------------------------- rain

def rain_rows(data, hours=24, max_spread=0.06):
    out = []
    for t, cs in data["candles"].items():
        m = data["markets"].get(t)
        if not m or m["result"] not in ("yes", "no") or not m.get("close_time"):
            continue
        close = F._ts(m["close_time"])
        q = E.quote(cs, close - hours * 3600, max_age_h=1)
        if not q or q[0] <= 0 or q[1] >= 1 or q[1] - q[0] > max_spread:
            continue
        b, a = q[0], q[1]
        mid, won = (a + b) / 2, m["result"] == "yes"
        day = dt.datetime.fromtimestamp(close, dt.timezone.utc).astimezone(ET).date().isoformat()
        if 0.05 <= mid < 0.45:
            leg, price, wins = "NO", 1 - b, not won
        elif 0.85 <= mid < 0.97:
            leg, price, wins = "YES", a, won
        else:
            continue
        k = math.floor(STAKE / price)
        cost = k * price + taker_fee(k, price, C.FEE_RATE)
        out.append({"series": t.split("-")[-1], "ticker": t, "day": day, "leg": leg, "spread": round(a - b, 3),
                    "cost": cost, "pnl": round((k if wins else 0) - cost, 4)})
    return out


def season(d):
    return {12: "winter", 1: "winter", 2: "winter", 3: "spring", 4: "spring", 5: "spring",
            6: "summer", 7: "summer", 8: "summer"}.get(int(d[5:7]), "autumn")


def rain(budget_min=120):
    since = dt.date(2024, 1, 1)
    data = D.kalshi_series("KXRAIN", since, workers=6, deadline=time.time() + budget_min * 60)
    rows = rain_rows(data)
    days = sorted({r["day"] for r in rows})
    half = days[len(days) // 2] if days else ""
    s = summarize([dict(r, filled=True) for r in rows])
    roi = lambda rs: round(sum(r["pnl"] for r in rs) / c, 4) if (c := sum(r["cost"] for r in rs)) else None
    seasons = {k: roi([r for r in rows if season(r["day"]) == k]) for k in ("winter", "spring", "summer", "autumn")}
    res = {"markets": len(data["markets"]), "with_candles": len(data["candles"]), "all": s,
           "first_day": days[0] if days else None, "last_day": days[-1] if days else None,
           "halves": [roi([r for r in rows if r["day"] < half]), roi([r for r in rows if r["day"] >= half])],
           "legs": {k: roi([r for r in rows if r["leg"] == k]) for k in ("NO", "YES")},
           "seasons": seasons, "tight_spread_2c": summarize([dict(r, filled=True) for r in rows if r["spread"] <= 0.02]),
           "cities_positive": f"{sum((roi(v) or 0) > 0 for v in _group(rows).values())}/{len(_group(rows))}"}
    full_year = days and (dt.date.fromisoformat(days[-1]) - dt.date.fromisoformat(days[0])).days >= 365
    ok_seasons = sum((v or 0) > 0 for v in seasons.values() if v is not None) >= 3 if full_year else True
    res["pass"] = bool(s.get("days", 0) >= 120 and (s.get("roi") or 0) >= 0.03 and all((v or 0) > 0 for v in res["legs"].values())
                       and all((v or 0) > 0 for v in res["halves"]) and ok_seasons and (s.get("t_day") or 0) >= 3.5)
    return res


def _group(rows):
    g = defaultdict(list)
    for r in rows:
        g[r["series"]].append(r)
    return g


# ---------------------------------------------------------------- report

def _p(v):
    return "n/a" if v is None else f"{v:+.1%}"


def markdown(r):
    out = [f"# Kalshi long-shot candidates ({r['generated_at']})", ""]
    f = r.get("fills")
    if f:
        out += ["## Candidate 1: sell temperature long shots the evening before (resting order)", "",
                f"Fee types: {f['fee_types']}. Markets still missing trades: {f['missing_markets']} (0 = complete).",
                f"**Pass (set before looking): {'YES' if f['pass'] else 'NO'}**", "",
                "| Entry | Fill rule | Orders | Filled | Fill % | Win | P&L | Return/$ | Older | Newer | t city-day | t day | Losing days | Worst day | Max drawdown |",
                "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for lab, key in (("8pm ET (main)", "main"), ("24h (context)", "context_24h")):
            for q, s in f[key].items():
                if not s.get("filled"):
                    out.append(f"| {lab} | {q} | {s['orders']} | 0 | | | | | | | | | | | |")
                    continue
                out.append(f"| {lab} | last in line after {q} | {s['orders']} | {s['filled']} | {s['fill_rate']:.0%} | {s['win_rate']:.1%} | ${s['pnl']} | "
                           f"{_p(s['roi'])} | {_p(s['roi_older'])} | {_p(s['roi_newer'])} | {s['t_cityday']} | {s['t_day']} | {s['losing_days']} | ${s['worst_day']} | ${s['max_drawdown']} |")
        mi = f["mirror"]
        out += ["", "Mirror (no fill assumptions): everyone who bought YES at 12c or less, 18h+ before close, on these markets:",
                f"older year: buyers lost {_p(mi['older']['buyers_roi'])} on ${mi['older']['buyers_spent']}; newer: {_p(mi['newer']['buyers_roi'])} on ${mi['newer']['buyers_spent']}.", ""]
    rn = r.get("rain")
    if rn:
        s = rn["all"]
        out += ["## Candidate 2: rain market, 24h before close (taker)", "",
                f"{rn['markets']} markets, {rn['with_candles']} with candles, {rn['first_day']} to {rn['last_day']}.",
                f"**Pass (set before looking): {'YES' if rn['pass'] else 'NO'}**", ""]
        if s.get("filled"):
            out += [f"All: {s['filled']} trades over {s['days']} days, win {s['win_rate']:.0%}, P&L ${s['pnl']}, return {_p(s['roi'])}, "
                    f"t (day) {s['t_day']}, losing days {s['losing_days']}, worst day ${s['worst_day']}, max drawdown ${s['max_drawdown']}.",
                    f"Halves: {_p(rn['halves'][0])} / {_p(rn['halves'][1])}. Legs: NO {_p(rn['legs']['NO'])}, YES {_p(rn['legs']['YES'])}.",
                    "Seasons: " + ", ".join(f"{k} {_p(v)}" for k, v in rn["seasons"].items()) + f". Cities positive: {rn['cities_positive']}."]
            t2 = rn["tight_spread_2c"]
            if t2.get("filled"):
                out.append(f"Spread <= 2c only: {t2['filled']} trades, return {_p(t2['roi'])}, t (day) {t2['t_day']}.")
    return "\n".join(out + [""])


def run(cmd="all", budget=240):
    r = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes")}
    if cmd in ("rain", "all"):
        r["rain"] = rain(budget if cmd == "rain" else budget * 0.3)
    if cmd in ("fills", "all"):
        r["fills"] = fills(budget if cmd == "fills" else budget * 0.7)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(r, indent=1, default=str))
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(markdown(r))
    D.log(f"wrote {OUT_MD}")
    return r


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="all", choices=["fills", "rain", "all"])
    ap.add_argument("--budget", type=int, default=240)
    a = ap.parse_args()
    run(a.cmd, a.budget)
