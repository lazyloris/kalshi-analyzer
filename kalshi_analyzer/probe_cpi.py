"""Probe: Kalshi inflation/jobs markets history + where the Cleveland Fed nowcast data lives. Read-only."""
import json
import re
import urllib.request

from . import config as C
from .http import get_json


def raw(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research script)", "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def main():
    for s in ("KXCPI", "KXCPIYOY", "KXCPICORE", "KXCPICOREYOY", "KXPAYROLLS", "KXU3", "KXFED", "KXGDP"):
        try:
            evs = get_json(f"{C.KALSHI_API}/events", {"series_ticker": s, "limit": 200}).get("events") or []
            st = {}
            for e in evs:
                st[e.get("status") or "?"] = st.get(e.get("status") or "?", 0) + 1
            print(s, len(evs), "events", st, [e.get("event_ticker") for e in evs[:3]], [e.get("event_ticker") for e in evs[-2:]])
        except Exception as ex:
            print(s, "ERR", str(ex)[:120])
    try:
        m = get_json(f"{C.KALSHI_API}/markets", {"series_ticker": "KXCPI", "status": "settled", "limit": 5}).get("markets") or []
        for x in m[:3]:
            print(json.dumps({k: x.get(k) for k in ("ticker", "event_ticker", "open_time", "close_time", "floor_strike", "cap_strike",
                                                    "strike_type", "result", "volume", "rules_primary")})[:500])
        if m:
            t = m[0]
            c = get_json(f"{C.KALSHI_API}/series/KXCPI/markets/{t['ticker']}/candlesticks",
                         {"start_ts": 0, "end_ts": 2000000000, "period_interval": 1440})
            print("candles", len(c.get("candlesticks") or []), json.dumps((c.get("candlesticks") or [{}])[0])[:400])
    except Exception as ex:
        print("KXCPI markets ERR", str(ex)[:200])
    for url in ("https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting",):
        try:
            h = raw(url)
            print(url, len(h))
            for u in sorted(set(re.findall(r"[\"'(]([^\"'()\s]*(?:\.json|\.csv|\.xlsx|/api/[^\"'()\s]*))", h)))[:40]:
                print("  link:", u)
            for u in sorted(set(re.findall(r"data-[a-z-]*url=\"([^\"]+)\"", h)))[:20]:
                print("  data-url:", u)
        except Exception as ex:
            print(url, "ERR", str(ex)[:200])


if __name__ == "__main__":
    main()
