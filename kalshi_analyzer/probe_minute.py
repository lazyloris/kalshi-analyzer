"""How far back does Kalshi keep 1-minute candles and individual trades? Read-only probe.
python -m kalshi_analyzer.probe_minute"""
import datetime as dt

from . import config as C
from .backtest import data as D
from .http import get_json

K = C.KALSHI_API


def probe():
    today = dt.date.today()
    rows = []
    for days in (3, 14, 45, 90, 180, 365, 540):
        d = today - dt.timedelta(days=days)
        ev = D.btc_event_tickers(d, d)[0]
        ms = []
        for url, p in ((f"{K}/markets", {"event_ticker": ev}), (f"{K}/historical/markets", {"event_ticker": ev})):
            try:
                ms = get_json(url, p, retries=3).get("markets") or []
            except Exception:
                ms = []
            if ms:
                src = "historical" if "historical" in url else "live"
                break
        if not ms:
            rows.append((days, ev, "no markets", "", ""))
            continue
        m = sorted(ms, key=lambda x: -float(x.get("volume_fp") or x.get("volume") or 0))[0]
        end = D._ts(m["close_time"])
        got = "error"
        for u in (f"{K}/series/KXBTCD/markets/{m['ticker']}/candlesticks", f"{K}/historical/markets/{m['ticker']}/candlesticks"):
            try:
                cs = get_json(u, {"start_ts": end - 6 * 3600, "end_ts": end, "period_interval": 1}, retries=2).get("candlesticks") or []
                got = f"{len(cs)} 1-min candles ({u.split('/')[-4] if 'historical' in u else 'series'})"
                if cs:
                    break
            except Exception as e:
                got = f"error {e}"[:80]
        trades = "error"
        for u in (f"{K}/markets/trades", f"{K}/historical/trades"):
            try:
                tr = get_json(u, {"ticker": m["ticker"], "limit": 1000}, retries=2).get("trades") or []
                trades = f"{len(tr)} trades ({'historical' if 'historical' in u else 'live'})"
                if tr:
                    break
            except Exception as e:
                trades = f"error {e}"[:80]
        rows.append((days, m["ticker"], src, got, trades))
    print("| Days ago | Market | Source | 1-min candles (last 6h) | Trades |\n|---|---|---|---|---|")
    for r in rows:
        print("| " + " | ".join(str(x) for x in r) + " |")


if __name__ == "__main__":
    probe()
