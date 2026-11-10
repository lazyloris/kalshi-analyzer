"""Price-level ladder test: is a market quoted at X cents, H hours before close, worth X cents?

No model at all. For every settled market with hourly candles, take the quote exactly H hours
before close (at most 1 hour old, spread <= 5c), put it in a YES-ask bucket, and score two
no-model bets held to settlement with the flat $10 stake and taker fee:
  - buy YES at the ask (the favorite side when the bucket is high)
  - buy NO at 1 - bid (the long-shot fade when the bucket is low)
Every number is reported per EVENT as well as per trade: all the strikes of one Bitcoin day
settle on the same price, so they are one bet, not eighteen. The split at 2026-03-13 and the
quarter-by-quarter signs are there to show whether a cell holds up over time.

Added by the 2026-11-10 review (docs/review-2026-11-10.md). Research only; nothing here trades.
"""
import datetime as dt
import json
import math
import statistics
from collections import defaultdict

from .. import config as C
from ..model import taker_fee
from . import data as D
from . import engine as E

OUT_MD = C.ROOT / "reports" / "ladder.md"
OUT_JSON = C.DASHBOARD_DATA / "ladder.json"
OOS_CUT = "2026-03-13"
BUCKETS = ((0.01, 0.04), (0.04, 0.07), (0.07, 0.12), (0.12, 0.25), (0.25, 0.50), (0.50, 0.75),
           (0.75, 0.88), (0.88, 0.93), (0.93, 0.96), (0.96, 0.995))
HOURS = (12, 6, 4, 3, 2, 1)
MIN_EVENTS = 30


def _ts(iso):
    return int(dt.datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp())


def _quarter(d):
    return f"{d[:4]}-Q{(int(d[5:7]) - 1) // 3 + 1}"


def event_stats(trades):
    """Return per $ staked, number of events, and a t-stat over events (one sample per event)."""
    if not trades:
        return None
    g = defaultdict(lambda: [0.0, 0.0])
    for t in trades:
        g[t["event"]][0] += t["pnl"]
        g[t["event"]][1] += t["cost"]
    rs = [p / c for p, c in g.values() if c]
    sd = statistics.stdev(rs) if len(rs) > 1 else 0.0
    staked = sum(t["cost"] for t in trades)
    return {"trades": len(trades), "events": len(rs), "win_rate": round(statistics.fmean(t["won"] for t in trades), 3),
            "pnl": round(sum(t["pnl"] for t in trades), 2), "roi": round(sum(t["pnl"] for t in trades) / staked, 4) if staked else None,
            "t_event": round(statistics.fmean(rs) / sd * math.sqrt(len(rs)), 2) if sd else None}


def ladder_trades(data, hours, lo, hi, side, max_spread=0.05, stake=E.STAKE):
    """All no-model trades for one cell: YES ask in [lo, hi) at `hours` before close, buy `side`."""
    ms, cs = data["markets"], data["candles"]
    out = []
    for ticker, c in cs.items():
        m = ms.get(ticker)
        if not m or m["result"] not in ("yes", "no") or not m.get("close_time"):
            continue
        close = _ts(m["close_time"])
        entry = close - hours * 3600
        q = E.quote(c, entry, max_age_h=1)
        if q is None or q[1] - q[0] > max_spread or not (lo <= q[1] < hi):
            continue
        bid, ask = q[0], q[1]
        price = ask if side == "yes" else 1 - bid
        n = max(1, math.floor(stake / price))
        cost = n * price + taker_fee(n, price, C.FEE_RATE)
        won = (m["result"] == "yes") == (side == "yes")
        out.append({"event": m["event_ticker"], "ticker": ticker, "ts": entry, "mid": (bid + ask) / 2,
                    "date": dt.datetime.fromtimestamp(close, dt.timezone.utc).date().isoformat(),
                    "side": side, "price": round(price, 4), "contracts": n, "cost": round(cost, 4),
                    "won": won, "pnl": round((n if won else 0) - cost, 4),
                    "volume_after": sum(x[3] or 0 for x in c if entry < x[0] <= close)})
    return out


def cell(data, hours, lo, hi):
    yes = ladder_trades(data, hours, lo, hi, "yes")
    if not yes:
        return None
    no = ladder_trades(data, hours, lo, hi, "no")
    old = [t for t in yes if t["date"] < OOS_CUT]
    new = [t for t in yes if t["date"] >= OOS_CUT]
    byq = defaultdict(list)
    for t in yes:
        byq[_quarter(t["date"])].append(t)
    quarters = {q: round(sum(t["pnl"] for t in v) / sum(t["cost"] for t in v), 4) for q, v in sorted(byq.items())}
    return {"hours": hours, "bucket": f"{lo * 100:.0f}-{hi * 100:.0f}c", "n": len(yes), "events": len({t["event"] for t in yes}),
            "market": round(statistics.fmean(t["mid"] for t in yes), 3),
            "actual": round(statistics.fmean(t["won"] for t in yes), 3),
            "yes": event_stats(yes), "no": event_stats(no),
            "yes_older": event_stats(old), "yes_newer": event_stats(new),
            "quarters_yes": quarters,
            "quarters_positive": f"{sum(1 for v in quarters.values() if v > 0)}/{len(quarters)}",
            "median_volume_after": round(statistics.median(t["volume_after"] for t in yes))}


def table(data, hours=HOURS, buckets=BUCKETS):
    rows = []
    for h in hours:
        for lo, hi in buckets:
            r = cell(data, h, lo, hi)
            if r:
                rows.append(r)
    return rows


def flagged(rows, min_events=MIN_EVENTS, t=2.5):
    """Cells where one side is clearly profitable at the EVENT level, in both periods."""
    out = []
    for r in rows:
        for side in ("yes", "no"):
            s = r[side]
            if not s or s["events"] < min_events or s["t_event"] is None or s["t_event"] < t:
                continue
            out.append({"hours": r["hours"], "bucket": r["bucket"], "side": side, **s})
    return out


def books():
    """Every ladder dataset in the cache: Bitcoin, Ethereum, weather highs/lows (all cities pooled)."""
    out = {"Bitcoin 5pm (KXBTCD)": D._load("kalshi_KXBTCD", None), "Ethereum 5pm (KXETHD)": D._load("kalshi_KXETHD", None)}
    for b in ("weather_high", "weather_low"):
        pooled = {"markets": {}, "candles": {}}
        for s in C.BOOKS[b]["series"]:
            d = D._load(f"kalshi_{s}", None)
            if d:
                pooled["markets"].update(d["markets"])
                pooled["candles"].update(d["candles"])
        out[C.BOOKS[b]["name"]] = pooled if pooled["candles"] else None
    return {k: v for k, v in out.items() if v and v.get("candles")}


def _pct(s, key="roi"):
    return "–" if not s or s.get(key) is None else f"{s[key] * 100:+.1f}%"


def _t(s):
    return "–" if not s or s.get("t_event") is None else f"{s['t_event']:.1f}"


def markdown(result):
    L = [f"# Price-level ladder test ({result['generated_at'][:10]})", "",
         "For each market, the quote H hours before close (at most 1h old, spread <= 5c) goes in a YES-ask bucket. "
         "Two no-model bets per bucket, $10 at the ask plus taker fee, held to settlement: buy YES, or buy NO at 1 - bid. "
         "**t is per event** (all strikes of one day are one bet). Older = before 2026-03-13. "
         f"Rows need {MIN_EVENTS}+ events. Flagged cells (|t| >= 2.5) are candidates, not proof: this table has about "
         "60 cells per book, so expect 1-3 flags by luck alone.", ""]
    for name, b in result["books"].items():
        L += [f"## {name}", "", f"{b['markets']} markets with candles, {b['events']} events, {b['first']} to {b['last']}.", "",
              "| Hours before | YES ask | n | Events | Market | Actual YES | Buy YES: return/$ | t(event) | Older | Newer | Quarters + | Buy NO: return/$ | t(event) | Median contracts after entry |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in b["rows"]:
            if r["events"] < MIN_EVENTS:
                continue
            flag = " **<==**" if any(x["hours"] == r["hours"] and x["bucket"] == r["bucket"] for x in b["flagged"]) else ""
            L.append(f"| {r['hours']}h | {r['bucket']} | {r['n']} | {r['events']} | {r['market']:.3f} | {r['actual']:.3f} | "
                     f"{_pct(r['yes'])} | {_t(r['yes'])} | {_pct(r['yes_older'])} | {_pct(r['yes_newer'])} | {r['quarters_positive']} | "
                     f"{_pct(r['no'])} | {_t(r['no'])} | {r['median_volume_after']}{flag} |")
        L.append("")
    return "\n".join(L)


def run(now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    result = {"generated_at": now.isoformat(timespec="minutes"), "books": {}}
    for name, data in books().items():
        rows = table(data)
        if not rows:
            continue
        dates = sorted(m["close_time"][:10] for m in data["markets"].values() if m.get("close_time") and m["ticker"] in data["candles"])
        result["books"][name] = {"markets": len(data["candles"]), "events": len({data["markets"][t]["event_ticker"] for t in data["candles"] if t in data["markets"]}),
                                 "first": dates[0] if dates else None, "last": dates[-1] if dates else None,
                                 "rows": rows, "flagged": flagged(rows)}
        D.log(f"ladder: {name}: {len(rows)} cells, {len(result['books'][name]['flagged'])} flagged")
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=1))
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(markdown(result))
    D.log(f"wrote {OUT_JSON} and {OUT_MD}")
    return result


if __name__ == "__main__":
    run()
