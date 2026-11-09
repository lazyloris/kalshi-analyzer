"""Price-ladder markets beyond Bitcoin: does "the market overprices big moves" hold elsewhere?

Same model as the Bitcoin book (lognormal around the latest price, 30-day realized volatility,
volatility scaled down), run on Ethereum, gold, silver, oil, natural gas, the S&P 500 and the Nasdaq.

Prices:
  Ethereum: Coinbase hourly (same as Bitcoin).
  Everything else: Yahoo Finance hourly bars (futures / index). Kalshi may settle on a slightly
  different number (spot vs front-month future), so each event learns a "basis" = Kalshi's
  settlement value / our price at close, from EARLIER events only (median of the last 15).

Time to close is measured from the last price we actually had (markets close overnight and on
weekends), and volatility comes from calendar-day returns, so the two use the same clock.
"""
import bisect
import datetime as dt
import json
import math
import statistics
import time
import urllib.parse
from zoneinfo import ZoneInfo
import urllib.request
from collections import defaultdict

from . import data as D
from . import engine as E

UTC = dt.timezone.utc
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/"
BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"

# id: name, Kalshi series (missing ones are skipped), price source, strike band for candles.
# Some series have an event EVERY HOUR (KXETHD: ~1M markets), so we keep one close per day:
# daily_events = event tickers built like Bitcoin's 5pm ones; close_hour = ET hour to keep
# (default: the most common close hour in the series).
ET = ZoneInfo("America/New_York")
ASSETS = {
    "eth": {"name": "Ethereum", "series": ["KXETHD"], "src": ("coinbase", "ETH-USD"), "band": 0.06,
            "daily_events": "17"},
    "gold": {"name": "Gold", "series": ["KXGOLDD"], "src": ("yahoo", "GC=F"), "band": 0.03},
    "silver": {"name": "Silver", "series": ["KXSILVERD"], "src": ("yahoo", "SI=F"), "band": 0.05},
    "wti": {"name": "WTI oil", "series": ["KXWTI"], "src": ("yahoo", "CL=F"), "band": 0.05},
    "brent": {"name": "Brent oil", "series": ["KXBRENTD"], "src": ("yahoo", "BZ=F"), "band": 0.05},
    "natgas": {"name": "Natural gas", "series": ["KXNATGASD"], "src": ("yahoo", "NG=F"), "band": 0.08},
    "spx": {"name": "S&P 500", "series": ["KXINX", "KXINXU"], "src": ("yahoo", "^GSPC"), "band": 0.03, "close_hour": 16},
    "ndx": {"name": "Nasdaq 100", "series": ["KXNASDAQ100", "KXNASDAQ100U"], "src": ("yahoo", "^NDX"), "band": 0.035,
            "close_hour": 16},
}
ENTRIES = ((8, "8h before"), (4, "4h before"), (1, "1h before"))
SPOT_MAX_AGE = 20 * 3600     # overnight gap is fine; we count time from the price we had
HIST_MAX_AGE = 4 * 86400     # weekends/holidays for the daily-return history
BASIS_N, BASIS_MIN = 15, 5


def price_file(aid):
    kind, sym = ASSETS[aid]["src"]
    return f"coinbase_close_{sym}" if kind == "coinbase" else f"yahoo_close_{sym}"


# ---------------------------------------------------------------- download

def yahoo_hourly(symbol, start, end):
    """{close_ts: price} from Yahoo hourly bars, keyed by bar END (start + 1h): never looks ahead."""
    name = f"yahoo_close_{symbol}"
    cached = {int(k): v for k, v in D._load(name, {}).items()}
    p1 = int(dt.datetime.combine(start, dt.time(), UTC).timestamp())
    p2 = int(dt.datetime.combine(end + dt.timedelta(days=1), dt.time(), UTC).timestamp())
    step = 90 * 86400
    t = p1
    while t < p2:
        e = min(p2, t + step)
        q = urllib.parse.urlencode({"period1": t, "period2": e, "interval": "60m", "includePrePost": "false"})
        req = urllib.request.Request(f"{YAHOO}{urllib.parse.quote(symbol)}?{q}", headers={"User-Agent": BROWSER_UA})
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    res = json.loads(r.read())["chart"]["result"][0]
                break
            except Exception as ex:
                if attempt == 4:
                    raise RuntimeError(f"Yahoo {symbol}: {ex}")
                time.sleep(3 * 2 ** attempt)
        closes = (res.get("indicators", {}).get("quote") or [{}])[0].get("close") or []
        for ts, c in zip(res.get("timestamp") or [], closes):
            if c is not None:
                cached[int(ts) + 3600] = float(c)
        t = e
        time.sleep(1)
    D._save(name, {str(k): v for k, v in cached.items()})
    return cached


def prices_for(aid, start, end):
    kind, sym = ASSETS[aid]["src"]
    if kind == "coinbase":
        return D.coinbase_hourly(sym, start, end)
    return yahoo_hourly(sym, start, end)


def _close_hour(m):
    return dt.datetime.fromtimestamp(D._ts(m["close_time"]), ET).hour


def one_close_per_day(markets, hour=None):
    """Drop intraday events: keep markets closing at `hour` ET (default: the most common hour)."""
    if not markets:
        return markets
    if hour is None:
        counts = defaultdict(int)
        for m in markets.values():
            counts[_close_hour(m)] += 1
        hour = max(counts, key=counts.get)
    return {t: m for t, m in markets.items() if _close_hour(m) == hour}


def fetch(days=240, only=None, budget_min=100):
    deadline = time.time() + budget_min * 60
    end = dt.date.today()
    start = end - dt.timedelta(days=days)
    for aid, a in ASSETS.items():
        if only and aid not in only:
            continue
        try:
            D.log(f"{a['name']}: prices")
            prices = prices_for(aid, start - dt.timedelta(days=40), end)
            hours = sorted(prices)
            D.log(f"{a['name']}: {len(prices)} hourly prices")
        except Exception as e:
            D.log(f"{a['name']}: price download failed, skipping: {e}")
            continue

        def near(m, band=a["band"]):  # only strikes near the price 8h before close get candles
            k = E._f(m["floor"]) or E._f(m["cap"])
            spot = price_at(prices, hours, D._ts(m["close_time"]) - 8 * 3600, SPOT_MAX_AGE)
            return k is not None and spot is not None and abs(k / spot[1] - 1) <= band

        for s in a["series"]:
            if time.time() > deadline:
                D.log(f"time budget used up; {s} waits for the next run")
                continue
            try:
                if a.get("daily_events"):
                    D.kalshi_events(s, D.btc_event_tickers(start, end - dt.timedelta(days=1), a["daily_events"], s),
                                    keep=near, deadline=deadline)
                    continue
                cached = D._load(f"kalshi_{s}", {"markets": {}, "candles": {}})
                rows = D.settled_markets(series=s, since=start)
                for r in rows:
                    cached["markets"][r["ticker"]] = r
                if not cached["markets"]:
                    D.log(f"{s}: no settled markets (series may not exist)")
                    continue
                before = len(cached["markets"])
                cached["markets"] = one_close_per_day(cached["markets"], a.get("close_hour"))
                D.log(f"{s}: kept {len(cached['markets'])} of {before} markets (one close per day)")
                D._fill_candles(s, cached, 4, keep=near, deadline=deadline)
            except Exception as e:
                D.log(f"{s}: failed: {e}")


# ---------------------------------------------------------------- events

def price_at(prices, hours, ts, max_age):
    """(price_ts, price) of the last close at or before ts, if not older than max_age."""
    i = bisect.bisect_right(hours, ts) - 1
    if i < 0 or ts - hours[i] > max_age:
        return None
    return hours[i], prices[hours[i]]


def realized_vol(prices, hours, ts, days=30):
    pts = [price_at(prices, hours, ts - k * 86400, HIST_MAX_AGE) for k in range(days + 1)]
    if None in pts:
        return None
    px = [p for _, p in reversed(pts)]
    rets = [math.log(b / a) for a, b in zip(px, px[1:])]
    return statistics.stdev(rets) * math.sqrt(365) if len(rets) > 2 else None


def asset_events(aid, data_by_series, prices):
    """One event per (Kalshi event, entry time), like engine.crypto_events, plus learned basis."""
    a = ASSETS[aid]
    hours = sorted(prices)
    by_event = defaultdict(list)
    for s, data in data_by_series.items():
        daily = one_close_per_day((data or {}).get("markets", {}), a.get("close_hour") or (17 if a.get("daily_events") else None))
        for m in daily.values():
            by_event[(s, m["event_ticker"])].append((m, data["candles"]))
    # settlement basis history: (close_ts, actual / our price at close)
    basis_hist = []
    for (s, ev), ms in by_event.items():
        close = max(D._ts(m["close_time"]) for m, _ in ms)
        actual = next((E._f(m["value"]) for m, _ in ms if E._f(m["value"])), None)
        px = price_at(prices, hours, close, SPOT_MAX_AGE)
        if actual and px:
            r = actual / px[1]
            if 0.9 < r < 1.1:  # ignore broken values
                basis_hist.append((close, r))
    basis_hist.sort()
    basis_ts = [t for t, _ in basis_hist]
    out = []
    for (s, ev), ms in by_event.items():
        close = max(D._ts(m["close_time"]) for m, _ in ms)
        for hrs, name in ENTRIES:
            ts = close - hrs * 3600
            px = price_at(prices, hours, ts, SPOT_MAX_AGE)
            vol = realized_vol(prices, hours, ts)
            j = bisect.bisect_right(basis_ts, ts - 3600)  # only events settled before entry
            past = [r for _, r in basis_hist[max(0, j - BASIS_N):j]]
            if px is None or not vol or len(past) < BASIS_MIN:
                continue
            basis = statistics.median(past)
            spot = px[1] * basis
            left = (close - px[0]) / 3600
            mk = []
            for m, cands in ms:
                if m["strike_type"] not in ("between", "greater", "less", "greater_or_equal"):
                    continue
                k = E._f(m["floor"]) or E._f(m["cap"])
                if k is None or abs(k / spot - 1) > a["band"]:
                    continue
                q = E.quote(cands.get(m["ticker"], []), ts)
                if q is None:
                    continue
                mk.append({**m, "bid": q[0], "ask": q[1], "vol24": q[2], "won_yes": m["result"] == "yes"})
            if mk:
                out.append({"book": f"asset_{aid}", "kind": "crypto", "series": s, "code": aid, "city": s,
                            "event": ev, "date": dt.datetime.fromtimestamp(close, UTC).date().isoformat(),
                            "entry": name, "ts": ts, "hours": left, "spot": spot, "vol": vol, "basis": basis,
                            "markets": mk})
    out.sort(key=lambda e: e["ts"])
    return out


def load(aid):
    a = ASSETS[aid]
    data = {s: D._load(f"kalshi_{s}", None) for s in a["series"]}
    data = {s: v for s, v in data.items() if v and v.get("markets")}
    prices = {int(k): v for k, v in D._load(price_file(aid), {}).items()}
    return data, prices


def strategies():
    p = lambda k: (lambda e, m: E.p_crypto(e, m, k))
    return [
        ("a_v1", "Full vol (v1 rule)", "Lognormal around the latest price, 30-day realized vol, 8c edge", E.edge_picker(p(1.0))),
        ("a_vol75", "Vol x0.75", "Same, volatility scaled down 25%", E.edge_picker(p(0.75))),
        ("a_vol50", "Vol x0.5 (Bitcoin's winner)", "Same, volatility halved", E.edge_picker(p(0.5))),
        ("a_vol50_e5", "Vol x0.5, 5c edge", "Halved volatility, lower edge bar", E.edge_picker(p(0.5), min_edge=0.05)),
        ("a_vol50_no", "Vol x0.5, NO only", "Halved volatility, only bet against moves", E.edge_picker(p(0.5), sides=("no",))),
        ("a_blend", "Full vol + 50% market blend", "Average our chance with the market price; 4c edge",
         E.edge_picker(p(1.0), min_edge=0.04, blend=0.5)),
        ("a_fade", "Long-shot fade (no model)", "Buy NO when YES costs 3-10c", E.longshot_fade()),
        ("a_fav", "Market favorite (no model)", "Buy YES on the market's favorite at 35-75c", E.market_favorite()),
    ]


def sweeps():
    return {"vol": [(k, E.edge_picker(lambda e, m, k=k: E.p_crypto(e, m, k))) for k in (0.3, 0.4, 0.5, 0.6, 0.75, 1.0)]}


def books(strategy_result):
    """{book_id: result} for every asset with data, in the backtest.json book format."""
    out = {}
    for aid, a in ASSETS.items():
        data, prices = load(aid)
        if not data or not prices:
            continue
        evs = asset_events(aid, data, prices)
        if not evs:
            D.log(f"{a['name']}: no usable events")
            continue
        bid = f"asset_{aid}"
        out[bid] = {
            "name": a["name"], "events": len({e["event"] for e in evs}),
            "first": evs[0]["date"], "last": evs[-1]["date"],
            "series": sorted(data), "basis": round(statistics.median(e["basis"] for e in evs), 4),
            "strategies": [strategy_result(sid, name, desc, bid, E.simulate(evs, pick))
                           for sid, name, desc, pick in strategies()],
            "sweeps": {"vol": [{"mult": k, **E.metrics(E.simulate(evs, p))} for k, p in sweeps()["vol"]]},
            "market_calibration": E.market_calibration(evs),
        }
    return out
