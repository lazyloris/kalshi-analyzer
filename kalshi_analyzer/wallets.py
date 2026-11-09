"""Study Polymarket's top wallets (read only, public data). python -m kalshi_analyzer.wallets

1. Who they are: the all-time profit leaderboard (+ any wallets named with --names).
2. How they trade: share of sports, how often they buy BOTH sides of one market (and whether the
   two sides together cost under $1, which locks in a profit), price levels they buy at.
3. Does skill persist: rank wallets on markets that ended before 2026, then look at 2026.
4. Can you copy them: for a sample of their buys, the price 1, 10 and 60 minutes later (what a
   copier would pay), held to resolution. Also shows whether prices drift their way after they buy
   (that drift is what copiers pay for).
Nothing here places orders. API field names are logged on first use because they are not
documented as stable.
"""
import argparse
import datetime as dt
import json
import statistics
import time
from collections import defaultdict

from . import config as C
from .http import get_json

DATA = "https://data-api.polymarket.com"
GAMMA = "https://gamma-api.polymarket.com"
CLOB = "https://clob.polymarket.com"
OUT_JSON = C.ROOT / "dashboard" / "data" / "wallets.json"
OUT_MD = C.ROOT / "reports" / "wallets.md"
SPORTS = ("nba", "nfl", "mlb", "nhl", "epl", "ucl", "cbb", "cfb", "ncaa", "atp", "wta", "ufc", "mls", "lal", "sea",
          "bun", "fl1", "itsa", "tennis", "soccer", "football", "basketball", "baseball", "hockey", "cricket",
          "esports", "lol", "cs2", "dota", "valorant", "f1", "golf", "boxing")
CUT = int(dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc).timestamp())
_seen_keys = set()


def log(msg):
    print(f"[wallets] {msg}", flush=True)


def _get(url, params=None, label=None):
    time.sleep(0.15)
    r = get_json(url, params, retries=4)
    if label and label not in _seen_keys:
        _seen_keys.add(label)
        sample = r[0] if isinstance(r, list) and r else r
        log(f"{label} sample keys: {sorted(sample)[:40] if isinstance(sample, dict) else type(sample).__name__}")
    return r


def _rows(r):
    if isinstance(r, list):
        return r
    if isinstance(r, dict):
        for k in ("data", "results", "leaderboard", "items", "history"):
            if isinstance(r.get(k), list):
                return r[k]
    return []


def _f(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def leaderboard(n=50):
    out = []
    for o in range(0, n, 50):
        try:
            rows = _rows(_get(f"{DATA}/v1/leaderboard", {"category": "OVERALL", "timePeriod": "ALL", "orderBy": "PNL",
                                                          "limit": 50, "offset": o}, "leaderboard"))
        except Exception as e:
            log(f"leaderboard v1 failed: {e}")
            rows = []
        if not rows and o == 0:
            rows = _rows(_get("https://lb-api.polymarket.com/profit", {"window": "all", "limit": n}, "lb-api"))
        for r in rows:
            w = r.get("proxyWallet") or r.get("address") or r.get("wallet")
            if w:
                out.append({"wallet": w.lower(), "name": r.get("userName") or r.get("name") or r.get("pseudonym") or "",
                            "pnl": _f(r.get("pnl") or r.get("amount")), "vol": _f(r.get("vol") or r.get("volume"))})
        if len(rows) < 50:
            break
    seen, uniq = set(), []
    for r in out:
        if r["wallet"] not in seen:
            seen.add(r["wallet"])
            uniq.append(r)
    return uniq[:n]


def find_wallet(name):
    try:
        r = _get(f"{GAMMA}/public-search", {"q": name, "search_profiles": "true", "limit_per_type": 5}, "search")
        for p in (r.get("profiles") or []) if isinstance(r, dict) else []:
            if (p.get("name") or p.get("pseudonym") or "").lower() == name.lower() and p.get("proxyWallet"):
                return {"wallet": p["proxyWallet"].lower(), "name": p.get("name") or name, "pnl": None, "vol": None}
    except Exception as e:
        log(f"search {name} failed: {e}")
    return None


def trades(wallet, max_n=10000):
    out = []
    for o in range(0, max_n, 500):
        try:
            rows = _rows(_get(f"{DATA}/trades", {"user": wallet, "limit": 500, "offset": o, "takerOnly": "false"}, "trades"))
        except Exception as e:
            log(f"  trades {wallet[:10]} offset {o}: {e}")
            break
        out += rows
        if len(rows) < 500:
            break
    return out


def closed_positions(wallet, max_n=5000):
    out = []
    for o in range(0, max_n, 50):
        try:
            rows = _rows(_get(f"{DATA}/closed-positions", {"user": wallet, "limit": 50, "offset": o,
                                                            "sortBy": "TIMESTAMP", "sortDirection": "DESC"}, "closed"))
        except Exception as e:
            log(f"  closed {wallet[:10]} offset {o}: {e}")
            break
        out += rows
        if len(rows) < 50:
            break
    return out


def is_sports(t):
    s = f"{t.get('eventSlug') or ''} {t.get('slug') or ''}".lower()
    return any(s.startswith(k + "-") or f"-{k}-" in s for k in SPORTS) or " vs" in (t.get("title") or "").lower()


def style(tr):
    """How a wallet trades, from its recent trades."""
    if not tr:
        return {}
    buys = [t for t in tr if (t.get("side") or "").upper() == "BUY"]
    by_mkt = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0]))  # cond -> outcomeIndex -> [size, cost]
    for t in buys:
        b = by_mkt[t.get("conditionId")][t.get("outcomeIndex", t.get("outcome"))]
        b[0] += _f(t.get("size"))
        b[1] += _f(t.get("size")) * _f(t.get("price"))
    both = [m for m in by_mkt.values() if len(m) >= 2]
    combined, locked = [], 0
    for m in both:
        sides = sorted(m.values(), key=lambda v: -v[0])[:2]
        avg = [c / s for s, c in sides if s]
        if len(avg) == 2:
            combined.append(sum(avg))
            locked += sum(avg) < 0.99
    ts = [int(_f(t.get("timestamp"))) for t in tr if t.get("timestamp")]
    prices = [_f(t.get("price")) for t in buys]
    usd = [_f(t.get("size")) * _f(t.get("price")) for t in tr]
    return {
        "trades": len(tr), "markets": len({t.get("conditionId") for t in tr}),
        "from": dt.datetime.fromtimestamp(min(ts), dt.timezone.utc).date().isoformat() if ts else None,
        "to": dt.datetime.fromtimestamp(max(ts), dt.timezone.utc).date().isoformat() if ts else None,
        "sports_share": round(sum(is_sports(t) for t in tr) / len(tr), 3),
        "sell_share": round(1 - len(buys) / len(tr), 3),
        "median_usd": round(statistics.median(usd), 2) if usd else None,
        "both_sides_share": round(len(both) / len(by_mkt), 3) if by_mkt else None,
        "both_sides_avg_cost": round(statistics.fmean(combined), 4) if combined else None,
        "both_sides_locked_share": round(locked / len(combined), 3) if combined else None,
        "buy_price_mix": {k: round(sum(lo <= p < hi for p in prices) / len(prices), 3) if prices else None
                          for k, lo, hi in (("<10c", 0, .1), ("10-50c", .1, .5), ("50-90c", .5, .9), (">=90c", .9, 1.01))},
    }


def pnl_split(closed):
    """Realized P&L before/after 2026 and by sports vs other, from closed positions."""
    out = {"pre2026": 0.0, "y2026": 0.0, "sports": 0.0, "other": 0.0, "n": len(closed), "win_rate": None}
    wins = 0
    for p in closed:
        v = _f(p.get("realizedPnl") or p.get("cashPnl"))
        ts = p.get("timestamp") or p.get("endDate")
        t = int(_f(ts)) if str(ts).replace(".", "").isdigit() else (
            int(dt.datetime.fromisoformat(str(ts).replace("Z", "+00:00")).timestamp()) if ts else CUT)
        out["pre2026" if t < CUT else "y2026"] += v
        out["sports" if is_sports(p) else "other"] += v
        wins += v > 0
    if closed:
        out["win_rate"] = round(wins / len(closed), 3)
    return {k: (round(v, 2) if isinstance(v, float) else v) for k, v in out.items()}


_res_cache = {}


def resolution(cond):
    """{outcomeIndex: 1.0/0.0} once resolved, else None."""
    if cond in _res_cache:
        return _res_cache[cond]
    res = None
    try:
        rows = _rows(_get(f"{GAMMA}/markets", {"condition_ids": cond}, "gamma_market"))
        if rows:
            m = rows[0]
            prices = m.get("outcomePrices")
            prices = json.loads(prices) if isinstance(prices, str) else prices
            if m.get("closed") and prices and all(_f(p) in (0.0, 1.0) for p in prices):
                res = {i: _f(p) for i, p in enumerate(prices)}
    except Exception as e:
        log(f"  resolution {cond[:10]}: {e}")
    _res_cache[cond] = res
    return res


def price_after(asset, ts, delays=(60, 600, 3600)):
    try:
        h = _rows(_get(f"{CLOB}/prices-history", {"market": asset, "startTs": ts - 120, "endTs": ts + max(delays) + 300,
                                                   "fidelity": 1}, "prices_history"))
    except Exception:
        return None
    pts = sorted((int(_f(x.get("t"))), _f(x.get("p"))) for x in h if x.get("t"))
    if not pts:
        return None
    out = {}
    for d in delays:
        after = [p for t, p in pts if t >= ts + d]
        out[d] = after[0] if after else None
    return out


def copy_test(tr, sample=150, slip=0.01):
    """Recent BUYs: wallet's own return vs a copier entering 1/10/60 min later (+1c slippage), held
    to resolution. Fees assumed 0 (most Polymarket markets); slippage covers the spread."""
    buys = sorted((t for t in tr if (t.get("side") or "").upper() == "BUY" and t.get("asset")),
                  key=lambda t: -int(_f(t.get("timestamp"))))
    rows = []
    for t in buys:
        if len(rows) >= sample:
            break
        res = resolution(t.get("conditionId"))
        if res is None:
            continue
        won = res.get(int(_f(t.get("outcomeIndex"), -1)))
        if won is None:
            continue
        p0, ts = _f(t.get("price")), int(_f(t.get("timestamp")))
        if not 0.01 <= p0 <= 0.99:
            continue
        later = price_after(t["asset"], ts)
        if not later:
            continue
        rows.append({"p0": p0, "won": won, "sports": is_sports(t), **{f"p{d}": v for d, v in later.items()}})
    if not rows:
        return {}

    def ret(p, won):
        p = min(p + slip, 0.995)
        return (won - p) / p

    out = {"n": len(rows), "own_roi": round(statistics.fmean((r["won"] - r["p0"]) / r["p0"] for r in rows), 4)}
    for d, label in ((60, "1m"), (600, "10m"), (3600, "60m")):
        rs = [r for r in rows if r.get(f"p{d}") is not None]
        if rs:
            out[f"copy_{label}_roi"] = round(statistics.fmean(ret(r[f"p{d}"], r["won"]) for r in rs), 4)
            out[f"drift_{label}"] = round(statistics.fmean(r[f"p{d}"] - r["p0"] for r in rs), 4)
            out[f"copy_{label}_n"] = len(rs)
    return out


def run(top=30, names=("swisstony",), deep=15, copy_sample=150):
    lb = leaderboard(max(top, 50))
    log(f"leaderboard: {len(lb)} wallets")
    wallets = lb[:top]
    for n in names:
        hit = next((w for w in lb if w["name"].lower() == n.lower()), None) or find_wallet(n)
        if hit and hit["wallet"] not in {w["wallet"] for w in wallets}:
            wallets.append(hit)
        log(f"{n}: {'found ' + hit['wallet'] if hit else 'NOT FOUND'}")
    result = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"), "wallets": []}
    for i, w in enumerate(wallets):
        log(f"[{i + 1}/{len(wallets)}] {w['name'] or w['wallet'][:10]}")
        tr = trades(w["wallet"])
        closed = closed_positions(w["wallet"])
        row = {**w, "style": style(tr), "pnl_split": pnl_split(closed)}
        if i < deep or w["name"].lower() in {n.lower() for n in names}:
            row["copy"] = copy_test(tr, copy_sample)
        result["wallets"].append(row)
        OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUT_JSON.write_text(json.dumps(result, indent=1))
    result["persistence"] = persistence(result["wallets"])
    OUT_JSON.write_text(json.dumps(result, indent=1))
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(markdown(result))
    log(f"wrote {OUT_MD}")
    return result


def persistence(rows):
    """Among these wallets: did the best pre-2026 earners also earn the most in 2026?"""
    xs = [(r["pnl_split"]["pre2026"], r["pnl_split"]["y2026"]) for r in rows if r.get("pnl_split", {}).get("n")]
    if len(xs) < 6:
        return None
    xs.sort(key=lambda x: -x[0])
    h = len(xs) // 2
    top, bot = xs[:h], xs[h:]
    return {"wallets": len(xs), "top_half_2026": round(statistics.fmean(y for _, y in top), 2),
            "bottom_half_2026": round(statistics.fmean(y for _, y in bot), 2),
            "positive_2026_share": round(sum(y > 0 for _, y in xs) / len(xs), 3)}


def _pct(v):
    return "–" if v is None else f"{v * 100:.0f}%"


def _roi(v):
    return "–" if v is None else f"{v * 100:+.1f}%"


def markdown(r):
    L = [f"# Polymarket top wallets ({r['generated_at'][:10]})", "",
         "Read-only study of public trades. Recent trades only (the API returns up to ~10,000 per wallet). "
         "Copy returns assume a 1c worse fill and no fees, held to resolution.", ""]
    p = r.get("persistence")
    if p:
        L += ["## Does skill persist?", "",
              f"Of {p['wallets']} wallets, the half that earned most before 2026 averaged {p['top_half_2026']:+,.0f} in 2026; "
              f"the other half averaged {p['bottom_half_2026']:+,.0f}. {_pct(p['positive_2026_share'])} made money in 2026.", ""]
    L += ["## How they trade", "",
          "| Wallet | All-time P&L | Trades seen | Sports | Sells | Buys both sides | Both sides cost | Locked-in share | Buys >=90c | Buys <10c |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for w in r["wallets"]:
        s = w.get("style") or {}
        mix = s.get("buy_price_mix") or {}
        L.append(f"| {w['name'] or w['wallet'][:10]} | {format(w['pnl'], '+,.0f') if w.get('pnl') is not None else '–'} | "
                 f"{s.get('trades', 0)} | {_pct(s.get('sports_share'))} | {_pct(s.get('sell_share'))} | "
                 f"{_pct(s.get('both_sides_share'))} | {s.get('both_sides_avg_cost') or '–'} | "
                 f"{_pct(s.get('both_sides_locked_share'))} | {_pct(mix.get('>=90c'))} | {_pct(mix.get('<10c'))} |")
    L += ["", "Both sides cost = average price of side A + side B in markets where they bought both. Under $1.00 "
              "means the pair pays out more than it cost whichever side wins (a locked-in profit).", "",
          "## Realized P&L split (closed positions)", "",
          "| Wallet | Positions | Win rate | Before 2026 | 2026 | Sports | Other |", "|---|---|---|---|---|---|---|"]
    for w in r["wallets"]:
        q = w.get("pnl_split") or {}
        L.append(f"| {w['name'] or w['wallet'][:10]} | {q.get('n', 0)} | {_pct(q.get('win_rate'))} | {q.get('pre2026', 0):+,.0f} | "
                 f"{q.get('y2026', 0):+,.0f} | {q.get('sports', 0):+,.0f} | {q.get('other', 0):+,.0f} |")
    L += ["", "## Copying them", "",
          "| Wallet | Buys tested | Their return | Copy 1 min later | Copy 10 min | Copy 60 min | Price drift 1m / 10m / 60m |",
          "|---|---|---|---|---|---|---|"]
    for w in r["wallets"]:
        c = w.get("copy")
        if not c:
            continue
        d = " / ".join("–" if c.get(f"drift_{k}") is None else f"{c[f'drift_{k}'] * 100:+.1f}c" for k in ("1m", "10m", "60m"))
        L.append(f"| {w['name'] or w['wallet'][:10]} | {c['n']} | {_roi(c.get('own_roi'))} | {_roi(c.get('copy_1m_roi'))} | "
                 f"{_roi(c.get('copy_10m_roi'))} | {_roi(c.get('copy_60m_roi'))} | {d} |")
    L += ["", "Positive drift = the price moved their way after they bought (copiers pay that move).", ""]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m kalshi_analyzer.wallets")
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--deep", type=int, default=15, help="how many wallets get the (slow) copy test")
    ap.add_argument("--names", default="swisstony", help="comma-separated usernames to include")
    a = ap.parse_args(argv)
    run(a.top, tuple(n for n in a.names.split(",") if n), a.deep)


if __name__ == "__main__":
    main()
