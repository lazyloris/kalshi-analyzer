from kalshi_analyzer import swing as S


def _cs(mids, t0=1_700_000_000):
    return [[t0 + i * 60, round(m - 0.01, 2), round(m + 0.01, 2), 1] for i, m in enumerate(mids)]


def test_drop_then_rebound_locks_profit():
    mids = [0.60] * 6 + [0.48] * 3 + [0.58] * 3
    t, = S.simulate({"A": {"series": "X", "result": "no", "cs": _cs(mids)}}, drop=0.10, rebound=0.05)
    assert t["side"] == "yes" and t["locked"] and t["pnl"] > 0  # profit even though YES lost


def test_no_rebound_is_held_to_settlement():
    mids = [0.60] * 6 + [0.48] * 6
    t, = S.simulate({"A": {"series": "X", "result": "no", "cs": _cs(mids)}}, drop=0.10, rebound=0.05)
    assert not t["locked"] and t["pnl"] < -9
