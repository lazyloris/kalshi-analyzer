# Backtest (2026-11-26)

Flat $10 per trade at the ask plus Kalshi fees, held to settlement. Prices are real hourly Kalshi quotes. Forecasts are archived NWS-blend (NBM) runs 1-2 days old. Bias/sigma learned only from earlier days.

## Live paper books vs backtest

| Book | Settled | Open | Live P&L | Live return/$ | Backtest rule | Backtest return/$ |
|---|---|---|---|---|---|---|
| bitcoin | 34 | 4 | +22.31 | +6.7% | c_vol50 | +0.4% |
| bitcoin_tod | 34 | 4 | +19.41 | +5.8% | s_combo_tod | +2.8% |
| ethereum | 34 | 4 | +4.56 | +1.4% | a_vol50 | -1.4% |
| ethereum_tod | 34 | 4 | -5.58 | -1.7% | s_combo_tod | +2.1% |
| weather_high | 170 | 17 | -27.57 | -1.7% | fade | +0.1% |
| weather_low | 93 | 10 | -14.55 | -1.6% | fade | +0.3% |

Live numbers need ~100 settled trades before they mean much.

## Weather: daily highs

3828 events, 2025-03-21 to 2026-11-25.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Kalshi price-spike fade (no model) (+181 on 496 trades).

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 496 | 45% | +181.44 | +3.6% | 0.57 | 0.36 | -149 | +330 | – | – | 0.1962 |
| Long-shot fade (no model) | 5053 | 95% | +44.01 | +0.1% | 0.29 | 0.35 | +51 | -7 | – | – | 0.0433 |
| Bayes: market prior + forecast | 2 | 50% | -4.85 | -24.4% | -0.29 | -0.29 | -10 | +5 | 74% | 0.3459 | 0.3305 |
| Bayes price-level, 99% sure | 1280 | 91% | -176.90 | -1.4% | -1.65 | -1.7 | -12 | -165 | 94% | 0.0787 | 0.0773 |
| Combined: rolling best (past 6 months) | 2941 | 94% | -199.81 | -0.7% | -1.23 | -1.43 | +77 | -277 | – | – | 0.0494 |
| Heavy-volume move (10c, 5x): fade | 318 | 48% | -236.10 | -7.3% | -0.99 | -0.75 | -161 | -75 | – | – | 0.1841 |
| Market favorite YES (no model) | 4721 | 51% | -243.12 | -0.5% | -0.36 | -0.36 | -285 | +42 | – | – | 0.243 |
| Bayes price-level, 95% sure | 2229 | 88% | -348.29 | -1.6% | -2.03 | -1.91 | -193 | -156 | 91% | 0.0958 | 0.0943 |
| Heavy-volume move (10c, 5x): follow | 300 | 49% | -384.84 | -12.7% | -2.03 | -1.89 | -283 | -102 | – | – | 0.1949 |
| Long-shot fade, limit order | 2888 | 92% | -482.80 | -1.8% | -3.3 | -3.31 | -200 | -283 | – | – | 0.073 |
| Heavy-volume move: fade | 1566 | 48% | -1057.25 | -6.7% | -2.01 | -2.52 | -1056 | -1 | – | – | 0.188 |
| Combined: 5+ strategies agree | 5117 | 49% | -1164.84 | -2.2% | -1.48 | -1.04 | -415 | -750 | 60% | 0.2205 | 0.236 |
| Heavy-volume move: follow | 1532 | 49% | -1685.94 | -10.9% | -3.78 | -3.52 | -781 | -905 | – | – | 0.1922 |
| Favorite, stop loss 25c | 4721 | 42% | -2491.05 | -5.2% | -3.93 | -3.93 | -2240 | -251 | – | – | 0.2419 |
| Favorite, take profit 10c | 4721 | 70% | -3694.35 | -7.7% | -8.43 | -8.43 | -2377 | -1318 | – | – | 0.2609 |
| Forecast bracket YES | 803 | 10% | -3880.76 | -45.9% | -6.97 | -6.97 | -1902 | -1979 | 33% | 0.1453 | 0.0889 |
| Favorite, stop loss 10c | 4721 | 28% | -4337.90 | -9.1% | -8.9 | -8.9 | -3071 | -1267 | – | – | 0.2375 |
| Favorite, take profit 15c / stop 15c | 4721 | 47% | -5536.51 | -11.6% | -15.28 | -15.28 | -3864 | -1672 | – | – | 0.2514 |
| Market favorite, limit order | 3847 | 39% | -6591.11 | -17.3% | -10.14 | -10.14 | -4329 | -2262 | – | – | 0.2368 |
| v2 + disagreement cap | 3405 | 33% | -8707.48 | -25.0% | -7.98 | -7.05 | -4401 | -4307 | 54% | 0.2014 | 0.1577 |
| v1 (what we ran live) | 4712 | 34% | -9269.48 | -19.2% | -7.33 | -6.69 | -4626 | -4644 | 63% | 0.2631 | 0.1668 |
| v2 + 50% market blend | 3822 | 31% | -9582.51 | -24.4% | -8.41 | -7.24 | -4942 | -4641 | 46% | 0.1911 | 0.1661 |
| v2 calibrated | 4301 | 32% | -10351.70 | -23.5% | -8.7 | -7.64 | -5414 | -4938 | 58% | 0.2453 | 0.1687 |
| Combined: 3+ strategies agree | 9845 | 46% | -10783.51 | -10.8% | -7.82 | -5.8 | -3996 | -6788 | 62% | 0.2717 | 0.1938 |

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
| 0.6 | 4288 | -9823.14 | -22.4% |
| 0.8 | 4146 | -10155.26 | -23.9% |
| 1.0 | 4301 | -10351.70 | -23.5% |
| 1.25 | 4560 | -9108.55 | -19.5% |
| 1.5 | 4718 | -8101.91 | -16.8% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 5234 | -11894.55 | -22.2% |
| blend 0.0, edge 0.05 | 4905 | -11220.63 | -22.3% |
| blend 0.0, edge 0.08 | 4301 | -10351.70 | -23.5% |
| blend 0.25, edge 0.03 | 4956 | -11636.24 | -22.9% |
| blend 0.25, edge 0.05 | 4446 | -10660.10 | -23.4% |
| blend 0.25, edge 0.08 | 3507 | -9217.47 | -25.6% |
| blend 0.5, edge 0.03 | 4278 | -10465.51 | -23.8% |
| blend 0.5, edge 0.05 | 3332 | -8721.35 | -25.5% |
| blend 0.5, edge 0.08 | 2042 | -4798.47 | -22.9% |
| blend 0.75, edge 0.03 | 2031 | -5478.16 | -26.1% |
| blend 0.75, edge 0.05 | 892 | -2008.36 | -21.8% |
| blend 0.75, edge 0.08 | 239 | -583.92 | -23.5% |

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
| Quarter | 2026-Q4 | 986 | -2402 | 32% |
| Price paid | 0.00-0.10 | 860 | -3198 | 4% |
| Price paid | 0.10-0.30 | 902 | -4176 | 10% |
| Price paid | 0.30-0.50 | 935 | -1311 | 37% |
| Price paid | 0.50-0.70 | 1269 | -1424 | 53% |
| Price paid | 0.70-0.90 | 334 | -233 | 71% |
| Price paid | 0.90-1.01 | 1 | -10 | 0% |
| Model vs market gap | 0.05-0.10 | 62 | -14 | 16% |
| Model vs market gap | 0.10-0.20 | 2142 | -5989 | 32% |
| Model vs market gap | 0.20-0.35 | 1650 | -3469 | 35% |
| Model vs market gap | 0.35-1.01 | 447 | -880 | 30% |
| Side | no | 2622 | -3228 | 48% |
| Side | yes | 1679 | -7123 | 8% |

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
| Quarter | 2026-Q4 | 46 | -25 | 50% |
| Price paid | 0.10-0.30 | 176 | -34 | 20% |
| Price paid | 0.30-0.50 | 133 | +35 | 42% |
| Price paid | 0.50-0.70 | 145 | +180 | 69% |
| Price paid | 0.70-0.90 | 42 | +0 | 76% |
| Model vs market gap | no model | 496 | +181 | 45% |
| Side | no | 287 | +145 | 58% |
| Side | yes | 209 | +36 | 26% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 37 | -76 | 60% |
| Quarter | 2025-Q3 | 211 | +7 | 95% |
| Quarter | 2025-Q4 | 159 | -19 | 91% |
| Quarter | 2026-Q1 | 484 | -129 | 87% |
| Quarter | 2026-Q2 | 530 | -94 | 88% |
| Quarter | 2026-Q3 | 538 | -33 | 89% |
| Quarter | 2026-Q4 | 270 | -4 | 87% |
| Price paid | 0.30-0.50 | 21 | -85 | 29% |
| Price paid | 0.50-0.70 | 37 | +17 | 54% |
| Price paid | 0.70-0.90 | 688 | -174 | 82% |
| Price paid | 0.90-1.01 | 1483 | -106 | 93% |
| Model vs market gap | 0.00-0.05 | 1998 | -178 | 90% |
| Model vs market gap | 0.05-0.10 | 210 | -85 | 77% |
| Model vs market gap | 0.10-0.20 | 21 | -85 | 29% |
| Side | no | 2169 | -261 | 90% |
| Side | yes | 60 | -88 | 43% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 544 | +57 | 96% |
| Quarter | 2025-Q4 | 268 | -37 | 94% |
| Quarter | 2026-Q1 | 968 | +74 | 96% |
| Quarter | 2026-Q2 | 1056 | -99 | 94% |
| Quarter | 2026-Q3 | 59 | -169 | 41% |
| Quarter | 2026-Q4 | 46 | -25 | 50% |
| Price paid | 0.10-0.30 | 28 | -246 | 4% |
| Price paid | 0.30-0.50 | 23 | +86 | 56% |
| Price paid | 0.50-0.70 | 40 | -10 | 60% |
| Price paid | 0.70-0.90 | 14 | -24 | 64% |
| Price paid | 0.90-1.01 | 2836 | -6 | 95% |
| Model vs market gap | no model | 2941 | -200 | 94% |
| Side | no | 2901 | +14 | 95% |
| Side | yes | 40 | -214 | 20% |

Forecast error (actual minus NBM forecast)

| City | Entry | n | Bias | RMSE |
|---|---|---|---|---|
| Austin | day before 10am | 257 | +1.74 | 3.31 |
| Austin | same day 8am | 259 | +1.48 | 2.92 |
| Chicago | day before 10am | 257 | +1.50 | 3.4 |
| Chicago | same day 8am | 255 | +1.30 | 2.84 |
| Denver | day before 10am | 258 | +1.75 | 3.38 |
| Denver | same day 8am | 255 | +1.69 | 2.95 |
| Los Angeles | day before 10am | 256 | +2.27 | 3.8 |
| Los Angeles | same day 8am | 258 | +2.26 | 3.54 |
| Miami | same day 8am | 258 | +1.97 | 2.62 |
| New York | same day 8am | 255 | -0.15 | 2.46 |
| Philadelphia | same day 8am | 254 | +1.74 | 2.88 |

## Weather: daily lows

2312 events, 2025-12-13 to 2026-11-25.

**Verdict:** Long-shot fade (no model): +100 on 3274 trades (+0.3% per $ staked, t=0.9), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 153 | 54% | +265.40 | +17.1% | 1.4 | 1.27 | -53 | +318 | – | – | 0.2107 |
| Combined: rolling best (past 6 months) | 1646 | 78% | +241.53 | +1.5% | 0.83 | 0.9 | +166 | +76 | – | – | 0.123 |
| Long-shot fade (no model) | 3274 | 96% | +99.95 | +0.3% | 0.9 | 0.98 | +87 | +13 | – | – | 0.0367 |
| Heavy-volume move: follow | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Heavy-volume move: fade | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Heavy-volume move (10c, 5x): follow | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Heavy-volume move (10c, 5x): fade | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Bayes: market prior + forecast | 1 | 0% | -10.25 | -100.0% | – | – | +0 | -10 | 49% | 0.2401 | 0.16 |
| Bayes price-level, 99% sure | 213 | 94% | -18.49 | -0.9% | -0.55 | -0.46 | -11 | -7 | 96% | 0.0538 | 0.0538 |
| Bayes price-level, 95% sure | 382 | 94% | -19.21 | -0.5% | -0.37 | -0.31 | -48 | +29 | 96% | 0.0573 | 0.0572 |
| Long-shot fade, limit order | 1728 | 93% | -211.10 | -1.3% | -1.94 | -1.59 | -56 | -155 | – | – | 0.0667 |
| Combined: 5+ strategies agree | 2273 | 46% | -462.03 | -2.0% | -0.87 | -0.98 | +495 | -957 | 54% | 0.2369 | 0.2381 |
| Market favorite YES (no model) | 2206 | 47% | -672.01 | -3.0% | -1.34 | -1.34 | +370 | -1042 | – | – | 0.2401 |
| Forecast bracket YES | 579 | 15% | -1722.47 | -28.4% | -3.56 | -3.56 | -997 | -725 | 35% | 0.1624 | 0.1225 |
| Favorite, take profit 10c | 2206 | 62% | -2855.88 | -12.8% | -8.28 | -8.28 | -1149 | -1706 | – | – | 0.2666 |
| Market favorite, limit order | 1836 | 36% | -3100.03 | -17.0% | -6.36 | -6.36 | -914 | -2186 | – | – | 0.2271 |
| v2 + 50% market blend | 1987 | 30% | -4069.99 | -19.9% | -4.36 | -4.11 | -1218 | -2852 | 41% | 0.1576 | 0.1428 |
| Favorite, stop loss 25c | 2206 | 28% | -5550.58 | -24.8% | -13.24 | -13.24 | -2292 | -3259 | – | – | 0.2287 |
| v2 calibrated | 2736 | 32% | -5912.77 | -21.0% | -5.79 | -5.36 | -1865 | -4048 | 53% | 0.1994 | 0.1494 |
| Favorite, stop loss 10c | 2206 | 14% | -5998.26 | -26.8% | -21.2 | -21.2 | -2984 | -3015 | – | – | 0.2163 |
| v2 + disagreement cap | 2371 | 32% | -6241.19 | -25.6% | -6.9 | -7.05 | -2249 | -3992 | 50% | 0.1761 | 0.1427 |
| Combined: 3+ strategies agree | 4710 | 41% | -6422.28 | -13.4% | -6.1 | -5.3 | -2110 | -4312 | 57% | 0.2326 | 0.1856 |
| Favorite, take profit 15c / stop 15c | 2206 | 28% | -6704.40 | -29.9% | -28.25 | -28.25 | -3421 | -3284 | – | – | 0.2349 |
| v1 (what we ran live) | 4003 | 32% | -11103.04 | -27.0% | -9.91 | -8.94 | -4558 | -6545 | 58% | 0.2264 | 0.148 |

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
| 0.6 | 3503 | -5568.76 | -15.6% |
| 0.8 | 2799 | -5167.18 | -18.0% |
| 1.0 | 2736 | -5912.77 | -21.0% |
| 1.25 | 3187 | -7401.53 | -22.6% |
| 1.5 | 3732 | -9193.37 | -24.1% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 4195 | -9709.73 | -22.5% |
| blend 0.0, edge 0.05 | 3603 | -8619.68 | -23.3% |
| blend 0.0, edge 0.08 | 2736 | -5912.77 | -21.0% |
| blend 0.25, edge 0.03 | 3599 | -8565.61 | -23.2% |
| blend 0.25, edge 0.05 | 2822 | -6041.38 | -20.8% |
| blend 0.25, edge 0.08 | 1838 | -3811.55 | -20.1% |
| blend 0.5, edge 0.03 | 2469 | -5301.11 | -20.8% |
| blend 0.5, edge 0.05 | 1601 | -3320.36 | -20.1% |
| blend 0.5, edge 0.08 | 774 | -674.67 | -8.4% |
| blend 0.75, edge 0.03 | 662 | -866.59 | -12.6% |
| blend 0.75, edge 0.05 | 264 | -656.74 | -23.9% |
| blend 0.75, edge 0.08 | 58 | -405.86 | -67.1% |

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
| Quarter | 2026-Q4 | 521 | -786 | 32% |
| Price paid | 0.00-0.10 | 586 | -2312 | 5% |
| Price paid | 0.10-0.30 | 836 | -2505 | 12% |
| Price paid | 0.30-0.50 | 326 | -624 | 35% |
| Price paid | 0.50-0.70 | 678 | -354 | 58% |
| Price paid | 0.70-0.90 | 309 | -119 | 74% |
| Price paid | 0.90-1.01 | 1 | +1 | 100% |
| Model vs market gap | 0.05-0.10 | 37 | +39 | 22% |
| Model vs market gap | 0.10-0.20 | 1699 | -4690 | 31% |
| Model vs market gap | 0.20-0.35 | 827 | -619 | 35% |
| Model vs market gap | 0.35-1.01 | 173 | -643 | 24% |
| Side | no | 1296 | -1009 | 56% |
| Side | yes | 1440 | -4904 | 10% |

Why: Long-shot fade (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q1 | 950 | -40 | 95% |
| Quarter | 2026-Q2 | 1044 | +162 | 97% |
| Quarter | 2026-Q3 | 976 | -12 | 96% |
| Quarter | 2026-Q4 | 304 | -11 | 96% |
| Price paid | 0.90-1.01 | 3274 | +100 | 96% |
| Model vs market gap | no model | 3274 | +100 | 96% |
| Side | no | 3274 | +100 | 96% |

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
| Quarter | 2026-Q4 | 89 | -26 | 90% |
| Price paid | 0.50-0.70 | 2 | -5 | 50% |
| Price paid | 0.70-0.90 | 15 | +14 | 80% |
| Price paid | 0.90-1.01 | 365 | -28 | 94% |
| Model vs market gap | 0.00-0.05 | 304 | +3 | 95% |
| Model vs market gap | 0.05-0.10 | 61 | -31 | 90% |
| Model vs market gap | 0.10-0.20 | 17 | +9 | 76% |
| Side | no | 365 | -28 | 94% |
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
| Austin | day before 10am | 257 | -2.72 | 4.18 |
| Austin | day before 8pm | 259 | -2.73 | 3.97 |
| Chicago | day before 10am | 257 | -1.57 | 2.98 |
| Chicago | day before 8pm | 259 | -1.38 | 2.63 |
| Denver | day before 10am | 258 | -4.05 | 5.33 |
| Denver | day before 8pm | 259 | -3.88 | 5.13 |
| Los Angeles | day before 10am | 257 | +0.38 | 1.7 |
| Los Angeles | day before 8pm | 259 | +0.49 | 1.6 |
| Miami | day before 8pm | 257 | -0.97 | 2.36 |
| New York | day before 8pm | 259 | -1.49 | 2.7 |
| Philadelphia | day before 8pm | 259 | +0.44 | 2.2 |

## Crypto: Bitcoin 5pm price

613 events, 2025-03-22 to 2026-11-25.

**Verdict:** Vol x0.5, weekends only: +194 on 246 trades (+8.1% per $ staked, t=2.71), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Time-of-day vol x0.5 | 1584 | 80% | +282.59 | +1.8% | 1.39 | 1.61 | -126 | +409 | 92% | 0.1741 | 0.1599 |
| Time-of-day vol x0.5, skip spikes | 982 | 81% | +263.54 | +2.8% | 1.71 | 1.57 | -137 | +401 | 92% | 0.1636 | 0.1537 |
| Vol x0.5, weekends only | 246 | 85% | +193.94 | +8.1% | 2.71 | 2.55 | +34 | +160 | 91% | 0.1179 | 0.1257 |
| Time-of-day vol x0.5, against trend + skip spikes | 517 | 82% | +159.99 | +3.2% | 1.45 | 1.44 | -112 | +272 | 92% | 0.1583 | 0.1491 |
| Regime-scaled vol x0.5 | 1982 | 78% | +155.75 | +0.8% | 0.68 | 0.71 | -243 | +399 | 93% | 0.19 | 0.1678 |
| Combined: rolling best (past 6 months) | 368 | 82% | +142.84 | +4.0% | 1.51 | 0.61 | -9 | +152 | 92% | 0.1626 | 0.1509 |
| Vol x0.5, skip spiked markets | 1112 | 79% | +136.42 | +1.3% | 0.79 | 0.91 | -157 | +293 | 93% | 0.1826 | 0.1631 |
| Bayes price-level, 95% sure | 689 | 92% | +132.81 | +2.0% | 1.69 | 0.94 | +14 | +119 | 93% | 0.0756 | 0.0765 |
| Vol x0.5, against the 24h trend | 840 | 79% | +87.03 | +1.1% | 0.56 | 0.84 | -202 | +289 | 93% | 0.1855 | 0.1651 |
| Long-shot fade (no model) | 1332 | 96% | +83.21 | +0.7% | 1.23 | 1.17 | -41 | +124 | – | – | 0.0342 |
| Vol x0.5, calm market only | 1048 | 79% | +82.02 | +0.8% | 0.5 | 0.67 | -114 | +196 | 92% | 0.1782 | 0.1609 |
| Bayes price-level, 99% sure | 350 | 92% | +74.17 | +2.2% | 1.31 | 1.22 | +43 | +32 | 93% | 0.077 | 0.0783 |
| Vol x0.5, against trend + skip spikes | 587 | 80% | +67.24 | +1.2% | 0.53 | 0.62 | -80 | +147 | 93% | 0.1791 | 0.1598 |
| Vol x0.5 | 1814 | 78% | +61.95 | +0.4% | 0.28 | 0.4 | -301 | +363 | 93% | 0.1911 | 0.1679 |
| Vol x0.5, skip news in window | 1790 | 78% | +42.55 | +0.2% | 0.19 | 0.32 | -318 | +360 | 93% | 0.1916 | 0.1681 |
| Vol x0.5, skip news days | 1709 | 78% | +31.17 | +0.2% | 0.14 | 0.27 | -292 | +323 | 93% | 0.1913 | 0.1676 |
| Vol x0.5, news days only | 105 | 78% | +30.78 | +3.0% | 0.58 | 0.56 | -1 | +32 | 93% | 0.1865 | 0.1727 |
| Bayes: market prior + full vol | 3 | 67% | -6.07 | -20.9% | -0.53 | -0.69 | +2 | -8 | 92% | 0.2927 | 0.2732 |
| Vol x0.5, busy market only | 766 | 76% | -20.07 | -0.3% | -0.14 | -0.14 | -198 | +178 | 93% | 0.2086 | 0.1775 |
| Vol x0.5, with the 24h trend | 974 | 77% | -25.08 | -0.3% | -0.13 | -0.55 | -101 | +76 | 93% | 0.1959 | 0.1703 |
| Fat-tail, moves x0.5 | 1905 | 73% | -52.77 | -0.3% | -0.2 | -0.3 | -182 | +129 | 89% | 0.2238 | 0.196 |
| Bayes: market prior + fat-tail | 17 | 53% | -54.40 | -32.5% | -2.02 | -1.46 | -16 | -38 | 85% | 0.3506 | 0.2928 |
| Vol x0.5, weekdays only | 1568 | 77% | -131.99 | -0.9% | -0.62 | -0.61 | -320 | +188 | 93% | 0.2025 | 0.1745 |
| Fat-tail, moves x0.75 | 1216 | 72% | -161.90 | -1.4% | -0.72 | -0.68 | -193 | +31 | 86% | 0.2088 | 0.191 |
| Vol x0.5, stop loss 25c | 1814 | 65% | -431.00 | -2.4% | -2.31 | -2.47 | -735 | +304 | 93% | 0.305 | 0.2339 |
| Vol x0.75 | 829 | 72% | -492.90 | -6.1% | -2.19 | -2.53 | -342 | -151 | 86% | 0.1727 | 0.1546 |
| Heavy-volume move: follow | 1260 | 62% | -676.83 | -5.4% | -2.08 | -1.35 | -595 | -82 | – | – | 0.1838 |
| Vol x0.5, take profit 10c | 1814 | 81% | -748.12 | -4.2% | -3.81 | -3.4 | -691 | -57 | 93% | 0.1668 | 0.1555 |
| Fat-tail (actual past moves) | 674 | 59% | -825.13 | -12.3% | -2.89 | -2.62 | -582 | -243 | 74% | 0.1996 | 0.1788 |
| Heavy-volume move (10c, 5x): follow | 748 | 60% | -865.53 | -11.6% | -3.91 | -2.92 | -494 | -372 | – | – | 0.1826 |
| Vol x0.5, stop loss 10c | 1814 | 47% | -1025.06 | -5.8% | -6.69 | -6.7 | -1067 | +42 | 93% | 0.4581 | 0.3241 |
| Combined: 5+ strategies agree | 2311 | 71% | -1053.81 | -4.6% | -2.47 | -3.38 | -1023 | -30 | 84% | 0.1776 | 0.1576 |
| Vol x0.5, take profit 15c / stop 15c | 1814 | 57% | -1111.39 | -6.3% | -7.44 | -7.57 | -1097 | -15 | 93% | 0.3711 | 0.2747 |
| v1 + 50% market blend | 306 | 33% | -1151.02 | -36.7% | -4.18 | -3.95 | -619 | -532 | 44% | 0.1194 | 0.1066 |
| Options vol x0.85, 5c gap | 841 | 56% | -1209.35 | -14.3% | -3.01 | -2.73 | -753 | -456 | 66% | 0.1249 | 0.1131 |
| Heavy-volume move (10c, 5x): fade | 794 | 37% | -1320.34 | -16.2% | -3.27 | -3.22 | -595 | -726 | – | – | 0.1734 |
| v1 (what we ran live) | 476 | 40% | -1384.17 | -28.5% | -3.91 | -3.5 | -1097 | -287 | 56% | 0.131 | 0.1029 |
| Options vol, 8c gap | 426 | 24% | -1445.55 | -32.7% | -3.49 | -2.76 | -1088 | -358 | 41% | 0.116 | 0.0876 |
| Options vol, NO only | 609 | 32% | -1749.72 | -28.0% | -3.75 | -3.32 | -1244 | -506 | 46% | 0.1255 | 0.1045 |
| Vol x0.5, limit order | 974 | 60% | -1830.03 | -19.4% | -9.08 | -9.44 | -1135 | -695 | 93% | 0.3472 | 0.2563 |
| Vol x0.5, limit order (strict fill) | 937 | 58% | -1950.07 | -21.5% | -9.8 | -9.95 | -1174 | -777 | 92% | 0.3607 | 0.264 |
| Vol x0.5 5c edge, limit order | 1064 | 59% | -2076.12 | -20.2% | -9.82 | -10.15 | -1273 | -803 | 92% | 0.3393 | 0.2528 |
| Options vol, 5c gap | 699 | 32% | -2156.02 | -30.0% | -4.57 | -4.46 | -1384 | -772 | 45% | 0.116 | 0.0952 |
| Heavy-volume move: fade | 1313 | 36% | -2274.23 | -16.9% | -4.26 | -4.44 | -900 | -1374 | – | – | 0.1766 |
| Combined: 3+ strategies agree | 3387 | 65% | -2778.55 | -8.3% | -4.88 | -5.24 | -2040 | -739 | 83% | 0.1747 | 0.156 |
| Kalshi price-spike fade (no model) | 1272 | 30% | -3240.82 | -24.7% | -6.02 | -5.63 | -1659 | -1582 | – | – | 0.1516 |

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
| 0.4 | 2012 | +31.90 | +0.2% |
| 0.5 | 1814 | +61.95 | +0.4% |
| 0.6 | 1444 | -235.18 | -1.7% |
| 0.75 | 829 | -492.90 | -6.1% |
| 1.0 | 476 | -1384.17 | -28.5% |
| 1.25 | 559 | -2440.07 | -41.8% |

Sweep: options vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 1634 | -214.64 | -1.4% |
| 0.7 | 1321 | -725.31 | -5.6% |
| 0.8 | 978 | -885.33 | -9.1% |
| 0.9 | 769 | -1611.84 | -20.7% |
| 1.0 | 699 | -2156.02 | -30.0% |
| 1.1 | 769 | -2949.62 | -36.9% |

Sweep: time-of-day vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 2003 | +69.83 | +0.4% |
| 0.5 | 1584 | +282.59 | +1.8% |
| 0.6 | 1070 | +282.90 | +2.7% |
| 0.75 | 456 | -17.48 | -0.4% |
| 1.0 | 338 | -1070.22 | -30.8% |

Sweep: fat-tail

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 2103 | -49.10 | -0.2% |
| 0.5 | 1905 | -52.77 | -0.3% |
| 0.6 | 1662 | -9.74 | -0.1% |
| 0.75 | 1216 | -161.90 | -1.4% |
| 0.9 | 831 | -624.74 | -7.6% |
| 1.0 | 674 | -825.13 | -12.3% |

Rolling best: which strategy it picked each quarter

| Quarter | Picked | Past t |
|---|---|---|
| 2025-Q1 | sat out | – |
| 2025-Q2 | sat out | – |
| 2025-Q3 | Vol x0.5, with the 24h trend | 0.44 |
| 2025-Q4 | sat out | – |
| 2026-Q1 | Vol x0.5, weekends only | 0.02 |
| 2026-Q2 | Vol x0.5, weekends only | 2.23 |
| 2026-Q3 | Time-of-day vol x0.5, against trend + skip spikes | 4.06 |
| 2026-Q4 | Time-of-day vol x0.5, against trend + skip spikes | 3.88 |

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
| 2026-Q4 | 110 | 1.414 |

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
| Quarter | 2026-Q4 | 75 | +91 | 51% |
| Price paid | 0.00-0.10 | 65 | -414 | 3% |
| Price paid | 0.10-0.30 | 196 | -996 | 8% |
| Price paid | 0.30-0.50 | 3 | -9 | 33% |
| Price paid | 0.50-0.70 | 15 | +4 | 67% |
| Price paid | 0.70-0.90 | 196 | +29 | 82% |
| Price paid | 0.90-1.01 | 1 | +1 | 100% |
| Model vs market gap | 0.05-0.10 | 22 | +190 | 59% |
| Model vs market gap | 0.10-0.20 | 415 | -1293 | 40% |
| Model vs market gap | 0.20-0.35 | 39 | -282 | 23% |
| Side | no | 312 | -813 | 41% |
| Side | yes | 164 | -571 | 38% |

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
| Quarter | 2026-Q4 | 169 | +68 | 79% |
| Price paid | 0.00-0.10 | 2 | -21 | 0% |
| Price paid | 0.10-0.30 | 3 | -32 | 0% |
| Price paid | 0.30-0.50 | 2 | +1 | 50% |
| Price paid | 0.50-0.70 | 223 | +151 | 72% |
| Price paid | 0.70-0.90 | 1575 | -35 | 79% |
| Price paid | 0.90-1.01 | 9 | -2 | 89% |
| Model vs market gap | 0.05-0.10 | 15 | -12 | 80% |
| Model vs market gap | 0.10-0.20 | 1244 | +4 | 80% |
| Model vs market gap | 0.20-0.35 | 554 | +65 | 74% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 1024 | +54 | 78% |
| Side | yes | 790 | +7 | 78% |

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
| Quarter | 2026-Q4 | 128 | -235 | 33% |
| Price paid | 0.10-0.30 | 709 | -3043 | 12% |
| Price paid | 0.30-0.50 | 297 | -454 | 34% |
| Price paid | 0.50-0.70 | 187 | +134 | 65% |
| Price paid | 0.70-0.90 | 79 | +122 | 89% |
| Model vs market gap | no model | 1272 | -3241 | 30% |
| Side | no | 613 | -1300 | 43% |
| Side | yes | 659 | -1940 | 18% |

Why: Time-of-day vol x0.5, against trend + skip spikes

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 4 | +11 | 100% |
| Quarter | 2025-Q2 | 39 | -9 | 77% |
| Quarter | 2025-Q3 | 67 | -6 | 79% |
| Quarter | 2025-Q4 | 87 | -112 | 69% |
| Quarter | 2026-Q1 | 87 | +58 | 85% |
| Quarter | 2026-Q2 | 104 | +156 | 91% |
| Quarter | 2026-Q3 | 77 | +58 | 86% |
| Quarter | 2026-Q4 | 52 | +3 | 79% |
| Price paid | 0.10-0.30 | 1 | -11 | 0% |
| Price paid | 0.50-0.70 | 41 | +29 | 73% |
| Price paid | 0.70-0.90 | 470 | +159 | 83% |
| Price paid | 0.90-1.01 | 5 | -17 | 60% |
| Model vs market gap | 0.05-0.10 | 12 | -4 | 83% |
| Model vs market gap | 0.10-0.20 | 430 | +150 | 83% |
| Model vs market gap | 0.20-0.35 | 75 | +14 | 76% |
| Side | no | 290 | +135 | 83% |
| Side | yes | 227 | +25 | 80% |

Why: Time-of-day vol x0.5

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 6 | +16 | 100% |
| Quarter | 2025-Q2 | 118 | -2 | 78% |
| Quarter | 2025-Q3 | 185 | -15 | 80% |
| Quarter | 2025-Q4 | 248 | -157 | 74% |
| Quarter | 2026-Q1 | 277 | +78 | 80% |
| Quarter | 2026-Q2 | 298 | +191 | 84% |
| Quarter | 2026-Q3 | 258 | +127 | 83% |
| Quarter | 2026-Q4 | 194 | +46 | 79% |
| Price paid | 0.10-0.30 | 2 | -21 | 0% |
| Price paid | 0.30-0.50 | 2 | +1 | 50% |
| Price paid | 0.50-0.70 | 142 | +118 | 73% |
| Price paid | 0.70-0.90 | 1430 | +199 | 81% |
| Price paid | 0.90-1.01 | 8 | -14 | 75% |
| Model vs market gap | 0.05-0.10 | 22 | -1 | 86% |
| Model vs market gap | 0.10-0.20 | 1268 | +209 | 81% |
| Model vs market gap | 0.20-0.35 | 293 | +71 | 75% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 913 | +257 | 80% |
| Side | yes | 671 | +25 | 79% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 93 | -18 | 91% |
| Quarter | 2025-Q3 | 21 | -41 | 71% |
| Quarter | 2025-Q4 | 4 | +2 | 75% |
| Quarter | 2026-Q1 | 7 | +10 | 100% |
| Quarter | 2026-Q2 | 140 | +32 | 91% |
| Quarter | 2026-Q3 | 238 | +115 | 94% |
| Quarter | 2026-Q4 | 186 | +32 | 91% |
| Price paid | 0.50-0.70 | 3 | +21 | 100% |
| Price paid | 0.70-0.90 | 191 | +106 | 89% |
| Price paid | 0.90-1.01 | 495 | +6 | 93% |
| Model vs market gap | 0.00-0.05 | 452 | +84 | 93% |
| Model vs market gap | 0.05-0.10 | 219 | +33 | 89% |
| Model vs market gap | 0.10-0.20 | 18 | +16 | 94% |
| Side | no | 288 | +87 | 94% |
| Side | yes | 401 | +46 | 90% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 139 | -79 | 74% |
| Quarter | 2026-Q1 | 52 | +90 | 90% |
| Quarter | 2026-Q2 | 48 | +70 | 90% |
| Quarter | 2026-Q3 | 77 | +58 | 86% |
| Quarter | 2026-Q4 | 52 | +3 | 79% |
| Price paid | 0.30-0.50 | 1 | -10 | 0% |
| Price paid | 0.50-0.70 | 48 | +64 | 77% |
| Price paid | 0.70-0.90 | 317 | +98 | 83% |
| Price paid | 0.90-1.01 | 2 | -9 | 50% |
| Model vs market gap | 0.05-0.10 | 12 | -3 | 83% |
| Model vs market gap | 0.10-0.20 | 274 | +161 | 84% |
| Model vs market gap | 0.20-0.35 | 81 | -20 | 72% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 209 | +172 | 84% |
| Side | yes | 159 | -29 | 78% |

## Weather: daily highs: late entries

2724 events, 2025-03-21 to 2026-11-25.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Late long-shot fade 1-4c (+30 on 982 trades).

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Late long-shot fade 1-4c | 982 | 99% | +29.87 | +0.3% | 0.96 | 1.44 | -5 | +35 | – | – | 0.0102 |
| Combined: 3+ strategies agree | 689 | 81% | +13.94 | +0.2% | 0.1 | 0.16 | +39 | -25 | 92% | 0.1687 | 0.15 |
| Bayes price-level, 99% sure | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Late long-shot fade | 748 | 96% | -9.74 | -0.1% | -0.16 | -0.33 | -34 | +25 | – | – | 0.0434 |
| Late favorite 90-97c | 837 | 94% | -25.30 | -0.3% | -0.36 | -0.36 | +0 | -25 | – | – | 0.0521 |
| Bayes price-level, 95% sure | 67 | 82% | -53.09 | -8.1% | -1.52 | -1.04 | -8 | -45 | 93% | 0.1559 | 0.1446 |
| Combined: rolling best (past 6 months) | 561 | 97% | -58.38 | -1.1% | -1.4 | -1.26 | -65 | +7 | – | – | 0.0306 |
| Late favorite 80-90c | 443 | 85% | -63.37 | -1.5% | -0.75 | -0.75 | +3 | -66 | – | – | 0.125 |
| Combined: 5+ strategies agree | 443 | 85% | -63.37 | -1.5% | -0.75 | -0.75 | +3 | -66 | – | – | 0.125 |
| Late fav 80-90c, stop loss 25c | 443 | 82% | -93.15 | -2.2% | -1.16 | -1.16 | -24 | -69 | – | – | 0.1482 |
| Late fav 80-90c, stop loss 10c | 443 | 78% | -104.42 | -2.4% | -1.35 | -1.35 | -25 | -80 | – | – | 0.1747 |
| Late fav 80-90c, take profit 15c / stop 15c | 443 | 80% | -123.76 | -2.9% | -1.58 | -1.58 | -44 | -80 | – | – | 0.1607 |
| Late fav 80-90c, take profit 10c | 443 | 86% | -135.41 | -3.1% | -1.65 | -1.65 | -27 | -108 | – | – | 0.1238 |
| Late favorite 50-80c | 552 | 67% | -168.95 | -3.1% | -1.04 | -1.04 | -98 | -71 | – | – | 0.2133 |
| Heavy-volume move (10c, 5x): follow | 855 | 72% | -476.96 | -5.7% | -2.42 | -2.15 | -349 | -127 | – | – | 0.1651 |
| Heavy-volume move: follow | 1328 | 69% | -535.07 | -4.1% | -1.73 | -1.05 | -492 | -43 | – | – | 0.1696 |
| Heavy-volume move (10c, 5x): fade | 1019 | 25% | -2289.65 | -21.7% | -4.15 | -4.03 | -852 | -1437 | – | – | 0.1486 |
| Heavy-volume move: fade | 1603 | 26% | -3514.67 | -21.2% | -5.11 | -4.97 | -2250 | -1264 | – | – | 0.1509 |

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
| Quarter | 2026-Q4 | 49 | -16 | 84% |
| Price paid | 0.70-0.90 | 388 | -65 | 84% |
| Price paid | 0.90-1.01 | 55 | +2 | 91% |
| Model vs market gap | no model | 443 | -63 | 85% |
| Side | yes | 443 | -63 | 85% |

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
| Quarter | 2026-Q4 | 88 | -9 | 98% |
| Price paid | 0.90-1.01 | 561 | -58 | 97% |
| Model vs market gap | no model | 561 | -58 | 97% |
| Side | no | 561 | -58 | 97% |

## Weather: daily lows: late entries

1895 events, 2025-12-13 to 2026-11-25.

**Verdict:** Heavy-volume move: fade: +406 on 760 trades (+5.2% per $ staked, t=0.74), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Heavy-volume move: fade | 760 | 35% | +405.62 | +5.2% | 0.74 | 0.67 | +398 | +7 | – | – | 0.1652 |
| Heavy-volume move (10c, 5x): fade | 338 | 31% | +115.68 | +3.3% | 0.31 | -0.31 | +98 | +18 | – | – | 0.1595 |
| Bayes price-level, 99% sure | 10 | 60% | +41.84 | +40.6% | 1.07 | 1.07 | +22 | +20 | 58% | 0.2435 | 0.2878 |
| Combined: rolling best (past 6 months) | 341 | 33% | -25.01 | -0.7% | -0.05 | -0.25 | -368 | +343 | – | – | 0.1606 |
| Bayes price-level, 95% sure | 36 | 42% | -34.27 | -9.4% | -0.51 | -0.49 | -10 | -24 | 61% | 0.3087 | 0.2904 |
| Late favorite 90-97c | 902 | 94% | -74.04 | -0.9% | -1.07 | -1.07 | -41 | -33 | – | – | 0.0537 |
| Late favorite 80-90c | 379 | 83% | -197.03 | -5.3% | -2.37 | -2.37 | -115 | -82 | – | – | 0.1435 |
| Combined: 5+ strategies agree | 379 | 83% | -197.03 | -5.3% | -2.37 | -2.37 | -115 | -82 | – | – | 0.1435 |
| Late long-shot fade 1-4c | 1951 | 98% | -202.96 | -1.1% | -3.03 | -2.84 | -180 | -23 | – | – | 0.023 |
| Combined: 3+ strategies agree | 434 | 80% | -239.04 | -5.6% | -2.37 | -2.49 | -168 | -71 | 55% | 0.1882 | 0.1576 |
| Late fav 80-90c, take profit 10c | 379 | 83% | -248.18 | -6.7% | -3.06 | -3.06 | -138 | -110 | – | – | 0.1416 |
| Heavy-volume move (10c, 5x): follow | 251 | 64% | -350.67 | -14.1% | -2.73 | -2.2 | -223 | -127 | – | – | 0.1701 |
| Late long-shot fade | 1376 | 93% | -361.80 | -2.7% | -3.87 | -3.62 | -270 | -92 | – | – | 0.0629 |
| Late fav 80-90c, stop loss 25c | 379 | 62% | -406.02 | -11.0% | -5.9 | -5.9 | -258 | -148 | – | – | 0.2819 |
| Late fav 80-90c, take profit 15c / stop 15c | 379 | 48% | -441.28 | -11.9% | -7.79 | -7.79 | -267 | -175 | – | – | 0.3747 |
| Late fav 80-90c, stop loss 10c | 379 | 39% | -443.40 | -12.0% | -8.64 | -8.64 | -266 | -178 | – | – | 0.4382 |
| Late favorite 50-80c | 439 | 58% | -644.06 | -14.8% | -4.15 | -4.15 | -234 | -410 | – | – | 0.2367 |
| Heavy-volume move: follow | 597 | 56% | -1198.77 | -20.2% | -5.49 | -5.54 | -574 | -625 | – | – | 0.1756 |

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
| Quarter | 2026-Q4 | 56 | -0 | 88% |
| Price paid | 0.70-0.90 | 336 | -186 | 82% |
| Price paid | 0.90-1.01 | 43 | -11 | 88% |
| Model vs market gap | no model | 379 | -197 | 83% |
| Side | yes | 379 | -197 | 83% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q2 | 6 | -61 | 0% |
| Quarter | 2026-Q3 | 20 | +18 | 50% |
| Quarter | 2026-Q4 | 10 | +9 | 50% |
| Price paid | 0.30-0.50 | 24 | +37 | 50% |
| Price paid | 0.50-0.70 | 9 | -42 | 33% |
| Price paid | 0.70-0.90 | 3 | -30 | 0% |
| Model vs market gap | 0.05-0.10 | 2 | -20 | 0% |
| Model vs market gap | 0.10-0.20 | 26 | -30 | 42% |
| Model vs market gap | 0.20-0.35 | 8 | +15 | 50% |
| Side | no | 33 | -4 | 46% |
| Side | yes | 3 | -30 | 0% |

Why: Heavy-volume move: fade

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q4 | 6 | +58 | 33% |
| Quarter | 2026-Q1 | 194 | -156 | 34% |
| Quarter | 2026-Q2 | 219 | +529 | 40% |
| Quarter | 2026-Q3 | 224 | -257 | 31% |
| Quarter | 2026-Q4 | 117 | +232 | 38% |
| Price paid | 0.10-0.30 | 477 | +102 | 18% |
| Price paid | 0.30-0.50 | 113 | +255 | 48% |
| Price paid | 0.50-0.70 | 57 | -2 | 61% |
| Price paid | 0.70-0.90 | 109 | +47 | 84% |
| Price paid | 0.90-1.01 | 4 | +4 | 100% |
| Model vs market gap | no model | 760 | +406 | 35% |
| Side | no | 437 | +346 | 42% |
| Side | yes | 323 | +60 | 27% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q3 | 224 | -257 | 31% |
| Quarter | 2026-Q4 | 117 | +232 | 38% |
| Price paid | 0.10-0.30 | 224 | -236 | 16% |
| Price paid | 0.30-0.50 | 51 | +182 | 55% |
| Price paid | 0.50-0.70 | 23 | +30 | 70% |
| Price paid | 0.70-0.90 | 40 | -4 | 80% |
| Price paid | 0.90-1.01 | 3 | +3 | 100% |
| Model vs market gap | no model | 341 | -25 | 33% |
| Side | no | 213 | -90 | 37% |
| Side | yes | 128 | +65 | 27% |

## Bitcoin: last 1-3 hours

613 events, 2025-03-22 to 2026-11-25.

**Verdict:** Late long-shot fade 1-4c: +94 on 919 trades (+1.0% per $ staked, t=6.6), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bayes price-level, 99% sure | 563 | 94% | +175.70 | +3.2% | 2.85 | 2.66 | +120 | +55 | 96% | 0.0535 | 0.0557 |
| Bayes price-level, 95% sure | 964 | 92% | +158.34 | +1.7% | 1.68 | 2.02 | +43 | +115 | 94% | 0.0737 | 0.0742 |
| Late long-shot fade | 776 | 97% | +121.50 | +1.6% | 2.73 | 2.17 | +28 | +93 | – | – | 0.0274 |
| Combined: rolling best (past 6 months) | 769 | 96% | +113.29 | +1.5% | 2.0 | 1.6 | +24 | +90 | 94% | 0.0712 | 0.0337 |
| Late long-shot fade 1-4c | 919 | 100% | +93.85 | +1.0% | 6.6 | 6.17 | +39 | +55 | – | – | 0.0025 |
| Combined: 3+ strategies agree | 265 | 89% | +88.43 | +3.4% | 1.53 | 1.57 | +10 | +79 | 90% | 0.0946 | 0.0904 |
| Late favorite 50-80c | 32 | 69% | +6.44 | +2.0% | 0.17 | 0.17 | -27 | +33 | – | – | 0.2203 |
| Late favorite 90-97c | 204 | 96% | +4.10 | +0.2% | 0.12 | 0.12 | +30 | -26 | – | – | 0.0425 |
| Late favorite 80-90c | 47 | 87% | -0.31 | -0.1% | 0.01 | 0.01 | -1 | +1 | – | – | 0.1141 |
| Combined: 5+ strategies agree | 47 | 87% | -0.31 | -0.1% | 0.01 | 0.01 | -1 | +1 | – | – | 0.1141 |
| Late fav 80-90c, take profit 10c | 47 | 87% | -1.58 | -0.3% | -0.04 | -0.04 | -1 | -0 | – | – | 0.1141 |
| Late fav 80-90c, stop loss 25c | 47 | 74% | -29.82 | -6.5% | -1.1 | -1.1 | -34 | +4 | – | – | 0.2007 |
| Late fav 80-90c, stop loss 10c | 47 | 60% | -47.16 | -10.2% | -1.87 | -1.87 | -49 | +2 | – | – | 0.2943 |
| Late fav 80-90c, take profit 15c / stop 15c | 47 | 64% | -48.94 | -10.6% | -1.84 | -1.84 | -49 | -0 | – | – | 0.2697 |
| Heavy-volume move (10c, 5x): follow | 813 | 66% | -613.38 | -7.6% | -2.87 | -2.11 | -387 | -227 | – | – | 0.1766 |
| Heavy-volume move: follow | 1341 | 66% | -967.55 | -7.3% | -3.43 | -2.9 | -638 | -330 | – | – | 0.1695 |
| Heavy-volume move (10c, 5x): fade | 882 | 31% | -1868.42 | -20.5% | -4.14 | -3.95 | -1221 | -647 | – | – | 0.165 |
| Heavy-volume move: fade | 1424 | 30% | -3612.08 | -24.6% | -6.46 | -5.61 | -2238 | -1374 | – | – | 0.1549 |

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
| Quarter | 2026-Q4 | 178 | +21 | 100% |
| Price paid | 0.90-1.01 | 919 | +94 | 100% |
| Model vs market gap | no model | 919 | +94 | 100% |
| Side | no | 919 | +94 | 100% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 11 | -3 | 91% |
| Quarter | 2025-Q3 | 58 | +11 | 93% |
| Quarter | 2025-Q4 | 76 | -19 | 88% |
| Quarter | 2026-Q1 | 135 | +35 | 95% |
| Quarter | 2026-Q2 | 257 | +10 | 91% |
| Quarter | 2026-Q3 | 250 | +199 | 96% |
| Quarter | 2026-Q4 | 177 | -76 | 86% |
| Price paid | 0.50-0.70 | 2 | -5 | 50% |
| Price paid | 0.70-0.90 | 401 | +106 | 86% |
| Price paid | 0.90-1.01 | 561 | +57 | 96% |
| Model vs market gap | 0.00-0.05 | 436 | +57 | 96% |
| Model vs market gap | 0.05-0.10 | 456 | +91 | 89% |
| Model vs market gap | 0.10-0.20 | 72 | +10 | 83% |
| Side | no | 167 | +30 | 90% |
| Side | yes | 797 | +128 | 92% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 50 | -0 | 96% |
| Quarter | 2025-Q4 | 29 | +3 | 100% |
| Quarter | 2026-Q1 | 127 | +17 | 100% |
| Quarter | 2026-Q2 | 260 | +14 | 99% |
| Quarter | 2026-Q3 | 181 | +141 | 96% |
| Quarter | 2026-Q4 | 122 | -61 | 86% |
| Price paid | 0.70-0.90 | 126 | +30 | 86% |
| Price paid | 0.90-1.01 | 643 | +83 | 98% |
| Model vs market gap | 0.00-0.05 | 139 | +32 | 97% |
| Model vs market gap | 0.05-0.10 | 153 | +41 | 88% |
| Model vs market gap | 0.10-0.20 | 11 | +6 | 82% |
| Model vs market gap | no model | 466 | +33 | 99% |
| Side | no | 527 | +85 | 99% |
| Side | yes | 242 | +28 | 91% |

## Ethereum

608 events, 2025-03-27 to 2026-11-25.

**Verdict:** Vol x0.5, weekends only: +85 on 161 trades (+5.4% per $ staked, t=1.07), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | t | t (event) | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Time-of-day vol x0.5, skip spikes | 811 | 82% | +169.14 | +2.1% | 1.26 | 1.17 | -52 | +221 | 92% | 0.1519 | 0.1431 |
| Time-of-day vol x0.5, against trend + skip spikes | 446 | 84% | +160.82 | +3.7% | 1.67 | 1.52 | -39 | +200 | 93% | 0.1412 | 0.1358 |
| Time-of-day vol x0.5 | 1275 | 81% | +106.05 | +0.9% | 0.62 | 1.32 | -139 | +245 | 92% | 0.1595 | 0.1471 |
| Vol x0.5, weekends only | 161 | 83% | +85.39 | +5.4% | 1.07 | 1.33 | +1 | +84 | 92% | 0.1332 | 0.1299 |
| Market favorite (no model) | 118 | 65% | +82.44 | +7.0% | 0.91 | 0.91 | +93 | -11 | – | – | 0.2035 |
| Bayes price-level, 95% sure | 49 | 80% | +61.96 | +12.8% | 1.49 | 1.49 | +43 | +19 | 77% | 0.149 | 0.1578 |
| Vol x0.5, skip spiked markets | 946 | 80% | +41.11 | +0.4% | 0.26 | -0.14 | -216 | +257 | 93% | 0.1739 | 0.1576 |
| Vol x0.5, against trend + skip spikes | 515 | 80% | +12.91 | +0.3% | 0.09 | -0.06 | -175 | +188 | 93% | 0.1762 | 0.1592 |
| Bayes: market prior + full vol | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Bayes: market prior + fat-tail | 0 | – | +0.00 | – | – | – | +0 | +0 | – | – | – |
| Long-shot fade (no model) | 619 | 96% | -16.84 | -0.3% | -0.28 | -0.18 | -88 | +71 | – | – | 0.0437 |
| Combined: rolling best (past 6 months) | 277 | 79% | -26.91 | -1.0% | -0.32 | -0.46 | -97 | +70 | 93% | 0.164 | 0.1538 |
| Bayes price-level, 99% sure | 3 | 0% | -29.77 | -100.0% | – | – | -10 | -20 | 72% | 0.5155 | 0.3521 |
| Vol x0.75 | 430 | 77% | -44.75 | -1.1% | -0.28 | -0.49 | -164 | +119 | 88% | 0.1596 | 0.1465 |
| Vol x0.5, news days only | 83 | 75% | -46.16 | -5.7% | -0.93 | -1.27 | -30 | -17 | 92% | 0.2044 | 0.1751 |
| Fat-tail (actual past moves) | 365 | 68% | -57.72 | -1.6% | -0.24 | -0.22 | -214 | +156 | 79% | 0.1862 | 0.1723 |
| Vol x0.5, calm market only | 777 | 79% | -58.43 | -0.8% | -0.38 | -0.06 | -226 | +168 | 92% | 0.1769 | 0.1595 |
| Vol x0.5, against the 24h trend | 723 | 79% | -59.00 | -0.8% | -0.4 | -0.49 | -284 | +225 | 93% | 0.1827 | 0.1632 |
| Vol x0.5, 5c edge | 1747 | 79% | -72.92 | -0.4% | -0.33 | 0.07 | -389 | +316 | 92% | 0.1755 | 0.1582 |
| Regime-scaled vol x0.5 | 1626 | 79% | -130.81 | -0.8% | -0.63 | 0.25 | -356 | +225 | 93% | 0.18 | 0.1594 |
| Vol x0.5, with the 24h trend | 746 | 78% | -145.84 | -2.0% | -1.03 | -1.08 | -100 | -46 | 92% | 0.1869 | 0.1634 |
| Vol x0.5, busy market only | 692 | 78% | -146.41 | -2.2% | -1.07 | -0.91 | -155 | +8 | 93% | 0.1937 | 0.1676 |
| Vol x0.5, skip news days | 1386 | 78% | -158.68 | -1.2% | -0.8 | -0.31 | -377 | +219 | 93% | 0.1837 | 0.1626 |
| Vol x0.5, NO only | 927 | 78% | -162.38 | -1.8% | -1.03 | -1.02 | -238 | +76 | 92% | 0.1808 | 0.1607 |
| Fat-tail, moves x0.75 | 922 | 74% | -199.82 | -2.2% | -1.08 | -1.21 | -232 | +32 | 87% | 0.2032 | 0.1854 |
| Vol x0.5, skip news in window | 1446 | 78% | -200.00 | -1.4% | -0.99 | -0.57 | -383 | +183 | 93% | 0.1852 | 0.1636 |
| Vol x0.5 (Bitcoin's winner) | 1469 | 78% | -204.84 | -1.4% | -1.01 | -0.67 | -394 | +189 | 93% | 0.1848 | 0.1633 |
| Full vol + 50% market blend | 107 | 26% | -250.82 | -22.7% | -0.99 | -0.78 | -288 | +38 | 38% | 0.1358 | 0.1221 |
| Vol x0.5, weekdays only | 1308 | 78% | -290.23 | -2.3% | -1.51 | -1.24 | -368 | +78 | 93% | 0.1912 | 0.1674 |
| Fat-tail, moves x0.5 | 1756 | 74% | -310.35 | -1.8% | -1.26 | -1.11 | -421 | +111 | 90% | 0.2068 | 0.1811 |
| Options vol x0.85, 5c gap | 455 | 57% | -407.81 | -8.9% | -1.05 | -0.85 | -566 | +158 | 68% | 0.1341 | 0.1201 |
| Options vol, NO only | 222 | 29% | -514.39 | -22.4% | -1.42 | -1.15 | -628 | +113 | 43% | 0.1191 | 0.0961 |
| Heavy-volume move (10c, 5x): follow | 421 | 60% | -545.75 | -13.0% | -3.26 | -3.11 | -266 | -280 | – | – | 0.182 |
| Options vol, 8c gap | 201 | 17% | -589.03 | -28.1% | -1.52 | -1.2 | -726 | +137 | 36% | 0.1318 | 0.0952 |
| Vol x0.5, take profit 10c | 1469 | 81% | -620.95 | -4.3% | -3.51 | -2.98 | -578 | -43 | 93% | 0.1649 | 0.1528 |
| Combined: 5+ strategies agree | 1743 | 74% | -710.94 | -4.2% | -2.1 | -1.67 | -777 | +66 | 87% | 0.1766 | 0.1596 |
| Vol x0.5, stop loss 25c | 1469 | 65% | -734.80 | -5.1% | -4.18 | -3.86 | -769 | +35 | 93% | 0.3022 | 0.2354 |
| Heavy-volume move (10c, 5x): fade | 470 | 36% | -826.58 | -17.1% | -2.6 | -2.81 | -180 | -646 | – | – | 0.1656 |
| Full vol (v1 rule) | 232 | 32% | -886.37 | -37.2% | -3.2 | -2.8 | -798 | -88 | 49% | 0.1262 | 0.0945 |
| Vol x0.5, take profit 15c / stop 15c | 1469 | 57% | -1015.18 | -7.1% | -7.33 | -6.61 | -865 | -150 | 93% | 0.3692 | 0.2795 |
| Heavy-volume move: follow | 765 | 57% | -1018.75 | -13.3% | -3.99 | -3.63 | -432 | -587 | – | – | 0.1861 |
| Heavy-volume move: fade | 829 | 38% | -1071.90 | -12.6% | -2.5 | -2.99 | -364 | -708 | – | – | 0.1726 |
| Vol x0.5, stop loss 10c | 1469 | 47% | -1091.63 | -7.6% | -7.44 | -6.91 | -967 | -125 | 93% | 0.4519 | 0.3292 |
| Options vol, 5c gap | 395 | 23% | -1509.13 | -36.9% | -3.52 | -3.28 | -1244 | -265 | 40% | 0.1215 | 0.094 |
| Vol x0.5, limit order | 736 | 57% | -1740.13 | -24.5% | -10.03 | -11.32 | -1147 | -594 | 92% | 0.3563 | 0.267 |
| Vol x0.5, limit order (strict fill) | 715 | 56% | -1792.21 | -25.9% | -10.42 | -11.68 | -1162 | -630 | 92% | 0.3666 | 0.2736 |
| Combined: 3+ strategies agree | 2473 | 66% | -1919.80 | -7.8% | -3.62 | -3.15 | -1356 | -564 | 84% | 0.1716 | 0.1577 |
| Vol x0.5 5c edge, limit order | 857 | 58% | -1937.31 | -23.4% | -10.35 | -11.79 | -1238 | -700 | 91% | 0.3424 | 0.2609 |
| Kalshi price-spike fade (no model) | 1082 | 31% | -2404.07 | -21.6% | -4.9 | -4.55 | -920 | -1484 | – | – | 0.17 |

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
| 0.3 | 2064 | -100.02 | -0.5% |
| 0.4 | 1828 | -283.49 | -1.6% |
| 0.5 | 1469 | -204.84 | -1.4% |
| 0.6 | 1000 | -229.33 | -2.4% |
| 0.75 | 430 | -44.75 | -1.1% |
| 1.0 | 232 | -886.37 | -37.2% |

Sweep: time-of-day vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1733 | -8.36 | -0.1% |
| 0.5 | 1275 | +106.05 | +0.9% |
| 0.6 | 726 | -107.39 | -1.5% |
| 0.75 | 247 | -316.13 | -13.0% |
| 1.0 | 246 | -956.79 | -37.4% |

Sweep: fat-tail

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 2011 | -130.51 | -0.7% |
| 0.5 | 1756 | -310.35 | -1.8% |
| 0.6 | 1418 | -127.84 | -0.9% |
| 0.75 | 922 | -199.82 | -2.2% |
| 0.9 | 536 | -217.19 | -4.1% |
| 1.0 | 365 | -57.72 | -1.6% |

Sweep: options vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 1385 | -384.10 | -2.8% |
| 0.7 | 908 | -353.09 | -4.0% |
| 0.8 | 549 | -422.17 | -7.8% |
| 0.9 | 390 | -670.36 | -16.9% |
| 1.0 | 395 | -1509.13 | -36.9% |
| 1.1 | 531 | -2900.33 | -52.2% |

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

Why: Vol x0.5, weekends only

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 2 | -8 | 50% |
| Quarter | 2025-Q2 | 4 | -3 | 75% |
| Quarter | 2025-Q3 | 22 | +21 | 91% |
| Quarter | 2025-Q4 | 36 | -23 | 75% |
| Quarter | 2026-Q1 | 43 | +11 | 86% |
| Quarter | 2026-Q2 | 21 | +25 | 90% |
| Quarter | 2026-Q3 | 13 | +67 | 92% |
| Quarter | 2026-Q4 | 20 | -6 | 75% |
| Price paid | 0.00-0.10 | 1 | -11 | 0% |
| Price paid | 0.10-0.30 | 1 | +51 | 100% |
| Price paid | 0.50-0.70 | 15 | -25 | 53% |
| Price paid | 0.70-0.90 | 134 | +60 | 86% |
| Price paid | 0.90-1.01 | 10 | +10 | 100% |
| Model vs market gap | 0.05-0.10 | 1 | -11 | 0% |
| Model vs market gap | 0.10-0.20 | 139 | +82 | 84% |
| Model vs market gap | 0.20-0.35 | 21 | +14 | 81% |
| Side | no | 92 | +47 | 85% |
| Side | yes | 69 | +38 | 81% |

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
| Quarter | 2026-Q4 | 95 | -354 | 30% |
| Price paid | 0.10-0.30 | 540 | -2109 | 13% |
| Price paid | 0.30-0.50 | 304 | -306 | 36% |
| Price paid | 0.50-0.70 | 184 | +13 | 60% |
| Price paid | 0.70-0.90 | 54 | -1 | 76% |
| Model vs market gap | no model | 1082 | -2404 | 31% |
| Side | no | 499 | -1243 | 34% |
| Side | yes | 583 | -1161 | 28% |

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
| Quarter | 2026-Q4 | 48 | +14 | 83% |
| Price paid | 0.50-0.70 | 37 | +61 | 78% |
| Price paid | 0.70-0.90 | 389 | +101 | 84% |
| Price paid | 0.90-1.01 | 20 | -1 | 90% |
| Model vs market gap | 0.05-0.10 | 7 | +8 | 100% |
| Model vs market gap | 0.10-0.20 | 401 | +156 | 84% |
| Model vs market gap | 0.20-0.35 | 37 | -8 | 73% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 215 | +143 | 87% |
| Side | yes | 231 | +18 | 81% |

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
| Quarter | 2026-Q4 | 146 | +48 | 82% |
| Price paid | 0.10-0.30 | 4 | -42 | 0% |
| Price paid | 0.50-0.70 | 146 | +5 | 67% |
| Price paid | 0.70-0.90 | 1083 | +122 | 83% |
| Price paid | 0.90-1.01 | 42 | +21 | 95% |
| Model vs market gap | 0.05-0.10 | 16 | -13 | 81% |
| Model vs market gap | 0.10-0.20 | 1127 | +153 | 82% |
| Model vs market gap | 0.20-0.35 | 131 | -38 | 72% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 643 | +24 | 81% |
| Side | yes | 632 | +82 | 81% |

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
| Quarter | 2026-Q4 | 48 | +14 | 83% |
| Price paid | 0.30-0.50 | 3 | -5 | 33% |
| Price paid | 0.50-0.70 | 31 | -33 | 58% |
| Price paid | 0.70-0.90 | 229 | +7 | 82% |
| Price paid | 0.90-1.01 | 14 | +3 | 93% |
| Model vs market gap | 0.05-0.10 | 6 | +7 | 100% |
| Model vs market gap | 0.10-0.20 | 223 | +2 | 82% |
| Model vs market gap | 0.20-0.35 | 22 | -19 | 68% |
| Model vs market gap | no model | 26 | -16 | 62% |
| Side | no | 120 | +79 | 88% |
| Side | yes | 157 | -105 | 73% |
