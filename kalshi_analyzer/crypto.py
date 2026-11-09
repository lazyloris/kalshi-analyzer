"""Coinbase public prices (no key): spot price and a 30-day realized volatility estimate."""
import datetime as dt
import math
import statistics
import time

from .config import COINBASE_API
from .http import get_json


def spot(product):
    return float(get_json(f"{COINBASE_API}/products/{product}/ticker")["price"])


def realized_vol(product, days=30):
    """Yearly volatility from daily closes: stdev of daily log returns * sqrt(365)."""
    candles = get_json(f"{COINBASE_API}/products/{product}/candles", {"granularity": 86400})
    closes = [c[4] for c in sorted(candles, key=lambda c: c[0])][-(days + 1):]
    rets = [math.log(b / a) for a, b in zip(closes, closes[1:])]
    return statistics.stdev(rets) * math.sqrt(365)


def hourly_closes(product, days=31, now=None):
    """{hour_end_ts: close} for the last `days` days of hourly candles (Coinbase: 300 per call)."""
    end = int((now or dt.datetime.now(dt.timezone.utc)).timestamp()) // 3600 * 3600
    t, out = end - days * 86400, {}
    while t < end:
        e = min(end, t + 300 * 3600)
        rows = get_json(f"{COINBASE_API}/products/{product}/candles", {
            "granularity": 3600, "start": dt.datetime.fromtimestamp(t, dt.timezone.utc).isoformat(),
            "end": dt.datetime.fromtimestamp(e, dt.timezone.utc).isoformat()})
        for r in rows:
            out[int(r[0]) + 3600] = float(r[4])
        t = e
        time.sleep(0.3)
    return out
