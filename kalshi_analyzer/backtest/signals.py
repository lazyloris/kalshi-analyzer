"""Extra signals on top of the price-ladder model (Bitcoin, Ethereum, other assets) and weather.

1. Limit orders ("maker"): instead of paying the ask, post 1c above the bid and only count the
   trade if a LATER hourly quote shows a seller at or below our price before the market closes.
   Hourly snapshots miss fills inside the hour, so this is on the cautious side. Maker fee uses
   Kalshi's 0.0175 coefficient (a quarter of the taker fee); most series charge no maker fee.
2. Scheduled news: CPI and jobs reports (8:30am ET) and Fed decisions (2pm ET), from the BLS and
   Federal Reserve 2026 calendars. Either skip those days, or only skip when the release lands
   between our entry and the close.
3. Time of day / weekends: volatility for each (weekday or weekend, ET hour) from the 30 days
   before entry, summed over the hours we actually hold. 24/7 markets only.
4. Volatility regime: last 24h volatility vs the last 30 days (both from hourly returns).
5. Trend: the price change over the last 24h; keep trades that go with it, or against it.
6. Kalshi price spikes: a market whose price moved 15c+ in the last 3 hours; bet on it moving back.
Nothing here looks past the entry time except the fill check, which only uses quotes after we
would have placed the order.
"""
import bisect
import datetime as dt
import math
from zoneinfo import ZoneInfo

from .. import config as C
from ..model import lognormal_probability, taker_fee
from . import engine as E

ET = ZoneInfo("America/New_York")
MAKER_RATE = 0.0175
HOUR = 3600

# BLS 2026 schedule (Employment Situation, CPI) and Fed 2026 decision days (second day of meeting).
JOBS_2026 = ["01-09", "02-11", "03-06", "04-03", "05-08", "06-05", "07-02", "08-07", "09-04", "10-02", "11-06", "12-04"]
CPI_2026 = ["01-13", "02-13", "03-11", "04-10", "05-12", "06-10", "07-14", "08-12", "09-11", "10-14", "11-10", "12-10"]
FOMC_2026 = ["01-28", "03-18", "04-29", "06-17", "07-29", "09-16", "10-28", "12-09"]


def _release(day, hh, mm, kind):
    m, d = map(int, day.split("-"))
    return int(dt.datetime(2026, m, d, hh, mm, tzinfo=ET).timestamp()), kind


RELEASES = sorted([_release(d, 8, 30, "jobs") for d in JOBS_2026] + [_release(d, 8, 30, "cpi") for d in CPI_2026]
                  + [_release(d, 14, 0, "fed") for d in FOMC_2026])
RELEASE_TS = [t for t, _ in RELEASES]


def _ts(iso):
    return int(dt.datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp())


def _close(e):
    return max(_ts(m["close_time"]) for m in e["markets"])


# ---------------------------------------------------------------- enrich events

def _hourly_returns(prices):
    hours = sorted(prices)
    out = {}
    for a, b in zip(hours, hours[1:]):
        if b - a == HOUR and prices[a] > 0 and prices[b] > 0:
            out[b] = math.log(prices[b] / prices[a])
    return out


def _bucket(ts):
    t = dt.datetime.fromtimestamp(ts, ET)
    return (t.weekday() >= 5, t.hour)


def enrich(events, prices=None, tod=False):
    """Adds news flags to every event; with prices, also vol regime, trend and (tod=True, 24/7
    markets) time-of-day volatility. Only uses prices up to the entry time."""
    rets = _hourly_returns(prices) if prices else {}
    rts = sorted(rets)
    hours = sorted(prices) if prices else []
    for e in events:
        close = _close(e)
        e["close"] = close
        i, j = bisect.bisect_right(RELEASE_TS, e["ts"]), bisect.bisect_right(RELEASE_TS, close)
        e["news_in_window"] = ",".join(k for _, k in RELEASES[i:j]) or None
        day = dt.datetime.fromtimestamp(close, ET).date()
        e["news_day"] = ",".join(k for t, k in RELEASES if dt.datetime.fromtimestamp(t, ET).date() == day) or None
        if not rts:
            continue
        a, b = bisect.bisect_left(rts, e["ts"] - 30 * 86400), bisect.bisect_right(rts, e["ts"])
        window = rts[a:b]
        if len(window) < 24 * 20:
            continue
        r2 = [rets[t] ** 2 for t in window]
        v30 = sum(r2) / len(r2)
        v24 = sum(r2[-24:]) / 24
        e["vol30h"] = math.sqrt(v30 * 8760)
        e["regime"] = math.sqrt(v24 / v30) if v30 else None
        k = bisect.bisect_right(hours, e["ts"]) - 1
        k0 = bisect.bisect_right(hours, e["ts"] - 24 * HOUR) - 1
        if k >= 0 and k0 >= 0 and e["ts"] - hours[k] <= 3 * HOUR:
            e["ret24"] = math.log(prices[hours[k]] / prices[hours[k0]])
        if tod:
            e["tod_vol"] = _tod_vol(rets, window, v30, e["ts"], close)
    return events


def _tod_vol(rets, window, v30, ts, close, shrink=5):
    """Yearly-equivalent volatility for the hours from ts to close, using each hour's own
    (weekday/weekend, ET hour) variance from the window, shrunk toward the 30-day average."""
    if len(window) < 24 * 27:
        return None
    by, n = {}, {}
    for t in window:
        bk = _bucket(t)
        by[bk] = by.get(bk, 0.0) + rets[t] ** 2
        n[bk] = n.get(bk, 0) + 1
    var = lambda bk: (by.get(bk, 0.0) + shrink * v30) / (n.get(bk, 0) + shrink)
    left = max(1, round((close - ts) / HOUR))
    total = sum(var(_bucket(ts + h * HOUR + HOUR)) for h in range(left))
    return math.sqrt(total * 8760 / left)


def live_tod_vol(prices, ts, close):
    """Same as the backtest, for the live paper books: prices = {hour_end_ts: price}, last 30 days."""
    rets = _hourly_returns(prices)
    window = [t for t in sorted(rets) if ts - 30 * 86400 <= t <= ts]
    if not window:
        return None
    v30 = sum(rets[t] ** 2 for t in window) / len(window)
    return _tod_vol(rets, window, v30, ts, close)


# ---------------------------------------------------------------- probabilities

def p_tod(e, m, mult=0.5):
    if not e.get("tod_vol"):
        return None
    return lognormal_probability(m["strike_type"], E._f(m["floor"]), E._f(m["cap"]), e["spot"], e["tod_vol"] * mult,
                                 e["hours"])


def p_regime(e, m, mult=0.5):
    if not e.get("regime"):
        return None
    scale = min(2.0, max(0.5, e["regime"])) ** 0.5
    return E.p_crypto(e, m, mult * scale)


# ---------------------------------------------------------------- picker wrappers

def only_events(base, keep):
    return lambda e: base(e) if keep(e) else []


def _direction(m, side):
    """+1 if the trade wins when the price goes up, -1 if down, 0 for a range."""
    if m["strike_type"] == "between":
        return 0
    up = m["strike_type"] in ("greater", "greater_or_equal")
    return (1 if up else -1) * (1 if side == "yes" else -1)


def by_trend(base, with_trend=True):
    def pick(e):
        r = e.get("ret24")
        if r is None:
            return []
        by_t = {m["ticker"]: m for m in e["markets"]}
        out = []
        for t in base(e):
            d = _direction(by_t[t["ticker"]], t["side"])
            agrees = d == 0 or d * r >= 0
            if agrees == with_trend:
                out.append(t)
        return out
    return pick


def _mid_before(m, ts):
    q = E.quote(m.get("cs") or [], ts, max_age_h=2)
    return None if q is None else (q[0] + q[1]) / 2


def spike_fade(move=0.15, lookback_h=3, lo=0.10, hi=0.90, max_per_event=2):
    """No model: when a market's price jumped 15c+ in the last 3 hours, bet it comes back."""
    def pick(e):
        out = []
        for m in e["markets"]:
            if m["ask"] - m["bid"] > 0.08:
                continue
            before = _mid_before(m, e["ts"] - lookback_h * HOUR)
            if before is None:
                continue
            ch = E.mid(m) - before
            if abs(ch) < move:
                continue
            side = "no" if ch > 0 else "yes"
            price = m["ask"] if side == "yes" else 1 - m["bid"]
            if lo <= price <= hi:
                out.append(E._trade(e, m, side, None))
        return out[:max_per_event]
    return pick


def skip_spiked(base, move=0.15, lookback_h=3):
    def pick(e):
        by_t = {m["ticker"]: m for m in e["markets"]}
        out = []
        for t in base(e):
            m = by_t[t["ticker"]]
            before = _mid_before(m, e["ts"] - lookback_h * HOUR)
            if before is None or abs(E.mid(m) - before) < move:
                out.append(t)
        return out
    return pick


def maker(base, improve=0.01, through=False, stop_before_h=0):
    """Turn the base picker's trades into limit orders 1c above our side's bid. Filled only if a
    later hourly quote shows our side's ask at (or, through=True, below) our price before close."""
    def pick(e):
        by_t = {m["ticker"]: m for m in e["markets"]}
        out = []
        for t in base(e):
            m = by_t[t["ticker"]]
            yes = t["side"] == "yes"
            bid = m["bid"] if yes else 1 - m["ask"]
            ask = m["ask"] if yes else 1 - m["bid"]
            limit = round(min(bid + improve, ask - 0.01), 2)
            if limit < bid or limit <= 0:
                continue
            end = _ts(m["close_time"]) - stop_before_h * HOUR
            filled = False
            for c in m.get("cs") or []:
                if e["ts"] < c[0] <= end and c[1] is not None and c[2] is not None:
                    side_ask = c[2] if yes else 1 - c[1]
                    if side_ask < limit - 1e-9 or (not through and side_ask <= limit + 1e-9):
                        filled = True
                        break
            if not filled:
                continue
            n = max(1, math.floor(E.STAKE / limit))
            fee = math.ceil(MAKER_RATE * n * limit * (1 - limit) * 100 - 1e-9) / 100
            cost = n * limit + fee
            won = t["won"]
            out.append({**t, "price": limit, "contracts": n, "fee": fee, "cost": round(cost, 4),
                        "pnl": round((n if won else 0) - cost, 4), "order": "maker"})
        return out
    return pick


def volume_move(follow=True, move=0.05, vol_mult=3.0, lookback_h=3, lo=0.10, hi=0.90, max_per_event=2):
    """Candles have volume but not who bought, so: a 5c+ move in the last 3 hours on 3x the market's
    usual hourly volume = heavy one-sided flow. follow=True bets it continues, False bets it reverses."""
    def pick(e):
        cands = []
        for m in e["markets"]:
            if m["ask"] - m["bid"] > 0.08:
                continue
            cs = [c for c in (m.get("cs") or []) if c[0] <= e["ts"]]
            recent = [c for c in cs if c[0] > e["ts"] - lookback_h * HOUR]
            past = [c for c in cs if e["ts"] - 7 * 24 * HOUR < c[0] <= e["ts"] - lookback_h * HOUR]
            if not recent or len(past) < 12:
                continue
            base = sum(c[3] or 0 for c in past) / len(past)
            vol = sum(c[3] or 0 for c in recent) / len(recent)
            before = _mid_before(m, e["ts"] - lookback_h * HOUR)
            if before is None or base <= 0 or vol < vol_mult * base:
                continue
            ch = E.mid(m) - before
            if abs(ch) < move:
                continue
            side = ("yes" if ch > 0 else "no") if follow else ("no" if ch > 0 else "yes")
            ask = m["ask"] if side == "yes" else 1 - m["bid"]
            if lo <= ask <= hi:
                cands.append((abs(ch) * vol / base, m, side))
        cands.sort(key=lambda x: -x[0])
        return [E._trade(e, m, side, None) for _, m, side in cands[:max_per_event]]
    return pick


def volume_strategies():
    return [
        ("v_follow", "Heavy-volume move: follow", "5c+ move on 3x usual volume in 3h: bet it continues", volume_move(True)),
        ("v_fade", "Heavy-volume move: fade", "Same signal, bet it reverses", volume_move(False)),
        ("v_follow_big", "Heavy-volume move (10c, 5x): follow", "Bigger move, heavier volume, follow", volume_move(True, 0.10, 5.0)),
        ("v_fade_big", "Heavy-volume move (10c, 5x): fade", "Bigger move, heavier volume, fade", volume_move(False, 0.10, 5.0)),
    ]


def exits(base, tp=None, sl=None):
    """Sell early: take profit when our side's bid is tp above what we paid, stop loss when it is sl
    below. Checked on each later hourly quote; selling pays the bid plus the taker fee again."""
    def pick(e):
        by_t = {m["ticker"]: m for m in e["markets"]}
        out = []
        for t in base(e):
            m = by_t[t["ticker"]]
            yes = t["side"] == "yes"
            end = _ts(m["close_time"])
            for c in m.get("cs") or []:
                if not (e["ts"] < c[0] < end) or c[1] is None or c[2] is None:
                    continue
                bid = c[1] if yes else 1 - c[2]
                if (tp is not None and bid >= t["price"] + tp) or (sl is not None and bid <= t["price"] - sl):
                    n = t["contracts"]
                    fee = taker_fee(n, bid, C.FEE_RATE)
                    t = {**t, "pnl": round(n * bid - fee - t["cost"], 4), "won": n * bid - fee > t["cost"],
                         "exit": "tp" if bid > t["price"] else "sl"}
                    break
            out.append(t)
        return out
    return pick


def exit_strategies(base, label):
    return [
        (f"x_tp15_sl15_{label}", f"{label}, take profit 15c / stop 15c", "Sell early at +15c or -15c", exits(base, 0.15, 0.15)),
        (f"x_tp10_{label}", f"{label}, take profit 10c", "Sell once up 10c, else hold", exits(base, tp=0.10)),
        (f"x_sl10_{label}", f"{label}, stop loss 10c", "Sell once down 10c, else hold", exits(base, sl=0.10)),
        (f"x_sl25_{label}", f"{label}, stop loss 25c", "Sell once down 25c, else hold", exits(base, sl=0.25)),
    ]


# ---------------------------------------------------------------- catalogues

def crypto_strategies(base_id="c_vol50", tod=True):
    """Signals layered on the Bitcoin/Ethereum winner (vol x0.5, 8c edge)."""
    base = E.edge_picker(lambda e, m: E.p_crypto(e, m, 0.5))
    base5 = E.edge_picker(lambda e, m: E.p_crypto(e, m, 0.5), min_edge=0.05)
    out = [
        ("s_maker", "Vol x0.5, limit order", "Same picks, but post 1c above the bid instead of paying the ask", maker(base)),
        ("s_maker5", "Vol x0.5 5c edge, limit order", "Lower edge bar, limit order", maker(base5)),
        ("s_maker_thru", "Vol x0.5, limit order (strict fill)", "Only filled if the price trades BELOW our limit",
         maker(base, through=True)),
        ("s_no_news_day", "Vol x0.5, skip news days", "Skip days with a CPI, jobs or Fed release",
         only_events(base, lambda e: not e.get("news_day"))),
        ("s_news_window", "Vol x0.5, skip news in window", "Skip only when the release lands between entry and close",
         only_events(base, lambda e: not e.get("news_in_window"))),
        ("s_news_only", "Vol x0.5, news days only", "Control: only days with a release",
         only_events(base, lambda e: bool(e.get("news_day")))),
        ("s_calm", "Vol x0.5, calm market only", "Last 24h quieter than the 30-day normal",
         only_events(base, lambda e: (e.get("regime") or 9) < 1)),
        ("s_busy", "Vol x0.5, busy market only", "Last 24h busier than normal",
         only_events(base, lambda e: (e.get("regime") or 0) >= 1)),
        ("s_regime", "Regime-scaled vol x0.5", "Vol x0.5, scaled up/down by how busy the last 24h was",
         E.edge_picker(p_regime)),
        ("s_with_trend", "Vol x0.5, with the 24h trend", "Keep trades that win if the last 24h move continues",
         by_trend(base, True)),
        ("s_against_trend", "Vol x0.5, against the 24h trend", "Keep trades that win if the last 24h move reverses",
         by_trend(base, False)),
        ("s_weekend", "Vol x0.5, weekends only", "Only Saturday/Sunday closes",
         only_events(base, lambda e: dt.datetime.fromtimestamp(e["ts"], ET).weekday() >= 5)),
        ("s_weekday", "Vol x0.5, weekdays only", "Only Monday-Friday closes",
         only_events(base, lambda e: dt.datetime.fromtimestamp(e["ts"], ET).weekday() < 5)),
        ("s_spike_fade", "Kalshi price-spike fade (no model)", "Bet against a 15c+ move in the last 3 hours", spike_fade()),
        ("s_skip_spiked", "Vol x0.5, skip spiked markets", "Leave markets that just jumped 15c+ alone",
         skip_spiked(base)),
    ]
    tod_base = E.edge_picker(lambda e, m: p_tod(e, m, 0.5))
    out += [
        ("s_combo_trend", "Vol x0.5, against trend + skip spikes", "The two filters that helped both Bitcoin and Ethereum",
         skip_spiked(by_trend(base, False))),
    ]
    if tod:
        out += [
            ("s_combo_tod", "Time-of-day vol x0.5, skip spikes", "Hour-by-hour volatility, leave markets that just jumped",
             skip_spiked(tod_base)),
            ("s_combo_all", "Time-of-day vol x0.5, against trend + skip spikes", "All three helpful signals together",
             skip_spiked(by_trend(tod_base, False))),
        ]
    if tod:
        out.append(("s_tod", "Time-of-day vol x0.5", "Volatility by hour and weekday/weekend, summed over the hours held",
                    E.edge_picker(lambda e, m: p_tod(e, m, 0.5))))
    out += exit_strategies(base, "Vol x0.5")
    out += volume_strategies()
    return out


def tod_sweep():
    return [(k, E.edge_picker(lambda e, m, k=k: p_tod(e, m, k))) for k in (0.4, 0.5, 0.6, 0.75, 1.0)]


def weather_strategies():
    fade = E.longshot_fade()
    return [
        ("s_fade_maker", "Long-shot fade, limit order", "Buy NO on 3-10c long shots, posting 1c above the bid", maker(fade)),
        ("s_fav_maker", "Market favorite, limit order", "Favorite YES at 35-75c, posting 1c above the bid",
         maker(E.market_favorite())),
        ("s_spike_fade", "Kalshi price-spike fade (no model)", "Bet against a 15c+ move in the last 3 hours", spike_fade()),
    ] + exit_strategies(E.market_favorite(), "Favorite") + volume_strategies()


def has_any(events, key):
    return sum(1 for e in events if e.get(key) is not None)
