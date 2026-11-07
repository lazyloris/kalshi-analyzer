"""python -m kalshi_analyzer [run | report | reset BOOK]"""
import argparse
import datetime as dt
import json
import shutil
import sys
from zoneinfo import ZoneInfo

from . import analysis, config as C, crypto, kalshi, ledger, nws, report, settle, strategy


def log(msg):
    print(msg, flush=True)


def migrate():
    """weather-v1 kept its files at data/*.csv. Move them into data/weather_high/ once."""
    old, new = C.DATA_DIR / "trades.csv", C.paths("weather_high")
    if old.exists() and not new["trades"].exists():
        new["dir"].mkdir(parents=True, exist_ok=True)
        for name in ("trades.csv", "forecasts.csv", "actuals.csv", "snapshots"):
            if (C.DATA_DIR / name).exists():
                shutil.move(str(C.DATA_DIR / name), str(new["dir"] / name))
        for name in ("summary.json", "trades.json"):
            (C.DASHBOARD_DATA / name).unlink(missing_ok=True)
        new["reports"].mkdir(parents=True, exist_ok=True)
        for f in C.REPORTS_DIR.glob("*.md"):
            shutil.move(str(f), str(new["reports"] / f.name))
        log("migrated weather-v1 files into data/weather_high/")


class Fetcher:
    """Caches outside data for one run so books sharing a city or asset don't refetch it."""

    def __init__(self, markets=kalshi.open_markets, extremes=nws.daily_extremes,
                 spot=crypto.spot, vol=crypto.realized_vol):
        self._markets, self._extremes, self._spot, self._vol = markets, extremes, spot, vol
        self.cache = {}

    def _get(self, key, fn, *a):
        if key not in self.cache:
            try:
                self.cache[key] = fn(*a)
            except Exception as e:
                log(f"{key}: failed: {e}")
                self.cache[key] = None
        return self.cache[key]

    def markets(self, series):
        return self._get(("m", series), self._markets, series)

    def extremes(self, stn):
        s = C.STATIONS[stn]
        return self._get(("wx", stn), self._extremes, s["lat"], s["lon"])

    def spot(self, product):
        return self._get(("spot", product), self._spot, product)

    def vol(self, product):
        return self._get(("vol", product), self._vol, product)


def run_book(book_id, f, now, do_settle=True):
    book, R, P = C.BOOKS[book_id], C.rules(book_id), C.paths(book_id)
    trades = ledger.read(P["trades"], {"book": book_id, "unit": book["unit"]})
    forecasts_all = ledger.read(P["forecasts"])
    actuals = ledger.read(P["actuals"])
    traded = {t["ticker"] for t in trades}
    per_event = {}
    for t in trades:
        per_event[t["event_ticker"]] = per_event.get(t["event_ticker"], 0) + 1

    snaps, new_fc, candidates, today_by_series = [], [], [], {}
    for series, key in book["series"].items():
        ctx = {}
        if book["kind"] == "weather":
            stn = C.STATIONS[key]
            today_by_series[series] = now.astimezone(ZoneInfo(stn["tz"])).date().isoformat()
            ex = f.extremes(key) or {}
            ctx["forecasts"] = ex.get(book["extreme"], {})
        elif book["kind"] == "crypto":
            ctx["spot"] = f.spot(book["asset"])
            ctx["vol"] = f.vol(book["asset"]) or book["fallback_vol"]
        markets = f.markets(series)
        if markets is None:
            continue
        if book.get("event_suffix"):
            markets = [m for m in markets if m["event_ticker"].endswith(book["event_suffix"])]
        seen_days = set()
        for m in markets:
            snap, cand = strategy.evaluate(book_id, m, ctx, now)
            snaps.append(snap)
            if book["kind"] == "weather" and snap["forecast"] != "" and m["target_date"] not in seen_days:
                seen_days.add(m["target_date"])
                _, lead_days = strategy.weather_lead(book, m["target_date"], C.STATIONS[key]["tz"], now)
                new_fc.append({"time": snap["time"], "series": series, "target_date": m["target_date"],
                               "lead_days": lead_days, "forecast": ctx["forecasts"][m["target_date"]]})
            if cand:
                candidates.append(cand)
        extra = f", spot {ctx['spot']}, vol {ctx['vol']:.2f}" if book["kind"] == "crypto" and ctx.get("spot") else ""
        log(f"[{book_id}] {series}: {len(markets)} markets{extra}")

    opened = 0
    for c in sorted(candidates, key=lambda c: -c["edge"]):
        if c["ticker"] in traded or per_event.get(c["event_ticker"], 0) >= R["MAX_POSITIONS_PER_EVENT"]:
            continue
        c["trade_id"] = f"{c['ticker']}-{c['side']}"
        traded.add(c["ticker"])
        per_event[c["event_ticker"]] = per_event.get(c["event_ticker"], 0) + 1
        trades.append(c)
        opened += 1
        log(f"[{book_id}] OPEN {c['city']} {c['target_date']} {c['side'].upper()} {c['bracket']} x{c['contracts']} "
            f"@ {c['price']:.2f} (model {c['model_p']:.0%}, edge {c['edge']*100:.1f}c)")

    forecasts_all += new_fc
    if do_settle:
        settle.settle_trades(trades, actuals, now, log)
        if book["kind"] == "weather":
            settle.record_actuals(actuals, forecasts_all, today_by_series, log)

    ledger.append(P["snapshots"] / f"{now.date().isoformat()}.csv", snaps, ledger.SNAPSHOT_FIELDS)
    ledger.append(P["forecasts"], new_fc, ledger.FORECAST_FIELDS)
    ledger.write(P["trades"], trades, ledger.TRADE_FIELDS)
    ledger.write(P["actuals"], actuals, ledger.ACTUAL_FIELDS)
    summary = write_outputs(book_id, trades, forecasts_all, actuals, now)
    log(f"[{book_id}] done: {len(snaps)} prices, {opened} new trades, {summary['open_count']} open, "
        f"bankroll ${summary['bankroll']:.2f}")
    return summary


def write_outputs(book_id, trades, forecasts, actuals, now):
    P = C.paths(book_id)
    summary = analysis.build(book_id, trades, forecasts, actuals, now)
    P["dash"].mkdir(parents=True, exist_ok=True)
    (P["dash"] / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    recent = sorted(trades, key=lambda t: t["opened_at"], reverse=True)[:500]
    (P["dash"] / "trades.json").write_text(json.dumps(recent, indent=1), encoding="utf-8")

    # This week's running scorecard, plus last week's final one if it's missing.
    P["reports"].mkdir(parents=True, exist_ok=True)
    today = now.date()
    for d in (today, today - dt.timedelta(days=7)):
        start, end = analysis.week_bounds(d)
        path = P["reports"] / f"{start.isocalendar()[0]}-W{start.isocalendar()[1]:02d}.md"
        has_trades = any(start.isoformat() <= t["target_date"] <= end.isoformat() for t in trades)
        if d == today or (has_trades and not path.exists()):
            path.write_text(report.scorecard(book_id, trades, forecasts, actuals, now, start, end), encoding="utf-8")
    return summary


def write_index(summaries, now):
    books = [{"id": s["book"], "name": s["name"], "short": s["short"], "bankroll": s["bankroll"],
              "starting_bankroll": s["starting_bankroll"], "settled": s["totals"].get("n", 0),
              "open": s["open_count"], "version": s["strategy_version"],
              "next_results_by": next((u["results_by"] for u in s.get("upcoming", []) if u["results_by"] != "unknown"), "")}
             for s in summaries]
    C.DASHBOARD_DATA.mkdir(parents=True, exist_ok=True)
    (C.DASHBOARD_DATA / "books.json").write_text(
        json.dumps({"generated_at": now.isoformat(timespec="minutes"), "books": books}, indent=1), encoding="utf-8")


def run(now=None, fetcher=None, do_settle=True):
    now = now or dt.datetime.now(dt.timezone.utc)
    migrate()
    f = fetcher or Fetcher()
    summaries = []
    for book_id in C.BOOKS:
        try:
            summaries.append(run_book(book_id, f, now, do_settle))
        except Exception as e:  # one broken book must not stop the others
            log(f"[{book_id}] FAILED: {e!r}")
    write_index(summaries, now)


def report_only(now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    migrate()
    summaries = []
    for book_id in C.BOOKS:
        P = C.paths(book_id)
        summaries.append(write_outputs(book_id, ledger.read(P["trades"], {"book": book_id, "unit": C.BOOKS[book_id]["unit"]}),
                                       ledger.read(P["forecasts"]), ledger.read(P["actuals"]), now))
    write_index(summaries, now)
    log("reports and dashboard data rebuilt")


def reset(book_id, now=None):
    """Archive a book's trades and start it over at its starting bankroll. Price history is kept."""
    if book_id not in C.BOOKS:
        raise SystemExit(f"unknown book {book_id!r}; choose from {', '.join(C.BOOKS)}")
    now = now or dt.datetime.now(dt.timezone.utc)
    P = C.paths(book_id)
    if P["trades"].exists():
        archive = P["dir"] / "archive"
        archive.mkdir(parents=True, exist_ok=True)
        dest = archive / f"trades-{now:%Y%m%dT%H%M}.csv"
        shutil.move(str(P["trades"]), str(dest))
        log(f"[{book_id}] archived trades to {dest.relative_to(C.ROOT)}")
    for f in P["reports"].glob("*.md") if P["reports"].exists() else []:
        f.unlink()
    report_only(now)
    log(f"[{book_id}] reset to ${C.BOOKS[book_id]['bankroll']:.0f}")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="kalshi_analyzer")
    ap.add_argument("command", nargs="?", default="run", choices=["run", "report", "reset"])
    ap.add_argument("book", nargs="?", help="for reset: a book id, or 'all'")
    a = ap.parse_args(argv)
    if a.command == "run":
        run()
    elif a.command == "report":
        report_only()
    else:
        for b in (list(C.BOOKS) if a.book == "all" else [a.book]):
            reset(b)


if __name__ == "__main__":
    sys.exit(main())
