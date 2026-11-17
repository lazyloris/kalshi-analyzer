"""Inflation test: does the Cleveland Fed's daily CPI nowcast beat Kalshi's monthly CPI markets?

Data (all public, no keys):
  - Kalshi KXCPI (headline CPI, month over month) and KXCPICORE (core) settled markets + hourly candles.
    expiration_value is the released number (single decimal).
  - Cleveland Fed nowcast_month.json: for each target month, the nowcast as published each business day
    (real-time vintages, so no look-ahead if we only use values dated before the entry day).
  - The nowcast's error spread at each lead is measured walk-forward: only from events released before the
    one being traded (12 needed), so the first year is calibration only.

Model: released value X (rounded to 0.1) ~ Normal(nowcast, sigma(lead)). YES on "more than K" wins when
the unrounded value is >= K + 0.05, so P(YES) = 1 - Phi((K + 0.05 - nowcast) / sigma).

Rule: at each lead (days before the 8:30am ET release) buy YES if P - ask - fee > edge, or NO if
(1 - P) - (1 - bid) - fee > edge. Taker, $1 contracts, fee 0.07 p (1-p).

Pass bar (written before the run): at some lead, edge 5c: return >= +5% per $, at least 100 trades,
event-clustered t >= 3, both halves of the period positive. Only ~60 events exist per series, so even a
pass is thin evidence.
"""
import csv
import datetime as dt
import io
import json
import math
import statistics as stats
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from . import data as D
from .. import config as C
from ..http import get_json

NOWCAST = "https://www.clevelandfed.org/-/media/files/webcharts/inflationnowcasting/nowcast_month.json"
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="
SERIES = {"KXCPI": ("CPI Inflation", "CPIAUCSL"), "KXCPICORE": ("Core CPI Inflation", "CPILFESL")}
LEADS = [14, 7, 3, 1, 0.125]          # days before release (0.125 = 3 hours)
EDGES = [0.03, 0.05, 0.10]
MONTHS = {m: i for i, m in enumerate(["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"], 1)}
UTC = dt.timezone.utc


def raw(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research script)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def fee(p):
    return 0.07 * p * (1 - p)


def nowcasts():
    """{(year, month): {series_name: [(date, value), ...]}} with real-time daily vintages."""
    out = {}
    for blk in json.loads(raw(NOWCAST)):
        sub = blk["chart"]["subcaption"]
        y, m = (int(x) for x in sub.split("-"))
        cats = [c["label"] for c in blk["categories"][0]["category"] if not c.get("vline")]
        dates = []
        for lab in cats:
            mm, dd = (int(x) for x in lab.split("/"))
            yy = y + 1 if mm < m else y          # vintages run into the following months
            dates.append(dt.date(yy, mm, dd))
        row = {}
        for ds in blk["dataset"]:
            vals = [(d, float(p["value"])) for d, p in zip(dates, ds["data"]) if p.get("value") not in ("", None)]
            row[ds["seriesname"]] = vals
        out[(y, m)] = row
    return out


def fred_mom(sid):
    rows = list(csv.reader(io.StringIO(raw(FRED + sid))))[1:]
    lv = [(dt.date.fromisoformat(r[0]), float(r[1])) for r in rows if r[1] not in ("", ".")]
    return {(d.year, d.month): round(100 * (v / lv[i - 1][1] - 1), 1) for i, (d, v) in enumerate(lv) if i}


def vintage(series_vals, before):
    """Latest nowcast dated strictly before `before` (a date)."""
    best = None
    for d, v in series_vals:
        if d < before:
            best = v
    return best


def sigma_table(nc, name, fred, release_guess_day=12):
    """Nowcast error by lead, 2013-07 to 2021-06 only (pre-test). Release day approximated as the 12th of
    the following month; leads are counted back from it."""
    errs = {L: [] for L in LEADS}
    for (y, m), row in nc.items():
        if (y, m) > (2021, 6) or (y, m) not in fred or name not in row:
            continue
        ry, rm = (y + 1, 1) if m == 12 else (y, m + 1)
        rel = dt.date(ry, rm, release_guess_day)
        for L in LEADS:
            v = vintage(row[name], rel - dt.timedelta(days=max(1, math.ceil(L))))
            if v is not None:
                errs[L].append(fred[(y, m)] - v)
    return {L: (math.sqrt(stats.fmean(e * e for e in es)) if len(es) > 10 else None, len(es)) for L, es in errs.items()}


def target_month(event_ticker):
    tail = event_ticker.split("-")[-1]
    return 2000 + int(tail[:2]), MONTHS[tail[2:5]]


def load_markets(series):
    evs = get_json(f"{C.KALSHI_API}/events", {"series_ticker": series, "limit": 200}).get("events") or []
    tickers = [e["event_ticker"] for e in evs]
    rows = []
    for t in tickers:                      # one at a time: parallel calls hit 429s and dropped old events
        rs = D.settled_markets(event_ticker=t)
        if not rs:
            time.sleep(3)
            rs = D.settled_markets(event_ticker=t)
        rows += rs
        time.sleep(0.3)
    rows = [r for r in rows if r["strike_type"] == "greater" and r["floor"] is not None]
    D.log(f"{series}: {len(tickers)} events, {len(rows)} settled 'greater' markets")

    def job(m):
        try:
            return m["ticker"], D.candles(series, m, hours_before=15 * 24)
        except Exception as e:
            D.log(f"  candles {m['ticker']}: {e}")
            return m["ticker"], []
    with ThreadPoolExecutor(2) as ex:
        cs = dict(ex.map(job, rows))
    return rows, cs


def quote_at(cands, ts):
    best = None
    for c in cands:
        if c[0] <= ts and ts - c[0] <= 36 * 3600 and c[1] is not None and c[2] is not None and 0 < c[2] <= 1:
            best = c
    return best


def run(series):
    """Walk-forward: the nowcast's error spread at each lead is measured only on events released before the
    one being traded (needs 12 earlier events), using Kalshi's own released values. No outside data needed."""
    name, _ = SERIES[series]
    nc = nowcasts()
    rows, cs = load_markets(series)
    events = {}
    for m in rows:
        events.setdefault(m["event_ticker"], []).append(m)
    order = sorted(events, key=lambda e: events[e][0]["close_time"])
    hist = {L: [] for L in LEADS}
    obs, sig_used = [], {}
    for ev in order:
        ms = events[ev]
        ym = target_month(ev)
        try:
            actual = float(next(m["value"] for m in ms if m["value"] not in ("", None)))
        except (StopIteration, ValueError):
            actual = None
        if ym not in nc or name not in nc[ym]:
            continue
        close = dt.datetime.fromisoformat(ms[0]["close_time"].replace("Z", "+00:00"))
        vint = {L: vintage(nc[ym][name], (close - dt.timedelta(days=L)).date()) for L in LEADS}
        for L in LEADS:
            if len(hist[L]) < 12 or vint[L] is None:
                continue
            s_ = math.sqrt(stats.fmean(e * e for e in hist[L]))
            sig_used.setdefault(L, []).append(s_)
            t = close - dt.timedelta(days=L)
            for m in ms:
                q = quote_at(cs.get(m["ticker"]) or [], int(t.timestamp()))
                if q is None:
                    continue
                k = float(m["floor"])
                p = 1 - phi((k + 0.05 - vint[L]) / s_)
                obs.append({"event": ev, "ticker": m["ticker"], "lead": L, "strike": k, "nowcast": vint[L], "p": p,
                            "bid": q[1], "ask": q[2], "yes": m["result"] == "yes", "value": actual, "close": m["close_time"][:10]})
        if actual is not None:
            for L in LEADS:
                if vint[L] is not None:
                    hist[L].append(actual - vint[L])
    sig = {L: (round(stats.fmean(v), 3) if v else None, len(hist[L])) for L, v in ((L, sig_used.get(L)) for L in LEADS)}
    D.log(f"{series}: {len(order)} events; mean sigma used by lead: {sig}")
    return sig, obs


def summarize(obs):
    out = {"brier": {}, "trades": {}}
    for L in LEADS:
        o = [x for x in obs if x["lead"] == L and 0.02 <= (x["bid"] + x["ask"]) / 2 <= 0.98]
        if not o:
            continue
        bm = stats.fmean(((x["bid"] + x["ask"]) / 2 - x["yes"]) ** 2 for x in o)
        bp = stats.fmean((x["p"] - x["yes"]) ** 2 for x in o)
        out["brier"][L] = {"n": len(o), "events": len({x["event"] for x in o}), "market": round(bm, 4), "nowcast": round(bp, 4)}
        for e in EDGES:
            tr = []
            for x in obs:
                if x["lead"] != L:
                    continue
                a, b = x["ask"], x["bid"]
                if x["p"] - a - fee(a) > e and a < 1:
                    tr.append((x, a + fee(a), 1.0 if x["yes"] else 0.0, "YES"))
                elif (1 - x["p"]) - (1 - b) - fee(1 - b) > e and b > 0:
                    c = 1 - b
                    tr.append((x, c + fee(c), 0.0 if x["yes"] else 1.0, "NO"))
            if not tr:
                continue
            cost = sum(t[1] for t in tr)
            pnl = sum(t[2] - t[1] for t in tr)
            by_ev = {}
            for t in tr:
                by_ev.setdefault(t[0]["event"], []).append(t[2] - t[1])
            evp = [sum(v) for v in by_ev.values()]
            tstat = stats.fmean(evp) / (stats.stdev(evp) / math.sqrt(len(evp))) if len(evp) > 2 and stats.stdev(evp) > 0 else 0
            mid = sorted({t[0]["close"] for t in tr})[len({t[0]["close"] for t in tr}) // 2]
            h1 = sum(t[2] - t[1] for t in tr if t[0]["close"] < mid)
            h2 = sum(t[2] - t[1] for t in tr if t[0]["close"] >= mid)
            out["trades"][f"{L}|{e}"] = {"lead": L, "edge": e, "n": len(tr), "events": len(evp), "win": round(stats.fmean(t[2] for t in tr), 3),
                                         "roi": round(pnl / cost, 4), "pnl": round(pnl, 2), "t": round(tstat, 2),
                                         "half1": round(h1, 2), "half2": round(h2, 2),
                                         "yes_share": round(sum(t[3] == "YES" for t in tr) / len(tr), 2)}
    return out


def main():
    rep = {}
    for s in SERIES:
        sig, obs = run(s)
        summ = summarize(obs)
        rep[s] = {"sigma": {str(k): v for k, v in sig.items()}, **summ}
        print(f"\n===== {s}: {len(obs)} market-lead observations")
        for L, b in summ["brier"].items():
            print(f"  lead {L}d: Brier market {b['market']} vs nowcast {b['nowcast']} on {b['n']} quotes / {b['events']} events")
        for k, t in summ["trades"].items():
            print(f"  lead {t['lead']}d edge {t['edge']}: {t['n']} trades / {t['events']} events, win {t['win']}, "
                  f"{t['roi']:+.1%}/$, ${t['pnl']:+.2f}, t {t['t']}, halves {t['half1']:+.2f}/{t['half2']:+.2f}, YES {t['yes_share']}")
    C.DATA_DIR.mkdir(parents=True, exist_ok=True)
    (C.DATA_DIR / "cpi_test.json").write_text(json.dumps(rep, indent=1, default=str))


if __name__ == "__main__":
    main()
