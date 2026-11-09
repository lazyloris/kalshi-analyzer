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
