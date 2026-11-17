"""Does the Bitcoin favorite rule work at other close times, not just 5pm ET?
python -m kalshi_analyzer.backtest.other_hours [--days 365] [--budget 240]

Exact same rule as the 5pm finding, picked before looking: YES on every KXBTCD strike whose ask is
75-88c or 93-96c, 4h before close, spread <= 5c, $10 flat. Hours tested: 10am, 1pm and 9pm ET
(event suffixes 10, 13, 21), plus 5pm (17) re-fetched the same way as a control.
Candles are only downloaded for strikes within 7% of the SAME hour's settle one day earlier
(known before entry), so the strike choice has no look-ahead.
Pass = positive return per $ in both the older (before 2026-03-13) and newer halves at that hour.
Own cache file (btc_hours), so other backtests' KXBTCD data is untouched. Read-only, paper research.
"""
import argparse
import datetime as dt
import json
import math
import time
from concurrent.futures import ThreadPoolExecutor

from .. import config as C
from ..model import taker_fee
from . import engine as E
from . import data as D
from . import ladder as L
from . import trend_filter as T

HOURS = ("10", "13", "21", "17")
BAND = 0.07
OUT_MD = C.ROOT / "reports" / "other_hours.md"
OUT_JSON = C.DASHBOARD_DATA / "other_hours.json"


def fetch(days, budget_min, workers=6):
    deadline = time.time() + budget_min * 60
    cache = D._load("btc_hours", {"markets": {}, "candles": {}, "events": {}})
    end = dt.date.today() - dt.timedelta(days=1)
    start = end - dt.timedelta(days=days)
    for h in HOURS:
        evs = D.btc_event_tickers(start, end, suffix=h)
        todo = [e for e in evs if e not in cache["events"]]
        D.log(f"hour {h}: {len(evs)} events, {len(todo)} to list")
        def lst(e):
            try:
                return e, D.settled_markets(event_ticker=e)
            except Exception as ex:
                D.log(f"  {e}: {ex}")
                return e, None
        with ThreadPoolExecutor(workers) as ex:
            for e, rows in ex.map(lst, todo):
                if rows is None:
                    continue
                cache["events"][e] = (rows[0].get("value") if rows else "") or ""
                for r in rows:
                    cache["markets"][r["ticker"]] = r
                if time.time() > deadline:
                    break
        D._save("btc_hours", cache)
    # strikes near the same hour's settle one day earlier
    def prev_settle(ev):
        d = dt.datetime.strptime(ev.split("-")[1][:7], "%y%b%d").date() - dt.timedelta(days=1)
        p = D.btc_event_tickers(d, d, suffix=ev[-2:])[0]
        try:
            return float(cache["events"].get(p) or "nan")
        except ValueError:
            return float("nan")
    want = []
    for t, m in cache["markets"].items():
        if t in cache["candles"] or m["result"] not in ("yes", "no"):
            continue
        ref, k = prev_settle(m["event_ticker"]), m.get("floor") or m.get("cap")
        if k and ref == ref and abs(float(k) / ref - 1) <= BAND:
            want.append(m)
    D.log(f"{len(want)} strikes need candles")
    def job(m):
        try:
            return m["ticker"], D.candles("KXBTCD", m, hours_before=6)
        except Exception as ex:
            D.log(f"  candles {m['ticker']}: {ex}")
            return m["ticker"], None
    done = 0
    with ThreadPoolExecutor(workers) as ex:
        for i in range(0, len(want), 500):
            if time.time() > deadline:
                D.log(f"time budget used up at {done}/{len(want)}; the next run continues")
                break
            for t, cs in ex.map(job, want[i:i + 500]):
                if cs is not None:
                    cache["candles"][t] = cs
                done += 1
            D._save("btc_hours", cache)
            D.log(f"  candles {done}/{len(want)}")
    D._save("btc_hours", cache)
    return cache, len(want) - done


def upside_no(sub, hours=4, lo=0.03, hi=0.12, max_spread=0.03):
    """Fable's crypto upside rule (review 2026-11-17, section 8): 4h before close, buy NO at 1 - yes_bid
    on every 'greater' strike whose YES bid is 3-12c with spread <= 3c; taker fee; $10; hold."""
    out = []
    for t, cs in sub["candles"].items():
        m = sub["markets"].get(t)
        if not m or m["result"] not in ("yes", "no") or m.get("strike_type") != "greater":
            continue
        close = L._ts(m["close_time"])
        q = E.quote(cs, close - hours * 3600, max_age_h=1)
        if not q or q[1] >= 1 or q[1] - q[0] > max_spread + 1e-9 or not (lo <= q[0] < hi):
            continue
        price = 1 - q[0]
        n = math.floor(10 / price)
        cost = n * price + taker_fee(n, price, C.FEE_RATE)
        won = m["result"] == "no"
        out.append({"event": m["event_ticker"], "ticker": t, "cost": round(cost, 4), "won": won,
                    "pnl": round((n if won else 0) - cost, 4),
                    "date": dt.datetime.fromtimestamp(close, dt.timezone.utc).date().isoformat()})
    return out


def diagnose(cache):
    """Per hour: markets with candles, how many are non-empty, and how early before close the first candle is."""
    out = {}
    for h in HOURS:
        tk = [t for t, m in cache["markets"].items() if m["event_ticker"].endswith(h) and t in cache["candles"]]
        ne = [t for t in tk if cache["candles"][t]]
        leads = sorted((L._ts(cache["markets"][t]["close_time"]) - cache["candles"][t][0][0]) / 3600 for t in ne)
        two = [t for t in ne if any(c[1] is not None and c[2] is not None for c in cache["candles"][t])]
        out[h] = {"with_candles": len(tk), "non_empty": len(ne), "two_sided": len(two),
                  "first_candle_hours_before_close_median": leads[len(leads) // 2] if leads else None,
                  "max": leads[-1] if leads else None}
    return out


def score(cache):
    res = {}
    for h in HOURS:
        sub = {"markets": {t: m for t, m in cache["markets"].items() if m["event_ticker"].endswith(h)},
               "candles": {t: c for t, c in cache["candles"].items() if cache["markets"].get(t, {}).get("event_ticker", "").endswith(h)}}
        rows = []
        for lo, hi in T.BANDS:
            rows += L.ladder_trades(sub, T.HOURS, lo, hi, "yes")
        s = T.stats(rows)
        s["pass"] = bool(s.get("trades") and (s.get("roi_older") or 0) > 0 and (s.get("roi_newer") or 0) > 0)
        u = upside_no(sub)
        s["upside"] = T.stats(u)
        s["_upside_rows"] = u
        res[h] = s
    pooled = [r for h in HOURS if h != "17" for r in res[h].pop("_upside_rows")]
    res["17"].pop("_upside_rows", None)
    p = T.stats(pooled)
    ctrl = res["17"]["upside"]
    p["pass"] = bool(p.get("trades") and (p["roi"] or 0) >= 0.015 and (p["t_day"] or 0) >= 3 and (p["roi_older"] or 0) > 0
                     and (p["roi_newer"] or 0) > 0 and (ctrl.get("roi") or 0) >= 0.02)
    res["upside_pooled_other_hours"] = p
    return res


def markdown(r):
    head = "| Close (ET) | Trades | Days | Win | P&L | Return/$ | Older | Newer | Losing days | Worst day | t (day) | Pass |\n|---|---|---|---|---|---|---|---|---|---|---|---|"
    out = [f"# Bitcoin favorite rule at other close times ({r['generated_at']})", "",
           "Same rule as 5pm, picked before looking. Pass = positive in both older and newer halves.",
           f"Strikes still missing candles: {r['missing']} (0 = complete).",
           f"Diagnostics: {r.get('diagnose')}", "", head]
    for h, s in ((k, v) for k, v in r["hours"].items() if k in HOURS):
        if not s.get("trades"):
            out.append(f"| {h}:00 | 0 | | | | | | | | | | |")
            continue
        out.append(f"| {h}:00{' (control)' if h == '17' else ''} | {s['trades']} | {s['days']} | {s['win_rate']:.0%} | ${s['pnl']} | "
                   f"{T._p(s['roi'])} | {T._p(s['roi_older'])} | {T._p(s['roi_newer'])} | {s['losing_days']} | ${s['worst_day']} | {s['t_day']} | {'yes' if s['pass'] else 'no'} |")
    out += ["", "## Fable's upside rule: buy NO on 'greater' strikes with YES bid 3-12c, 4h before close (BTC only)", "",
            "Pass (set before looking): other hours pooled >= +1.5%/$, t (day) >= 3, older and newer positive, and the 5pm control >= +2%.", "",
            "| Close (ET) | Trades | Days | Win | P&L | Return/$ | Older | Newer | Losing days | Worst day | t (day) |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    rows = [(f"{h}:00" + (" (control)" if h == "17" else ""), r["hours"][h]["upside"]) for h in HOURS]
    rows.append(("Other hours pooled", r["hours"]["upside_pooled_other_hours"]))
    for name, s in rows:
        if not s.get("trades"):
            out.append(f"| {name} | 0 | | | | | | | | | |")
            continue
        out.append(f"| {name} | {s['trades']} | {s['days']} | {s['win_rate']:.1%} | ${s['pnl']} | {T._p(s['roi'])} | {T._p(s['roi_older'])} | "
                   f"{T._p(s['roi_newer'])} | {s['losing_days']} | ${s['worst_day']} | {s['t_day']} |")
    out.append(f"**Upside rule pass: {'YES' if r['hours']['upside_pooled_other_hours'].get('pass') else 'NO'}**")
    return "\n".join(out + [""])


def run(days=365, budget=240):
    cache, missing = fetch(days, budget)
    r = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"), "missing": max(0, missing), "hours": score(cache), "diagnose": diagnose(cache)}
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(r, indent=1))
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(markdown(r))
    D.log(f"wrote {OUT_MD}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=600)
    ap.add_argument("--budget", type=int, default=240)
    a = ap.parse_args()
    run(a.days, a.budget)
