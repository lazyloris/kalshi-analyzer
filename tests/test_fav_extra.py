from kalshi_analyzer.backtest import fav_extra as F


def _c(ask=0.80, won=True, close=100000, hours=4):
    return {"ticker": "T", "event": "E1", "close": close, "hours": hours, "bid": ask - 0.01, "ask": ask,
            "won": won, "source": "live", "date": "2026-05-01"}


def test_trade_rows_parses_both_price_formats():
    rows = F.trade_rows([{"created_time": "2026-05-01T12:00:00Z", "yes_price": 81, "count": 5, "taker_side": "no"},
                         {"created_time": "2026-05-01T11:00:00Z", "yes_price_dollars": "0.7900", "count_fp": "2.00"}])
    assert rows[0][1] == 0.79 and rows[0][2] == 2 and rows[1][1] == 0.81 and rows[1][3] == "no"


def test_maker_fill_rules_and_no_lookahead():
    c = _c()
    entry = c["close"] - 4 * 3600
    before = {"T": [[entry - 10, 0.70, 5, "no"]]}                       # trade before entry: ignored
    assert not F.maker_sim([c], before, 0.02)[0]["filled"]
    at_bid = {"T": [[entry + 60, 0.78, 5, "no"]]}
    assert not F.maker_sim([c], at_bid, 0.02, "through")[0]["filled"]   # at our price: not surely filled
    r = F.maker_sim([c], at_bid, 0.02, "touch")[0]
    assert r["filled"] and r["price"] == 0.78 and r["pnl"] == round(12 - 12 * 0.78, 4)
    below = {"T": [[entry + 60, 0.77, 1, "yes"]]}
    assert F.maker_sim([c], below, 0.02, "through")[0]["filled"]
    late = {"T": [[c["close"] - 600, 0.70, 1, "no"]]}                   # after the 30-min cutoff
    assert not F.maker_sim([c], late, 0.02)[0]["filled"]
    lost = F.maker_sim([_c(won=False)], below, 0.02)[0]
    assert lost["pnl"] < 0


def test_score_counts_missed_fills_as_zero():
    rows = [{**_c(), "filled": True, "cost": 9.36, "pnl": 2.64}, {**_c(), "event": "E2", "filled": False, "cost": 0.0, "pnl": 0.0}]
    s = F.score(rows)
    assert s["fill_rate"] == 0.5 and s["pnl"] == 2.64 and s["roi"] == round(2.64 / 9.36, 4)
