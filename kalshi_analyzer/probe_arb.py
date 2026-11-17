"""Probe: which Polymarket crypto price markets line up with Kalshi's KXBTCD/KXETHD events? Read-only."""
import datetime as dt
import json

from . import config as C
from .http import get_json

GAMMA = "https://gamma-api.polymarket.com"


def main():
    now = dt.datetime.now(dt.timezone.utc)
    print("now", now.isoformat())
    seen = {}
    variants = [{"tag_slug": "crypto", "closed": "false", "limit": 50},
                {"tag_slug": "bitcoin", "closed": "false", "limit": 50},
                {"tag_slug": "crypto-prices", "closed": "false", "limit": 50},
                {"closed": "false", "limit": 50, "end_date_min": "2026-11-17T00:00:00Z", "end_date_max": "2026-11-20T00:00:00Z"}]
    for v in variants:
        for off in range(0, 500, 50):
            try:
                evs = get_json(f"{GAMMA}/events", dict(v, offset=off))
            except Exception as e:
                print(v, off, "ERR", e); break
            for e in evs:
                seen[e.get("slug")] = e
            if len(evs) < 50:
                break
        print(v, "->", len(seen))
    print(f"\n== {len(seen)} open crypto events")
    for slug, e in sorted(seen.items(), key=lambda kv: kv[1].get("endDate") or ""):
        if (e.get("endDate") or "") > "2026-11-25":
            continue
        ms = e.get("markets") or []
        print(e.get("endDate"), slug, "| mkts", len(ms), "| vol24", e.get("volume24hr"))
        if any(k in slug for k in ("above", "price-on", "up-or-down")) and ms:
            print("   desc:", (e.get("description") or "")[:300].replace("\n", " "))
            for m in ms[:14]:
                print("     ", m.get("question"), "| bid", m.get("bestBid"), "ask", m.get("bestAsk"),
                      "| fees", m.get("feesEnabled"), "| liq", m.get("liquidityNum"))
    print("\n== Kalshi open KXBTCD events")
    data = get_json(f"{C.KALSHI_API}/events", {"series_ticker": "KXBTCD", "status": "open", "limit": 50})
    for e in sorted(data.get("events") or [], key=lambda e: e.get("event_ticker"))[:30]:
        print(e.get("event_ticker"), e.get("sub_title"), e.get("strike_date"))
    m = get_json(f"{C.KALSHI_API}/markets", {"series_ticker": "KXBTCD", "status": "open", "limit": 5})
    for x in (m.get("markets") or [])[:3]:
        print(json.dumps({k: x.get(k) for k in ("ticker", "open_time", "close_time", "rules_primary", "floor_strike", "yes_bid_dollars", "yes_ask_dollars")})[:600])


if __name__ == "__main__":
    main()
