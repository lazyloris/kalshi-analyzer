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

## What changed (v2)

- Sigma is now **measured**, not guessed: a rolling forecast error per city and days ahead, with a
  floor so it never gets overconfident. The starting values before any data are 1.5 / 2.0 / 2.8°F.
- Bias per city is learned the same way.
- **Market blend:** the trade decision uses a mix of our model and the market price. The weight
  comes from the backtest.
- **Disagreement cap:** if the model and market disagree by more than a set amount, skip the trade.
- Bitcoin volatility is scaled down, by a factor from the backtest.
- All books were reset to $1,000. The old trades are archived in `data/<book>/archive/`, and the
  dashboard's version column separates v1 from v2.
- A backtester now replays months of real Kalshi prices against archived forecasts, so the next
  rule change is tested on hundreds of events, not 14.
