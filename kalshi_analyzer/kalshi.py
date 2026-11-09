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


def _volume(m):
    """Contracts traded. Newer API responses use fixed-point strings (volume_fp)."""
    for k in ("volume_fp", "volume", "volume_24h_fp", "volume_24h"):
        v = m.get(k)
        if v not in (None, ""):
            try:
                if float(v):
                    return float(v)
            except (TypeError, ValueError):
                pass
    return 0


def target_date_from_event(event_ticker):
    """KXHIGHNY-25NOV07 -> date(2025, 11, 7)."""
    code = event_ticker.split("-")[-1]
    return dt.date(2000 + int(code[:2]), MONTHS[code[2:5]], int(code[5:7]))


def _target_date(m):
    try:
        return target_date_from_event(m["event_ticker"]).isoformat()
    except (KeyError, ValueError, IndexError):
        return (m.get("close_time") or "")[:10]


def normalize(m, series):
    st = m.get("strike_type")
    if not m.get("ticker"):
        return None
    return {
        "ticker": m["ticker"],
        "event_ticker": m["event_ticker"],
        "series": series,
        "target_date": _target_date(m),
        "strike_type": st or "custom",
        "yes_sub_title": m.get("yes_sub_title") or "",
        "floor": m.get("floor_strike"),
        "cap": m.get("cap_strike"),
        "yes_bid": _price(m, "yes_bid"),
        "yes_ask": _price(m, "yes_ask"),
        "no_bid": _price(m, "no_bid"),
        "no_ask": _price(m, "no_ask"),
        "volume": _volume(m),
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


def mid_hours_ago(series, ticker, hours=3, now=None):
    """Kalshi's YES mid price about `hours` ago from hourly candlesticks, or None."""
    now = int((now or dt.datetime.now(dt.timezone.utc)).timestamp())
    data = get_json(f"{KALSHI_API}/series/{series}/markets/{ticker}/candlesticks",
                    {"start_ts": now - (hours + 2) * 3600, "end_ts": now - hours * 3600 + 1800, "period_interval": 60})
    best = None
    for c in data.get("candlesticks") or []:
        bid, ask = _price(c.get("yes_bid") or {}, "close"), _price(c.get("yes_ask") or {}, "close")
        if bid is not None and ask is not None and 0 < bid <= ask < 1 and int(c["end_period_ts"]) <= now - hours * 3600 + 1800:
            best = (bid + ask) / 2
    return best
