"""Minute-level test: does Kalshi's Bitcoin daily market lag behind Coinbase?
python -m kalshi_analyzer.minute_lag --days 120

For each KXBTCD 5pm-ET event, take strikes within 2% of the price, 1-minute Kalshi candles and
1-minute Coinbase prices over the last 6 hours. Each minute: if BTC moved 0.3%+ in the last 5
minutes and the market's ask is below a simple fair value by `edge`, buy (taker, with fee).
Fair value = lognormal with the last 6h of minute volatility (x mult). Two exits: hold to
settlement, or sell at the bid 15 minutes later (catching the catch-up only).
Only data up to each minute is used. Read-only.
"""
import argparse
import bisect
import datetime as dt
import json
import math
import statistics
import time

from . import config as C
from .backtest import data as D
from .http import get_json
from .model import lognormal_probability, taker_fee

OUT_MD = C.ROOT / "reports" / "minute_lag.md"
OUT_JSON = C.ROOT / "dashboard" / "data" / "minute_lag.json"
CACHE = "minute_lag"


def coinbase_minutes(start_ts, end_ts):
    out = {}
    t = start_ts
    while t < end_ts:
        e = min(end_ts, t + 300 * 60)
        rows = get_json(f"{C.COINBASE_API}/products/BTC-USD/candles", {
            "granularity": 60, "start": dt.datetime.fromtimestamp(t, dt.timezone.utc).isoformat(),
            "end": dt.datetime.fromtimestamp(e, dt.timezone.utc).isoformat()}, retries=5)
        for r in rows:
            out[int(r[0]) + 60] = float(r[4])  # keyed by candle END: never a price from the future
        t = e
        time.sleep(0.3)
    return out


def kalshi_minutes(m, start_ts, end_ts):
    params = {"start_ts": start_ts, "end_ts": end_ts, "period_interval": 1}
    urls = [f"{D.K}/series/KXBTCD/markets/{m['ticker']}/candlesticks",
            f"{D.K}/historical/markets/{m['ticker']}/candlesticks"]
    if m["source"] == "historical":
        urls.reverse()
    for u in urls:
        try:
            return D._parse_candles(get_json(u, params, retries=4))
        except Exception:
            continue
    return []


def fetch(days):
    cache = D._load(CACHE, {"events": {}})
    today = dt.date.today()
    for ev in D.btc_event_tickers(today - dt.timedelta(days=days), today - dt.timedelta(days=1)):
        if ev in cache["events"]:
            continue
        ms = D.settled_markets(event_ticker=ev)
        if not ms:
            continue
        close = max(D._ts(m["close_time"]) for m in ms)
        start = close - 6 * 3600
        try:
            px = coinbase_minutes(start - 6 * 3600, close)  # 6h extra for volatility
        except Exception as e:
            D.log(f"{ev}: coinbase {e}")
            continue
        hrs = sorted(px)
        k = bisect.bisect_right(hrs, start) - 1
        spot = px[hrs[k]] if k >= 0 else None
        if not spot:
            continue
        keep = []
        for m in ms:
            strike = _num(m["floor"]) or _num(m["cap"])
            if strike and abs(strike / spot - 1) <= 0.02 and m["strike_type"] in ("greater", "greater_or_equal", "less"):
                cs = kalshi_minutes(m, start, close)
                if cs:
                    keep.append({**m, "cs": cs})
        cache["events"][ev] = {"close": close, "px": {str(t): v for t, v in px.items()}, "markets": keep}
        D.log(f"{ev}: {len(keep)} markets")
        D._save(CACHE, cache)
    return cache


def _num(v):
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):
        return None


def simulate(cache, move=0.003, edge=0.05, mult=1.0, hold="settle", stake=10.0):
    trades = []
    for ev, e in sorted(cache["events"].items()):
        px = {int(t): v for t, v in e["px"].items()}
        ts_sorted = sorted(px)
        close = e["close"]
        for m in e["markets"]:
            lo, hi = _num(m["floor"]), _num(m["cap"])
            won_yes = m["result"] == "yes"
            cs = sorted(m["cs"])
            last_trade = -1e18
            for i, c in enumerate(cs):
                t, bid, ask = c[0], c[1], c[2]
                if bid is None or ask is None or ask - bid > 0.06 or t - last_trade < 3600 or t > close - 300:
                    continue
                k = bisect.bisect_right(ts_sorted, t) - 1
                k5 = bisect.bisect_right(ts_sorted, t - 300) - 1
                if k < 360 or k5 < 0 or t - ts_sorted[k] > 120:
                    continue
                spot, spot5 = px[ts_sorted[k]], px[ts_sorted[k5]]
                r = math.log(spot / spot5)
                if abs(r) < move:
                    continue
                window = [px[ts_sorted[j]] for j in range(k - 360, k + 1)]
                rets = [math.log(b / a) for a, b in zip(window, window[1:])]
                vol = statistics.pstdev(rets) * math.sqrt(525600) * mult
                hours = (close - t) / 3600
                try:
                    p_yes = lognormal_probability(m["strike_type"], lo, hi, spot, max(vol, 0.05), hours)
                except ValueError:
                    continue
                # only trade in the direction BTC just moved (that's the lag being tested)
                side = None
                if p_yes - ask >= edge:
                    side = "yes"
                elif (1 - p_yes) - (1 - bid) >= edge:
                    side = "no"
                if side is None:
                    continue
                up_for_side = (side == "yes") == (m["strike_type"] != "less")
                if (r > 0) != up_for_side:
                    continue
                price = ask if side == "yes" else 1 - bid
                n = max(1, math.floor(stake / price))
                cost = n * price + taker_fee(n, price, C.FEE_RATE)
                won = won_yes if side == "yes" else not won_yes
                if hold == "settle":
                    pnl = (n if won else 0) - cost
                else:
                    later = [x for x in cs[i + 1:] if x[0] >= t + 900 and x[1] is not None and x[2] is not None]
                    if not later:
                        pnl = (n if won else 0) - cost
                    else:
                        sell = later[0][1] if side == "yes" else 1 - later[0][2]
                        pnl = n * sell - taker_fee(n, sell, C.FEE_RATE) - cost
                trades.append({"event": ev, "ticker": m["ticker"], "ts": t, "side": side, "price": round(price, 3),
                               "p_model": round(p_yes if side == "yes" else 1 - p_yes, 3), "pnl": round(pnl, 3),
                               "cost": round(cost, 3), "date": dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat()})
                last_trade = t
    return trades


def summary(trades):
    if not trades:
        return {"trades": 0}
    staked = sum(t["cost"] for t in trades)
    pnl = sum(t["pnl"] for t in trades)
    rets = [t["pnl"] / t["cost"] for t in trades]
    sd = statistics.pstdev(rets) if len(rets) > 1 else 0
    half = len(trades) // 2
    s = sorted(trades, key=lambda t: t["ts"])
    return {"trades": len(trades), "pnl": round(pnl, 2), "roi": round(pnl / staked, 4),
            "t": round(statistics.fmean(rets) / sd * math.sqrt(len(rets)), 2) if sd else None,
            "first_half": round(sum(t["pnl"] for t in s[:half]), 1), "second_half": round(sum(t["pnl"] for t in s[half:]), 1),
            "older": round(sum(t["pnl"] for t in s if t["date"] < "2026-03-13"), 1)}


def run(days):
    cache = fetch(days)
    rows = []
    for move in (0.002, 0.003, 0.005):
        for edge in (0.03, 0.05, 0.08):
            for mult in (0.5, 1.0):
                for hold in ("settle", "15m"):
                    rows.append({"move": move, "edge": edge, "mult": mult, "hold": hold,
                                 **summary(simulate(cache, move, edge, mult, hold))})
    rows.sort(key=lambda r: -(r.get("pnl") or -1e9))
    n_ev = len(cache["events"])
    L = [f"# Minute-level Bitcoin lag test ({dt.date.today()})", "",
         f"{n_ev} daily events, strikes within 2% of the price, last 6 hours before 5pm ET. "
         "Buy when BTC moved X% in 5 minutes and the Kalshi ask is below fair value by the edge. "
         "Taker fees included. 'older' = P&L before 2026-03-13.", "",
         "| BTC move | Edge | Vol x | Exit | Trades | P&L | Return/$ | t | 1st half | 2nd half | Older |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['move'] * 100:.1f}% | {r['edge'] * 100:.0f}c | {r['mult']} | {r['hold']} | {r['trades']} | "
                 f"{r.get('pnl', 0):+.1f} | {(r.get('roi') or 0) * 100:+.1f}% | {r.get('t') or '–'} | "
                 f"{r.get('first_half', 0):+.0f} | {r.get('second_half', 0):+.0f} | {r.get('older', 0):+.0f} |")
    L += ["", "18 settings were tried, so the best row is flattered by selection. Look for rows that are "
              "positive in both halves AND in the older period.", ""]
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(L))
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps({"events": n_ev, "rows": rows}, indent=1))
    D.log(f"wrote {OUT_MD}")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m kalshi_analyzer.minute_lag")
    ap.add_argument("--days", type=int, default=120)
    run(ap.parse_args(argv).days)


if __name__ == "__main__":
    main()
