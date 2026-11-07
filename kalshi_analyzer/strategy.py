"""weather-v1: buy the side the forecast says is underpriced, hold to settlement.

Rule, in plain words:
  1. Model the day's high as Normal(NWS forecast + city bias, sigma for that lead time).
  2. For each temperature bracket, compute the model's chance it hits.
  3. If model chance - (ask price + fee per contract) >= MIN_EDGE on YES or NO, buy that side.
  4. Skip thin/odd markets (price outside 5-90c, spread > 10c, < 6h before the high).
  5. At most 2 positions per city-day, never re-buy the same market, $10 per trade.
"""
import datetime as dt
import math
from zoneinfo import ZoneInfo

from . import config as C
from .model import bracket_center, bracket_label, bracket_probability, taker_fee


def lead_info(target_date: str, tz: str, now: dt.datetime):
    """Hours from now until ~4pm local on the target date (when highs usually happen)."""
    d = dt.date.fromisoformat(target_date)
    peak = dt.datetime(d.year, d.month, d.day, 16, tzinfo=ZoneInfo(tz))
    local_today = now.astimezone(ZoneInfo(tz)).date()
    return (peak - now).total_seconds() / 3600, (d - local_today).days


def evaluate(m, forecast_high, now):
    """Return (snapshot_row, candidate_trade_or_None) for one market."""
    city = C.CITIES[m["series"]]
    lead_hours, lead_days = lead_info(m["target_date"], city["tz"], now)
    sigma = C.SIGMA_BY_LEAD_DAYS.get(lead_days)
    snap = {k: m[k] for k in ("series", "ticker", "target_date", "strike_type", "floor", "cap",
                              "yes_bid", "yes_ask", "no_bid", "no_ask", "volume")}
    snap.update(time=now.isoformat(timespec="minutes"), forecast_high=forecast_high, sigma=sigma or "")
    if forecast_high is None or sigma is None:
        snap["model_p"] = ""
        return snap, None
    mu = forecast_high + C.CITY_BIAS_F.get(m["series"], 0.0)
    p_yes = bracket_probability(m["strike_type"], _f(m["floor"]), _f(m["cap"]), mu, sigma)
    snap["model_p"] = round(p_yes, 4)
    if lead_hours < C.MIN_LEAD_HOURS:
        return snap, None

    best = None
    for side, p, ask, bid in (("yes", p_yes, m["yes_ask"], m["yes_bid"]),
                              ("no", 1 - p_yes, m["no_ask"], m["no_bid"])):
        if ask is None or bid is None or not (C.MIN_PRICE <= ask <= C.MAX_PRICE):
            continue
        spread = ask - bid
        if spread > C.MAX_SPREAD:
            continue
        contracts = max(1, math.floor(C.STAKE_DOLLARS / ask))
        fee = taker_fee(contracts, ask, C.FEE_RATE)
        edge = p - ask - fee / contracts
        if edge >= C.MIN_EDGE and (best is None or edge > best["edge"]):
            best = {
                "strategy_version": C.STRATEGY_VERSION,
                "opened_at": now.isoformat(timespec="minutes"),
                "series": m["series"], "city": city["city"], "ticker": m["ticker"],
                "event_ticker": m["event_ticker"], "target_date": m["target_date"],
                "bracket": bracket_label(m["strike_type"], _f(m["floor"]), _f(m["cap"])),
                "strike_type": m["strike_type"], "floor": m["floor"], "cap": m["cap"],
                "side": side, "contracts": contracts, "price": round(ask, 4), "fee": fee,
                "cost": round(contracts * ask + fee, 2), "model_p": round(p, 4),
                "market_p": round(ask, 4), "edge": round(edge, 4),
                "forecast_high": forecast_high, "sigma": sigma,
                "lead_hours": round(lead_hours, 1), "lead_days": lead_days,
                "distance_f": round(bracket_center(m["strike_type"], _f(m["floor"]), _f(m["cap"])) - mu, 1),
                "spread": round(spread, 4), "volume": m["volume"], "status": "open",
            }
    return snap, best


def _f(v):
    return None if v in (None, "") else float(v)
