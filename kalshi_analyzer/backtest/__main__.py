"""python -m kalshi_analyzer.backtest [fetch|run|all|scan] [--days 240]

fetch  download/refresh historical data into data/backtest_cache
run    replay every strategy, write dashboard/data/backtest.json and reports/backtest.md
all    both (default)
scan   market scanner across all Kalshi categories (see scanner.py)
assets-fetch  download Ethereum/gold/oil/S&P/... ladders (see assets.py); `run` includes them
"""
import argparse
import datetime as dt
import json

from .. import config as C
from . import data as D
from . import engine as E
from . import signals as S

OUT_JSON = C.DASHBOARD_DATA / "backtest.json"
OUT_MD = C.ROOT / "reports" / "backtest.md"
WEATHER_BOOKS = ("weather_high", "weather_low")


def fetch(days):
    end = dt.date.today()
    start = end - dt.timedelta(days=days)
    for code in C.STATIONS:
        D.log(f"NBM forecasts {code}")
        D.nbm_forecasts(code, start - dt.timedelta(days=2), end)
    for b in WEATHER_BOOKS:
        for series in C.BOOKS[b]["series"]:
            D.kalshi_series(series, start)
    try:
        fetch_bitcoin(start, end)
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


def _strategy_result(sid, name, desc, book, trades):
    by_entry = E.breakdown(trades, "entry")
    return {"id": sid, "name": name, "desc": desc, "book": book, **E.metrics(trades),
            "by_entry": by_entry, "by_city": E.breakdown(trades, "city"), "by_side": E.breakdown(trades, "side"),
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
                      for sid, name, desc, pick in E.weather_strategies() + S.weather_strategies()]
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
        if evs:
            result["books"]["bitcoin"] = {
                "name": C.BOOKS["bitcoin"]["name"], "events": len({e["event"] for e in evs}),
                "first": evs[0]["date"], "last": evs[-1]["date"],
                "strategies": [_strategy_result(sid, name, desc, "bitcoin", E.simulate(evs, pick))
                               for sid, name, desc, pick in E.crypto_strategies() + (E.iv_strategies() if has_iv else [])
                               + S.crypto_strategies()],
                "sweeps": {"vol": [{"mult": k, **E.metrics(E.simulate(evs, p))} for k, p in E.crypto_sweeps()["vol"]],
                           **({"options vol": [{"mult": k, **E.metrics(E.simulate(evs, p))} for k, p in E.iv_sweeps()]}
                              if has_iv else {}),
                           "time-of-day vol": [{"mult": k, **E.metrics(E.simulate(evs, p))} for k, p in S.tod_sweep()]},
                "iv_coverage": round(has_iv / len(evs), 3),
                "market_calibration": E.market_calibration(evs),
            }
    try:
        from . import assets
        result["books"].update(assets.books(_strategy_result))
    except Exception as e:  # never lose the weather/Bitcoin results over a new market
        D.log(f"asset backtest failed: {e}")
    for b, r in result["books"].items():
        r["verdict"] = verdict(r["strategies"])
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=1))
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(markdown(result))
    D.log(f"wrote {OUT_JSON} and {OUT_MD}")
    return result


def verdict(strats, min_trades=30):
    """Best strategy that made money in BOTH halves of the period with enough trades, if any."""
    ok = [s for s in strats if s["trades"] >= min_trades and s["first_half"] > 0 and s["second_half"] > 0]
    if not ok:
        best = max(strats, key=lambda s: s["pnl"])
        return {"id": None, "text": f"No strategy made money in both halves with {min_trades}+ trades. "
                                    f"Least bad: {best['name']} ({best['pnl']:+.0f} on {best['trades']} trades)."}
    best = max(ok, key=lambda s: s["roi"])
    return {"id": best["id"], "text": f"{best['name']}: {best['pnl']:+.0f} on {best['trades']} trades "
                                      f"({best['roi'] * 100:+.1f}% per $ staked), profitable in both halves."}


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
        for name, rows in x.get("sweeps", {}).items():
            L += ["", f"Sweep: {name}", "", "| Setting | Trades | P&L | Return/$ |", "|---|---|---|---|"]
            for s in rows:
                setting = s.get("mult", "")
                if "blend" in s:
                    setting = f"blend {s['blend']}, edge {s['min_edge']}"
                L.append(f"| {setting} | {s['trades']} | {s['pnl']:+.2f} | "
                         f"{_roi(s['roi'])} |")
        if x.get("forecast_errors"):
            L += ["", "Forecast error (actual minus NBM forecast)", "", "| City | Entry | n | Bias | RMSE |", "|---|---|---|---|---|"]
            L += [f"| {f['city']} | {f['entry']} | {f['n']} | {f['bias']:+.2f} | {f['rmse']} |" for f in x["forecast_errors"]]
        L.append("")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m kalshi_analyzer.backtest")
    ap.add_argument("cmd", nargs="?", default="all", choices=["fetch", "run", "all", "scan", "scan-fetch", "scan-run", "assets-fetch"])
    ap.add_argument("--days", type=int, default=240)
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
        assets.fetch(a.days, budget_min=a.budget)
        return
    if a.cmd in ("fetch", "all"):
        fetch(a.days)
    if a.cmd in ("run", "all"):
        run()


if __name__ == "__main__":
    main()
