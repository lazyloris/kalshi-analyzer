"""Settle open paper trades and record actual values from settled Kalshi markets."""
import datetime as dt

from . import config as C, kalshi
from .explain import explain
from .http import get_json


def actual_from_event(markets):
    """Best estimate of the final value from an event's settled markets: (value, approx)."""
    for m in markets:
        try:
            return float(m["expiration_value"]), False
        except (TypeError, ValueError):
            pass
    ladder = []
    for m in markets:
        lo = float(m["floor"]) if m["floor"] not in (None, "") else None
        hi = float(m["cap"]) if m["cap"] not in (None, "") else None
        if m["result"] == "yes" and m["strike_type"] == "between":
            return (lo + hi) / 2, True
        if m["strike_type"] in ("greater", "greater_or_equal") and lo is not None:
            ladder.append((lo, m["result"]))
    # "Above X" ladders: the value sits between the highest YES strike and the lowest NO strike.
    yes = [k for k, r in ladder if r == "yes"]
    no = [k for k, r in ladder if r == "no"]
    if yes and no:
        return (max(yes) + min(no)) / 2, True
    for m in markets:
        if m["result"] == "yes" and m["strike_type"] == "greater":
            return float(m["floor"]) + 1, True
        if m["result"] == "yes" and m["strike_type"] == "less":
            return float(m["cap"]) - 1, True
    return None, True


def event_markets(event_ticker, series):
    data = get_json(f"{C.KALSHI_API}/markets", {"event_ticker": event_ticker, "limit": 200})
    return [n for n in (kalshi.normalize(m, series) for m in data.get("markets", [])) if n]


def settle_trades(trades, actuals, now, log):
    known = {(a["series"], a["target_date"]): a for a in actuals}
    cache = {}
    for t in trades:
        if t["status"] != "open":
            continue
        try:
            if t["event_ticker"] not in cache:
                cache[t["event_ticker"]] = event_markets(t["event_ticker"], t["series"])
            ms = cache[t["event_ticker"]]
        except Exception as e:  # keep going; try again next hour
            log(f"settle {t['ticker']}: {e}")
            continue
        mine = next((m for m in ms if m["ticker"] == t["ticker"]), None)
        if not mine or mine["result"] not in ("yes", "no"):
            continue
        value, approx = (None, True) if t.get("book") == "trending" else actual_from_event(ms)
        if value is not None and (t["series"], t["target_date"]) not in known:
            row = {"series": t["series"], "target_date": t["target_date"], "actual": value,
                   "approx": int(approx), "source": "kalshi settlement"}
            actuals.append(row)
            known[(t["series"], t["target_date"])] = row
        won = mine["result"] == t["side"]
        payout = float(t["contracts"]) if won else 0.0
        t.update(status="settled", result=mine["result"], won=str(int(won)), payout=payout,
                 pnl=round(payout - float(t["cost"]), 2), closed_at=now.isoformat(timespec="minutes"))
        if value is not None and t.get("forecast") not in (None, ""):
            t["actual"] = value
            t["forecast_error"] = round(value - float(t["forecast"]), 2)
        t["cause"], t["why"] = explain(t)
        log(f"settled {t['ticker']} {t['side']} -> {t['result']} pnl {t['pnl']}")


def record_actuals(actuals, forecasts, today_by_series, log):
    """Weather: fill actual temps for past days we forecast, even untraded (to measure NWS error)."""
    have = {(a["series"], a["target_date"]) for a in actuals}
    wanted = {(f["series"], f["target_date"]) for f in forecasts}
    for series, day in sorted(wanted - have):
        if day >= today_by_series.get(series, "9999"):
            continue
        d = dt.date.fromisoformat(day)
        event = f"{series}-{d:%y}{d.strftime('%b').upper()}{d:%d}"
        try:
            ms = event_markets(event, series)
        except Exception as e:
            log(f"actual {event}: {e}")
            continue
        if not ms or not all(m["result"] in ("yes", "no") for m in ms):
            continue
        value, approx = actual_from_event(ms)
        if value is not None:
            actuals.append({"series": series, "target_date": day, "actual": value,
                            "approx": int(approx), "source": "kalshi settlement"})
