# Backtest (2026-11-12)

Flat $10 per trade at the ask plus Kalshi fees, held to settlement. Prices are real hourly Kalshi quotes. Forecasts are archived NWS-blend (NBM) runs 1-2 days old. Bias/sigma learned only from earlier days.

## Live paper books vs backtest

| Book | Settled | Open | Live P&L | Live return/$ | Backtest rule | Backtest return/$ |
|---|---|---|---|---|---|---|
| bitcoin | 6 | 4 | +6.86 | +11.6% | c_vol50 | +0.4% |
| bitcoin_tod | 6 | 4 | -9.36 | -16.0% | s_combo_tod | +3.0% |
| ethereum | 6 | 4 | -8.60 | -14.7% | a_vol50 | -1.6% |
| ethereum_tod | 6 | 4 | -8.63 | -14.7% | s_combo_tod | +2.1% |
| weather_high | 29 | 14 | +3.47 | +1.2% | fade | +0.1% |
| weather_low | 11 | 7 | -15.77 | -14.9% | fade | +0.3% |

Live numbers need ~100 settled trades before they mean much.

## Weather: daily highs

3731 events, 2025-03-21 to 2026-11-11.

**Verdict:** Long-shot fade (no model): +38 on 4936 trades (+0.1% per $ staked, t=0.25), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 483 | 44% | +140.06 | +2.8% | 0.44 | 0.3 | -193 | +333 | – | – | 0.1953 |
| Long-shot fade (no model) | 4936 | 95% | +38.04 | +0.1% | 0.25 | 0.33 | +33 | +5 | – | – | 0.0433 |
| Bayes: market prior + forecast | 2 | 50% | -4.85 | -24.4% | -0.29 | -0.29 | -10 | +5 | 74% | 0.3459 | 0.3305 |
| Bayes price-level, 99% sure | 1243 | 91% | -141.73 | -1.2% | -1.36 | -1.39 | -7 | -135 | 94% | 0.0769 | 0.0757 |
| Heavy-volume move (10c, 5x): fade | 308 | 48% | -209.18 | -6.7% | -0.88 | -0.69 | -208 | -2 | – | – | 0.184 |
| Market favorite YES (no model) | 4579 | 50% | -211.44 | -0.5% | -0.31 | -0.31 | -115 | -97 | – | – | 0.2424 |
| Combined: rolling best (past 6 months) | 2928 | 94% | -241.19 | -0.9% | -1.55 | -1.61 | +84 | -325 | – | – | 0.0486 |
| Bayes price-level, 95% sure | 2163 | 88% | -339.47 | -1.6% | -2.02 | -1.8 | -209 | -130 | 91% | 0.0953 | 0.0938 |
| Heavy-volume move (10c, 5x): follow | 290 | 49% | -388.11 | -13.2% | -2.08 | -1.84 | -287 | -102 | – | – | 0.1952 |
| Long-shot fade, limit order | 2827 | 92% | -470.71 | -1.8% | -3.25 | -3.25 | -200 | -270 | – | – | 0.073 |
| Combined: 5+ strategies agree | 4946 | 49% | -972.60 | -1.9% | -1.25 | -0.91 | -330 | -642 | 61% | 0.2279 | 0.2363 |
| Heavy-volume move: fade | 1529 | 48% | -1093.49 | -7.1% | -2.11 | -2.61 | -1044 | -50 | – | – | 0.1872 |
| Heavy-volume move: follow | 1494 | 49% | -1655.96 | -11.0% | -3.77 | -3.51 | -705 | -951 | – | – | 0.1916 |
| Favorite, stop loss 25c | 4579 | 42% | -2421.04 | -5.2% | -3.86 | -3.86 | -2110 | -311 | – | – | 0.2411 |
| Forecast bracket YES | 751 | 10% | -3434.68 | -43.5% | -6.22 | -6.22 | -1774 | -1660 | 33% | 0.1468 | 0.0918 |
| Favorite, take profit 10c | 4579 | 70% | -3668.39 | -7.9% | -8.48 | -8.48 | -2229 | -1440 | – | – | 0.2612 |
| Favorite, stop loss 10c | 4579 | 28% | -4200.24 | -9.1% | -8.72 | -8.72 | -2902 | -1299 | – | – | 0.2364 |
| Favorite, take profit 15c / stop 15c | 4579 | 47% | -5384.79 | -11.6% | -15.05 | -15.05 | -3751 | -1634 | – | – | 0.251 |
| Market favorite, limit order | 3731 | 39% | -6414.22 | -17.4% | -10.0 | -10.0 | -4335 | -2079 | – | – | 0.2359 |
| v2 + disagreement cap | 3240 | 33% | -8353.27 | -25.2% | -7.92 | -7.13 | -3992 | -4361 | 54% | 0.2012 | 0.1575 |
| v2 + 50% market blend | 3604 | 31% | -9274.75 | -25.0% | -8.34 | -7.52 | -4367 | -4908 | 46% | 0.1909 | 0.1651 |
| v1 (what we ran live) | 4454 | 34% | -9427.06 | -20.6% | -7.71 | -7.02 | -4253 | -5174 | 63% | 0.2629 | 0.1648 |
| v2 calibrated | 4062 | 32% | -10219.46 | -24.5% | -8.89 | -8.1 | -4829 | -5390 | 58% | 0.2452 | 0.1678 |
| Combined: 3+ strategies agree | 9447 | 46% | -10506.04 | -11.0% | -7.79 | -5.84 | -3790 | -6716 | 62% | 0.2722 | 0.1932 |

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
| 0.6 | 4047 | -9474.03 | -22.9% |
| 0.8 | 3905 | -9833.63 | -24.5% |
| 1.0 | 4062 | -10219.46 | -24.5% |
| 1.25 | 4320 | -8976.81 | -20.3% |
| 1.5 | 4473 | -7958.34 | -17.4% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 4952 | -11720.79 | -23.1% |
| blend 0.0, edge 0.05 | 4642 | -11064.34 | -23.2% |
| blend 0.0, edge 0.08 | 4062 | -10219.46 | -24.5% |
| blend 0.25, edge 0.03 | 4691 | -11442.79 | -23.8% |
| blend 0.25, edge 0.05 | 4203 | -10528.77 | -24.4% |
| blend 0.25, edge 0.08 | 3294 | -8750.43 | -25.9% |
| blend 0.5, edge 0.03 | 4042 | -10301.17 | -24.8% |
| blend 0.5, edge 0.05 | 3122 | -8254.06 | -25.7% |
| blend 0.5, edge 0.08 | 1890 | -4650.68 | -23.9% |
| blend 0.75, edge 0.03 | 1884 | -5231.79 | -26.9% |
| blend 0.75, edge 0.05 | 813 | -2014.66 | -23.9% |
| blend 0.75, edge 0.08 | 216 | -667.98 | -29.8% |

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
| Quarter | 2026-Q4 | 747 | -2269 | 30% |
| Price paid | 0.00-0.10 | 815 | -3086 | 4% |
| Price paid | 0.10-0.30 | 865 | -4063 | 10% |
| Price paid | 0.30-0.50 | 861 | -1375 | 36% |
| Price paid | 0.50-0.70 | 1195 | -1446 | 53% |
| Price paid | 0.70-0.90 | 325 | -240 | 71% |
| Price paid | 0.90-1.01 | 1 | -10 | 0% |
| Model vs market gap | 0.05-0.10 | 59 | -148 | 15% |
| Model vs market gap | 0.10-0.20 | 2063 | -5863 | 32% |
| Model vs market gap | 0.20-0.35 | 1541 | -3240 | 34% |
| Model vs market gap | 0.35-1.01 | 399 | -969 | 28% |
| Side | no | 2457 | -3362 | 48% |
| Side | yes | 1605 | -6857 | 8% |

Why: Long-shot fade (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 61 | -11 | 93% |
| Quarter | 2025-Q2 | 536 | +34 | 96% |
| Quarter | 2025-Q3 | 544 | +57 | 96% |
| Quarter | 2025-Q4 | 268 | -37 | 94% |
| Quarter | 2026-Q1 | 968 | +74 | 96% |
| Quarter | 2026-Q2 | 1056 | -99 | 94% |
| Quarter | 2026-Q3 | 1079 | -8 | 95% |
| Quarter | 2026-Q4 | 424 | +29 | 96% |
| Price paid | 0.90-1.01 | 4936 | +38 | 95% |
| Model vs market gap | no model | 4936 | +38 | 95% |
| Side | no | 4936 | +38 | 95% |

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
| Quarter | 2026-Q4 | 33 | -67 | 46% |
| Price paid | 0.10-0.30 | 173 | -3 | 20% |
| Price paid | 0.30-0.50 | 127 | -28 | 40% |
| Price paid | 0.50-0.70 | 142 | +173 | 69% |
| Price paid | 0.70-0.90 | 41 | -2 | 76% |
| Model vs market gap | no model | 483 | +140 | 44% |
| Side | no | 279 | +95 | 58% |
| Side | yes | 204 | +46 | 26% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 37 | -76 | 60% |
| Quarter | 2025-Q3 | 211 | +7 | 95% |
| Quarter | 2025-Q4 | 159 | -19 | 91% |
| Quarter | 2026-Q1 | 484 | -129 | 87% |
| Quarter | 2026-Q2 | 530 | -94 | 88% |
| Quarter | 2026-Q3 | 538 | -33 | 89% |
| Quarter | 2026-Q4 | 204 | +5 | 88% |
| Price paid | 0.30-0.50 | 21 | -85 | 29% |
| Price paid | 0.50-0.70 | 32 | +9 | 53% |
| Price paid | 0.70-0.90 | 669 | -159 | 82% |
| Price paid | 0.90-1.01 | 1441 | -104 | 93% |
| Model vs market gap | 0.00-0.05 | 1938 | -159 | 90% |
| Model vs market gap | 0.05-0.10 | 204 | -96 | 77% |
| Model vs market gap | 0.10-0.20 | 21 | -85 | 29% |
| Side | no | 2108 | -243 | 90% |
| Side | yes | 55 | -96 | 42% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 544 | +57 | 96% |
| Quarter | 2025-Q4 | 268 | -37 | 94% |
| Quarter | 2026-Q1 | 968 | +74 | 96% |
| Quarter | 2026-Q2 | 1056 | -99 | 94% |
| Quarter | 2026-Q3 | 59 | -169 | 41% |
| Quarter | 2026-Q4 | 33 | -67 | 46% |
| Price paid | 0.10-0.30 | 25 | -215 | 4% |
| Price paid | 0.30-0.50 | 17 | +23 | 47% |
| Price paid | 0.50-0.70 | 37 | -18 | 60% |
| Price paid | 0.70-0.90 | 13 | -26 | 62% |
| Price paid | 0.90-1.01 | 2836 | -6 | 95% |
| Model vs market gap | no model | 2928 | -241 | 94% |
| Side | no | 2893 | -36 | 95% |
| Side | yes | 35 | -205 | 17% |

Forecast error (actual minus NBM forecast)

| City | Entry | n | Bias | RMSE |
|---|---|---|---|---|
| Austin | day before 10am | 243 | +1.79 | 3.28 |
| Austin | same day 8am | 245 | +1.51 | 2.92 |
| Chicago | day before 10am | 243 | +1.48 | 3.45 |
| Chicago | same day 8am | 241 | +1.30 | 2.87 |
| Denver | day before 10am | 244 | +1.75 | 3.41 |
| Denver | same day 8am | 241 | +1.68 | 2.97 |
| Los Angeles | day before 10am | 242 | +2.30 | 3.87 |
| Los Angeles | same day 8am | 244 | +2.31 | 3.61 |
| Miami | same day 8am | 244 | +2.04 | 2.65 |
| New York | same day 8am | 241 | -0.25 | 2.45 |
| Philadelphia | same day 8am | 241 | +1.73 | 2.87 |

## Weather: daily lows

2214 events, 2025-12-13 to 2026-11-11.

**Verdict:** Long-shot fade (no model): +103 on 3204 trades (+0.3% per $ staked, t=0.94), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 152 | 53% | +257.44 | +16.7% | 1.35 | 1.22 | -53 | +310 | – | – | 0.2106 |
| Combined: rolling best (past 6 months) | 1645 | 78% | +233.57 | +1.5% | 0.8 | 0.87 | +165 | +68 | – | – | 0.1229 |
| Long-shot fade (no model) | 3204 | 96% | +102.74 | +0.3% | 0.94 | 1.08 | +80 | +23 | – | – | 0.0366 |
| Heavy-volume move: follow | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Heavy-volume move: fade | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Heavy-volume move (10c, 5x): follow | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Heavy-volume move (10c, 5x): fade | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Bayes price-level, 95% sure | 362 | 94% | -7.94 | -0.2% | -0.16 | -0.07 | -53 | +45 | 96% | 0.056 | 0.0565 |
| Bayes: market prior + forecast | 1 | 0% | -10.25 | -100.0% | – | – | +0 | -10 | 49% | 0.2401 | 0.16 |
| Bayes price-level, 99% sure | 194 | 94% | -17.23 | -0.9% | -0.54 | -0.43 | -15 | -2 | 96% | 0.0541 | 0.0541 |
| Long-shot fade, limit order | 1691 | 93% | -203.04 | -1.3% | -1.89 | -1.51 | -70 | -133 | – | – | 0.0666 |
| Combined: 5+ strategies agree | 2172 | 46% | -538.19 | -2.4% | -1.04 | -1.18 | +652 | -1191 | 55% | 0.236 | 0.2373 |
| Market favorite YES (no model) | 2109 | 47% | -646.79 | -3.0% | -1.32 | -1.32 | +501 | -1148 | – | – | 0.2396 |
| Forecast bracket YES | 546 | 14% | -1780.61 | -31.1% | -3.87 | -3.87 | -1057 | -724 | 34% | 0.1605 | 0.1195 |
| Favorite, take profit 10c | 2109 | 62% | -2737.92 | -12.8% | -8.12 | -8.12 | -984 | -1754 | – | – | 0.266 |
| Market favorite, limit order | 1755 | 36% | -2995.51 | -17.2% | -6.3 | -6.3 | -733 | -2262 | – | – | 0.2264 |
| v2 + 50% market blend | 1858 | 29% | -3905.60 | -20.4% | -4.29 | -4.04 | -973 | -2932 | 41% | 0.1565 | 0.1414 |
| Favorite, stop loss 25c | 2109 | 28% | -5261.14 | -24.6% | -12.79 | -12.79 | -2185 | -3076 | – | – | 0.2288 |
| v2 calibrated | 2581 | 31% | -5682.55 | -21.4% | -5.69 | -5.17 | -1637 | -4046 | 52% | 0.1997 | 0.1494 |
| Favorite, stop loss 10c | 2109 | 14% | -5729.32 | -26.8% | -20.61 | -20.61 | -2847 | -2882 | – | – | 0.2162 |
| v2 + disagreement cap | 2243 | 31% | -6130.80 | -26.6% | -6.96 | -6.98 | -2143 | -3988 | 50% | 0.177 | 0.1425 |
| Combined: 3+ strategies agree | 4459 | 40% | -6197.00 | -13.6% | -6.04 | -5.33 | -2057 | -4140 | 56% | 0.2329 | 0.1856 |
| Favorite, take profit 15c / stop 15c | 2109 | 28% | -6342.36 | -29.6% | -27.2 | -27.2 | -3268 | -3074 | – | – | 0.2352 |
| v1 (what we ran live) | 3793 | 32% | -10412.57 | -26.7% | -9.48 | -8.67 | -4440 | -5972 | 57% | 0.2259 | 0.1477 |

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
| 0.6 | 3336 | -5353.65 | -15.8% |
| 0.8 | 2644 | -5051.29 | -18.6% |
| 1.0 | 2581 | -5682.55 | -21.4% |
| 1.25 | 3004 | -6805.17 | -22.1% |
| 1.5 | 3526 | -8669.14 | -24.0% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 3977 | -9135.54 | -22.4% |
| blend 0.0, edge 0.05 | 3409 | -8135.35 | -23.2% |
| blend 0.0, edge 0.08 | 2581 | -5682.55 | -21.4% |
| blend 0.25, edge 0.03 | 3402 | -8047.61 | -23.0% |
| blend 0.25, edge 0.05 | 2667 | -5798.05 | -21.1% |
| blend 0.25, edge 0.08 | 1713 | -3558.11 | -20.2% |
| blend 0.5, edge 0.03 | 2328 | -5081.92 | -21.2% |
| blend 0.5, edge 0.05 | 1490 | -3151.39 | -20.5% |
| blend 0.5, edge 0.08 | 722 | -551.96 | -7.4% |
| blend 0.75, edge 0.03 | 621 | -638.50 | -9.9% |
| blend 0.75, edge 0.05 | 247 | -555.70 | -21.6% |
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
| Quarter | 2026-Q4 | 366 | -556 | 29% |
| Price paid | 0.00-0.10 | 554 | -2208 | 4% |
| Price paid | 0.10-0.30 | 799 | -2295 | 12% |
| Price paid | 0.30-0.50 | 312 | -671 | 34% |
| Price paid | 0.50-0.70 | 630 | -374 | 58% |
| Price paid | 0.70-0.90 | 285 | -136 | 73% |
| Price paid | 0.90-1.01 | 1 | +1 | 100% |
| Model vs market gap | 0.05-0.10 | 36 | +38 | 19% |
| Model vs market gap | 0.10-0.20 | 1617 | -4553 | 31% |
| Model vs market gap | 0.20-0.35 | 767 | -590 | 34% |
| Model vs market gap | 0.35-1.01 | 161 | -578 | 24% |
| Side | no | 1212 | -1139 | 55% |
| Side | yes | 1369 | -4543 | 10% |

Why: Long-shot fade (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q1 | 950 | -40 | 95% |
| Quarter | 2026-Q2 | 1044 | +162 | 97% |
| Quarter | 2026-Q3 | 976 | -12 | 96% |
| Quarter | 2026-Q4 | 234 | -8 | 96% |
| Price paid | 0.90-1.01 | 3204 | +103 | 96% |
| Model vs market gap | no model | 3204 | +103 | 96% |
| Side | no | 3204 | +103 | 96% |

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
| Quarter | 2026-Q4 | 69 | -14 | 90% |
| Price paid | 0.50-0.70 | 2 | -5 | 50% |
| Price paid | 0.70-0.90 | 14 | +24 | 86% |
| Price paid | 0.90-1.01 | 346 | -27 | 94% |
| Model vs market gap | 0.00-0.05 | 288 | +5 | 96% |
| Model vs market gap | 0.05-0.10 | 58 | -32 | 90% |
| Model vs market gap | 0.10-0.20 | 16 | +19 | 81% |
| Side | no | 346 | -27 | 94% |
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
| Austin | day before 10am | 243 | -2.62 | 4.12 |
| Austin | day before 8pm | 245 | -2.71 | 3.99 |
| Chicago | day before 10am | 243 | -1.61 | 3.02 |
| Chicago | day before 8pm | 245 | -1.38 | 2.66 |
| Denver | day before 10am | 244 | -3.97 | 5.26 |
| Denver | day before 8pm | 245 | -3.84 | 5.11 |
| Los Angeles | day before 10am | 243 | +0.35 | 1.71 |
| Los Angeles | day before 8pm | 245 | +0.47 | 1.61 |
| Miami | day before 8pm | 243 | -0.97 | 2.38 |
| New York | day before 8pm | 245 | -1.62 | 2.71 |
| Philadelphia | day before 8pm | 245 | +0.44 | 2.21 |

## Crypto: Bitcoin 5pm price

599 events, 2025-03-22 to 2026-11-11.

**Verdict:** Vol x0.5, weekends only: +150 on 230 trades (+6.7% per $ staked, t=2.15), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Time-of-day vol x0.5 | 1528 | 80% | +325.01 | +2.2% | 1.64 | 1.85 | -153 | +478 | 92% | 0.1706 | 0.1581 |
| Time-of-day vol x0.5, skip spikes | 953 | 82% | +275.75 | +3.0% | 1.84 | 1.73 | -163 | +439 | 92% | 0.1611 | 0.1524 |
| Time-of-day vol x0.5, against trend + skip spikes | 502 | 82% | +191.73 | +3.9% | 1.8 | 1.91 | -115 | +307 | 92% | 0.1525 | 0.1458 |
| Regime-scaled vol x0.5 | 1929 | 78% | +170.74 | +0.9% | 0.75 | 0.78 | -229 | +399 | 93% | 0.1884 | 0.167 |
| Bayes price-level, 95% sure | 640 | 92% | +154.12 | +2.5% | 2.07 | 1.12 | +10 | +145 | 93% | 0.0716 | 0.0729 |
| Vol x0.5, weekends only | 230 | 84% | +149.69 | +6.7% | 2.15 | 2.09 | +17 | +132 | 91% | 0.1219 | 0.1265 |
| Vol x0.5, skip spiked markets | 1085 | 79% | +130.64 | +1.2% | 0.77 | 0.96 | -186 | +317 | 93% | 0.1813 | 0.1622 |
| Vol x0.5, against the 24h trend | 818 | 79% | +105.27 | +1.3% | 0.69 | 1.1 | -158 | +263 | 93% | 0.183 | 0.1635 |
| Bayes price-level, 99% sure | 310 | 93% | +97.97 | +3.3% | 1.91 | 1.64 | +42 | +56 | 93% | 0.0697 | 0.0719 |
| Combined: rolling best (past 6 months) | 296 | 81% | +95.02 | +3.3% | 1.17 | 0.38 | -54 | +149 | 92% | 0.1568 | 0.1473 |
| Vol x0.5, against trend + skip spikes | 574 | 80% | +88.27 | +1.6% | 0.72 | 0.93 | -72 | +160 | 93% | 0.1753 | 0.1574 |
| Vol x0.5, calm market only | 1038 | 79% | +86.90 | +0.9% | 0.53 | 0.7 | -94 | +181 | 92% | 0.1774 | 0.1603 |
| Vol x0.5 | 1758 | 78% | +76.54 | +0.4% | 0.35 | 0.47 | -289 | +365 | 93% | 0.189 | 0.1669 |
| Long-shot fade (no model) | 1282 | 96% | +61.42 | +0.5% | 0.91 | 0.94 | -51 | +112 | – | – | 0.0354 |
| Vol x0.5, skip news in window | 1734 | 78% | +57.14 | +0.3% | 0.26 | 0.39 | -288 | +345 | 93% | 0.1895 | 0.167 |
| Vol x0.5, skip news days | 1653 | 78% | +45.76 | +0.3% | 0.21 | 0.34 | -276 | +322 | 93% | 0.1892 | 0.1665 |
| Vol x0.5, news days only | 105 | 78% | +30.78 | +3.0% | 0.58 | 0.56 | -1 | +32 | 93% | 0.1865 | 0.1727 |
| Bayes: market prior + full vol | 3 | 67% | -6.07 | -20.9% | -0.53 | -0.69 | +2 | -8 | 92% | 0.2927 | 0.2732 |
| Vol x0.5, busy market only | 720 | 76% | -10.36 | -0.1% | -0.08 | -0.08 | -208 | +198 | 93% | 0.2058 | 0.1764 |
| Vol x0.5, with the 24h trend | 940 | 78% | -28.73 | -0.3% | -0.16 | -0.6 | -133 | +104 | 93% | 0.1943 | 0.1698 |
| Bayes: market prior + fat-tail | 14 | 57% | -37.12 | -26.9% | -1.51 | -1.2 | -18 | -19 | 86% | 0.3377 | 0.2814 |
| Fat-tail, moves x0.5 | 1848 | 73% | -71.80 | -0.4% | -0.28 | -0.35 | -214 | +142 | 89% | 0.2226 | 0.1953 |
| Vol x0.5, weekdays only | 1528 | 77% | -73.15 | -0.5% | -0.36 | -0.35 | -306 | +233 | 93% | 0.1992 | 0.1729 |
| Fat-tail, moves x0.75 | 1160 | 73% | -157.79 | -1.4% | -0.72 | -0.68 | -190 | +33 | 86% | 0.2069 | 0.19 |
| Vol x0.5, stop loss 25c | 1758 | 65% | -438.64 | -2.5% | -2.4 | -2.56 | -735 | +297 | 93% | 0.3052 | 0.2343 |
| Vol x0.75 | 784 | 72% | -489.13 | -6.3% | -2.21 | -2.56 | -321 | -168 | 85% | 0.1699 | 0.1527 |
| Heavy-volume move: follow | 1226 | 62% | -630.88 | -5.2% | -1.96 | -1.27 | -595 | -36 | – | – | 0.183 |
| Fat-tail (actual past moves) | 623 | 58% | -635.20 | -10.2% | -2.0 | -1.36 | -557 | -78 | 73% | 0.2011 | 0.1805 |
| Vol x0.5, take profit 10c | 1758 | 81% | -693.09 | -4.0% | -3.61 | -3.21 | -670 | -23 | 93% | 0.165 | 0.1546 |
| Heavy-volume move (10c, 5x): follow | 730 | 60% | -862.11 | -11.9% | -3.96 | -2.93 | -476 | -386 | – | – | 0.183 |
| Combined: 5+ strategies agree | 2237 | 71% | -987.94 | -4.5% | -2.32 | -3.31 | -988 | +1 | 84% | 0.1742 | 0.1555 |
| Vol x0.5, stop loss 10c | 1758 | 47% | -1030.17 | -6.0% | -6.9 | -6.89 | -1070 | +40 | 93% | 0.4611 | 0.3264 |
| Vol x0.5, take profit 15c / stop 15c | 1758 | 57% | -1090.08 | -6.3% | -7.44 | -7.56 | -1073 | -17 | 93% | 0.3728 | 0.2762 |
| v1 + 50% market blend | 285 | 30% | -1120.66 | -38.2% | -4.09 | -3.89 | -636 | -485 | 41% | 0.1096 | 0.0977 |
| Options vol x0.85, 5c gap | 806 | 56% | -1180.54 | -14.6% | -2.95 | -2.68 | -695 | -485 | 65% | 0.1209 | 0.11 |
| Heavy-volume move (10c, 5x): fade | 776 | 37% | -1262.89 | -15.9% | -3.14 | -3.13 | -691 | -572 | – | – | 0.1736 |
| v1 (what we ran live) | 448 | 38% | -1371.99 | -30.0% | -3.89 | -3.5 | -950 | -422 | 53% | 0.126 | 0.0982 |
| Options vol, 8c gap | 414 | 23% | -1414.51 | -32.9% | -3.41 | -2.71 | -1025 | -390 | 39% | 0.1099 | 0.0824 |
| Vol x0.5, limit order | 948 | 60% | -1716.40 | -18.8% | -8.66 | -9.02 | -1087 | -629 | 92% | 0.3419 | 0.2541 |
| Options vol, NO only | 589 | 31% | -1749.79 | -28.9% | -3.76 | -3.33 | -1366 | -383 | 45% | 0.1238 | 0.1024 |
| Vol x0.5, limit order (strict fill) | 912 | 59% | -1833.37 | -20.8% | -9.37 | -9.54 | -1150 | -683 | 92% | 0.3552 | 0.2616 |
| Vol x0.5 5c edge, limit order | 1038 | 60% | -1962.49 | -19.6% | -9.42 | -9.75 | -1225 | -738 | 91% | 0.3342 | 0.2507 |
| Options vol, 5c gap | 679 | 31% | -2144.41 | -30.6% | -4.56 | -4.45 | -1313 | -831 | 44% | 0.1134 | 0.0927 |
| Heavy-volume move: fade | 1279 | 35% | -2330.34 | -17.8% | -4.45 | -4.56 | -828 | -1503 | – | – | 0.1755 |
| Combined: 3+ strategies agree | 3278 | 65% | -2553.60 | -7.9% | -4.4 | -4.95 | -1978 | -576 | 82% | 0.1721 | 0.1552 |
| Kalshi price-spike fade (no model) | 1235 | 30% | -3105.03 | -24.4% | -5.84 | -5.48 | -1626 | -1479 | – | – | 0.1524 |

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
| 0.4 | 1956 | +92.44 | +0.5% |
| 0.5 | 1758 | +76.54 | +0.4% |
| 0.6 | 1389 | -279.08 | -2.1% |
| 0.75 | 784 | -489.13 | -6.3% |
| 1.0 | 448 | -1371.99 | -30.0% |
| 1.25 | 546 | -2411.72 | -42.2% |

Sweep: options vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 1578 | -234.87 | -1.5% |
| 0.7 | 1268 | -722.84 | -5.8% |
| 0.8 | 936 | -872.58 | -9.4% |
| 0.9 | 737 | -1589.82 | -21.3% |
| 1.0 | 679 | -2144.41 | -30.6% |
| 1.1 | 751 | -2914.15 | -37.2% |

Sweep: time-of-day vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1948 | +89.81 | +0.5% |
| 0.5 | 1528 | +325.01 | +2.2% |
| 0.6 | 1014 | +282.51 | +2.9% |
| 0.75 | 410 | -16.03 | -0.4% |
| 1.0 | 324 | -1069.50 | -32.0% |

Sweep: fat-tail

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 2046 | -85.87 | -0.4% |
| 0.5 | 1848 | -71.80 | -0.4% |
| 0.6 | 1607 | +19.11 | +0.1% |
| 0.75 | 1160 | -157.79 | -1.4% |
| 0.9 | 777 | -636.99 | -8.3% |
| 1.0 | 623 | -635.20 | -10.2% |

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
| 2026-Q4 | 82 | 1.208 |

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
| Quarter | 2026-Q4 | 47 | +103 | 36% |
| Price paid | 0.00-0.10 | 65 | -414 | 3% |
| Price paid | 0.10-0.30 | 196 | -996 | 8% |
| Price paid | 0.30-0.50 | 3 | -9 | 33% |
| Price paid | 0.50-0.70 | 11 | +14 | 73% |
| Price paid | 0.70-0.90 | 172 | +31 | 83% |
| Price paid | 0.90-1.01 | 1 | +1 | 100% |
| Model vs market gap | 0.05-0.10 | 21 | +189 | 57% |
| Model vs market gap | 0.10-0.20 | 389 | -1289 | 38% |
| Model vs market gap | 0.20-0.35 | 38 | -272 | 24% |
| Side | no | 289 | -826 | 37% |
| Side | yes | 159 | -546 | 38% |

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
| Quarter | 2026-Q4 | 113 | +83 | 82% |
| Price paid | 0.00-0.10 | 2 | -21 | 0% |
| Price paid | 0.10-0.30 | 3 | -32 | 0% |
| Price paid | 0.30-0.50 | 2 | +1 | 50% |
| Price paid | 0.50-0.70 | 202 | +152 | 73% |
| Price paid | 0.70-0.90 | 1540 | -22 | 79% |
| Price paid | 0.90-1.01 | 9 | -2 | 89% |
| Model vs market gap | 0.05-0.10 | 15 | -12 | 80% |
| Model vs market gap | 0.10-0.20 | 1227 | +32 | 80% |
| Model vs market gap | 0.20-0.35 | 515 | +52 | 74% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 984 | +2 | 78% |
| Side | yes | 774 | +74 | 79% |

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
| Quarter | 2026-Q4 | 12 | +18 | 92% |
| Price paid | 0.00-0.10 | 2 | -21 | 0% |
| Price paid | 0.10-0.30 | 3 | -32 | 0% |
| Price paid | 0.30-0.50 | 1 | -10 | 0% |
| Price paid | 0.50-0.70 | 24 | +91 | 92% |
| Price paid | 0.70-0.90 | 194 | +127 | 86% |
| Price paid | 0.90-1.01 | 6 | -5 | 83% |
| Model vs market gap | 0.05-0.10 | 5 | -17 | 60% |
| Model vs market gap | 0.10-0.20 | 185 | +125 | 86% |
| Model vs market gap | 0.20-0.35 | 39 | +37 | 80% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 142 | +163 | 87% |
| Side | yes | 88 | -14 | 80% |

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
| Quarter | 2026-Q4 | 91 | -100 | 35% |
| Price paid | 0.10-0.30 | 683 | -2906 | 12% |
| Price paid | 0.30-0.50 | 294 | -457 | 34% |
| Price paid | 0.50-0.70 | 185 | +139 | 65% |
| Price paid | 0.70-0.90 | 73 | +119 | 89% |
| Model vs market gap | no model | 1235 | -3105 | 30% |
| Side | no | 603 | -1311 | 42% |
| Side | yes | 632 | -1794 | 18% |

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
| Quarter | 2026-Q4 | 38 | +37 | 87% |
| Price paid | 0.10-0.30 | 1 | -11 | 0% |
| Price paid | 0.50-0.70 | 38 | +29 | 74% |
| Price paid | 0.70-0.90 | 458 | +190 | 84% |
| Price paid | 0.90-1.01 | 5 | -17 | 60% |
| Model vs market gap | 0.05-0.10 | 12 | -4 | 83% |
| Model vs market gap | 0.10-0.20 | 419 | +156 | 83% |
| Model vs market gap | 0.20-0.35 | 71 | +40 | 79% |
| Side | no | 285 | +118 | 83% |
| Side | yes | 217 | +74 | 82% |

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
| Quarter | 2026-Q4 | 138 | +86 | 83% |
| Price paid | 0.10-0.30 | 2 | -21 | 0% |
| Price paid | 0.30-0.50 | 2 | +1 | 50% |
| Price paid | 0.50-0.70 | 130 | +119 | 74% |
| Price paid | 0.70-0.90 | 1386 | +240 | 81% |
| Price paid | 0.90-1.01 | 8 | -14 | 75% |
| Model vs market gap | 0.05-0.10 | 22 | -1 | 86% |
| Model vs market gap | 0.10-0.20 | 1245 | +196 | 81% |
| Model vs market gap | 0.20-0.35 | 260 | +126 | 77% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 876 | +225 | 80% |
| Side | yes | 652 | +100 | 80% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 93 | -18 | 91% |
| Quarter | 2025-Q3 | 21 | -41 | 71% |
| Quarter | 2025-Q4 | 4 | +2 | 75% |
| Quarter | 2026-Q1 | 7 | +10 | 100% |
| Quarter | 2026-Q2 | 140 | +32 | 91% |
| Quarter | 2026-Q3 | 238 | +115 | 94% |
| Quarter | 2026-Q4 | 137 | +54 | 93% |
| Price paid | 0.50-0.70 | 2 | +15 | 100% |
| Price paid | 0.70-0.90 | 178 | +117 | 90% |
| Price paid | 0.90-1.01 | 460 | +22 | 93% |
| Model vs market gap | 0.00-0.05 | 413 | +82 | 94% |
| Model vs market gap | 0.05-0.10 | 209 | +56 | 90% |
| Model vs market gap | 0.10-0.20 | 18 | +16 | 94% |
| Side | no | 259 | +69 | 94% |
| Side | yes | 381 | +85 | 91% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 139 | -79 | 74% |
| Quarter | 2026-Q1 | 52 | +90 | 90% |
| Quarter | 2026-Q2 | 48 | +70 | 90% |
| Quarter | 2026-Q3 | 19 | -23 | 74% |
| Quarter | 2026-Q4 | 38 | +37 | 87% |
| Price paid | 0.00-0.10 | 2 | -21 | 0% |
| Price paid | 0.10-0.30 | 2 | -21 | 0% |
| Price paid | 0.30-0.50 | 1 | -10 | 0% |
| Price paid | 0.50-0.70 | 36 | +68 | 81% |
| Price paid | 0.70-0.90 | 252 | +87 | 83% |
| Price paid | 0.90-1.01 | 3 | -8 | 67% |
| Model vs market gap | 0.05-0.10 | 11 | -18 | 73% |
| Model vs market gap | 0.10-0.20 | 217 | +114 | 84% |
| Model vs market gap | 0.20-0.35 | 67 | -6 | 73% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 165 | +100 | 82% |
| Side | yes | 131 | -5 | 79% |

## Weather: daily highs: late entries

2686 events, 2025-03-21 to 2026-11-11.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Late long-shot fade 1-4c (+48 on 963 trades).

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Late long-shot fade 1-4c | 963 | 99% | +47.80 | +0.5% | 1.7 | 1.79 | -7 | +55 | – | – | 0.0084 |
| Combined: 3+ strategies agree | 680 | 81% | +17.32 | +0.3% | 0.12 | 0.18 | +55 | -38 | 92% | 0.1687 | 0.1491 |
| Late favorite 90-97c | 822 | 95% | +8.51 | +0.1% | 0.14 | 0.14 | -4 | +13 | – | – | 0.0488 |
| Bayes price-level, 99% sure | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Late long-shot fade | 742 | 95% | -12.13 | -0.2% | -0.21 | -0.38 | -36 | +24 | – | – | 0.0438 |
| Bayes price-level, 95% sure | 64 | 84% | -34.18 | -5.4% | -1.07 | -0.52 | -9 | -26 | 93% | 0.1359 | 0.1269 |
| Combined: rolling best (past 6 months) | 542 | 97% | -40.45 | -0.8% | -1.04 | -1.07 | -66 | +26 | – | – | 0.0282 |
| Late favorite 80-90c | 436 | 86% | -51.25 | -1.2% | -0.62 | -0.62 | -3 | -48 | – | – | 0.1231 |
| Combined: 5+ strategies agree | 436 | 86% | -51.25 | -1.2% | -0.62 | -0.62 | -3 | -48 | – | – | 0.1231 |
| Late fav 80-90c, stop loss 25c | 436 | 82% | -87.18 | -2.1% | -1.1 | -1.1 | -30 | -57 | – | – | 0.1467 |
| Late fav 80-90c, stop loss 10c | 436 | 78% | -98.45 | -2.3% | -1.29 | -1.29 | -30 | -68 | – | – | 0.1736 |
| Late fav 80-90c, take profit 15c / stop 15c | 436 | 80% | -117.66 | -2.8% | -1.52 | -1.52 | -49 | -69 | – | – | 0.1593 |
| Late fav 80-90c, take profit 10c | 436 | 86% | -122.68 | -2.9% | -1.53 | -1.53 | -32 | -91 | – | – | 0.1219 |
| Late favorite 50-80c | 547 | 67% | -174.82 | -3.2% | -1.08 | -1.08 | -107 | -68 | – | – | 0.2136 |
| Heavy-volume move (10c, 5x): follow | 846 | 72% | -476.38 | -5.7% | -2.43 | -2.21 | -358 | -118 | – | – | 0.1661 |
| Heavy-volume move: follow | 1314 | 69% | -512.56 | -3.9% | -1.67 | -1.0 | -525 | +13 | – | – | 0.169 |
| Heavy-volume move (10c, 5x): fade | 1009 | 25% | -2211.08 | -21.1% | -4.01 | -3.91 | -894 | -1317 | – | – | 0.1495 |
| Heavy-volume move: fade | 1585 | 26% | -3646.22 | -22.2% | -5.41 | -5.13 | -2156 | -1490 | – | – | 0.1501 |

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
| Quarter | 2026-Q4 | 42 | -4 | 86% |
| Price paid | 0.70-0.90 | 382 | -63 | 85% |
| Price paid | 0.90-1.01 | 54 | +12 | 93% |
| Model vs market gap | no model | 436 | -51 | 86% |
| Side | yes | 436 | -51 | 86% |

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
| Quarter | 2026-Q4 | 69 | +9 | 100% |
| Price paid | 0.90-1.01 | 542 | -40 | 97% |
| Model vs market gap | no model | 542 | -40 | 97% |
| Side | no | 542 | -40 | 97% |

## Weather: daily lows: late entries

1811 events, 2025-12-13 to 2026-11-11.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Heavy-volume move: fade (+337 on 727 trades).

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Heavy-volume move: fade | 727 | 34% | +337.41 | +4.5% | 0.63 | 0.52 | +474 | -136 | – | – | 0.1635 |
| Bayes price-level, 99% sure | 9 | 67% | +52.26 | +56.4% | 1.45 | 1.45 | +8 | +45 | 57% | 0.232 | 0.305 |
| Bayes price-level, 95% sure | 32 | 47% | +6.27 | +1.9% | 0.09 | 0.13 | -37 | +44 | 60% | 0.2954 | 0.2965 |
| Heavy-volume move (10c, 5x): fade | 324 | 29% | -2.61 | -0.1% | 0.0 | -0.69 | +139 | -142 | – | – | 0.1567 |
| Late favorite 90-97c | 876 | 94% | -87.84 | -1.1% | -1.26 | -1.26 | -47 | -41 | – | – | 0.0551 |
| Combined: rolling best (past 6 months) | 308 | 31% | -93.22 | -2.9% | -0.25 | -0.55 | -506 | +413 | – | – | 0.156 |
| Late favorite 80-90c | 360 | 82% | -212.95 | -6.0% | -2.59 | -2.59 | -95 | -118 | – | – | 0.148 |
| Combined: 5+ strategies agree | 360 | 82% | -212.95 | -6.0% | -2.59 | -2.59 | -95 | -118 | – | – | 0.148 |
| Late long-shot fade 1-4c | 1828 | 98% | -216.10 | -1.2% | -3.23 | -3.02 | -138 | -78 | – | – | 0.0245 |
| Combined: 3+ strategies agree | 413 | 79% | -251.46 | -6.2% | -2.54 | -2.66 | -151 | -101 | 55% | 0.1882 | 0.1619 |
| Late fav 80-90c, take profit 10c | 360 | 82% | -259.38 | -7.4% | -3.24 | -3.24 | -117 | -143 | – | – | 0.146 |
| Heavy-volume move (10c, 5x): follow | 238 | 66% | -298.81 | -12.7% | -2.5 | -2.04 | -187 | -112 | – | – | 0.1699 |
| Late long-shot fade | 1337 | 93% | -366.70 | -2.9% | -3.95 | -3.7 | -278 | -89 | – | – | 0.064 |
| Late fav 80-90c, stop loss 25c | 360 | 62% | -405.71 | -11.5% | -5.98 | -5.98 | -227 | -179 | – | – | 0.2865 |
| Late fav 80-90c, stop loss 10c | 360 | 39% | -428.70 | -12.2% | -8.45 | -8.45 | -242 | -187 | – | – | 0.4377 |
| Late fav 80-90c, take profit 15c / stop 15c | 360 | 48% | -433.14 | -12.3% | -7.75 | -7.75 | -240 | -193 | – | – | 0.3764 |
| Late favorite 50-80c | 421 | 58% | -628.72 | -15.1% | -4.15 | -4.15 | -226 | -403 | – | – | 0.2387 |
| Heavy-volume move: follow | 566 | 57% | -1176.21 | -20.9% | -5.89 | -5.62 | -555 | -621 | – | – | 0.1749 |

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
| Quarter | 2026-Q4 | 37 | -16 | 84% |
| Price paid | 0.70-0.90 | 320 | -199 | 81% |
| Price paid | 0.90-1.01 | 40 | -14 | 88% |
| Model vs market gap | no model | 360 | -213 | 82% |
| Side | yes | 360 | -213 | 82% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q2 | 6 | -61 | 0% |
| Quarter | 2026-Q3 | 20 | +18 | 50% |
| Quarter | 2026-Q4 | 6 | +49 | 83% |
| Price paid | 0.30-0.50 | 22 | +58 | 55% |
| Price paid | 0.50-0.70 | 7 | -22 | 43% |
| Price paid | 0.70-0.90 | 3 | -30 | 0% |
| Model vs market gap | 0.05-0.10 | 2 | -20 | 0% |
| Model vs market gap | 0.10-0.20 | 23 | +1 | 48% |
| Model vs market gap | 0.20-0.35 | 7 | +26 | 57% |
| Side | no | 29 | +36 | 52% |
| Side | yes | 3 | -30 | 0% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q3 | 224 | -257 | 31% |
| Quarter | 2026-Q4 | 84 | +164 | 32% |
| Price paid | 0.10-0.30 | 212 | -262 | 16% |
| Price paid | 0.30-0.50 | 47 | +142 | 53% |
| Price paid | 0.50-0.70 | 19 | +21 | 68% |
| Price paid | 0.70-0.90 | 27 | +2 | 82% |
| Price paid | 0.90-1.01 | 3 | +3 | 100% |
| Model vs market gap | no model | 308 | -93 | 31% |
| Side | no | 193 | -53 | 35% |
| Side | yes | 115 | -40 | 25% |

## Bitcoin: last 1-3 hours

599 events, 2025-03-22 to 2026-11-11.

**Verdict:** Late long-shot fade 1-4c: +89 on 877 trades (+1.0% per $ staked, t=6.23), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bayes price-level, 95% sure | 918 | 92% | +221.75 | +2.5% | 2.49 | 2.64 | +52 | +170 | 94% | 0.0682 | 0.0696 |
| Bayes price-level, 99% sure | 528 | 95% | +219.47 | +4.3% | 3.97 | 3.31 | +99 | +120 | 96% | 0.0459 | 0.0494 |
| Combined: rolling best (past 6 months) | 734 | 97% | +157.06 | +2.2% | 3.17 | 2.25 | +22 | +135 | 94% | 0.0584 | 0.0281 |
| Late long-shot fade | 739 | 97% | +104.13 | +1.5% | 2.34 | 1.88 | +41 | +63 | – | – | 0.0286 |
| Combined: 3+ strategies agree | 250 | 90% | +102.99 | +4.2% | 1.88 | 1.84 | -0 | +103 | 90% | 0.0889 | 0.0865 |
| Late long-shot fade 1-4c | 877 | 100% | +88.63 | +1.0% | 6.23 | 5.85 | +37 | +52 | – | – | 0.0026 |
| Late favorite 90-97c | 199 | 97% | +31.42 | +1.7% | 1.29 | 1.29 | +28 | +3 | – | – | 0.0305 |
| Late favorite 50-80c | 31 | 68% | -0.41 | -0.1% | 0.01 | 0.01 | -31 | +31 | – | – | 0.2216 |
| Late favorite 80-90c | 46 | 87% | -1.96 | -0.4% | -0.06 | -0.06 | -1 | -1 | – | – | 0.116 |
| Combined: 5+ strategies agree | 46 | 87% | -1.96 | -0.4% | -0.06 | -0.06 | -1 | -1 | – | – | 0.116 |
| Late fav 80-90c, take profit 10c | 46 | 87% | -3.23 | -0.7% | -0.11 | -0.11 | -1 | -2 | – | – | 0.116 |
| Late fav 80-90c, stop loss 25c | 46 | 74% | -31.47 | -7.0% | -1.17 | -1.17 | -34 | +3 | – | – | 0.2045 |
| Late fav 80-90c, stop loss 10c | 46 | 59% | -48.81 | -10.8% | -1.95 | -1.95 | -49 | +1 | – | – | 0.3001 |
| Late fav 80-90c, take profit 15c / stop 15c | 46 | 63% | -50.59 | -11.2% | -1.92 | -1.92 | -49 | -2 | – | – | 0.2749 |
| Heavy-volume move (10c, 5x): follow | 792 | 66% | -643.19 | -8.2% | -3.05 | -2.23 | -323 | -320 | – | – | 0.1777 |
| Heavy-volume move: follow | 1300 | 66% | -993.13 | -7.7% | -3.57 | -2.98 | -618 | -375 | – | – | 0.1692 |
| Heavy-volume move (10c, 5x): fade | 861 | 31% | -1769.82 | -19.9% | -3.97 | -3.88 | -1150 | -620 | – | – | 0.166 |
| Heavy-volume move: fade | 1383 | 30% | -3564.63 | -25.0% | -6.55 | -5.84 | -2115 | -1449 | – | – | 0.1544 |

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
| Quarter | 2026-Q4 | 1 | +2 | 100% |
| Price paid | 0.70-0.90 | 38 | +1 | 87% |
| Price paid | 0.90-1.01 | 8 | -3 | 88% |
| Model vs market gap | no model | 46 | -2 | 87% |
| Side | yes | 46 | -2 | 87% |

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
| Quarter | 2026-Q4 | 136 | +16 | 100% |
| Price paid | 0.90-1.01 | 877 | +89 | 100% |
| Model vs market gap | no model | 877 | +89 | 100% |
| Side | no | 877 | +89 | 100% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 11 | -3 | 91% |
| Quarter | 2025-Q3 | 58 | +11 | 93% |
| Quarter | 2025-Q4 | 76 | -19 | 88% |
| Quarter | 2026-Q1 | 135 | +35 | 95% |
| Quarter | 2026-Q2 | 257 | +10 | 91% |
| Quarter | 2026-Q3 | 250 | +199 | 96% |
| Quarter | 2026-Q4 | 131 | -12 | 88% |
| Price paid | 0.50-0.70 | 2 | -5 | 50% |
| Price paid | 0.70-0.90 | 386 | +159 | 87% |
| Price paid | 0.90-1.01 | 530 | +68 | 96% |
| Model vs market gap | 0.00-0.05 | 407 | +69 | 97% |
| Model vs market gap | 0.05-0.10 | 439 | +142 | 90% |
| Model vs market gap | 0.10-0.20 | 72 | +10 | 83% |
| Side | no | 154 | +38 | 91% |
| Side | yes | 764 | +184 | 93% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 50 | -0 | 96% |
| Quarter | 2025-Q4 | 29 | +3 | 100% |
| Quarter | 2026-Q1 | 127 | +17 | 100% |
| Quarter | 2026-Q2 | 260 | +14 | 99% |
| Quarter | 2026-Q3 | 181 | +141 | 96% |
| Quarter | 2026-Q4 | 87 | -18 | 88% |
| Price paid | 0.70-0.90 | 117 | +71 | 89% |
| Price paid | 0.90-1.01 | 617 | +86 | 99% |
| Model vs market gap | 0.00-0.05 | 116 | +38 | 98% |
| Model vs market gap | 0.05-0.10 | 141 | +79 | 91% |
| Model vs market gap | 0.10-0.20 | 11 | +6 | 82% |
| Model vs market gap | no model | 466 | +33 | 99% |
| Side | no | 518 | +88 | 99% |
| Side | yes | 216 | +69 | 93% |

## Ethereum

594 events, 2025-03-27 to 2026-11-11.

**Verdict:** Market favorite (no model): +115 on 112 trades (+10.3% per $ staked, t=1.3), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Time-of-day vol x0.5, skip spikes | 784 | 82% | +159.46 | +2.1% | 1.22 | 1.11 | -59 | +218 | 92% | 0.1522 | 0.1432 |
| Time-of-day vol x0.5, against trend + skip spikes | 430 | 84% | +156.67 | +3.7% | 1.67 | 1.52 | -21 | +177 | 93% | 0.1406 | 0.135 |
| Market favorite (no model) | 112 | 67% | +115.48 | +10.3% | 1.3 | 1.3 | +69 | +46 | – | – | 0.2033 |
| Time-of-day vol x0.5 | 1228 | 81% | +82.36 | +0.7% | 0.49 | 1.22 | -149 | +231 | 92% | 0.1607 | 0.148 |
| Vol x0.5, weekends only | 147 | 84% | +80.00 | +5.6% | 1.05 | 1.21 | -0 | +80 | 92% | 0.1273 | 0.1246 |
| Bayes price-level, 95% sure | 44 | 80% | +59.89 | +13.8% | 1.5 | 1.5 | +32 | +28 | 77% | 0.1514 | 0.1615 |
| Vol x0.5, skip spiked markets | 917 | 80% | +35.61 | +0.4% | 0.23 | -0.2 | -210 | +246 | 93% | 0.1739 | 0.1578 |
| Vol x0.5, against trend + skip spikes | 497 | 80% | +12.94 | +0.3% | 0.1 | -0.06 | -158 | +171 | 93% | 0.1756 | 0.1588 |
| Bayes: market prior + full vol | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Bayes: market prior + fat-tail | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Long-shot fade (no model) | 602 | 95% | -24.31 | -0.4% | -0.43 | -0.33 | -91 | +67 | – | – | 0.0448 |
| Bayes price-level, 99% sure | 3 | 0% | -29.77 | -100.0% | – | – | -10 | -20 | 72% | 0.5155 | 0.3521 |
| Combined: rolling best (past 6 months) | 261 | 79% | -31.06 | -1.2% | -0.36 | -0.52 | -88 | +57 | 93% | 0.1644 | 0.1537 |
| Vol x0.5, news days only | 83 | 75% | -46.16 | -5.7% | -0.93 | -1.27 | -30 | -17 | 92% | 0.2044 | 0.1751 |
| Vol x0.5, against the 24h trend | 699 | 78% | -70.46 | -1.0% | -0.48 | -0.58 | -273 | +203 | 92% | 0.184 | 0.1641 |
| Vol x0.75 | 397 | 76% | -75.86 | -1.9% | -0.5 | -0.69 | -178 | +102 | 88% | 0.1653 | 0.1511 |
| Fat-tail (actual past moves) | 334 | 66% | -76.18 | -2.3% | -0.33 | -0.35 | -225 | +148 | 78% | 0.1911 | 0.1761 |
| Vol x0.5, calm market only | 753 | 79% | -80.64 | -1.1% | -0.54 | -0.18 | -220 | +139 | 92% | 0.1782 | 0.1603 |
| Vol x0.5, 5c edge | 1693 | 79% | -88.41 | -0.5% | -0.4 | 0.02 | -380 | +291 | 92% | 0.1758 | 0.1585 |
| Vol x0.5, busy market only | 666 | 78% | -133.97 | -2.1% | -1.0 | -0.82 | -158 | +24 | 93% | 0.194 | 0.1683 |
| Vol x0.5, with the 24h trend | 720 | 78% | -144.15 | -2.1% | -1.04 | -1.1 | -117 | -27 | 92% | 0.1872 | 0.164 |
| Vol x0.5, skip news days | 1336 | 78% | -168.45 | -1.3% | -0.87 | -0.33 | -327 | +158 | 92% | 0.1844 | 0.1634 |
| Regime-scaled vol x0.5 | 1577 | 79% | -169.68 | -1.1% | -0.82 | 0.02 | -318 | +148 | 93% | 0.181 | 0.1601 |
| Fat-tail, moves x0.75 | 868 | 73% | -209.30 | -2.5% | -1.17 | -1.33 | -257 | +47 | 86% | 0.2057 | 0.1876 |
| Vol x0.5, skip news in window | 1396 | 78% | -209.77 | -1.5% | -1.05 | -0.6 | -381 | +171 | 92% | 0.186 | 0.1644 |
| Vol x0.5, NO only | 896 | 78% | -210.77 | -2.4% | -1.35 | -1.34 | -246 | +35 | 92% | 0.1844 | 0.1629 |
| Vol x0.5 (Bitcoin's winner) | 1419 | 78% | -214.61 | -1.6% | -1.07 | -0.7 | -390 | +175 | 92% | 0.1856 | 0.1641 |
| Full vol + 50% market blend | 97 | 23% | -223.31 | -22.1% | -0.87 | -0.71 | -341 | +117 | 34% | 0.1203 | 0.1089 |
| Vol x0.5, weekdays only | 1272 | 78% | -294.61 | -2.4% | -1.56 | -1.21 | -377 | +83 | 93% | 0.1924 | 0.1686 |
| Fat-tail, moves x0.5 | 1698 | 74% | -329.26 | -2.0% | -1.36 | -1.25 | -387 | +58 | 90% | 0.2075 | 0.1818 |
| Options vol x0.85, 5c gap | 431 | 56% | -411.93 | -9.5% | -1.06 | -0.88 | -568 | +156 | 66% | 0.1333 | 0.1195 |
| Options vol, NO only | 215 | 27% | -515.42 | -23.2% | -1.42 | -1.16 | -585 | +70 | 42% | 0.1203 | 0.0965 |
| Heavy-volume move (10c, 5x): follow | 408 | 60% | -515.48 | -12.7% | -3.13 | -2.95 | -244 | -272 | – | – | 0.1813 |
| Options vol, 8c gap | 198 | 17% | -571.14 | -27.7% | -1.48 | -1.17 | -716 | +145 | 35% | 0.1257 | 0.0908 |
| Vol x0.5, take profit 10c | 1419 | 81% | -607.98 | -4.4% | -3.49 | -2.93 | -576 | -32 | 92% | 0.1654 | 0.1534 |
| Combined: 5+ strategies agree | 1689 | 74% | -710.35 | -4.3% | -2.11 | -1.68 | -736 | +25 | 87% | 0.177 | 0.1598 |
| Vol x0.5, stop loss 25c | 1419 | 65% | -734.39 | -5.3% | -4.25 | -3.9 | -751 | +17 | 92% | 0.304 | 0.2367 |
| Heavy-volume move (10c, 5x): fade | 457 | 35% | -866.21 | -18.4% | -2.8 | -2.96 | -232 | -634 | – | – | 0.1646 |
| Full vol (v1 rule) | 216 | 28% | -872.28 | -39.2% | -3.16 | -2.8 | -714 | -158 | 46% | 0.1198 | 0.0887 |
| Heavy-volume move: follow | 745 | 57% | -991.30 | -13.3% | -3.93 | -3.57 | -483 | -508 | – | – | 0.1865 |
| Vol x0.5, take profit 15c / stop 15c | 1419 | 57% | -999.04 | -7.2% | -7.35 | -6.61 | -852 | -147 | 92% | 0.3713 | 0.2811 |
| Heavy-volume move: fade | 807 | 38% | -1046.20 | -12.7% | -2.48 | -2.92 | -311 | -735 | – | – | 0.1731 |
| Vol x0.5, stop loss 10c | 1419 | 47% | -1103.61 | -8.0% | -7.64 | -7.07 | -947 | -156 | 92% | 0.4558 | 0.3318 |
| Options vol, 5c gap | 387 | 22% | -1478.00 | -36.8% | -3.44 | -3.24 | -1214 | -264 | 38% | 0.1161 | 0.0897 |
| Vol x0.5, limit order | 714 | 57% | -1679.83 | -24.4% | -9.84 | -11.15 | -1092 | -588 | 92% | 0.3561 | 0.2675 |
| Vol x0.5, limit order (strict fill) | 693 | 56% | -1731.91 | -25.9% | -10.23 | -11.52 | -1108 | -624 | 92% | 0.3668 | 0.2744 |
| Vol x0.5 5c edge, limit order | 833 | 58% | -1872.63 | -23.3% | -10.15 | -11.62 | -1235 | -638 | 91% | 0.3419 | 0.2611 |
| Combined: 3+ strategies agree | 2403 | 66% | -1883.76 | -7.9% | -3.58 | -3.18 | -1294 | -590 | 84% | 0.1713 | 0.1574 |
| Kalshi price-spike fade (no model) | 1052 | 31% | -2307.19 | -21.3% | -4.75 | -4.42 | -789 | -1518 | – | – | 0.1702 |

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
| 0.3 | 2008 | -104.51 | -0.5% |
| 0.4 | 1774 | -291.16 | -1.7% |
| 0.5 | 1419 | -214.61 | -1.6% |
| 0.6 | 954 | -251.73 | -2.7% |
| 0.75 | 397 | -75.86 | -1.9% |
| 1.0 | 216 | -872.28 | -39.2% |

Sweep: time-of-day vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1683 | -34.40 | -0.2% |
| 0.5 | 1228 | +82.36 | +0.7% |
| 0.6 | 689 | -138.32 | -2.1% |
| 0.75 | 230 | -291.25 | -12.8% |
| 1.0 | 238 | -930.56 | -37.5% |

Sweep: fat-tail

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1953 | -149.42 | -0.8% |
| 0.5 | 1698 | -329.26 | -2.0% |
| 0.6 | 1361 | -140.47 | -1.1% |
| 0.75 | 868 | -209.30 | -2.5% |
| 0.9 | 490 | -240.63 | -5.0% |
| 1.0 | 334 | -76.18 | -2.3% |

Sweep: options vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 1336 | -403.79 | -3.1% |
| 0.7 | 868 | -378.73 | -4.5% |
| 0.8 | 520 | -437.24 | -8.5% |
| 0.9 | 371 | -660.83 | -17.5% |
| 1.0 | 387 | -1478.00 | -36.8% |
| 1.1 | 525 | -2863.09 | -52.1% |

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
| Quarter | 2026-Q4 | 6 | +17 | 83% |
| Price paid | 0.30-0.50 | 27 | +39 | 48% |
| Price paid | 0.50-0.70 | 58 | -5 | 62% |
| Price paid | 0.70-0.90 | 27 | +81 | 96% |
| Model vs market gap | no model | 112 | +115 | 67% |
| Side | yes | 112 | +115 | 67% |

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
| Quarter | 2026-Q4 | 65 | -257 | 29% |
| Price paid | 0.10-0.30 | 524 | -1988 | 13% |
| Price paid | 0.30-0.50 | 297 | -335 | 36% |
| Price paid | 0.50-0.70 | 178 | +21 | 60% |
| Price paid | 0.70-0.90 | 53 | -5 | 76% |
| Model vs market gap | no model | 1052 | -2307 | 31% |
| Side | no | 489 | -1267 | 34% |
| Side | yes | 563 | -1040 | 28% |

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
| Quarter | 2026-Q4 | 32 | +10 | 84% |
| Price paid | 0.50-0.70 | 34 | +61 | 79% |
| Price paid | 0.70-0.90 | 376 | +98 | 84% |
| Price paid | 0.90-1.01 | 20 | -1 | 90% |
| Model vs market gap | 0.05-0.10 | 7 | +8 | 100% |
| Model vs market gap | 0.10-0.20 | 385 | +152 | 85% |
| Model vs market gap | 0.20-0.35 | 37 | -8 | 73% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 211 | +133 | 87% |
| Side | yes | 219 | +23 | 81% |

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
| Quarter | 2026-Q4 | 99 | +25 | 82% |
| Price paid | 0.10-0.30 | 4 | -42 | 0% |
| Price paid | 0.50-0.70 | 135 | +35 | 69% |
| Price paid | 0.70-0.90 | 1047 | +68 | 82% |
| Price paid | 0.90-1.01 | 42 | +21 | 95% |
| Model vs market gap | 0.05-0.10 | 15 | -15 | 80% |
| Model vs market gap | 0.10-0.20 | 1086 | +122 | 82% |
| Model vs market gap | 0.20-0.35 | 126 | -29 | 72% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 618 | -20 | 80% |
| Side | yes | 610 | +102 | 82% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 2 | +2 | 100% |
| Quarter | 2025-Q3 | 5 | +5 | 100% |
| Quarter | 2025-Q4 | 1 | -10 | 0% |
| Quarter | 2026-Q2 | 12 | +24 | 75% |
| Quarter | 2026-Q3 | 17 | +29 | 76% |
| Quarter | 2026-Q4 | 7 | +10 | 86% |
| Price paid | 0.50-0.70 | 32 | +42 | 72% |
| Price paid | 0.70-0.90 | 5 | +11 | 100% |
| Price paid | 0.90-1.01 | 7 | +7 | 100% |
| Model vs market gap | 0.05-0.10 | 22 | +57 | 96% |
| Model vs market gap | 0.10-0.20 | 22 | +2 | 64% |
| Side | no | 2 | -9 | 50% |
| Side | yes | 42 | +69 | 81% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 76 | -4 | 80% |
| Quarter | 2025-Q4 | 81 | -86 | 73% |
| Quarter | 2026-Q2 | 26 | -16 | 62% |
| Quarter | 2026-Q3 | 46 | +64 | 94% |
| Quarter | 2026-Q4 | 32 | +10 | 84% |
| Price paid | 0.30-0.50 | 3 | -5 | 33% |
| Price paid | 0.50-0.70 | 28 | -33 | 57% |
| Price paid | 0.70-0.90 | 216 | +4 | 82% |
| Price paid | 0.90-1.01 | 14 | +3 | 93% |
| Model vs market gap | 0.05-0.10 | 6 | +7 | 100% |
| Model vs market gap | 0.10-0.20 | 207 | -2 | 82% |
| Model vs market gap | 0.20-0.35 | 22 | -19 | 68% |
| Model vs market gap | no model | 26 | -16 | 62% |
| Side | no | 116 | +69 | 87% |
| Side | yes | 145 | -100 | 72% |
