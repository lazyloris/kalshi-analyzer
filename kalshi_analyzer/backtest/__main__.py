"""python -m kalshi_analyzer.backtest [fetch|run|all|scan] [--days 240]

fetch  download/refresh historical data into data/backtest_cache
run    replay every strategy, write dashboard/data/backtest.json and reports/backtest.md
all    both (default)
scan   market scanner across all Kalshi categories (see scanner.py)
assets-fetch  download Ethereum/gold/oil/S&P/... ladders (see assets.py); `run` includes them
"""
import argparse
import time
import datetime as dt
import json
import math

from .. import config as C
from . import data as D
from . import engine as E
from . import signals as S
from . import bayes as B
from . import fattail as F

OUT_JSON = C.DASHBOARD_DATA / "backtest.json"
OUT_MD = C.ROOT / "reports" / "backtest.md"
WEATHER_BOOKS = ("weather_high", "weather_low")


WHY_IDS = {"m_rolling", "v2", "c_v1", "c_vol50", "s_tod", "s_combo_all", "s_spike_fade", "late_fav_80_90", "b_bucket95"}
OOS_CUT = "2026-03-13"  # strategies were chosen on data from here on; earlier days are a fresh test


def fetch(days, crypto_days=None, weather_days=None, budget_min=150):
    end = dt.date.today()
    start = end - dt.timedelta(days=days)
    crypto_start = end - dt.timedelta(days=crypto_days or days)
    weather_start = end - dt.timedelta(days=weather_days or days)  # Kalshi prices only; NBM stays at `days`
    deadline = time.time() + budget_min * 60
    for code in C.STATIONS:
        D.log(f"NBM forecasts {code}")
        D.nbm_forecasts(code, start - dt.timedelta(days=2), end)
    for b in WEATHER_BOOKS:
        for series in C.BOOKS[b]["series"]:
            D.kalshi_series(series, weather_start, deadline=deadline)
    try:
        fetch_bitcoin(crypto_start, end)
    except Exception as e:  # weather results still get written
        D.log(f"Bitcoin download failed: {e}")


def fetch_bitcoin(start, end):
    D.log("Coinbase BTC-USD hourly")
    prices = D.coinbase_hourly("BTC-USD", start - dt.timedelta(days=35), end)
    hours = sorted(prices)

    def near_spot(m):  # only strikes within 4% of the price at 9am ET get candles
        k = E._f(m["floor"]) or E._f(m["cap"])
        ts = D._ts(m["close_time"]) - 8 * 3600
        spot = E._price_at(prices, hours, ts)
        return k is not None and spot is not None and abs(k / spot - 1) <= 0.04

    D.kalshi_events("KXBTCD", D.btc_event_tickers(start, end - dt.timedelta(days=1)), keep=near_spot)
    try:
        D.log("Deribit DVOL BTC (options-implied volatility)")
        D.deribit_dvol("BTC", start - dt.timedelta(days=2), end)
    except Exception as e:
        D.log(f"DVOL download failed: {e}")


def load():
    kalshi = {s: D._load(f"kalshi_{s}", None) for b in WEATHER_BOOKS for s in C.BOOKS[b]["series"]}
    nbm = {c: D._load(f"nbm_{c}", {}) for c in C.STATIONS}
    btc = D._load("kalshi_KXBTCD", None)
    prices = {int(k): v for k, v in D._load("coinbase_close_BTC-USD", {}).items()}
    return kalshi, nbm, btc, prices


def _quarter(d):
    return f"{d[:4]}-Q{(int(d[5:7]) - 1) // 3 + 1}"


def _band(edges, v):
    for lo, hi in zip(edges, edges[1:]):
        if lo <= v < hi:
            return f"{lo:.2f}-{hi:.2f}"
    return "other"


def why(trades):
    """Where the money was made or lost: by quarter, price paid, side, and model-vs-market gap."""
    for t in trades:
        t["_q"] = _quarter(t["date"])
        t["_price"] = _band((0, .1, .3, .5, .7, .9, 1.01), t["price"])
        gap = abs(t["p_model"] - t["p_market"]) if t.get("p_model") is not None and t.get("p_market") is not None else None
        t["_gap"] = "no model" if gap is None else _band((0, .05, .10, .20, .35, 1.01), gap)
    out = {k: E.breakdown(trades, f"_{k}") for k in ("q", "price", "gap")}
    for t in trades:
        for k in ("_q", "_price", "_gap"):
            t.pop(k, None)
    return out


def vol_check(evs):
    """Per quarter: how big the moves really were vs the 30-day volatility we assumed.
    ratio ~1 = vol estimate was right; ~0.5 = the market moved half as much as assumed."""
    g = {}
    for e in evs:
        if e.get("actual") and e.get("spot") and e.get("vol"):
            s = e["vol"] * (max(e["hours"], 0.01) / 8760) ** 0.5
            g.setdefault(_quarter(e["date"]), []).append((math.log(e["actual"] / e["spot"]) / s) ** 2)
    return {q: {"n": len(v), "ratio": round((sum(v) / len(v)) ** 0.5, 3)} for q, v in sorted(g.items())}


TRADES = {}  # book -> {sid: trades}, for the combined strategies


def _tstat(ts):
    if len(ts) < 2:
        return None
    rets = [t["pnl"] / t["cost"] for t in ts]
    m = sum(rets) / len(rets)
    sd = (sum((r - m) ** 2 for r in rets) / (len(rets) - 1)) ** 0.5
    return m / sd * len(rets) ** 0.5 if sd else None


def rolling_pick(by_sid, lookback_days=180, min_trades=30, lag_days=2):
    """Each quarter, trade only the strategy with the best t-stat over the previous `lookback_days`
    (trades that had settled, so nothing from the future). Sits out if none made money."""
    allt = [t for ts in by_sid.values() for t in ts]
    if not allt:
        return [], []
    qs = sorted({_quarter(t["date"]) for t in allt})
    out, picks = [], []
    for q in qs:
        y, n = int(q[:4]), int(q[-1])
        start = dt.date(y, 3 * n - 2, 1)
        lo = (start - dt.timedelta(days=lookback_days)).isoformat()
        hi = (start - dt.timedelta(days=lag_days)).isoformat()
        best, best_t = None, 0.0
        for sid, ts in by_sid.items():
            past = [t for t in ts if lo <= t["date"] < hi]
            tt = _tstat(past)
            if len(past) >= min_trades and sum(t["pnl"] for t in past) > 0 and tt and tt > best_t:
                best, best_t = sid, tt
        picks.append({"quarter": q, "pick": best, "t": round(best_t, 2) if best else None})
        if best:
            out += [t for t in by_sid[best] if _quarter(t["date"]) == q]
    return out, picks


def consensus(by_sid, k=3):
    """Trades that k+ different strategies made (same entry, market and side)."""
    seen = {}
    for sid, ts in by_sid.items():
        for t in ts:
            key = (t["ts"], t["ticker"], t["side"])
            seen.setdefault(key, [t, set()])[1].add(sid)
    return sorted((t for t, sids in seen.values() if len(sids) >= k), key=lambda t: t["ts"])


def add_combined(book, r):
    by_sid = {sid: ts for sid, ts in TRADES.get(book, {}).items() if not sid.startswith("m_")}
    if not by_sid:
        return
    trades, picks = rolling_pick(by_sid)
    r["strategies"].append(_strategy_result("m_rolling", "Combined: rolling best (past 6 months)",
                                            "Each quarter, trade the strategy that did best over the previous 6 months",
                                            book, trades))
    r["rolling_picks"] = picks
    for k in (3, 5):
        r["strategies"].append(_strategy_result(f"m_consensus{k}", f"Combined: {k}+ strategies agree",
                                                f"Only trades that at least {k} strategies made", book, consensus(by_sid, k)))


def _strategy_result(sid, name, desc, book, trades):
    TRADES.setdefault(book, {})[sid] = trades
    by_entry = E.breakdown(trades, "entry")
    old = [t for t in trades if t["date"] < OOS_CUT]
    staked = sum(t["cost"] for t in old)
    older = {"trades": len(old), "pnl": round(sum(t["pnl"] for t in old), 2),
             "roi": round(sum(t["pnl"] for t in old) / staked, 4) if staked else None}
    return {"id": sid, "name": name, "desc": desc, "book": book, **E.metrics(trades), "older": older,
            "by_entry": by_entry, "by_city": E.breakdown(trades, "city"), "by_side": E.breakdown(trades, "side"),
            "why": why(trades),
            "curve": E.curve(trades)}


def run(now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    kalshi, nbm, btc, prices = load()
    result = {"generated_at": now.isoformat(timespec="minutes"), "stake": E.STAKE, "books": {}}
    for b in WEATHER_BOOKS:
        evs = E.calibrate(E.weather_events(b, kalshi, nbm))
        if not evs:
            continue
        S.enrich(evs)
        strategies = [_strategy_result(sid, name, desc, b, E.simulate(evs, pick))
                      for sid, name, desc, pick in E.weather_strategies() + S.weather_strategies()
                      + B.strategies(lambda e, m: E.p_weather(e, m), "forecast")]
        sw = E.weather_sweeps()
        result["books"][b] = {
            "name": C.BOOKS[b]["name"], "events": len({e["event"] for e in evs}),
            "first": evs[0]["date"], "last": evs[-1]["date"],
            "strategies": strategies,
            "sweeps": {
                "sigma": [{"mult": k, **E.metrics(E.simulate(evs, p))} for k, p in sw["sigma"]],
                "blend": [{"blend": w, "min_edge": edge, **E.metrics(E.simulate(evs, p))} for (w, edge), p in sw["blend"]],
            },
            "forecast_errors": E.forecast_errors(evs),
            "market_calibration": E.market_calibration(evs),
        }
    if btc and prices:
        evs = E.crypto_events("KXBTCD", btc, prices)
        iv = {int(k): v for k, v in D._load("dvol_BTC", {}).items()}
        has_iv = E.attach_ivol(evs, iv) if evs and iv else 0
        S.enrich(evs, prices, tod=True)
        has_emp = F.attach(evs, prices) if evs else 0
        if evs:
            result["books"]["bitcoin"] = {
                "name": C.BOOKS["bitcoin"]["name"], "events": len({e["event"] for e in evs}),
                "first": evs[0]["date"], "last": evs[-1]["date"],
                "strategies": [_strategy_result(sid, name, desc, "bitcoin", E.simulate(evs, pick))
                               for sid, name, desc, pick in E.crypto_strategies() + (E.iv_strategies() if has_iv else [])
                               + S.crypto_strategies()
                               + B.strategies(lambda e, m: E.p_crypto(e, m, 1.0), "full vol")
                               + (F.strategies() if has_emp else [])],
                "sweeps": {"vol": [{"mult": k, **E.metrics(E.simulate(evs, p))} for k, p in E.crypto_sweeps()["vol"]],
                           **({"options vol": [{"mult": k, **E.metrics(E.simulate(evs, p))} for k, p in E.iv_sweeps()]}
                              if has_iv else {}),
                           "time-of-day vol": [{"mult": k, **E.metrics(E.simulate(evs, p))} for k, p in S.tod_sweep()],
                           **({"fat-tail": [{"mult": k, **E.metrics(E.simulate(evs, p))} for k, p in F.sweep()]}
                              if has_emp else {})},
                "iv_coverage": round(has_iv / len(evs), 3),
                "vol_check": vol_check(evs),
                "market_calibration": E.market_calibration(evs),
            }
    late = [(f"{b}_late", f"{C.BOOKS[b]['name']}: late entries", E.weather_events(b, kalshi, nbm, E.LATE_ENTRIES))
            for b in WEATHER_BOOKS]
    if btc and prices:
        late.append(("bitcoin_late", "Bitcoin: last 1-3 hours", E.crypto_events("KXBTCD", btc, prices, E.CRYPTO_LATE)))
    for bid, name, evs in late:
        if evs:
            result["books"][bid] = {
                "name": name, "events": len({e["event"] for e in evs}), "first": evs[0]["date"], "last": evs[-1]["date"],
                "strategies": [_strategy_result(sid, n, desc, bid, E.simulate(evs, pick))
                               for sid, n, desc, pick in E.late_strategies() + B.strategies()
                               + S.exit_strategies(E.market_favorite(0.80, 0.90), "Late fav 80-90c")],
                "market_calibration": E.market_calibration(evs),
            }
    try:
        from . import assets
        result["books"].update(assets.books(_strategy_result))
    except Exception as e:  # never lose the weather/Bitcoin results over a new market
        D.log(f"asset backtest failed: {e}")
    for b, r in result["books"].items():
        add_combined(b, r)
        r["verdict"] = verdict(r["strategies"])
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=1))
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(markdown(result))
    D.log(f"wrote {OUT_JSON} and {OUT_MD}")
    return result


def verdict(strats, min_trades=50):
    """Most reliable strategy (highest t-stat, so small lucky samples don't win) that made money in
    BOTH halves of the period with enough trades, if any."""
    ok = [s for s in strats if s["trades"] >= min_trades and s["first_half"] > 0 and s["second_half"] > 0]
    if not ok:
        best = max(strats, key=lambda s: s["pnl"])
        return {"id": None, "text": f"No strategy made money in both halves with {min_trades}+ trades. "
                                    f"Least bad: {best['name']} ({best['pnl']:+.0f} on {best['trades']} trades)."}
    best = max(ok, key=lambda s: s["t_stat"] or 0)
    return {"id": best["id"], "text": f"{best['name']}: {best['pnl']:+.0f} on {best['trades']} trades "
                                      f"({best['roi'] * 100:+.1f}% per $ staked, t={best['t_stat']}), profitable in both halves."}


def _roi(v):
    return "–" if v is None else f"{v * 100:+.1f}%"


def markdown(r):
    L = [f"# Backtest ({r['generated_at'][:10]})", "",
         f"Flat ${r['stake']:.0f} per trade at the ask plus Kalshi fees, held to settlement. "
         "Prices are real hourly Kalshi quotes. Forecasts are archived NWS-blend (NBM) runs 1-2 days old. "
         "Bias/sigma learned only from earlier days.", ""]
    for b, x in r["books"].items():
        L += [f"## {x['name']}", "", f"{x['events']} events, {x['first']} to {x['last']}.", "",
              f"**Verdict:** {x['verdict']['text']}", "",
              "| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for s in sorted(x["strategies"], key=lambda s: -s["pnl"]):
            pct = lambda v: "–" if v is None else f"{v * 100:.0f}%"
            L.append(f"| {s['name']} | {s['trades']} | {pct(s['win_rate'])} | {s['pnl']:+.2f} | "
                     f"{_roi(s['roi'])} | {s['first_half']:+.0f} | {s['second_half']:+.0f} | "
                     f"{pct(s['avg_claimed'])} | {s['brier_model'] if s['brier_model'] is not None else '–'} | "
                     f"{s['brier_market'] if s['brier_market'] is not None else '–'} |")
        if any(s.get("older", {}).get("trades") for s in x["strategies"]):
            L += ["", f"Before {OOS_CUT} (fresh test: strategies were picked on later data)", "",
                  "| Strategy | Trades | P&L | Return/$ |", "|---|---|---|---|"]
            for s in sorted(x["strategies"], key=lambda s: -(s["older"]["pnl"])):
                o = s["older"]
                L.append(f"| {s['name']} | {o['trades']} | {o['pnl']:+.2f} | {_roi(o['roi'])} |")
        for name, rows in x.get("sweeps", {}).items():
            L += ["", f"Sweep: {name}", "", "| Setting | Trades | P&L | Return/$ |", "|---|---|---|---|"]
            for s in rows:
                setting = s.get("mult", "")
                if "blend" in s:
                    setting = f"blend {s['blend']}, edge {s['min_edge']}"
                L.append(f"| {setting} | {s['trades']} | {s['pnl']:+.2f} | "
                         f"{_roi(s['roi'])} |")
        if x.get("rolling_picks"):
            L += ["", "Rolling best: which strategy it picked each quarter", "", "| Quarter | Picked | Past t |", "|---|---|---|"]
            names = {s["id"]: s["name"] for s in x["strategies"]}
            L += [f"| {p['quarter']} | {names.get(p['pick'], 'sat out') if p['pick'] else 'sat out'} | {p['t'] or '–'} |"
                  for p in x["rolling_picks"]]
        if x.get("vol_check"):
            L += ["", "Volatility check: real moves vs the 30-day volatility assumed (1.0 = right, 0.5 = moved half as much)",
                  "", "| Quarter | Events | Ratio |", "|---|---|---|"]
            L += [f"| {q} | {v['n']} | {v['ratio']} |" for q, v in x["vol_check"].items()]
        picks = [s for s in x["strategies"] if s["id"] in WHY_IDS or s["id"] == x["verdict"].get("id")]
        for s in picks:
            w = s.get("why") or {}
            L += ["", f"Why: {s['name']}", "", "| Split | Group | Trades | P&L | Win % |", "|---|---|---|---|---|"]
            for split, label in (("q", "Quarter"), ("price", "Price paid"), ("gap", "Model vs market gap")):
                for k, v in (w.get(split) or {}).items():
                    L.append(f"| {label} | {k} | {v['trades']} | {v['pnl']:+.0f} | {v['win_rate'] * 100:.0f}% |")
            for k, v in (s.get("by_side") or {}).items():
                L.append(f"| Side | {k} | {v['trades']} | {v['pnl']:+.0f} | {v['win_rate'] * 100:.0f}% |")
        if x.get("forecast_errors"):
            L += ["", "Forecast error (actual minus NBM forecast)", "", "| City | Entry | n | Bias | RMSE |", "|---|---|---|---|---|"]
            L += [f"| {f['city']} | {f['entry']} | {f['n']} | {f['bias']:+.2f} | {f['rmse']} |" for f in x["forecast_errors"]]
        L.append("")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m kalshi_analyzer.backtest")
    ap.add_argument("cmd", nargs="?", default="all", choices=["fetch", "run", "all", "scan", "scan-fetch", "scan-run", "assets-fetch"])
    ap.add_argument("--days", type=int, default=240)
    ap.add_argument("--crypto-days", type=int, default=None,
                    help="fetch/assets-fetch: longer history for Bitcoin/Ethereum only")
    ap.add_argument("--weather-days", type=int, default=None,
                    help="fetch: longer Kalshi weather price history (no forecasts that far back)")
    ap.add_argument("--budget", type=int, default=100, help="assets-fetch: minutes before stopping (resumes next run)")
    ap.add_argument("--top", type=int, default=150, help="scanner: how many of the most-traded series")
    a = ap.parse_args(argv)
    if a.cmd.startswith("scan"):
        from . import scanner
        if a.cmd in ("scan", "scan-fetch"):
            scanner.fetch(top=a.top, days=min(a.days, 60))
        if a.cmd in ("scan", "scan-run"):
            scanner.analyze()
        return
    if a.cmd == "assets-fetch":
        from . import assets
        assets.fetch(a.days, budget_min=a.budget, crypto_days=a.crypto_days)
        return
    if a.cmd in ("fetch", "all"):
        fetch(a.days, a.crypto_days, a.weather_days)
    if a.cmd in ("run", "all"):
        run()


if __name__ == "__main__":
    main()
