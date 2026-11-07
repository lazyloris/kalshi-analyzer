import csv
import datetime as dt
import json

import pytest

from kalshi_analyzer import __main__ as app, config as C, kalshi, ledger, nws, settle, strategy
from kalshi_analyzer.explain import explain
from kalshi_analyzer.model import bracket_probability, lognormal_probability, taker_fee

NOW = dt.datetime(2026, 11, 7, 13, 0, tzinfo=dt.timezone.utc)  # 8am New York


@pytest.fixture
def tmp_repo(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "ROOT", tmp_path)
    monkeypatch.setattr(C, "DATA_DIR", tmp_path / "data")
    monkeypatch.setattr(C, "DASHBOARD_DATA", tmp_path / "dash")
    monkeypatch.setattr(C, "REPORTS_DIR", tmp_path / "reports")
    return tmp_path


def test_target_date():
    assert kalshi.target_date_from_event("KXHIGHNY-26NOV08") == dt.date(2026, 11, 8)
    assert kalshi.target_date_from_event("KXBTCD-26NOV0717") == dt.date(2026, 11, 7)


def test_probabilities_sum_to_one():
    brackets = [("less", None, 50)] + [("between", a, a + 1) for a in range(50, 60, 2)] + [("greater", 59, None)]
    assert sum(bracket_probability(t, f, c, 55.3, 2.5) for t, f, c in brackets) == pytest.approx(1.0)


def test_lognormal():
    assert lognormal_probability("greater", 100, None, 100, 0.5, 24) == pytest.approx(0.5, abs=0.01)
    assert lognormal_probability("greater", 110, None, 100, 0.5, 24) < 0.05
    up = lognormal_probability("greater", 102, None, 100, 0.5, 24)
    assert up + lognormal_probability("less", None, 102, 100, 0.5, 24) == pytest.approx(1.0)


def test_fee_rounds_up():
    assert taker_fee(20, 0.50, 0.07) == 0.35
    assert taker_fee(1, 0.50, 0.07) == 0.02


def test_price_fields():
    m = {"ticker": "X", "event_ticker": "KXHIGHNY-26NOV08", "strike_type": "between", "floor_strike": 55,
         "cap_strike": 56, "yes_bid_dollars": "0.2000", "yes_ask": 25, "no_bid_dollars": "0.7500", "no_ask_dollars": "0.8000"}
    n = kalshi.normalize(m, "KXHIGHNY")
    assert (n["yes_bid"], n["yes_ask"], n["no_ask"]) == (0.2, 0.25, 0.8)
    assert kalshi.normalize(dict(m, volume_fp="1234.00"), "KXHIGHNY")["volume"] == 1234.0


def test_nws_low_belongs_to_next_morning(monkeypatch):
    periods = [
        {"isDaytime": True, "temperature": 60, "temperatureUnit": "F", "startTime": "2026-11-07T06:00:00-05:00"},
        {"isDaytime": False, "temperature": 45, "temperatureUnit": "F", "startTime": "2026-11-07T18:00:00-05:00"},
        {"isDaytime": False, "temperature": 47, "temperatureUnit": "F", "startTime": "2026-11-07T01:00:00-05:00"},
    ]
    monkeypatch.setattr(nws, "get_json", lambda url, *a, **k: {"properties": {"forecast": "x", "periods": periods}})
    ex = nws.daily_extremes(1, 2)
    assert ex["high"] == {"2026-11-07": 60}
    assert ex["low"] == {"2026-11-08": 45, "2026-11-07": 47}


def mk(ticker, st, floor, cap, yb, ya, day="2026-11-08", series="KXHIGHNY", close=None, event=None):
    d = dt.date.fromisoformat(day)
    return {"ticker": ticker, "event_ticker": event or f"{series}-{d:%y}{d.strftime('%b').upper()}{d:%d}", "series": series,
            "target_date": day, "strike_type": st, "floor": floor, "cap": cap, "yes_bid": yb, "yes_ask": ya,
            "no_bid": round(1 - ya, 2), "no_ask": round(1 - yb, 2), "volume": 500, "status": "open",
            "result": "", "expiration_value": "", "close_time": close, "yes_sub_title": ""}


def test_weather_buys_underpriced_yes():
    snap, cand = strategy.evaluate("weather_high", mk("T55", "between", 55, 56, 0.10, 0.12), {"forecasts": {"2026-11-08": 55.5}}, NOW)
    assert cand and cand["side"] == "yes" and cand["edge"] >= 0.08 and cand["book"] == "weather_high"
    _, cand = strategy.evaluate("weather_high", mk("T55", "between", 55, 56, 0.28, 0.30), {"forecasts": {"2026-11-08": 55.5}}, NOW)
    assert cand is None


def test_weather_skips_wide_spread_and_late():
    ctx = {"forecasts": {"2026-11-08": 55.5}}
    assert strategy.evaluate("weather_high", mk("T", "between", 55, 56, 0.01, 0.15), ctx, NOW)[1] is None
    late = dt.datetime(2026, 11, 8, 18, 0, tzinfo=dt.timezone.utc)
    assert strategy.evaluate("weather_high", mk("T", "between", 55, 56, 0.10, 0.12), ctx, late)[1] is None


def test_low_book_stops_before_sunrise():
    m = mk("L", "between", 40, 41, 0.10, 0.12, series="KXLOWTNYC")
    ctx = {"forecasts": {"2026-11-08": 40.5}}
    assert strategy.evaluate("weather_low", m, ctx, NOW)[1] is not None          # 8am the day before
    late = dt.datetime(2026, 11, 8, 7, 0, tzinfo=dt.timezone.utc)                 # 2am NY on the day
    assert strategy.evaluate("weather_low", m, ctx, late)[1] is None


def test_crypto_buys_cheap_near_money():
    m = mk("B", "greater", 75000, None, 0.20, 0.22, day="2026-11-07", series="KXBTCD",
           close="2026-11-07T22:00:00Z", event="KXBTCD-26NOV0717")
    snap, cand = strategy.evaluate("bitcoin", m, {"spot": 75500, "vol": 0.5}, NOW)
    assert snap["model_p"] > 0.6 and cand["side"] == "yes" and cand["city"] == "Bitcoin"
    late = dt.datetime(2026, 11, 7, 21, 0, tzinfo=dt.timezone.utc)
    assert strategy.evaluate("bitcoin", m, {"spot": 75500, "vol": 0.5}, late)[1] is None


def test_fade_buys_no_on_longshot():
    m = mk("S", "custom", None, None, 0.04, 0.06, series="KXSPOTIFYARTIST", close="2026-11-08T04:00:00Z")
    _, cand = strategy.evaluate("trending", m, {}, NOW)
    assert cand["side"] == "no" and cand["price"] == 0.96
    assert strategy.evaluate("trending", mk("S", "custom", None, None, 0.30, 0.32, series="KXSPOTIFYARTIST",
                                            close="2026-11-08T04:00:00Z"), {}, NOW)[1] is None


def test_explain_close_call():
    t = {"side": "yes", "bracket": "55-56F", "model_p": "0.3", "price": "0.12", "won": "0", "forecast": "55.5", "unit": "F",
         "sigma": "2.5", "actual": "57", "result": "no", "strike_type": "between", "floor": "55", "cap": "56"}
    cause, why = explain(t)
    assert cause == "close_call" and "Missed by 1F" in why


def test_actual_from_above_ladder():
    ms = [{"strike_type": "greater", "floor": k, "cap": None, "result": "yes" if k < 75600 else "no", "expiration_value": ""}
          for k in (75000, 75500, 76000)]
    assert settle.actual_from_event(ms) == (75750, True)


class FakeFetcher(app.Fetcher):
    def __init__(self, markets):
        super().__init__(markets=lambda s: markets.get(s, []), extremes=lambda la, lo: {"high": {"2026-11-08": 55.5}, "low": {}},
                         spot=lambda p: 75500.0, vol=lambda p: 0.5)


def test_full_run_offline(tmp_repo, monkeypatch):
    hi = [mk("NY-B53", "between", 53, 54, 0.30, 0.32), mk("NY-B55", "between", 55, 56, 0.10, 0.12),
          mk("NY-B57", "between", 57, 58, 0.30, 0.32), mk("NY-G58", "greater", 58, None, 0.05, 0.07)]
    btc = [mk("BTC-75000", "greater", 75000, None, 0.20, 0.22, day="2026-11-07", series="KXBTCD",
              close="2026-11-07T22:00:00Z", event="KXBTCD-26NOV0717"),
           mk("BTC-HOURLY", "greater", 75000, None, 0.20, 0.22, day="2026-11-07", series="KXBTCD",
              close="2026-11-07T15:00:00Z", event="KXBTCD-26NOV0710")]
    app.run(now=NOW, fetcher=FakeFetcher({"KXHIGHNY": hi, "KXBTCD": btc}), do_settle=False)
    t_hi = ledger.read(C.paths("weather_high")["trades"])
    t_btc = ledger.read(C.paths("bitcoin")["trades"])
    assert any(t["ticker"] == "NY-B55" and t["side"] == "yes" for t in t_hi) and len(t_hi) <= 2
    assert [t["ticker"] for t in t_btc] == ["BTC-75000"]  # hourly 10am contract filtered out
    idx = json.loads((C.DASHBOARD_DATA / "books.json").read_text())
    assert [b["id"] for b in idx["books"]] == list(C.BOOKS)
    assert all(b["bankroll"] == 1000 for b in idx["books"])

    def fake_event(event, series):
        src = hi if series == "KXHIGHNY" else btc
        out = []
        for m in src:
            m = dict(m, status="finalized", expiration_value="56" if series == "KXHIGHNY" else "75800")
            m["result"] = ("yes" if m["ticker"] == "NY-B55" else "no") if series == "KXHIGHNY" else "yes"
            out.append(m)
        return out
    monkeypatch.setattr(settle, "event_markets", fake_event)
    app.run(now=NOW + dt.timedelta(days=1, hours=12), fetcher=FakeFetcher({}), do_settle=True)
    t = next(t for t in ledger.read(C.paths("weather_high")["trades"]) if t["ticker"] == "NY-B55")
    assert t["status"] == "settled" and t["won"] == "1" and float(t["pnl"]) > 0 and t["cause"] == "forecast_right"
    b = ledger.read(C.paths("bitcoin")["trades"])[0]
    assert b["won"] == "1" and "Price at entry $75,500.00" in b["why"]
    s = json.loads((C.paths("weather_high")["dash"] / "summary.json").read_text())
    assert s["forecast_accuracy"][0]["bias"] == 0.5
    assert list(C.paths("weather_high")["reports"].glob("*.md"))

    app.reset("bitcoin", now=NOW + dt.timedelta(days=2))
    assert not C.paths("bitcoin")["trades"].exists()
    assert list((C.paths("bitcoin")["dir"] / "archive").glob("trades-*.csv"))
    idx = json.loads((C.DASHBOARD_DATA / "books.json").read_text())
    assert next(b for b in idx["books"] if b["id"] == "bitcoin")["bankroll"] == 1000


def test_migrates_weather_v1_files(tmp_repo):
    (C.DATA_DIR / "snapshots").mkdir(parents=True)
    with (C.DATA_DIR / "trades.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["trade_id", "status", "forecast_high", "distance_f", "event_ticker", "ticker", "opened_at", "target_date"])
        w.writerow(["x", "open", "51.0", "0.5", "E", "T", "2026-11-07T04:28", "2026-11-07"])
    app.migrate()
    rows = ledger.read(C.paths("weather_high")["trades"])
    assert rows[0]["forecast"] == "51.0" and rows[0]["distance"] == "0.5"
    assert not (C.DATA_DIR / "trades.csv").exists()
