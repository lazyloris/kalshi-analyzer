"""Read-only Kalshi market data. No API key needed for public market data."""
import datetime as dt

from .config import KALSHI_API
from .http import get_json

MONTHS = {m: i for i, m in enumerate(
    ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"], 1)}


def _price(m, name):
    """Dollar price 0..1 from either the *_dollars string or the older integer-cents field."""
    d = m.get(f"{name}_dollars")
    if d not in (None, ""):
        return float(d)
    v = m.get(name)
    if v in (None, ""):
        return None
    v = float(v)
    return v / 100 if v > 1 else v


def target_date_from_event(event_ticker):
    """KXHIGHNY-25NOV07 -> date(2025, 11, 7)."""
    code = event_ticker.split("-")[-1]
    return dt.date(2000 + int(code[:2]), MONTHS[code[2:5]], int(code[5:7]))


def normalize(m, series):
    st = m.get("strike_type")
    if st not in ("between", "greater", "less"):
        return None
    return {
        "ticker": m["ticker"],
        "event_ticker": m["event_ticker"],
        "series": series,
        "target_date": target_date_from_event(m["event_ticker"]).isoformat(),
        "strike_type": st,
        "floor": m.get("floor_strike"),
        "cap": m.get("cap_strike"),
        "yes_bid": _price(m, "yes_bid"),
        "yes_ask": _price(m, "yes_ask"),
        "no_bid": _price(m, "no_bid"),
        "no_ask": _price(m, "no_ask"),
        "volume": m.get("volume") or 0,
        "status": m.get("status"),
        "result": m.get("result") or "",
        "expiration_value": m.get("expiration_value") or "",
        "close_time": m.get("close_time"),
    }


def open_markets(series):
    out, cursor = [], None
    while True:
        params = {"series_ticker": series, "status": "open", "limit": 200}
        if cursor:
            params["cursor"] = cursor
        data = get_json(f"{KALSHI_API}/markets", params)
        for m in data.get("markets", []):
            n = normalize(m, series)
            if n:
                out.append(n)
        cursor = data.get("cursor")
        if not cursor:
            return out


def market(ticker, series):
    data = get_json(f"{KALSHI_API}/markets/{ticker}")
    return normalize(data["market"], series)
