# Post-mortem: first paper trades (Nov 7–8, 2026)

**Result:** every book that settled lost money. All money is paper.

| Book | Settled | Won | P&L | Still open at reset |
|---|---|---|---|---|
| Weather highs | 14 | 2 | −$105.34 | 23 |
| Weather lows | 3 | 1 | −$17.12 | 15 |
| Bitcoin | 2 | 0 | −$21.14 | 2 |
| Gold | 0 | 0 | $0 | 2 |
| Trending | 0 | 0 | $0 | 0 |

## What went wrong

1. **The weather model was far too unsure of itself.** It assumed the NWS forecast misses by
   about 2.0°F same-day and 2.5°F next-day (sigma). The real miss on these days was about 1.6°F
   on average, with almost no bias. A wider curve spreads probability onto the brackets next to the
   forecast, so the model:
   - bought cheap YES on neighbor brackets (7–18¢). That was 7 of 7 losses on highs and 2 of 2 on lows.
   - bought NO on the bracket the forecast pointed at. 5 of 7 lost: the temperature landed right
     where the forecast said (Miami 87, Philadelphia 59, Los Angeles 85).
2. **It trusted itself over the market by huge margins.** It thought its trades would win 49% of
   the time on average at an average price of 26¢. They won 14%. A gap that big is almost always
   the model being wrong, not the market. Accuracy score (Brier, lower is better) for highs:
   model 0.21, market 0.09.
3. **Bitcoin had the same problem.** 30-day realized volatility made the model think a $750 move
   in 17 hours was likely. It bought NO on "above $75,000" and "above $75,250" at 8–15¢, and both lost.
4. **One settlement detail we had wrong.** Kalshi's weather rules name **The Weather Company**
   (weather.com/kalshi) as the source, for the station's daily climate report. Our notes said "NWS".
   The number is the same station report, but small differences are possible, and the backtest
   learns any bias.
5. **Too few trades to be sure.** 19 settled trades is a small sample. Still, the errors all point
   the same way, and the fix (narrower, calibrated sigma, plus respect for the market) is cheap
   to test.

## What the backtest said (Mar 12 - Nov 7, 2026)

Real hourly Kalshi prices, archived NWS-blend forecasts, and $10 per trade with fees. Full numbers
are on the dashboard's Backtest page and in `docs/backtest-log.md`.

- **Weather: no forecast model beat the market.** Every model version lost 17-27% per dollar
  over about 1,700 events per book. That includes v1 (what we ran), calibrated sigma and bias, a
  market blend, and a disagreement cap. The market's prices were well calibrated. Our v1 live loss
  (-$105 on 14 trades) is exactly what the backtest predicts, so it was not bad luck.
- **Weather long-shot fade** (buy NO when YES costs 3-10c) was about break-even: -0.3% on highs,
  +0.6% on lows.
- **Bitcoin: our volatility was too high.** v1 lost 30% per dollar. Halving the volatility was the
  only setting profitable in both halves of the period: +5.2% per dollar on 711 trades. Kalshi's
  Bitcoin long shots are overpriced (YES at 5-10c won 3.6% of the time), and the fade earned +1.7%.
- One backtest bug was caught: Coinbase candles were keyed by start time, which leaked one hour
  of future price and made Bitcoin look like +39%. It is fixed, and the numbers above are the
  corrected ones.

## What changed (v2, live)

| Book | v1 | v2 |
|---|---|---|
| Weather highs / lows | Normal model, sigma 2.0/2.5F | **Long-shot fade.** Forecasts are still logged, and bias/sigma are learned per city for the next model attempt (starting sigma 1.5/2.0/2.8F). |
| Bitcoin | 30-day realized vol | **Vol x0.5** |
| Gold | 30-day realized vol | Vol x0.5. Copied from Bitcoin and **not backtested on gold**. |
| Trending | Long-shot fade | Unchanged |

New live options exist for later tests: `MARKET_BLEND` (trust the market price partly) and
`MAX_GAP` (skip big disagreements). Both are off by default because they didn't help in the backtest.

All books were reset to $1,000. The old trades are archived in `data/<book>/archive/`.
