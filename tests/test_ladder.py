import datetime as dt

from kalshi_analyzer.backtest import engine as E
from kalshi_analyzer.backtest import ladder as L


def _ladder(days=40, strikes=6, seed=2):
    """Daily 'above X' ladders where the market quotes every strike at 80c but 95% of them win:
    favorites are underpriced, so buying YES should score and buying NO should lose."""
    import random
    rnd = random.Random(seed)
    ms, cs = {}, {}
    for d in range(days):
        close = dt.datetime(2026, 1, 1, 21, tzinfo=dt.timezone.utc) + dt.timedelta(days=d)
        ev = f"KXTEST-{d:03d}"
        for k in range(strikes):
            t = f"{ev}-T{k}"
            won = rnd.random() < 0.95
            ms[t] = {"ticker": t, "event_ticker": ev, "strike_type": "greater", "floor": k, "cap": None,
                     "close_time": close.isoformat().replace("+00:00", "Z"), "result": "yes" if won else "no",
                     "value": "1", "source": "live"}
            cs[t] = [[int(close.timestamp()) - h * 3600, 0.79, 0.81, 10.0] for h in range(24, 0, -1)]
    return {"markets": ms, "candles": cs}


def test_ladder_cell_scores_per_event():
    data = _ladder()
    r = L.cell(data, 4, 0.75, 0.88)
    assert r["n"] == 240 and r["events"] == 40 and r["bucket"] == "75-88c"
    assert r["yes"]["roi"] > 0.05 and r["no"]["roi"] < 0  # 95% win at 81c is cheap
    assert r["yes"]["events"] == 40 and r["yes"]["t_event"] > 2
    assert L.cell(data, 4, 0.10, 0.20) is None  # nothing quoted there


def test_ladder_trades_use_quote_at_entry_only():
    data = _ladder(days=3)
    t = L.ladder_trades(data, 4, 0.75, 0.88, "yes")
    close = int(dt.datetime(2026, 1, 1, 21, tzinfo=dt.timezone.utc).timestamp())
    assert t[0]["ts"] == close - 4 * 3600 and t[0]["price"] == 0.81
    # NO is bought at 1 - bid
    assert L.ladder_trades(data, 4, 0.75, 0.88, "no")[0]["price"] == round(1 - 0.79, 4)


def test_event_t_collapses_strikes_of_one_event():
    close = dt.datetime(2026, 1, 1, 21, tzinfo=dt.timezone.utc)
    trades = []
    for d in range(10):
        for k in range(5):  # five strikes per day, all winning or all losing together
            won = d % 3 != 0
            trades.append({"ts": int(close.timestamp()) + d * 86400, "ticker": f"KXTEST-{d}-T{k}", "pnl": 1.0 if won else -8.0,
                           "cost": 8.0, "won": won, "price": 0.8, "p_model": None, "p_market": 0.8, "date": "2026-01-01"})
    m = E.metrics(trades)
    assert m["trades"] == 50 and m["events"] == 10
    assert abs(m["t_stat"]) > abs(m["t_event"])  # per-trade t overstates the evidence


def test_ladder_run_writes_report(tmp_path, monkeypatch):
    from kalshi_analyzer.backtest import data as D
    monkeypatch.setattr(D, "CACHE", tmp_path / "cache")
    monkeypatch.setattr(L, "OUT_JSON", tmp_path / "ladder.json")
    monkeypatch.setattr(L, "OUT_MD", tmp_path / "ladder.md")
    D._save("kalshi_KXBTCD", _ladder())
    r = L.run(dt.datetime(2026, 11, 10, tzinfo=dt.timezone.utc))
    b = r["books"]["Bitcoin 5pm (KXBTCD)"]
    assert b["events"] == 40 and any(x["side"] == "yes" for x in b["flagged"])
    assert "Price-level ladder test" in (tmp_path / "ladder.md").read_text()


def test_bayes_bucket_key_is_not_off_by_one_at_bucket_edges():
    assert int(0.95 / 0.05) == 18  # the floating-point trap
    assert int(0.95 / 0.05 + 1e-9) == 19 and int(0.9 / 0.05 + 1e-9) == 18
