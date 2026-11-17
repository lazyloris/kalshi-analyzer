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
    import datetime as dt
    m = get_json(f"{C.KALSHI_API}/markets", {"event_ticker": "KXCPI-26SEP", "limit": 50}).get("markets") or []
    for x in m[:2]:
        o = int(dt.datetime.fromisoformat(x["open_time"].replace("Z", "+00:00")).timestamp())
        c = int(dt.datetime.fromisoformat(x["close_time"].replace("Z", "+00:00")).timestamp())
        for per in (60, 1440):
            try:
                cs = get_json(f"{C.KALSHI_API}/series/KXCPI/markets/{x['ticker']}/candlesticks",
                              {"start_ts": max(o, c - 4900 * per * 60), "end_ts": c, "period_interval": per}).get("candlesticks") or []
                print(x["ticker"], per, len(cs), json.dumps(cs[-1])[:500] if cs else "")
            except Exception as ex:
                print(x["ticker"], per, "ERR", str(ex)[:150])
    for f in ("nowcast_month", "nowcast_quarter"):
        try:
            d = json.loads(raw(f"https://www.clevelandfed.org/-/media/files/webcharts/inflationnowcasting/{f}.json"))
            print(f, type(d).__name__, len(d))
            if isinstance(d, list):
                print(json.dumps(d[0])[:1500]); print(json.dumps(d[-1])[:1500])
            else:
                print(list(d)[:20]); print(json.dumps(d)[:1500])
        except Exception as ex:
            print(f, "ERR", str(ex)[:200])
    return
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
