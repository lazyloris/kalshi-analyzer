"""python -m kalshi_analyzer [run|report|sample]"""
import argparse
import datetime as dt
import json
import sys
from zoneinfo import ZoneInfo

from . import analysis, config as C, kalshi, ledger, nws, report, settle, strategy


def log(msg):
    print(msg, flush=True)


def run(now=None, fetch_markets=kalshi.open_markets, fetch_highs=nws.daily_highs, do_settle=True):
    now = now or dt.datetime.now(dt.timezone.utc)
    trades = ledger.read(C.TRADES_CSV)
    forecasts_all = ledger.read(C.FORECASTS_CSV)
    actuals = ledger.read(C.DATA_DIR / "actuals.csv")
    traded = {t["ticker"] for t in trades}
    per_event = {}
    for t in trades:
        per_event[t["event_ticker"]] = per_event.get(t["event_ticker"], 0) + 1

    snaps, new_fc, candidates, today_by_series = [], [], [], {}
    for series, city in C.CITIES.items():
        today_by_series[series] = now.astimezone(ZoneInfo(city["tz"])).date().isoformat()
        try:
            highs = fetch_highs(city["lat"], city["lon"])
        except Exception as e:
            log(f"{series}: forecast failed: {e}")
            highs = {}
        try:
            markets = fetch_markets(series)
        except Exception as e:
            log(f"{series}: markets failed: {e}")
            continue
        seen_days = set()
        for m in markets:
            fh = highs.get(m["target_date"])
            snap, cand = strategy.evaluate(m, fh, now)
            snaps.append(snap)
            if fh is not None and m["target_date"] not in seen_days:
                seen_days.add(m["target_date"])
                _, lead_days = strategy.lead_info(m["target_date"], city["tz"], now)
                new_fc.append({"time": snap["time"], "series": series, "target_date": m["target_date"],
                               "lead_days": lead_days, "forecast_high": fh})
            if cand:
                candidates.append(cand)
        log(f"{series}: {len(markets)} markets, forecast days {sorted(highs)[:3]}")

    opened = []
    for c in sorted(candidates, key=lambda c: -c["edge"]):
        if c["ticker"] in traded or per_event.get(c["event_ticker"], 0) >= C.MAX_POSITIONS_PER_EVENT:
            continue
        c["trade_id"] = f"{c['ticker']}-{c['side']}"
        traded.add(c["ticker"])
        per_event[c["event_ticker"]] = per_event.get(c["event_ticker"], 0) + 1
        trades.append(c)
        opened.append(c)
        log(f"OPEN {c['city']} {c['target_date']} {c['side'].upper()} {c['bracket']} x{c['contracts']} @ {c['price']:.2f} "
            f"(model {c['model_p']:.0%}, edge {c['edge']*100:.1f}c)")

    forecasts_all += new_fc
    if do_settle:
        settle.settle_trades(trades, actuals, now, log)
        settle.record_actuals(actuals, forecasts_all, today_by_series, log)

    day = now.date().isoformat()
    ledger.append(C.SNAPSHOT_DIR / f"{day}.csv", snaps, ledger.SNAPSHOT_FIELDS)
    ledger.append(C.FORECASTS_CSV, new_fc, ledger.FORECAST_FIELDS)
    ledger.write(C.TRADES_CSV, trades, ledger.TRADE_FIELDS)
    ledger.write(C.DATA_DIR / "actuals.csv", actuals, ledger.ACTUAL_FIELDS)
    write_outputs(trades, forecasts_all, actuals, now)
    log(f"done: {len(snaps)} prices saved, {len(opened)} new trades, {sum(t['status']=='open' for t in trades)} open")


def write_outputs(trades, forecasts, actuals, now):
    summary = analysis.build(trades, forecasts, actuals, now)
    C.DASHBOARD_DATA.mkdir(parents=True, exist_ok=True)
    (C.DASHBOARD_DATA / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    recent = sorted(trades, key=lambda t: t["opened_at"], reverse=True)[:500]
    (C.DASHBOARD_DATA / "trades.json").write_text(json.dumps(recent, indent=1), encoding="utf-8")

    # This week's running scorecard, plus last week's final one if it's missing.
    C.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    today = now.date()
    for d in (today, today - dt.timedelta(days=7)):
        start, end = analysis.week_bounds(d)
        path = C.REPORTS_DIR / f"{start.isocalendar()[0]}-W{start.isocalendar()[1]:02d}.md"
        has_trades = any(start.isoformat() <= t["target_date"] <= end.isoformat() for t in trades)
        if d == today or (has_trades and not path.exists()):
            path.write_text(report.scorecard(trades, forecasts, actuals, now, start, end), encoding="utf-8")


def report_only():
    now = dt.datetime.now(dt.timezone.utc)
    write_outputs(ledger.read(C.TRADES_CSV), ledger.read(C.FORECASTS_CSV),
                  ledger.read(C.DATA_DIR / "actuals.csv"), now)
    log("reports and dashboard data rebuilt")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="kalshi_analyzer")
    ap.add_argument("command", nargs="?", default="run", choices=["run", "report"])
    args = ap.parse_args(argv)
    if args.command == "run":
        run()
    else:
        report_only()


if __name__ == "__main__":
    sys.exit(main())
