"""Market scanner: which Kalshi markets are worth our time?

For the most-traded series in every category it replays recent settled events and measures, at
24h / 6h / 1h before close:
  - spread and volume (can we even trade it?)
  - calibration: when the market said X%, how often did YES win? (long shots over/under-priced?)
  - simple no-model strategies after fees: long-shot fade, favorite buy, and a price-correction
    rule learned on the older 2/3 of events and tested on the newest 1/3 (holdout)
  - bracket-sum arbitrage: all YES asks of a one-winner ladder adding to under $1 (or bids over $1)

python -m kalshi_analyzer.backtest scan [--top 150] [--days 45]
"""
import datetime as dt
import json
import math
import statistics
from collections import defaultdict

from .. import config as C
from ..http import get_json
from ..model import taker_fee
from . import data as D
from . import engine as E

K = C.KALSHI_API
HORIZONS = (24, 6, 1)
OUT_JSON = C.DASHBOARD_DATA / "scanner.json"
OUT_MD = C.ROOT / "reports" / "scanner.md"
BUCKETS = (0, .03, .06, .10, .15, .25, .35, .50, .65, .75, .85, .90, .94, .97, 1.0001)


def _series_of(event_ticker):
    return event_ticker.split("-")[0]


def active_series(max_pages=250):
    """Aggregate currently open markets (excluding multi-leg parlays) by series."""
    agg = defaultdict(lambda: {"markets": 0, "vol24": 0.0, "oi": 0.0, "spreads": []})
    cursor, pages = None, 0
    while pages < max_pages:
        params = {"status": "open", "limit": 1000, "mve_filter": "exclude"}
        if cursor:
            params["cursor"] = cursor
        data = get_json(f"{K}/markets", params, retries=5, timeout=60)
        for m in data.get("markets") or []:
            s = _series_of(m["event_ticker"])
            if s.startswith("KXMVE"):
                continue
            a = agg[s]
            a["markets"] += 1
            a["vol24"] += E._f(m.get("volume_24h_fp")) or E._f(m.get("volume_24h")) or 0.0
            a["oi"] += E._f(m.get("open_interest_fp")) or E._f(m.get("open_interest")) or 0.0
            b, k = E._f(m.get("yes_bid_dollars")), E._f(m.get("yes_ask_dollars"))
            if b and k and 0 < b < k < 1:
                a["spreads"].append(k - b)
        pages += 1
        cursor = data.get("cursor")
        if not cursor:
            break
    D.log(f"scanner: {pages} pages of open markets, {len(agg)} active series")
    return agg


def series_meta():
    data = get_json(f"{K}/series", {"limit": 20000}, retries=5, timeout=120)
    return {s["ticker"]: {"category": s.get("category") or "Other", "title": s.get("title") or s["ticker"],
                          "frequency": s.get("frequency") or "", "fee_multiplier": s.get("fee_multiplier", 1),
                          "fee_type": s.get("fee_type") or ""} for s in data.get("series") or []}


def pick_series(agg, meta, top=150, per_category=6):
    rows = [(s, a) for s, a in agg.items() if a["vol24"] > 0]
    rows.sort(key=lambda x: -x[1]["vol24"])
    chosen = [s for s, _ in rows[:top]]
    by_cat = defaultdict(list)
    for s, _ in rows:
        by_cat[meta.get(s, {}).get("category", "Other")].append(s)
    for cat, ss in by_cat.items():
        for s in ss[:per_category]:
            if s not in chosen:
                chosen.append(s)
    return chosen


def _fill(series, cached, name, workers=4):
    todo = [m for t, m in cached["markets"].items() if t not in cached["candles"]]
    if todo:
        D.log(f"  {series}: candles for {len(todo)} markets")
    from concurrent.futures import ThreadPoolExecutor

    def job(m):
        try:
            return m["ticker"], D.candles(series, m, hours_before=30)
        except Exception as e:
            D.log(f"  candles {m['ticker']}: {e}")
            return m["ticker"], None
    with ThreadPoolExecutor(workers) as ex:
        for t, cs in ex.map(job, todo):
            if cs is not None:
                cached["candles"][t] = cs
    D._save(name, cached)
    return cached


def fetch(top=150, days=45):
    since = dt.date.today() - dt.timedelta(days=days)
    agg = active_series()
    meta = series_meta()
    chosen = pick_series(agg, meta, top=top)
    D.log(f"scanner: scanning {len(chosen)} series")
    for i, s in enumerate(chosen):
        name = f"scan_{s}"
        cached = D._load(name, {"markets": {}, "candles": {}})
        try:
            rows = D.settled_markets(series=s, since=since)
        except Exception as e:
            D.log(f"  {s}: {e}")
            continue
        by_event = defaultdict(list)
        for r in rows:
            by_event[r["event_ticker"]].append(r)
        events = sorted(by_event, key=lambda e: max(m["close_time"] or "" for m in by_event[e]))
        if len(events) > 10:
            step = len(events) / 10
            events = [events[int(k * step)] for k in range(10)]
        flags = cached.setdefault("events", {})
        for ev in events:
            for m in sorted(by_event[ev], key=lambda m: m["ticker"])[:30]:
                cached["markets"].setdefault(m["ticker"], m)
        for ev in {m["event_ticker"] for m in cached["markets"].values()}:
            if ev not in flags:  # needed so arbitrage only counts true one-winner events
                try:
                    flags[ev] = bool((get_json(f"{K}/events/{ev}", retries=3).get("event") or {}).get("mutually_exclusive"))
                except Exception:
                    pass
        _fill(s, cached, name)
        if i % 20 == 0:
            D.log(f"scanner: {i + 1}/{len(chosen)} series")
    snapshot = {s: {"vol24": round(agg[s]["vol24"]), "open_markets": agg[s]["markets"],
                    "open_interest": round(agg[s]["oi"]),
                    "median_spread": round(statistics.median(agg[s]["spreads"]), 3) if agg[s]["spreads"] else None,
                    **meta.get(s, {"category": "Other", "title": s})} for s in chosen}
    D._save("scan_index", snapshot)


# ---------------------------------------------------------------- analysis

def quotes(snapshot):
    """One row per (market, horizon): series, event, close, bid, ask, won."""
    out = []
    for s, info in snapshot.items():
        cached = D._load(f"scan_{s}", None)
        if not cached:
            continue
        flags = cached.get("events", {})
        for t, m in cached["markets"].items():
            cs = cached["candles"].get(t)
            if not cs or not m.get("close_time"):
                continue
            close = D._ts(m["close_time"])
            for h in HORIZONS:
                q = E.quote(cs, close - h * 3600, max_age_h=3)
                if q:
                    out.append({"series": s, "category": info.get("category", "Other"), "event": m["event_ticker"],
                                "ticker": t, "close": close, "h": h, "bid": q[0], "ask": q[1],
                                "mid": (q[0] + q[1]) / 2, "won": m["result"] == "yes",
                                "strike_type": m["strike_type"], "exclusive": flags.get(m["event_ticker"]),
                                "n_event": sum(1 for x in cached["markets"].values() if x["event_ticker"] == m["event_ticker"])})
    return out


def _bucket(p):
    for lo, hi in zip(BUCKETS, BUCKETS[1:]):
        if lo <= p < hi:
            return lo
    return BUCKETS[-2]


def _trade(q, side, fee_mult=1.0):
    ask = q["ask"] if side == "yes" else 1 - q["bid"]
    c = max(1, math.floor(E.STAKE / ask))
    fee = taker_fee(c, ask, C.FEE_RATE * fee_mult)
    won = q["won"] if side == "yes" else not q["won"]
    cost = c * ask + fee
    return {"pnl": (c if won else 0) - cost, "cost": cost, "won": won, "date": dt.datetime.fromtimestamp(q["close"], dt.timezone.utc).date().isoformat(),
            "ts": q["close"]}


def strat_fade(q):
    if 0.03 <= q["bid"] and q["ask"] <= 0.10 and q["ask"] - q["bid"] <= 0.05:
        return "no"


def strat_favorite(q):
    if 0.85 <= q["bid"] and q["ask"] <= 0.97 and q["ask"] - q["bid"] <= 0.05:
        return "yes"


def learn_table(train):
    """Price bucket -> (n, actual YES rate)."""
    g = defaultdict(lambda: [0, 0])
    for q in train:
        b = g[_bucket(q["mid"])]
        b[0] += 1
        b[1] += q["won"]
    return {k: (n, w / n) for k, (n, w) in g.items() if n}


def strat_corrected(table, min_edge=0.03, min_n=30):
    def pick(q):
        n, rate = table.get(_bucket(q["mid"]), (0, None))
        if n < min_n or q["ask"] - q["bid"] > 0.10:
            return None
        # shrink the learned rate toward the price when data is thin
        p = (n * rate + 30 * q["mid"]) / (n + 30)
        for side, price, chance in (("yes", q["ask"], p), ("no", 1 - q["bid"], 1 - p)):
            c = max(1, math.floor(E.STAKE / price))
            if 0.02 <= price <= 0.98 and chance - price - taker_fee(c, price, C.FEE_RATE) / c >= min_edge:
                return side
    return pick


def score(qs, picker):
    trades = [_trade(q, side) for q in qs for side in [picker(q)] if side]
    if not trades:
        return {"trades": 0, "pnl": 0.0, "roi": None, "roi_ci": None, "win_rate": None}
    staked = sum(t["cost"] for t in trades)
    return {"trades": len(trades), "pnl": round(sum(t["pnl"] for t in trades), 2),
            "roi": round(sum(t["pnl"] for t in trades) / staked, 4), "roi_ci": E.roi_ci(trades),
            "win_rate": round(sum(t["won"] for t in trades) / len(trades), 3)}


def calibration_rows(qs):
    g = defaultdict(lambda: [0, 0, 0.0])
    for q in qs:
        b = g[_bucket(q["mid"])]
        b[0] += 1
        b[1] += q["won"]
        b[2] += q["mid"]
    return [{"bucket": f"{lo * 100:.0f}c+", "n": n, "market": round(sp / n, 3), "actual": round(w / n, 3)}
            for lo, (n, w, sp) in sorted(g.items())]


def arbitrage(qs):
    """Events Kalshi marks mutually exclusive (exactly one market can win), with EVERY market of
    the event quoted at the same horizon. Profit after fees if you bought every YES (sum of asks
    < $1) or every NO. Hourly candle quotes aren't simultaneous, so treat hits as leads to verify."""
    by = defaultdict(list)
    for q in qs:
        by[(q["event"], q["h"])].append(q)
    checked, found = 0, []
    for (ev, h), ms in by.items():
        if len(ms) < 3 or not ms[0].get("exclusive") or len(ms) != ms[0].get("n_event") or len(ms) >= 30:  # 30 = capped sample
            continue
        checked += 1
        fee = sum(taker_fee(1, q["ask"], C.FEE_RATE) for q in ms)
        buy_yes = 1 - sum(q["ask"] for q in ms) - fee
        fee_no = sum(taker_fee(1, 1 - q["bid"], C.FEE_RATE) for q in ms)
        buy_no = (len(ms) - 1) - sum(1 - q["bid"] for q in ms) - fee_no
        best = max(buy_yes, buy_no)
        if best > 0:
            found.append({"event": ev, "hours_before": h, "markets": len(ms),
                          "profit_per_set": round(best, 3), "side": "all YES" if buy_yes >= buy_no else "all NO"})
    return {"ladders_checked": checked, "opportunities": sorted(found, key=lambda x: -x["profit_per_set"])[:25],
            "count": len(found)}


def analyze(now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    snapshot = D._load("scan_index", {})
    qs = quotes(snapshot)
    D.log(f"scanner: {len(qs)} quotes from {len(snapshot)} series")
    by_series = defaultdict(list)
    for q in qs:
        by_series[q["series"]].append(q)
    # price-correction rule: learn per category on the older 2/3 of time, test on the newest 1/3
    closes = sorted(q["close"] for q in qs)
    cut = closes[int(len(closes) * 2 / 3)] if closes else 0
    by_cat = defaultdict(list)
    for q in qs:
        by_cat[q["category"]].append(q)
    tables = {c: learn_table([q for q in v if q["close"] < cut and q["h"] == 6]) for c, v in by_cat.items()}

    series_rows = []
    for s, v in by_series.items():
        info = snapshot.get(s, {})
        six = [q for q in v if q["h"] == 6]
        test6 = [q for q in six if q["close"] >= cut]
        row = {"series": s, "title": info.get("title", s), "category": info.get("category", "Other"),
               "frequency": info.get("frequency", ""), "vol24": info.get("vol24"), "open_markets": info.get("open_markets"),
               "median_spread": info.get("median_spread"), "quotes": len(v), "events": len({q["event"] for q in v}),
               "brier_market": round(statistics.fmean((q["mid"] - q["won"]) ** 2 for q in six), 4) if six else None,
               "fade": score(six, strat_fade), "favorite": score(six, strat_favorite),
               "corrected_holdout": score(test6, strat_corrected(tables.get(row_cat(info), {})))}
        series_rows.append(row)
    series_rows.sort(key=lambda r: -max([x["roi"] or -9 for x in (r["fade"], r["favorite"], r["corrected_holdout"]) if x["trades"] >= 15] or [-9]))

    cats = []
    for c, v in by_cat.items():
        six = [q for q in v if q["h"] == 6]
        test6 = [q for q in six if q["close"] >= cut]
        cats.append({"category": c, "series": len({q["series"] for q in v}), "quotes": len(v),
                     "fade": score(six, strat_fade), "favorite": score(six, strat_favorite),
                     "corrected_holdout": score(test6, strat_corrected(tables.get(c, {}))),
                     "calibration": calibration_rows(six)})
    cats.sort(key=lambda r: -r["quotes"])

    timing = []
    for h in HORIZONS:
        hq = [q for q in qs if q["h"] == h]
        timing.append({"hours_before": h, "quotes": len(hq),
                       "median_spread": round(statistics.median(q["ask"] - q["bid"] for q in hq), 3) if hq else None,
                       "brier_market": round(statistics.fmean((q["mid"] - q["won"]) ** 2 for q in hq), 4) if hq else None,
                       "fade": score(hq, strat_fade), "favorite": score(hq, strat_favorite)})

    result = {"generated_at": now.isoformat(timespec="minutes"), "series_scanned": len(by_series),
              "quotes": len(qs), "holdout_from": dt.datetime.fromtimestamp(cut, dt.timezone.utc).date().isoformat() if cut else None,
              "categories": cats, "series": series_rows, "timing": timing, "arbitrage": arbitrage(qs)}
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=1))
    OUT_MD.write_text(markdown(result))
    D.log(f"wrote {OUT_JSON} and {OUT_MD}")
    return result


def row_cat(info):
    return info.get("category", "Other")


def _r(x):
    if not x or x.get("roi") is None:
        return "–"
    ci = x.get("roi_ci")
    return f"{x['roi'] * 100:+.1f}% ({x['trades']})" + (f" [{ci[0] * 100:+.0f}..{ci[1] * 100:+.0f}]" if ci else "")


def markdown(r):
    L = [f"# Market scanner ({r['generated_at'][:10]})", "",
         f"{r['series_scanned']} series, {r['quotes']} price snapshots. Returns per $ staked after fees, "
         "(trades) [90% range]. Price-correction rule is learned on older events and scored only on events "
         f"from {r['holdout_from']} on.", "",
         "## By category (6h before close)", "",
         "| Category | Series | Long-shot fade | Favorite buy | Price-correction (holdout) |", "|---|---|---|---|---|"]
    for c in r["categories"]:
        L.append(f"| {c['category']} | {c['series']} | {_r(c['fade'])} | {_r(c['favorite'])} | {_r(c['corrected_holdout'])} |")
    L += ["", "## Entry timing (all scanned series)", "", "| Hours before close | Snapshots | Median spread | Fade | Favorite |", "|---|---|---|---|---|"]
    for t in r["timing"]:
        L.append(f"| {t['hours_before']} | {t['quotes']} | {t['median_spread']} | {_r(t['fade'])} | {_r(t['favorite'])} |")
    a = r["arbitrage"]
    L += ["", f"## Bracket-sum arbitrage", "", f"{a['count']} opportunities in {a['ladders_checked']} one-winner ladders checked."]
    for o in a["opportunities"][:10]:
        L.append(f"- {o['event']} {o['hours_before']}h before: {o['side']}, +${o['profit_per_set']} per set ({o['markets']} markets)")
    L += ["", "## Top series", "", "| Series | Category | 24h volume | Spread | Fade | Favorite | Correction (holdout) |", "|---|---|---|---|---|---|---|"]
    for s in r["series"][:40]:
        L.append(f"| {s['title']} ({s['series']}) | {s['category']} | {s['vol24']} | {s['median_spread']} | {_r(s['fade'])} | {_r(s['favorite'])} | {_r(s['corrected_holdout'])} |")
    return "\n".join(L) + "\n"
