from kalshi_analyzer import minute_lag as ML


def test_lag_trade_buys_yes_after_jump_when_kalshi_is_stale():
    close = 1_800_000_000 - 1_800_000_000 % 60
    px = {}
    for i in range(720):
        t = close - (720 - i) * 60
        px[str(t)] = 100_000.0 * (1 + 0.0002 * (i % 2))  # calm
    jump_t = close - 3 * 3600
    for t in list(px):
        if int(t) >= jump_t:
            px[t] = 101_000.0  # +1% jump 3h before close
    cs = [[close - (360 - i) * 60, 0.40, 0.42, 5] for i in range(361)]  # Kalshi never reprices
    m = {"ticker": "T", "floor": "100500", "cap": None, "strike_type": "greater", "result": "yes", "cs": cs}
    cache = {"events": {"E": {"close": close, "px": px, "markets": [m]}}}
    trades = ML.simulate(cache, move=0.003, edge=0.05, mult=1.0)
    assert trades and trades[0]["side"] == "yes" and trades[0]["ts"] >= jump_t
    assert all(t["pnl"] > 0 for t in trades)
    s = ML.summary(trades)
    assert s["trades"] == len(trades)


def test_delay_uses_a_later_quote():
    close = 1_800_000_000 - 1_800_000_000 % 60
    px = {str(close - (720 - i) * 60): 100_000.0 * (1 + 0.0002 * (i % 2)) for i in range(720)}
    jump_t = close - 3 * 3600
    for t in list(px):
        if int(t) >= jump_t:
            px[t] = 101_000.0
    cs = [[close - (360 - i) * 60, 0.40, 0.42, 5] for i in range(361)]
    for c in cs:
        if c[0] > jump_t:
            c[1], c[2] = 0.60, 0.62  # Kalshi catches up one minute after the jump
    m = {"ticker": "T", "floor": "100500", "cap": None, "strike_type": "greater", "result": "yes", "cs": cs}
    cache = {"events": {"E": {"close": close, "px": px, "markets": [m]}}}
    now = ML.simulate(cache, 0.003, 0.05, 1.0)
    late = ML.simulate(cache, 0.003, 0.05, 1.0, delay=1)
    assert now and now[0]["price"] == 0.42
    assert not late or late[0]["price"] == 0.62
