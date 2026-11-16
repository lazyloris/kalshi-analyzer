# Backtest (2026-11-16)

Flat $10 per trade at the ask plus Kalshi fees, held to settlement. Prices are real hourly Kalshi quotes. Forecasts are archived NWS-blend (NBM) runs 1-2 days old. Bias/sigma learned only from earlier days.

## Live paper books vs backtest

| Book | Settled | Open | Live P&L | Live return/$ | Backtest rule | Backtest return/$ |
|---|---|---|---|---|---|---|
| bitcoin | 14 | 4 | +22.64 | +16.6% | c_vol50 | +0.4% |
| bitcoin_tod | 14 | 4 | +19.59 | +14.3% | s_combo_tod | +2.7% |
| ethereum | 14 | 4 | -13.12 | -9.6% | a_vol50 | -1.6% |
| ethereum_tod | 14 | 4 | -23.26 | -17.0% | s_combo_tod | +1.9% |
| weather_high | 64 | 25 | -31.23 | -5.1% | fade | +0.1% |
| weather_low | 25 | 11 | -10.73 | -4.5% | fade | +0.3% |

Live numbers need ~100 settled trades before they mean much.

## Weather: daily highs

3757 events, 2025-03-21 to 2026-11-15.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Kalshi price-spike fade (no model) (+145 on 489 trades).

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 489 | 45% | +145.28 | +2.9% | 0.46 | 0.28 | -184 | +330 | – | – | 0.1959 |
| Long-shot fade (no model) | 4971 | 95% | +34.78 | +0.1% | 0.23 | 0.27 | +41 | -6 | – | – | 0.0434 |
| Bayes: market prior + forecast | 2 | 50% | -4.85 | -24.4% | -0.29 | -0.29 | -10 | +5 | 74% | 0.3459 | 0.3305 |
| Bayes price-level, 99% sure | 1258 | 91% | -181.05 | -1.5% | -1.7 | -1.75 | -9 | -172 | 94% | 0.0794 | 0.078 |
| Heavy-volume move (10c, 5x): fade | 312 | 48% | -194.34 | -6.2% | -0.81 | -0.62 | -228 | +33 | – | – | 0.1842 |
| Combined: rolling best (past 6 months) | 2934 | 94% | -235.97 | -0.8% | -1.48 | -1.66 | +86 | -322 | – | – | 0.049 |
| Market favorite YES (no model) | 4617 | 50% | -345.83 | -0.7% | -0.51 | -0.51 | -168 | -178 | – | – | 0.2426 |
| Bayes price-level, 95% sure | 2185 | 88% | -392.16 | -1.9% | -2.3 | -2.14 | -206 | -186 | 91% | 0.0968 | 0.0952 |
| Heavy-volume move (10c, 5x): follow | 294 | 49% | -413.31 | -13.9% | -2.21 | -1.97 | -295 | -118 | – | – | 0.1952 |
| Long-shot fade, limit order | 2846 | 92% | -479.29 | -1.8% | -3.3 | -3.31 | -194 | -286 | – | – | 0.0731 |
| Heavy-volume move: fade | 1542 | 48% | -997.53 | -6.4% | -1.9 | -2.45 | -1019 | +22 | – | – | 0.1883 |
| Combined: 5+ strategies agree | 4993 | 49% | -1125.47 | -2.2% | -1.45 | -1.09 | -393 | -732 | 60% | 0.2246 | 0.2363 |
| Heavy-volume move: follow | 1507 | 49% | -1656.29 | -10.9% | -3.74 | -3.45 | -741 | -915 | – | – | 0.1927 |
| Favorite, stop loss 25c | 4617 | 42% | -2507.34 | -5.4% | -3.99 | -3.99 | -2137 | -370 | – | – | 0.2414 |
| Forecast bracket YES | 763 | 10% | -3506.52 | -43.7% | -6.32 | -6.32 | -1770 | -1737 | 33% | 0.1463 | 0.0915 |
| Favorite, take profit 10c | 4617 | 70% | -3714.84 | -8.0% | -8.56 | -8.56 | -2267 | -1448 | – | – | 0.2611 |
| Favorite, stop loss 10c | 4617 | 28% | -4306.91 | -9.2% | -8.93 | -8.93 | -2985 | -1322 | – | – | 0.2368 |
| Favorite, take profit 15c / stop 15c | 4617 | 47% | -5436.00 | -11.6% | -15.14 | -15.14 | -3802 | -1634 | – | – | 0.2512 |
| Market favorite, limit order | 3764 | 39% | -6568.28 | -17.7% | -10.21 | -10.21 | -4357 | -2212 | – | – | 0.2363 |
| v2 + disagreement cap | 3293 | 33% | -8306.22 | -24.6% | -7.75 | -7.01 | -4086 | -4221 | 54% | 0.2008 | 0.1577 |
| v1 (what we ran live) | 4527 | 34% | -9115.21 | -19.6% | -7.37 | -6.7 | -4468 | -4647 | 63% | 0.2622 | 0.1658 |
| v2 + 50% market blend | 3665 | 31% | -9254.77 | -24.6% | -8.29 | -7.39 | -4454 | -4801 | 46% | 0.1903 | 0.1654 |
| v2 calibrated | 4135 | 32% | -10022.08 | -23.6% | -8.58 | -7.82 | -4958 | -5064 | 58% | 0.244 | 0.168 |
| Combined: 3+ strategies agree | 9561 | 46% | -10566.72 | -10.9% | -7.79 | -5.85 | -3993 | -6574 | 62% | 0.2708 | 0.1935 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| v2 calibrated | 15 | +151.03 | +99.4% |
| v2 + 50% market blend | 13 | +130.80 | +99.7% |
| Long-shot fade (no model) | 2149 | +109.36 | +0.5% |
| Forecast bracket YES | 4 | +104.20 | +249.3% |
| Combined: rolling best (past 6 months) | 1552 | +86.34 | +0.6% |
| v1 (what we ran live) | 12 | +38.08 | +31.2% |
| v2 + disagreement cap | 12 | +37.79 | +31.2% |
| Bayes: market prior + forecast | 0 | +0.00 | – |
| Bayes price-level, 99% sure | 292 | -83.94 | -3.0% |
| Long-shot fade, limit order | 1157 | -122.44 | -1.1% |
| Kalshi price-spike fade (no model) | 222 | -123.93 | -5.5% |
| Heavy-volume move (10c, 5x): fade | 165 | -190.60 | -11.4% |
| Combined: 5+ strategies agree | 2337 | -198.82 | -0.8% |
| Bayes price-level, 95% sure | 767 | -235.73 | -3.2% |
| Market favorite YES (no model) | 2336 | -243.35 | -1.0% |
| Heavy-volume move (10c, 5x): follow | 152 | -269.05 | -17.5% |
| Combined: 3+ strategies agree | 2725 | -288.42 | -1.1% |
| Heavy-volume move: follow | 682 | -570.38 | -8.3% |
| Heavy-volume move: fade | 714 | -1017.50 | -14.1% |
| Favorite, stop loss 25c | 2336 | -2221.02 | -9.4% |
| Favorite, take profit 10c | 2336 | -2320.61 | -9.8% |
| Favorite, stop loss 10c | 2336 | -3076.66 | -13.0% |
| Favorite, take profit 15c / stop 15c | 2336 | -3850.34 | -16.2% |
| Market favorite, limit order | 1835 | -4268.62 | -23.5% |

Sweep: sigma

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 4108 | -9280.64 | -22.1% |
| 0.8 | 3975 | -9669.47 | -23.7% |
| 1.0 | 4135 | -10022.08 | -23.6% |
| 1.25 | 4391 | -8832.63 | -19.7% |
| 1.5 | 4544 | -7809.19 | -16.9% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 5032 | -11579.05 | -22.4% |
| blend 0.0, edge 0.05 | 4720 | -10902.17 | -22.5% |
| blend 0.0, edge 0.08 | 4135 | -10022.08 | -23.6% |
| blend 0.25, edge 0.03 | 4770 | -11290.49 | -23.1% |
| blend 0.25, edge 0.05 | 4277 | -10325.11 | -23.5% |
| blend 0.25, edge 0.08 | 3355 | -8730.45 | -25.3% |
| blend 0.5, edge 0.03 | 4113 | -10113.06 | -23.9% |
| blend 0.5, edge 0.05 | 3181 | -8225.55 | -25.1% |
| blend 0.5, edge 0.08 | 1928 | -4554.52 | -23.0% |
| blend 0.75, edge 0.03 | 1922 | -5173.41 | -26.1% |
| blend 0.75, edge 0.05 | 834 | -1874.51 | -21.7% |
| blend 0.75, edge 0.08 | 223 | -624.99 | -27.0% |

Rolling best: which strategy it picked each quarter

| Quarter | Picked | Past t |
|---|---|---|
| 2025-Q1 | sat out | – |
| 2025-Q2 | sat out | – |
| 2025-Q3 | Long-shot fade (no model) | 0.57 |
| 2025-Q4 | Long-shot fade (no model) | 1.58 |
| 2026-Q1 | Long-shot fade (no model) | 0.16 |
| 2026-Q2 | Long-shot fade (no model) | 0.31 |
| 2026-Q3 | Heavy-volume move (10c, 5x): fade | 1.0 |
| 2026-Q4 | Kalshi price-spike fade (no model) | 1.4 |

Why: v2 calibrated

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q1 | 285 | -591 | 37% |
| Quarter | 2026-Q2 | 1467 | -4421 | 33% |
| Quarter | 2026-Q3 | 1563 | -2938 | 32% |
| Quarter | 2026-Q4 | 820 | -2072 | 32% |
| Price paid | 0.00-0.10 | 834 | -3122 | 5% |
| Price paid | 0.10-0.30 | 875 | -3998 | 10% |
| Price paid | 0.30-0.50 | 882 | -1279 | 37% |
| Price paid | 0.50-0.70 | 1215 | -1378 | 53% |
| Price paid | 0.70-0.90 | 328 | -235 | 71% |
| Price paid | 0.90-1.01 | 1 | -10 | 0% |
| Model vs market gap | 0.05-0.10 | 62 | -14 | 16% |
| Model vs market gap | 0.10-0.20 | 2093 | -5918 | 32% |
| Model vs market gap | 0.20-0.35 | 1566 | -3223 | 35% |
| Model vs market gap | 0.35-1.01 | 414 | -868 | 30% |
| Side | no | 2504 | -3138 | 48% |
| Side | yes | 1631 | -6884 | 8% |

Why: Kalshi price-spike fade (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 8 | -46 | 25% |
| Quarter | 2025-Q2 | 60 | +32 | 35% |
| Quarter | 2025-Q3 | 53 | -102 | 40% |
| Quarter | 2025-Q4 | 23 | +22 | 48% |
| Quarter | 2026-Q1 | 99 | -104 | 39% |
| Quarter | 2026-Q2 | 111 | +134 | 50% |
| Quarter | 2026-Q3 | 96 | +272 | 52% |
| Quarter | 2026-Q4 | 39 | -62 | 46% |
| Price paid | 0.10-0.30 | 174 | -13 | 20% |
| Price paid | 0.30-0.50 | 130 | -10 | 41% |
| Price paid | 0.50-0.70 | 144 | +171 | 69% |
| Price paid | 0.70-0.90 | 41 | -2 | 76% |
| Model vs market gap | no model | 489 | +145 | 45% |
| Side | no | 282 | +109 | 58% |
| Side | yes | 207 | +36 | 26% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 37 | -76 | 60% |
| Quarter | 2025-Q3 | 211 | +7 | 95% |
| Quarter | 2025-Q4 | 159 | -19 | 91% |
| Quarter | 2026-Q1 | 484 | -129 | 87% |
| Quarter | 2026-Q2 | 530 | -94 | 88% |
| Quarter | 2026-Q3 | 538 | -33 | 89% |
| Quarter | 2026-Q4 | 226 | -48 | 86% |
| Price paid | 0.30-0.50 | 21 | -85 | 29% |
| Price paid | 0.50-0.70 | 33 | -1 | 52% |
| Price paid | 0.70-0.90 | 676 | -181 | 82% |
| Price paid | 0.90-1.01 | 1455 | -125 | 93% |
| Model vs market gap | 0.00-0.05 | 1958 | -204 | 90% |
| Model vs market gap | 0.05-0.10 | 206 | -104 | 77% |
| Model vs market gap | 0.10-0.20 | 21 | -85 | 29% |
| Side | no | 2129 | -286 | 89% |
| Side | yes | 56 | -106 | 41% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 544 | +57 | 96% |
| Quarter | 2025-Q4 | 268 | -37 | 94% |
| Quarter | 2026-Q1 | 968 | +74 | 96% |
| Quarter | 2026-Q2 | 1056 | -99 | 94% |
| Quarter | 2026-Q3 | 59 | -169 | 41% |
| Quarter | 2026-Q4 | 39 | -62 | 46% |
| Price paid | 0.10-0.30 | 26 | -226 | 4% |
| Price paid | 0.30-0.50 | 20 | +41 | 50% |
| Price paid | 0.50-0.70 | 39 | -19 | 59% |
| Price paid | 0.70-0.90 | 13 | -26 | 62% |
| Price paid | 0.90-1.01 | 2836 | -6 | 95% |
| Model vs market gap | no model | 2934 | -236 | 94% |
| Side | no | 2896 | -22 | 95% |
| Side | yes | 38 | -214 | 18% |

Forecast error (actual minus NBM forecast)

| City | Entry | n | Bias | RMSE |
|---|---|---|---|---|
| Austin | day before 10am | 247 | +1.76 | 3.33 |
| Austin | same day 8am | 249 | +1.49 | 2.94 |
| Chicago | day before 10am | 247 | +1.48 | 3.43 |
| Chicago | same day 8am | 245 | +1.31 | 2.86 |
| Denver | day before 10am | 248 | +1.74 | 3.38 |
| Denver | same day 8am | 245 | +1.67 | 2.95 |
| Los Angeles | day before 10am | 246 | +2.27 | 3.84 |
| Los Angeles | same day 8am | 248 | +2.28 | 3.58 |
| Miami | same day 8am | 248 | +2.04 | 2.65 |
| New York | same day 8am | 244 | -0.24 | 2.44 |
| Philadelphia | same day 8am | 244 | +1.71 | 2.87 |

## Weather: daily lows

2242 events, 2025-12-13 to 2026-11-15.

**Verdict:** Long-shot fade (no model): +96 on 3214 trades (+0.3% per $ staked, t=0.88), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 152 | 53% | +257.44 | +16.7% | 1.35 | 1.22 | -53 | +310 | – | – | 0.2106 |
| Combined: rolling best (past 6 months) | 1645 | 78% | +233.57 | +1.5% | 0.8 | 0.87 | +165 | +68 | – | – | 0.1229 |
| Long-shot fade (no model) | 3214 | 96% | +96.21 | +0.3% | 0.88 | 0.99 | +72 | +24 | – | – | 0.0368 |
| Heavy-volume move: follow | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Heavy-volume move: fade | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Heavy-volume move (10c, 5x): follow | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Heavy-volume move (10c, 5x): fade | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Bayes: market prior + forecast | 1 | 0% | -10.25 | -100.0% | – | – | +0 | -10 | 49% | 0.2401 | 0.16 |
| Bayes price-level, 95% sure | 369 | 94% | -14.72 | -0.4% | -0.29 | -0.22 | -52 | +37 | 96% | 0.0575 | 0.0579 |
| Bayes price-level, 99% sure | 201 | 94% | -24.01 | -1.2% | -0.71 | -0.63 | -14 | -10 | 96% | 0.0569 | 0.0567 |
| Long-shot fade, limit order | 1699 | 93% | -207.87 | -1.3% | -1.93 | -1.56 | -67 | -140 | – | – | 0.0668 |
| Combined: 5+ strategies agree | 2195 | 46% | -578.44 | -2.6% | -1.11 | -1.23 | +618 | -1196 | 54% | 0.235 | 0.2375 |
| Market favorite YES (no model) | 2131 | 47% | -676.62 | -3.1% | -1.37 | -1.37 | +528 | -1205 | – | – | 0.2398 |
| Forecast bracket YES | 552 | 14% | -1724.35 | -29.8% | -3.71 | -3.71 | -1089 | -636 | 34% | 0.1617 | 0.1215 |
| Favorite, take profit 10c | 2131 | 62% | -2788.55 | -12.9% | -8.22 | -8.22 | -982 | -1807 | – | – | 0.2661 |
| Market favorite, limit order | 1774 | 36% | -3039.87 | -17.3% | -6.36 | -6.36 | -765 | -2275 | – | – | 0.2266 |
| v2 + 50% market blend | 1883 | 30% | -3921.92 | -20.2% | -4.3 | -4.02 | -1056 | -2866 | 41% | 0.1563 | 0.1416 |
| Favorite, stop loss 25c | 2131 | 28% | -5345.01 | -24.7% | -12.93 | -12.93 | -2159 | -3186 | – | – | 0.2289 |
| v2 calibrated | 2610 | 31% | -5706.18 | -21.3% | -5.7 | -5.16 | -1746 | -3960 | 52% | 0.1992 | 0.1493 |
| Favorite, stop loss 10c | 2131 | 14% | -5793.86 | -26.8% | -20.72 | -20.72 | -2826 | -2968 | – | – | 0.2163 |
| v2 + disagreement cap | 2265 | 31% | -6119.66 | -26.3% | -6.93 | -6.93 | -2042 | -4078 | 50% | 0.1762 | 0.1425 |
| Combined: 3+ strategies agree | 4511 | 40% | -6251.41 | -13.6% | -6.07 | -5.34 | -2077 | -4174 | 56% | 0.232 | 0.1858 |
| Favorite, take profit 15c / stop 15c | 2131 | 28% | -6448.43 | -29.8% | -27.53 | -27.53 | -3264 | -3185 | – | – | 0.2352 |
| v1 (what we ran live) | 3839 | 32% | -10442.24 | -26.5% | -9.45 | -8.52 | -4620 | -5823 | 57% | 0.2254 | 0.1478 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Combined: 5+ strategies agree | 357 | +329.90 | +9.1% |
| Market favorite YES (no model) | 356 | +264.39 | +7.3% |
| Combined: 3+ strategies agree | 373 | +245.97 | +6.5% |
| Forecast bracket YES | 7 | +73.31 | +99.5% |
| v2 + disagreement cap | 17 | +62.01 | +36.3% |
| Heavy-volume move: follow | 0 | +0.00 | – |
| Heavy-volume move: fade | 0 | +0.00 | – |
| Heavy-volume move (10c, 5x): follow | 0 | +0.00 | – |
| Heavy-volume move (10c, 5x): fade | 0 | +0.00 | – |
| Bayes price-level, 95% sure | 0 | +0.00 | – |
| Bayes price-level, 99% sure | 0 | +0.00 | – |
| Bayes: market prior + forecast | 0 | +0.00 | – |
| Combined: rolling best (past 6 months) | 0 | +0.00 | – |
| v2 + 50% market blend | 17 | -18.42 | -10.6% |
| v2 calibrated | 18 | -28.84 | -15.7% |
| v1 (what we ran live) | 17 | -30.72 | -17.7% |
| Long-shot fade (no model) | 718 | -40.35 | -0.6% |
| Long-shot fade, limit order | 431 | -98.02 | -2.4% |
| Kalshi price-spike fade (no model) | 32 | -114.28 | -35.2% |
| Favorite, take profit 10c | 356 | -253.68 | -7.0% |
| Market favorite, limit order | 290 | -306.98 | -10.7% |
| Favorite, stop loss 25c | 356 | -703.87 | -19.4% |
| Favorite, stop loss 10c | 356 | -955.17 | -26.3% |
| Favorite, take profit 15c / stop 15c | 356 | -1099.83 | -30.3% |

Sweep: sigma

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 3368 | -5299.07 | -15.4% |
| 0.8 | 2672 | -4999.35 | -18.2% |
| 1.0 | 2610 | -5706.18 | -21.3% |
| 1.25 | 3044 | -6937.59 | -22.2% |
| 1.5 | 3570 | -8712.39 | -23.8% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 4020 | -9243.47 | -22.4% |
| blend 0.0, edge 0.05 | 3449 | -8211.54 | -23.2% |
| blend 0.0, edge 0.08 | 2610 | -5706.18 | -21.3% |
| blend 0.25, edge 0.03 | 3442 | -8123.80 | -23.0% |
| blend 0.25, edge 0.05 | 2698 | -5842.26 | -21.0% |
| blend 0.25, edge 0.08 | 1737 | -3563.91 | -19.9% |
| blend 0.5, edge 0.03 | 2354 | -5108.89 | -21.1% |
| blend 0.5, edge 0.05 | 1512 | -3150.41 | -20.2% |
| blend 0.5, edge 0.08 | 731 | -590.06 | -7.8% |
| blend 0.75, edge 0.03 | 629 | -666.61 | -10.2% |
| blend 0.75, edge 0.05 | 248 | -566.21 | -21.9% |
| blend 0.75, edge 0.08 | 55 | -374.62 | -65.3% |

Rolling best: which strategy it picked each quarter

| Quarter | Picked | Past t |
|---|---|---|
| 2025-Q4 | sat out | – |
| 2026-Q1 | sat out | – |
| 2026-Q2 | Market favorite YES (no model) | 0.41 |
| 2026-Q3 | Long-shot fade (no model) | 1.62 |
| 2026-Q4 | Kalshi price-spike fade (no model) | 1.95 |

Why: v2 calibrated

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q1 | 212 | -82 | 43% |
| Quarter | 2026-Q2 | 916 | -1917 | 32% |
| Quarter | 2026-Q3 | 1087 | -3128 | 29% |
| Quarter | 2026-Q4 | 395 | -580 | 30% |
| Price paid | 0.00-0.10 | 559 | -2261 | 4% |
| Price paid | 0.10-0.30 | 808 | -2354 | 12% |
| Price paid | 0.30-0.50 | 316 | -616 | 35% |
| Price paid | 0.50-0.70 | 639 | -347 | 58% |
| Price paid | 0.70-0.90 | 287 | -129 | 74% |
| Price paid | 0.90-1.01 | 1 | +1 | 100% |
| Model vs market gap | 0.05-0.10 | 36 | +38 | 19% |
| Model vs market gap | 0.10-0.20 | 1633 | -4570 | 31% |
| Model vs market gap | 0.20-0.35 | 778 | -576 | 35% |
| Model vs market gap | 0.35-1.01 | 163 | -598 | 24% |
| Side | no | 1227 | -1084 | 55% |
| Side | yes | 1383 | -4623 | 10% |

Why: Long-shot fade (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q1 | 950 | -40 | 95% |
| Quarter | 2026-Q2 | 1044 | +162 | 97% |
| Quarter | 2026-Q3 | 976 | -12 | 96% |
| Quarter | 2026-Q4 | 244 | -15 | 96% |
| Price paid | 0.90-1.01 | 3214 | +96 | 96% |
| Model vs market gap | no model | 3214 | +96 | 96% |
| Side | no | 3214 | +96 | 96% |

Why: Kalshi price-spike fade (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q4 | 1 | -10 | 0% |
| Quarter | 2026-Q1 | 34 | -22 | 41% |
| Quarter | 2026-Q2 | 53 | +65 | 53% |
| Quarter | 2026-Q3 | 58 | +211 | 60% |
| Quarter | 2026-Q4 | 6 | +13 | 67% |
| Price paid | 0.10-0.30 | 46 | +145 | 26% |
| Price paid | 0.30-0.50 | 29 | +54 | 48% |
| Price paid | 0.50-0.70 | 52 | +17 | 64% |
| Price paid | 0.70-0.90 | 25 | +41 | 88% |
| Model vs market gap | no model | 152 | +257 | 53% |
| Side | no | 95 | +48 | 64% |
| Side | yes | 57 | +210 | 35% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q2 | 98 | -13 | 94% |
| Quarter | 2026-Q3 | 195 | +19 | 95% |
| Quarter | 2026-Q4 | 76 | -21 | 90% |
| Price paid | 0.50-0.70 | 2 | -5 | 50% |
| Price paid | 0.70-0.90 | 14 | +24 | 86% |
| Price paid | 0.90-1.01 | 353 | -34 | 94% |
| Model vs market gap | 0.00-0.05 | 293 | -3 | 95% |
| Model vs market gap | 0.05-0.10 | 60 | -31 | 90% |
| Model vs market gap | 0.10-0.20 | 16 | +19 | 81% |
| Side | no | 353 | -34 | 94% |
| Side | yes | 16 | +19 | 81% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q2 | 663 | +232 | 51% |
| Quarter | 2026-Q3 | 976 | -12 | 96% |
| Quarter | 2026-Q4 | 6 | +13 | 67% |
| Price paid | 0.10-0.30 | 2 | -21 | 0% |
| Price paid | 0.30-0.50 | 445 | +373 | 48% |
| Price paid | 0.50-0.70 | 206 | -122 | 55% |
| Price paid | 0.70-0.90 | 16 | +16 | 81% |
| Price paid | 0.90-1.01 | 976 | -12 | 96% |
| Model vs market gap | no model | 1645 | +234 | 78% |
| Side | no | 979 | +19 | 96% |
| Side | yes | 666 | +215 | 51% |

Forecast error (actual minus NBM forecast)

| City | Entry | n | Bias | RMSE |
|---|---|---|---|---|
| Austin | day before 10am | 247 | -2.63 | 4.12 |
| Austin | day before 8pm | 249 | -2.72 | 3.98 |
| Chicago | day before 10am | 247 | -1.58 | 3.01 |
| Chicago | day before 8pm | 249 | -1.38 | 2.65 |
| Denver | day before 10am | 248 | -3.95 | 5.23 |
| Denver | day before 8pm | 249 | -3.81 | 5.07 |
| Los Angeles | day before 10am | 247 | +0.34 | 1.7 |
| Los Angeles | day before 8pm | 249 | +0.47 | 1.6 |
| Miami | day before 8pm | 247 | -0.94 | 2.38 |
| New York | day before 8pm | 249 | -1.62 | 2.71 |
| Philadelphia | day before 8pm | 249 | +0.45 | 2.21 |

## Crypto: Bitcoin 5pm price

603 events, 2025-03-22 to 2026-11-15.

**Verdict:** Vol x0.5, weekends only: +163 on 238 trades (+7.0% per $ staked, t=2.3), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Time-of-day vol x0.5 | 1544 | 80% | +309.27 | +2.1% | 1.54 | 1.76 | -142 | +451 | 92% | 0.1717 | 0.1588 |
| Time-of-day vol x0.5, skip spikes | 963 | 81% | +255.19 | +2.7% | 1.67 | 1.55 | -163 | +418 | 92% | 0.1631 | 0.1535 |
| Regime-scaled vol x0.5 | 1942 | 78% | +189.39 | +1.0% | 0.83 | 0.86 | -230 | +420 | 93% | 0.188 | 0.1669 |
| Vol x0.5, weekends only | 238 | 84% | +162.75 | +7.0% | 2.3 | 2.22 | +23 | +140 | 91% | 0.1216 | 0.1268 |
| Time-of-day vol x0.5, against trend + skip spikes | 508 | 82% | +158.42 | +3.2% | 1.45 | 1.51 | -110 | +268 | 93% | 0.1577 | 0.1488 |
| Bayes price-level, 95% sure | 653 | 92% | +141.37 | +2.2% | 1.84 | 1.01 | -6 | +147 | 93% | 0.0745 | 0.0756 |
| Vol x0.5, skip spiked markets | 1095 | 79% | +126.97 | +1.2% | 0.74 | 0.87 | -170 | +297 | 93% | 0.182 | 0.1627 |
| Vol x0.5, calm market only | 1042 | 79% | +87.42 | +0.9% | 0.54 | 0.7 | -100 | +188 | 92% | 0.1774 | 0.1604 |
| Vol x0.5 | 1774 | 78% | +77.69 | +0.4% | 0.35 | 0.47 | -286 | +364 | 93% | 0.1892 | 0.167 |
| Bayes price-level, 99% sure | 319 | 92% | +76.95 | +2.5% | 1.42 | 1.22 | +46 | +31 | 93% | 0.0761 | 0.0779 |
| Vol x0.5, against the 24h trend | 823 | 79% | +68.77 | +0.9% | 0.44 | 0.82 | -178 | +247 | 93% | 0.1858 | 0.1651 |
| Long-shot fade (no model) | 1297 | 96% | +68.19 | +0.5% | 1.01 | 1.01 | -48 | +116 | – | – | 0.035 |
| Vol x0.5, against trend + skip spikes | 578 | 80% | +61.92 | +1.1% | 0.49 | 0.68 | -78 | +140 | 93% | 0.1784 | 0.1592 |
| Combined: rolling best (past 6 months) | 302 | 80% | +61.71 | +2.1% | 0.75 | -0.08 | -56 | +117 | 92% | 0.1654 | 0.1523 |
| Vol x0.5, skip news in window | 1750 | 78% | +58.29 | +0.3% | 0.26 | 0.39 | -301 | +360 | 93% | 0.1897 | 0.1672 |
| Vol x0.5, skip news days | 1669 | 78% | +46.91 | +0.3% | 0.21 | 0.34 | -288 | +335 | 93% | 0.1894 | 0.1667 |
| Vol x0.5, news days only | 105 | 78% | +30.78 | +3.0% | 0.58 | 0.56 | -1 | +32 | 93% | 0.1865 | 0.1727 |
| Vol x0.5, with the 24h trend | 951 | 78% | +8.92 | +0.1% | 0.07 | -0.42 | -111 | +119 | 93% | 0.1921 | 0.1688 |
| Bayes: market prior + full vol | 3 | 67% | -6.07 | -20.9% | -0.53 | -0.69 | +2 | -8 | 92% | 0.2927 | 0.2732 |
| Vol x0.5, busy market only | 732 | 76% | -9.73 | -0.1% | -0.08 | -0.08 | -216 | +206 | 93% | 0.206 | 0.1766 |
| Bayes: market prior + fat-tail | 14 | 57% | -37.12 | -26.9% | -1.51 | -1.2 | -18 | -19 | 86% | 0.3377 | 0.2814 |
| Fat-tail, moves x0.5 | 1864 | 73% | -69.36 | -0.4% | -0.27 | -0.34 | -225 | +156 | 89% | 0.223 | 0.1956 |
| Vol x0.5, weekdays only | 1536 | 77% | -85.06 | -0.6% | -0.41 | -0.41 | -307 | +222 | 93% | 0.1997 | 0.1733 |
| Fat-tail, moves x0.75 | 1176 | 73% | -164.66 | -1.4% | -0.75 | -0.7 | -205 | +40 | 86% | 0.2074 | 0.1904 |
| Vol x0.5, stop loss 25c | 1774 | 65% | -432.90 | -2.5% | -2.36 | -2.52 | -734 | +301 | 93% | 0.3048 | 0.2342 |
| Vol x0.75 | 793 | 72% | -500.18 | -6.4% | -2.26 | -2.64 | -336 | -164 | 85% | 0.1715 | 0.154 |
| Fat-tail (actual past moves) | 635 | 59% | -619.79 | -9.8% | -1.94 | -1.32 | -550 | -69 | 73% | 0.1995 | 0.1797 |
| Heavy-volume move: follow | 1234 | 62% | -644.48 | -5.2% | -2.01 | -1.31 | -568 | -77 | – | – | 0.1842 |
| Vol x0.5, take profit 10c | 1774 | 81% | -698.42 | -4.0% | -3.62 | -3.23 | -667 | -32 | 93% | 0.1649 | 0.1546 |
| Heavy-volume move (10c, 5x): follow | 734 | 60% | -848.66 | -11.6% | -3.88 | -2.88 | -483 | -366 | – | – | 0.1835 |
| Combined: 5+ strategies agree | 2257 | 71% | -1001.32 | -4.5% | -2.36 | -3.33 | -990 | -11 | 84% | 0.1749 | 0.156 |
| Vol x0.5, stop loss 10c | 1774 | 47% | -1019.71 | -5.9% | -6.78 | -6.78 | -1066 | +46 | 93% | 0.4593 | 0.3255 |
| Vol x0.5, take profit 15c / stop 15c | 1774 | 57% | -1083.62 | -6.2% | -7.37 | -7.5 | -1080 | -3 | 93% | 0.3714 | 0.2754 |
| v1 + 50% market blend | 289 | 31% | -1122.44 | -37.8% | -4.09 | -3.89 | -631 | -491 | 42% | 0.1109 | 0.099 |
| Options vol x0.85, 5c gap | 812 | 56% | -1189.72 | -14.6% | -2.97 | -2.7 | -690 | -499 | 65% | 0.1222 | 0.1112 |
| Heavy-volume move (10c, 5x): fade | 780 | 37% | -1271.25 | -15.9% | -3.16 | -3.15 | -646 | -625 | – | – | 0.1741 |
| v1 (what we ran live) | 452 | 38% | -1373.77 | -29.8% | -3.9 | -3.5 | -971 | -403 | 54% | 0.1268 | 0.0991 |
| Options vol, 8c gap | 417 | 24% | -1407.48 | -32.5% | -3.39 | -2.69 | -1035 | -372 | 40% | 0.1092 | 0.0821 |
| Options vol, NO only | 593 | 31% | -1740.72 | -28.5% | -3.73 | -3.32 | -1388 | -353 | 45% | 0.123 | 0.102 |
| Vol x0.5, limit order | 953 | 60% | -1753.36 | -19.1% | -8.81 | -9.2 | -1107 | -647 | 92% | 0.3435 | 0.255 |
| Vol x0.5, limit order (strict fill) | 917 | 58% | -1870.33 | -21.1% | -9.52 | -9.71 | -1141 | -729 | 92% | 0.3568 | 0.2625 |
| Vol x0.5 5c edge, limit order | 1043 | 60% | -1999.45 | -19.8% | -9.56 | -9.92 | -1232 | -768 | 91% | 0.3357 | 0.2515 |
| Options vol, 5c gap | 683 | 31% | -2135.23 | -30.3% | -4.53 | -4.43 | -1300 | -835 | 44% | 0.1128 | 0.0924 |
| Heavy-volume move: fade | 1287 | 35% | -2234.48 | -16.9% | -4.22 | -4.39 | -854 | -1380 | – | – | 0.1768 |
| Combined: 3+ strategies agree | 3304 | 65% | -2565.46 | -7.8% | -4.41 | -4.96 | -2016 | -549 | 82% | 0.173 | 0.1558 |
| Kalshi price-spike fade (no model) | 1244 | 30% | -3166.29 | -24.7% | -5.94 | -5.58 | -1611 | -1555 | – | – | 0.1519 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Vol x0.5, weekends only | 141 | +56.47 | +4.1% |
| Vol x0.5, news days only | 28 | +6.46 | +2.4% |
| Bayes: market prior + full vol | 3 | -6.07 | -20.9% |
| Bayes price-level, 99% sure | 36 | -10.20 | -3.0% |
| Combined: rolling best (past 6 months) | 181 | -17.12 | -1.0% |
| Bayes: market prior + fat-tail | 14 | -37.12 | -26.9% |
| Bayes price-level, 95% sure | 119 | -55.37 | -4.9% |
| Long-shot fade (no model) | 487 | -72.52 | -1.6% |
| Vol x0.5, against trend + skip spikes | 356 | -75.63 | -2.2% |
| Vol x0.5, calm market only | 595 | -79.49 | -1.4% |
| Time-of-day vol x0.5, against trend + skip spikes | 266 | -102.10 | -3.9% |
| Vol x0.5, with the 24h trend | 544 | -132.77 | -2.5% |
| Time-of-day vol x0.5 | 770 | -134.42 | -1.8% |
| Fat-tail, moves x0.5 | 1077 | -153.09 | -1.5% |
| Vol x0.5, against the 24h trend | 491 | -158.03 | -3.3% |
| Time-of-day vol x0.5, skip spikes | 482 | -159.93 | -3.4% |
| Regime-scaled vol x0.5 | 1116 | -173.17 | -1.6% |
| Vol x0.5, skip spiked markets | 651 | -189.21 | -3.0% |
| Vol x0.5, busy market only | 440 | -211.31 | -4.9% |
| Fat-tail, moves x0.75 | 671 | -220.21 | -3.3% |
| Vol x0.5 | 1035 | -290.80 | -2.9% |
| Vol x0.5, skip news days | 1007 | -297.26 | -3.0% |
| Vol x0.5, skip news in window | 1031 | -308.44 | -3.1% |
| Vol x0.5, weekdays only | 894 | -347.27 | -4.0% |
| Vol x0.75 | 478 | -381.95 | -8.2% |
| v1 + 50% market blend | 98 | -383.34 | -38.8% |
| Heavy-volume move (10c, 5x): follow | 418 | -566.26 | -13.6% |
| Heavy-volume move: follow | 641 | -606.88 | -9.5% |
| Fat-tail (actual past moves) | 347 | -613.41 | -17.9% |
| Options vol x0.85, 5c gap | 391 | -679.92 | -17.4% |
| v1 (what we ran live) | 201 | -707.84 | -34.9% |
| Vol x0.5, take profit 10c | 1035 | -710.01 | -7.0% |
| Heavy-volume move (10c, 5x): fade | 456 | -714.38 | -15.3% |
| Vol x0.5, stop loss 25c | 1035 | -745.19 | -7.4% |
| Options vol, 8c gap | 182 | -761.37 | -40.6% |
| Options vol, NO only | 241 | -879.70 | -35.7% |
| Combined: 5+ strategies agree | 1240 | -964.92 | -7.9% |
| Heavy-volume move: fade | 684 | -993.84 | -14.2% |
| Options vol, 5c gap | 303 | -1022.87 | -32.9% |
| Vol x0.5, stop loss 10c | 1035 | -1109.95 | -11.0% |
| Vol x0.5, take profit 15c / stop 15c | 1035 | -1151.01 | -11.4% |
| Vol x0.5, limit order | 564 | -1292.34 | -23.7% |
| Vol x0.5, limit order (strict fill) | 546 | -1351.26 | -25.6% |
| Vol x0.5 5c edge, limit order | 606 | -1417.97 | -24.2% |
| Kalshi price-spike fade (no model) | 709 | -1905.83 | -26.0% |
| Combined: 3+ strategies agree | 1761 | -1962.31 | -11.3% |

Sweep: vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1972 | +60.19 | +0.3% |
| 0.5 | 1774 | +77.69 | +0.4% |
| 0.6 | 1404 | -246.88 | -1.8% |
| 0.75 | 793 | -500.18 | -6.4% |
| 1.0 | 452 | -1373.77 | -29.8% |
| 1.25 | 548 | -2406.03 | -41.9% |

Sweep: options vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 1594 | -225.84 | -1.5% |
| 0.7 | 1283 | -733.60 | -5.8% |
| 0.8 | 944 | -878.50 | -9.3% |
| 0.9 | 743 | -1599.00 | -21.2% |
| 1.0 | 683 | -2135.23 | -30.3% |
| 1.1 | 755 | -2904.97 | -36.9% |

Sweep: time-of-day vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1964 | +67.42 | +0.4% |
| 0.5 | 1544 | +309.27 | +2.1% |
| 0.6 | 1030 | +290.11 | +2.9% |
| 0.75 | 423 | -19.01 | -0.5% |
| 1.0 | 324 | -1069.50 | -32.0% |

Sweep: fat-tail

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 2062 | -76.90 | -0.4% |
| 0.5 | 1864 | -69.36 | -0.4% |
| 0.6 | 1623 | +20.05 | +0.1% |
| 0.75 | 1176 | -164.66 | -1.4% |
| 0.9 | 790 | -618.25 | -7.9% |
| 1.0 | 635 | -619.79 | -9.8% |

Rolling best: which strategy it picked each quarter

| Quarter | Picked | Past t |
|---|---|---|
| 2025-Q1 | sat out | – |
| 2025-Q2 | sat out | – |
| 2025-Q3 | Vol x0.5, with the 24h trend | 0.44 |
| 2025-Q4 | sat out | – |
| 2026-Q1 | Vol x0.5, weekends only | 0.02 |
| 2026-Q2 | Vol x0.5, weekends only | 2.23 |
| 2026-Q3 | Vol x0.5, weekends only | 4.04 |
| 2026-Q4 | Time-of-day vol x0.5, against trend + skip spikes | 3.85 |

Volatility check: real moves vs the 30-day volatility assumed (1.0 = right, 0.5 = moved half as much)

| Quarter | Events | Ratio |
|---|---|---|
| 2025-Q1 | 20 | 0.364 |
| 2025-Q2 | 182 | 1.377 |
| 2025-Q3 | 184 | 1.255 |
| 2025-Q4 | 176 | 1.288 |
| 2026-Q1 | 180 | 1.329 |
| 2026-Q2 | 182 | 0.994 |
| 2026-Q3 | 184 | 1.018 |
| 2026-Q4 | 90 | 1.268 |

Why: v1 (what we ran live)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 6 | -63 | 0% |
| Quarter | 2025-Q2 | 45 | -142 | 56% |
| Quarter | 2025-Q3 | 37 | -139 | 51% |
| Quarter | 2025-Q4 | 46 | -209 | 37% |
| Quarter | 2026-Q1 | 79 | -281 | 47% |
| Quarter | 2026-Q2 | 92 | +22 | 46% |
| Quarter | 2026-Q3 | 96 | -663 | 12% |
| Quarter | 2026-Q4 | 51 | +101 | 39% |
| Price paid | 0.00-0.10 | 65 | -414 | 3% |
| Price paid | 0.10-0.30 | 196 | -996 | 8% |
| Price paid | 0.30-0.50 | 3 | -9 | 33% |
| Price paid | 0.50-0.70 | 11 | +14 | 73% |
| Price paid | 0.70-0.90 | 176 | +29 | 82% |
| Price paid | 0.90-1.01 | 1 | +1 | 100% |
| Model vs market gap | 0.05-0.10 | 21 | +189 | 57% |
| Model vs market gap | 0.10-0.20 | 393 | -1291 | 38% |
| Model vs market gap | 0.20-0.35 | 38 | -272 | 24% |
| Side | no | 292 | -818 | 38% |
| Side | yes | 160 | -556 | 38% |

Why: Vol x0.5

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 9 | +7 | 89% |
| Quarter | 2025-Q2 | 245 | -2 | 78% |
| Quarter | 2025-Q3 | 271 | -151 | 74% |
| Quarter | 2025-Q4 | 274 | -143 | 75% |
| Quarter | 2026-Q1 | 298 | +21 | 77% |
| Quarter | 2026-Q2 | 298 | +186 | 82% |
| Quarter | 2026-Q3 | 250 | +76 | 81% |
| Quarter | 2026-Q4 | 129 | +84 | 81% |
| Price paid | 0.00-0.10 | 2 | -21 | 0% |
| Price paid | 0.10-0.30 | 3 | -32 | 0% |
| Price paid | 0.30-0.50 | 2 | +1 | 50% |
| Price paid | 0.50-0.70 | 206 | +157 | 73% |
| Price paid | 0.70-0.90 | 1552 | -26 | 79% |
| Price paid | 0.90-1.01 | 9 | -2 | 89% |
| Model vs market gap | 0.05-0.10 | 15 | -12 | 80% |
| Model vs market gap | 0.10-0.20 | 1236 | +18 | 80% |
| Model vs market gap | 0.20-0.35 | 522 | +67 | 74% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 995 | +40 | 78% |
| Side | yes | 779 | +38 | 79% |

Why: Vol x0.5, weekends only

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 2 | +5 | 100% |
| Quarter | 2025-Q2 | 17 | -11 | 71% |
| Quarter | 2025-Q3 | 37 | -6 | 81% |
| Quarter | 2025-Q4 | 43 | +7 | 81% |
| Quarter | 2026-Q1 | 52 | +90 | 90% |
| Quarter | 2026-Q2 | 48 | +70 | 90% |
| Quarter | 2026-Q3 | 19 | -23 | 74% |
| Quarter | 2026-Q4 | 20 | +31 | 90% |
| Price paid | 0.00-0.10 | 2 | -21 | 0% |
| Price paid | 0.10-0.30 | 3 | -32 | 0% |
| Price paid | 0.30-0.50 | 1 | -10 | 0% |
| Price paid | 0.50-0.70 | 25 | +96 | 92% |
| Price paid | 0.70-0.90 | 201 | +134 | 86% |
| Price paid | 0.90-1.01 | 6 | -5 | 83% |
| Model vs market gap | 0.05-0.10 | 5 | -17 | 60% |
| Model vs market gap | 0.10-0.20 | 190 | +126 | 86% |
| Model vs market gap | 0.20-0.35 | 42 | +50 | 81% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 148 | +184 | 88% |
| Side | yes | 90 | -21 | 79% |

Why: Kalshi price-spike fade (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 18 | -67 | 28% |
| Quarter | 2025-Q2 | 185 | -404 | 28% |
| Quarter | 2025-Q3 | 166 | -575 | 22% |
| Quarter | 2025-Q4 | 188 | -821 | 23% |
| Quarter | 2026-Q1 | 191 | -308 | 32% |
| Quarter | 2026-Q2 | 195 | -521 | 33% |
| Quarter | 2026-Q3 | 201 | -309 | 38% |
| Quarter | 2026-Q4 | 100 | -161 | 33% |
| Price paid | 0.10-0.30 | 691 | -2990 | 12% |
| Price paid | 0.30-0.50 | 295 | -434 | 35% |
| Price paid | 0.50-0.70 | 185 | +139 | 65% |
| Price paid | 0.70-0.90 | 73 | +119 | 89% |
| Model vs market gap | no model | 1244 | -3166 | 30% |
| Side | no | 605 | -1299 | 42% |
| Side | yes | 639 | -1868 | 18% |

Why: Time-of-day vol x0.5, against trend + skip spikes

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 4 | +11 | 100% |
| Quarter | 2025-Q2 | 39 | -9 | 77% |
| Quarter | 2025-Q3 | 67 | -6 | 79% |
| Quarter | 2025-Q4 | 87 | -112 | 69% |
| Quarter | 2026-Q1 | 87 | +58 | 85% |
| Quarter | 2026-Q2 | 103 | +155 | 91% |
| Quarter | 2026-Q3 | 77 | +58 | 86% |
| Quarter | 2026-Q4 | 44 | +3 | 80% |
| Price paid | 0.10-0.30 | 1 | -11 | 0% |
| Price paid | 0.50-0.70 | 38 | +29 | 74% |
| Price paid | 0.70-0.90 | 464 | +156 | 83% |
| Price paid | 0.90-1.01 | 5 | -17 | 60% |
| Model vs market gap | 0.05-0.10 | 12 | -4 | 83% |
| Model vs market gap | 0.10-0.20 | 424 | +132 | 82% |
| Model vs market gap | 0.20-0.35 | 72 | +30 | 78% |
| Side | no | 285 | +118 | 83% |
| Side | yes | 223 | +40 | 81% |

Why: Time-of-day vol x0.5

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 6 | +16 | 100% |
| Quarter | 2025-Q2 | 118 | -2 | 78% |
| Quarter | 2025-Q3 | 185 | -15 | 80% |
| Quarter | 2025-Q4 | 248 | -157 | 74% |
| Quarter | 2026-Q1 | 277 | +78 | 80% |
| Quarter | 2026-Q2 | 298 | +193 | 84% |
| Quarter | 2026-Q3 | 258 | +127 | 83% |
| Quarter | 2026-Q4 | 154 | +71 | 82% |
| Price paid | 0.10-0.30 | 2 | -21 | 0% |
| Price paid | 0.30-0.50 | 2 | +1 | 50% |
| Price paid | 0.50-0.70 | 131 | +124 | 74% |
| Price paid | 0.70-0.90 | 1401 | +220 | 81% |
| Price paid | 0.90-1.01 | 8 | -14 | 75% |
| Model vs market gap | 0.05-0.10 | 22 | -1 | 86% |
| Model vs market gap | 0.10-0.20 | 1257 | +178 | 81% |
| Model vs market gap | 0.20-0.35 | 264 | +128 | 77% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 885 | +253 | 81% |
| Side | yes | 659 | +57 | 80% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 93 | -18 | 91% |
| Quarter | 2025-Q3 | 21 | -41 | 71% |
| Quarter | 2025-Q4 | 4 | +2 | 75% |
| Quarter | 2026-Q1 | 7 | +10 | 100% |
| Quarter | 2026-Q2 | 140 | +32 | 91% |
| Quarter | 2026-Q3 | 238 | +115 | 94% |
| Quarter | 2026-Q4 | 150 | +41 | 92% |
| Price paid | 0.50-0.70 | 3 | +21 | 100% |
| Price paid | 0.70-0.90 | 182 | +113 | 90% |
| Price paid | 0.90-1.01 | 468 | +8 | 93% |
| Model vs market gap | 0.00-0.05 | 422 | +69 | 93% |
| Model vs market gap | 0.05-0.10 | 213 | +56 | 90% |
| Model vs market gap | 0.10-0.20 | 18 | +16 | 94% |
| Side | no | 263 | +78 | 94% |
| Side | yes | 390 | +63 | 91% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 139 | -79 | 74% |
| Quarter | 2026-Q1 | 52 | +90 | 90% |
| Quarter | 2026-Q2 | 48 | +70 | 90% |
| Quarter | 2026-Q3 | 19 | -23 | 74% |
| Quarter | 2026-Q4 | 44 | +3 | 80% |
| Price paid | 0.00-0.10 | 2 | -21 | 0% |
| Price paid | 0.10-0.30 | 2 | -21 | 0% |
| Price paid | 0.30-0.50 | 1 | -10 | 0% |
| Price paid | 0.50-0.70 | 36 | +68 | 81% |
| Price paid | 0.70-0.90 | 258 | +54 | 82% |
| Price paid | 0.90-1.01 | 3 | -8 | 67% |
| Model vs market gap | 0.05-0.10 | 11 | -18 | 73% |
| Model vs market gap | 0.10-0.20 | 222 | +90 | 83% |
| Model vs market gap | 0.20-0.35 | 68 | -15 | 72% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 165 | +100 | 82% |
| Side | yes | 137 | -38 | 77% |

## Weather: daily highs: late entries

2695 events, 2025-03-21 to 2026-11-15.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Late long-shot fade 1-4c (+49 on 969 trades).

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Late long-shot fade 1-4c | 969 | 99% | +48.52 | +0.5% | 1.73 | 1.81 | -6 | +55 | – | – | 0.0084 |
| Combined: 3+ strategies agree | 683 | 81% | +26.13 | +0.4% | 0.19 | 0.25 | +57 | -31 | 92% | 0.1687 | 0.1488 |
| Late favorite 90-97c | 823 | 95% | +8.78 | +0.1% | 0.14 | 0.14 | -4 | +13 | – | – | 0.0487 |
| Bayes price-level, 99% sure | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Late long-shot fade | 743 | 95% | -11.86 | -0.2% | -0.2 | -0.37 | -36 | +24 | – | – | 0.0437 |
| Bayes price-level, 95% sure | 64 | 84% | -34.18 | -5.4% | -1.07 | -0.52 | -9 | -26 | 93% | 0.1359 | 0.1269 |
| Combined: rolling best (past 6 months) | 548 | 97% | -39.73 | -0.7% | -1.02 | -1.06 | -66 | +26 | – | – | 0.0279 |
| Late favorite 80-90c | 438 | 86% | -48.57 | -1.1% | -0.59 | -0.59 | -1 | -47 | – | – | 0.1226 |
| Combined: 5+ strategies agree | 438 | 86% | -48.57 | -1.1% | -0.59 | -0.59 | -1 | -47 | – | – | 0.1226 |
| Late fav 80-90c, stop loss 25c | 438 | 82% | -84.50 | -2.0% | -1.06 | -1.06 | -28 | -56 | – | – | 0.1461 |
| Late fav 80-90c, stop loss 10c | 438 | 78% | -95.77 | -2.2% | -1.26 | -1.26 | -28 | -67 | – | – | 0.1729 |
| Late fav 80-90c, take profit 15c / stop 15c | 438 | 80% | -114.98 | -2.7% | -1.48 | -1.48 | -47 | -68 | – | – | 0.1587 |
| Late fav 80-90c, take profit 10c | 438 | 86% | -120.24 | -2.8% | -1.5 | -1.5 | -30 | -90 | – | – | 0.1214 |
| Late favorite 50-80c | 548 | 67% | -168.69 | -3.1% | -1.04 | -1.04 | -103 | -65 | – | – | 0.2136 |
| Heavy-volume move (10c, 5x): follow | 851 | 72% | -464.52 | -5.5% | -2.37 | -2.15 | -355 | -109 | – | – | 0.1655 |
| Heavy-volume move: follow | 1320 | 69% | -493.85 | -3.8% | -1.61 | -0.97 | -518 | +24 | – | – | 0.1685 |
| Heavy-volume move (10c, 5x): fade | 1014 | 25% | -2263.32 | -21.5% | -4.1 | -3.97 | -831 | -1432 | – | – | 0.149 |
| Heavy-volume move: fade | 1591 | 26% | -3708.75 | -22.5% | -5.5 | -5.18 | -2188 | -1521 | – | – | 0.1498 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Combined: 3+ strategies agree | 214 | +9.94 | +0.5% |
| Late long-shot fade 1-4c | 377 | +7.88 | +0.2% |
| Bayes price-level, 99% sure | 0 | +0.00 | – |
| Late favorite 90-97c | 341 | -10.77 | -0.3% |
| Bayes price-level, 95% sure | 19 | -13.67 | -7.4% |
| Late favorite 80-90c | 157 | -16.87 | -1.1% |
| Combined: 5+ strategies agree | 157 | -16.87 | -1.1% |
| Late fav 80-90c, take profit 10c | 157 | -30.92 | -2.0% |
| Late fav 80-90c, stop loss 25c | 157 | -46.55 | -3.0% |
| Late fav 80-90c, stop loss 10c | 157 | -49.18 | -3.2% |
| Late long-shot fade | 237 | -53.63 | -2.4% |
| Late fav 80-90c, take profit 15c / stop 15c | 157 | -56.64 | -3.7% |
| Combined: rolling best (past 6 months) | 198 | -73.11 | -3.8% |
| Late favorite 50-80c | 169 | -113.02 | -6.8% |
| Heavy-volume move (10c, 5x): follow | 242 | -190.46 | -8.0% |
| Heavy-volume move: follow | 374 | -308.00 | -8.3% |
| Heavy-volume move (10c, 5x): fade | 320 | -861.38 | -25.9% |
| Heavy-volume move: fade | 507 | -1428.70 | -27.2% |

Rolling best: which strategy it picked each quarter

| Quarter | Picked | Past t |
|---|---|---|
| 2025-Q1 | sat out | – |
| 2025-Q2 | sat out | – |
| 2025-Q3 | Late long-shot fade 1-4c | 25.46 |
| 2025-Q4 | Late long-shot fade 1-4c | 29.08 |
| 2026-Q1 | Late long-shot fade | 0.17 |
| 2026-Q2 | sat out | – |
| 2026-Q3 | Late long-shot fade 1-4c | 1.41 |
| 2026-Q4 | Late long-shot fade 1-4c | 1.81 |

Why: Late favorite 80-90c

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 7 | -1 | 86% |
| Quarter | 2025-Q2 | 44 | +5 | 89% |
| Quarter | 2025-Q3 | 34 | -8 | 85% |
| Quarter | 2025-Q4 | 22 | -11 | 82% |
| Quarter | 2026-Q1 | 78 | -4 | 86% |
| Quarter | 2026-Q2 | 105 | +2 | 87% |
| Quarter | 2026-Q3 | 104 | -30 | 84% |
| Quarter | 2026-Q4 | 44 | -1 | 86% |
| Price paid | 0.70-0.90 | 384 | -60 | 85% |
| Price paid | 0.90-1.01 | 54 | +12 | 93% |
| Model vs market gap | no model | 438 | -49 | 86% |
| Side | yes | 438 | -49 | 86% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 3 | +2 | 100% |
| Quarter | 2025-Q3 | 9 | -24 | 67% |
| Quarter | 2026-Q1 | 9 | +10 | 100% |
| Quarter | 2026-Q2 | 17 | -23 | 76% |
| Quarter | 2026-Q3 | 17 | +2 | 88% |
| Quarter | 2026-Q4 | 9 | -2 | 89% |
| Price paid | 0.50-0.70 | 2 | -2 | 50% |
| Price paid | 0.70-0.90 | 10 | -18 | 70% |
| Price paid | 0.90-1.01 | 52 | -14 | 88% |
| Model vs market gap | 0.00-0.05 | 24 | +3 | 92% |
| Model vs market gap | 0.05-0.10 | 35 | -28 | 83% |
| Model vs market gap | 0.10-0.20 | 5 | -9 | 60% |
| Side | no | 19 | -19 | 79% |
| Side | yes | 45 | -15 | 87% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 47 | +5 | 100% |
| Quarter | 2025-Q4 | 38 | -25 | 92% |
| Quarter | 2026-Q1 | 172 | -48 | 93% |
| Quarter | 2026-Q3 | 216 | +19 | 100% |
| Quarter | 2026-Q4 | 75 | +9 | 100% |
| Price paid | 0.90-1.01 | 548 | -40 | 97% |
| Model vs market gap | no model | 548 | -40 | 97% |
| Side | no | 548 | -40 | 97% |

## Weather: daily lows: late entries

1839 events, 2025-12-13 to 2026-11-15.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Heavy-volume move: fade (+409 on 742 trades).

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Heavy-volume move: fade | 742 | 35% | +409.27 | +5.3% | 0.75 | 0.67 | +424 | -15 | – | – | 0.1654 |
| Heavy-volume move (10c, 5x): fade | 328 | 30% | +86.31 | +2.5% | 0.23 | -0.41 | +134 | -48 | – | – | 0.1604 |
| Bayes price-level, 99% sure | 10 | 60% | +41.84 | +40.6% | 1.07 | 1.07 | +22 | +20 | 58% | 0.2435 | 0.2878 |
| Bayes price-level, 95% sure | 34 | 44% | -14.21 | -4.1% | -0.22 | -0.19 | -24 | +10 | 60% | 0.2982 | 0.2876 |
| Combined: rolling best (past 6 months) | 323 | 32% | -21.36 | -0.6% | -0.05 | -0.26 | -514 | +492 | – | – | 0.1608 |
| Late favorite 90-97c | 886 | 94% | -82.19 | -1.0% | -1.18 | -1.18 | -45 | -37 | – | – | 0.0546 |
| Late long-shot fade 1-4c | 1868 | 98% | -212.14 | -1.1% | -3.17 | -2.96 | -145 | -67 | – | – | 0.024 |
| Late favorite 80-90c | 368 | 82% | -213.17 | -5.9% | -2.57 | -2.57 | -112 | -101 | – | – | 0.147 |
| Combined: 5+ strategies agree | 368 | 82% | -213.17 | -5.9% | -2.57 | -2.57 | -112 | -101 | – | – | 0.147 |
| Late fav 80-90c, take profit 10c | 368 | 82% | -260.87 | -7.3% | -3.23 | -3.23 | -133 | -127 | – | – | 0.1451 |
| Combined: 3+ strategies agree | 422 | 79% | -262.03 | -6.3% | -2.61 | -2.74 | -166 | -96 | 55% | 0.1882 | 0.1609 |
| Heavy-volume move (10c, 5x): follow | 241 | 65% | -283.01 | -11.8% | -2.25 | -1.81 | -197 | -86 | – | – | 0.1718 |
| Late long-shot fade | 1347 | 93% | -362.83 | -2.8% | -3.9 | -3.65 | -276 | -87 | – | – | 0.0635 |
| Late fav 80-90c, stop loss 25c | 368 | 62% | -410.54 | -11.4% | -6.02 | -6.02 | -242 | -168 | – | – | 0.2859 |
| Late fav 80-90c, stop loss 10c | 368 | 39% | -436.54 | -12.1% | -8.55 | -8.55 | -250 | -186 | – | – | 0.4378 |
| Late fav 80-90c, take profit 15c / stop 15c | 368 | 48% | -438.55 | -12.2% | -7.8 | -7.8 | -250 | -189 | – | – | 0.3758 |
| Late favorite 50-80c | 429 | 58% | -640.75 | -15.1% | -4.18 | -4.18 | -225 | -416 | – | – | 0.2372 |
| Heavy-volume move: follow | 579 | 57% | -1159.56 | -20.1% | -5.56 | -5.37 | -557 | -603 | – | – | 0.1761 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Heavy-volume move: fade | 145 | +171.93 | +11.5% |
| Bayes price-level, 95% sure | 0 | +0.00 | – |
| Bayes price-level, 99% sure | 0 | +0.00 | – |
| Combined: rolling best (past 6 months) | 0 | +0.00 | – |
| Late favorite 50-80c | 66 | -26.78 | -4.1% |
| Late favorite 90-97c | 162 | -32.68 | -2.1% |
| Late long-shot fade 1-4c | 365 | -36.90 | -1.0% |
| Combined: 3+ strategies agree | 64 | -52.53 | -8.4% |
| Late favorite 80-90c | 58 | -59.55 | -10.5% |
| Combined: 5+ strategies agree | 58 | -59.55 | -10.5% |
| Late fav 80-90c, take profit 10c | 58 | -70.59 | -12.5% |
| Heavy-volume move (10c, 5x): follow | 42 | -82.86 | -19.9% |
| Late fav 80-90c, take profit 15c / stop 15c | 58 | -103.31 | -18.3% |
| Late fav 80-90c, stop loss 25c | 58 | -105.82 | -18.7% |
| Late long-shot fade | 258 | -108.97 | -4.4% |
| Late fav 80-90c, stop loss 10c | 58 | -114.36 | -20.3% |
| Heavy-volume move (10c, 5x): fade | 60 | -131.84 | -21.1% |
| Heavy-volume move: follow | 108 | -320.53 | -29.8% |

Rolling best: which strategy it picked each quarter

| Quarter | Picked | Past t |
|---|---|---|
| 2025-Q4 | sat out | – |
| 2026-Q1 | sat out | – |
| 2026-Q2 | sat out | – |
| 2026-Q3 | Heavy-volume move: fade | 0.95 |
| 2026-Q4 | Heavy-volume move: fade | 0.92 |

Why: Late favorite 80-90c

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q4 | 3 | -7 | 67% |
| Quarter | 2026-Q1 | 73 | -36 | 82% |
| Quarter | 2026-Q2 | 102 | -43 | 83% |
| Quarter | 2026-Q3 | 145 | -111 | 81% |
| Quarter | 2026-Q4 | 45 | -17 | 84% |
| Price paid | 0.70-0.90 | 327 | -200 | 81% |
| Price paid | 0.90-1.01 | 41 | -13 | 88% |
| Model vs market gap | no model | 368 | -213 | 82% |
| Side | yes | 368 | -213 | 82% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q2 | 6 | -61 | 0% |
| Quarter | 2026-Q3 | 20 | +18 | 50% |
| Quarter | 2026-Q4 | 8 | +29 | 62% |
| Price paid | 0.30-0.50 | 24 | +37 | 50% |
| Price paid | 0.50-0.70 | 7 | -22 | 43% |
| Price paid | 0.70-0.90 | 3 | -30 | 0% |
| Model vs market gap | 0.05-0.10 | 2 | -20 | 0% |
| Model vs market gap | 0.10-0.20 | 24 | -10 | 46% |
| Model vs market gap | 0.20-0.35 | 8 | +15 | 50% |
| Side | no | 31 | +16 | 48% |
| Side | yes | 3 | -30 | 0% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q3 | 224 | -257 | 31% |
| Quarter | 2026-Q4 | 99 | +236 | 35% |
| Price paid | 0.10-0.30 | 217 | -215 | 16% |
| Price paid | 0.30-0.50 | 50 | +170 | 54% |
| Price paid | 0.50-0.70 | 20 | +28 | 70% |
| Price paid | 0.70-0.90 | 33 | -8 | 79% |
| Price paid | 0.90-1.01 | 3 | +3 | 100% |
| Model vs market gap | no model | 323 | -21 | 32% |
| Side | no | 200 | -69 | 36% |
| Side | yes | 123 | +48 | 27% |

## Bitcoin: last 1-3 hours

603 events, 2025-03-22 to 2026-11-15.

**Verdict:** Late long-shot fade 1-4c: +90 on 891 trades (+1.0% per $ staked, t=6.35), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bayes price-level, 95% sure | 932 | 92% | +202.32 | +2.2% | 2.23 | 2.48 | +61 | +142 | 94% | 0.0699 | 0.071 |
| Bayes price-level, 99% sure | 542 | 95% | +200.04 | +3.8% | 3.44 | 3.06 | +109 | +91 | 96% | 0.0494 | 0.0523 |
| Combined: rolling best (past 6 months) | 748 | 97% | +137.63 | +1.9% | 2.6 | 2.0 | +22 | +115 | 94% | 0.0646 | 0.0307 |
| Late long-shot fade | 751 | 97% | +110.32 | +1.5% | 2.48 | 1.97 | +43 | +67 | – | – | 0.0282 |
| Late long-shot fade 1-4c | 891 | 100% | +90.25 | +1.0% | 6.35 | 5.94 | +37 | +53 | – | – | 0.0026 |
| Combined: 3+ strategies agree | 256 | 90% | +89.56 | +3.6% | 1.57 | 1.62 | +5 | +85 | 90% | 0.0928 | 0.0909 |
| Late favorite 90-97c | 201 | 96% | +22.63 | +1.2% | 0.85 | 0.85 | +29 | -6 | – | – | 0.0343 |
| Late favorite 80-90c | 47 | 87% | -0.31 | -0.1% | 0.01 | 0.01 | -1 | +1 | – | – | 0.1141 |
| Combined: 5+ strategies agree | 47 | 87% | -0.31 | -0.1% | 0.01 | 0.01 | -1 | +1 | – | – | 0.1141 |
| Late favorite 50-80c | 31 | 68% | -0.41 | -0.1% | 0.01 | 0.01 | -31 | +31 | – | – | 0.2216 |
| Late fav 80-90c, take profit 10c | 47 | 87% | -1.58 | -0.3% | -0.04 | -0.04 | -1 | -0 | – | – | 0.1141 |
| Late fav 80-90c, stop loss 25c | 47 | 74% | -29.82 | -6.5% | -1.1 | -1.1 | -34 | +4 | – | – | 0.2007 |
| Late fav 80-90c, stop loss 10c | 47 | 60% | -47.16 | -10.2% | -1.87 | -1.87 | -49 | +2 | – | – | 0.2943 |
| Late fav 80-90c, take profit 15c / stop 15c | 47 | 64% | -48.94 | -10.6% | -1.84 | -1.84 | -49 | -0 | – | – | 0.2697 |
| Heavy-volume move (10c, 5x): follow | 797 | 66% | -625.68 | -7.9% | -2.96 | -2.17 | -343 | -282 | – | – | 0.1771 |
| Heavy-volume move: follow | 1311 | 66% | -996.98 | -7.7% | -3.58 | -3.01 | -625 | -372 | – | – | 0.1695 |
| Heavy-volume move (10c, 5x): fade | 866 | 31% | -1821.71 | -20.4% | -4.09 | -3.97 | -1160 | -662 | – | – | 0.1655 |
| Heavy-volume move: fade | 1394 | 30% | -3517.59 | -24.5% | -6.36 | -5.49 | -2150 | -1367 | – | – | 0.1548 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Bayes price-level, 99% sure | 80 | +43.52 | +5.6% |
| Late favorite 90-97c | 168 | +38.28 | +2.4% |
| Late long-shot fade 1-4c | 153 | +18.81 | +1.2% |
| Late long-shot fade | 236 | +16.94 | +0.8% |
| Combined: rolling best (past 6 months) | 159 | +13.07 | +0.8% |
| Bayes price-level, 95% sure | 232 | -5.79 | -0.3% |
| Late favorite 80-90c | 41 | -8.95 | -2.2% |
| Combined: 5+ strategies agree | 41 | -8.95 | -2.2% |
| Late fav 80-90c, take profit 10c | 41 | -10.22 | -2.5% |
| Late favorite 50-80c | 27 | -15.37 | -5.7% |
| Combined: 3+ strategies agree | 96 | -32.67 | -3.5% |
| Late fav 80-90c, stop loss 25c | 41 | -38.46 | -9.6% |
| Late fav 80-90c, stop loss 10c | 41 | -55.80 | -13.9% |
| Late fav 80-90c, take profit 15c / stop 15c | 41 | -57.58 | -14.3% |
| Heavy-volume move (10c, 5x): follow | 377 | -322.65 | -8.7% |
| Heavy-volume move: follow | 571 | -564.38 | -10.0% |
| Heavy-volume move (10c, 5x): fade | 424 | -1101.76 | -25.2% |
| Heavy-volume move: fade | 633 | -1891.35 | -29.0% |

Rolling best: which strategy it picked each quarter

| Quarter | Picked | Past t |
|---|---|---|
| 2025-Q1 | sat out | – |
| 2025-Q2 | sat out | – |
| 2025-Q3 | Late long-shot fade | 20.4 |
| 2025-Q4 | Late long-shot fade 1-4c | 14.93 |
| 2026-Q1 | Late long-shot fade 1-4c | 19.74 |
| 2026-Q2 | Late long-shot fade 1-4c | 26.72 |
| 2026-Q3 | Bayes price-level, 99% sure | 2.52 |
| 2026-Q4 | Bayes price-level, 99% sure | 4.06 |

Why: Late favorite 80-90c

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 1 | +1 | 100% |
| Quarter | 2025-Q2 | 15 | +1 | 87% |
| Quarter | 2025-Q3 | 11 | +3 | 91% |
| Quarter | 2025-Q4 | 7 | -12 | 71% |
| Quarter | 2026-Q1 | 7 | -2 | 86% |
| Quarter | 2026-Q2 | 2 | +2 | 100% |
| Quarter | 2026-Q3 | 2 | +3 | 100% |
| Quarter | 2026-Q4 | 2 | +4 | 100% |
| Price paid | 0.70-0.90 | 39 | +2 | 87% |
| Price paid | 0.90-1.01 | 8 | -3 | 88% |
| Model vs market gap | no model | 47 | -0 | 87% |
| Side | yes | 47 | -0 | 87% |

Why: Late long-shot fade 1-4c

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 3 | +0 | 100% |
| Quarter | 2025-Q2 | 10 | +1 | 100% |
| Quarter | 2025-Q3 | 31 | +4 | 100% |
| Quarter | 2025-Q4 | 29 | +3 | 100% |
| Quarter | 2026-Q1 | 127 | +17 | 100% |
| Quarter | 2026-Q2 | 260 | +14 | 99% |
| Quarter | 2026-Q3 | 281 | +33 | 100% |
| Quarter | 2026-Q4 | 150 | +18 | 100% |
| Price paid | 0.90-1.01 | 891 | +90 | 100% |
| Model vs market gap | no model | 891 | +90 | 100% |
| Side | no | 891 | +90 | 100% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 11 | -3 | 91% |
| Quarter | 2025-Q3 | 58 | +11 | 93% |
| Quarter | 2025-Q4 | 76 | -19 | 88% |
| Quarter | 2026-Q1 | 135 | +35 | 95% |
| Quarter | 2026-Q2 | 257 | +10 | 91% |
| Quarter | 2026-Q3 | 250 | +199 | 96% |
| Quarter | 2026-Q4 | 145 | -32 | 88% |
| Price paid | 0.50-0.70 | 2 | -5 | 50% |
| Price paid | 0.70-0.90 | 390 | +143 | 87% |
| Price paid | 0.90-1.01 | 540 | +64 | 96% |
| Model vs market gap | 0.00-0.05 | 416 | +64 | 97% |
| Model vs market gap | 0.05-0.10 | 444 | +127 | 89% |
| Model vs market gap | 0.10-0.20 | 72 | +10 | 83% |
| Side | no | 156 | +41 | 91% |
| Side | yes | 776 | +162 | 92% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 50 | -0 | 96% |
| Quarter | 2025-Q4 | 29 | +3 | 100% |
| Quarter | 2026-Q1 | 127 | +17 | 100% |
| Quarter | 2026-Q2 | 260 | +14 | 99% |
| Quarter | 2026-Q3 | 181 | +141 | 96% |
| Quarter | 2026-Q4 | 101 | -37 | 87% |
| Price paid | 0.70-0.90 | 121 | +55 | 88% |
| Price paid | 0.90-1.01 | 627 | +82 | 99% |
| Model vs market gap | 0.00-0.05 | 125 | +34 | 98% |
| Model vs market gap | 0.05-0.10 | 146 | +64 | 90% |
| Model vs market gap | 0.10-0.20 | 11 | +6 | 82% |
| Model vs market gap | no model | 466 | +33 | 99% |
| Side | no | 520 | +91 | 99% |
| Side | yes | 228 | +47 | 92% |

## Ethereum

598 events, 2025-03-27 to 2026-11-15.

**Verdict:** Market favorite (no model): +109 on 114 trades (+9.6% per $ staked, t=1.23), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Time-of-day vol x0.5, skip spikes | 791 | 82% | +150.45 | +1.9% | 1.14 | 0.99 | -54 | +205 | 92% | 0.1532 | 0.1439 |
| Time-of-day vol x0.5, against trend + skip spikes | 435 | 84% | +143.13 | +3.4% | 1.5 | 1.35 | -28 | +172 | 93% | 0.1432 | 0.137 |
| Market favorite (no model) | 114 | 67% | +109.42 | +9.6% | 1.23 | 1.23 | +73 | +36 | – | – | 0.2039 |
| Time-of-day vol x0.5 | 1240 | 81% | +88.02 | +0.7% | 0.52 | 1.27 | -158 | +246 | 92% | 0.1607 | 0.1481 |
| Vol x0.5, weekends only | 154 | 82% | +65.16 | +4.3% | 0.81 | 1.03 | -5 | +71 | 92% | 0.1389 | 0.133 |
| Bayes price-level, 95% sure | 45 | 78% | +49.70 | +11.2% | 1.2 | 1.2 | +32 | +18 | 76% | 0.1589 | 0.166 |
| Vol x0.5, skip spiked markets | 925 | 80% | +16.61 | +0.2% | 0.11 | -0.37 | -212 | +229 | 93% | 0.1752 | 0.1586 |
| Bayes: market prior + full vol | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Bayes: market prior + fat-tail | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Vol x0.5, against trend + skip spikes | 503 | 80% | -10.59 | -0.2% | -0.1 | -0.25 | -164 | +154 | 93% | 0.1786 | 0.1608 |
| Long-shot fade (no model) | 608 | 95% | -21.73 | -0.4% | -0.38 | -0.28 | -90 | +68 | – | – | 0.0444 |
| Bayes price-level, 99% sure | 3 | 0% | -29.77 | -100.0% | – | – | -10 | -20 | 72% | 0.5155 | 0.3521 |
| Combined: rolling best (past 6 months) | 266 | 79% | -44.60 | -1.7% | -0.53 | -0.68 | -94 | +50 | 93% | 0.1686 | 0.1565 |
| Vol x0.5, news days only | 83 | 75% | -46.16 | -5.7% | -0.93 | -1.27 | -30 | -17 | 92% | 0.2044 | 0.1751 |
| Vol x0.75 | 404 | 76% | -62.30 | -1.6% | -0.4 | -0.6 | -170 | +108 | 88% | 0.1625 | 0.149 |
| Fat-tail (actual past moves) | 342 | 67% | -66.49 | -2.0% | -0.28 | -0.29 | -209 | +142 | 78% | 0.1883 | 0.1741 |
| Vol x0.5, calm market only | 755 | 79% | -77.34 | -1.1% | -0.51 | -0.16 | -216 | +139 | 92% | 0.1777 | 0.16 |
| Vol x0.5, 5c edge | 1710 | 79% | -87.02 | -0.5% | -0.4 | 0.05 | -371 | +284 | 92% | 0.1761 | 0.1588 |
| Vol x0.5, against the 24h trend | 705 | 78% | -93.99 | -1.4% | -0.64 | -0.74 | -279 | +185 | 93% | 0.1861 | 0.1655 |
| Vol x0.5, with the 24h trend | 727 | 78% | -124.95 | -1.8% | -0.9 | -0.96 | -119 | -6 | 92% | 0.1855 | 0.163 |
| Vol x0.5, busy market only | 677 | 78% | -141.60 | -2.1% | -1.05 | -0.86 | -153 | +11 | 93% | 0.1948 | 0.169 |
| Regime-scaled vol x0.5 | 1590 | 79% | -154.95 | -1.0% | -0.75 | 0.15 | -328 | +173 | 93% | 0.1809 | 0.1602 |
| Vol x0.5, skip news days | 1349 | 78% | -172.78 | -1.3% | -0.89 | -0.34 | -361 | +188 | 93% | 0.1847 | 0.1636 |
| Vol x0.5, NO only | 903 | 78% | -191.57 | -2.2% | -1.23 | -1.2 | -238 | +46 | 92% | 0.183 | 0.1621 |
| Vol x0.5, skip news in window | 1409 | 78% | -214.10 | -1.6% | -1.07 | -0.61 | -393 | +179 | 93% | 0.1862 | 0.1645 |
| Vol x0.5 (Bitcoin's winner) | 1432 | 78% | -218.94 | -1.6% | -1.09 | -0.71 | -383 | +164 | 93% | 0.1858 | 0.1642 |
| Fat-tail, moves x0.75 | 884 | 73% | -220.93 | -2.5% | -1.22 | -1.3 | -241 | +20 | 86% | 0.2059 | 0.1878 |
| Full vol + 50% market blend | 98 | 24% | -221.76 | -21.8% | -0.87 | -0.7 | -337 | +115 | 34% | 0.1191 | 0.108 |
| Vol x0.5, weekdays only | 1278 | 78% | -284.10 | -2.3% | -1.5 | -1.16 | -383 | +99 | 93% | 0.1915 | 0.168 |
| Fat-tail, moves x0.5 | 1716 | 74% | -349.11 | -2.1% | -1.44 | -1.29 | -384 | +35 | 90% | 0.2081 | 0.1822 |
| Options vol x0.85, 5c gap | 437 | 56% | -401.32 | -9.2% | -1.03 | -0.85 | -558 | +157 | 67% | 0.1316 | 0.1183 |
| Heavy-volume move (10c, 5x): follow | 411 | 60% | -509.54 | -12.4% | -3.09 | -2.9 | -242 | -267 | – | – | 0.1803 |
| Options vol, NO only | 216 | 27% | -513.87 | -23.0% | -1.42 | -1.16 | -596 | +82 | 42% | 0.1198 | 0.0962 |
| Options vol, 8c gap | 199 | 17% | -569.59 | -27.5% | -1.47 | -1.17 | -716 | +146 | 36% | 0.1251 | 0.0904 |
| Vol x0.5, take profit 10c | 1432 | 81% | -619.51 | -4.4% | -3.54 | -2.97 | -574 | -46 | 93% | 0.1658 | 0.1536 |
| Combined: 5+ strategies agree | 1704 | 74% | -720.74 | -4.3% | -2.14 | -1.69 | -749 | +28 | 87% | 0.1772 | 0.16 |
| Vol x0.5, stop loss 25c | 1432 | 65% | -732.21 | -5.2% | -4.23 | -3.87 | -753 | +21 | 93% | 0.3038 | 0.2367 |
| Full vol (v1 rule) | 218 | 29% | -868.35 | -38.7% | -3.14 | -2.78 | -724 | -144 | 46% | 0.1188 | 0.0883 |
| Heavy-volume move (10c, 5x): fade | 460 | 35% | -897.72 | -19.0% | -2.9 | -3.08 | -169 | -728 | – | – | 0.1638 |
| Heavy-volume move: follow | 751 | 57% | -978.04 | -13.0% | -3.86 | -3.48 | -483 | -495 | – | – | 0.1859 |
| Vol x0.5, take profit 15c / stop 15c | 1432 | 57% | -1003.30 | -7.2% | -7.35 | -6.62 | -860 | -144 | 93% | 0.3712 | 0.2813 |
| Heavy-volume move: fade | 813 | 38% | -1096.07 | -13.2% | -2.6 | -3.06 | -322 | -774 | – | – | 0.1725 |
| Vol x0.5, stop loss 10c | 1432 | 47% | -1096.32 | -7.8% | -7.56 | -7.01 | -954 | -142 | 93% | 0.4549 | 0.3315 |
| Options vol, 5c gap | 388 | 23% | -1476.45 | -36.7% | -3.44 | -3.24 | -1212 | -264 | 39% | 0.1158 | 0.0895 |
| Vol x0.5, limit order | 720 | 57% | -1703.95 | -24.5% | -9.94 | -11.26 | -1109 | -595 | 92% | 0.3568 | 0.2679 |
| Vol x0.5, limit order (strict fill) | 699 | 56% | -1756.03 | -26.0% | -10.34 | -11.62 | -1125 | -631 | 92% | 0.3674 | 0.2747 |
| Vol x0.5 5c edge, limit order | 841 | 58% | -1901.13 | -23.4% | -10.26 | -11.73 | -1235 | -666 | 91% | 0.3426 | 0.2616 |
| Combined: 3+ strategies agree | 2425 | 66% | -1933.89 | -8.1% | -3.67 | -3.22 | -1331 | -603 | 84% | 0.1717 | 0.1576 |
| Kalshi price-spike fade (no model) | 1060 | 31% | -2339.95 | -21.4% | -4.8 | -4.46 | -805 | -1535 | – | – | 0.1702 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Market favorite (no model) | 62 | +78.19 | +12.5% |
| Bayes price-level, 99% sure | 0 | +0.00 | – |
| Bayes: market prior + full vol | 0 | +0.00 | – |
| Bayes: market prior + fat-tail | 0 | +0.00 | – |
| Time-of-day vol x0.5, against trend + skip spikes | 257 | -2.57 | -0.1% |
| Bayes price-level, 95% sure | 8 | -3.04 | -3.9% |
| Vol x0.5, weekends only | 100 | -3.06 | -0.3% |
| Vol x0.5, news days only | 24 | -15.54 | -6.6% |
| Time-of-day vol x0.5, skip spikes | 467 | -49.93 | -1.1% |
| Long-shot fade (no model) | 307 | -88.63 | -3.0% |
| Combined: rolling best (past 6 months) | 157 | -89.49 | -5.8% |
| Time-of-day vol x0.5 | 742 | -106.11 | -1.5% |
| Vol x0.5, with the 24h trend | 468 | -114.09 | -2.5% |
| Vol x0.5, against trend + skip spikes | 311 | -146.47 | -4.8% |
| Vol x0.75 | 253 | -153.77 | -6.2% |
| Vol x0.5, busy market only | 452 | -186.03 | -4.2% |
| Vol x0.5, skip spiked markets | 573 | -192.83 | -3.5% |
| Fat-tail (actual past moves) | 201 | -197.99 | -10.0% |
| Full vol + 50% market blend | 33 | -208.07 | -61.7% |
| Vol x0.5, calm market only | 449 | -229.40 | -5.2% |
| Fat-tail, moves x0.75 | 563 | -239.74 | -4.3% |
| Vol x0.5, against the 24h trend | 433 | -301.34 | -7.1% |
| Vol x0.5, NO only | 613 | -312.80 | -5.2% |
| Heavy-volume move (10c, 5x): follow | 251 | -334.68 | -13.4% |
| Regime-scaled vol x0.5 | 1007 | -353.14 | -3.6% |
| Vol x0.5, 5c edge | 1082 | -364.24 | -3.5% |
| Fat-tail, moves x0.5 | 1066 | -387.84 | -3.7% |
| Vol x0.5, skip news days | 877 | -399.89 | -4.7% |
| Vol x0.5, weekdays only | 801 | -412.37 | -5.3% |
| Heavy-volume move (10c, 5x): fade | 286 | -412.75 | -14.0% |
| Vol x0.5 (Bitcoin's winner) | 901 | -415.43 | -4.7% |
| Vol x0.5, skip news in window | 897 | -428.49 | -4.9% |
| Heavy-volume move: fade | 470 | -459.06 | -9.5% |
| Heavy-volume move: follow | 427 | -504.33 | -11.8% |
| Options vol, NO only | 100 | -511.69 | -50.1% |
| Options vol, 8c gap | 78 | -558.56 | -69.4% |
| Options vol x0.85, 5c gap | 244 | -584.42 | -24.2% |
| Vol x0.5, take profit 10c | 901 | -661.20 | -7.5% |
| Full vol (v1 rule) | 105 | -682.19 | -63.4% |
| Combined: 5+ strategies agree | 1038 | -803.84 | -7.9% |
| Vol x0.5, stop loss 25c | 901 | -829.01 | -9.4% |
| Vol x0.5, take profit 15c / stop 15c | 901 | -972.57 | -11.1% |
| Vol x0.5, stop loss 10c | 901 | -1040.07 | -11.8% |
| Options vol, 5c gap | 169 | -1082.45 | -62.3% |
| Vol x0.5, limit order | 447 | -1307.40 | -30.3% |
| Kalshi price-spike fade (no model) | 678 | -1337.76 | -19.1% |
| Vol x0.5, limit order (strict fill) | 433 | -1341.46 | -32.1% |
| Vol x0.5 5c edge, limit order | 522 | -1444.87 | -28.7% |
| Combined: 3+ strategies agree | 1484 | -1631.01 | -11.1% |

Sweep: vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.3 | 2026 | -124.36 | -0.6% |
| 0.4 | 1791 | -300.82 | -1.7% |
| 0.5 | 1432 | -218.94 | -1.6% |
| 0.6 | 966 | -257.40 | -2.7% |
| 0.75 | 404 | -62.30 | -1.6% |
| 1.0 | 218 | -868.35 | -38.7% |

Sweep: time-of-day vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1696 | -22.46 | -0.1% |
| 0.5 | 1240 | +88.02 | +0.7% |
| 0.6 | 698 | -120.93 | -1.8% |
| 0.75 | 231 | -289.70 | -12.7% |
| 1.0 | 241 | -918.06 | -36.6% |

Sweep: fat-tail

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1971 | -169.27 | -0.9% |
| 0.5 | 1716 | -349.11 | -2.1% |
| 0.6 | 1379 | -160.32 | -1.2% |
| 0.75 | 884 | -220.93 | -2.5% |
| 0.9 | 502 | -227.59 | -4.6% |
| 1.0 | 342 | -66.49 | -2.0% |

Sweep: options vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 1348 | -398.13 | -3.0% |
| 0.7 | 879 | -374.41 | -4.3% |
| 0.8 | 527 | -423.68 | -8.1% |
| 0.9 | 376 | -652.37 | -17.1% |
| 1.0 | 388 | -1476.45 | -36.7% |
| 1.1 | 527 | -2872.19 | -52.0% |

Rolling best: which strategy it picked each quarter

| Quarter | Picked | Past t |
|---|---|---|
| 2025-Q1 | sat out | – |
| 2025-Q2 | sat out | – |
| 2025-Q3 | Time-of-day vol x0.5, against trend + skip spikes | 1.99 |
| 2025-Q4 | Time-of-day vol x0.5, against trend + skip spikes | 0.7 |
| 2026-Q1 | sat out | – |
| 2026-Q2 | Market favorite (no model) | 0.89 |
| 2026-Q3 | Time-of-day vol x0.5, against trend + skip spikes | 2.27 |
| 2026-Q4 | Time-of-day vol x0.5, against trend + skip spikes | 2.97 |

Why: Market favorite (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 19 | +32 | 68% |
| Quarter | 2025-Q3 | 12 | +34 | 83% |
| Quarter | 2025-Q4 | 15 | +6 | 60% |
| Quarter | 2026-Q1 | 21 | +51 | 67% |
| Quarter | 2026-Q2 | 26 | -16 | 62% |
| Quarter | 2026-Q3 | 13 | -9 | 62% |
| Quarter | 2026-Q4 | 8 | +11 | 75% |
| Price paid | 0.30-0.50 | 27 | +39 | 48% |
| Price paid | 0.50-0.70 | 60 | -11 | 62% |
| Price paid | 0.70-0.90 | 27 | +81 | 96% |
| Model vs market gap | no model | 114 | +109 | 67% |
| Side | yes | 114 | +109 | 67% |

Why: Kalshi price-spike fade (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 4 | +5 | 50% |
| Quarter | 2025-Q2 | 109 | -38 | 34% |
| Quarter | 2025-Q3 | 206 | -419 | 29% |
| Quarter | 2025-Q4 | 221 | -457 | 28% |
| Quarter | 2026-Q1 | 171 | -545 | 28% |
| Quarter | 2026-Q2 | 129 | -151 | 36% |
| Quarter | 2026-Q3 | 147 | -445 | 32% |
| Quarter | 2026-Q4 | 73 | -290 | 29% |
| Price paid | 0.10-0.30 | 528 | -2030 | 13% |
| Price paid | 0.30-0.50 | 299 | -324 | 36% |
| Price paid | 0.50-0.70 | 180 | +19 | 60% |
| Price paid | 0.70-0.90 | 53 | -5 | 76% |
| Model vs market gap | no model | 1060 | -2340 | 31% |
| Side | no | 490 | -1246 | 34% |
| Side | yes | 570 | -1094 | 28% |

Why: Time-of-day vol x0.5, against trend + skip spikes

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 2 | +4 | 100% |
| Quarter | 2025-Q2 | 43 | +50 | 88% |
| Quarter | 2025-Q3 | 76 | -4 | 80% |
| Quarter | 2025-Q4 | 81 | -86 | 73% |
| Quarter | 2026-Q1 | 75 | +45 | 87% |
| Quarter | 2026-Q2 | 75 | +74 | 88% |
| Quarter | 2026-Q3 | 46 | +64 | 94% |
| Quarter | 2026-Q4 | 37 | -4 | 81% |
| Price paid | 0.50-0.70 | 34 | +61 | 79% |
| Price paid | 0.70-0.90 | 381 | +84 | 84% |
| Price paid | 0.90-1.01 | 20 | -1 | 90% |
| Model vs market gap | 0.05-0.10 | 7 | +8 | 100% |
| Model vs market gap | 0.10-0.20 | 390 | +138 | 84% |
| Model vs market gap | 0.20-0.35 | 37 | -8 | 73% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 211 | +133 | 87% |
| Side | yes | 224 | +10 | 81% |

Why: Time-of-day vol x0.5

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 6 | +2 | 83% |
| Quarter | 2025-Q2 | 110 | +16 | 82% |
| Quarter | 2025-Q3 | 218 | -58 | 78% |
| Quarter | 2025-Q4 | 246 | -119 | 76% |
| Quarter | 2026-Q1 | 220 | +81 | 84% |
| Quarter | 2026-Q2 | 207 | +39 | 81% |
| Quarter | 2026-Q3 | 122 | +97 | 88% |
| Quarter | 2026-Q4 | 111 | +30 | 82% |
| Price paid | 0.10-0.30 | 4 | -42 | 0% |
| Price paid | 0.50-0.70 | 136 | +42 | 69% |
| Price paid | 0.70-0.90 | 1058 | +67 | 82% |
| Price paid | 0.90-1.01 | 42 | +21 | 95% |
| Model vs market gap | 0.05-0.10 | 15 | -15 | 80% |
| Model vs market gap | 0.10-0.20 | 1098 | +127 | 82% |
| Model vs market gap | 0.20-0.35 | 126 | -29 | 72% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 625 | -0 | 80% |
| Side | yes | 615 | +88 | 82% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 2 | +2 | 100% |
| Quarter | 2025-Q3 | 5 | +5 | 100% |
| Quarter | 2025-Q4 | 1 | -10 | 0% |
| Quarter | 2026-Q2 | 12 | +24 | 75% |
| Quarter | 2026-Q3 | 17 | +29 | 76% |
| Quarter | 2026-Q4 | 8 | -0 | 75% |
| Price paid | 0.50-0.70 | 33 | +32 | 70% |
| Price paid | 0.70-0.90 | 5 | +11 | 100% |
| Price paid | 0.90-1.01 | 7 | +7 | 100% |
| Model vs market gap | 0.05-0.10 | 23 | +47 | 91% |
| Model vs market gap | 0.10-0.20 | 22 | +2 | 64% |
| Side | no | 2 | -9 | 50% |
| Side | yes | 43 | +59 | 79% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 76 | -4 | 80% |
| Quarter | 2025-Q4 | 81 | -86 | 73% |
| Quarter | 2026-Q2 | 26 | -16 | 62% |
| Quarter | 2026-Q3 | 46 | +64 | 94% |
| Quarter | 2026-Q4 | 37 | -4 | 81% |
| Price paid | 0.30-0.50 | 3 | -5 | 33% |
| Price paid | 0.50-0.70 | 28 | -33 | 57% |
| Price paid | 0.70-0.90 | 221 | -10 | 81% |
| Price paid | 0.90-1.01 | 14 | +3 | 93% |
| Model vs market gap | 0.05-0.10 | 6 | +7 | 100% |
| Model vs market gap | 0.10-0.20 | 212 | -16 | 81% |
| Model vs market gap | 0.20-0.35 | 22 | -19 | 68% |
| Model vs market gap | no model | 26 | -16 | 62% |
| Side | no | 116 | +69 | 87% |
| Side | yes | 150 | -114 | 72% |
