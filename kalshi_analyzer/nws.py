"""National Weather Service point forecasts (free, no key)."""
import datetime as dt

from .config import NWS_API
from .http import get_json


def daily_extremes(lat, lon):
    """Return {"high": {date: F}, "low": {date: F}} from the NWS 7-day forecast for a point.

    A daytime period's temperature is that day's high. A night period starting on the evening of
    day D holds the low reached around sunrise on D+1, so it is filed under D+1.
    """
    point = get_json(f"{NWS_API}/points/{lat:.4f},{lon:.4f}")
    fc = get_json(point["properties"]["forecast"])
    out = {"high": {}, "low": {}}
    for p in fc["properties"]["periods"]:
        t = float(p["temperature"])
        if p.get("temperatureUnit") == "C":
            t = t * 9 / 5 + 32
        start = dt.datetime.fromisoformat(p["startTime"])
        if p.get("isDaytime"):
            out["high"].setdefault(start.date().isoformat(), t)
        else:
            # "Overnight" periods that start after midnight already belong to that same morning.
            day = start.date() if start.hour < 6 else start.date() + dt.timedelta(days=1)
            out["low"].setdefault(day.isoformat(), t)
    return out
