"""Probe: which Polymarket crypto price markets line up with Kalshi's KXBTCD/KXETHD events? Read-only."""
import datetime as dt
import json

from . import config as C
from .http import get_json

GAMMA = "https://gamma-api.polymarket.com"


def main():
    now = dt.datetime.now(dt.timezone.utc)
    print("now", now.isoformat())
    for q in ("bitcoin-above", "ethereum-above", "bitcoin-price", "what-price-will-bitcoin-hit"):
        try:
            evs = get_json(f"{GAMMA}/events", {"slug_contains": q, "closed": "false", "limit": 20})
        except Exception as e:
            print(q, "ERR", e)
            evs = []
        if not evs:
            try:
                evs = [e for e in get_json(f"{GAMMA}/events", {"closed": "false", "limit": 500, "tag_slug": "crypto"}) if q in e.get("slug", "")]
            except Exception as e:
                print("tag fallback ERR", e)
        print(f"\n== {q}: {len(evs)} events")
        for e in evs[:6]:
            ms = e.get("markets") or []
            print(e.get("slug"), "| end", e.get("endDate"), "| markets", len(ms))
            print("   desc:", (e.get("description") or "")[:400].replace("\n", " "))
            for m in ms[:4]:
                print("   ", m.get("question"), "| bid", m.get("bestBid"), "ask", m.get("bestAsk"), "| outcomePrices", m.get("outcomePrices"),
                      "| fees?", m.get("feesEnabled", m.get("makerBaseFee")), "| end", m.get("endDate"))
    print("\n== Kalshi open KXBTCD events")
    data = get_json(f"{C.KALSHI_API}/events", {"series_ticker": "KXBTCD", "status": "open", "limit": 50})
    for e in sorted(data.get("events") or [], key=lambda e: e.get("event_ticker"))[:30]:
        print(e.get("event_ticker"), e.get("sub_title"), e.get("strike_date"))
    m = get_json(f"{C.KALSHI_API}/markets", {"series_ticker": "KXBTCD", "status": "open", "limit": 5})
    for x in (m.get("markets") or [])[:3]:
        print(json.dumps({k: x.get(k) for k in ("ticker", "open_time", "close_time", "rules_primary", "floor_strike", "yes_bid_dollars", "yes_ask_dollars")})[:600])


if __name__ == "__main__":
    main()
