"""Replay past Kalshi markets against what we could have known at the time, for several strategies.

No look-ahead:
  - prices are the last hourly candle (bid/ask) at or before the entry time
  - weather forecasts are NBM runs made 1-2 days earlier (older than what we'd really have, so
    results are, if anything, a little pessimistic)
  - bias and sigma are learned only from days that had already settled before the entry
Every trade is a flat $10 at the ask plus the Kalshi taker fee, held to settlement.
"""
import datetime as dt
import math
import statistics
from collections import defaultdict
from zoneinfo import ZoneInfo

from .. import config as C
from ..kalshi import target_date_from_event
from ..model import bracket_probability, calibrate_errors, lognormal_probability, taker_fee

STAKE = 10.0
# (name, day offset from target date, local hour, days ahead for sigma, NBM forecast age in days)
ENTRIES = {
    "high": [("same day 8am", 0, 8, 0, 1), ("day before 10am", -1, 10, 1, 2)],
    "low": [("day before 8pm", -1, 20, 1, 1), ("day before 10am", -1, 10, 1, 2)],
}
DEFAULT_SIGMA = {0: 1.5, 1: 2.0, 2: 2.8}
V1_SIGMA = {0: 2.0, 1: 2.5, 2: 3.2}


def _f(v):
    try:
        return None if v in (None, "") else float(v)
    except (TypeError, ValueError):  # e.g. expiration_value "No" on some markets
        return None


def quote(cs, ts, max_age_h=6):
    """Last (bid, ask, volume_24h) at or before ts, or None if no two-sided market."""
    best, vol = None, 0.0
    for c in cs:
        if c[0] <= ts:
            if c[0] >= ts - 24 * 3600:
                vol += c[3] or 0
            if c[0] >= ts - max_age_h * 3600 and (best is None or c[0] > best[0]):
                best = c
    if not best or best[1] is None or best[2] is None:
        return None
    bid, ask = best[1], best[2]
    if bid <= 0 or ask >= 1 or ask <= bid - 1e-9:
        return None
    return bid, ask, vol


# ---------------------------------------------------------------- decision points

def weather_events(book_id, kalshi_by_series, nbm_by_code):
    """One record per (event, entry): markets with quotes, forecast, actual. Sorted by entry time."""
    book = C.BOOKS[book_id]
    out = []
    for series, code in book["series"].items():
        data = kalshi_by_series.get(series)
        if not data:
            continue
        stn, nbm = C.STATIONS[code], nbm_by_code.get(code, {})
        by_event = defaultdict(list)
        for t, m in data["markets"].items():
            by_event[m["event_ticker"]].append(m)
        for ev, ms in by_event.items():
            try:
                day = target_date_from_event(ev)
            except (ValueError, KeyError, IndexError):
                continue
            actual = next((_f(m["value"]) for m in ms if _f(m["value"]) is not None), None)
            if actual is None:
                continue
            for name, off, hour, lead_days, fc_age in ENTRIES[book["extreme"]]:
                d = day + dt.timedelta(days=off)
                ts = int(dt.datetime(d.year, d.month, d.day, hour, tzinfo=ZoneInfo(stn["tz"])).timestamp())
                fc = (nbm.get(day.isoformat(), {}).get(book["extreme"], {}) or {}).get(str(fc_age))
                mk = []
                for m in ms:
                    if m["strike_type"] not in ("between", "greater", "less", "greater_or_equal"):
                        continue
                    q = quote(data["candles"].get(m["ticker"], []), ts)
                    if q is None:
                        continue
                    mk.append({**m, "bid": q[0], "ask": q[1], "vol24": q[2], "won_yes": m["result"] == "yes",
                               "cs": data["candles"].get(m["ticker"], [])})
                if mk:
                    out.append({"book": book_id, "kind": "weather", "series": series, "code": code,
                                "city": stn["city"], "event": ev, "date": day.isoformat(), "entry": name,
                                "ts": ts, "lead_days": lead_days, "forecast": fc, "actual": actual, "markets": mk})
    out.sort(key=lambda e: e["ts"])
    return out


def calibrate(events, window_days=60, prior_n=10):
    """Add walk-forward bias/sigma to each weather event, from earlier settled days only."""
    hist = defaultdict(list)  # (series, entry) -> [(settled_ts, error)]
    for e in events:
        key = (e["series"], e["entry"])
        cutoff = e["ts"] - window_days * 86400
        errs = [err for ts, err in hist[key] if cutoff <= ts <= e["ts"]]
        bias, sigma, n = calibrate_errors(errs, DEFAULT_SIGMA[e["lead_days"]], prior_n)
        e["bias"], e["sigma"], e["calib_n"] = bias, sigma, n
        if e["forecast"] is not None:
            # result is public the next morning after the target day
            settled = int(dt.datetime.fromisoformat(e["date"]).replace(tzinfo=dt.timezone.utc).timestamp()) + 36 * 3600
            hist[key].append((settled, e["actual"] - e["forecast"]))
    return events


def crypto_events(series, data, prices, entries=((8, "8h before"), (4, "4h before"))):
    """Bitcoin 5pm ET events. Spot = Coinbase hourly close; vol = 30-day realized from daily closes."""
    hours = sorted(prices)
    out = []
    by_event = defaultdict(list)
    for m in data["markets"].values():
        by_event[m["event_ticker"]].append(m)
    for ev, ms in by_event.items():
        close = max(int(dt.datetime.fromisoformat(m["close_time"].replace("Z", "+00:00")).timestamp()) for m in ms)
        actual = next((_f(m["value"]) for m in ms if _f(m["value"]) is not None), None)
        for hrs, name in entries:
            ts = close - hrs * 3600
            spot = _price_at(prices, hours, ts)
            daily = [_price_at(prices, hours, ts - k * 86400) for k in range(31)]
            if spot is None or None in daily:
                continue
            daily.reverse()
            rets = [math.log(b / a) for a, b in zip(daily, daily[1:])]
            vol = statistics.stdev(rets) * math.sqrt(365)
            mk = []
            for m in ms:
                if m["strike_type"] not in ("between", "greater", "less", "greater_or_equal"):
                    continue
                k = _f(m["floor"]) or _f(m["cap"])
                if k is None or abs(k / spot - 1) > 0.04:
                    continue
                q = quote(data["candles"].get(m["ticker"], []), ts)
                if q is None:
                    continue
                mk.append({**m, "bid": q[0], "ask": q[1], "vol24": q[2], "won_yes": m["result"] == "yes",
                               "cs": data["candles"].get(m["ticker"], [])})
            if mk:
                out.append({"book": "bitcoin", "kind": "crypto", "series": series, "code": "BTC", "city": "Bitcoin",
                            "event": ev, "date": dt.datetime.fromtimestamp(close, dt.timezone.utc).date().isoformat(),
                            "entry": name, "ts": ts, "hours": hrs, "spot": spot, "vol": vol, "actual": actual,
                            "markets": mk})
    out.sort(key=lambda e: e["ts"])
    return out


def _price_at(prices, hours, ts):
    import bisect
    i = bisect.bisect_right(hours, ts) - 1
    if i < 0 or ts - hours[i] > 3 * 3600:
        return None
    return prices[hours[i]]


# ---------------------------------------------------------------- probability models

def p_weather(e, m, sigma_mult=1.0, fixed=None, use_bias=True):
    if e["forecast"] is None:
        return None
    mu = e["forecast"] + (e["bias"] if use_bias else 0.0)
    sigma = (fixed or {}).get(e["lead_days"]) if fixed else e["sigma"] * sigma_mult
    return bracket_probability(m["strike_type"], _f(m["floor"]), _f(m["cap"]), mu, sigma)


def p_crypto(e, m, vol_mult=1.0):
    return lognormal_probability(m["strike_type"], _f(m["floor"]), _f(m["cap"]), e["spot"], e["vol"] * vol_mult, e["hours"])


def p_iv(e, m, mult=1.0):
    """Same lognormal, but with the OPTIONS market's implied volatility at entry time."""
    if not e.get("ivol"):
        return None
    return lognormal_probability(m["strike_type"], _f(m["floor"]), _f(m["cap"]), e["spot"], e["ivol"] * mult, e["hours"])


def attach_ivol(events, iv, max_age=26 * 3600):
    """iv = {close_ts: implied vol in % (e.g. DVOL 45 or VIX 18)}. Sets e["ivol"] (fraction) from
    the last value at or before entry; never a later one."""
    hours = sorted(iv)
    n = 0
    for e in events:
        v = _price_at_age(iv, hours, e["ts"], max_age) if hours else None
        e["ivol"] = v / 100 if v else None
        n += bool(v)
    return n


def _price_at_age(prices, hours, ts, max_age):
    import bisect
    i = bisect.bisect_right(hours, ts) - 1
    if i < 0 or ts - hours[i] > max_age:
        return None
    return prices[hours[i]]


def iv_strategies():
    """Trade only when Kalshi's price disagrees with what the options market implies."""
    p = lambda k: (lambda e, m: p_iv(e, m, k))
    return [
        ("iv_5", "Options vol, 5c gap", "Chance from options-implied volatility; trade when Kalshi is off by 5c+ after fees",
         edge_picker(p(1.0), min_edge=0.05)),
        ("iv_8", "Options vol, 8c gap", "Same, bigger gap required", edge_picker(p(1.0), min_edge=0.08)),
        ("iv_no", "Options vol, NO only", "Only bet against moves Kalshi overprices vs options, 5c gap",
         edge_picker(p(1.0), min_edge=0.05, sides=("no",))),
        ("iv_85", "Options vol x0.85, 5c gap", "Options usually overstate the real move a bit (risk premium); shrink 15%",
         edge_picker(p(0.85), min_edge=0.05)),
    ]


def iv_sweeps():
    return [(k, edge_picker(lambda e, m, k=k: p_iv(e, m, k), min_edge=0.05)) for k in (0.6, 0.7, 0.8, 0.9, 1.0, 1.1)]


def mid(m):
    return (m["bid"] + m["ask"]) / 2


# ---------------------------------------------------------------- trade pickers

def _trade(e, m, side, p_side):
    ask = m["ask"] if side == "yes" else 1 - m["bid"]
    bid = m["bid"] if side == "yes" else 1 - m["ask"]
    contracts = max(1, math.floor(STAKE / ask))
    fee = taker_fee(contracts, ask, C.FEE_RATE)
    cost = contracts * ask + fee
    won = m["won_yes"] if side == "yes" else not m["won_yes"]
    mkt = (ask + bid) / 2
    return {"date": e["date"], "ts": e["ts"], "series": e["series"], "city": e["city"], "entry": e["entry"],
            "ticker": m["ticker"], "side": side, "price": round(ask, 4), "contracts": contracts, "fee": fee,
            "cost": round(cost, 4), "p_model": round(p_side, 4) if p_side is not None else None,
            "p_market": round(mkt, 4), "edge": round((p_side or mkt) - ask - fee / contracts, 4),
            "won": bool(won), "pnl": round((contracts if won else 0) - cost, 4)}


def edge_picker(prob, min_edge=0.08, blend=0.0, max_gap=None, min_price=0.05, max_price=0.90,
                max_spread=0.10, max_per_event=2, sides=("yes", "no")):
    """The live rule: buy the side where (our chance - price - fee) >= min_edge.
    blend = weight on the market's own price (0 = pure model). max_gap = skip if model and market
    disagree by more than this (big gaps are usually the model being wrong)."""
    def pick(e):
        cands = []
        for m in e["markets"]:
            p_yes = prob(e, m)
            if p_yes is None or m["ask"] - m["bid"] > max_spread:
                continue
            p_mkt = mid(m)
            if max_gap is not None and abs(p_yes - p_mkt) > max_gap:
                continue
            p_use = (1 - blend) * p_yes + blend * p_mkt
            for side in sides:
                ask = m["ask"] if side == "yes" else 1 - m["bid"]
                p = p_use if side == "yes" else 1 - p_use
                if not (min_price <= ask <= max_price):
                    continue
                c = max(1, math.floor(STAKE / ask))
                edge = p - ask - taker_fee(c, ask, C.FEE_RATE) / c
                if edge >= min_edge:
                    cands.append((edge, m, side, p))
        cands.sort(key=lambda x: -x[0])
        out, used = [], set()
        for edge, m, side, p in cands:
            if m["ticker"] in used:
                continue
            used.add(m["ticker"])
            out.append(_trade(e, m, side, p))
            if len(out) >= max_per_event:
                break
        return out
    return pick


def forecast_bracket(min_edge=0.05, max_price=0.70):
    """Buy YES on the single bracket our (calibrated) model thinks is most likely, if it's cheap enough."""
    def pick(e):
        ps = [(p_weather(e, m), m) for m in e["markets"] if m["strike_type"] == "between"]
        ps = [(p, m) for p, m in ps if p is not None]
        if not ps:
            return []
        p, m = max(ps, key=lambda x: x[0])
        c = max(1, math.floor(STAKE / m["ask"]))
        if m["ask"] <= max_price and m["ask"] - m["bid"] <= 0.10 and p - m["ask"] - taker_fee(c, m["ask"], C.FEE_RATE) / c >= min_edge:
            return [_trade(e, m, "yes", p)]
        return []
    return pick


def market_favorite(lo=0.35, hi=0.75):
    """Control: buy YES on whatever the market already thinks is most likely. No model at all."""
    def pick(e):
        ms = [m for m in e["markets"] if m["ask"] - m["bid"] <= 0.10]
        if not ms:
            return []
        m = max(ms, key=mid)
        return [_trade(e, m, "yes", None)] if lo <= m["ask"] <= hi else []
    return pick


def longshot_fade(lo=0.03, hi=0.10):
    """Buy NO on cheap long shots (YES at 3-10c). No model: tests whether long shots are overpriced."""
    def pick(e):
        out = []
        for m in e["markets"]:
            if lo <= m["bid"] and m["ask"] <= hi and m["ask"] - m["bid"] <= 0.05:
                out.append(_trade(e, m, "no", None))
        return out[:2]
    return pick


# ---------------------------------------------------------------- strategy catalogue

def weather_strategies():
    v1 = lambda e, m: p_weather(e, m, fixed=V1_SIGMA, use_bias=False)
    v2 = lambda e, m: p_weather(e, m)
    return [
        ("v1", "v1 (what we ran live)", "Normal curve around the forecast, fixed sigma 2.0/2.5F, no bias, 8c edge",
         edge_picker(v1)),
        ("v2", "v2 calibrated", "Same, but bias and sigma learned from past forecast misses",
         edge_picker(v2)),
        ("v2_blend", "v2 + 50% market blend", "Average our chance with the market price; 4c edge",
         edge_picker(v2, min_edge=0.04, blend=0.5)),
        ("v2_cap", "v2 + disagreement cap", "v2, but skip when model and market disagree by more than 25 points",
         edge_picker(v2, max_gap=0.25)),
        ("fc_bracket", "Forecast bracket YES", "Buy YES on the bracket the calibrated forecast points at, if it costs 70c or less with 5c+ edge",
         forecast_bracket()),
        ("favorite", "Market favorite YES (no model)", "Buy YES on the market's top bracket when it costs 35-75c",
         market_favorite()),
        ("fade", "Long-shot fade (no model)", "Buy NO when YES costs 3-10c",
         longshot_fade()),
    ]


def weather_sweeps():
    out = {"sigma": [], "blend": []}
    for k in (0.6, 0.8, 1.0, 1.25, 1.5):
        out["sigma"].append((k, edge_picker(lambda e, m, k=k: p_weather(e, m, sigma_mult=k))))
    for w in (0.0, 0.25, 0.5, 0.75):
        for edge in (0.03, 0.05, 0.08):
            out["blend"].append(((w, edge), edge_picker(lambda e, m: p_weather(e, m), min_edge=edge, blend=w)))
    return out


def crypto_strategies():
    return [
        ("c_v1", "v1 (what we ran live)", "Lognormal around Coinbase price, 30-day realized vol, 8c edge",
         edge_picker(lambda e, m: p_crypto(e, m))),
        ("c_vol75", "Vol x0.75", "Same, but volatility scaled down 25%", edge_picker(lambda e, m: p_crypto(e, m, 0.75))),
        ("c_vol50", "Vol x0.5", "Same, but volatility halved", edge_picker(lambda e, m: p_crypto(e, m, 0.5))),
        ("c_blend", "v1 + 50% market blend", "Average our chance with the market price; 4c edge",
         edge_picker(lambda e, m: p_crypto(e, m), min_edge=0.04, blend=0.5)),
        ("c_fade", "Long-shot fade (no model)", "Buy NO when YES costs 3-10c", longshot_fade()),
    ]


def crypto_sweeps():
    return {"vol": [(k, edge_picker(lambda e, m, k=k: p_crypto(e, m, k))) for k in (0.4, 0.5, 0.6, 0.75, 1.0, 1.25)]}


# ---------------------------------------------------------------- simulate + score

def simulate(events, picker, entry=None):
    trades = []
    for e in events:
        if entry and e["entry"] != entry:
            continue
        trades.extend(picker(e))
    return trades


def metrics(trades):
    n = len(trades)
    if not n:
        return {"trades": 0, "wins": 0, "win_rate": None, "pnl": 0.0, "staked": 0.0, "roi": None,
                "avg_price": None, "avg_claimed": None, "brier_model": None, "brier_market": None,
                "max_drawdown": 0.0, "t_stat": None, "first_half": 0.0, "second_half": 0.0,
                "roi_ci": None, "holdout": None}
    trades = sorted(trades, key=lambda t: t["ts"])
    pnl = [t["pnl"] for t in trades]
    staked = sum(t["cost"] for t in trades)
    cum, peak, dd = 0.0, 0.0, 0.0
    for x in pnl:
        cum += x
        peak = max(peak, cum)
        dd = min(dd, cum - peak)
    rets = [t["pnl"] / t["cost"] for t in trades]
    sd = statistics.stdev(rets) if n > 1 else 0
    pm = [t for t in trades if t["p_model"] is not None]
    half = n // 2
    return {
        "trades": n, "wins": sum(t["won"] for t in trades), "win_rate": round(sum(t["won"] for t in trades) / n, 3),
        "pnl": round(sum(pnl), 2), "staked": round(staked, 2), "roi": round(sum(pnl) / staked, 4),
        "avg_price": round(statistics.fmean(t["price"] for t in trades), 3),
        "avg_claimed": round(statistics.fmean(t["p_model"] for t in pm), 3) if pm else None,
        "brier_model": round(statistics.fmean((t["p_model"] - t["won"]) ** 2 for t in pm), 4) if pm else None,
        "brier_market": round(statistics.fmean((t["p_market"] - t["won"]) ** 2 for t in trades), 4),
        "max_drawdown": round(dd, 2),
        "t_stat": round(statistics.fmean(rets) / sd * math.sqrt(n), 2) if sd else None,
        "first_half": round(sum(pnl[:half]), 2), "second_half": round(sum(pnl[half:]), 2),
        "roi_ci": roi_ci(trades),
        "holdout": holdout(trades),
    }


HOLDOUT_DAYS = 60


def roi_ci(trades, n_boot=400, seed=7):
    """90% bootstrap range for return per $ staked (resampling trades)."""
    import random
    if len(trades) < 10:
        return None
    rnd = random.Random(seed)
    pnl = [t["pnl"] for t in trades]
    cost = [t["cost"] for t in trades]
    n, sims = len(trades), []
    for _ in range(n_boot):
        idx = [rnd.randrange(n) for _ in range(n)]
        sims.append(sum(pnl[i] for i in idx) / sum(cost[i] for i in idx))
    sims.sort()
    return [round(sims[int(0.05 * n_boot)], 4), round(sims[int(0.95 * n_boot) - 1], 4)]


def holdout(trades, days=HOLDOUT_DAYS):
    """Result on the most recent `days` only: settings were chosen before looking at this part,
    so it's the fairest guess of live performance. (From the 2026-11-08 run on, pick settings on
    the earlier part and only read this at the end.)"""
    if not trades:
        return None
    last = max(t["date"] for t in trades)
    cut = (dt.date.fromisoformat(last) - dt.timedelta(days=days)).isoformat()
    h = [t for t in trades if t["date"] > cut]
    if not h:
        return None
    staked = sum(t["cost"] for t in h)
    return {"from": cut, "trades": len(h), "pnl": round(sum(t["pnl"] for t in h), 2),
            "roi": round(sum(t["pnl"] for t in h) / staked, 4) if staked else None}


def curve(trades):
    by_day = defaultdict(float)
    for t in trades:
        by_day[t["date"]] += t["pnl"]
    out, cum = [], 0.0
    for d in sorted(by_day):
        cum += by_day[d]
        out.append([d, round(cum, 2)])
    return out


def breakdown(trades, key):
    g = defaultdict(list)
    for t in trades:
        g[t[key]].append(t)
    return {k: {"trades": len(v), "pnl": round(sum(x["pnl"] for x in v), 2),
                "win_rate": round(sum(x["won"] for x in v) / len(v), 3)} for k, v in sorted(g.items())}


def forecast_errors(events):
    """How far off the archived NBM forecast was, per city and entry (one record per event+entry)."""
    g = defaultdict(list)
    for e in events:
        if e["forecast"] is not None:
            g[(e["city"], e["entry"])].append(e["actual"] - e["forecast"])
    out = []
    for (city, entry), errs in sorted(g.items()):
        out.append({"city": city, "entry": entry, "n": len(errs), "bias": round(statistics.fmean(errs), 2),
                    "rmse": round(math.sqrt(statistics.fmean([x * x for x in errs])), 2),
                    "stdev": round(statistics.stdev(errs), 2) if len(errs) > 1 else None})
    return out


def market_calibration(events, buckets=(0, .05, .1, .2, .3, .4, .5, .6, .7, .8, .9, .95, 1.0001)):
    """Across every quoted market: when the market said X%, how often did YES win?"""
    g = defaultdict(lambda: [0, 0, 0.0])
    seen = set()
    for e in events:
        for m in e["markets"]:
            key = (m["ticker"], e["entry"])
            if key in seen:
                continue
            seen.add(key)
            p = mid(m)
            for lo, hi in zip(buckets, buckets[1:]):
                if lo <= p < hi:
                    b = g[(lo, hi)]
                    b[0] += 1
                    b[1] += m["won_yes"]
                    b[2] += p
                    break
    return [{"range": f"{lo * 100:.0f}-{min(hi, 1) * 100:.0f}c", "n": n, "market": round(sp / n, 3),
             "actual": round(w / n, 3)} for (lo, hi), (n, w, sp) in sorted(g.items()) if n]
