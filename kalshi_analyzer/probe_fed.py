"""Probe: Kalshi Fed markets vs Polymarket Fed decision markets, history availability. Read-only."""
import json

from . import config as C
from .http import get_json

GAMMA = "https://gamma-api.polymarket.com"
CLOB = "https://clob.polymarket.com"


def main():
    for s in ("KXFEDDECISION", "KXFED", "FEDDECISION"):
        try:
            evs = get_json(f"{C.KALSHI_API}/events", {"series_ticker": s, "limit": 200}).get("events") or []
            print(s, len(evs), [e.get("event_ticker") for e in evs[:4]], [e.get("event_ticker") for e in evs[-3:]])
            if evs:
                ms = get_json(f"{C.KALSHI_API}/markets", {"event_ticker": evs[min(3, len(evs)-1)]["event_ticker"], "limit": 50}).get("markets") or []
                for m in ms[:6]:
                    print("   ", m.get("ticker"), m.get("strike_type"), m.get("floor_strike"), m.get("cap_strike"), m.get("result"),
                          m.get("close_time"), (m.get("yes_sub_title") or "")[:40])
        except Exception as e:
            print(s, "ERR", str(e)[:150])
    for q in ("fed decision", "fed interest rates"):
        try:
            r = get_json(f"{GAMMA}/public-search", {"q": q, "limit_per_type": 50, "events_status": "all"})
            evs = r.get("events") or []
            print(f"\nsearch '{q}': {len(evs)}")
            for e in evs[:50]:
                print("  ", e.get("slug"), e.get("endDate"), e.get("closed"), round(float(e.get("volume") or 0)))
        except Exception as e:
            print("search ERR", str(e)[:150])
    for slug in ("fed-decision-in-october", "fed-decision-in-december", "fed-decision-in-september-2026", "fed-decision-in-october-2026"):
        try:
            evs = get_json(f"{GAMMA}/events", {"slug": slug})
            for e in evs[:1]:
                print("\n", slug, e.get("endDate"), e.get("closed"))
                for m in (e.get("markets") or [])[:6]:
                    toks = json.loads(m.get("clobTokenIds") or "[]")
                    print("   ", m.get("question"), m.get("outcomePrices"), m.get("closed"))
                    if toks:
                        h = get_json(f"{CLOB}/prices-history", {"market": toks[0], "interval": "max", "fidelity": 60}).get("history") or []
                        print("      history points", len(h), h[:1], h[-1:])
        except Exception as e:
            print(slug, "ERR", str(e)[:150])


if __name__ == "__main__":
    main()
