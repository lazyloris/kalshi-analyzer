"""Two follow-ups to the Bitcoin favorite finding (docs/review-2026-11-10.md, C2.2 and C2.7).
python -m kalshi_analyzer.backtest.fav_extra [maker|assets|all]

maker: instead of paying the ask, rest a YES bid a few cents lower at the entry time. Kalshi's
       public trade feed (/markets/trades, /historical/trades) says whether someone later traded
       at or below our price. "Through" = a trade printed BELOW our bid (we'd surely be filled);
       "touch" = a trade at our bid where the taker sold (we'd be filled if first in line).
       Only trades after the entry time count. Missed fills earn nothing, so the fair comparison
       is total P&L per opportunity, not per fill.
assets: the same no-model ladder test (ladder.py) on other Kalshi daily price markets. Strikes are
       chosen near the PREVIOUS event's settlement value (known before entry), so no look-ahead.
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

from .. import config as C
from ..http import get_json
from ..model import taker_fee
from . import data as D
from . import engine as E
from . import ladder as L

K = C.KALSHI_API
OUT_MD = C.ROOT / "reports" / "fav_extra.md"
OUT_JSON = C.DASHBOARD_DATA / "fav_extra.json"
BANDS = ((0.75, 0.88), (0.93, 0.96))
MAKER_FEE = 0.0175  # Kalshi's maker fee on series that charge one; the review found KXBTCD charges none

# Daily price ladders besides Bitcoin. band = strikes within this fraction of the last settle.
OTHER = {"KXETHD": 0.06, "KXGOLDD": 0.03, "KXSILVERD": 0.05, "KXWTI": 0.05, "KXBRENTD": 0.05,
         "KXNATGASD": 0.08, "KXINXU": 0.03, "KXINX": 0.03, "KXNASDAQ100U": 0.03, "KXNASDAQ100": 0.03,
         "KXSOLD": 0.08, "KXXRPD": 0.08, "KXDOGED": 0.08}


def _ts(iso):
    return int(dt.datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp())


def _num(v):
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------- maker test

def trade_rows(raw):
    """Kalshi trade objects -> [ts, yes_price (0-1), count, taker_side]."""
    out = []
    for t in raw:
        p = _num(t.get("yes_price_dollars"))
        if p is None:
            p = _num(t.get("yes_price"))
            if p is not None and p > 1:
                p /= 100
        n = _num(t.get("count_fp")) or _num(t.get("count")) or 0
        if p is None or not t.get("created_time"):
            continue
        out.append([_ts(t["created_time"]), p, n, t.get("taker_side") or ""])
    return sorted(out)


def market_trades(ticker, start, end, historical=False):
    urls = [f"{K}/markets/trades", f"{K}/historical/trades"]
    if historical:
        urls.reverse()
    for u in urls:
        out, cursor = [], None
        try:
            while True:
                p = {"ticker": ticker, "min_ts": start, "max_ts": end, "limit": 1000}
                if cursor:
                    p["cursor"] = cursor
                data = get_json(u, p, retries=4)
                out += data.get("trades") or []
                cursor = data.get("cursor")
                if not cursor or not data.get("trades"):
                    break
        except Exception:
            continue
        if out:
            return trade_rows(out)
    return []


def candidates(data, hours=(4, 3)):
    """Markets whose YES ask sits in a favorite band at an entry time (same filter as ladder.py)."""
    out = []
    for ticker, cs in data["candles"].items():
        m = data["markets"].get(ticker)
        if not m or m["result"] not in ("yes", "no") or not m.get("close_time"):
            continue
        close = _ts(m["close_time"])
        for h in hours:
            q = E.quote(cs, close - h * 3600, max_age_h=1)
            if q and q[1] - q[0] <= 0.05 and any(lo <= q[1] < hi for lo, hi in BANDS):
                out.append({"ticker": ticker, "event": m["event_ticker"], "close": close, "hours": h,
                            "bid": q[0], "ask": q[1], "won": m["result"] == "yes", "source": m["source"],
                            "date": dt.datetime.fromtimestamp(close, dt.timezone.utc).date().isoformat()})
    return out


def fetch_trades(series, cands, workers=4, budget_min=150):
    name = f"trades_fav_{series}"
    cache = D._load(name, {})
    deadline = time.time() + budget_min * 60
    todo = sorted({(c["ticker"], c["close"], c["source"]) for c in cands if c["ticker"] not in cache})
    D.log(f"{series}: {len(todo)} markets need trades ({len(cache)} cached)")

    def job(x):
        t, close, src = x
        return t, market_trades(t, close - 5 * 3600, close, src == "historical")

    with ThreadPoolExecutor(workers) as ex:
        for i in range(0, len(todo), 200):
            if time.time() > deadline:
                D.log("  trade budget used up; next run continues")
                break
            for t, rows in ex.map(job, todo[i:i + 200]):
                cache[t] = rows
            D._save(name, cache)
            D.log(f"  trades {min(i + 200, len(todo))}/{len(todo)}")
    D._save(name, cache)
    return cache


def maker_sim(cands, trades, offset, rule="through", expire_h=None, maker_fee=0.0, stake=E.STAKE):
    """Rest a YES bid at ask - offset at entry; filled per `rule` before expiry (default: 30 min before close)."""
    out = []
    for c in cands:
        tr = trades.get(c["ticker"])
        if tr is None:
            continue
        price = round(c["ask"] - offset, 2)
        if price <= 0:
            continue
        entry = c["close"] - c["hours"] * 3600
        stop = entry + expire_h * 3600 if expire_h else c["close"] - 1800
        n = max(1, math.floor(stake / price))
        filled = False
        for ts, p, cnt, side in tr:
            if ts <= entry or ts > stop:
                continue
            if (rule == "through" and p < price - 1e-9) or (rule == "touch" and p <= price + 1e-9 and side == "no"):
                filled = True
                break
        pnl = 0.0
        cost = n * price + (math.ceil(maker_fee * n * price * (1 - price) * 100 - 1e-9) / 100 if maker_fee else 0)
        if filled:
            pnl = (n if c["won"] else 0) - cost
        out.append({**c, "filled": filled, "price": price, "cost": cost if filled else 0.0, "pnl": round(pnl, 4)})
    return out


def taker_sim(cands, stake=E.STAKE):
    out = []
    for c in cands:
        n = max(1, math.floor(stake / c["ask"]))
        cost = n * c["ask"] + taker_fee(n, c["ask"], C.FEE_RATE)
        out.append({**c, "filled": True, "price": c["ask"], "cost": cost, "pnl": round((n if c["won"] else 0) - cost, 4)})
    return out


def score(rows):
    filled = [r for r in rows if r["filled"]]
    if not rows:
        return None
    g = defaultdict(float)
    for r in rows:
        g[r["event"]] += r["pnl"]
    days = list(g.values())
    sd = statistics.stdev(days) if len(days) > 1 else 0
    staked = sum(r["cost"] for r in filled)
    return {"opportunities": len(rows), "fills": len(filled), "fill_rate": round(len(filled) / len(rows), 3),
            "win_rate_filled": round(statistics.fmean(r["won"] for r in filled), 3) if filled else None,
            "win_rate_all": round(statistics.fmean(r["won"] for r in rows), 3),
            "pnl": round(sum(r["pnl"] for r in rows), 2), "roi": round(sum(r["pnl"] for r in rows) / staked, 4) if staked else None,
            "t_day": round(statistics.fmean(days) / sd * math.sqrt(len(days)), 2) if sd else None,
            "older": round(sum(r["pnl"] for r in rows if r["date"] < L.OOS_CUT), 1),
            "newer": round(sum(r["pnl"] for r in rows if r["date"] >= L.OOS_CUT), 1)}


def maker(series=("KXBTCD", "KXETHD"), budget_min=150):
    res = {}
    for s in series:
        data = D._load(f"kalshi_{s}", None)
        if not data:
            D.log(f"{s}: no candle cache, skipping")
            continue
        cands = candidates(data)
        trades = fetch_trades(s, cands, budget_min=budget_min / len(series))
        have = [c for c in cands if c["ticker"] in trades]
        rows = []
        for h in (4, 3):
            for lo, hi in BANDS:
                cs = [c for c in have if c["hours"] == h and lo <= c["ask"] < hi]
                if not cs:
                    continue
                base = {"hours": h, "band": f"{lo * 100:.0f}-{hi * 100:.0f}c"}
                rows.append({**base, "how": "taker (buy at ask)", **score(taker_sim(cs))})
                for off in (0.01, 0.02, 0.03):
                    for rule in ("through", "touch"):
                        rows.append({**base, "how": f"bid ask-{off * 100:.0f}c, {rule}", **score(maker_sim(cs, trades, off, rule))})
                    rows.append({**base, "how": f"bid ask-{off * 100:.0f}c, through, 1h expiry",
                                 **score(maker_sim(cs, trades, off, "through", expire_h=1))})
                rows.append({**base, "how": "bid ask-2c, through, with 1.75% maker fee",
                             **score(maker_sim(cs, trades, 0.02, "through", maker_fee=MAKER_FEE))})
        res[s] = {"candidates": len(cands), "with_trades": len(have), "rows": rows}
    return res


# ---------------------------------------------------------------- other assets

def fetch_assets(days=400, budget_min=120, workers=4):
    deadline = time.time() + budget_min * 60
    since = dt.date.today() - dt.timedelta(days=days)
    out = {}
    for s, band in OTHER.items():
        if time.time() > deadline:
            D.log(f"time budget used up; {s} waits for the next run")
            continue
        name = "kalshi_KXETHD" if s == "KXETHD" else f"ladder_{s}"
        cached = D._load(name, {"markets": {}, "candles": {}})
        if s != "KXETHD":
            rows = D.settled_markets(series=s, since=since)
            D.log(f"{s}: {len(rows)} settled markets")
            by_ev = defaultdict(list)
            for r in rows:
                by_ev[r["event_ticker"]].append(r)
            evs = sorted(by_ev, key=lambda e: max(m["close_time"] or "" for m in by_ev[e]))
            prev = None
            for ev in evs:
                ms = by_ev[ev]
                vals = [_num(m["value"]) for m in ms if _num(m["value"])]
                if prev:
                    for m in ms:
                        k = _num(m["floor"]) or _num(m["cap"])
                        if k and abs(k / prev - 1) <= band:
                            cached["markets"][m["ticker"]] = m
                if vals:
                    prev = vals[0]
            todo = [m for t, m in cached["markets"].items() if t not in cached["candles"]]
            D.log(f"{s}: {len(cached['markets'])} near-price markets, {len(todo)} need candles")

            def job(m, s=s):
                try:
                    return m["ticker"], D.candles(s, m, hours_before=14)
                except Exception as e:
                    D.log(f"  {m['ticker']}: {e}")
                    return m["ticker"], None
            with ThreadPoolExecutor(workers) as ex:
                for i in range(0, len(todo), 400):
                    if time.time() > deadline:
                        break
                    for t, cs in ex.map(job, todo[i:i + 400]):
                        if cs is not None:
                            cached["candles"][t] = cs
                    D._save(name, cached)
                    D.log(f"  {s}: {min(i + 400, len(todo))}/{len(todo)}")
            D._save(name, cached)
        if cached["candles"]:
            out[s] = cached
    return out


def assets(days=400, budget_min=120):
    res = {}
    for s, data in fetch_assets(days, budget_min).items():
        rows = L.table(data, hours=(6, 4, 3, 2, 1))
        fav = [r for r in rows if r["bucket"] in ("75-88c", "93-96c", "88-93c")]
        evs = {data["markets"][t]["event_ticker"] for t in data["candles"] if t in data["markets"]}
        res[s] = {"markets": len(data["candles"]), "events": len(evs), "rows": fav}
    return res


# ---------------------------------------------------------------- report

def _p(v):
    return "–" if v is None else f"{v * 100:+.1f}%"


def markdown(r):
    out = [f"# Favorite follow-ups ({r['generated_at'][:10]})", "",
           "Follow-ups to the Bitcoin favorite finding. Per-day t treats each day (event) as one sample. "
           "Older = before 2026-03-13. Many rows per table, so trust patterns, not single cells.", ""]
    if r.get("maker"):
        out += ["## 1. Limit order instead of paying the ask", "",
                "Rest a YES bid below the ask at the entry time. **Through** = a later trade printed below our bid "
                "(surely filled). **Touch** = a seller traded at our bid (filled only if first in line). "
                "P&L counts missed fills as zero, so compare totals with the taker row.", ""]
        for s, x in r["maker"].items():
            out += [f"### {s} ({x['with_trades']} of {x['candidates']} entries have trade data)", "",
                    "| Entry | Band | How | Chances | Fills | Fill rate | Win % (filled) | Win % (all) | P&L | Return/$ | t (day) | Older | Newer |",
                    "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
            for w in x["rows"]:
                out.append(f"| {w['hours']}h | {w['band']} | {w['how']} | {w['opportunities']} | {w['fills']} | "
                           f"{w['fill_rate'] * 100:.0f}% | {(w['win_rate_filled'] or 0) * 100:.1f}% | {w['win_rate_all'] * 100:.1f}% | "
                           f"{w['pnl']:+.1f} | {_p(w['roi'])} | {w['t_day'] if w['t_day'] is not None else '–'} | "
                           f"{w['older']:+.0f} | {w['newer']:+.0f} |")
            out.append("")
    if r.get("assets"):
        out += ["## 2. The same favorite ladder on other daily price markets", "",
                "Buy YES at the ask, held to settlement, taker fee. Strikes near the previous settle.", "",
                "| Series | Entry | Band | n | Days | Market | Actual | Return/$ | t (day) | Older | Newer | Quarters + |",
                "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for s, x in r["assets"].items():
            for w in x["rows"]:
                if w["events"] < 20:
                    continue
                out.append(f"| {s} | {w['hours']}h | {w['bucket']} | {w['n']} | {w['events']} | {w['market']:.3f} | "
                           f"{w['actual']:.3f} | {_p(w['yes']['roi'])} | {w['yes']['t_event']} | {_p((w['yes_older'] or {}).get('roi'))} | "
                           f"{_p((w['yes_newer'] or {}).get('roi'))} | {w['quarters_positive']} |")
        out += ["", "Series with no rows had too little data (under 20 days in a cell) or don't exist.", ""]
    return "\n".join(out)


def run(cmd="all", days=400, budget_min=150):
    r = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes")}
    if cmd in ("maker", "all"):
        r["maker"] = maker(budget_min=budget_min if cmd == "maker" else budget_min / 2)
    if cmd in ("assets", "all"):
        r["assets"] = assets(days, budget_min if cmd == "assets" else budget_min / 2)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(r, indent=1, default=str))
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(markdown(r))
    D.log(f"wrote {OUT_MD}")
    return r


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m kalshi_analyzer.backtest.fav_extra")
    ap.add_argument("cmd", nargs="?", default="all", choices=["maker", "assets", "all"])
    ap.add_argument("--days", type=int, default=400)
    ap.add_argument("--budget", type=int, default=150, help="minutes of downloading before saving and stopping")
    a = ap.parse_args(argv)
    run(a.cmd, a.days, a.budget)


if __name__ == "__main__":
    main()
