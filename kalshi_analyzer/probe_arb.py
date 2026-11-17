"""Probe: which Polymarket crypto price markets line up with Kalshi's KXBTCD/KXETHD events? Read-only."""
import datetime as dt
import json

from . import config as C
from .http import get_json

GAMMA = "https://gamma-api.polymarket.com"


def main():
    now = dt.datetime.now(dt.timezone.utc)
    print("now", now.isoformat())
    for slug in ("bitcoin-above-on-november-17", "bitcoin-above-on-november-18", "ethereum-above-on-november-17",
                 "bitcoin-price-on-november-17", "what-price-will-bitcoin-hit-in-november-2026"):
        try:
            evs = get_json(f"{GAMMA}/events", {"slug": slug})
        except Exception as e:
            print(slug, "ERR", e); continue
        print(f"\n== {slug}: {len(evs)} events")
        for e in evs[:1]:
            ms = e.get("markets") or []
            print("end", e.get("endDate"), "| markets", len(ms))
            print("   desc:", (e.get("description") or "")[:700].replace("\n", " "))
            for m in ms[:30]:
                print("   ", m.get("question"), "| bid", m.get("bestBid"), "ask", m.get("bestAsk"), "| fees", m.get("feesEnabled"),
                      "| liq", m.get("liquidityNum"), "| vol24", m.get("volume24hr"))
    try:
        r = get_json(f"{GAMMA}/public-search", {"q": "bitcoin above", "limit_per_type": 10})
        for e in (r.get("events") or [])[:10]:
            print("search:", e.get("slug"), e.get("endDate"))
    except Exception as e:
        print("search ERR", e)
    print("\n== Kalshi open KXBTCD events")
    data = get_json(f"{C.KALSHI_API}/events", {"series_ticker": "KXBTCD", "status": "open", "limit": 50})
    for e in sorted(data.get("events") or [], key=lambda e: e.get("event_ticker"))[:30]:
        print(e.get("event_ticker"), e.get("sub_title"), e.get("strike_date"))
    m = get_json(f"{C.KALSHI_API}/markets", {"series_ticker": "KXBTCD", "status": "open", "limit": 5})
    for x in (m.get("markets") or [])[:3]:
        print(json.dumps({k: x.get(k) for k in ("ticker", "open_time", "close_time", "rules_primary", "floor_strike", "yes_bid_dollars", "yes_ask_dollars")})[:600])


if __name__ == "__main__":
    main()
