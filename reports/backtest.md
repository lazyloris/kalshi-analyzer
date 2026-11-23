# Backtest (2026-11-23)

Flat $10 per trade at the ask plus Kalshi fees, held to settlement. Prices are real hourly Kalshi quotes. Forecasts are archived NWS-blend (NBM) runs 1-2 days old. Bias/sigma learned only from earlier days.

## Live paper books vs backtest

| Book | Settled | Open | Live P&L | Live return/$ | Backtest rule | Backtest return/$ |
|---|---|---|---|---|---|---|
| bitcoin | 28 | 4 | +16.04 | +5.9% | c_vol50 | +0.5% |
| bitcoin_tod | 28 | 4 | +13.14 | +4.8% | s_combo_tod | +2.7% |
| ethereum | 28 | 4 | -11.30 | -4.1% | a_vol50 | -1.5% |
| ethereum_tod | 28 | 4 | -21.44 | -7.8% | s_combo_tod | +2.1% |
| weather_high | 146 | 15 | -38.46 | -2.8% | fade | +0.1% |
| weather_low | 79 | 7 | -19.21 | -2.5% | fade | +0.3% |

Live numbers need ~100 settled trades before they mean much.

## Weather: daily highs

3807 events, 2025-03-21 to 2026-11-22.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Kalshi price-spike fade (no model) (+159 on 493 trades).

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 493 | 45% | +158.55 | +3.1% | 0.5 | 0.32 | -148 | +307 | – | – | 0.1961 |
| Long-shot fade (no model) | 5031 | 95% | +35.49 | +0.1% | 0.24 | 0.3 | +56 | -21 | – | – | 0.0435 |
| Bayes: market prior + forecast | 2 | 50% | -4.85 | -24.4% | -0.29 | -0.29 | -10 | +5 | 74% | 0.3459 | 0.3305 |
| Bayes price-level, 99% sure | 1272 | 91% | -171.81 | -1.4% | -1.61 | -1.66 | -15 | -157 | 94% | 0.0785 | 0.0772 |
| Combined: rolling best (past 6 months) | 2938 | 94% | -222.70 | -0.8% | -1.38 | -1.54 | +86 | -309 | – | – | 0.0492 |
| Market favorite YES (no model) | 4691 | 51% | -238.46 | -0.5% | -0.35 | -0.35 | -267 | +28 | – | – | 0.2428 |
| Heavy-volume move (10c, 5x): fade | 317 | 48% | -245.95 | -7.6% | -1.03 | -0.8 | -151 | -95 | – | – | 0.1839 |
| Bayes price-level, 95% sure | 2216 | 88% | -346.82 | -1.6% | -2.03 | -1.87 | -198 | -149 | 91% | 0.0957 | 0.0942 |
| Heavy-volume move (10c, 5x): follow | 299 | 50% | -374.62 | -12.4% | -1.98 | -1.84 | -289 | -86 | – | – | 0.1947 |
| Long-shot fade, limit order | 2878 | 92% | -488.08 | -1.8% | -3.34 | -3.34 | -203 | -285 | – | – | 0.0733 |
| Heavy-volume move: fade | 1562 | 48% | -1083.50 | -6.9% | -2.06 | -2.55 | -1050 | -34 | – | – | 0.1878 |
| Combined: 5+ strategies agree | 5081 | 49% | -1116.22 | -2.2% | -1.43 | -1.01 | -441 | -675 | 60% | 0.2226 | 0.236 |
| Heavy-volume move: follow | 1528 | 49% | -1659.85 | -10.8% | -3.73 | -3.48 | -760 | -899 | – | – | 0.192 |
| Favorite, stop loss 25c | 4691 | 42% | -2474.79 | -5.2% | -3.91 | -3.91 | -2234 | -240 | – | – | 0.2416 |
| Favorite, take profit 10c | 4691 | 70% | -3659.32 | -7.7% | -8.37 | -8.37 | -2358 | -1301 | – | – | 0.261 |
| Forecast bracket YES | 788 | 10% | -3769.72 | -45.5% | -6.79 | -6.79 | -1829 | -1941 | 33% | 0.1453 | 0.0894 |
| Favorite, stop loss 10c | 4691 | 28% | -4328.06 | -9.1% | -8.9 | -8.9 | -3081 | -1247 | – | – | 0.2371 |
| Favorite, take profit 15c / stop 15c | 4691 | 47% | -5509.04 | -11.6% | -15.23 | -15.23 | -3867 | -1642 | – | – | 0.2513 |
| Market favorite, limit order | 3820 | 39% | -6573.58 | -17.4% | -10.15 | -10.15 | -4328 | -2246 | – | – | 0.2366 |
| v2 + disagreement cap | 3369 | 33% | -8533.51 | -24.7% | -7.83 | -6.91 | -4263 | -4270 | 54% | 0.2009 | 0.1575 |
| v1 (what we ran live) | 4659 | 34% | -9278.54 | -19.4% | -7.37 | -6.73 | -4677 | -4602 | 63% | 0.2632 | 0.1662 |
| v2 + 50% market blend | 3773 | 31% | -9482.00 | -24.4% | -8.34 | -7.18 | -4820 | -4662 | 46% | 0.1908 | 0.1656 |
| v2 calibrated | 4250 | 32% | -10262.64 | -23.5% | -8.65 | -7.6 | -5281 | -4982 | 58% | 0.2449 | 0.1682 |
| Combined: 3+ strategies agree | 9760 | 46% | -10701.81 | -10.8% | -7.78 | -5.76 | -3936 | -6765 | 62% | 0.2719 | 0.1936 |

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
| 0.6 | 4235 | -9673.82 | -22.3% |
| 0.8 | 4092 | -10041.34 | -23.9% |
| 1.0 | 4250 | -10262.64 | -23.5% |
| 1.25 | 4509 | -9052.96 | -19.6% |
| 1.5 | 4666 | -8035.88 | -16.9% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 5172 | -11841.41 | -22.3% |
| blend 0.0, edge 0.05 | 4848 | -11173.60 | -22.5% |
| blend 0.0, edge 0.08 | 4250 | -10262.64 | -23.5% |
| blend 0.25, edge 0.03 | 4899 | -11572.44 | -23.0% |
| blend 0.25, edge 0.05 | 4393 | -10576.30 | -23.5% |
| blend 0.25, edge 0.08 | 3459 | -9127.45 | -25.7% |
| blend 0.5, edge 0.03 | 4227 | -10344.66 | -23.8% |
| blend 0.5, edge 0.05 | 3284 | -8631.33 | -25.6% |
| blend 0.5, edge 0.08 | 2007 | -4804.51 | -23.3% |
| blend 0.75, edge 0.03 | 2000 | -5483.25 | -26.6% |
| blend 0.75, edge 0.05 | 876 | -1997.18 | -22.0% |
| blend 0.75, edge 0.08 | 234 | -593.14 | -24.4% |

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
| Quarter | 2026-Q4 | 935 | -2313 | 32% |
| Price paid | 0.00-0.10 | 854 | -3135 | 5% |
| Price paid | 0.10-0.30 | 893 | -4153 | 10% |
| Price paid | 0.30-0.50 | 918 | -1348 | 37% |
| Price paid | 0.50-0.70 | 1251 | -1381 | 54% |
| Price paid | 0.70-0.90 | 333 | -236 | 71% |
| Price paid | 0.90-1.01 | 1 | -10 | 0% |
| Model vs market gap | 0.05-0.10 | 62 | -14 | 16% |
| Model vs market gap | 0.10-0.20 | 2127 | -5904 | 32% |
| Model vs market gap | 0.20-0.35 | 1623 | -3439 | 35% |
| Model vs market gap | 0.35-1.01 | 438 | -906 | 30% |
| Side | no | 2583 | -3232 | 48% |
| Side | yes | 1667 | -7031 | 8% |

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
| Quarter | 2026-Q4 | 43 | -48 | 46% |
| Price paid | 0.10-0.30 | 176 | -34 | 20% |
| Price paid | 0.30-0.50 | 132 | +24 | 42% |
| Price paid | 0.50-0.70 | 144 | +171 | 69% |
| Price paid | 0.70-0.90 | 41 | -2 | 76% |
| Model vs market gap | no model | 493 | +159 | 45% |
| Side | no | 285 | +133 | 58% |
| Side | yes | 208 | +25 | 26% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 37 | -76 | 60% |
| Quarter | 2025-Q3 | 211 | +7 | 95% |
| Quarter | 2025-Q4 | 159 | -19 | 91% |
| Quarter | 2026-Q1 | 484 | -129 | 87% |
| Quarter | 2026-Q2 | 530 | -94 | 88% |
| Quarter | 2026-Q3 | 538 | -33 | 89% |
| Quarter | 2026-Q4 | 257 | -3 | 88% |
| Price paid | 0.30-0.50 | 21 | -85 | 29% |
| Price paid | 0.50-0.70 | 35 | +18 | 54% |
| Price paid | 0.70-0.90 | 684 | -169 | 82% |
| Price paid | 0.90-1.01 | 1476 | -110 | 93% |
| Model vs market gap | 0.00-0.05 | 1987 | -178 | 90% |
| Model vs market gap | 0.05-0.10 | 208 | -85 | 77% |
| Model vs market gap | 0.10-0.20 | 21 | -85 | 29% |
| Side | no | 2158 | -260 | 90% |
| Side | yes | 58 | -87 | 43% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 544 | +57 | 96% |
| Quarter | 2025-Q4 | 268 | -37 | 94% |
| Quarter | 2026-Q1 | 968 | +74 | 96% |
| Quarter | 2026-Q2 | 1056 | -99 | 94% |
| Quarter | 2026-Q3 | 59 | -169 | 41% |
| Quarter | 2026-Q4 | 43 | -48 | 46% |
| Price paid | 0.10-0.30 | 28 | -246 | 4% |
| Price paid | 0.30-0.50 | 22 | +75 | 55% |
| Price paid | 0.50-0.70 | 39 | -19 | 59% |
| Price paid | 0.70-0.90 | 13 | -26 | 62% |
| Price paid | 0.90-1.01 | 2836 | -6 | 95% |
| Model vs market gap | no model | 2938 | -223 | 94% |
| Side | no | 2899 | +2 | 94% |
| Side | yes | 39 | -225 | 18% |

Forecast error (actual minus NBM forecast)

| City | Entry | n | Bias | RMSE |
|---|---|---|---|---|
| Austin | day before 10am | 254 | +1.77 | 3.33 |
| Austin | same day 8am | 256 | +1.49 | 2.93 |
| Chicago | day before 10am | 254 | +1.52 | 3.42 |
| Chicago | same day 8am | 252 | +1.33 | 2.85 |
| Denver | day before 10am | 255 | +1.75 | 3.39 |
| Denver | same day 8am | 252 | +1.69 | 2.96 |
| Los Angeles | day before 10am | 253 | +2.28 | 3.82 |
| Los Angeles | same day 8am | 255 | +2.27 | 3.55 |
| Miami | same day 8am | 255 | +2.01 | 2.63 |
| New York | same day 8am | 252 | -0.17 | 2.47 |
| Philadelphia | same day 8am | 251 | +1.75 | 2.88 |

## Weather: daily lows

2291 events, 2025-12-13 to 2026-11-22.

**Verdict:** Long-shot fade (no model): +103 on 3256 trades (+0.3% per $ staked, t=0.94), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 153 | 54% | +265.40 | +17.1% | 1.4 | 1.27 | -53 | +318 | – | – | 0.2107 |
| Combined: rolling best (past 6 months) | 1646 | 78% | +241.53 | +1.5% | 0.83 | 0.9 | +166 | +76 | – | – | 0.123 |
| Long-shot fade (no model) | 3256 | 96% | +103.26 | +0.3% | 0.94 | 1.04 | +82 | +21 | – | – | 0.0366 |
| Heavy-volume move: follow | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Heavy-volume move: fade | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Heavy-volume move (10c, 5x): follow | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Heavy-volume move (10c, 5x): fade | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Bayes: market prior + forecast | 1 | 0% | -10.25 | -100.0% | – | – | +0 | -10 | 49% | 0.2401 | 0.16 |
| Bayes price-level, 99% sure | 211 | 94% | -19.41 | -1.0% | -0.58 | -0.49 | -12 | -8 | 96% | 0.0543 | 0.0542 |
| Bayes price-level, 95% sure | 380 | 94% | -20.13 | -0.5% | -0.39 | -0.33 | -49 | +29 | 96% | 0.0576 | 0.0575 |
| Long-shot fade, limit order | 1718 | 93% | -205.68 | -1.3% | -1.9 | -1.54 | -59 | -146 | – | – | 0.0666 |
| Combined: 5+ strategies agree | 2250 | 46% | -503.46 | -2.2% | -0.95 | -1.06 | +520 | -1023 | 55% | 0.2379 | 0.238 |
| Market favorite YES (no model) | 2184 | 47% | -723.95 | -3.3% | -1.45 | -1.45 | +408 | -1132 | – | – | 0.24 |
| Forecast bracket YES | 569 | 15% | -1676.73 | -28.1% | -3.48 | -3.48 | -997 | -680 | 35% | 0.1625 | 0.1227 |
| Favorite, take profit 10c | 2184 | 62% | -2895.89 | -13.1% | -8.44 | -8.44 | -1093 | -1803 | – | – | 0.2663 |
| Market favorite, limit order | 1815 | 36% | -3176.06 | -17.6% | -6.57 | -6.57 | -909 | -2267 | – | – | 0.2268 |
| v2 + 50% market blend | 1956 | 30% | -3990.23 | -19.8% | -4.3 | -4.1 | -1184 | -2806 | 41% | 0.1578 | 0.1431 |
| Favorite, stop loss 25c | 2184 | 28% | -5470.37 | -24.7% | -13.1 | -13.1 | -2257 | -3214 | – | – | 0.2289 |
| v2 calibrated | 2701 | 32% | -5851.17 | -21.1% | -5.76 | -5.29 | -1848 | -4003 | 52% | 0.1994 | 0.1495 |
| Favorite, stop loss 10c | 2184 | 14% | -5934.70 | -26.8% | -21.03 | -21.03 | -2932 | -3002 | – | – | 0.2165 |
| v2 + disagreement cap | 2341 | 32% | -6184.60 | -25.7% | -6.88 | -6.97 | -2274 | -3911 | 50% | 0.1764 | 0.143 |
| Combined: 3+ strategies agree | 4654 | 41% | -6420.37 | -13.5% | -6.14 | -5.34 | -2160 | -4260 | 57% | 0.2329 | 0.1857 |
| Favorite, take profit 15c / stop 15c | 2184 | 28% | -6620.66 | -29.9% | -27.99 | -27.99 | -3371 | -3250 | – | – | 0.2351 |
| v1 (what we ran live) | 3952 | 32% | -10829.70 | -26.7% | -9.68 | -8.71 | -4523 | -6307 | 57% | 0.2268 | 0.1484 |

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
| 0.6 | 3462 | -5395.04 | -15.3% |
| 0.8 | 2761 | -5089.44 | -18.0% |
| 1.0 | 2701 | -5851.17 | -21.1% |
| 1.25 | 3143 | -7154.87 | -22.2% |
| 1.5 | 3681 | -8951.42 | -23.7% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 4143 | -9509.74 | -22.4% |
| blend 0.0, edge 0.05 | 3557 | -8465.47 | -23.2% |
| blend 0.0, edge 0.08 | 2701 | -5851.17 | -21.1% |
| blend 0.25, edge 0.03 | 3552 | -8400.73 | -23.0% |
| blend 0.25, edge 0.05 | 2787 | -5979.78 | -20.8% |
| blend 0.25, edge 0.08 | 1809 | -3640.16 | -19.5% |
| blend 0.5, edge 0.03 | 2436 | -5229.19 | -20.8% |
| blend 0.5, edge 0.05 | 1574 | -3169.55 | -19.5% |
| blend 0.5, edge 0.08 | 761 | -612.99 | -7.8% |
| blend 0.75, edge 0.03 | 654 | -797.16 | -11.7% |
| blend 0.75, edge 0.05 | 262 | -635.64 | -23.3% |
| blend 0.75, edge 0.08 | 57 | -395.30 | -66.5% |

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
| Quarter | 2026-Q4 | 486 | -725 | 32% |
| Price paid | 0.00-0.10 | 577 | -2216 | 5% |
| Price paid | 0.10-0.30 | 830 | -2541 | 12% |
| Price paid | 0.30-0.50 | 324 | -636 | 35% |
| Price paid | 0.50-0.70 | 670 | -334 | 58% |
| Price paid | 0.70-0.90 | 299 | -124 | 74% |
| Price paid | 0.90-1.01 | 1 | +1 | 100% |
| Model vs market gap | 0.05-0.10 | 37 | +39 | 22% |
| Model vs market gap | 0.10-0.20 | 1681 | -4704 | 31% |
| Model vs market gap | 0.20-0.35 | 811 | -554 | 35% |
| Model vs market gap | 0.35-1.01 | 172 | -632 | 24% |
| Side | no | 1276 | -974 | 56% |
| Side | yes | 1425 | -4877 | 10% |

Why: Long-shot fade (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q1 | 950 | -40 | 95% |
| Quarter | 2026-Q2 | 1044 | +162 | 97% |
| Quarter | 2026-Q3 | 976 | -12 | 96% |
| Quarter | 2026-Q4 | 286 | -8 | 96% |
| Price paid | 0.90-1.01 | 3256 | +103 | 96% |
| Model vs market gap | no model | 3256 | +103 | 96% |
| Side | no | 3256 | +103 | 96% |

Why: Kalshi price-spike fade (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q4 | 1 | -10 | 0% |
| Quarter | 2026-Q1 | 34 | -22 | 41% |
| Quarter | 2026-Q2 | 53 | +65 | 53% |
| Quarter | 2026-Q3 | 58 | +211 | 60% |
| Quarter | 2026-Q4 | 7 | +21 | 71% |
| Price paid | 0.10-0.30 | 46 | +145 | 26% |
| Price paid | 0.30-0.50 | 29 | +54 | 48% |
| Price paid | 0.50-0.70 | 53 | +25 | 64% |
| Price paid | 0.70-0.90 | 25 | +41 | 88% |
| Model vs market gap | no model | 153 | +265 | 54% |
| Side | no | 96 | +56 | 65% |
| Side | yes | 57 | +210 | 35% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q2 | 98 | -13 | 94% |
| Quarter | 2026-Q3 | 195 | +19 | 95% |
| Quarter | 2026-Q4 | 87 | -27 | 90% |
| Price paid | 0.50-0.70 | 2 | -5 | 50% |
| Price paid | 0.70-0.90 | 15 | +14 | 80% |
| Price paid | 0.90-1.01 | 363 | -29 | 94% |
| Model vs market gap | 0.00-0.05 | 303 | +2 | 95% |
| Model vs market gap | 0.05-0.10 | 60 | -31 | 90% |
| Model vs market gap | 0.10-0.20 | 17 | +9 | 76% |
| Side | no | 363 | -29 | 94% |
| Side | yes | 17 | +9 | 76% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q2 | 663 | +232 | 51% |
| Quarter | 2026-Q3 | 976 | -12 | 96% |
| Quarter | 2026-Q4 | 7 | +21 | 71% |
| Price paid | 0.10-0.30 | 2 | -21 | 0% |
| Price paid | 0.30-0.50 | 445 | +373 | 48% |
| Price paid | 0.50-0.70 | 207 | -114 | 56% |
| Price paid | 0.70-0.90 | 16 | +16 | 81% |
| Price paid | 0.90-1.01 | 976 | -12 | 96% |
| Model vs market gap | no model | 1646 | +242 | 78% |
| Side | no | 980 | +27 | 96% |
| Side | yes | 666 | +215 | 51% |

Forecast error (actual minus NBM forecast)

| City | Entry | n | Bias | RMSE |
|---|---|---|---|---|
| Austin | day before 10am | 254 | -2.73 | 4.2 |
| Austin | day before 8pm | 256 | -2.76 | 3.99 |
| Chicago | day before 10am | 254 | -1.57 | 2.98 |
| Chicago | day before 8pm | 256 | -1.37 | 2.63 |
| Denver | day before 10am | 255 | -4.03 | 5.3 |
| Denver | day before 8pm | 256 | -3.87 | 5.11 |
| Los Angeles | day before 10am | 254 | +0.37 | 1.71 |
| Los Angeles | day before 8pm | 256 | +0.48 | 1.6 |
| Miami | day before 8pm | 254 | -0.97 | 2.37 |
| New York | day before 8pm | 256 | -1.50 | 2.72 |
| Philadelphia | day before 8pm | 256 | +0.41 | 2.2 |

## Crypto: Bitcoin 5pm price

610 events, 2025-03-22 to 2026-11-22.

**Verdict:** Vol x0.5, weekends only: +194 on 246 trades (+8.1% per $ staked, t=2.71), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Time-of-day vol x0.5 | 1572 | 80% | +311.95 | +2.0% | 1.54 | 1.76 | -115 | +427 | 92% | 0.1726 | 0.1593 |
| Time-of-day vol x0.5, skip spikes | 978 | 81% | +253.27 | +2.7% | 1.65 | 1.51 | -141 | +394 | 92% | 0.1642 | 0.1542 |
| Regime-scaled vol x0.5 | 1970 | 78% | +195.02 | +1.0% | 0.85 | 0.88 | -251 | +446 | 93% | 0.1885 | 0.1673 |
| Vol x0.5, weekends only | 246 | 85% | +193.94 | +8.1% | 2.71 | 2.55 | +34 | +160 | 91% | 0.1179 | 0.1257 |
| Time-of-day vol x0.5, against trend + skip spikes | 515 | 82% | +156.18 | +3.1% | 1.41 | 1.4 | -115 | +271 | 92% | 0.1589 | 0.1495 |
| Bayes price-level, 95% sure | 678 | 92% | +131.50 | +2.0% | 1.68 | 0.92 | +9 | +123 | 93% | 0.0754 | 0.0763 |
| Vol x0.5, skip spiked markets | 1109 | 79% | +125.16 | +1.2% | 0.72 | 0.86 | -164 | +289 | 93% | 0.1831 | 0.1633 |
| Vol x0.5, calm market only | 1046 | 79% | +89.34 | +0.9% | 0.55 | 0.71 | -105 | +194 | 92% | 0.1777 | 0.1606 |
| Vol x0.5 | 1802 | 78% | +86.92 | +0.5% | 0.39 | 0.51 | -306 | +393 | 93% | 0.1898 | 0.1675 |
| Long-shot fade (no model) | 1323 | 96% | +79.15 | +0.6% | 1.17 | 1.12 | -42 | +121 | – | – | 0.0344 |
| Bayes price-level, 99% sure | 341 | 92% | +74.87 | +2.3% | 1.34 | 1.23 | +36 | +39 | 93% | 0.0762 | 0.0777 |
| Vol x0.5, against the 24h trend | 836 | 79% | +74.35 | +0.9% | 0.48 | 0.77 | -196 | +271 | 93% | 0.1863 | 0.1656 |
| Vol x0.5, skip news in window | 1778 | 78% | +67.52 | +0.4% | 0.3 | 0.43 | -326 | +394 | 93% | 0.1903 | 0.1677 |
| Vol x0.5, against trend + skip spikes | 586 | 80% | +64.98 | +1.1% | 0.51 | 0.6 | -80 | +144 | 93% | 0.1794 | 0.16 |
| Combined: rolling best (past 6 months) | 309 | 80% | +59.47 | +2.0% | 0.71 | -0.2 | -60 | +119 | 92% | 0.1674 | 0.1534 |
| Vol x0.5, skip news days | 1697 | 78% | +56.14 | +0.3% | 0.25 | 0.38 | -285 | +341 | 93% | 0.19 | 0.1672 |
| Vol x0.5, news days only | 105 | 78% | +30.78 | +3.0% | 0.58 | 0.56 | -1 | +32 | 93% | 0.1865 | 0.1727 |
| Vol x0.5, with the 24h trend | 966 | 78% | +12.57 | +0.1% | 0.09 | -0.4 | -118 | +130 | 93% | 0.1929 | 0.1692 |
| Vol x0.5, busy market only | 756 | 76% | -2.42 | -0.0% | -0.02 | -0.03 | -186 | +184 | 93% | 0.2067 | 0.1771 |
| Bayes: market prior + full vol | 3 | 67% | -6.07 | -20.9% | -0.53 | -0.69 | +2 | -8 | 92% | 0.2927 | 0.2732 |
| Bayes: market prior + fat-tail | 15 | 60% | -34.86 | -23.6% | -1.39 | -1.04 | -18 | -17 | 86% | 0.3165 | 0.2655 |
| Fat-tail, moves x0.5 | 1892 | 73% | -37.37 | -0.2% | -0.15 | -0.22 | -189 | +151 | 89% | 0.2228 | 0.1956 |
| Vol x0.5, weekdays only | 1556 | 77% | -107.02 | -0.7% | -0.51 | -0.5 | -298 | +191 | 93% | 0.2012 | 0.1741 |
| Fat-tail, moves x0.75 | 1204 | 73% | -130.15 | -1.1% | -0.57 | -0.56 | -213 | +83 | 86% | 0.2067 | 0.1902 |
| Vol x0.5, stop loss 25c | 1802 | 65% | -420.09 | -2.4% | -2.26 | -2.43 | -736 | +316 | 93% | 0.3045 | 0.2339 |
| Vol x0.75 | 818 | 72% | -474.82 | -5.9% | -2.12 | -2.49 | -346 | -129 | 86% | 0.1707 | 0.1537 |
| Fat-tail (actual past moves) | 663 | 59% | -596.04 | -9.0% | -1.85 | -1.27 | -588 | -8 | 73% | 0.198 | 0.1794 |
| Heavy-volume move: follow | 1250 | 62% | -645.27 | -5.2% | -1.99 | -1.3 | -576 | -70 | – | – | 0.1837 |
| Vol x0.5, take profit 10c | 1802 | 81% | -708.99 | -4.0% | -3.64 | -3.24 | -689 | -20 | 93% | 0.1654 | 0.155 |
| Heavy-volume move (10c, 5x): follow | 743 | 60% | -846.03 | -11.4% | -3.84 | -2.88 | -509 | -337 | – | – | 0.1831 |
| Combined: 5+ strategies agree | 2293 | 71% | -1006.77 | -4.5% | -2.36 | -3.3 | -992 | -15 | 84% | 0.176 | 0.1568 |
| Vol x0.5, stop loss 10c | 1802 | 47% | -1011.91 | -5.8% | -6.63 | -6.64 | -1062 | +50 | 93% | 0.4571 | 0.324 |
| Vol x0.5, take profit 15c / stop 15c | 1802 | 57% | -1097.91 | -6.2% | -7.38 | -7.52 | -1093 | -5 | 93% | 0.3706 | 0.2747 |
| v1 + 50% market blend | 300 | 33% | -1116.97 | -36.3% | -4.06 | -3.84 | -614 | -503 | 44% | 0.1127 | 0.1013 |
| Options vol x0.85, 5c gap | 833 | 56% | -1179.90 | -14.1% | -2.93 | -2.67 | -723 | -457 | 66% | 0.1222 | 0.1115 |
| Heavy-volume move (10c, 5x): fade | 789 | 37% | -1309.29 | -16.2% | -3.24 | -3.19 | -665 | -644 | – | – | 0.1738 |
| v1 (what we ran live) | 468 | 40% | -1356.54 | -28.4% | -3.83 | -3.44 | -1055 | -301 | 55% | 0.1261 | 0.0996 |
| Options vol, 8c gap | 422 | 24% | -1418.58 | -32.4% | -3.42 | -2.7 | -1067 | -352 | 40% | 0.1118 | 0.0845 |
| Options vol, NO only | 601 | 32% | -1743.78 | -28.2% | -3.74 | -3.31 | -1202 | -542 | 46% | 0.1242 | 0.1033 |
| Vol x0.5, limit order | 966 | 60% | -1794.01 | -19.2% | -8.94 | -9.36 | -1122 | -672 | 93% | 0.3455 | 0.256 |
| Vol x0.5, limit order (strict fill) | 929 | 58% | -1914.05 | -21.3% | -9.67 | -9.86 | -1160 | -754 | 92% | 0.359 | 0.2636 |
| Vol x0.5 5c edge, limit order | 1056 | 60% | -2040.10 | -20.0% | -9.69 | -10.07 | -1273 | -767 | 92% | 0.3376 | 0.2525 |
| Options vol, 5c gap | 691 | 32% | -2138.29 | -30.0% | -4.54 | -4.43 | -1342 | -797 | 45% | 0.114 | 0.0937 |
| Heavy-volume move: fade | 1303 | 36% | -2301.32 | -17.2% | -4.33 | -4.48 | -871 | -1430 | – | – | 0.1764 |
| Combined: 3+ strategies agree | 3363 | 65% | -2607.00 | -7.8% | -4.47 | -4.99 | -2040 | -567 | 82% | 0.1738 | 0.1558 |
| Kalshi price-spike fade (no model) | 1262 | 30% | -3263.17 | -25.1% | -6.11 | -5.7 | -1689 | -1574 | – | – | 0.1508 |

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
| 0.4 | 2000 | +49.45 | +0.2% |
| 0.5 | 1802 | +86.92 | +0.5% |
| 0.6 | 1432 | -223.78 | -1.6% |
| 0.75 | 818 | -474.82 | -5.9% |
| 1.0 | 468 | -1356.54 | -28.4% |
| 1.25 | 555 | -2413.10 | -41.6% |

Sweep: options vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 1622 | -198.59 | -1.2% |
| 0.7 | 1309 | -706.49 | -5.5% |
| 0.8 | 968 | -860.49 | -8.9% |
| 0.9 | 761 | -1582.39 | -20.5% |
| 1.0 | 691 | -2138.29 | -30.0% |
| 1.1 | 763 | -2925.41 | -36.8% |

Sweep: time-of-day vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1992 | +64.54 | +0.3% |
| 0.5 | 1572 | +311.95 | +2.0% |
| 0.6 | 1058 | +310.43 | +3.0% |
| 0.75 | 444 | -0.12 | -0.0% |
| 1.0 | 332 | -1047.55 | -30.7% |

Sweep: fat-tail

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 2090 | -56.27 | -0.3% |
| 0.5 | 1892 | -37.37 | -0.2% |
| 0.6 | 1651 | +44.99 | +0.3% |
| 0.75 | 1204 | -130.15 | -1.1% |
| 0.9 | 818 | -594.50 | -7.4% |
| 1.0 | 663 | -596.04 | -9.0% |

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
| 2026-Q4 | 104 | 1.385 |

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
| Quarter | 2026-Q4 | 67 | +119 | 51% |
| Price paid | 0.00-0.10 | 65 | -414 | 3% |
| Price paid | 0.10-0.30 | 196 | -996 | 8% |
| Price paid | 0.30-0.50 | 3 | -9 | 33% |
| Price paid | 0.50-0.70 | 14 | +14 | 71% |
| Price paid | 0.70-0.90 | 189 | +47 | 83% |
| Price paid | 0.90-1.01 | 1 | +1 | 100% |
| Model vs market gap | 0.05-0.10 | 22 | +190 | 59% |
| Model vs market gap | 0.10-0.20 | 408 | -1275 | 40% |
| Model vs market gap | 0.20-0.35 | 38 | -272 | 24% |
| Side | no | 306 | -805 | 40% |
| Side | yes | 162 | -552 | 39% |

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
| Quarter | 2026-Q4 | 157 | +93 | 80% |
| Price paid | 0.00-0.10 | 2 | -21 | 0% |
| Price paid | 0.10-0.30 | 3 | -32 | 0% |
| Price paid | 0.30-0.50 | 2 | +1 | 50% |
| Price paid | 0.50-0.70 | 217 | +181 | 73% |
| Price paid | 0.70-0.90 | 1569 | -40 | 79% |
| Price paid | 0.90-1.01 | 9 | -2 | 89% |
| Model vs market gap | 0.05-0.10 | 15 | -12 | 80% |
| Model vs market gap | 0.10-0.20 | 1243 | +2 | 80% |
| Model vs market gap | 0.20-0.35 | 543 | +92 | 75% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 1016 | +64 | 78% |
| Side | yes | 786 | +22 | 78% |

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
| Quarter | 2026-Q4 | 28 | +62 | 93% |
| Price paid | 0.00-0.10 | 2 | -21 | 0% |
| Price paid | 0.10-0.30 | 3 | -32 | 0% |
| Price paid | 0.30-0.50 | 1 | -10 | 0% |
| Price paid | 0.50-0.70 | 29 | +115 | 93% |
| Price paid | 0.70-0.90 | 205 | +146 | 86% |
| Price paid | 0.90-1.01 | 6 | -5 | 83% |
| Model vs market gap | 0.05-0.10 | 5 | -17 | 60% |
| Model vs market gap | 0.10-0.20 | 192 | +133 | 86% |
| Model vs market gap | 0.20-0.35 | 48 | +74 | 83% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 154 | +207 | 88% |
| Side | yes | 92 | -13 | 79% |

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
| Quarter | 2026-Q4 | 118 | -258 | 32% |
| Price paid | 0.10-0.30 | 703 | -3078 | 12% |
| Price paid | 0.30-0.50 | 297 | -454 | 34% |
| Price paid | 0.50-0.70 | 186 | +143 | 65% |
| Price paid | 0.70-0.90 | 76 | +126 | 90% |
| Model vs market gap | no model | 1262 | -3263 | 30% |
| Side | no | 609 | -1288 | 42% |
| Side | yes | 653 | -1976 | 18% |

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
| Quarter | 2026-Q4 | 51 | +1 | 78% |
| Price paid | 0.10-0.30 | 1 | -11 | 0% |
| Price paid | 0.50-0.70 | 41 | +29 | 73% |
| Price paid | 0.70-0.90 | 468 | +155 | 83% |
| Price paid | 0.90-1.01 | 5 | -17 | 60% |
| Model vs market gap | 0.05-0.10 | 12 | -4 | 83% |
| Model vs market gap | 0.10-0.20 | 428 | +146 | 83% |
| Model vs market gap | 0.20-0.35 | 75 | +14 | 76% |
| Side | no | 290 | +135 | 83% |
| Side | yes | 225 | +21 | 80% |

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
| Quarter | 2026-Q4 | 182 | +73 | 81% |
| Price paid | 0.10-0.30 | 2 | -21 | 0% |
| Price paid | 0.30-0.50 | 2 | +1 | 50% |
| Price paid | 0.50-0.70 | 139 | +132 | 74% |
| Price paid | 0.70-0.90 | 1421 | +213 | 81% |
| Price paid | 0.90-1.01 | 8 | -14 | 75% |
| Model vs market gap | 0.05-0.10 | 22 | -1 | 86% |
| Model vs market gap | 0.10-0.20 | 1267 | +209 | 81% |
| Model vs market gap | 0.20-0.35 | 282 | +100 | 76% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 905 | +270 | 81% |
| Side | yes | 667 | +42 | 80% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 93 | -18 | 91% |
| Quarter | 2025-Q3 | 21 | -41 | 71% |
| Quarter | 2025-Q4 | 4 | +2 | 75% |
| Quarter | 2026-Q1 | 7 | +10 | 100% |
| Quarter | 2026-Q2 | 140 | +32 | 91% |
| Quarter | 2026-Q3 | 238 | +115 | 94% |
| Quarter | 2026-Q4 | 175 | +31 | 91% |
| Price paid | 0.50-0.70 | 3 | +21 | 100% |
| Price paid | 0.70-0.90 | 188 | +100 | 89% |
| Price paid | 0.90-1.01 | 487 | +11 | 93% |
| Model vs market gap | 0.00-0.05 | 444 | +77 | 93% |
| Model vs market gap | 0.05-0.10 | 216 | +39 | 89% |
| Model vs market gap | 0.10-0.20 | 18 | +16 | 94% |
| Side | no | 281 | +92 | 94% |
| Side | yes | 397 | +39 | 90% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 139 | -79 | 74% |
| Quarter | 2026-Q1 | 52 | +90 | 90% |
| Quarter | 2026-Q2 | 48 | +70 | 90% |
| Quarter | 2026-Q3 | 19 | -23 | 74% |
| Quarter | 2026-Q4 | 51 | +1 | 78% |
| Price paid | 0.00-0.10 | 2 | -21 | 0% |
| Price paid | 0.10-0.30 | 2 | -21 | 0% |
| Price paid | 0.30-0.50 | 1 | -10 | 0% |
| Price paid | 0.50-0.70 | 39 | +67 | 80% |
| Price paid | 0.70-0.90 | 262 | +53 | 82% |
| Price paid | 0.90-1.01 | 3 | -8 | 67% |
| Model vs market gap | 0.05-0.10 | 11 | -18 | 73% |
| Model vs market gap | 0.10-0.20 | 226 | +104 | 83% |
| Model vs market gap | 0.20-0.35 | 71 | -31 | 70% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 170 | +117 | 83% |
| Side | yes | 139 | -58 | 76% |

## Weather: daily highs: late entries

2712 events, 2025-03-21 to 2026-11-22.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Late long-shot fade 1-4c (+29 on 974 trades).

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Late long-shot fade 1-4c | 974 | 99% | +28.97 | +0.3% | 0.93 | 1.41 | -6 | +35 | – | – | 0.0103 |
| Combined: 3+ strategies agree | 687 | 81% | +9.99 | +0.1% | 0.07 | 0.13 | +37 | -27 | 92% | 0.1687 | 0.1503 |
| Bayes price-level, 99% sure | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Late long-shot fade | 746 | 95% | -10.57 | -0.1% | -0.18 | -0.35 | -35 | +24 | – | – | 0.0435 |
| Late favorite 90-97c | 833 | 94% | -27.14 | -0.3% | -0.39 | -0.39 | -1 | -26 | – | – | 0.0524 |
| Bayes price-level, 95% sure | 67 | 82% | -53.09 | -8.1% | -1.52 | -1.04 | -8 | -45 | 93% | 0.1559 | 0.1446 |
| Combined: rolling best (past 6 months) | 553 | 97% | -59.28 | -1.1% | -1.42 | -1.29 | -66 | +6 | – | – | 0.0311 |
| Late favorite 80-90c | 442 | 85% | -64.71 | -1.5% | -0.77 | -0.77 | +3 | -67 | – | – | 0.1252 |
| Combined: 5+ strategies agree | 442 | 85% | -64.71 | -1.5% | -0.77 | -0.77 | +3 | -67 | – | – | 0.1252 |
| Late fav 80-90c, stop loss 25c | 442 | 82% | -94.49 | -2.2% | -1.18 | -1.18 | -24 | -70 | – | – | 0.1485 |
| Late fav 80-90c, stop loss 10c | 442 | 78% | -105.76 | -2.5% | -1.37 | -1.37 | -25 | -81 | – | – | 0.1751 |
| Late fav 80-90c, take profit 15c / stop 15c | 442 | 80% | -125.10 | -2.9% | -1.59 | -1.59 | -44 | -81 | – | – | 0.161 |
| Late fav 80-90c, take profit 10c | 442 | 86% | -136.63 | -3.2% | -1.67 | -1.67 | -27 | -110 | – | – | 0.1241 |
| Late favorite 50-80c | 550 | 67% | -176.57 | -3.2% | -1.09 | -1.09 | -100 | -76 | – | – | 0.2137 |
| Heavy-volume move (10c, 5x): follow | 853 | 72% | -485.54 | -5.8% | -2.46 | -2.21 | -354 | -132 | – | – | 0.1652 |
| Heavy-volume move: follow | 1326 | 69% | -543.65 | -4.1% | -1.76 | -1.08 | -496 | -48 | – | – | 0.1696 |
| Heavy-volume move (10c, 5x): fade | 1017 | 25% | -2269.32 | -21.5% | -4.11 | -3.99 | -842 | -1428 | – | – | 0.1487 |
| Heavy-volume move: fade | 1599 | 26% | -3473.33 | -21.0% | -5.05 | -4.91 | -2229 | -1244 | – | – | 0.1511 |

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
| Quarter | 2026-Q4 | 48 | -17 | 83% |
| Price paid | 0.70-0.90 | 387 | -66 | 84% |
| Price paid | 0.90-1.01 | 55 | +2 | 91% |
| Model vs market gap | no model | 442 | -65 | 85% |
| Side | yes | 442 | -65 | 85% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 3 | +2 | 100% |
| Quarter | 2025-Q3 | 9 | -24 | 67% |
| Quarter | 2026-Q1 | 9 | +10 | 100% |
| Quarter | 2026-Q2 | 17 | -23 | 76% |
| Quarter | 2026-Q3 | 17 | +2 | 88% |
| Quarter | 2026-Q4 | 12 | -21 | 75% |
| Price paid | 0.50-0.70 | 2 | -2 | 50% |
| Price paid | 0.70-0.90 | 10 | -18 | 70% |
| Price paid | 0.90-1.01 | 55 | -33 | 86% |
| Model vs market gap | 0.00-0.05 | 26 | -6 | 88% |
| Model vs market gap | 0.05-0.10 | 36 | -38 | 81% |
| Model vs market gap | 0.10-0.20 | 5 | -9 | 60% |
| Side | no | 21 | -28 | 76% |
| Side | yes | 46 | -25 | 85% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 47 | +5 | 100% |
| Quarter | 2025-Q4 | 38 | -25 | 92% |
| Quarter | 2026-Q1 | 172 | -48 | 93% |
| Quarter | 2026-Q3 | 216 | +19 | 100% |
| Quarter | 2026-Q4 | 80 | -10 | 98% |
| Price paid | 0.90-1.01 | 553 | -59 | 97% |
| Model vs market gap | no model | 553 | -59 | 97% |
| Side | no | 553 | -59 | 97% |

## Weather: daily lows: late entries

1877 events, 2025-12-13 to 2026-11-22.

**Verdict:** Heavy-volume move (10c, 5x): fade: +135 on 335 trades (+3.9% per $ staked, t=0.36), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Heavy-volume move: fade | 756 | 35% | +413.48 | +5.3% | 0.76 | 0.69 | +419 | -6 | – | – | 0.1656 |
| Heavy-volume move (10c, 5x): fade | 335 | 31% | +135.25 | +3.9% | 0.36 | -0.26 | +119 | +16 | – | – | 0.1607 |
| Bayes price-level, 99% sure | 10 | 60% | +41.84 | +40.6% | 1.07 | 1.07 | +22 | +20 | 58% | 0.2435 | 0.2878 |
| Bayes price-level, 95% sure | 34 | 44% | -14.21 | -4.1% | -0.22 | -0.19 | -24 | +10 | 60% | 0.2982 | 0.2876 |
| Combined: rolling best (past 6 months) | 337 | 33% | -17.15 | -0.5% | -0.03 | -0.23 | -367 | +350 | – | – | 0.1615 |
| Late favorite 90-97c | 898 | 94% | -77.02 | -0.9% | -1.11 | -1.11 | -43 | -34 | – | – | 0.0539 |
| Late favorite 80-90c | 373 | 82% | -204.54 | -5.6% | -2.46 | -2.46 | -108 | -97 | – | – | 0.1455 |
| Combined: 5+ strategies agree | 373 | 82% | -204.54 | -5.6% | -2.46 | -2.46 | -108 | -97 | – | – | 0.1455 |
| Late long-shot fade 1-4c | 1921 | 98% | -206.47 | -1.1% | -3.08 | -2.89 | -162 | -45 | – | – | 0.0233 |
| Combined: 3+ strategies agree | 428 | 79% | -246.55 | -5.9% | -2.45 | -2.57 | -172 | -74 | 55% | 0.1882 | 0.1595 |
| Late fav 80-90c, take profit 10c | 373 | 83% | -254.73 | -7.0% | -3.15 | -3.15 | -130 | -124 | – | – | 0.1435 |
| Heavy-volume move (10c, 5x): follow | 248 | 64% | -342.37 | -13.9% | -2.68 | -2.15 | -213 | -129 | – | – | 0.1719 |
| Late long-shot fade | 1368 | 93% | -354.84 | -2.7% | -3.82 | -3.56 | -272 | -83 | – | – | 0.0626 |
| Late fav 80-90c, stop loss 25c | 373 | 62% | -401.91 | -11.0% | -5.87 | -5.87 | -244 | -158 | – | – | 0.2825 |
| Late fav 80-90c, take profit 15c / stop 15c | 373 | 48% | -437.93 | -12.0% | -7.76 | -7.76 | -255 | -183 | – | – | 0.3746 |
| Late fav 80-90c, stop loss 10c | 373 | 39% | -438.51 | -12.0% | -8.56 | -8.56 | -254 | -184 | – | – | 0.4374 |
| Late favorite 50-80c | 434 | 58% | -632.42 | -14.7% | -4.11 | -4.11 | -228 | -405 | – | – | 0.2364 |
| Heavy-volume move: follow | 593 | 56% | -1180.65 | -20.0% | -5.42 | -5.45 | -552 | -628 | – | – | 0.1762 |

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
| Quarter | 2026-Q4 | 50 | -8 | 86% |
| Price paid | 0.70-0.90 | 332 | -192 | 82% |
| Price paid | 0.90-1.01 | 41 | -13 | 88% |
| Model vs market gap | no model | 373 | -205 | 82% |
| Side | yes | 373 | -205 | 82% |

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

Why: Heavy-volume move (10c, 5x): fade

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q4 | 5 | +68 | 40% |
| Quarter | 2026-Q1 | 79 | -270 | 24% |
| Quarter | 2026-Q2 | 85 | +299 | 38% |
| Quarter | 2026-Q3 | 111 | -186 | 26% |
| Quarter | 2026-Q4 | 55 | +223 | 38% |
| Price paid | 0.10-0.30 | 235 | +119 | 18% |
| Price paid | 0.30-0.50 | 40 | -10 | 38% |
| Price paid | 0.50-0.70 | 25 | +6 | 64% |
| Price paid | 0.70-0.90 | 35 | +21 | 86% |
| Model vs market gap | no model | 335 | +135 | 31% |
| Side | no | 209 | +196 | 36% |
| Side | yes | 126 | -61 | 22% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q3 | 224 | -257 | 31% |
| Quarter | 2026-Q4 | 113 | +240 | 38% |
| Price paid | 0.10-0.30 | 222 | -215 | 16% |
| Price paid | 0.30-0.50 | 50 | +170 | 54% |
| Price paid | 0.50-0.70 | 23 | +30 | 70% |
| Price paid | 0.70-0.90 | 39 | -5 | 80% |
| Price paid | 0.90-1.01 | 3 | +3 | 100% |
| Model vs market gap | no model | 337 | -17 | 33% |
| Side | no | 209 | -83 | 37% |
| Side | yes | 128 | +65 | 27% |

## Bitcoin: last 1-3 hours

610 events, 2025-03-22 to 2026-11-22.

**Verdict:** Late long-shot fade 1-4c: +93 on 913 trades (+1.0% per $ staked, t=6.55), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bayes price-level, 99% sure | 560 | 94% | +171.14 | +3.2% | 2.78 | 2.57 | +118 | +53 | 96% | 0.0538 | 0.0559 |
| Bayes price-level, 95% sure | 956 | 92% | +145.32 | +1.6% | 1.54 | 1.89 | +41 | +104 | 94% | 0.0742 | 0.0746 |
| Late long-shot fade | 770 | 97% | +119.10 | +1.6% | 2.67 | 2.14 | +27 | +92 | – | – | 0.0276 |
| Combined: rolling best (past 6 months) | 766 | 96% | +108.73 | +1.5% | 1.92 | 1.5 | +23 | +85 | 94% | 0.0718 | 0.0337 |
| Late long-shot fade 1-4c | 913 | 100% | +93.13 | +1.0% | 6.55 | 6.13 | +39 | +54 | – | – | 0.0025 |
| Combined: 3+ strategies agree | 262 | 89% | +82.78 | +3.2% | 1.44 | 1.47 | +9 | +74 | 90% | 0.0961 | 0.091 |
| Late favorite 90-97c | 204 | 96% | +4.10 | +0.2% | 0.12 | 0.12 | +30 | -26 | – | – | 0.0425 |
| Late favorite 80-90c | 47 | 87% | -0.31 | -0.1% | 0.01 | 0.01 | -1 | +1 | – | – | 0.1141 |
| Combined: 5+ strategies agree | 47 | 87% | -0.31 | -0.1% | 0.01 | 0.01 | -1 | +1 | – | – | 0.1141 |
| Late favorite 50-80c | 31 | 68% | -0.41 | -0.1% | 0.01 | 0.01 | -31 | +31 | – | – | 0.2216 |
| Late fav 80-90c, take profit 10c | 47 | 87% | -1.58 | -0.3% | -0.04 | -0.04 | -1 | -0 | – | – | 0.1141 |
| Late fav 80-90c, stop loss 25c | 47 | 74% | -29.82 | -6.5% | -1.1 | -1.1 | -34 | +4 | – | – | 0.2007 |
| Late fav 80-90c, stop loss 10c | 47 | 60% | -47.16 | -10.2% | -1.87 | -1.87 | -49 | +2 | – | – | 0.2943 |
| Late fav 80-90c, take profit 15c / stop 15c | 47 | 64% | -48.94 | -10.6% | -1.84 | -1.84 | -49 | -0 | – | – | 0.2697 |
| Heavy-volume move (10c, 5x): follow | 806 | 66% | -607.73 | -7.6% | -2.85 | -2.11 | -357 | -251 | – | – | 0.1775 |
| Heavy-volume move: follow | 1330 | 66% | -961.14 | -7.3% | -3.42 | -2.87 | -636 | -325 | – | – | 0.17 |
| Heavy-volume move (10c, 5x): fade | 875 | 31% | -1824.31 | -20.2% | -4.05 | -3.84 | -1201 | -623 | – | – | 0.1657 |
| Heavy-volume move: fade | 1413 | 30% | -3552.25 | -24.4% | -6.36 | -5.55 | -2176 | -1377 | – | – | 0.1553 |

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
| Quarter | 2026-Q4 | 172 | +21 | 100% |
| Price paid | 0.90-1.01 | 913 | +93 | 100% |
| Model vs market gap | no model | 913 | +93 | 100% |
| Side | no | 913 | +93 | 100% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 11 | -3 | 91% |
| Quarter | 2025-Q3 | 58 | +11 | 93% |
| Quarter | 2025-Q4 | 76 | -19 | 88% |
| Quarter | 2026-Q1 | 135 | +35 | 95% |
| Quarter | 2026-Q2 | 257 | +10 | 91% |
| Quarter | 2026-Q3 | 250 | +199 | 96% |
| Quarter | 2026-Q4 | 169 | -89 | 85% |
| Price paid | 0.50-0.70 | 2 | -5 | 50% |
| Price paid | 0.70-0.90 | 396 | +95 | 86% |
| Price paid | 0.90-1.01 | 558 | +55 | 96% |
| Model vs market gap | 0.00-0.05 | 433 | +54 | 96% |
| Model vs market gap | 0.05-0.10 | 451 | +81 | 88% |
| Model vs market gap | 0.10-0.20 | 72 | +10 | 83% |
| Side | no | 163 | +24 | 90% |
| Side | yes | 793 | +121 | 92% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 50 | -0 | 96% |
| Quarter | 2025-Q4 | 29 | +3 | 100% |
| Quarter | 2026-Q1 | 127 | +17 | 100% |
| Quarter | 2026-Q2 | 260 | +14 | 99% |
| Quarter | 2026-Q3 | 181 | +141 | 96% |
| Quarter | 2026-Q4 | 119 | -66 | 86% |
| Price paid | 0.70-0.90 | 125 | +27 | 86% |
| Price paid | 0.90-1.01 | 641 | +81 | 98% |
| Model vs market gap | 0.00-0.05 | 138 | +32 | 97% |
| Model vs market gap | 0.05-0.10 | 151 | +37 | 88% |
| Model vs market gap | 0.10-0.20 | 11 | +6 | 82% |
| Model vs market gap | no model | 466 | +33 | 99% |
| Side | no | 526 | +84 | 99% |
| Side | yes | 240 | +25 | 91% |

## Ethereum

605 events, 2025-03-27 to 2026-11-22.

**Verdict:** Market favorite (no model): +103 on 116 trades (+8.8% per $ staked, t=1.14), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Time-of-day vol x0.5, skip spikes | 805 | 82% | +162.40 | +2.1% | 1.22 | 1.12 | -59 | +221 | 92% | 0.152 | 0.1432 |
| Time-of-day vol x0.5, against trend + skip spikes | 442 | 84% | +150.51 | +3.5% | 1.56 | 1.41 | -33 | +183 | 93% | 0.1424 | 0.1365 |
| Market favorite (no model) | 116 | 66% | +102.54 | +8.8% | 1.14 | 1.14 | +87 | +15 | – | – | 0.2029 |
| Time-of-day vol x0.5 | 1265 | 81% | +100.77 | +0.8% | 0.59 | 1.3 | -153 | +253 | 92% | 0.1595 | 0.1472 |
| Vol x0.5, weekends only | 161 | 83% | +85.39 | +5.4% | 1.07 | 1.33 | +1 | +84 | 92% | 0.1332 | 0.1299 |
| Bayes price-level, 95% sure | 49 | 80% | +61.96 | +12.8% | 1.49 | 1.49 | +43 | +19 | 77% | 0.149 | 0.1578 |
| Vol x0.5, skip spiked markets | 940 | 80% | +34.37 | +0.4% | 0.21 | -0.19 | -221 | +255 | 93% | 0.1741 | 0.1578 |
| Vol x0.5, against trend + skip spikes | 511 | 80% | +2.60 | +0.1% | 0.0 | -0.15 | -168 | +170 | 93% | 0.1776 | 0.16 |
| Bayes: market prior + full vol | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Bayes: market prior + fat-tail | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Long-shot fade (no model) | 617 | 96% | -18.33 | -0.3% | -0.31 | -0.21 | -88 | +70 | – | – | 0.0438 |
| Bayes price-level, 99% sure | 3 | 0% | -29.77 | -100.0% | – | – | -10 | -20 | 72% | 0.5155 | 0.3521 |
| Combined: rolling best (past 6 months) | 273 | 79% | -37.22 | -1.4% | -0.44 | -0.59 | -101 | +64 | 93% | 0.1666 | 0.1553 |
| Vol x0.75 | 422 | 77% | -44.70 | -1.1% | -0.28 | -0.5 | -160 | +116 | 88% | 0.1586 | 0.1463 |
| Vol x0.5, news days only | 83 | 75% | -46.16 | -5.7% | -0.93 | -1.27 | -30 | -17 | 92% | 0.2044 | 0.1751 |
| Fat-tail (actual past moves) | 357 | 68% | -60.01 | -1.7% | -0.25 | -0.24 | -213 | +153 | 79% | 0.1856 | 0.1724 |
| Vol x0.5, against the 24h trend | 718 | 78% | -70.65 | -1.0% | -0.48 | -0.58 | -276 | +206 | 93% | 0.184 | 0.164 |
| Vol x0.5, calm market only | 769 | 79% | -71.78 | -1.0% | -0.48 | -0.15 | -210 | +139 | 92% | 0.1776 | 0.16 |
| Vol x0.5, 5c edge | 1737 | 79% | -78.20 | -0.5% | -0.36 | 0.05 | -391 | +313 | 92% | 0.1754 | 0.1583 |
| Regime-scaled vol x0.5 | 1616 | 79% | -136.09 | -0.9% | -0.66 | 0.23 | -356 | +220 | 93% | 0.1799 | 0.1595 |
| Vol x0.5, busy market only | 690 | 78% | -138.34 | -2.1% | -1.01 | -0.86 | -157 | +18 | 93% | 0.1928 | 0.1674 |
| Vol x0.5, with the 24h trend | 741 | 78% | -139.47 | -1.9% | -0.99 | -1.05 | -105 | -35 | 92% | 0.1856 | 0.163 |
| Vol x0.5, skip news days | 1376 | 78% | -163.96 | -1.2% | -0.83 | -0.34 | -365 | +201 | 93% | 0.1836 | 0.1628 |
| Vol x0.5, NO only | 919 | 78% | -175.33 | -1.9% | -1.12 | -1.09 | -224 | +48 | 92% | 0.1813 | 0.1611 |
| Vol x0.5, skip news in window | 1436 | 78% | -205.28 | -1.5% | -1.02 | -0.6 | -380 | +174 | 93% | 0.1852 | 0.1638 |
| Vol x0.5 (Bitcoin's winner) | 1459 | 78% | -210.12 | -1.5% | -1.04 | -0.7 | -395 | +185 | 93% | 0.1848 | 0.1635 |
| Fat-tail, moves x0.75 | 911 | 73% | -212.11 | -2.4% | -1.16 | -1.29 | -199 | -13 | 86% | 0.2035 | 0.1859 |
| Full vol + 50% market blend | 104 | 27% | -221.53 | -20.6% | -0.86 | -0.7 | -278 | +56 | 37% | 0.1214 | 0.1109 |
| Vol x0.5, weekdays only | 1298 | 78% | -295.51 | -2.3% | -1.55 | -1.27 | -367 | +71 | 93% | 0.1912 | 0.1676 |
| Fat-tail, moves x0.5 | 1745 | 74% | -325.87 | -1.9% | -1.33 | -1.19 | -410 | +84 | 90% | 0.2069 | 0.1813 |
| Options vol x0.85, 5c gap | 449 | 57% | -387.06 | -8.6% | -0.99 | -0.81 | -560 | +173 | 68% | 0.1306 | 0.1179 |
| Options vol, NO only | 218 | 28% | -508.62 | -22.6% | -1.4 | -1.14 | -606 | +98 | 42% | 0.1189 | 0.0958 |
| Heavy-volume move (10c, 5x): follow | 418 | 60% | -515.80 | -12.4% | -3.09 | -2.98 | -256 | -260 | – | – | 0.1808 |
| Options vol, 8c gap | 199 | 17% | -569.59 | -27.5% | -1.47 | -1.17 | -716 | +146 | 36% | 0.1251 | 0.0904 |
| Vol x0.5, take profit 10c | 1459 | 81% | -614.68 | -4.3% | -3.49 | -2.96 | -589 | -25 | 93% | 0.1647 | 0.1528 |
| Combined: 5+ strategies agree | 1731 | 74% | -711.92 | -4.2% | -2.11 | -1.69 | -768 | +56 | 87% | 0.1763 | 0.1594 |
| Vol x0.5, stop loss 25c | 1459 | 65% | -746.48 | -5.2% | -4.27 | -3.93 | -759 | +13 | 93% | 0.303 | 0.2361 |
| Full vol (v1 rule) | 228 | 32% | -858.21 | -36.6% | -3.09 | -2.73 | -777 | -81 | 48% | 0.1182 | 0.0894 |
| Heavy-volume move (10c, 5x): fade | 467 | 35% | -890.23 | -18.6% | -2.84 | -2.97 | -201 | -689 | – | – | 0.1645 |
| Heavy-volume move: follow | 760 | 57% | -993.34 | -13.1% | -3.9 | -3.57 | -434 | -559 | – | – | 0.1858 |
| Vol x0.5, take profit 15c / stop 15c | 1459 | 57% | -1016.80 | -7.1% | -7.37 | -6.64 | -870 | -146 | 93% | 0.3698 | 0.2801 |
| Heavy-volume move: fade | 822 | 38% | -1093.35 | -13.0% | -2.58 | -2.99 | -347 | -746 | – | – | 0.1727 |
| Vol x0.5, stop loss 10c | 1459 | 47% | -1099.93 | -7.7% | -7.52 | -6.97 | -964 | -136 | 93% | 0.4525 | 0.3299 |
| Options vol, 5c gap | 391 | 23% | -1480.97 | -36.5% | -3.45 | -3.24 | -1223 | -258 | 39% | 0.1174 | 0.091 |
| Vol x0.5, limit order | 731 | 57% | -1730.30 | -24.5% | -10.01 | -11.3 | -1117 | -614 | 92% | 0.3562 | 0.2674 |
| Vol x0.5, limit order (strict fill) | 710 | 56% | -1782.38 | -26.0% | -10.4 | -11.67 | -1142 | -640 | 92% | 0.3666 | 0.2741 |
| Combined: 3+ strategies agree | 2458 | 66% | -1918.86 | -7.9% | -3.62 | -3.17 | -1404 | -514 | 84% | 0.1715 | 0.1576 |
| Vol x0.5 5c edge, limit order | 852 | 58% | -1927.48 | -23.4% | -10.32 | -11.78 | -1230 | -698 | 91% | 0.3423 | 0.2613 |
| Kalshi price-spike fade (no model) | 1075 | 30% | -2388.33 | -21.6% | -4.88 | -4.52 | -878 | -1511 | – | – | 0.1702 |

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
| 0.3 | 2053 | -115.54 | -0.6% |
| 0.4 | 1818 | -292.00 | -1.6% |
| 0.5 | 1459 | -210.12 | -1.5% |
| 0.6 | 990 | -234.61 | -2.4% |
| 0.75 | 422 | -44.70 | -1.1% |
| 1.0 | 228 | -858.21 | -36.6% |

Sweep: time-of-day vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1723 | -13.64 | -0.1% |
| 0.5 | 1265 | +100.77 | +0.8% |
| 0.6 | 716 | -101.30 | -1.5% |
| 0.75 | 239 | -298.15 | -12.6% |
| 1.0 | 244 | -937.35 | -36.9% |

Sweep: fat-tail

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 2000 | -146.03 | -0.7% |
| 0.5 | 1745 | -325.87 | -1.9% |
| 0.6 | 1407 | -143.36 | -1.0% |
| 0.75 | 911 | -212.11 | -2.4% |
| 0.9 | 527 | -221.13 | -4.3% |
| 1.0 | 357 | -60.01 | -1.7% |

Sweep: options vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 1375 | -389.38 | -2.9% |
| 0.7 | 898 | -344.00 | -3.9% |
| 0.8 | 543 | -401.42 | -7.4% |
| 0.9 | 384 | -649.61 | -16.7% |
| 1.0 | 391 | -1480.97 | -36.5% |
| 1.1 | 529 | -2880.89 | -52.0% |

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
| Quarter | 2026-Q4 | 10 | +4 | 70% |
| Price paid | 0.30-0.50 | 28 | +29 | 46% |
| Price paid | 0.50-0.70 | 60 | -11 | 62% |
| Price paid | 0.70-0.90 | 28 | +84 | 96% |
| Model vs market gap | no model | 116 | +103 | 66% |
| Side | yes | 116 | +103 | 66% |

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
| Quarter | 2026-Q4 | 88 | -338 | 28% |
| Price paid | 0.10-0.30 | 537 | -2078 | 13% |
| Price paid | 0.30-0.50 | 303 | -323 | 36% |
| Price paid | 0.50-0.70 | 182 | +18 | 60% |
| Price paid | 0.70-0.90 | 53 | -5 | 76% |
| Model vs market gap | no model | 1075 | -2388 | 30% |
| Side | no | 495 | -1258 | 34% |
| Side | yes | 580 | -1130 | 28% |

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
| Quarter | 2026-Q4 | 44 | +4 | 82% |
| Price paid | 0.50-0.70 | 36 | +57 | 78% |
| Price paid | 0.70-0.90 | 386 | +95 | 84% |
| Price paid | 0.90-1.01 | 20 | -1 | 90% |
| Model vs market gap | 0.05-0.10 | 7 | +8 | 100% |
| Model vs market gap | 0.10-0.20 | 397 | +146 | 84% |
| Model vs market gap | 0.20-0.35 | 37 | -8 | 73% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 214 | +141 | 87% |
| Side | yes | 228 | +10 | 81% |

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
| Quarter | 2026-Q4 | 136 | +43 | 82% |
| Price paid | 0.10-0.30 | 4 | -42 | 0% |
| Price paid | 0.50-0.70 | 142 | +14 | 68% |
| Price paid | 0.70-0.90 | 1077 | +107 | 82% |
| Price paid | 0.90-1.01 | 42 | +21 | 95% |
| Model vs market gap | 0.05-0.10 | 16 | -13 | 81% |
| Model vs market gap | 0.10-0.20 | 1121 | +135 | 82% |
| Model vs market gap | 0.20-0.35 | 127 | -25 | 72% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 638 | +19 | 81% |
| Side | yes | 627 | +82 | 81% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 2 | +2 | 100% |
| Quarter | 2025-Q3 | 5 | +5 | 100% |
| Quarter | 2025-Q4 | 1 | -10 | 0% |
| Quarter | 2026-Q2 | 12 | +24 | 75% |
| Quarter | 2026-Q3 | 17 | +29 | 76% |
| Quarter | 2026-Q4 | 12 | +12 | 83% |
| Price paid | 0.50-0.70 | 34 | +37 | 71% |
| Price paid | 0.70-0.90 | 8 | +18 | 100% |
| Price paid | 0.90-1.01 | 7 | +7 | 100% |
| Model vs market gap | 0.05-0.10 | 27 | +59 | 93% |
| Model vs market gap | 0.10-0.20 | 22 | +2 | 64% |
| Side | no | 2 | -9 | 50% |
| Side | yes | 47 | +71 | 81% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 76 | -4 | 80% |
| Quarter | 2025-Q4 | 81 | -86 | 73% |
| Quarter | 2026-Q2 | 26 | -16 | 62% |
| Quarter | 2026-Q3 | 46 | +64 | 94% |
| Quarter | 2026-Q4 | 44 | +4 | 82% |
| Price paid | 0.30-0.50 | 3 | -5 | 33% |
| Price paid | 0.50-0.70 | 30 | -37 | 57% |
| Price paid | 0.70-0.90 | 226 | +1 | 81% |
| Price paid | 0.90-1.01 | 14 | +3 | 93% |
| Model vs market gap | 0.05-0.10 | 6 | +7 | 100% |
| Model vs market gap | 0.10-0.20 | 219 | -9 | 81% |
| Model vs market gap | 0.20-0.35 | 22 | -19 | 68% |
| Model vs market gap | no model | 26 | -16 | 62% |
| Side | no | 119 | +77 | 87% |
| Side | yes | 154 | -114 | 72% |
