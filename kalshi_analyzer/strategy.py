"""One rule for every book: buy the side our model says is underpriced, hold to settlement.

  1. Model the outcome:
       weather: actual temp ~ Normal(NWS forecast + city bias, sigma for days ahead)
       crypto:  price at 5pm ~ lognormal around the Coinbase spot price, 30-day realized volatility
  2. For each bracket, compute the model's chance it hits.
  3. Blend our chance with the market's (MARKET_BLEND), skip if they disagree by more than MAX_GAP,
     then if chance - (ask + fee per contract) >= MIN_EDGE on YES or NO, buy that side.
  4. Skip thin/odd markets (price outside 5-90c, spread > 10c, too close to the outcome).
  5. At most 2 positions per event, never re-buy the same market, flat paper stake.
"""
import datetime as dt
import math
from zoneinfo import ZoneInfo

from . import config as C
from .model import (bracket_center, bracket_label, bracket_probability, lognormal_probability,
                    price_sigma, taker_fee)


def results_by(book_id, close_time):
    """When to check back: market close + typical settle delay for this kind of market (ISO, UTC)."""
    if not close_time:
        return ""
    close = dt.datetime.fromisoformat(close_time.replace("Z", "+00:00"))
    hours = C.SETTLE_DELAY_HOURS.get(C.BOOKS[book_id]["kind"], 6)
    return (close + dt.timedelta(hours=hours)).isoformat(timespec="minutes")


def timing(book_id, m, contracts, p, cost):
    return {"closes_at": m.get("close_time") or "", "results_by": results_by(book_id, m.get("close_time")),
            "expected_pnl": round(contracts * p - cost, 2)}


def _f(v):
    return None if v in (None, "") else float(v)


def weather_lead(book, target_date, tz, now):
    """Hours until the usual time of the high/low on the target date, and days ahead (local)."""
    d = dt.date.fromisoformat(target_date)
    peak = dt.datetime(d.year, d.month, d.day, book["peak_hour"], tzinfo=ZoneInfo(tz))
    return (peak - now).total_seconds() / 3600, (d - now.astimezone(ZoneInfo(tz)).date()).days


def model(book_id, m, ctx, now):
    """Return (p_yes, forecast, sigma, lead_hours, lead_days, label) or None if we can't model it."""
    book = C.BOOKS[book_id]
    st, lo, hi = m["strike_type"], _f(m["floor"]), _f(m["cap"])
    if book["kind"] == "weather":
        stn = C.STATIONS[book["series"][m["series"]]]
        lead_hours, lead_days = weather_lead(book, m["target_date"], stn["tz"], now)
        sigma = book["sigma_by_lead_days"].get(lead_days)
        fc = ctx.get("forecasts", {}).get(m["target_date"])
        if fc is None or sigma is None:
            return None
        bias = book["bias"].get(m["series"], 0.0)
        learned = ctx.get("calib", {}).get(lead_days)
        if learned:  # bias/sigma measured from this city's own past forecast misses
            bias, sigma = bias + learned[0], learned[1]
        mu = fc + bias
        return bracket_probability(st, lo, hi, mu, sigma), mu, sigma, lead_hours, lead_days, stn["city"]
    spot, vol = ctx.get("spot"), ctx.get("vol")
    close = dt.datetime.fromisoformat(m["close_time"].replace("Z", "+00:00")) if m.get("close_time") else None
    if spot is None or close is None:
        return None
    hours = (close - now).total_seconds() / 3600
    if hours <= 0:
        return None
    if book.get("vol_model") == "tod":  # volatility for the actual hours held (nights/weekends are calmer)
        from .backtest.signals import live_tod_vol
        prices = ctx.get("hourly")
        vol = live_tod_vol(prices, int(now.timestamp()), int(close.timestamp())) if prices else None
        if vol is None:
            return None
    vol = vol * book.get("vol_mult", 1.0)
    p = lognormal_probability(st, lo, hi, spot, vol, hours)
    return p, spot, price_sigma(spot, vol, hours), hours, int(hours // 24), C.ASSET_NAMES.get(book["series"][m["series"]], m["series"])


def evaluate(book_id, m, ctx, now):
    """Return (snapshot_row, candidate_trade_or_None) for one market."""
    book, R = C.BOOKS[book_id], C.rules(book_id)
    snap = {k: m[k] for k in ("series", "ticker", "target_date", "strike_type", "floor", "cap",
                              "yes_bid", "yes_ask", "no_bid", "no_ask", "volume")}
    snap["time"] = now.isoformat(timespec="minutes")
    if book["kind"] == "fade":
        return snap, fade(book_id, m, now, snap)
    if book.get("strategy") == "favorite":
        snap.update(forecast="", sigma="", model_p="")
        return snap, favorite(book_id, m, now)
    if book.get("strategy") == "upside_no":
        snap.update(forecast="", sigma="", model_p="")
        return snap, upside_no(book_id, m, now)
    if book.get("strategy") == "nowcast":
        return snap, nowcast_trade(book_id, m, ctx, now, snap)
    try:
        res = model(book_id, m, ctx, now)
    except ValueError:  # bracket type the model doesn't understand
        res = None
    if res is None:
        snap.update(forecast="", sigma="", model_p="")
        return snap, None
    p_yes, mu, sigma, lead_hours, lead_days, label = res
    snap.update(forecast=round(mu, 2), sigma=round(sigma, 3), model_p=round(p_yes, 4))
    if book.get("strategy") == "fade":  # model still logged for learning, but trades use the fade rule
        return snap, fade(book_id, m, now, snap)
    if lead_hours < R["MIN_LEAD_HOURS"]:
        return snap, None

    best = None
    st, lo, hi = m["strike_type"], _f(m["floor"]), _f(m["cap"])
    p_model = p_yes
    if m["yes_bid"] is not None and m["yes_ask"] is not None:
        p_mkt = (m["yes_bid"] + m["yes_ask"]) / 2
        # A model that disagrees hugely with the market is usually the one that's wrong.
        if R.get("MAX_GAP") is not None and abs(p_yes - p_mkt) > R["MAX_GAP"]:
            return snap, None
        p_yes = (1 - R.get("MARKET_BLEND", 0.0)) * p_yes + R.get("MARKET_BLEND", 0.0) * p_mkt
    for side, p, ask, bid in (("yes", p_yes, m["yes_ask"], m["yes_bid"]),
                              ("no", 1 - p_yes, m["no_ask"], m["no_bid"])):
        if ask is None or bid is None or not (R["MIN_PRICE"] <= ask <= R["MAX_PRICE"]):
            continue
        spread = ask - bid
        if spread > R["MAX_SPREAD"]:
            continue
        contracts = max(1, math.floor(R["STAKE_DOLLARS"] / ask))
        fee = taker_fee(contracts, ask, C.FEE_RATE)
        edge = p - ask - fee / contracts
        if edge >= R["MIN_EDGE"] and (best is None or edge > best["edge"]):
            best = {
                "book": book_id, "strategy_version": book["version"],
                "opened_at": now.isoformat(timespec="minutes"),
                "series": m["series"], "city": label, "ticker": m["ticker"],
                "event_ticker": m["event_ticker"], "target_date": m["target_date"],
                "bracket": bracket_label(st, lo, hi, book["unit"]),
                "strike_type": st, "floor": m["floor"], "cap": m["cap"],
                "side": side, "contracts": contracts, "price": round(ask, 4), "fee": fee,
                "cost": round(contracts * ask + fee, 2), "model_p": round(p, 4),
                "raw_model_p": round(p_model if side == "yes" else 1 - p_model, 4),
                "market_p": round(ask, 4), "edge": round(edge, 4),
                "forecast": round(mu, 2), "sigma": round(sigma, 3), "unit": book["unit"],
                "lead_hours": round(lead_hours, 1), "lead_days": lead_days,
                "distance": round(bracket_center(st, lo, hi) - mu, 2),
                "spread": round(spread, 4), "volume": m["volume"], "status": "open",
                **timing(book_id, m, contracts, p, contracts * ask + fee),
            }
    if best and book.get("skip_spike") and ctx.get("mid_before"):
        # Leave markets whose price just jumped: in the backtest those moves were real information.
        before = ctx["mid_before"](m["series"], m["ticker"])
        if before is not None and m["yes_bid"] is not None and m["yes_ask"] is not None \
                and abs((m["yes_bid"] + m["yes_ask"]) / 2 - before) >= book["skip_spike"]:
            return snap, None
    return snap, best


def fade(book_id, m, now, snap):
    """Trending book: buy NO when YES is a cheap long shot. 'Model' = the market price minus nothing;
    the stats measure whether long shots really win less often than their price says."""
    book, R = C.BOOKS[book_id], C.rules(book_id)
    for k in ("forecast", "sigma", "model_p"):
        snap.setdefault(k, "")
    ya, yb, na, nb = m["yes_ask"], m["yes_bid"], m["no_ask"], m["no_bid"]
    close = dt.datetime.fromisoformat(m["close_time"].replace("Z", "+00:00")) if m.get("close_time") else None
    if None in (ya, yb, na, nb) or close is None:
        return None
    hours = (close - now).total_seconds() / 3600
    if hours < R["MIN_LEAD_HOURS"] or not (book["fade_min_yes"] <= yb and ya <= book["fade_max_yes"]):
        return None
    if na > R["MAX_PRICE"] or na - nb > R["MAX_SPREAD"]:
        return None
    contracts = max(1, math.floor(R["STAKE_DOLLARS"] / na))
    fee = taker_fee(contracts, na, C.FEE_RATE)
    implied_no = 1 - (ya + yb) / 2  # what the market says NO is worth (mid price)
    return {
        "book": book_id, "strategy_version": book["version"], "opened_at": now.isoformat(timespec="minutes"),
        "series": m["series"], "city": C.STATIONS.get(book["series"][m["series"]], {}).get("city", book["series"][m["series"]]),
        "ticker": m["ticker"],
        "event_ticker": m["event_ticker"], "target_date": m["target_date"],
        "bracket": m.get("yes_sub_title") or m["ticker"].split("-")[-1],
        "strike_type": m["strike_type"], "floor": m["floor"], "cap": m["cap"],
        "side": "no", "contracts": contracts, "price": round(na, 4), "fee": fee,
        "cost": round(contracts * na + fee, 2), "model_p": round(implied_no, 4), "market_p": round(na, 4),
        "edge": round(implied_no - na - fee / contracts, 4), "forecast": "", "sigma": "", "unit": "",
        "lead_hours": round(hours, 1), "lead_days": int(hours // 24), "distance": "",
        "spread": round(na - nb, 4), "volume": m["volume"], "status": "open",
        **timing(book_id, m, contracts, implied_no, contracts * na + fee),
    }


def fav_band(book, ask):
    """(low, high, backtest win rate) of the favorite band this YES ask falls in, or None."""
    for lo, hi, win in book["fav_bands"]:
        if lo <= ask < hi:
            return lo, hi, win
    return None


def favorite(book_id, m, now):
    """Pre-registered favorite test: buy YES at the ask when it sits in a band, 3.5-4.5h before close.
    No model; the 'model' chance logged is the band's backtest win rate."""
    book, R = C.BOOKS[book_id], C.rules(book_id)
    ya, yb = m["yes_ask"], m["yes_bid"]
    close = dt.datetime.fromisoformat(m["close_time"].replace("Z", "+00:00")) if m.get("close_time") else None
    if ya is None or yb is None or close is None:
        return None
    hours = (close - now).total_seconds() / 3600
    lo_h, hi_h = book["fav_lead_hours"]
    if not (lo_h <= hours <= hi_h) or ya - yb > R["MAX_SPREAD"]:
        return None
    band = fav_band(book, ya)
    if band is None:
        return None
    contracts = max(1, math.floor(R["STAKE_DOLLARS"] / ya))
    fee = taker_fee(contracts, ya, C.FEE_RATE)
    p = band[2]
    st, lo, hi = m["strike_type"], _f(m["floor"]), _f(m["cap"])
    return {
        "book": book_id, "strategy_version": book["version"], "opened_at": now.isoformat(timespec="minutes"),
        "series": m["series"], "city": C.ASSET_NAMES.get(book["series"][m["series"]], m["series"]),
        "ticker": m["ticker"], "event_ticker": m["event_ticker"], "target_date": m["target_date"],
        "bracket": bracket_label(st, lo, hi, book["unit"]), "strike_type": st, "floor": m["floor"], "cap": m["cap"],
        "side": "yes", "contracts": contracts, "price": round(ya, 4), "fee": fee,
        "cost": round(contracts * ya + fee, 2), "model_p": p, "market_p": round(ya, 4),
        "edge": round(p - ya - fee / contracts, 4), "forecast": "", "sigma": "", "unit": book["unit"],
        "lead_hours": round(hours, 2), "lead_days": 0, "distance": "",
        "spread": round(ya - yb, 4), "volume": m["volume"], "status": "open",
        "cap_key": f"{m['event_ticker']}|{band[0]:.2f}",
        **timing(book_id, m, contracts, p, contracts * ya + fee),
    }


def upside_no(book_id, m, now):
    """Fable's crypto upside rule (review 2026-11-17, section 8): 3.5-4.5h before close, buy NO at
    1 - yes_bid on 'greater' strikes whose YES bid is 3-12c with spread <= 3c. No model; the 'model'
    chance logged is the backtest win rate."""
    book, R = C.BOOKS[book_id], C.rules(book_id)
    ya, yb = m["yes_ask"], m["yes_bid"]
    close = dt.datetime.fromisoformat(m["close_time"].replace("Z", "+00:00")) if m.get("close_time") else None
    if ya is None or yb is None or close is None or m["strike_type"] != "greater":
        return None
    hours = (close - now).total_seconds() / 3600
    lo_h, hi_h = book["lead_hours"]
    lo_b, hi_b = book["yes_bid_band"]
    if not (lo_h <= hours <= hi_h) or ya - yb > R["MAX_SPREAD"] + 1e-9 or not (lo_b <= yb < hi_b) or ya >= 1:
        return None
    price = round(1 - yb, 4)
    contracts = max(1, math.floor(R["STAKE_DOLLARS"] / price))
    fee = taker_fee(contracts, price, C.FEE_RATE)
    p = book["backtest_win_rate"]
    st, lo, hi = m["strike_type"], _f(m["floor"]), _f(m["cap"])
    return {
        "book": book_id, "strategy_version": book["version"], "opened_at": now.isoformat(timespec="minutes"),
        "series": m["series"], "city": C.ASSET_NAMES.get(book["series"][m["series"]], m["series"]),
        "ticker": m["ticker"], "event_ticker": m["event_ticker"], "target_date": m["target_date"],
        "bracket": bracket_label(st, lo, hi, book["unit"]), "strike_type": st, "floor": m["floor"], "cap": m["cap"],
        "side": "no", "contracts": contracts, "price": price, "fee": fee,
        "cost": round(contracts * price + fee, 2), "model_p": p, "market_p": price,
        "edge": round(p - price - fee / contracts, 4), "forecast": "", "sigma": "", "unit": book["unit"],
        "lead_hours": round(hours, 2), "lead_days": 0, "distance": "",
        "spread": round(ya - yb, 4), "volume": m["volume"], "status": "open", "cap_key": m["ticker"],
        **timing(book_id, m, contracts, p, contracts * price + fee),
    }


def nowcast_trade(book_id, m, ctx, now, snap):
    """Core CPI side test (PR #29): Normal(nowcast, sigma) on the released value, taker, 5c edge, 2.5-3.5h out."""
    book, R = C.BOOKS[book_id], C.rules(book_id)
    snap.update(forecast="", sigma="", model_p="")
    ya, yb = m["yes_ask"], m["yes_bid"]
    close = dt.datetime.fromisoformat(m["close_time"].replace("Z", "+00:00")) if m.get("close_time") else None
    nc = (ctx.get("nowcast") or {}).get(m["event_ticker"])
    if ya is None or yb is None or close is None or nc is None or m["strike_type"] != "greater" or m["floor"] in (None, ""):
        return None
    k, sigma = float(m["floor"]), book["sigma"]
    p = 1 - 0.5 * (1 + math.erf((k + 0.05 - nc) / (sigma * math.sqrt(2))))
    snap.update(forecast=round(nc, 4), sigma=sigma, model_p=round(p, 4))
    hours = (close - now).total_seconds() / 3600
    lo_h, hi_h = book["lead_hours"]
    if not (lo_h <= hours <= hi_h) or ya - yb > R["MAX_SPREAD"] + 1e-9:
        return None
    best = None
    for side, price, chance in (("yes", ya, p), ("no", round(1 - yb, 4), 1 - p)):
        if not (R["MIN_PRICE"] <= price <= R["MAX_PRICE"]):
            continue
        contracts = max(1, math.floor(R["STAKE_DOLLARS"] / price))
        fee = taker_fee(contracts, price, C.FEE_RATE)
        edge = chance - price - fee / contracts
        if edge >= R["MIN_EDGE"] and (best is None or edge > best[4]):
            best = (side, price, chance, contracts, edge, fee)
    if best is None:
        return None
    side, price, chance, contracts, edge, fee = best
    st, lo, hi = m["strike_type"], _f(m["floor"]), _f(m["cap"])
    return {
        "book": book_id, "strategy_version": book["version"], "opened_at": now.isoformat(timespec="minutes"),
        "series": m["series"], "city": "Core CPI", "ticker": m["ticker"], "event_ticker": m["event_ticker"],
        "target_date": m["target_date"], "bracket": bracket_label(st, lo, hi, book["unit"]), "strike_type": st,
        "floor": m["floor"], "cap": m["cap"], "side": side, "contracts": contracts, "price": price, "fee": fee,
        "cost": round(contracts * price + fee, 2), "model_p": round(chance, 4), "market_p": price,
        "edge": round(edge, 4), "forecast": round(nc, 4), "sigma": sigma, "unit": book["unit"],
        "lead_hours": round(hours, 2), "lead_days": 0, "distance": round(nc - (k + 0.05), 4),
        "spread": round(ya - yb, 4), "volume": m["volume"], "status": "open", "cap_key": m["ticker"],
        **timing(book_id, m, contracts, chance, contracts * price + fee),
    }


def kill_reason(book_id, trades, now):
    """Pre-registered kill rules for the favorite test. Returns why the test has stopped, or None."""
    book = C.BOOKS[book_id]
    k = book.get("kill")
    if not k:
        return None
    end = dt.date.fromisoformat(book["test_start"]) + dt.timedelta(days=book["test_days"])
    settled = [t for t in trades if t["status"] == "settled"]
    days = {}
    for t in settled:
        days[t["target_date"]] = days.get(t["target_date"], 0.0) + float(t["pnl"])
    order = sorted(days)
    if k.get("max_drawdown") is not None:
        run = peak = 0.0
        for d in order:
            run += days[d]; peak = max(peak, run)
            if peak - run > k["max_drawdown"]:
                return f"drop from peak over ${k['max_drawdown']:.0f} (on {d})"
        first = sorted(settled, key=lambda t: t.get("closed_at") or t["target_date"])[:k["loss_window_trades"]]
        if sum(1 for t in first if float(t["pnl"]) < 0) >= k["max_losses"]:
            return f"{k['max_losses']} losses within the first {k['loss_window_trades']} trades"
        if now.date() >= end:
            return f"test finished on {end.isoformat()}"
        return None
    for i in range(len(order)):
        window = order[i:i + k["window_days"]]
        if sum(1 for d in window if days[d] < 0) >= k["losing_days"]:
            return f"{k['losing_days']} losing days within {k['window_days']} trading days (from {window[0]})"
    staked = sum(float(t["cost"]) for t in settled)
    elapsed = (now.date() - dt.date.fromisoformat(book["test_start"])).days
    if staked and (elapsed >= k["min_days"] or len(settled) >= k["min_trades"]) and sum(days.values()) < 0:
        return f"return per $ below 0 after {elapsed} days and {len(settled)} trades"
    if now.date() >= end:
        return f"60-day test finished on {end.isoformat()}"
    return None
