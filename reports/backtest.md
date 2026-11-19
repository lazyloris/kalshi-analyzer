# Backtest (2026-11-19)

Flat $10 per trade at the ask plus Kalshi fees, held to settlement. Prices are real hourly Kalshi quotes. Forecasts are archived NWS-blend (NBM) runs 1-2 days old. Bias/sigma learned only from earlier days.

## Live paper books vs backtest

| Book | Settled | Open | Live P&L | Live return/$ | Backtest rule | Backtest return/$ |
|---|---|---|---|---|---|---|
| bitcoin | 20 | 4 | +16.75 | +8.6% | c_vol50 | +0.2% |
| bitcoin_tod | 20 | 4 | +13.70 | +7.0% | s_combo_tod | +2.5% |
| ethereum | 20 | 4 | +4.81 | +2.5% | a_vol50 | -1.5% |
| ethereum_tod | 20 | 4 | -5.33 | -2.7% | s_combo_tod | +2.1% |
| weather_high | 104 | 16 | -49.76 | -5.0% | fade | +0.0% |
| weather_low | 48 | 9 | -11.92 | -2.6% | fade | +0.3% |

Live numbers need ~100 settled trades before they mean much.

## Weather: daily highs

3778 events, 2025-03-21 to 2026-11-18.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Kalshi price-spike fade (no model) (+159 on 493 trades).

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 493 | 45% | +158.55 | +3.1% | 0.5 | 0.32 | -148 | +307 | – | – | 0.1961 |
| Long-shot fade (no model) | 4991 | 95% | +15.72 | +0.0% | 0.1 | 0.16 | +46 | -30 | – | – | 0.0438 |
| Bayes: market prior + forecast | 2 | 50% | -4.85 | -24.4% | -0.29 | -0.29 | -10 | +5 | 74% | 0.3459 | 0.3305 |
| Bayes price-level, 99% sure | 1262 | 91% | -176.98 | -1.5% | -1.66 | -1.71 | -8 | -169 | 94% | 0.0792 | 0.0778 |
| Heavy-volume move (10c, 5x): fade | 314 | 48% | -215.23 | -6.8% | -0.9 | -0.71 | -155 | -60 | – | – | 0.1834 |
| Combined: rolling best (past 6 months) | 2938 | 94% | -222.70 | -0.8% | -1.38 | -1.54 | +86 | -309 | – | – | 0.0492 |
| Market favorite YES (no model) | 4648 | 50% | -311.13 | -0.7% | -0.46 | -0.46 | -222 | -90 | – | – | 0.2426 |
| Bayes price-level, 95% sure | 2198 | 88% | -369.32 | -1.7% | -2.17 | -2.02 | -212 | -158 | 91% | 0.0964 | 0.0948 |
| Heavy-volume move (10c, 5x): follow | 296 | 49% | -408.23 | -13.7% | -2.18 | -1.94 | -291 | -118 | – | – | 0.1943 |
| Long-shot fade, limit order | 2857 | 92% | -502.06 | -1.9% | -3.44 | -3.43 | -200 | -302 | – | – | 0.0738 |
| Heavy-volume move: fade | 1550 | 48% | -998.82 | -6.4% | -1.9 | -2.42 | -1029 | +30 | – | – | 0.1881 |
| Combined: 5+ strategies agree | 5035 | 49% | -1157.27 | -2.3% | -1.48 | -1.1 | -346 | -812 | 60% | 0.2228 | 0.2359 |
| Heavy-volume move: follow | 1515 | 49% | -1688.15 | -11.0% | -3.81 | -3.53 | -729 | -960 | – | – | 0.1924 |
| Favorite, stop loss 25c | 4648 | 42% | -2514.44 | -5.3% | -3.99 | -3.99 | -2176 | -338 | – | – | 0.2414 |
| Forecast bracket YES | 776 | 10% | -3643.24 | -44.6% | -6.57 | -6.57 | -1844 | -1800 | 33% | 0.1458 | 0.0905 |
| Favorite, take profit 10c | 4648 | 70% | -3708.97 | -7.9% | -8.52 | -8.52 | -2327 | -1382 | – | – | 0.2609 |
| Favorite, stop loss 10c | 4648 | 28% | -4361.09 | -9.3% | -9.02 | -9.02 | -3029 | -1332 | – | – | 0.2369 |
| Favorite, take profit 15c / stop 15c | 4648 | 47% | -5517.41 | -11.7% | -15.32 | -15.32 | -3822 | -1695 | – | – | 0.2512 |
| Market favorite, limit order | 3790 | 39% | -6553.93 | -17.5% | -10.16 | -10.16 | -4317 | -2237 | – | – | 0.2363 |
| v2 + disagreement cap | 3323 | 33% | -8258.19 | -24.3% | -7.59 | -6.67 | -4168 | -4090 | 54% | 0.2009 | 0.1577 |
| v1 (what we ran live) | 4588 | 34% | -9101.17 | -19.4% | -7.25 | -6.61 | -4638 | -4463 | 63% | 0.263 | 0.1659 |
| v2 + 50% market blend | 3710 | 31% | -9293.03 | -24.4% | -8.2 | -7.07 | -4658 | -4635 | 46% | 0.1909 | 0.1656 |
| v2 calibrated | 4184 | 32% | -10059.34 | -23.4% | -8.5 | -7.48 | -5043 | -5016 | 58% | 0.2451 | 0.1682 |
| Combined: 3+ strategies agree | 9642 | 46% | -10582.22 | -10.8% | -7.72 | -5.78 | -4039 | -6544 | 62% | 0.2719 | 0.1936 |

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
| 0.6 | 4163 | -9550.26 | -22.4% |
| 0.8 | 4026 | -9906.18 | -24.0% |
| 1.0 | 4184 | -10059.34 | -23.4% |
| 1.25 | 4439 | -8812.49 | -19.4% |
| 1.5 | 4594 | -7777.45 | -16.6% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 5091 | -11650.25 | -22.3% |
| blend 0.0, edge 0.05 | 4774 | -10958.00 | -22.4% |
| blend 0.0, edge 0.08 | 4184 | -10059.34 | -23.4% |
| blend 0.25, edge 0.03 | 4825 | -11356.84 | -22.9% |
| blend 0.25, edge 0.05 | 4326 | -10362.37 | -23.3% |
| blend 0.25, edge 0.08 | 3397 | -8949.06 | -25.7% |
| blend 0.5, edge 0.03 | 4161 | -10140.47 | -23.7% |
| blend 0.5, edge 0.05 | 3223 | -8444.16 | -25.5% |
| blend 0.5, edge 0.08 | 1963 | -4746.77 | -23.5% |
| blend 0.75, edge 0.03 | 1956 | -5355.80 | -26.5% |
| blend 0.75, edge 0.05 | 854 | -1951.73 | -22.1% |
| blend 0.75, edge 0.08 | 228 | -618.47 | -26.1% |

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
| Quarter | 2026-Q4 | 869 | -2109 | 32% |
| Price paid | 0.00-0.10 | 838 | -2964 | 5% |
| Price paid | 0.10-0.30 | 885 | -4103 | 10% |
| Price paid | 0.30-0.50 | 902 | -1336 | 37% |
| Price paid | 0.50-0.70 | 1225 | -1410 | 53% |
| Price paid | 0.70-0.90 | 333 | -236 | 71% |
| Price paid | 0.90-1.01 | 1 | -10 | 0% |
| Model vs market gap | 0.05-0.10 | 62 | -14 | 16% |
| Model vs market gap | 0.10-0.20 | 2107 | -5763 | 32% |
| Model vs market gap | 0.20-0.35 | 1586 | -3363 | 34% |
| Model vs market gap | 0.35-1.01 | 429 | -919 | 29% |
| Side | no | 2540 | -3238 | 48% |
| Side | yes | 1644 | -6822 | 8% |

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
| Quarter | 2026-Q4 | 239 | -25 | 87% |
| Price paid | 0.30-0.50 | 21 | -85 | 29% |
| Price paid | 0.50-0.70 | 34 | +8 | 53% |
| Price paid | 0.70-0.90 | 681 | -174 | 82% |
| Price paid | 0.90-1.01 | 1462 | -119 | 93% |
| Model vs market gap | 0.00-0.05 | 1970 | -190 | 90% |
| Model vs market gap | 0.05-0.10 | 207 | -94 | 77% |
| Model vs market gap | 0.10-0.20 | 21 | -85 | 29% |
| Side | no | 2141 | -273 | 89% |
| Side | yes | 57 | -97 | 42% |

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
| Austin | day before 10am | 250 | +1.79 | 3.35 |
| Austin | same day 8am | 252 | +1.52 | 2.95 |
| Chicago | day before 10am | 250 | +1.50 | 3.43 |
| Chicago | same day 8am | 248 | +1.32 | 2.86 |
| Denver | day before 10am | 251 | +1.73 | 3.38 |
| Denver | same day 8am | 248 | +1.66 | 2.95 |
| Los Angeles | day before 10am | 249 | +2.28 | 3.83 |
| Los Angeles | same day 8am | 251 | +2.28 | 3.58 |
| Miami | same day 8am | 251 | +2.03 | 2.65 |
| New York | same day 8am | 247 | -0.20 | 2.46 |
| Philadelphia | same day 8am | 247 | +1.73 | 2.88 |

## Weather: daily lows

2263 events, 2025-12-13 to 2026-11-18.

**Verdict:** Long-shot fade (no model): +94 on 3231 trades (+0.3% per $ staked, t=0.86), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 152 | 53% | +257.44 | +16.7% | 1.35 | 1.22 | -53 | +310 | – | – | 0.2106 |
| Combined: rolling best (past 6 months) | 1645 | 78% | +233.57 | +1.5% | 0.8 | 0.87 | +165 | +68 | – | – | 0.1229 |
| Long-shot fade (no model) | 3231 | 96% | +93.69 | +0.3% | 0.86 | 0.93 | +76 | +17 | – | – | 0.0369 |
| Heavy-volume move: follow | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Heavy-volume move: fade | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Heavy-volume move (10c, 5x): follow | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Heavy-volume move (10c, 5x): fade | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Bayes: market prior + forecast | 1 | 0% | -10.25 | -100.0% | – | – | +0 | -10 | 49% | 0.2401 | 0.16 |
| Bayes price-level, 99% sure | 206 | 94% | -21.71 | -1.1% | -0.65 | -0.57 | -13 | -9 | 96% | 0.0556 | 0.0554 |
| Bayes price-level, 95% sure | 375 | 94% | -22.43 | -0.6% | -0.44 | -0.38 | -50 | +28 | 96% | 0.0583 | 0.0582 |
| Long-shot fade, limit order | 1709 | 93% | -211.14 | -1.3% | -1.96 | -1.59 | -64 | -148 | – | – | 0.0669 |
| Combined: 5+ strategies agree | 2220 | 46% | -399.43 | -1.8% | -0.76 | -0.87 | +534 | -933 | 54% | 0.2373 | 0.238 |
| Market favorite YES (no model) | 2155 | 47% | -611.96 | -2.8% | -1.24 | -1.24 | +475 | -1087 | – | – | 0.24 |
| Forecast bracket YES | 556 | 15% | -1641.49 | -28.2% | -3.43 | -3.43 | -1010 | -632 | 34% | 0.1623 | 0.1224 |
| Favorite, take profit 10c | 2155 | 62% | -2778.10 | -12.7% | -8.15 | -8.15 | -1013 | -1766 | – | – | 0.2664 |
| Market favorite, limit order | 1792 | 36% | -3009.52 | -16.9% | -6.25 | -6.25 | -823 | -2187 | – | – | 0.2269 |
| v2 + 50% market blend | 1911 | 30% | -3869.54 | -19.6% | -4.19 | -4.0 | -1150 | -2719 | 41% | 0.1575 | 0.1425 |
| Favorite, stop loss 25c | 2155 | 28% | -5378.28 | -24.6% | -12.95 | -12.95 | -2208 | -3171 | – | – | 0.2288 |
| v2 calibrated | 2644 | 31% | -5687.80 | -20.9% | -5.62 | -5.15 | -1820 | -3868 | 52% | 0.2002 | 0.1499 |
| Favorite, stop loss 10c | 2155 | 14% | -5865.27 | -26.8% | -20.91 | -20.91 | -2884 | -2981 | – | – | 0.2165 |
| v2 + disagreement cap | 2295 | 32% | -6038.84 | -25.6% | -6.73 | -6.83 | -2138 | -3901 | 50% | 0.1769 | 0.1432 |
| Combined: 3+ strategies agree | 4570 | 41% | -6163.71 | -13.2% | -5.91 | -5.14 | -1995 | -4169 | 57% | 0.2339 | 0.1862 |
| Favorite, take profit 15c / stop 15c | 2155 | 28% | -6512.02 | -29.8% | -27.7 | -27.7 | -3314 | -3198 | – | – | 0.2353 |
| v1 (what we ran live) | 3889 | 32% | -10548.00 | -26.4% | -9.45 | -8.52 | -4522 | -6026 | 57% | 0.227 | 0.1485 |

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
| 0.6 | 3401 | -5254.87 | -15.2% |
| 0.8 | 2703 | -4957.02 | -17.9% |
| 1.0 | 2644 | -5687.80 | -20.9% |
| 1.25 | 3080 | -6940.15 | -21.9% |
| 1.5 | 3615 | -8763.98 | -23.7% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 4070 | -9351.09 | -22.4% |
| blend 0.0, edge 0.05 | 3492 | -8260.69 | -23.0% |
| blend 0.0, edge 0.08 | 2644 | -5687.80 | -20.9% |
| blend 0.25, edge 0.03 | 3486 | -8183.51 | -22.8% |
| blend 0.25, edge 0.05 | 2731 | -5813.36 | -20.7% |
| blend 0.25, edge 0.08 | 1765 | -3511.69 | -19.3% |
| blend 0.5, edge 0.03 | 2383 | -5067.02 | -20.6% |
| blend 0.5, edge 0.05 | 1537 | -3087.09 | -19.4% |
| blend 0.5, edge 0.08 | 743 | -582.95 | -7.6% |
| blend 0.75, edge 0.03 | 638 | -726.55 | -11.0% |
| blend 0.75, edge 0.05 | 251 | -597.72 | -22.9% |
| blend 0.75, edge 0.08 | 56 | -385.27 | -65.9% |

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
| Quarter | 2026-Q4 | 429 | -561 | 30% |
| Price paid | 0.00-0.10 | 565 | -2089 | 5% |
| Price paid | 0.10-0.30 | 817 | -2448 | 12% |
| Price paid | 0.30-0.50 | 320 | -637 | 35% |
| Price paid | 0.50-0.70 | 651 | -382 | 58% |
| Price paid | 0.70-0.90 | 290 | -133 | 73% |
| Price paid | 0.90-1.01 | 1 | +1 | 100% |
| Model vs market gap | 0.05-0.10 | 36 | +38 | 19% |
| Model vs market gap | 0.10-0.20 | 1649 | -4545 | 31% |
| Model vs market gap | 0.20-0.35 | 794 | -562 | 35% |
| Model vs market gap | 0.35-1.01 | 165 | -619 | 24% |
| Side | no | 1246 | -1032 | 55% |
| Side | yes | 1398 | -4655 | 10% |

Why: Long-shot fade (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q1 | 950 | -40 | 95% |
| Quarter | 2026-Q2 | 1044 | +162 | 97% |
| Quarter | 2026-Q3 | 976 | -12 | 96% |
| Quarter | 2026-Q4 | 261 | -17 | 96% |
| Price paid | 0.90-1.01 | 3231 | +94 | 96% |
| Model vs market gap | no model | 3231 | +94 | 96% |
| Side | no | 3231 | +94 | 96% |

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
| Quarter | 2026-Q4 | 82 | -29 | 89% |
| Price paid | 0.50-0.70 | 2 | -5 | 50% |
| Price paid | 0.70-0.90 | 15 | +14 | 80% |
| Price paid | 0.90-1.01 | 358 | -31 | 94% |
| Model vs market gap | 0.00-0.05 | 298 | -0 | 95% |
| Model vs market gap | 0.05-0.10 | 60 | -31 | 90% |
| Model vs market gap | 0.10-0.20 | 17 | +9 | 76% |
| Side | no | 358 | -31 | 94% |
| Side | yes | 17 | +9 | 76% |

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
| Austin | day before 10am | 250 | -2.68 | 4.16 |
| Austin | day before 8pm | 252 | -2.73 | 3.98 |
| Chicago | day before 10am | 250 | -1.57 | 2.99 |
| Chicago | day before 8pm | 252 | -1.38 | 2.64 |
| Denver | day before 10am | 251 | -3.96 | 5.23 |
| Denver | day before 8pm | 252 | -3.82 | 5.07 |
| Los Angeles | day before 10am | 250 | +0.36 | 1.71 |
| Los Angeles | day before 8pm | 252 | +0.48 | 1.6 |
| Miami | day before 8pm | 250 | -0.96 | 2.39 |
| New York | day before 8pm | 252 | -1.58 | 2.7 |
| Philadelphia | day before 8pm | 252 | +0.44 | 2.2 |

## Crypto: Bitcoin 5pm price

606 events, 2025-03-22 to 2026-11-18.

**Verdict:** Vol x0.5, weekends only: +163 on 238 trades (+7.0% per $ staked, t=2.3), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Time-of-day vol x0.5 | 1556 | 80% | +280.21 | +1.8% | 1.39 | 1.62 | -138 | +418 | 92% | 0.1732 | 0.1595 |
| Time-of-day vol x0.5, skip spikes | 969 | 81% | +235.09 | +2.5% | 1.53 | 1.41 | -155 | +390 | 92% | 0.1647 | 0.1544 |
| Vol x0.5, weekends only | 238 | 84% | +162.75 | +7.0% | 2.3 | 2.22 | +23 | +140 | 91% | 0.1216 | 0.1268 |
| Regime-scaled vol x0.5 | 1954 | 78% | +149.23 | +0.8% | 0.65 | 0.69 | -225 | +374 | 93% | 0.1895 | 0.1677 |
| Time-of-day vol x0.5, against trend + skip spikes | 509 | 82% | +148.68 | +3.0% | 1.35 | 1.41 | -110 | +259 | 93% | 0.1589 | 0.1494 |
| Bayes price-level, 95% sure | 665 | 92% | +130.48 | +2.0% | 1.68 | 0.91 | +2 | +129 | 93% | 0.0756 | 0.0766 |
| Vol x0.5, skip spiked markets | 1100 | 79% | +104.63 | +1.0% | 0.6 | 0.75 | -163 | +268 | 93% | 0.1836 | 0.1634 |
| Vol x0.5, calm market only | 1046 | 79% | +89.34 | +0.9% | 0.55 | 0.71 | -105 | +194 | 92% | 0.1777 | 0.1606 |
| Long-shot fade (no model) | 1309 | 96% | +72.78 | +0.6% | 1.08 | 1.05 | -45 | +118 | – | – | 0.0347 |
| Bayes price-level, 99% sure | 330 | 92% | +65.32 | +2.1% | 1.17 | 1.08 | +42 | +24 | 93% | 0.0786 | 0.0799 |
| Vol x0.5, against the 24h trend | 827 | 78% | +54.54 | +0.7% | 0.34 | 0.71 | -197 | +252 | 93% | 0.1871 | 0.1658 |
| Vol x0.5, against trend + skip spikes | 579 | 79% | +52.18 | +0.9% | 0.41 | 0.59 | -78 | +130 | 93% | 0.1797 | 0.16 |
| Combined: rolling best (past 6 months) | 303 | 80% | +51.97 | +1.8% | 0.63 | -0.21 | -56 | +108 | 92% | 0.1674 | 0.1533 |
| Vol x0.5 | 1786 | 78% | +39.35 | +0.2% | 0.18 | 0.31 | -309 | +348 | 93% | 0.1909 | 0.1679 |
| Vol x0.5, news days only | 105 | 78% | +30.78 | +3.0% | 0.58 | 0.56 | -1 | +32 | 93% | 0.1865 | 0.1727 |
| Vol x0.5, skip news in window | 1762 | 78% | +19.95 | +0.1% | 0.09 | 0.22 | -296 | +316 | 93% | 0.1914 | 0.1681 |
| Vol x0.5, skip news days | 1681 | 78% | +8.57 | +0.1% | 0.03 | 0.17 | -295 | +303 | 93% | 0.1912 | 0.1676 |
| Bayes: market prior + full vol | 3 | 67% | -6.07 | -20.9% | -0.53 | -0.69 | +2 | -8 | 92% | 0.2927 | 0.2732 |
| Vol x0.5, with the 24h trend | 959 | 78% | -15.19 | -0.2% | -0.08 | -0.54 | -113 | +98 | 93% | 0.1943 | 0.1698 |
| Bayes: market prior + fat-tail | 14 | 57% | -37.12 | -26.9% | -1.51 | -1.2 | -18 | -19 | 86% | 0.3377 | 0.2814 |
| Vol x0.5, busy market only | 740 | 76% | -49.99 | -0.7% | -0.34 | -0.34 | -203 | +153 | 93% | 0.2097 | 0.1783 |
| Fat-tail, moves x0.5 | 1876 | 73% | -88.38 | -0.5% | -0.34 | -0.4 | -201 | +113 | 89% | 0.2237 | 0.1958 |
| Vol x0.5, weekdays only | 1548 | 77% | -123.40 | -0.8% | -0.59 | -0.58 | -296 | +173 | 93% | 0.2016 | 0.1743 |
| Fat-tail, moves x0.75 | 1188 | 72% | -186.00 | -1.6% | -0.84 | -0.77 | -199 | +13 | 86% | 0.2087 | 0.191 |
| Vol x0.5, stop loss 25c | 1786 | 65% | -451.95 | -2.6% | -2.45 | -2.61 | -742 | +290 | 93% | 0.3058 | 0.2346 |
| Vol x0.75 | 803 | 72% | -512.71 | -6.5% | -2.31 | -2.67 | -329 | -183 | 85% | 0.1725 | 0.1545 |
| Fat-tail (actual past moves) | 647 | 59% | -641.13 | -10.0% | -2.01 | -1.36 | -582 | -59 | 73% | 0.2016 | 0.1811 |
| Heavy-volume move: follow | 1244 | 62% | -643.64 | -5.2% | -1.99 | -1.3 | -579 | -64 | – | – | 0.1844 |
| Vol x0.5, take profit 10c | 1786 | 81% | -733.00 | -4.2% | -3.77 | -3.37 | -692 | -41 | 93% | 0.1663 | 0.1553 |
| Heavy-volume move (10c, 5x): follow | 739 | 60% | -853.48 | -11.6% | -3.88 | -2.9 | -502 | -351 | – | – | 0.1839 |
| Vol x0.5, stop loss 10c | 1786 | 47% | -1037.30 | -5.9% | -6.84 | -6.85 | -1069 | +32 | 93% | 0.4592 | 0.3253 |
| Combined: 5+ strategies agree | 2274 | 71% | -1061.35 | -4.7% | -2.5 | -3.42 | -1003 | -58 | 84% | 0.1769 | 0.1572 |
| Vol x0.5, take profit 15c / stop 15c | 1786 | 57% | -1109.66 | -6.4% | -7.49 | -7.63 | -1086 | -24 | 93% | 0.3719 | 0.2755 |
| v1 + 50% market blend | 292 | 31% | -1140.91 | -38.0% | -4.16 | -3.94 | -623 | -518 | 42% | 0.1148 | 0.1023 |
| Options vol x0.85, 5c gap | 822 | 56% | -1207.45 | -14.6% | -3.01 | -2.74 | -730 | -477 | 66% | 0.1236 | 0.1122 |
| Heavy-volume move (10c, 5x): fade | 785 | 37% | -1267.47 | -15.7% | -3.14 | -3.11 | -667 | -601 | – | – | 0.1745 |
| v1 (what we ran live) | 457 | 38% | -1387.50 | -29.7% | -3.93 | -3.53 | -992 | -395 | 54% | 0.1288 | 0.1005 |
| Options vol, 8c gap | 419 | 24% | -1427.50 | -32.8% | -3.44 | -2.73 | -1046 | -382 | 40% | 0.1124 | 0.0847 |
| Options vol, NO only | 595 | 31% | -1760.74 | -28.8% | -3.78 | -3.35 | -1398 | -363 | 45% | 0.1252 | 0.1038 |
| Vol x0.5, limit order | 959 | 60% | -1811.01 | -19.6% | -9.06 | -9.44 | -1109 | -702 | 92% | 0.3469 | 0.2566 |
| Vol x0.5, limit order (strict fill) | 923 | 58% | -1927.98 | -21.6% | -9.78 | -9.95 | -1158 | -770 | 92% | 0.3602 | 0.2642 |
| Vol x0.5 5c edge, limit order | 1049 | 59% | -2057.10 | -20.3% | -9.8 | -10.14 | -1235 | -822 | 92% | 0.3389 | 0.2531 |
| Options vol, 5c gap | 685 | 31% | -2155.25 | -30.5% | -4.58 | -4.47 | -1310 | -845 | 44% | 0.1148 | 0.094 |
| Heavy-volume move: fade | 1297 | 36% | -2252.19 | -16.9% | -4.25 | -4.41 | -874 | -1378 | – | – | 0.177 |
| Combined: 3+ strategies agree | 3330 | 65% | -2618.93 | -7.9% | -4.5 | -5.02 | -2025 | -594 | 82% | 0.1745 | 0.1565 |
| Kalshi price-spike fade (no model) | 1254 | 30% | -3204.26 | -24.8% | -6.0 | -5.62 | -1663 | -1541 | – | – | 0.1516 |

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
| 0.4 | 1984 | +23.16 | +0.1% |
| 0.5 | 1786 | +39.35 | +0.2% |
| 0.6 | 1416 | -265.09 | -1.9% |
| 0.75 | 803 | -512.71 | -6.5% |
| 1.0 | 457 | -1387.50 | -29.7% |
| 1.25 | 550 | -2426.05 | -42.1% |

Sweep: options vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 1606 | -245.33 | -1.6% |
| 0.7 | 1295 | -743.58 | -5.8% |
| 0.8 | 956 | -890.38 | -9.4% |
| 0.9 | 751 | -1608.60 | -21.1% |
| 1.0 | 685 | -2155.25 | -30.5% |
| 1.1 | 757 | -2902.09 | -36.8% |

Sweep: time-of-day vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1976 | +30.45 | +0.2% |
| 0.5 | 1556 | +280.21 | +1.8% |
| 0.6 | 1042 | +258.20 | +2.5% |
| 0.75 | 432 | -36.61 | -0.9% |
| 1.0 | 324 | -1069.50 | -32.0% |

Sweep: fat-tail

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 2074 | -107.28 | -0.5% |
| 0.5 | 1876 | -88.38 | -0.5% |
| 0.6 | 1635 | -13.94 | -0.1% |
| 0.75 | 1188 | -186.00 | -1.6% |
| 0.9 | 802 | -639.59 | -8.1% |
| 1.0 | 647 | -641.13 | -10.0% |

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
| 2026-Q4 | 96 | 1.285 |

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
| Quarter | 2026-Q4 | 56 | +88 | 41% |
| Price paid | 0.00-0.10 | 65 | -414 | 3% |
| Price paid | 0.10-0.30 | 196 | -996 | 8% |
| Price paid | 0.30-0.50 | 3 | -9 | 33% |
| Price paid | 0.50-0.70 | 12 | +4 | 67% |
| Price paid | 0.70-0.90 | 180 | +25 | 82% |
| Price paid | 0.90-1.01 | 1 | +1 | 100% |
| Model vs market gap | 0.05-0.10 | 21 | +189 | 57% |
| Model vs market gap | 0.10-0.20 | 398 | -1305 | 39% |
| Model vs market gap | 0.20-0.35 | 38 | -272 | 24% |
| Side | no | 296 | -834 | 38% |
| Side | yes | 161 | -553 | 38% |

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
| Quarter | 2026-Q4 | 141 | +46 | 79% |
| Price paid | 0.00-0.10 | 2 | -21 | 0% |
| Price paid | 0.10-0.30 | 3 | -32 | 0% |
| Price paid | 0.30-0.50 | 2 | +1 | 50% |
| Price paid | 0.50-0.70 | 209 | +142 | 72% |
| Price paid | 0.70-0.90 | 1561 | -49 | 79% |
| Price paid | 0.90-1.01 | 9 | -2 | 89% |
| Model vs market gap | 0.05-0.10 | 15 | -12 | 80% |
| Model vs market gap | 0.10-0.20 | 1241 | -5 | 80% |
| Model vs market gap | 0.20-0.35 | 529 | +52 | 74% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 1003 | +15 | 78% |
| Side | yes | 783 | +25 | 78% |

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
| Quarter | 2026-Q4 | 110 | -199 | 33% |
| Price paid | 0.10-0.30 | 697 | -3015 | 12% |
| Price paid | 0.30-0.50 | 297 | -454 | 34% |
| Price paid | 0.50-0.70 | 186 | +143 | 65% |
| Price paid | 0.70-0.90 | 74 | +122 | 89% |
| Model vs market gap | no model | 1254 | -3204 | 30% |
| Side | no | 607 | -1292 | 42% |
| Side | yes | 647 | -1913 | 18% |

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
| Quarter | 2026-Q4 | 45 | -7 | 78% |
| Price paid | 0.10-0.30 | 1 | -11 | 0% |
| Price paid | 0.50-0.70 | 39 | +20 | 72% |
| Price paid | 0.70-0.90 | 464 | +156 | 83% |
| Price paid | 0.90-1.01 | 5 | -17 | 60% |
| Model vs market gap | 0.05-0.10 | 12 | -4 | 83% |
| Model vs market gap | 0.10-0.20 | 424 | +132 | 82% |
| Model vs market gap | 0.20-0.35 | 73 | +21 | 77% |
| Side | no | 285 | +118 | 83% |
| Side | yes | 224 | +31 | 80% |

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
| Quarter | 2026-Q4 | 166 | +41 | 80% |
| Price paid | 0.10-0.30 | 2 | -21 | 0% |
| Price paid | 0.30-0.50 | 2 | +1 | 50% |
| Price paid | 0.50-0.70 | 133 | +104 | 73% |
| Price paid | 0.70-0.90 | 1411 | +210 | 81% |
| Price paid | 0.90-1.01 | 8 | -14 | 75% |
| Model vs market gap | 0.05-0.10 | 22 | -1 | 86% |
| Model vs market gap | 0.10-0.20 | 1261 | +189 | 81% |
| Model vs market gap | 0.20-0.35 | 272 | +88 | 76% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 893 | +225 | 80% |
| Side | yes | 663 | +56 | 80% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 93 | -18 | 91% |
| Quarter | 2025-Q3 | 21 | -41 | 71% |
| Quarter | 2025-Q4 | 4 | +2 | 75% |
| Quarter | 2026-Q1 | 7 | +10 | 100% |
| Quarter | 2026-Q2 | 140 | +32 | 91% |
| Quarter | 2026-Q3 | 238 | +115 | 94% |
| Quarter | 2026-Q4 | 162 | +30 | 91% |
| Price paid | 0.50-0.70 | 3 | +21 | 100% |
| Price paid | 0.70-0.90 | 184 | +104 | 89% |
| Price paid | 0.90-1.01 | 478 | +5 | 93% |
| Model vs market gap | 0.00-0.05 | 433 | +68 | 93% |
| Model vs market gap | 0.05-0.10 | 214 | +46 | 89% |
| Model vs market gap | 0.10-0.20 | 18 | +16 | 94% |
| Side | no | 270 | +84 | 94% |
| Side | yes | 395 | +47 | 90% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 139 | -79 | 74% |
| Quarter | 2026-Q1 | 52 | +90 | 90% |
| Quarter | 2026-Q2 | 48 | +70 | 90% |
| Quarter | 2026-Q3 | 19 | -23 | 74% |
| Quarter | 2026-Q4 | 45 | -7 | 78% |
| Price paid | 0.00-0.10 | 2 | -21 | 0% |
| Price paid | 0.10-0.30 | 2 | -21 | 0% |
| Price paid | 0.30-0.50 | 1 | -10 | 0% |
| Price paid | 0.50-0.70 | 37 | +58 | 78% |
| Price paid | 0.70-0.90 | 258 | +54 | 82% |
| Price paid | 0.90-1.01 | 3 | -8 | 67% |
| Model vs market gap | 0.05-0.10 | 11 | -18 | 73% |
| Model vs market gap | 0.10-0.20 | 222 | +90 | 83% |
| Model vs market gap | 0.20-0.35 | 69 | -25 | 71% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 165 | +100 | 82% |
| Side | yes | 138 | -48 | 77% |

## Weather: daily highs: late entries

2699 events, 2025-03-21 to 2026-11-18.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Late long-shot fade 1-4c (+49 on 970 trades).

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Late long-shot fade 1-4c | 970 | 99% | +48.61 | +0.5% | 1.73 | 1.82 | -6 | +55 | – | – | 0.0084 |
| Combined: 3+ strategies agree | 683 | 81% | +26.13 | +0.4% | 0.19 | 0.25 | +57 | -31 | 92% | 0.1687 | 0.1488 |
| Late favorite 90-97c | 824 | 95% | +9.43 | +0.1% | 0.15 | 0.15 | -4 | +13 | – | – | 0.0487 |
| Bayes price-level, 99% sure | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Late long-shot fade | 743 | 95% | -11.86 | -0.2% | -0.2 | -0.37 | -36 | +24 | – | – | 0.0437 |
| Bayes price-level, 95% sure | 64 | 84% | -34.18 | -5.4% | -1.07 | -0.52 | -9 | -26 | 93% | 0.1359 | 0.1269 |
| Combined: rolling best (past 6 months) | 549 | 97% | -39.64 | -0.7% | -1.01 | -1.05 | -66 | +26 | – | – | 0.0278 |
| Late favorite 80-90c | 438 | 86% | -48.57 | -1.1% | -0.59 | -0.59 | -1 | -47 | – | – | 0.1226 |
| Combined: 5+ strategies agree | 438 | 86% | -48.57 | -1.1% | -0.59 | -0.59 | -1 | -47 | – | – | 0.1226 |
| Late fav 80-90c, stop loss 25c | 438 | 82% | -84.50 | -2.0% | -1.06 | -1.06 | -28 | -56 | – | – | 0.1461 |
| Late fav 80-90c, stop loss 10c | 438 | 78% | -95.77 | -2.2% | -1.26 | -1.26 | -28 | -67 | – | – | 0.1729 |
| Late fav 80-90c, take profit 15c / stop 15c | 438 | 80% | -114.98 | -2.7% | -1.48 | -1.48 | -47 | -68 | – | – | 0.1587 |
| Late fav 80-90c, take profit 10c | 438 | 86% | -120.24 | -2.8% | -1.5 | -1.5 | -30 | -90 | – | – | 0.1214 |
| Late favorite 50-80c | 548 | 67% | -168.69 | -3.1% | -1.04 | -1.04 | -103 | -65 | – | – | 0.2136 |
| Heavy-volume move (10c, 5x): follow | 851 | 72% | -464.52 | -5.5% | -2.37 | -2.15 | -355 | -109 | – | – | 0.1655 |
| Heavy-volume move: follow | 1320 | 69% | -493.85 | -3.8% | -1.61 | -0.97 | -518 | +24 | – | – | 0.1685 |
| Heavy-volume move (10c, 5x): fade | 1015 | 25% | -2273.84 | -21.6% | -4.12 | -4.0 | -831 | -1443 | – | – | 0.1488 |
| Heavy-volume move: fade | 1592 | 26% | -3719.27 | -22.6% | -5.51 | -5.2 | -2198 | -1521 | – | – | 0.1497 |

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
| Quarter | 2026-Q4 | 76 | +10 | 100% |
| Price paid | 0.90-1.01 | 549 | -40 | 97% |
| Model vs market gap | no model | 549 | -40 | 97% |
| Side | no | 549 | -40 | 97% |

## Weather: daily lows: late entries

1856 events, 2025-12-13 to 2026-11-18.

**Verdict:** Heavy-volume move: fade: +424 on 748 trades (+5.5% per $ staked, t=0.78), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Heavy-volume move: fade | 748 | 35% | +424.48 | +5.5% | 0.78 | 0.71 | +416 | +8 | – | – | 0.1656 |
| Heavy-volume move (10c, 5x): fade | 332 | 30% | +122.05 | +3.5% | 0.32 | -0.29 | +130 | -7 | – | – | 0.161 |
| Bayes price-level, 99% sure | 10 | 60% | +41.84 | +40.6% | 1.07 | 1.07 | +22 | +20 | 58% | 0.2435 | 0.2878 |
| Combined: rolling best (past 6 months) | 329 | 32% | -6.15 | -0.2% | -0.0 | -0.2 | -341 | +335 | – | – | 0.1614 |
| Bayes price-level, 95% sure | 34 | 44% | -14.21 | -4.1% | -0.22 | -0.19 | -24 | +10 | 60% | 0.2982 | 0.2876 |
| Late favorite 90-97c | 889 | 94% | -80.90 | -0.9% | -1.16 | -1.16 | -45 | -36 | – | – | 0.0544 |
| Late favorite 80-90c | 373 | 82% | -204.54 | -5.6% | -2.46 | -2.46 | -108 | -97 | – | – | 0.1455 |
| Combined: 5+ strategies agree | 373 | 82% | -204.54 | -5.6% | -2.46 | -2.46 | -108 | -97 | – | – | 0.1455 |
| Late long-shot fade 1-4c | 1887 | 98% | -210.34 | -1.1% | -3.14 | -2.94 | -144 | -66 | – | – | 0.0237 |
| Combined: 3+ strategies agree | 427 | 79% | -253.40 | -6.1% | -2.52 | -2.64 | -174 | -79 | 55% | 0.1882 | 0.1594 |
| Late fav 80-90c, take profit 10c | 373 | 83% | -254.73 | -7.0% | -3.15 | -3.15 | -130 | -124 | – | – | 0.1435 |
| Heavy-volume move (10c, 5x): follow | 245 | 64% | -311.58 | -12.8% | -2.46 | -1.99 | -192 | -119 | – | – | 0.1725 |
| Late long-shot fade | 1353 | 93% | -360.25 | -2.8% | -3.88 | -3.62 | -275 | -86 | – | – | 0.0633 |
| Late fav 80-90c, stop loss 25c | 373 | 62% | -401.91 | -11.0% | -5.87 | -5.87 | -244 | -158 | – | – | 0.2825 |
| Late fav 80-90c, take profit 15c / stop 15c | 373 | 48% | -437.93 | -12.0% | -7.76 | -7.76 | -255 | -183 | – | – | 0.3746 |
| Late fav 80-90c, stop loss 10c | 373 | 39% | -438.51 | -12.0% | -8.56 | -8.56 | -254 | -184 | – | – | 0.4374 |
| Late favorite 50-80c | 431 | 58% | -648.53 | -15.2% | -4.23 | -4.23 | -235 | -414 | – | – | 0.2369 |
| Heavy-volume move: follow | 586 | 57% | -1186.73 | -20.3% | -5.66 | -5.48 | -546 | -640 | – | – | 0.1761 |

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

Why: Heavy-volume move: fade

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q4 | 6 | +58 | 33% |
| Quarter | 2026-Q1 | 194 | -156 | 34% |
| Quarter | 2026-Q2 | 219 | +529 | 40% |
| Quarter | 2026-Q3 | 224 | -257 | 31% |
| Quarter | 2026-Q4 | 105 | +251 | 36% |
| Price paid | 0.10-0.30 | 473 | +144 | 18% |
| Price paid | 0.30-0.50 | 112 | +244 | 47% |
| Price paid | 0.50-0.70 | 55 | -14 | 60% |
| Price paid | 0.70-0.90 | 104 | +47 | 85% |
| Price paid | 0.90-1.01 | 4 | +4 | 100% |
| Model vs market gap | no model | 748 | +424 | 35% |
| Side | no | 427 | +361 | 41% |
| Side | yes | 321 | +64 | 27% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q3 | 224 | -257 | 31% |
| Quarter | 2026-Q4 | 105 | +251 | 36% |
| Price paid | 0.10-0.30 | 220 | -194 | 16% |
| Price paid | 0.30-0.50 | 50 | +170 | 54% |
| Price paid | 0.50-0.70 | 21 | +18 | 67% |
| Price paid | 0.70-0.90 | 35 | -4 | 80% |
| Price paid | 0.90-1.01 | 3 | +3 | 100% |
| Model vs market gap | no model | 329 | -6 | 32% |
| Side | no | 203 | -75 | 36% |
| Side | yes | 126 | +69 | 27% |

## Bitcoin: last 1-3 hours

606 events, 2025-03-22 to 2026-11-18.

**Verdict:** Late long-shot fade 1-4c: +92 on 901 trades (+1.0% per $ staked, t=6.45), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bayes price-level, 99% sure | 553 | 94% | +175.52 | +3.3% | 2.89 | 2.75 | +116 | +60 | 96% | 0.0527 | 0.0549 |
| Bayes price-level, 95% sure | 944 | 92% | +167.72 | +1.8% | 1.81 | 2.18 | +44 | +124 | 94% | 0.0723 | 0.0729 |
| Late long-shot fade | 760 | 97% | +114.48 | +1.6% | 2.57 | 2.04 | +25 | +89 | – | – | 0.0279 |
| Combined: rolling best (past 6 months) | 759 | 96% | +113.11 | +1.5% | 2.03 | 1.67 | +23 | +90 | 94% | 0.0702 | 0.0328 |
| Late long-shot fade 1-4c | 901 | 100% | +91.69 | +1.0% | 6.45 | 6.03 | +38 | +54 | – | – | 0.0025 |
| Combined: 3+ strategies agree | 259 | 89% | +81.12 | +3.2% | 1.41 | 1.44 | +7 | +74 | 90% | 0.0961 | 0.092 |
| Late favorite 90-97c | 202 | 96% | +23.09 | +1.2% | 0.87 | 0.87 | +29 | -6 | – | – | 0.0341 |
| Late favorite 80-90c | 47 | 87% | -0.31 | -0.1% | 0.01 | 0.01 | -1 | +1 | – | – | 0.1141 |
| Combined: 5+ strategies agree | 47 | 87% | -0.31 | -0.1% | 0.01 | 0.01 | -1 | +1 | – | – | 0.1141 |
| Late favorite 50-80c | 31 | 68% | -0.41 | -0.1% | 0.01 | 0.01 | -31 | +31 | – | – | 0.2216 |
| Late fav 80-90c, take profit 10c | 47 | 87% | -1.58 | -0.3% | -0.04 | -0.04 | -1 | -0 | – | – | 0.1141 |
| Late fav 80-90c, stop loss 25c | 47 | 74% | -29.82 | -6.5% | -1.1 | -1.1 | -34 | +4 | – | – | 0.2007 |
| Late fav 80-90c, stop loss 10c | 47 | 60% | -47.16 | -10.2% | -1.87 | -1.87 | -49 | +2 | – | – | 0.2943 |
| Late fav 80-90c, take profit 15c / stop 15c | 47 | 64% | -48.94 | -10.6% | -1.84 | -1.84 | -49 | -0 | – | – | 0.2697 |
| Heavy-volume move (10c, 5x): follow | 802 | 66% | -630.59 | -8.0% | -2.97 | -2.23 | -338 | -293 | – | – | 0.1777 |
| Heavy-volume move: follow | 1320 | 66% | -1011.54 | -7.7% | -3.62 | -3.04 | -623 | -388 | – | – | 0.1704 |
| Heavy-volume move (10c, 5x): fade | 871 | 31% | -1782.72 | -19.8% | -3.96 | -3.76 | -1181 | -602 | – | – | 0.1658 |
| Heavy-volume move: fade | 1403 | 30% | -3448.98 | -23.8% | -6.18 | -5.37 | -2178 | -1271 | – | – | 0.1555 |

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
| Quarter | 2026-Q4 | 160 | +19 | 100% |
| Price paid | 0.90-1.01 | 901 | +92 | 100% |
| Model vs market gap | no model | 901 | +92 | 100% |
| Side | no | 901 | +92 | 100% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 11 | -3 | 91% |
| Quarter | 2025-Q3 | 58 | +11 | 93% |
| Quarter | 2025-Q4 | 76 | -19 | 88% |
| Quarter | 2026-Q1 | 135 | +35 | 95% |
| Quarter | 2026-Q2 | 257 | +10 | 91% |
| Quarter | 2026-Q3 | 250 | +199 | 96% |
| Quarter | 2026-Q4 | 157 | -66 | 86% |
| Price paid | 0.50-0.70 | 2 | -5 | 50% |
| Price paid | 0.70-0.90 | 394 | +104 | 86% |
| Price paid | 0.90-1.01 | 548 | +69 | 96% |
| Model vs market gap | 0.00-0.05 | 423 | +68 | 97% |
| Model vs market gap | 0.05-0.10 | 449 | +89 | 89% |
| Model vs market gap | 0.10-0.20 | 72 | +10 | 83% |
| Side | no | 160 | +22 | 90% |
| Side | yes | 784 | +145 | 92% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 50 | -0 | 96% |
| Quarter | 2025-Q4 | 29 | +3 | 100% |
| Quarter | 2026-Q1 | 127 | +17 | 100% |
| Quarter | 2026-Q2 | 260 | +14 | 99% |
| Quarter | 2026-Q3 | 181 | +141 | 96% |
| Quarter | 2026-Q4 | 112 | -62 | 86% |
| Price paid | 0.70-0.90 | 124 | +26 | 86% |
| Price paid | 0.90-1.01 | 635 | +87 | 99% |
| Model vs market gap | 0.00-0.05 | 132 | +38 | 98% |
| Model vs market gap | 0.05-0.10 | 150 | +36 | 88% |
| Model vs market gap | 0.10-0.20 | 11 | +6 | 82% |
| Model vs market gap | no model | 466 | +33 | 99% |
| Side | no | 523 | +82 | 99% |
| Side | yes | 236 | +31 | 92% |

## Ethereum

601 events, 2025-03-27 to 2026-11-18.

**Verdict:** Market favorite (no model): +112 on 115 trades (+9.8% per $ staked, t=1.26), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Time-of-day vol x0.5, skip spikes | 797 | 82% | +165.26 | +2.1% | 1.25 | 1.12 | -57 | +222 | 92% | 0.1521 | 0.1432 |
| Time-of-day vol x0.5, against trend + skip spikes | 439 | 84% | +153.87 | +3.6% | 1.61 | 1.46 | -25 | +179 | 93% | 0.142 | 0.1363 |
| Market favorite (no model) | 115 | 67% | +112.49 | +9.8% | 1.26 | 1.26 | +73 | +39 | – | – | 0.2027 |
| Time-of-day vol x0.5 | 1252 | 81% | +106.92 | +0.9% | 0.63 | 1.32 | -154 | +261 | 92% | 0.1596 | 0.1474 |
| Vol x0.5, weekends only | 154 | 82% | +65.16 | +4.3% | 0.81 | 1.03 | -5 | +71 | 92% | 0.1389 | 0.133 |
| Bayes price-level, 95% sure | 48 | 79% | +59.81 | +12.6% | 1.43 | 1.43 | +43 | +17 | 77% | 0.1517 | 0.1603 |
| Vol x0.5, skip spiked markets | 931 | 80% | +31.42 | +0.4% | 0.2 | -0.24 | -207 | +238 | 93% | 0.1741 | 0.1579 |
| Vol x0.5, against trend + skip spikes | 507 | 80% | +0.15 | +0.0% | -0.01 | -0.17 | -159 | +159 | 93% | 0.1774 | 0.1599 |
| Bayes: market prior + full vol | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Bayes: market prior + fat-tail | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Long-shot fade (no model) | 611 | 95% | -20.82 | -0.4% | -0.36 | -0.26 | -89 | +68 | – | – | 0.0442 |
| Bayes price-level, 99% sure | 3 | 0% | -29.77 | -100.0% | – | – | -10 | -20 | 72% | 0.5155 | 0.3521 |
| Combined: rolling best (past 6 months) | 270 | 79% | -33.86 | -1.3% | -0.4 | -0.55 | -102 | +68 | 93% | 0.1661 | 0.1551 |
| Vol x0.5, news days only | 83 | 75% | -46.16 | -5.7% | -0.93 | -1.27 | -30 | -17 | 92% | 0.2044 | 0.1751 |
| Vol x0.75 | 411 | 77% | -46.54 | -1.2% | -0.29 | -0.53 | -175 | +128 | 88% | 0.1599 | 0.1473 |
| Fat-tail (actual past moves) | 347 | 67% | -51.67 | -1.5% | -0.22 | -0.23 | -200 | +148 | 78% | 0.1859 | 0.1725 |
| Vol x0.5, calm market only | 762 | 79% | -68.39 | -0.9% | -0.45 | -0.16 | -206 | +138 | 92% | 0.1773 | 0.1599 |
| Vol x0.5, 5c edge | 1723 | 79% | -77.86 | -0.5% | -0.36 | 0.02 | -385 | +307 | 92% | 0.1756 | 0.1585 |
| Vol x0.5, against the 24h trend | 711 | 78% | -78.03 | -1.1% | -0.53 | -0.63 | -285 | +207 | 93% | 0.1847 | 0.1645 |
| Vol x0.5, with the 24h trend | 734 | 78% | -131.75 | -1.8% | -0.95 | -1.0 | -110 | -22 | 92% | 0.1855 | 0.1631 |
| Regime-scaled vol x0.5 | 1602 | 79% | -135.75 | -0.9% | -0.66 | 0.2 | -340 | +204 | 93% | 0.1801 | 0.1598 |
| Vol x0.5, busy market only | 683 | 78% | -141.39 | -2.1% | -1.04 | -0.89 | -155 | +13 | 93% | 0.1937 | 0.1682 |
| Vol x0.5, skip news days | 1362 | 78% | -163.62 | -1.2% | -0.84 | -0.37 | -355 | +191 | 93% | 0.1839 | 0.1631 |
| Vol x0.5, NO only | 911 | 78% | -197.76 | -2.2% | -1.26 | -1.26 | -230 | +32 | 92% | 0.1829 | 0.162 |
| Vol x0.5, skip news in window | 1422 | 78% | -204.94 | -1.5% | -1.02 | -0.64 | -383 | +178 | 93% | 0.1855 | 0.1641 |
| Vol x0.5 (Bitcoin's winner) | 1445 | 78% | -209.78 | -1.5% | -1.04 | -0.73 | -384 | +174 | 93% | 0.1851 | 0.1638 |
| Fat-tail, moves x0.75 | 897 | 73% | -211.77 | -2.4% | -1.16 | -1.32 | -225 | +14 | 86% | 0.2045 | 0.1868 |
| Full vol + 50% market blend | 100 | 25% | -218.29 | -21.0% | -0.85 | -0.69 | -347 | +128 | 35% | 0.117 | 0.1064 |
| Vol x0.5, weekdays only | 1291 | 78% | -274.94 | -2.2% | -1.44 | -1.18 | -377 | +102 | 93% | 0.1906 | 0.1675 |
| Fat-tail, moves x0.5 | 1729 | 74% | -339.95 | -2.0% | -1.4 | -1.31 | -396 | +56 | 90% | 0.2074 | 0.1817 |
| Options vol x0.85, 5c gap | 443 | 57% | -387.91 | -8.7% | -1.0 | -0.83 | -565 | +177 | 67% | 0.1301 | 0.1173 |
| Options vol, NO only | 216 | 27% | -513.87 | -23.0% | -1.42 | -1.16 | -596 | +82 | 42% | 0.1198 | 0.0962 |
| Heavy-volume move (10c, 5x): follow | 414 | 60% | -526.25 | -12.8% | -3.18 | -3.01 | -262 | -264 | – | – | 0.1813 |
| Options vol, 8c gap | 199 | 17% | -569.59 | -27.5% | -1.47 | -1.17 | -716 | +146 | 36% | 0.1251 | 0.0904 |
| Vol x0.5, take profit 10c | 1445 | 81% | -618.13 | -4.4% | -3.52 | -3.02 | -576 | -42 | 93% | 0.1653 | 0.1533 |
| Combined: 5+ strategies agree | 1717 | 74% | -711.58 | -4.2% | -2.11 | -1.7 | -762 | +50 | 87% | 0.1766 | 0.1597 |
| Vol x0.5, stop loss 25c | 1445 | 65% | -750.96 | -5.3% | -4.31 | -4.0 | -749 | -2 | 93% | 0.3044 | 0.2371 |
| Heavy-volume move (10c, 5x): fade | 463 | 35% | -860.78 | -18.1% | -2.75 | -2.9 | -180 | -681 | – | – | 0.1648 |
| Full vol (v1 rule) | 221 | 30% | -863.23 | -37.9% | -3.12 | -2.77 | -735 | -128 | 47% | 0.1172 | 0.0874 |
| Heavy-volume move: follow | 756 | 57% | -1003.79 | -13.3% | -3.96 | -3.58 | -445 | -559 | – | – | 0.1862 |
| Vol x0.5, take profit 15c / stop 15c | 1445 | 57% | -1021.14 | -7.2% | -7.43 | -6.74 | -866 | -156 | 93% | 0.3712 | 0.2813 |
| Heavy-volume move: fade | 818 | 38% | -1063.90 | -12.7% | -2.51 | -2.94 | -326 | -737 | – | – | 0.1729 |
| Vol x0.5, stop loss 10c | 1445 | 47% | -1111.11 | -7.9% | -7.62 | -7.1 | -960 | -151 | 93% | 0.4541 | 0.3311 |
| Options vol, 5c gap | 388 | 23% | -1476.45 | -36.7% | -3.44 | -3.24 | -1212 | -264 | 39% | 0.1158 | 0.0895 |
| Vol x0.5, limit order | 725 | 57% | -1712.55 | -24.5% | -9.96 | -11.26 | -1113 | -599 | 92% | 0.3562 | 0.2676 |
| Vol x0.5, limit order (strict fill) | 704 | 56% | -1764.63 | -26.0% | -10.35 | -11.63 | -1127 | -638 | 92% | 0.3667 | 0.2744 |
| Combined: 3+ strategies agree | 2441 | 66% | -1887.79 | -7.8% | -3.57 | -3.15 | -1377 | -511 | 84% | 0.1713 | 0.1576 |
| Vol x0.5 5c edge, limit order | 846 | 58% | -1909.73 | -23.4% | -10.27 | -11.73 | -1239 | -671 | 91% | 0.3421 | 0.2614 |
| Kalshi price-spike fade (no model) | 1068 | 31% | -2336.06 | -21.2% | -4.77 | -4.42 | -846 | -1490 | – | – | 0.1703 |

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
| 0.3 | 2039 | -115.20 | -0.6% |
| 0.4 | 1804 | -291.66 | -1.7% |
| 0.5 | 1445 | -209.78 | -1.5% |
| 0.6 | 976 | -234.27 | -2.5% |
| 0.75 | 411 | -46.54 | -1.2% |
| 1.0 | 221 | -863.23 | -37.9% |

Sweep: time-of-day vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1709 | -13.30 | -0.1% |
| 0.5 | 1252 | +106.92 | +0.9% |
| 0.6 | 707 | -97.41 | -1.4% |
| 0.75 | 234 | -284.27 | -12.3% |
| 1.0 | 241 | -918.06 | -36.6% |

Sweep: fat-tail

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1984 | -160.11 | -0.8% |
| 0.5 | 1729 | -339.95 | -2.0% |
| 0.6 | 1392 | -151.16 | -1.1% |
| 0.75 | 897 | -211.77 | -2.4% |
| 0.9 | 513 | -220.79 | -4.4% |
| 1.0 | 347 | -51.67 | -1.5% |

Sweep: options vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 1361 | -388.97 | -2.9% |
| 0.7 | 889 | -352.40 | -4.0% |
| 0.8 | 536 | -403.82 | -7.6% |
| 0.9 | 381 | -645.09 | -16.7% |
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
| Quarter | 2026-Q4 | 9 | +14 | 78% |
| Price paid | 0.30-0.50 | 27 | +39 | 48% |
| Price paid | 0.50-0.70 | 60 | -11 | 62% |
| Price paid | 0.70-0.90 | 28 | +84 | 96% |
| Model vs market gap | no model | 115 | +112 | 67% |
| Side | yes | 115 | +112 | 67% |

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
| Quarter | 2026-Q4 | 81 | -286 | 30% |
| Price paid | 0.10-0.30 | 533 | -2036 | 13% |
| Price paid | 0.30-0.50 | 301 | -323 | 36% |
| Price paid | 0.50-0.70 | 181 | +28 | 60% |
| Price paid | 0.70-0.90 | 53 | -5 | 76% |
| Model vs market gap | no model | 1068 | -2336 | 31% |
| Side | no | 493 | -1258 | 34% |
| Side | yes | 575 | -1078 | 28% |

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
| Quarter | 2026-Q4 | 41 | +7 | 83% |
| Price paid | 0.50-0.70 | 35 | +66 | 80% |
| Price paid | 0.70-0.90 | 384 | +89 | 84% |
| Price paid | 0.90-1.01 | 20 | -1 | 90% |
| Model vs market gap | 0.05-0.10 | 7 | +8 | 100% |
| Model vs market gap | 0.10-0.20 | 394 | +149 | 84% |
| Model vs market gap | 0.20-0.35 | 37 | -8 | 73% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 212 | +135 | 87% |
| Side | yes | 227 | +19 | 81% |

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
| Quarter | 2026-Q4 | 123 | +49 | 83% |
| Price paid | 0.10-0.30 | 4 | -42 | 0% |
| Price paid | 0.50-0.70 | 139 | +44 | 69% |
| Price paid | 0.70-0.90 | 1067 | +84 | 82% |
| Price paid | 0.90-1.01 | 42 | +21 | 95% |
| Model vs market gap | 0.05-0.10 | 15 | -15 | 80% |
| Model vs market gap | 0.10-0.20 | 1110 | +146 | 82% |
| Model vs market gap | 0.20-0.35 | 126 | -29 | 72% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 631 | +2 | 80% |
| Side | yes | 621 | +105 | 82% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 2 | +2 | 100% |
| Quarter | 2025-Q3 | 5 | +5 | 100% |
| Quarter | 2025-Q4 | 1 | -10 | 0% |
| Quarter | 2026-Q2 | 12 | +24 | 75% |
| Quarter | 2026-Q3 | 17 | +29 | 76% |
| Quarter | 2026-Q4 | 11 | +10 | 82% |
| Price paid | 0.50-0.70 | 34 | +37 | 71% |
| Price paid | 0.70-0.90 | 7 | +15 | 100% |
| Price paid | 0.90-1.01 | 7 | +7 | 100% |
| Model vs market gap | 0.05-0.10 | 26 | +57 | 92% |
| Model vs market gap | 0.10-0.20 | 22 | +2 | 64% |
| Side | no | 2 | -9 | 50% |
| Side | yes | 46 | +69 | 80% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 76 | -4 | 80% |
| Quarter | 2025-Q4 | 81 | -86 | 73% |
| Quarter | 2026-Q2 | 26 | -16 | 62% |
| Quarter | 2026-Q3 | 46 | +64 | 94% |
| Quarter | 2026-Q4 | 41 | +7 | 83% |
| Price paid | 0.30-0.50 | 3 | -5 | 33% |
| Price paid | 0.50-0.70 | 29 | -27 | 59% |
| Price paid | 0.70-0.90 | 224 | -5 | 81% |
| Price paid | 0.90-1.01 | 14 | +3 | 93% |
| Model vs market gap | 0.05-0.10 | 6 | +7 | 100% |
| Model vs market gap | 0.10-0.20 | 216 | -5 | 82% |
| Model vs market gap | 0.20-0.35 | 22 | -19 | 68% |
| Model vs market gap | no model | 26 | -16 | 62% |
| Side | no | 117 | +70 | 87% |
| Side | yes | 153 | -104 | 72% |
