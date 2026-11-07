"""National Weather Service point forecasts (free, no key)."""
from .config import NWS_API
from .http import get_json


def daily_highs(lat, lon):
    """Return {'YYYY-MM-DD': forecast_high_F} from the NWS 7-day forecast for a point."""
    point = get_json(f"{NWS_API}/points/{lat:.4f},{lon:.4f}")
    fc = get_json(point["properties"]["forecast"])
    highs = {}
    for p in fc["properties"]["periods"]:
        if not p.get("isDaytime"):
            continue
        t = float(p["temperature"])
        if p.get("temperatureUnit") == "C":
            t = t * 9 / 5 + 32
        highs.setdefault(p["startTime"][:10], t)
    return highs
