# Backtest log

One entry per backtest run that led to a decision. Raw results for the latest run are in
`reports/backtest.md` and on the dashboard's Backtest page. Git history has every weekly run.

How to read the numbers: flat $10 per trade at the ask plus the Kalshi taker fee, held to
settlement. "Return per $" is P&L divided by money staked. A strategy counts only if it made
money in **both halves** of the period with 30+ trades.

---

## 2026-11-08: first backtest, v1 to v2

- **Data:** Mar 12 to Nov 7, 2026. Highs had 1,677 events, lows 1,685, Bitcoin 239 (5pm ET only, strikes within 4% of the price).
- **Entries tested:** highs at 8am on the day and 10am the day before. Lows at 8pm and 10am the day before. Bitcoin 8h and 4h before the close.
- **Forecasts:** Open-Meteo NBM runs made 1-2 days earlier. These are staler than live NWS forecasts, so the weather results lean pessimistic.

| Book | Best | Worst | Live v1 equivalent |
|---|---|---|---|
| Highs | Market favorite, +$8 / 2,208 trades (0%) | v2 calibrated, -24.8% | v1, -20.7% |
| Lows | Long-shot fade, +$135 / 2,489 (+0.6%, but lost in the 2nd half) | v1, -27.2% | v1, -27.2% |
| Bitcoin | Vol x0.5, +$360 / 711 (+5.2%, both halves, t=2.75) | Blend, -43.5% | v1, -29.8% |

**Findings**
- Weather markets are well calibrated, and our forecast model's accuracy score (Brier) is worse than the market's on every strategy. A sigma sweep (0.6x-1.5x) and a blend sweep (0-75% market weight) were all negative.
- NBM daily max/min from hourly values runs about 1.5-2F cold on highs and warm on lows. The learned bias absorbs this.
- Bitcoin YES long shots are overpriced and favorites are underpriced (a favorite-longshot bias). A lower volatility exploits that.
- Bug fixed during this run: a 1-hour look-ahead in Coinbase prices had inflated Bitcoin to +39%.

**Decision (v2):** weather books switch to the long-shot fade while forecasts keep being logged. Bitcoin and gold use vol x0.5. All books reset.

**Next ideas to test:** a fresher forecast source for weather (live NWS hourly plus same-day observations); Bitcoin vol x0.5 with the fade combined; a gold backtest; trending fade on settled history.

---

## 2026-11-08: market scanner, first run

- **Data:** the 115 most-traded series across 10 categories (Sports 76, Commodities 6, Economics 6, Weather 6, Financials 5, Science 5, Mentions 4, Politics 3, Elections 2, Entertainment 2). Sampled 10 recent events each (about 45 days), giving 27,569 price snapshots at 24h, 6h and 1h before close.
- **Arbitrage:** 0 real opportunities in 351 one-winner events. The first run showed 162, but those were false positives from ladders where several markets can win. Fixed by only using events Kalshi marks mutually exclusive.
- **Sports:** very well calibrated, so it's hard to beat on price alone. The fade was -1.3%, favorites -2.9%, and the price-correction rule -19.5% on the holdout.
- **Commodities (gold, oil):** the same pattern as Bitcoin. Mid-priced YES on price ranges wins less often than priced (25-35c contracts won about 17%), and favorites win more (94c+ won 100%). This points to markets overpricing big moves.
- **Entry timing:** buying favorites 24h out lost 4.8%. In the last hour it made +1.8% (90% range -0..+4). That's borderline and needs care, because the last hour can overlap with games already underway.
- **Price-correction rule (holdout):** failed in Sports. Too few trades elsewhere to judge.

**Decision:** no live change. Next, test the Bitcoin-style model (lognormal with reduced volatility) on other price markets: gold, WTI and Brent oil, Ethereum, and S&P 500 / Nasdaq daily ranges, with full history.

---

## 2026-11-09: other price markets (run 42569514706, main)

- **Data:** Mar 13 to Nov 8, 2026. Bitcoin and weather were re-run on the same history. Ethereum (KXETHD, 5pm events only, Coinbase prices) had 235 events.
- **Yahoo blocked us:** gold, silver, WTI, Brent, natural gas, S&P 500 and Nasdaq all got HTTP 429 (Too Many Requests) from Yahoo on GitHub's servers, so they have no results yet. The options-implied indexes on Yahoo (VIX, OVX, GVZ) are affected too. A data source that allows automated access is needed.
- **Ethereum confirms the Bitcoin pattern:** vol x0.5 with a 5c edge made +$241 on 585 trades (+4.2%/$), and vol x0.5 made +3.7% on 494. Both were profitable in both halves. Full vol (v1) lost 15.8%. The vol sweep is positive from 0.3 to 0.75 and negative at 1.0.
- **Bitcoin (re-run):** vol x0.5 made +$363 on 707 trades (+5.3%), in both halves. Unchanged.
- **Weather:** still no strategy made money in both halves.
- The verdict line picked "Market favorite" (+7.5% on only 50 trades). The more trustworthy result is vol x0.5 with its 10x larger sample.

**Decision:** no live change yet. Next: an Ethereum paper book with vol x0.5 + 5c edge alongside Bitcoin, a replacement price source for commodities and indexes, and the options-implied check (PR #10).
