"""Paper scanner: Kalshi KXBTCD/KXETHD vs Polymarket "Bitcoin/Ethereum above $X" on the same close hour. Read-only.

Both venues ask "will the price be above X at hour H?". Kalshi settles on the CF Benchmarks BRTI (60-second
average before H); Polymarket settles on the Binance BTC/USDT (or ETH/USDT) close at H. Those differ slightly
(basis risk), so we also log both spot prices every loop.

A locked pair: buy YES on venue A at strike Ka and NO on venue B at strike Kb with Ka <= Kb. At least one leg
always pays $1 (both pay if Ka < S <= Kb), so profit is at least  1 - yes_ask_A - no_ask_B - fees.
Fees on both venues (crypto): 0.07 * p * (1 - p) per contract for takers (Polymarket docs: feeRate 0.07).

Writes data/arb/YYYY-MM-DD.jsonl: one "loop" row per sample and one "pair" row for every pair whose
edge after fees is above -2c (so near-misses are visible too).
"""
import datetime as dt
import json
import math
import os
import pathlib
import sys
import time
from zoneinfo import ZoneInfo

from . import config as C
from .http import get_json

GAMMA = "https://gamma-api.polymarket.com"
CLOB = "https://clob.polymarket.com"
NY = ZoneInfo("America/New_York")
OUT = pathlib.Path("data/arb")
SERIES = {"KXBTCD": ("bitcoin", "BTC"), "KXETHD": ("ethereum", "ETH")}
SPOT = {"BTC": ("BTC-USD", "BTCUSDT"), "ETH": ("ETH-USD", "ETHUSDT")}
KEEP_ABOVE = -0.02


def fee(p):
    return 0.07 * p * (1 - p)


def _f(x):
    try:
        return None if x is None or x == "" else float(x)
    except (TypeError, ValueError):
        return None


def poly_slugs(name, close_utc):
    t = close_utc.astimezone(NY)
    month = t.strftime("%B").lower()
    base = f"{name}-above-on-{month}-{t.day}-{t.year}"
    h = t.hour % 12 or 12
    hourly = f"{base}-{h}{'am' if t.hour < 12 else 'pm'}-et"
    return [hourly, base] if t.hour == 12 else [hourly]


def kalshi_quotes(event_ticker):
    data = get_json(f"{C.KALSHI_API}/markets", {"event_ticker": event_ticker, "limit": 200})
    out, close = [], None
    for m in data.get("markets") or []:
        close = close or m.get("close_time")
        if m.get("strike_type") != "greater" or m.get("status") not in (None, "active", "open"):
            continue
        k = _f(m.get("floor_strike"))
        bid, ask = _f(m.get("yes_bid_dollars")), _f(m.get("yes_ask_dollars"))
        if bid is None and m.get("yes_bid") is not None:
            bid = m["yes_bid"] / 100
        if ask is None and m.get("yes_ask") is not None:
            ask = m["yes_ask"] / 100
        if k is None:
            continue
        out.append({"venue": "kalshi", "id": m.get("ticker"), "strike": round(k + 0.01, 2),
                    "yes_bid": bid if bid and bid > 0 else None, "yes_ask": ask if ask and ask < 1 else None})
    return out, close


def poly_quotes(slug):
    evs = get_json(f"{GAMMA}/events", {"slug": slug})
    if not evs:
        return [], None
    e = evs[0]
    out = []
    for m in e.get("markets") or []:
        if m.get("closed") or not m.get("active", True):
            continue
        k = None
        for key in ("groupItemThreshold", "line"):
            k = _f(m.get(key))
            if k:
                break
        if not k:
            q = (m.get("question") or "").replace(",", "")
            nums = [float(w.strip("$?")) for w in q.split() if w.strip("$?").replace(".", "").isdigit()]
            nums = [n for n in nums if n > 500]
            k = nums[0] if nums else None
        if k is None:
            continue
        bid, ask = _f(m.get("bestBid")), _f(m.get("bestAsk"))
        try:
            tokens = json.loads(m.get("clobTokenIds") or "[]")
        except ValueError:
            tokens = []
        out.append({"venue": "poly", "id": m.get("slug") or m.get("id"), "strike": k, "tokens": tokens,
                    "yes_bid": bid if bid and bid > 0 else None, "yes_ask": ask if ask and ask < 1 else None})
    return out, e.get("endDate")


def spot(asset):
    cb, bn = SPOT[asset]
    row = {}
    try:
        row["coinbase"] = _f(get_json(f"https://api.exchange.coinbase.com/products/{cb}/ticker", retries=1).get("price"))
    except Exception:
        row["coinbase"] = None
    try:
        row["binance"] = _f(get_json("https://data-api.binance.vision/api/v3/ticker/price", {"symbol": bn}, retries=1).get("price"))
    except Exception:
        row["binance"] = None
    return row


def pairs(kal, pol):
    """Every locked combination: YES on one venue at strike a, NO on the other at strike b >= a."""
    found = []
    for yes_side, no_side in ((kal, pol), (pol, kal)):
        for y in yes_side:
            if y["yes_ask"] is None:
                continue
            for n in no_side:
                if n["yes_bid"] is None or n["strike"] < y["strike"] - 0.5:
                    continue
                no_ask = 1 - n["yes_bid"]
                cost = y["yes_ask"] + no_ask
                edge = 1 - cost - fee(y["yes_ask"]) - fee(no_ask)
                if edge > KEEP_ABOVE:
                    found.append({"yes_venue": y["venue"], "yes_id": y["id"], "yes_strike": y["strike"], "yes_ask": y["yes_ask"],
                                  "no_venue": n["venue"], "no_id": n["id"], "no_strike": n["strike"], "no_ask": round(no_ask, 4),
                                  "gross": round(1 - cost, 4), "edge": round(edge, 4),
                                  "same_strike": abs(n["strike"] - y["strike"]) <= 0.5,
                                  "_ytok": y.get("tokens"), "_ntok": n.get("tokens")})
    return found


def poly_depth(tokens, side_yes, price):
    """Shares available at or better than `price` on the Polymarket leg (YES ask side, or NO ask side)."""
    try:
        tok = tokens[0] if side_yes else tokens[1]
        book = get_json(f"{CLOB}/book", {"token_id": tok}, retries=1)
        return round(sum(float(a["size"]) for a in book.get("asks") or [] if float(a["price"]) <= price + 1e-9), 1)
    except Exception:
        return None


def kalshi_depth(ticker, side_yes, price):
    """Contracts available at or better than `price` on the Kalshi leg. YES ask = 1 - NO bid and vice versa."""
    try:
        ob = (get_json(f"{C.KALSHI_API}/markets/{ticker}/orderbook", retries=1).get("orderbook_fp")
              or get_json(f"{C.KALSHI_API}/markets/{ticker}/orderbook", retries=1).get("orderbook") or {})
        levels = ob.get("no_dollars" if side_yes else "yes_dollars") or ob.get("no" if side_yes else "yes") or []
        total = 0.0
        for lvl in levels:
            p, q = float(lvl[0]), float(lvl[1])
            p = p / 100 if p > 1 else p
            if 1 - p <= price + 1e-9:
                total += q
        return round(total, 1)
    except Exception:
        return None


def loop_once(now):
    rows = []
    for series, (name, asset) in SERIES.items():
        try:
            evs = get_json(f"{C.KALSHI_API}/events", {"series_ticker": series, "status": "open", "limit": 50}).get("events") or []
        except Exception as e:
            rows.append({"kind": "error", "where": series, "err": str(e)[:200]})
            continue
        sp = None
        for e in evs:
            et = e.get("event_ticker")
            try:
                kal, close_s = kalshi_quotes(et)
            except Exception as ex:
                rows.append({"kind": "error", "where": et, "err": str(ex)[:200]})
                continue
            if not close_s:
                continue
            close = dt.datetime.fromisoformat(close_s.replace("Z", "+00:00"))
            if close - now > dt.timedelta(hours=26):
                continue
            for slug in poly_slugs(name, close):
                try:
                    pol, pend = poly_quotes(slug)
                except Exception as ex:
                    rows.append({"kind": "error", "where": slug, "err": str(ex)[:200]})
                    continue
                if not pol:
                    continue
                if sp is None:
                    sp = spot(asset)
                ps = pairs(kal, pol)
                mins = round((close - now).total_seconds() / 60, 1)
                rows.append({"kind": "loop", "asset": asset, "kalshi_event": et, "poly_slug": slug, "poly_end": pend,
                             "close": close.isoformat(), "mins_left": mins, "n_kalshi": len(kal), "n_poly": len(pol),
                             "best_edge": max([p["edge"] for p in ps], default=None), **{f"spot_{k}": v for k, v in sp.items()}})
                for p in ps:
                    if p["edge"] > 0:
                        yv, nv = p["yes_venue"], p["no_venue"]
                        p["yes_depth"] = (kalshi_depth(p["yes_id"], True, p["yes_ask"]) if yv == "kalshi"
                                          else poly_depth(p["_ytok"], True, p["yes_ask"]))
                        p["no_depth"] = (kalshi_depth(p["no_id"], False, p["no_ask"]) if nv == "kalshi"
                                         else poly_depth(p["_ntok"], False, p["no_ask"]))
                    p.pop("_ytok", None); p.pop("_ntok", None)
                    rows.append({"kind": "pair", "asset": asset, "kalshi_event": et, "poly_slug": slug,
                                 "close": close.isoformat(), "mins_left": mins, **p})
    return rows


def main(minutes=345, every=30):
    OUT.mkdir(parents=True, exist_ok=True)
    stop = time.time() + minutes * 60
    flush_every = int(os.environ.get("ARB_FLUSH_MIN", "60")) * 60
    last_flush = time.time()
    n = 0
    while time.time() < stop:
        now = dt.datetime.now(dt.timezone.utc)
        try:
            rows = loop_once(now)
        except Exception as e:
            rows = [{"kind": "error", "where": "loop", "err": str(e)[:200]}]
        path = OUT / f"{now:%Y-%m-%d}.jsonl"
        with path.open("a") as f:
            for r in rows:
                f.write(json.dumps({"t": now.isoformat(timespec="seconds"), **r}) + "\n")
        n += 1
        good = [r for r in rows if r.get("kind") == "pair" and r["edge"] > 0]
        loops = [r for r in rows if r.get("kind") == "loop"]
        print(f"{now:%H:%M:%S} matched {len(loops)} event pairs, {len(good)} positive-edge pairs"
              + (f", best {max(r['edge'] for r in good):+.3f}" if good else ""), flush=True)
        if time.time() - last_flush > flush_every and os.environ.get("ARB_COMMIT"):
            os.system("bash .github/scripts/commit_arb.sh")
            last_flush = time.time()
        time.sleep(max(1, every - (time.time() - now.timestamp())))
    print("loops", n)


if __name__ == "__main__":
    main(float(sys.argv[1]) if len(sys.argv) > 1 else 345)
