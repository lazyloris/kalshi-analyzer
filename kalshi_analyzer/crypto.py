"""Coinbase public prices (no key): spot price and a 30-day realized volatility estimate."""
import math
import statistics

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
