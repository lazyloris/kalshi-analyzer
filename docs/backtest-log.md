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
