"""Historical data for the backtester. All public, no keys.

  Kalshi settled markets + hourly candlesticks (bid/ask/volume per hour)
      recent (~2 months): /markets?status=settled and /series/{s}/markets/{t}/candlesticks
      older:              /historical/markets and /historical/markets/{t}/candlesticks
  Open-Meteo "previous runs" API: what the NWS blend model (NBM) forecast 1 and 2 days ahead,
      hour by hour, for past dates. NWS itself doesn't keep old point forecasts.
  Coinbase hourly candles for Bitcoin.

Everything is cached in data/backtest_cache (gzip json, not committed; GitHub Actions keeps it
between runs), so later runs only download new days.
"""
import datetime as dt
import gzip
import json
import time
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from zoneinfo import ZoneInfo

from .. import config as C
from ..http import get_json

CACHE = C.DATA_DIR / "backtest_cache"
OPEN_METEO = "https://previous-runs-api.open-meteo.com/v1/forecast"
K = C.KALSHI_API
UTC = dt.timezone.utc


def log(msg):
    print(f"[backtest] {msg}", flush=True)


def _load(name, default):
    p = CACHE / f"{name}.json.gz"
    if not p.exists():
        return default
    with gzip.open(p, "rt", encoding="utf-8") as f:
        return json.load(f)


def _save(name, obj):
    CACHE.mkdir(parents=True, exist_ok=True)
    tmp = CACHE / f"{name}.json.gz.tmp"
    with gzip.open(tmp, "wt", encoding="utf-8") as f:
        json.dump(obj, f, separators=(",", ":"))
    tmp.replace(CACHE / f"{name}.json.gz")


def _ts(iso):
    return int(dt.datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp())


def _num(d, *names):
    for n in names:
        v = d.get(n) if isinstance(d, dict) else None
        if v not in (None, ""):
            return float(v)
    return None


def _market_row(m, source):
    return {"ticker": m["ticker"], "event_ticker": m["event_ticker"], "strike_type": m.get("strike_type") or "custom",
            "floor": m.get("floor_strike"), "cap": m.get("cap_strike"), "close_time": m.get("close_time"),
            "result": m.get("result") or "", "value": m.get("expiration_value") or "", "source": source}


def settled_markets(series=None, event_ticker=None, since=None):
    """All settled markets of a series (or one event), newest first, back to `since` (date)."""
    out = {}
    for base, source in ((f"{K}/markets", "live"), (f"{K}/historical/markets", "historical")):
        cursor = None
        while True:
            params = {"limit": 1000}
            if series:
                params["series_ticker"] = series
            if event_ticker:
                params["event_ticker"] = event_ticker
            if source == "live":
                params["status"] = "settled"
            if cursor:
                params["cursor"] = cursor
            try:
                data = get_json(base, params)
            except (RuntimeError, urllib.error.HTTPError) as e:
                log(f"  {base} {series or event_ticker}: {e}")
                break
            ms = data.get("markets") or []
            for m in ms:
                if m.get("result") in ("yes", "no") and m["ticker"] not in out:
                    out[m["ticker"]] = _market_row(m, source)
            cursor = data.get("cursor")
            oldest = min((m.get("close_time") or "9" for m in ms), default="0")
            if not cursor or not ms or (since and oldest[:10] < since.isoformat()):
                break
    rows = list(out.values())
    if since:
        rows = [r for r in rows if (r["close_time"] or "")[:10] >= since.isoformat()]
    return rows


def _parse_candles(data):
    out = []
    for c in data.get("candlesticks") or []:
        bid = _num(c.get("yes_bid", {}), "close_dollars", "close")
        ask = _num(c.get("yes_ask", {}), "close_dollars", "close")
        vol = _num(c, "volume_fp", "volume") or 0.0
        if bid is not None and bid > 1:
            bid /= 100
        if ask is not None and ask > 1:
            ask /= 100
        out.append([int(c["end_period_ts"]), bid, ask, vol])
    return out


def candles(series, m, hours_before=60):
    """Hourly [end_ts, yes_bid, yes_ask, volume] for the last `hours_before` hours before close."""
    end = _ts(m["close_time"])
    params = {"start_ts": end - hours_before * 3600, "end_ts": end, "period_interval": 60}
    urls = [f"{K}/series/{series}/markets/{m['ticker']}/candlesticks", f"{K}/historical/markets/{m['ticker']}/candlesticks"]
    if m["source"] == "historical":
        urls.reverse()
    for u in urls:
        try:
            return _parse_candles(get_json(u, params, retries=5))
        except urllib.error.HTTPError as e:
            if e.code != 404:
                raise
        except RuntimeError:
            time.sleep(2)
    return []


def kalshi_series(series, since, workers=4):
    """Settled markets + candles for one series, using and updating the cache."""
    cached = _load(f"kalshi_{series}", {"markets": {}, "candles": {}})
    rows = settled_markets(series=series, since=since)
    for r in rows:
        cached["markets"][r["ticker"]] = r
    return _fill_candles(series, cached, workers)


def _fill_candles(series, cached, workers, keep=None, deadline=None):
    """deadline (time.time() value): stop early and save what we have; the next run continues."""
    todo = [m for t, m in cached["markets"].items() if t not in cached["candles"] and (keep is None or keep(m))]
    log(f"{series}: {len(cached['markets'])} settled markets, {len(todo)} need candles")

    def job(m):
        try:
            return m["ticker"], candles(series, m)
        except Exception as e:  # keep going; a missing market just isn't traded
            log(f"  candles {m['ticker']}: {e}")
            return m["ticker"], None

    done = 0
    with ThreadPoolExecutor(workers) as ex:
        for i in range(0, len(todo), 500):
            if deadline and time.time() > deadline:
                log(f"  {series}: time budget used up at {done}/{len(todo)}; next run continues")
                break
            for t, cs in ex.map(job, todo[i:i + 500]):
                if cs is not None:
                    cached["candles"][t] = cs
                done += 1
            log(f"  {series}: {done}/{len(todo)}")
            _save(f"kalshi_{series}", cached)
    _save(f"kalshi_{series}", cached)
    return cached


def kalshi_events(series, event_tickers, keep=None, workers=4, deadline=None):
    """Same as kalshi_series but for a list of event tickers (Bitcoin has too many hourly events).
    keep(market) -> bool limits which markets get candles (e.g. strikes near the price)."""
    cached = _load(f"kalshi_{series}", {"markets": {}, "candles": {}, "events": []})
    seen = set(cached.get("events", []))
    for ev in event_tickers:
        if ev in seen:
            continue
        rows = settled_markets(event_ticker=ev)
        for r in rows:
            cached["markets"][r["ticker"]] = r
        if rows:
            seen.add(ev)
    cached["events"] = sorted(seen)
    return _fill_candles(series, cached, workers, keep, deadline)


def nbm_forecasts(code, start, end):
    """{date: {"high": {1: f, 2: f}, "low": {1: f, 2: f}}} - daily max/min of the hourly NBM
    forecast made 1 and 2 days earlier (Open-Meteo previous-runs API), local calendar day."""
    stn = C.STATIONS[code]
    cached = _load(f"nbm_{code}", {})
    have = set(cached)
    d = start
    while d <= end:
        chunk_end = min(end, d + dt.timedelta(days=60))
        days = {(d + dt.timedelta(days=i)).isoformat() for i in range((chunk_end - d).days + 1)}
        # refetch the last few days in case they were incomplete
        if days <= have and chunk_end < end - dt.timedelta(days=3):
            d = chunk_end + dt.timedelta(days=1)
            continue
        data = get_json(OPEN_METEO, {
            "latitude": stn["lat"], "longitude": stn["lon"], "models": "ncep_nbm_conus",
            "hourly": "temperature_2m_previous_day1,temperature_2m_previous_day2",
            "start_date": d.isoformat(), "end_date": chunk_end.isoformat(),
            "temperature_unit": "fahrenheit", "timezone": stn["tz"]}, retries=5, timeout=60)
        h = data.get("hourly") or {}
        per = {}
        for i, t in enumerate(h.get("time", [])):
            day = t[:10]
            for lead in (1, 2):
                v = (h.get(f"temperature_2m_previous_day{lead}") or [None] * (i + 1))[i]
                if v is not None:
                    per.setdefault(day, {}).setdefault(lead, []).append(v)
        for day, leads in per.items():
            rec = {"high": {}, "low": {}}
            for lead, vals in leads.items():
                if len(vals) >= 20:  # need most of the day
                    rec["high"][str(lead)] = round(max(vals), 1)
                    rec["low"][str(lead)] = round(min(vals), 1)
            cached[day] = rec
        d = chunk_end + dt.timedelta(days=1)
        time.sleep(0.5)
    _save(f"nbm_{code}", cached)
    return cached


def coinbase_hourly(product, start, end):
    """{close_ts: close price} from Coinbase hourly candles. Keyed by the candle's END time
    (start + 1h) so a lookup at time t never sees a price from after t."""
    cached = {int(k): v for k, v in _load(f"coinbase_close_{product}", {}).items()}
    t = int(dt.datetime.combine(start, dt.time(), UTC).timestamp())
    stop = int(dt.datetime.combine(end + dt.timedelta(days=1), dt.time(), UTC).timestamp())
    step = 300 * 3600
    while t < stop:
        e = min(stop, t + step)
        if all(h + 3600 in cached for h in range(t, e, 3600)) and e < stop - 86400:
            t = e
            continue
        rows = get_json(f"{C.COINBASE_API}/products/{product}/candles", {
            "granularity": 3600, "start": dt.datetime.fromtimestamp(t, UTC).isoformat(),
            "end": dt.datetime.fromtimestamp(e, UTC).isoformat()}, retries=5)
        for r in rows:
            cached[int(r[0]) + 3600] = float(r[4])
        t = e
        time.sleep(0.35)
    _save(f"coinbase_close_{product}", {str(k): v for k, v in cached.items()})
    return cached


def btc_event_tickers(start, end, suffix="17", series="KXBTCD"):
    out, d = [], start
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    while d <= end:
        out.append(f"{series}-{d:%y}{months[d.month - 1]}{d:%d}{suffix}")
        d += dt.timedelta(days=1)
    return out


def local_ts(day, hour, tz):
    return int(dt.datetime(day.year, day.month, day.day, hour, tzinfo=ZoneInfo(tz)).timestamp())
