import datetime as dt
import json

import pytest

from kalshi_analyzer import __main__ as app, analysis, config as C, kalshi, settle, strategy
from kalshi_analyzer.explain import explain
from kalshi_analyzer.model import bracket_probability, taker_fee

NOW = dt.datetime(2026, 11, 7, 13, 0, tzinfo=dt.timezone.utc)  # 8am New York


def test_target_date():
    assert kalshi.target_date_from_event("KXHIGHNY-26NOV08") == dt.date(2026, 11, 8)


def test_probabilities_sum_to_one():
    brackets = [("less", None, 50)] + [("between", a, a + 1) for a in range(50, 60, 2)] + [("greater", 59, None)]
    total = sum(bracket_probability(t, f, c, 55.3, 2.5) for t, f, c in brackets)
    assert total == pytest.approx(1.0, abs=1e-9)


def test_fee_rounds_up():
    assert taker_fee(20, 0.50, 0.07) == 0.35
    assert taker_fee(1, 0.50, 0.07) == 0.02


def test_price_fields():
    m = {"ticker": "X", "event_ticker": "KXHIGHNY-26NOV08", "strike_type": "between", "floor_strike": 55,
         "cap_strike": 56, "yes_bid_dollars": "0.2000", "yes_ask": 25, "no_bid_dollars": "0.7500", "no_ask_dollars": "0.8000"}
    n = kalshi.normalize(m, "KXHIGHNY")
    assert (n["yes_bid"], n["yes_ask"], n["no_ask"]) == (0.2, 0.25, 0.8)
    assert kalshi.normalize(dict(m, volume_fp="1234.00"), "KXHIGHNY")["volume"] == 1234.0


def mk(ticker, st, floor, cap, yb, ya, day="2026-11-08"):
    d = dt.date.fromisoformat(day)
    return {"ticker": ticker, "event_ticker": f"KXHIGHNY-{d:%y}{d.strftime('%b').upper()}{d:%d}", "series": "KXHIGHNY",
            "target_date": day, "strike_type": st, "floor": floor, "cap": cap, "yes_bid": yb, "yes_ask": ya,
            "no_bid": round(1 - ya, 2), "no_ask": round(1 - yb, 2), "volume": 500, "status": "open",
            "result": "", "expiration_value": "", "close_time": None}


def test_strategy_buys_underpriced_yes():
    m = mk("T55", "between", 55, 56, 0.10, 0.12)  # forecast 55.5 -> model ~30%
    snap, cand = strategy.evaluate(m, 55.5, NOW)
    assert cand and cand["side"] == "yes" and cand["edge"] >= C.MIN_EDGE
    assert snap["model_p"] > 0.25


def test_strategy_skips_fair_price():
    m = mk("T55", "between", 55, 56, 0.28, 0.30)
    _, cand = strategy.evaluate(m, 55.5, NOW)
    assert cand is None


def test_strategy_skips_wide_spread_and_late():
    _, cand = strategy.evaluate(mk("T", "between", 55, 56, 0.01, 0.15), 55.5, NOW)
    assert cand is None
    late = dt.datetime(2026, 11, 8, 18, 0, tzinfo=dt.timezone.utc)  # 1pm NY on target day
    _, cand = strategy.evaluate(mk("T", "between", 55, 56, 0.10, 0.12), 55.5, late)
    assert cand is None


def test_explain_close_call():
    t = {"side": "yes", "bracket": "55-56F", "model_p": "0.3", "price": "0.12", "won": "0", "forecast_high": "55.5",
         "sigma": "2.5", "actual_high": "57", "result": "no", "strike_type": "between", "floor": "55", "cap": "56"}
    cause, why = explain(t)
    assert cause == "close_call" and "Missed by 1F" in why


def test_full_run_offline(tmp_path, monkeypatch):
    for name, val in {"DATA_DIR": tmp_path / "data", "SNAPSHOT_DIR": tmp_path / "data/snapshots",
                      "TRADES_CSV": tmp_path / "data/trades.csv", "FORECASTS_CSV": tmp_path / "data/forecasts.csv",
                      "DASHBOARD_DATA": tmp_path / "dash", "REPORTS_DIR": tmp_path / "reports"}.items():
        monkeypatch.setattr(C, name, val)
    markets = [mk("NY-B53", "between", 53, 54, 0.30, 0.32), mk("NY-B55", "between", 55, 56, 0.10, 0.12),
               mk("NY-B57", "between", 57, 58, 0.30, 0.32), mk("NY-G58", "greater", 58, None, 0.05, 0.07)]
    fetch_m = lambda s: markets if s == "KXHIGHNY" else []
    fetch_h = lambda lat, lon: {"2026-11-08": 55.5}
    app.run(now=NOW, fetch_markets=fetch_m, fetch_highs=fetch_h, do_settle=False)
    trades = app.ledger.read(C.TRADES_CSV)
    assert any(t["ticker"] == "NY-B55" and t["side"] == "yes" for t in trades)
    assert len(trades) <= C.MAX_POSITIONS_PER_EVENT

    # Next day: market settles; actual high 56 -> 55-56 YES wins.
    def fake_event(event, series):
        out = []
        for m in markets:
            m = dict(m, status="finalized", expiration_value="56")
            m["result"] = "yes" if m["ticker"] == "NY-B55" else "no"
            out.append(m)
        return out
    monkeypatch.setattr(settle, "event_markets", fake_event)
    later = NOW + dt.timedelta(days=1, hours=12)
    app.run(now=later, fetch_markets=lambda s: [], fetch_highs=fetch_h, do_settle=True)
    trades = app.ledger.read(C.TRADES_CSV)
    t = next(t for t in trades if t["ticker"] == "NY-B55")
    assert t["status"] == "settled" and t["won"] == "1" and float(t["pnl"]) > 0
    assert t["cause"] == "forecast_right"
    summary = json.loads((C.DASHBOARD_DATA / "summary.json").read_text())
    assert summary["totals"]["n"] == len(trades)
    assert summary["forecast_accuracy"][0]["bias"] == 0.5
    assert list((tmp_path / "reports").glob("*.md"))
