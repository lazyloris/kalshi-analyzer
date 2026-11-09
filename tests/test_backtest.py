import datetime as dt
import random

from kalshi_analyzer.backtest import __main__ as BT
from kalshi_analyzer.backtest import data as D
from kalshi_analyzer.backtest import engine as E

MON = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def _fake_weather(days=40, seed=1):
    rnd = random.Random(seed)
    markets, cands, nbm = {}, {}, {}
    start = dt.date(2026, 9, 1)
    for i in range(days):
        d = start + dt.timedelta(days=i)
        fc = 60 + rnd.uniform(-10, 10)
        actual = round(fc + rnd.gauss(0.5, 1.5))
        nbm[d.isoformat()] = {"high": {"1": round(fc, 1), "2": round(fc + rnd.gauss(0, 1), 1)}, "low": {}}
        ev = f"KXHIGHNY-{d:%y}{MON[d.month - 1]}{d:%d}"
        close = dt.datetime(d.year, d.month, d.day, 23, 59, tzinfo=dt.timezone.utc) + dt.timedelta(hours=5)
        base = int(round(fc)) - 6
        for k in range(6):
            lo = base + 2 * k
            t = f"{ev}-B{lo + 0.5}"
            won = lo <= actual <= lo + 1
            markets[t] = {"ticker": t, "event_ticker": ev, "strike_type": "between", "floor": lo, "cap": lo + 1,
                          "close_time": close.isoformat().replace("+00:00", "Z"), "result": "yes" if won else "no",
                          "value": f"{actual}.00", "source": "live"}
            p = max(0.02, min(0.95, 0.45 - 0.12 * abs(lo + 0.5 - fc)))
            cands[t] = [[int(close.timestamp()) - h * 3600, round(p - 0.01, 2), round(p + 0.01, 2), 5.0]
                        for h in range(60, 0, -1)]
    return {"markets": markets, "candles": cands}, nbm


def test_quote_uses_last_candle_before_entry():
    cs = [[100, 0.2, 0.25, 1], [3700, 0.3, 0.33, 2], [7300, 0.9, 0.95, 3]]
    assert E.quote(cs, 7000) == (0.3, 0.33, 3)
    assert E.quote(cs, 50) is None
    assert E.quote([[100, 0.0, 1.0, 0]], 200) is None  # no two-sided market


def test_calibration_learns_bias_without_lookahead():
    k, nbm = _fake_weather()
    evs = E.calibrate(E.weather_events("weather_high", {"KXHIGHNY": k}, {"NY": nbm}))
    assert evs and evs[0]["calib_n"] == 0 and evs[0]["bias"] == 0
    late = [e for e in evs if e["entry"] == "same day 8am"][-1]
    assert late["calib_n"] >= 20 and 0 < late["bias"] < 1.5 and 1.0 <= late["sigma"] < 2.2


def test_full_backtest_offline(tmp_path, monkeypatch):
    monkeypatch.setattr(D, "CACHE", tmp_path / "cache")
    monkeypatch.setattr(BT, "OUT_JSON", tmp_path / "bt.json")
    monkeypatch.setattr(BT, "OUT_MD", tmp_path / "bt.md")
    k, nbm = _fake_weather()
    D._save("kalshi_KXHIGHNY", k)
    D._save("nbm_NY", nbm)
    r = BT.run(dt.datetime(2026, 11, 8, tzinfo=dt.timezone.utc))
    wh = r["books"]["weather_high"]
    ids = {s["id"] for s in wh["strategies"]}
    assert {"v1", "v2", "v2_blend", "fc_bracket", "favorite", "fade"} <= ids
    assert any(s["trades"] > 0 for s in wh["strategies"])
    assert wh["sweeps"]["sigma"] and wh["forecast_errors"][0]["n"] > 0
    assert "Verdict" in (tmp_path / "bt.md").read_text()
    for s in wh["strategies"]:
        assert s["trades"] == 0 or abs(sum(v["pnl"] for v in s["by_city"].values()) - s["pnl"]) < 0.05


def test_crypto_events_and_strategies():
    close = dt.datetime(2026, 10, 20, 21, 0, tzinfo=dt.timezone.utc)
    prices = {int(close.timestamp()) - h * 3600: 70000 * (1 + 0.001 * ((h % 7) - 3)) for h in range(0, 40 * 24)}
    ms, cs = {}, {}
    for k in range(-3, 4):
        strike = 70000 + 500 * k - 0.01
        t = f"KXBTCD-26OCT2017-T{strike}"
        ms[t] = {"ticker": t, "event_ticker": "KXBTCD-26OCT2017", "strike_type": "greater", "floor": strike, "cap": None,
                 "close_time": close.isoformat().replace("+00:00", "Z"), "result": "yes" if k <= 0 else "no",
                 "value": "70100", "source": "live"}
        p = max(0.03, min(0.97, 0.5 - 0.15 * k))
        cs[t] = [[int(close.timestamp()) - h * 3600, p - 0.01, p + 0.01, 3] for h in range(20, 0, -1)]
    evs = E.crypto_events("KXBTCD", {"markets": ms, "candles": cs}, prices)
    assert len(evs) == 2 and evs[0]["vol"] > 0
    for sid, name, desc, pick in E.crypto_strategies():
        E.metrics(E.simulate(evs, pick))


def test_scanner_analyze_offline(tmp_path, monkeypatch):
    from kalshi_analyzer.backtest import scanner as SC
    monkeypatch.setattr(D, "CACHE", tmp_path / "cache")
    monkeypatch.setattr(SC, "OUT_JSON", tmp_path / "scan.json")
    monkeypatch.setattr(SC, "OUT_MD", tmp_path / "scan.md")
    rnd = random.Random(3)
    markets, cands = {}, {}
    base = dt.datetime(2026, 9, 20, 20, tzinfo=dt.timezone.utc)
    for e in range(30):
        close = base + dt.timedelta(days=e)
        ev = f"KXTEST-{e:02d}"
        winner = rnd.randrange(5)
        for k in range(5):
            t = f"{ev}-B{k}"
            markets[t] = {"ticker": t, "event_ticker": ev, "strike_type": "between", "floor": k, "cap": k,
                          "close_time": close.isoformat().replace("+00:00", "Z"), "result": "yes" if k == winner else "no",
                          "value": "", "source": "live"}
            p = 0.6 if k == winner else 0.07  # market is right-ish; long shots slightly overpriced
            cands[t] = [[int(close.timestamp()) - h * 3600, round(p - 0.01, 2), round(p + 0.01, 2), 3] for h in range(30, 0, -1)]
    D._save("scan_KXTEST", {"markets": markets, "candles": cands, "events": {f"KXTEST-{e:02d}": True for e in range(30)}})
    D._save("scan_index", {"KXTEST": {"category": "Test", "title": "Test series", "vol24": 100, "open_markets": 5, "median_spread": 0.02}})
    r = SC.analyze(dt.datetime(2026, 11, 8, tzinfo=dt.timezone.utc))
    assert r["series_scanned"] == 1 and r["quotes"] == 30 * 5 * 3
    assert r["series"][0]["fade"]["trades"] > 0 and r["series"][0]["fade"]["roi"] > 0
    assert r["arbitrage"]["ladders_checked"] == 90
    assert "Market scanner" in (tmp_path / "scan.md").read_text()


def test_asset_events_learn_basis_and_trade(tmp_path, monkeypatch):
    from kalshi_analyzer.backtest import assets as A
    monkeypatch.setattr(D, "CACHE", tmp_path / "cache")
    monkeypatch.setattr(BT, "OUT_JSON", tmp_path / "bt.json")
    monkeypatch.setattr(BT, "OUT_MD", tmp_path / "bt.md")
    rnd = random.Random(5)
    first = dt.datetime(2026, 8, 1, 21, tzinfo=dt.timezone.utc)
    prices, px = {}, 2000.0
    t0 = int(first.timestamp()) - 40 * 86400
    for h in range(0, 110 * 24):
        px *= 1 + rnd.gauss(0, 0.003)
        prices[t0 + h * 3600] = px
    hours = sorted(prices)
    ms, cs = {}, {}
    for d in range(60):
        close = int((first + dt.timedelta(days=d)).timestamp())
        settle = A.price_at(prices, hours, close, 7200)[1] * 1.004  # Kalshi source 0.4% above ours
        spot = A.price_at(prices, hours, close - 8 * 3600, 7200)[1]
        ev = f"KXGOLDD-{d:02d}"
        for k in range(-4, 5):
            strike = round(spot * (1 + 0.005 * k), 2)
            t = f"{ev}-T{strike}"
            ms[t] = {"ticker": t, "event_ticker": ev, "strike_type": "greater", "floor": strike, "cap": None,
                     "close_time": dt.datetime.fromtimestamp(close, dt.timezone.utc).isoformat().replace("+00:00", "Z"),
                     "result": "yes" if settle > strike else "no", "value": f"{settle:.2f}", "source": "live"}
            p = max(0.03, min(0.97, 0.5 - 0.12 * k))
            cs[t] = [[close - h * 3600, round(p - 0.01, 2), round(p + 0.01, 2), 3] for h in range(30, 0, -1)]
    D._save("kalshi_KXGOLDD", {"markets": ms, "candles": cs})
    D._save("yahoo_close_GC=F", {str(k): v for k, v in prices.items()})
    evs = A.asset_events("gold", *A.load("gold"))
    assert evs and abs(evs[-1]["basis"] - 1.004) < 1e-3
    assert {e["entry"] for e in evs} == {"8h before", "4h before", "1h before"}
    r = BT.run(dt.datetime(2026, 11, 8, tzinfo=dt.timezone.utc))
    g = r["books"]["asset_gold"]
    assert g["events"] > 40 and g["verdict"]["text"] and g["sweeps"]["vol"]


def test_one_close_per_day_drops_hourly_events():
    from kalshi_analyzer.backtest import assets as A
    ms = {}
    for d in range(3):
        for h in range(24):
            t = dt.datetime(2026, 10, 1 + d, h, tzinfo=dt.timezone.utc)
            ms[f"E{d}{h}"] = {"close_time": t.isoformat().replace("+00:00", "Z")}
    kept = A.one_close_per_day(ms, 17)
    assert len(kept) == 3  # 17:00 ET = 21:00 UTC in October
    assert len(A.one_close_per_day({"a": ms["E00"]})) == 1


def test_implied_vol_strategies_use_only_past_values():
    close = dt.datetime(2026, 10, 20, 21, 0, tzinfo=dt.timezone.utc)
    ts = int(close.timestamp())
    prices = {ts - h * 3600: 70000 * (1 + 0.001 * ((h % 7) - 3)) for h in range(0, 40 * 24)}
    ms, cs = {}, {}
    for k in range(-3, 4):
        strike = 70000 + 500 * k - 0.01
        t = f"KXBTCD-26OCT2017-T{strike}"
        ms[t] = {"ticker": t, "event_ticker": "KXBTCD-26OCT2017", "strike_type": "greater", "floor": strike, "cap": None,
                 "close_time": close.isoformat().replace("+00:00", "Z"), "result": "yes" if k <= 0 else "no",
                 "value": "70100", "source": "live"}
        p = max(0.03, min(0.97, 0.5 - 0.15 * k))
        cs[t] = [[ts - h * 3600, p - 0.01, p + 0.01, 3] for h in range(20, 0, -1)]
    evs = E.crypto_events("KXBTCD", {"markets": ms, "candles": cs}, prices)
    iv = {ts - 9 * 3600: 40.0, ts - 5 * 3600: 80.0}  # 80 only becomes known after the 8h entry
    assert E.attach_ivol(evs, iv) == 2
    by = {e["entry"]: e["ivol"] for e in evs}
    assert by["8h before"] == 0.40 and by["4h before"] == 0.80
    for sid, name, desc, pick in E.iv_strategies():
        E.metrics(E.simulate(evs, pick))


def _btc_events(hours_of_prices=40 * 24):
    close = dt.datetime(2026, 10, 20, 21, 0, tzinfo=dt.timezone.utc)
    ts = int(close.timestamp())
    prices = {ts - h * 3600: 70000 * (1 + 0.002 * ((h % 7) - 3)) for h in range(0, hours_of_prices)}
    ms, cs = {}, {}
    for k in range(-3, 4):
        strike = 70000 + 500 * k - 0.01
        t = f"KXBTCD-26OCT2017-T{strike}"
        ms[t] = {"ticker": t, "event_ticker": "KXBTCD-26OCT2017", "strike_type": "greater", "floor": strike, "cap": None,
                 "close_time": close.isoformat().replace("+00:00", "Z"), "result": "yes" if k <= 0 else "no",
                 "value": "70100", "source": "live"}
        p = max(0.03, min(0.97, 0.5 - 0.15 * k))
        cs[t] = [[ts - h * 3600, p - 0.02, p + 0.02, 3] for h in range(20, 0, -1)]
    return E.crypto_events("KXBTCD", {"markets": ms, "candles": cs}, prices), prices, ts


def test_signals_enrich_and_strategies_run():
    from kalshi_analyzer.backtest import signals as S
    evs, prices, ts = _btc_events()
    S.enrich(evs, prices, tod=True)
    e = evs[0]
    assert e["close"] == ts and e["tod_vol"] > 0 and e["regime"] > 0 and "ret24" in e
    assert e["news_in_window"] is None  # Oct 20 2026: no CPI/jobs/Fed release
    for sid, name, desc, pick in S.crypto_strategies() + S.weather_strategies():
        E.metrics(E.simulate(evs, pick))


def test_news_calendar_flags_cpi_day():
    from kalshi_analyzer.backtest import signals as S
    close = int(dt.datetime(2026, 10, 14, 17, tzinfo=S.ET).timestamp())
    m = {"close_time": dt.datetime.fromtimestamp(close, dt.timezone.utc).isoformat()}
    early = {"ts": close - 10 * 3600, "markets": [m]}  # 7am, before the 8:30 CPI release
    late = {"ts": close - 4 * 3600, "markets": [m]}
    S.enrich([early, late])
    assert early["news_in_window"] == "cpi" and late["news_in_window"] is None
    assert early["news_day"] == late["news_day"] == "cpi"


def test_maker_fills_only_when_a_later_quote_reaches_our_price():
    from kalshi_analyzer.backtest import signals as S
    close = 10 * 3600
    m = {"ticker": "T", "strike_type": "greater", "floor": 1, "cap": None, "close_time":
         dt.datetime.fromtimestamp(close, dt.timezone.utc).isoformat(), "bid": 0.40, "ask": 0.45, "won_yes": True,
         "cs": [[3600, 0.40, 0.45, 1], [7200, 0.38, 0.40, 1]]}
    e = {"date": "x", "ts": 3600, "series": "S", "city": "c", "entry": "e", "markets": [m]}
    base = lambda ev: [E._trade(ev, m, "yes", 0.6)]
    got = S.maker(base)(e)
    assert len(got) == 1 and got[0]["price"] == 0.41 and got[0]["order"] == "maker"
    assert got[0]["pnl"] > base(e)[0]["pnl"]  # cheaper than paying the 45c ask
    m["cs"] = [[3600, 0.40, 0.45, 1], [7200, 0.41, 0.44, 1]]  # never comes down to 41c
    assert S.maker(base)(e) == []
    m["cs"] = [[3600, 0.40, 0.45, 1], [7200, 0.39, 0.41, 1]]
    assert len(S.maker(base)(e)) == 1 and S.maker(base, through=True)(e) == []


def test_spike_fade_bets_against_recent_jump():
    from kalshi_analyzer.backtest import signals as S
    m = {"ticker": "T", "strike_type": "greater", "floor": 1, "cap": None, "close_time": "2026-10-20T21:00:00Z",
         "bid": 0.60, "ask": 0.62, "won_yes": False, "cs": [[0, 0.30, 0.32, 1], [3 * 3600, 0.60, 0.62, 1]]}
    e = {"date": "x", "ts": 3 * 3600 + 60, "series": "S", "city": "c", "entry": "e", "markets": [m]}
    t = S.spike_fade()(e)
    assert len(t) == 1 and t[0]["side"] == "no" and t[0]["won"]


def test_late_strategies_buy_the_favorite_in_band():
    from kalshi_analyzer.backtest import engine as E
    e = {"book": "x", "kind": "weather", "series": "S", "event": "EV", "date": "2025-06-01", "entry": "same day 4pm", "ts": 0,
         "city": "C", "markets": [
             {"ticker": "A", "bid": 0.84, "ask": 0.86, "won_yes": True},
             {"ticker": "B", "bid": 0.10, "ask": 0.12, "won_yes": False}]}
    picks = {sid: pick(e) for sid, _, _, pick in E.late_strategies()}
    assert [t["ticker"] for t in picks["late_fav_80_90"]] == ["A"]
    assert picks["late_fav_50_80"] == [] and picks["late_fav_90_97"] == []


def test_beta_cdf_matches_known_values():
    from kalshi_analyzer.backtest.bayes import beta_cdf
    assert abs(beta_cdf(0.5, 1, 1) - 0.5) < 1e-9
    assert abs(beta_cdf(0.3, 2, 2) - (3 * 0.09 - 2 * 0.027)) < 1e-9
    assert abs(beta_cdf(0.9, 50, 5) - (1 - beta_cdf(0.1, 5, 50))) < 1e-9


def _ev(i, ask, won):
    import datetime as dt
    d = (dt.date(2025, 1, 1) + dt.timedelta(days=i)).isoformat()
    ts = int(dt.datetime.fromisoformat(d + "T12:00:00+00:00").timestamp())
    return {"book": "x", "kind": "weather", "series": "S", "event": f"E{i}", "date": d, "entry": "a", "ts": ts,
            "city": "C", "markets": [{"ticker": f"T{i}", "bid": ask - 0.02, "ask": ask, "won_yes": won}]}


def test_bucket_posterior_learns_underpriced_level_without_lookahead():
    from kalshi_analyzer.backtest import bayes as B, engine as E
    evs = [_ev(i, 0.60, True) for i in range(80)]  # 60c YES that always wins
    trades = E.simulate(evs, B.bucket_posterior(0.95))
    assert trades and all(t["side"] == "yes" for t in trades)
    first = min(t["date"] for t in trades)
    assert first >= evs[31]["date"]  # needs 30 settled (outcomes known 2 days later)


def test_market_prior_ignores_a_useless_model():
    from kalshi_analyzer.backtest import bayes as B, engine as E
    import random
    rnd = random.Random(1)
    evs = [_ev(i, 0.52, rnd.random() < 0.5) for i in range(400)]
    pick = B.market_prior(lambda e, m: rnd.random(), min_obs=100)
    E.simulate(evs, pick)
    assert pick.state["w"] <= 0.1


def test_fat_tail_odds_come_from_past_moves_only():
    from kalshi_analyzer.backtest import fattail as F
    t0 = 1_700_000_000 - 1_700_000_000 % 3600
    prices = {t0 + i * 3600: 100.0 * (1.01 if i % 2 else 1.0) for i in range(24 * 100)}
    e = {"ts": t0 + 24 * 95 * 3600, "hours": 1, "spot": 100.0}
    prices[e["ts"] + 3600] = 1e9  # a future price must not leak in
    assert F.attach([e], prices) == 1
    assert max(e["emp"]) < 0.02
    m = {"strike_type": "greater", "floor": "100.5", "cap": None}
    assert abs(F.p_emp(e, m) - 0.5) < 0.02  # half of past 1h moves were +1%
