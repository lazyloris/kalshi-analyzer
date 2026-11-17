"""Does the Bitcoin favorite rule lose when BTC is already falling? (week-1 paper losses, 2026-11-13/14)
python -m kalshi_analyzer.backtest.trend_filter

Same trades as the verified finding: YES on every KXBTCD 5pm strike whose ask is 75-88c or 93-96c,
4h before close, spread <= 5c. For each trade, BTC's % change over the 24h before entry (Coinbase
hourly closes, keyed by candle end, so no look-ahead).
Pre-registered main filter (chosen before looking): SKIP when the 24h change is <= -3%.
Other cutoffs are shown for context only; picking the best one would be curve fitting.
Read-only, paper research.
"""
import datetime as dt
import json
import statistics
from collections import defaultdict

from .. import config as C
from . import data as D
from . import ladder as L

BANDS = ((0.75, 0.88), (0.93, 0.96))
HOURS = 4
MAIN_CUT = -0.03
CONTEXT_CUTS = (-0.02, -0.04, -0.05)
BUCKETS = ((-1, -0.05), (-0.05, -0.03), (-0.03, -0.01), (-0.01, 0.01), (0.01, 0.03), (0.03, 1))
OUT_MD = C.ROOT / "reports" / "trend_filter.md"
OUT_JSON = C.DASHBOARD_DATA / "trend_filter.json"


def trades_with_trend(data, closes):
    rows = []
    for lo, hi in BANDS:
        for t in L.ladder_trades(data, HOURS, lo, hi, "yes"):
            if not t["event"].endswith("17"):
                continue
            h = int(t["ts"]) // 3600 * 3600
            now, before = closes.get(h), closes.get(h - 86400)
            if now and before:
                rows.append({**t, "band": f"{lo:.2f}", "chg24": now / before - 1})
    return rows


def stats(rows):
    if not rows:
        return {"trades": 0}
    days = defaultdict(float)
    for r in rows:
        days[r["date"]] += r["pnl"]
    d = list(days.values())
    sd = statistics.stdev(d) if len(d) > 1 else 0
    staked = sum(r["cost"] for r in rows)
    def part(rs):
        s = sum(r["cost"] for r in rs)
        return round(sum(r["pnl"] for r in rs) / s, 4) if s else None
    return {"trades": len(rows), "days": len(d), "win_rate": round(statistics.fmean(r["won"] for r in rows), 3),
            "pnl": round(sum(r["pnl"] for r in rows), 2), "roi": round(sum(r["pnl"] for r in rows) / staked, 4),
            "losing_days": sum(1 for x in d if x < 0), "worst_day": round(min(d), 2),
            "t_day": round(statistics.fmean(d) / sd * len(d) ** 0.5, 2) if sd else None,
            "roi_older": part([r for r in rows if r["date"] < L.OOS_CUT]),
            "roi_newer": part([r for r in rows if r["date"] >= L.OOS_CUT])}


def run():
    data = D._load("kalshi_KXBTCD", None)
    if not data:
        raise SystemExit("no KXBTCD candle cache")
    dates = sorted(m["close_time"][:10] for m in data["markets"].values() if m.get("close_time"))
    start = dt.date.fromisoformat(dates[0]) - dt.timedelta(days=2)
    closes = D.coinbase_hourly("BTC-USD", start, dt.date.fromisoformat(dates[-1]))
    rows = trades_with_trend(data, closes)
    r = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"),
         "all": stats(rows),
         "main": {"cut": MAIN_CUT, "kept": stats([x for x in rows if x["chg24"] > MAIN_CUT]),
                  "skipped": stats([x for x in rows if x["chg24"] <= MAIN_CUT])},
         "context": {str(c): stats([x for x in rows if x["chg24"] > c]) for c in CONTEXT_CUTS},
         "buckets": {f"{lo:+.0%} to {hi:+.0%}": stats([x for x in rows if lo < x["chg24"] <= hi]) for lo, hi in BUCKETS}}
    r["calibration"] = calibrate(rows)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(r, indent=1))
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(markdown(r))
    D.log(f"wrote {OUT_MD}")
    return r


def calibrate(rows, span_days=60):
    """Kill-rule calibration: over every 60-day stretch of history, the worst drop from peak in
    running P&L, and how often 3 losing days landed within 10 trading days (the old rule)."""
    days = defaultdict(float)
    for r in rows:
        days[r["date"]] += r["pnl"]
    order = sorted(days)
    dds, trips = [], 0
    for i, start in enumerate(order):
        end = (dt.date.fromisoformat(start) + dt.timedelta(days=span_days)).isoformat()
        win = [d for d in order[i:] if d < end]
        if (dt.date.fromisoformat(order[-1]) - dt.date.fromisoformat(start)).days < span_days:
            break
        run = peak = dd = 0.0
        for d in win:
            run += days[d]; peak = max(peak, run); dd = max(dd, peak - run)
        dds.append(dd)
        trips += any(sum(1 for d in win[j:j + 10] if days[d] < 0) >= 3 for j in range(len(win)))
    dds.sort()
    q = lambda f: round(dds[min(len(dds) - 1, int(f * len(dds)))], 2) if dds else None
    return {"windows": len(dds), "old_rule_trip_rate": round(trips / len(dds), 3) if dds else None,
            "max_drawdown_p50": q(0.5), "p90": q(0.9), "p95": q(0.95), "p99": q(0.99), "max": dds[-1] if dds else None,
            "daily_pnl": {d: round(days[d], 2) for d in order}}


def _p(v):
    return "n/a" if v is None else f"{v:+.1%}"


def markdown(r):
    head = "| Set | Trades | Days | Win | P&L | Return/$ | Older | Newer | Losing days | Worst day | t (day) |\n|---|---|---|---|---|---|---|---|---|---|---|"
    def line(name, s):
        if not s.get("trades"):
            return f"| {name} | 0 | | | | | | | | | |"
        return (f"| {name} | {s['trades']} | {s['days']} | {s['win_rate']:.0%} | ${s['pnl']} | {_p(s['roi'])} | "
                f"{_p(s['roi_older'])} | {_p(s['roi_newer'])} | {s['losing_days']} | ${s['worst_day']} | {s['t_day']} |")
    out = [f"# Bitcoin favorite: falling-market filter ({r['generated_at']})", "",
           "Main test, picked before looking: skip the day when BTC is down 3% or more over the 24h before entry.", "",
           head, line("All trades (no filter)", r["all"]), line("Kept (filter on)", r["main"]["kept"]),
           line("Skipped (down >=3%)", r["main"]["skipped"]), "", "## Other cutoffs (context only, don't pick the best)", "", head]
    out += [line(f"Skip when down >= {-float(c):.0%}", s) for c, s in r["context"].items()]
    c = r.get("calibration") or {}
    out += ["", "## Kill-rule calibration (60-day stretches of history)", "",
            f"Windows: {c.get('windows')}. Old rule (3 losing days in 10) would have tripped in {c.get('old_rule_trip_rate')} of them.",
            f"Worst drop from peak per window: median ${c.get('max_drawdown_p50')}, 90th ${c.get('p90')}, 95th ${c.get('p95')}, 99th ${c.get('p99')}, max ${c.get('max')}."]
    out += ["", "## By BTC 24h change", "", head] + [line(k, s) for k, s in r["buckets"].items()] + [""]
    return "\n".join(out)


if __name__ == "__main__":
    run()
