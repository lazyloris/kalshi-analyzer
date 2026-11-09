"""Swing pairing (swisstony-style) on 1-minute Kalshi data. python -m kalshi_analyzer.swing --days 90

Rule: when one side's price drops D cents within 5 minutes, buy that side (taker, fee). If the price
later swings back up X cents, lock in: buying the other side then makes YES + NO cost under $1, so we
are paid whichever side wins (same money as selling at the bid). If it never swings back, we are stuck
holding one side to settlement. One open position per market at a time. Read-only.

Groups: live sports games (Kalshi "...GAME" series in Sports), Bitcoin/Ethereum daily (reuses the
minute-lag download if present).
"""
import argparse
import datetime as dt
import json
import math
import statistics
from collections import defaultdict

from . import config as C
from .backtest import data as D
from .http import get_json
from .model import taker_fee

K = C.KALSHI_API
OUT_MD = C.ROOT / "reports" / "swing.md"
OUT_JSON = C.ROOT / "dashboard" / "data" / "swing.json"


def game_series():
    data = get_json(f"{K}/series", {"limit": 20000}, retries=5, timeout=120)
    out = [s["ticker"] for s in data.get("series") or []
           if (s.get("category") or "") == "Sports" and s["ticker"].endswith("GAME")]
    D.log(f"sports game series: {out}")
    return out


def last_trade_ts(m):
    for u in (f"{K}/markets/trades", f"{K}/historical/trades"):
        try:
            tr = get_json(u, {"ticker": m["ticker"], "limit": 1}, retries=3).get("trades") or []
        except Exception:
            continue
        if tr:
            t = tr[0].get("created_time")
            if t:
                return int(dt.datetime.fromisoformat(t.replace("Z", "+00:00")).timestamp())
    return None


def minute_candles(series, m, start, end):
    urls = [f"{K}/series/{series}/markets/{m['ticker']}/candlesticks", f"{K}/historical/markets/{m['ticker']}/candlesticks"]
    if m["source"] == "historical":
        urls.reverse()
    for u in urls:
        try:
            cs = D._parse_candles(get_json(u, {"start_ts": start, "end_ts": end, "period_interval": 1}, retries=3))
            if cs:
                return cs
        except Exception:
            continue
    return []


MAJOR = ("KXNFLGAME", "KXNBAGAME", "KXMLBGAME", "KXNHLGAME", "KXNCAAFGAME", "KXNCAAMBGAME", "KXEPLGAME",
         "KXUCLGAME", "KXLALIGAGAME", "KXSERIEAGAME", "KXBUNDESLIGAGAME", "KXMLSGAME", "KXATPGAME", "KXWTAGAME",
         "KXWNBAGAME", "KXLIGUE1GAME")


def fetch_sports(days, per_series=400, max_markets=5000):
    """Major leagues first, at most `per_series` markets each (eSoccer alone has 45k)."""
    cache = D._load("swing_sports", {"markets": {}})
    since = dt.date.today() - dt.timedelta(days=days)
    available = game_series()
    order = [x for x in MAJOR if x in available] + [x for x in available if x not in MAJOR]
    todo = []
    for s in order:
        ms = D.settled_markets(series=s, since=since)
        D.log(f"{s}: {len(ms)} settled markets")
        todo += [(s, m) for m in ms[:per_series] if m["ticker"] not in cache["markets"]]
    for i, (s, m) in enumerate(todo[:max_markets]):
        end = last_trade_ts(m)
        if not end:
            cache["markets"][m["ticker"]] = None
            continue
        cs = minute_candles(s, m, end - 4 * 3600, end)  # the live game is roughly the last 4 hours of trading
        cache["markets"][m["ticker"]] = {"series": s, "result": m["result"], "cs": cs} if len(cs) > 30 else None
        if i % 200 == 0:
            D.log(f"  sports {i}/{len(todo)}")
            D._save("swing_sports", cache)
    D._save("swing_sports", cache)
    return {t: v for t, v in cache["markets"].items() if v}


def crypto_markets():
    from . import minute_lag
    out = {}
    for asset in ("BTC", "ETH"):
        try:
            minute_lag.fetch(120, asset)  # uses the cached download when present
        except Exception as e:
            D.log(f"crypto minute data {asset}: {e}")
    for name in ("minute_lag", "minute_lag_ETH"):
        c = D._load(name, {"events": {}})
        for ev, e in c["events"].items():
            for m in e["markets"]:
                out[m["ticker"]] = {"series": ev.split("-")[0], "result": m["result"], "cs": m["cs"]}
    return out


def simulate(markets, drop=0.10, rebound=0.05, lookback=5, stake=10.0, max_spread=0.05):
    trades = []
    for tk, m in markets.items():
        cs = [c for c in m["cs"] if c[1] is not None and c[2] is not None and 0 < c[1] <= c[2] < 1]
        won_yes = m["result"] == "yes"
        i = lookback
        while i < len(cs):
            t, bid, ask = cs[i][0], cs[i][1], cs[i][2]
            prev = cs[i - lookback]
            if prev[0] < t - (lookback + 2) * 60 or ask - bid > max_spread:
                i += 1
                continue
            mid, pmid = (bid + ask) / 2, (prev[1] + prev[2]) / 2
            side = "yes" if pmid - mid >= drop else "no" if mid - pmid >= drop else None
            if side is None:
                i += 1
                continue
            price = ask if side == "yes" else 1 - bid
            if not 0.05 <= price <= 0.95:
                i += 1
                continue
            n = max(1, math.floor(stake / price))
            cost = n * price + taker_fee(n, price, C.FEE_RATE)
            out, j = None, i + 1
            while j < len(cs):
                b = cs[j][1] if side == "yes" else 1 - cs[j][2]  # what our side sells for (= other side's cost to lock)
                if b >= price + rebound:
                    other = 1 - b
                    lock_cost = n * other + taker_fee(n, other, C.FEE_RATE)
                    out = {"pnl": n - cost - lock_cost, "locked": True, "exit_ts": cs[j][0]}
                    break
                j += 1
            if out is None:
                won = won_yes if side == "yes" else not won_yes
                out = {"pnl": (n if won else 0) - cost, "locked": False, "exit_ts": None}
                j = len(cs)
            trades.append({"ticker": tk, "series": m["series"], "ts": t, "side": side, "price": round(price, 3),
                           "cost": round(cost, 3), "pnl": round(out["pnl"], 3), "locked": out["locked"],
                           "date": dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat()})
            i = j + 1
    return trades


def summary(trades):
    if not trades:
        return {"trades": 0}
    staked = sum(t["cost"] for t in trades)
    pnl = sum(t["pnl"] for t in trades)
    lk = [t for t in trades if t["locked"]]
    s = sorted(trades, key=lambda t: t["ts"])
    h = len(s) // 2
    by_mkt = defaultdict(float)
    for t in trades:
        by_mkt[t["ticker"]] += t["pnl"]
    rs = list(by_mkt.values())
    sd = statistics.pstdev(rs) if len(rs) > 1 else 0
    return {"trades": len(trades), "markets": len(by_mkt), "pnl": round(pnl, 2), "roi": round(pnl / staked, 4),
            "lock_rate": round(len(lk) / len(trades), 3),
            "pnl_locked": round(sum(t["pnl"] for t in lk), 1), "pnl_stuck": round(pnl - sum(t["pnl"] for t in lk), 1),
            "t_markets": round(statistics.fmean(rs) / sd * math.sqrt(len(rs)), 2) if sd else None,
            "first_half": round(sum(t["pnl"] for t in s[:h]), 1), "second_half": round(sum(t["pnl"] for t in s[h:]), 1)}


def run(days):
    groups = {"Sports games": fetch_sports(days), "Bitcoin/Ethereum daily": crypto_markets()}
    L = [f"# Swing pairing test ({dt.date.today()})", "",
         "Buy the side that just dropped D cents in 5 minutes; lock in when it swings back X cents (buying the "
         "other side so the pair costs under $1); otherwise hold to settlement. Taker fees on every leg. "
         "1-minute Kalshi quotes. t is per market (trades in one game move together).", ""]
    out = {}
    for g, mk in groups.items():
        rows = []
        for drop in (0.05, 0.10, 0.15):
            for reb in (0.03, 0.05, 0.10):
                rows.append({"drop": drop, "rebound": reb, **summary(simulate(mk, drop, reb))})
        rows.sort(key=lambda r: -(r.get("pnl") or -1e9))
        out[g] = {"markets": len(mk), "rows": rows}
        by_series = defaultdict(int)
        for v in mk.values():
            by_series[v["series"]] += 1
        L += [f"## {g} ({len(mk)} markets: " + ", ".join(f"{k} {v}" for k, v in sorted(by_series.items(), key=lambda x: -x[1])[:8]) + ")", "",
              "| Drop | Swing back | Trades | Markets | Locked | P&L | Return/$ | From locks | From stuck | t | 1st half | 2nd half |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for r in rows:
            L.append(f"| {r['drop'] * 100:.0f}c | {r['rebound'] * 100:.0f}c | {r['trades']} | {r.get('markets', 0)} | "
                     f"{(r.get('lock_rate') or 0) * 100:.0f}% | {r.get('pnl', 0):+.1f} | {(r.get('roi') or 0) * 100:+.1f}% | "
                     f"{r.get('pnl_locked', 0):+.0f} | {r.get('pnl_stuck', 0):+.0f} | {r.get('t_markets') or '–'} | "
                     f"{r.get('first_half', 0):+.0f} | {r.get('second_half', 0):+.0f} |")
        L.append("")
    L += ["9 settings per group, so the best row is flattered. Taker-only: real swing traders post limit "
          "orders and earn the spread, which candles can't show.", ""]
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(L))
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=1))
    D.log(f"wrote {OUT_MD}")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m kalshi_analyzer.swing")
    ap.add_argument("--days", type=int, default=90)
    run(ap.parse_args(argv).days)


if __name__ == "__main__":
    main()
