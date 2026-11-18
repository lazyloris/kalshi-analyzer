"""Fed decision test: Kalshi KXFEDDECISION vs Polymarket's (much bigger) Fed decision markets.

Idea: Polymarket's Fed markets trade $100M-$650M per meeting, Kalshi's far less. If Kalshi lags, buying on
Kalshi toward the Polymarket price and holding to the decision should pay.

Data (public, no keys): Kalshi settled markets + hourly candles (bid/ask); Polymarket Gamma events and
CLOB /prices-history (hourly last price). Outcomes matched by meeting month and by wording:
hold <-> "no change", cut 25 <-> "decrease ... 25 bps", cut >25 <-> "decrease ... 50+ bps".

Rule: at each lead before Kalshi's close, buy YES on Kalshi if poly_p - ask - fee > edge, or NO if
(1 - poly_p) - (1 - bid) - fee > edge. Taker, $1 contracts, fee 0.07 p (1-p). Hold to settlement.

Pass bar (written before the run): at some lead with a 5c edge, +5% per $, 60+ trades, meeting-clustered
t >= 3, both halves positive. About 25-30 meetings exist, so this is thin either way.
"""
import datetime as dt
import json
import math
import re
import statistics as stats
import time

from . import data as D
from .. import config as C
from ..http import get_json

GAMMA = "https://gamma-api.polymarket.com"
CLOB = "https://clob.polymarket.com"
LEADS = [14, 7, 3, 1, 0.25]
EDGES = [0.03, 0.05, 0.10]
MONTHS = {m: i for i, m in enumerate(["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"], 1)}
MONTH_NAMES = {v: k for k, v in MONTHS.items()}


def fee(p):
    return 0.07 * p * (1 - p)


def kalshi_outcome(ticker):
    suf = ticker.split("-")[-1]
    return {"H0": "hold", "C25": "cut25", "C26": "cut50"}.get(suf)


def poly_outcome(q):
    q = q.lower()
    if "no change" in q:
        return "hold"
    if "decrease" in q or "cut" in q:
        if re.search(r"50\+|50 \+|50 bps|>25|more than 25", q):
            return "cut50"
        if "25" in q:
            return "cut25"
    return None


def poly_events():
    found = {}
    for q in ("fed decision", "fed interest rates", "fed decision in", "fed interest rates 2023", "fed interest rates 2024",
              "fed decision 2025", "fed decision 2026"):
        try:
            r = get_json(f"{GAMMA}/public-search", {"q": q, "limit_per_type": 100, "events_status": "all"})
        except Exception as e:
            D.log(f"search {q}: {e}")
            continue
        for e in r.get("events") or []:
            s = e.get("slug") or ""
            if (s.startswith("fed-decision-in-") or s.startswith("fed-interest-rates-")) and e.get("closed"):
                found[s] = e
        time.sleep(0.5)
    out = {}
    for s, e in found.items():
        end = (e.get("endDate") or "")[:10]
        if not end:
            continue
        d = dt.date.fromisoformat(end)
        try:
            full = get_json(f"{GAMMA}/events", {"slug": s})[0]
        except Exception as ex:
            D.log(f"event {s}: {ex}")
            continue
        mk = {}
        for m in full.get("markets") or []:
            o = poly_outcome(m.get("question") or "")
            toks = json.loads(m.get("clobTokenIds") or "[]")
            if o and toks:
                mk[o] = toks[0]
        # endDate can fall on the day after the meeting in UTC; key by the month of the day before too
        for key in {(d.year, d.month), ((d - dt.timedelta(days=1)).year, (d - dt.timedelta(days=1)).month)}:
            if key not in out or len(mk) > len(out[key][1]):
                out[key] = (s, mk)
    D.log(f"polymarket: {len(found)} closed Fed events, {len(out)} meeting months")
    return out


def poly_history(token, start, end):
    try:
        h = get_json(f"{CLOB}/prices-history", {"market": token, "startTs": start, "endTs": end, "fidelity": 60}).get("history") or []
    except Exception as e:
        D.log(f"  history {token[:10]}: {e}")
        return []
    return [(int(x["t"]), float(x["p"])) for x in h]


def at(series, ts, max_age=6 * 3600):
    best = None
    for t, p in series:
        if t <= ts and ts - t <= max_age:
            best = p
    return best


def run():
    evs = get_json(f"{C.KALSHI_API}/events", {"series_ticker": "KXFEDDECISION", "limit": 200}).get("events") or []
    pm = poly_events()
    obs = []
    for e in evs:
        et = e["event_ticker"]
        tail = et.split("-")[-1]
        try:
            key = (2000 + int(tail[:2]), MONTHS[tail[2:5]])
        except (ValueError, KeyError):
            continue
        if key not in pm:
            continue
        rows = D.settled_markets(event_ticker=et)
        time.sleep(0.3)
        for m in rows:
            o = kalshi_outcome(m["ticker"])
            if not o or o not in pm[key][1]:
                continue
            close = D._ts(m["close_time"])
            cs = D.candles("KXFEDDECISION", m, hours_before=15 * 24)
            ph = poly_history(pm[key][1][o], close - 15 * 86400, close)
            for L in LEADS:
                ts = int(close - L * 86400)
                q = None
                for c in cs:
                    if c[0] <= ts and ts - c[0] <= 36 * 3600 and c[1] is not None and c[2] is not None and 0 < c[2] < 1:
                        q = c
                pp = at(ph, ts)
                if q is None or pp is None:
                    continue
                obs.append({"event": et, "outcome": o, "lead": L, "bid": q[1], "ask": q[2], "poly": pp,
                            "yes": m["result"] == "yes", "close": m["close_time"][:10]})
    D.log(f"{len(obs)} observations over {len({o['event'] for o in obs})} meetings")
    return obs


def summarize(obs):
    out = {"brier": {}, "trades": {}}
    for L in LEADS:
        o = [x for x in obs if x["lead"] == L]
        if not o:
            continue
        out["brier"][L] = {"n": len(o), "meetings": len({x["event"] for x in o}),
                           "kalshi_mid": round(stats.fmean(((x["bid"] + x["ask"]) / 2 - x["yes"]) ** 2 for x in o), 4),
                           "polymarket": round(stats.fmean((x["poly"] - x["yes"]) ** 2 for x in o), 4),
                           "mean_gap_c": round(100 * stats.fmean(abs(x["poly"] - (x["bid"] + x["ask"]) / 2) for x in o), 2)}
        for e in EDGES:
            tr = []
            for x in o:
                a, b, p = x["ask"], x["bid"], x["poly"]
                if p - a - fee(a) > e:
                    tr.append((x, a + fee(a), 1.0 if x["yes"] else 0.0))
                elif (1 - p) - (1 - b) - fee(1 - b) > e and b > 0:
                    tr.append((x, (1 - b) + fee(1 - b), 0.0 if x["yes"] else 1.0))
            if not tr:
                continue
            cost = sum(t[1] for t in tr)
            pnl = sum(t[2] - t[1] for t in tr)
            by = {}
            for t in tr:
                by[t[0]["event"]] = by.get(t[0]["event"], 0) + t[2] - t[1]
            v = list(by.values())
            tstat = stats.fmean(v) / (stats.stdev(v) / math.sqrt(len(v))) if len(v) > 2 and stats.stdev(v) > 0 else 0
            days = sorted(t[0]["close"] for t in tr)
            mid = days[len(days) // 2]
            out["trades"][f"{L}|{e}"] = {"lead": L, "edge": e, "n": len(tr), "meetings": len(v),
                                         "win": round(stats.fmean(t[2] for t in tr), 3), "roi": round(pnl / cost, 4),
                                         "pnl": round(pnl, 2), "t": round(tstat, 2),
                                         "half1": round(sum(t[2] - t[1] for t in tr if t[0]["close"] < mid), 2),
                                         "half2": round(sum(t[2] - t[1] for t in tr if t[0]["close"] >= mid), 2)}
    return out


def main():
    obs = run()
    s = summarize(obs)
    for L, b in s["brier"].items():
        print(f"lead {L}d: Brier Kalshi {b['kalshi_mid']} vs Polymarket {b['polymarket']}, mean gap {b['mean_gap_c']}c, "
              f"{b['n']} quotes / {b['meetings']} meetings")
    for t in s["trades"].values():
        print(f"  lead {t['lead']}d edge {t['edge']}: {t['n']} trades / {t['meetings']} meetings, win {t['win']}, "
              f"{t['roi']:+.1%}/$, ${t['pnl']:+.2f}, t {t['t']}, halves {t['half1']:+.2f}/{t['half2']:+.2f}")
    C.DATA_DIR.mkdir(parents=True, exist_ok=True)
    (C.DATA_DIR / "fed_test.json").write_text(json.dumps({"summary": s, "obs": obs}, default=str))


if __name__ == "__main__":
    main()
