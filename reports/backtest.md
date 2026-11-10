# Backtest (2026-11-09)

Flat $10 per trade at the ask plus Kalshi fees, held to settlement. Prices are real hourly Kalshi quotes. Forecasts are archived NWS-blend (NBM) runs 1-2 days old. Bias/sigma learned only from earlier days.

## Live paper books vs backtest

| Book | Settled | Open | Live P&L | Live return/$ | Backtest rule | Backtest return/$ |
|---|---|---|---|---|---|---|
| bitcoin | 0 | 4 | +0.00 | – | c_vol50 | +0.4% |
| bitcoin_tod | 0 | 4 | +0.00 | – | s_combo_tod | +2.9% |
| ethereum | 0 | 4 | +0.00 | – | a_vol50 | -1.8% |
| ethereum_tod | 0 | 4 | +0.00 | – | s_combo_tod | +2.0% |
| weather_high | 0 | 11 | +0.00 | – | fade | +0.1% |
| weather_low | 0 | 4 | +0.00 | – | fade | +0.3% |

Live numbers need ~100 settled trades before they mean much.

## Weather: daily highs

3731 events, 2025-03-18 to 2026-11-08.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Kalshi price-spike fade (no model) (+114 on 484 trades).

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 484 | 44% | +114.33 | +2.3% | -204 | +318 | – | – | 0.195 |
| Long-shot fade (no model) | 4928 | 95% | +35.53 | +0.1% | +40 | -5 | – | – | 0.0434 |
| Bayes: market prior + forecast | 2 | 50% | -4.85 | -24.4% | -10 | +5 | 74% | 0.3459 | 0.3305 |
| Bayes price-level, 99% sure | 1028 | 89% | -107.27 | -1.1% | -27 | -80 | 92% | 0.0995 | 0.0983 |
| Market favorite YES (no model) | 4569 | 50% | -180.22 | -0.4% | -134 | -46 | – | – | 0.2425 |
| Heavy-volume move (10c, 5x): fade | 308 | 48% | -209.41 | -6.7% | -208 | -2 | – | – | 0.1837 |
| Bayes price-level, 95% sure | 1928 | 87% | -238.21 | -1.3% | -130 | -108 | 90% | 0.107 | 0.1059 |
| Heavy-volume move (10c, 5x): follow | 290 | 49% | -391.66 | -13.4% | -274 | -118 | – | – | 0.1948 |
| Long-shot fade, limit order | 2820 | 92% | -472.94 | -1.8% | -211 | -262 | – | – | 0.0732 |
| Combined: rolling best (past 6 months) | 2484 | 76% | -693.90 | -2.9% | -332 | -362 | 92% | 0.1131 | 0.1277 |
| Combined: 5+ strategies agree | 4933 | 49% | -909.17 | -1.8% | -337 | -572 | 61% | 0.2301 | 0.2366 |
| Heavy-volume move: fade | 1524 | 48% | -1060.54 | -6.9% | -1091 | +31 | – | – | 0.1871 |
| Heavy-volume move: follow | 1489 | 49% | -1694.27 | -11.3% | -700 | -994 | – | – | 0.1915 |
| Favorite, stop loss 25c | 4569 | 42% | -2362.55 | -5.1% | -2142 | -220 | – | – | 0.2409 |
| Forecast bracket YES | 739 | 10% | -3397.55 | -43.7% | -1711 | -1686 | 33% | 0.1466 | 0.0915 |
| Favorite, take profit 10c | 4569 | 70% | -3688.57 | -8.0% | -2220 | -1469 | – | – | 0.2616 |
| Favorite, stop loss 10c | 4569 | 28% | -4163.06 | -9.0% | -2950 | -1213 | – | – | 0.2361 |
| Favorite, take profit 15c / stop 15c | 4569 | 47% | -5429.16 | -11.8% | -3770 | -1659 | – | – | 0.2509 |
| Market favorite, limit order | 3719 | 39% | -6414.99 | -17.5% | -4312 | -2103 | – | – | 0.2359 |
| v2 + disagreement cap | 3213 | 33% | -8369.79 | -25.4% | -4217 | -4153 | 54% | 0.2012 | 0.1572 |
| v2 + 50% market blend | 3555 | 31% | -9247.46 | -25.3% | -4237 | -5011 | 46% | 0.1904 | 0.1646 |
| v1 (what we ran live) | 4401 | 34% | -9383.88 | -20.8% | -4259 | -5125 | 63% | 0.2626 | 0.1645 |
| v2 calibrated | 4011 | 32% | -10187.19 | -24.8% | -4702 | -5485 | 58% | 0.2445 | 0.1673 |
| Combined: 3+ strategies agree | 8954 | 44% | -10526.69 | -11.6% | -3795 | -6731 | 62% | 0.2717 | 0.202 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| v2 calibrated | 15 | +151.03 | +99.4% |
| v2 + 50% market blend | 13 | +130.80 | +99.7% |
| Long-shot fade (no model) | 2166 | +107.27 | +0.5% |
| Forecast bracket YES | 4 | +104.20 | +249.3% |
| v1 (what we ran live) | 12 | +38.08 | +31.2% |
| v2 + disagreement cap | 12 | +37.79 | +31.2% |
| Bayes: market prior + forecast | 0 | +0.00 | – |
| Bayes price-level, 99% sure | 326 | -82.84 | -2.6% |
| Long-shot fade, limit order | 1165 | -126.37 | -1.2% |
| Bayes price-level, 95% sure | 652 | -133.91 | -2.1% |
| Kalshi price-spike fade (no model) | 224 | -144.65 | -6.3% |
| Heavy-volume move (10c, 5x): fade | 166 | -201.00 | -11.9% |
| Combined: 5+ strategies agree | 2359 | -207.50 | -0.9% |
| Market favorite YES (no model) | 2358 | -252.03 | -1.1% |
| Heavy-volume move (10c, 5x): follow | 153 | -266.79 | -17.3% |
| Combined: 3+ strategies agree | 2531 | -311.05 | -1.2% |
| Combined: rolling best (past 6 months) | 1271 | -363.91 | -2.9% |
| Heavy-volume move: follow | 684 | -578.54 | -8.4% |
| Heavy-volume move: fade | 716 | -1025.64 | -14.1% |
| Favorite, stop loss 25c | 2358 | -2229.92 | -9.3% |
| Favorite, take profit 10c | 2358 | -2333.98 | -9.8% |
| Favorite, stop loss 10c | 2358 | -3104.18 | -13.0% |
| Favorite, take profit 15c / stop 15c | 2358 | -3898.38 | -16.3% |
| Market favorite, limit order | 1852 | -4313.16 | -23.5% |

Sweep: sigma

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 3990 | -9405.70 | -23.1% |
| 0.8 | 3853 | -9815.15 | -24.8% |
| 1.0 | 4011 | -10187.19 | -24.8% |
| 1.25 | 4268 | -8855.22 | -20.3% |
| 1.5 | 4416 | -7843.97 | -17.4% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 4891 | -11662.46 | -23.2% |
| blend 0.0, edge 0.05 | 4584 | -11036.50 | -23.5% |
| blend 0.0, edge 0.08 | 4011 | -10187.19 | -24.8% |
| blend 0.25, edge 0.03 | 4633 | -11414.80 | -24.0% |
| blend 0.25, edge 0.05 | 4151 | -10498.61 | -24.6% |
| blend 0.25, edge 0.08 | 3247 | -8744.37 | -26.2% |
| blend 0.5, edge 0.03 | 3992 | -10264.49 | -25.0% |
| blend 0.5, edge 0.05 | 3077 | -8236.42 | -26.0% |
| blend 0.5, edge 0.08 | 1853 | -4562.21 | -23.9% |
| blend 0.75, edge 0.03 | 1847 | -5143.32 | -27.0% |
| blend 0.75, edge 0.05 | 787 | -1928.43 | -23.7% |
| blend 0.75, edge 0.08 | 211 | -668.88 | -30.5% |

Rolling best: which strategy it picked each quarter

| Quarter | Picked | Past t |
|---|---|---|
| 2025-Q1 | sat out | – |
| 2025-Q2 | sat out | – |
| 2025-Q3 | Market favorite YES (no model) | 0.4 |
| 2025-Q4 | Long-shot fade (no model) | 1.76 |
| 2026-Q1 | Bayes price-level, 99% sure | 0.59 |
| 2026-Q2 | Long-shot fade (no model) | 0.33 |
| 2026-Q3 | Heavy-volume move (10c, 5x): fade | 1.0 |
| 2026-Q4 | Kalshi price-spike fade (no model) | 1.4 |

Why: v2 calibrated

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q1 | 285 | -591 | 37% |
| Quarter | 2026-Q2 | 1467 | -4421 | 33% |
| Quarter | 2026-Q3 | 1563 | -2938 | 32% |
| Quarter | 2026-Q4 | 696 | -2237 | 30% |
| Price paid | 0.00-0.10 | 806 | -3101 | 4% |
| Price paid | 0.10-0.30 | 857 | -4020 | 10% |
| Price paid | 0.30-0.50 | 838 | -1397 | 36% |
| Price paid | 0.50-0.70 | 1186 | -1437 | 53% |
| Price paid | 0.70-0.90 | 323 | -221 | 71% |
| Price paid | 0.90-1.01 | 1 | -10 | 0% |
| Model vs market gap | 0.05-0.10 | 59 | -148 | 15% |
| Model vs market gap | 0.10-0.20 | 2047 | -5898 | 31% |
| Model vs market gap | 0.20-0.35 | 1520 | -3216 | 34% |
| Model vs market gap | 0.35-1.01 | 385 | -925 | 28% |
| Side | no | 2420 | -3367 | 48% |
| Side | yes | 1591 | -6820 | 8% |

Why: Kalshi price-spike fade (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 10 | -67 | 20% |
| Quarter | 2025-Q2 | 60 | +32 | 35% |
| Quarter | 2025-Q3 | 53 | -102 | 40% |
| Quarter | 2025-Q4 | 23 | +22 | 48% |
| Quarter | 2026-Q1 | 99 | -104 | 39% |
| Quarter | 2026-Q2 | 111 | +134 | 50% |
| Quarter | 2026-Q3 | 96 | +272 | 52% |
| Quarter | 2026-Q4 | 32 | -72 | 44% |
| Price paid | 0.10-0.30 | 174 | -13 | 20% |
| Price paid | 0.30-0.50 | 128 | -38 | 40% |
| Price paid | 0.50-0.70 | 141 | +168 | 69% |
| Price paid | 0.70-0.90 | 41 | -2 | 76% |
| Model vs market gap | no model | 484 | +114 | 44% |
| Side | no | 280 | +69 | 57% |
| Side | yes | 204 | +46 | 26% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 13 | -43 | 62% |
| Quarter | 2025-Q3 | 186 | +11 | 91% |
| Quarter | 2025-Q4 | 111 | +15 | 89% |
| Quarter | 2026-Q1 | 490 | -91 | 87% |
| Quarter | 2026-Q2 | 497 | -72 | 87% |
| Quarter | 2026-Q3 | 443 | -43 | 87% |
| Quarter | 2026-Q4 | 188 | -15 | 86% |
| Price paid | 0.30-0.50 | 4 | -41 | 0% |
| Price paid | 0.50-0.70 | 24 | +32 | 58% |
| Price paid | 0.70-0.90 | 690 | -154 | 82% |
| Price paid | 0.90-1.01 | 1210 | -76 | 91% |
| Model vs market gap | 0.00-0.05 | 1649 | -141 | 88% |
| Model vs market gap | 0.05-0.10 | 274 | -47 | 82% |
| Model vs market gap | 0.10-0.20 | 5 | -51 | 0% |
| Side | no | 1899 | -219 | 88% |
| Side | yes | 29 | -19 | 48% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 819 | -221 | 48% |
| Quarter | 2025-Q4 | 268 | -37 | 94% |
| Quarter | 2026-Q1 | 250 | -96 | 87% |
| Quarter | 2026-Q2 | 1056 | -99 | 94% |
| Quarter | 2026-Q3 | 59 | -169 | 41% |
| Quarter | 2026-Q4 | 32 | -72 | 44% |
| Price paid | 0.10-0.30 | 25 | -215 | 4% |
| Price paid | 0.30-0.50 | 477 | -215 | 41% |
| Price paid | 0.50-0.70 | 383 | -21 | 57% |
| Price paid | 0.70-0.90 | 51 | -84 | 65% |
| Price paid | 0.90-1.01 | 1548 | -159 | 94% |
| Model vs market gap | 0.00-0.05 | 219 | -63 | 88% |
| Model vs market gap | 0.05-0.10 | 31 | -33 | 81% |
| Model vs market gap | no model | 2234 | -598 | 75% |
| Side | no | 1630 | -268 | 92% |
| Side | yes | 854 | -426 | 47% |

Forecast error (actual minus NBM forecast)

| City | Entry | n | Bias | RMSE |
|---|---|---|---|---|
| Austin | day before 10am | 240 | +1.84 | 3.29 |
| Austin | same day 8am | 242 | +1.54 | 2.93 |
| Chicago | day before 10am | 240 | +1.44 | 3.43 |
| Chicago | same day 8am | 238 | +1.27 | 2.85 |
| Denver | day before 10am | 241 | +1.74 | 3.41 |
| Denver | same day 8am | 238 | +1.67 | 2.97 |
| Los Angeles | day before 10am | 239 | +2.31 | 3.89 |
| Los Angeles | same day 8am | 241 | +2.32 | 3.63 |
| Miami | same day 8am | 241 | +2.05 | 2.66 |
| New York | same day 8am | 238 | -0.26 | 2.46 |
| Philadelphia | same day 8am | 238 | +1.74 | 2.88 |

## Weather: daily lows

2193 events, 2025-12-13 to 2026-11-08.

**Verdict:** Long-shot fade (no model): +100 on 3197 trades (+0.3% per $ staked, t=0.92), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 152 | 53% | +257.44 | +16.7% | -53 | +310 | – | – | 0.2106 |
| Combined: rolling best (past 6 months) | 1645 | 78% | +233.57 | +1.5% | +165 | +68 | – | – | 0.1229 |
| Long-shot fade (no model) | 3197 | 96% | +100.17 | +0.3% | +79 | +22 | – | – | 0.0367 |
| Heavy-volume move: follow | 0 | – | +0.00 | – | +0 | +0 | – | – | – |
| Heavy-volume move: fade | 0 | – | +0.00 | – | +0 | +0 | – | – | – |
| Heavy-volume move (10c, 5x): follow | 0 | – | +0.00 | – | +0 | +0 | – | – | – |
| Heavy-volume move (10c, 5x): fade | 0 | – | +0.00 | – | +0 | +0 | – | – | – |
| Bayes: market prior + forecast | 1 | 0% | -10.25 | -100.0% | +0 | -10 | 49% | 0.2401 | 0.16 |
| Bayes price-level, 99% sure | 158 | 90% | -13.80 | -0.9% | -29 | +15 | 93% | 0.0864 | 0.0861 |
| Bayes price-level, 95% sure | 349 | 90% | -116.17 | -3.4% | -156 | +40 | 92% | 0.0672 | 0.0668 |
| Long-shot fade, limit order | 1689 | 93% | -204.21 | -1.3% | -71 | -134 | – | – | 0.0667 |
| Combined: 5+ strategies agree | 2158 | 46% | -516.26 | -2.4% | +650 | -1166 | 54% | 0.2351 | 0.2371 |
| Market favorite YES (no model) | 2094 | 47% | -614.23 | -2.9% | +458 | -1073 | – | – | 0.2394 |
| Forecast bracket YES | 540 | 14% | -1717.56 | -30.3% | -1026 | -692 | 34% | 0.1609 | 0.1206 |
| Favorite, take profit 10c | 2094 | 62% | -2714.27 | -12.8% | -986 | -1728 | – | – | 0.2661 |
| Market favorite, limit order | 1741 | 36% | -2965.32 | -17.2% | -795 | -2171 | – | – | 0.226 |
| v2 + 50% market blend | 1842 | 29% | -3901.93 | -20.5% | -1126 | -2776 | 41% | 0.1562 | 0.1411 |
| Favorite, stop loss 25c | 2094 | 29% | -5190.13 | -24.4% | -2220 | -2970 | – | – | 0.2285 |
| v2 calibrated | 2557 | 31% | -5643.92 | -21.5% | -1580 | -4064 | 52% | 0.1998 | 0.1494 |
| Favorite, stop loss 10c | 2094 | 14% | -5692.74 | -26.8% | -2837 | -2856 | – | – | 0.2159 |
| v2 + disagreement cap | 2226 | 31% | -6118.05 | -26.8% | -2100 | -4018 | 50% | 0.1775 | 0.1426 |
| Combined: 3+ strategies agree | 4286 | 39% | -6127.26 | -14.0% | -2017 | -4110 | 57% | 0.2332 | 0.1896 |
| Favorite, take profit 15c / stop 15c | 2094 | 28% | -6301.99 | -29.6% | -3268 | -3034 | – | – | 0.2351 |
| v1 (what we ran live) | 3767 | 32% | -10461.69 | -27.0% | -4429 | -6032 | 57% | 0.2259 | 0.1473 |

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
| 0.6 | 3313 | -5234.09 | -15.5% |
| 0.8 | 2622 | -4958.61 | -18.4% |
| 1.0 | 2557 | -5643.92 | -21.5% |
| 1.25 | 2980 | -6754.74 | -22.1% |
| 1.5 | 3497 | -8674.27 | -24.2% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 3942 | -9193.31 | -22.7% |
| blend 0.0, edge 0.05 | 3379 | -8079.76 | -23.3% |
| blend 0.0, edge 0.08 | 2557 | -5643.92 | -21.5% |
| blend 0.25, edge 0.03 | 3373 | -7957.47 | -22.9% |
| blend 0.25, edge 0.05 | 2643 | -5745.31 | -21.1% |
| blend 0.25, edge 0.08 | 1699 | -3555.26 | -20.3% |
| blend 0.5, edge 0.03 | 2307 | -5047.08 | -21.2% |
| blend 0.5, edge 0.05 | 1477 | -3104.01 | -20.3% |
| blend 0.5, edge 0.08 | 713 | -504.92 | -6.8% |
| blend 0.75, edge 0.03 | 613 | -577.71 | -9.1% |
| blend 0.75, edge 0.05 | 241 | -516.07 | -20.6% |
| blend 0.75, edge 0.08 | 53 | -353.82 | -64.0% |

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
| Quarter | 2026-Q4 | 342 | -518 | 28% |
| Price paid | 0.00-0.10 | 549 | -2155 | 5% |
| Price paid | 0.10-0.30 | 790 | -2255 | 12% |
| Price paid | 0.30-0.50 | 305 | -709 | 33% |
| Price paid | 0.50-0.70 | 628 | -388 | 58% |
| Price paid | 0.70-0.90 | 284 | -139 | 73% |
| Price paid | 0.90-1.01 | 1 | +1 | 100% |
| Model vs market gap | 0.05-0.10 | 36 | +38 | 19% |
| Model vs market gap | 0.10-0.20 | 1605 | -4516 | 31% |
| Model vs market gap | 0.20-0.35 | 757 | -608 | 34% |
| Model vs market gap | 0.35-1.01 | 159 | -557 | 24% |
| Side | no | 1201 | -1183 | 55% |
| Side | yes | 1356 | -4461 | 10% |

Why: Long-shot fade (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q1 | 950 | -40 | 95% |
| Quarter | 2026-Q2 | 1044 | +162 | 97% |
| Quarter | 2026-Q3 | 976 | -12 | 96% |
| Quarter | 2026-Q4 | 227 | -11 | 96% |
| Price paid | 0.90-1.01 | 3197 | +100 | 96% |
| Model vs market gap | no model | 3197 | +100 | 96% |
| Side | no | 3197 | +100 | 96% |

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
| Quarter | 2026-Q1 | 10 | -106 | 0% |
| Quarter | 2026-Q2 | 75 | -10 | 89% |
| Quarter | 2026-Q3 | 146 | +2 | 92% |
| Quarter | 2026-Q4 | 118 | -2 | 95% |
| Price paid | 0.10-0.30 | 10 | -106 | 0% |
| Price paid | 0.50-0.70 | 8 | -5 | 62% |
| Price paid | 0.90-1.01 | 331 | -5 | 93% |
| Model vs market gap | 0.00-0.05 | 253 | -71 | 91% |
| Model vs market gap | 0.05-0.10 | 88 | -40 | 89% |
| Model vs market gap | 0.10-0.20 | 8 | -5 | 62% |
| Side | no | 331 | -5 | 93% |
| Side | yes | 18 | -111 | 28% |

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
| Austin | day before 10am | 240 | -2.67 | 4.14 |
| Austin | day before 8pm | 242 | -2.76 | 4.01 |
| Chicago | day before 10am | 240 | -1.61 | 3.03 |
| Chicago | day before 8pm | 242 | -1.38 | 2.67 |
| Denver | day before 10am | 241 | -3.93 | 5.2 |
| Denver | day before 8pm | 242 | -3.81 | 5.05 |
| Los Angeles | day before 10am | 240 | +0.36 | 1.71 |
| Los Angeles | day before 8pm | 242 | +0.48 | 1.61 |
| Miami | day before 8pm | 240 | -0.98 | 2.39 |
| New York | day before 8pm | 242 | -1.67 | 2.71 |
| Philadelphia | day before 8pm | 242 | +0.42 | 2.21 |

## Crypto: Bitcoin 5pm price

599 events, 2025-03-19 to 2026-11-08.

**Verdict:** Bayes price-level, 95% sure: +196 on 781 trades (+2.6% per $ staked, t=2.28), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Time-of-day vol x0.5 | 1521 | 80% | +305.72 | +2.1% | -138 | +444 | 92% | 0.1714 | 0.1587 |
| Time-of-day vol x0.5, skip spikes | 952 | 82% | +272.57 | +2.9% | -150 | +423 | 92% | 0.1613 | 0.1525 |
| Bayes price-level, 95% sure | 781 | 92% | +196.49 | +2.6% | +27 | +169 | 93% | 0.0761 | 0.0774 |
| Time-of-day vol x0.5, against trend + skip spikes | 503 | 82% | +195.64 | +4.0% | -113 | +309 | 92% | 0.1523 | 0.1457 |
| Combined: rolling best (past 6 months) | 611 | 81% | +177.76 | +3.0% | -3 | +181 | 93% | 0.1669 | 0.155 |
| Regime-scaled vol x0.5 | 1931 | 78% | +174.05 | +0.9% | -216 | +390 | 93% | 0.1882 | 0.1668 |
| Vol x0.5, weekends only | 230 | 84% | +149.69 | +6.7% | +17 | +132 | 91% | 0.1219 | 0.1265 |
| Vol x0.5, skip spiked markets | 1085 | 79% | +141.09 | +1.3% | -163 | +304 | 93% | 0.1805 | 0.1617 |
| Bayes price-level, 99% sure | 434 | 92% | +109.54 | +2.6% | -9 | +118 | 94% | 0.0715 | 0.0729 |
| Vol x0.5, against the 24h trend | 819 | 79% | +108.88 | +1.4% | -169 | +278 | 93% | 0.1828 | 0.1635 |
| Vol x0.5, against trend + skip spikes | 575 | 80% | +104.82 | +1.9% | -73 | +178 | 93% | 0.1734 | 0.1566 |
| Vol x0.5 | 1752 | 78% | +75.81 | +0.4% | -288 | +364 | 93% | 0.1887 | 0.1666 |
| Vol x0.5, calm market only | 1040 | 79% | +75.58 | +0.8% | -94 | +169 | 92% | 0.1779 | 0.1605 |
| Long-shot fade (no model) | 1275 | 96% | +58.49 | +0.5% | -52 | +111 | – | – | 0.0356 |
| Vol x0.5, skip news in window | 1728 | 78% | +56.41 | +0.3% | -287 | +343 | 93% | 0.1892 | 0.1668 |
| Vol x0.5, news days only | 101 | 79% | +40.11 | +4.1% | -10 | +50 | 93% | 0.1772 | 0.166 |
| Vol x0.5, skip news days | 1651 | 78% | +35.70 | +0.2% | -290 | +326 | 93% | 0.1894 | 0.1666 |
| Vol x0.5, busy market only | 712 | 77% | +0.23 | +0.0% | -206 | +206 | 93% | 0.2045 | 0.1755 |
| Bayes: market prior + full vol | 1 | 0% | -9.66 | -100.0% | +0 | -10 | 93% | 0.8638 | 0.7482 |
| Vol x0.5, with the 24h trend | 933 | 78% | -33.07 | -0.4% | -110 | +76 | 93% | 0.1939 | 0.1693 |
| Bayes: market prior + fat-tail | 25 | 64% | -41.26 | -16.8% | -28 | -14 | 86% | 0.2871 | 0.2499 |
| Vol x0.5, weekdays only | 1522 | 77% | -73.88 | -0.5% | -316 | +243 | 93% | 0.1988 | 0.1726 |
| Fat-tail, moves x0.5 | 1851 | 73% | -83.84 | -0.5% | -198 | +114 | 89% | 0.2226 | 0.1951 |
| Fat-tail, moves x0.75 | 1159 | 72% | -200.74 | -1.8% | -198 | -2 | 86% | 0.2085 | 0.1908 |
| Vol x0.5, stop loss 25c | 1752 | 65% | -429.21 | -2.5% | -740 | +311 | 93% | 0.3049 | 0.2342 |
| Vol x0.75 | 780 | 72% | -503.01 | -6.6% | -313 | -190 | 85% | 0.1707 | 0.153 |
| Heavy-volume move: follow | 1228 | 62% | -620.36 | -5.1% | -600 | -20 | – | – | 0.1825 |
| Fat-tail (actual past moves) | 618 | 58% | -659.60 | -10.7% | -599 | -61 | 73% | 0.2048 | 0.1826 |
| Vol x0.5, take profit 10c | 1752 | 81% | -690.57 | -4.0% | -661 | -29 | 93% | 0.1651 | 0.1545 |
| Heavy-volume move (10c, 5x): follow | 733 | 61% | -851.97 | -11.7% | -496 | -356 | – | – | 0.1813 |
| Combined: 5+ strategies agree | 2227 | 71% | -1013.78 | -4.6% | -1013 | -1 | 84% | 0.1746 | 0.1556 |
| Vol x0.5, stop loss 10c | 1752 | 47% | -1022.91 | -6.0% | -1078 | +55 | 93% | 0.4614 | 0.3269 |
| Vol x0.5, take profit 15c / stop 15c | 1752 | 57% | -1072.76 | -6.3% | -1077 | +4 | 93% | 0.3723 | 0.2762 |
| v1 + 50% market blend | 281 | 30% | -1131.81 | -39.1% | -642 | -489 | 41% | 0.1107 | 0.0982 |
| Options vol x0.85, 5c gap | 806 | 56% | -1195.19 | -14.8% | -706 | -489 | 65% | 0.1218 | 0.1107 |
| Heavy-volume move (10c, 5x): fade | 779 | 37% | -1341.35 | -16.8% | -754 | -587 | – | – | 0.1719 |
| v1 (what we ran live) | 444 | 37% | -1383.14 | -30.5% | -929 | -454 | 53% | 0.127 | 0.0986 |
| Options vol, 8c gap | 415 | 24% | -1412.59 | -32.8% | -1012 | -400 | 40% | 0.1097 | 0.0822 |
| Vol x0.5, limit order | 944 | 60% | -1711.15 | -18.8% | -1109 | -602 | 93% | 0.3416 | 0.2537 |
| Options vol, NO only | 589 | 31% | -1764.81 | -29.1% | -1341 | -424 | 45% | 0.1249 | 0.1033 |
| Vol x0.5, limit order (strict fill) | 907 | 59% | -1830.36 | -20.9% | -1149 | -681 | 92% | 0.3553 | 0.2615 |
| Vol x0.5 5c edge, limit order | 1038 | 60% | -1947.81 | -19.4% | -1204 | -743 | 91% | 0.3326 | 0.2495 |
| Options vol, 5c gap | 680 | 31% | -2157.19 | -30.8% | -1286 | -872 | 44% | 0.1143 | 0.0934 |
| Heavy-volume move: fade | 1281 | 35% | -2382.57 | -18.1% | -892 | -1490 | – | – | 0.175 |
| Combined: 3+ strategies agree | 3274 | 65% | -2630.47 | -8.1% | -1950 | -681 | 82% | 0.1718 | 0.155 |
| Kalshi price-spike fade (no model) | 1236 | 30% | -3214.89 | -25.2% | -1654 | -1561 | – | – | 0.1513 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Vol x0.5, weekends only | 141 | +56.47 | +4.1% |
| Vol x0.5, news days only | 28 | +6.46 | +2.4% |
| Bayes: market prior + full vol | 1 | -9.66 | -100.0% |
| Combined: rolling best (past 6 months) | 439 | -13.00 | -0.3% |
| Bayes price-level, 99% sure | 73 | -24.36 | -3.5% |
| Bayes price-level, 95% sure | 233 | -33.32 | -1.5% |
| Bayes: market prior + fat-tail | 25 | -41.26 | -16.8% |
| Vol x0.5, against trend + skip spikes | 358 | -69.23 | -2.0% |
| Long-shot fade (no model) | 492 | -70.68 | -1.5% |
| Vol x0.5, calm market only | 601 | -75.32 | -1.3% |
| Time-of-day vol x0.5, against trend + skip spikes | 268 | -95.70 | -3.7% |
| Vol x0.5, with the 24h trend | 547 | -125.26 | -2.3% |
| Time-of-day vol x0.5 | 775 | -132.17 | -1.8% |
| Fat-tail, moves x0.5 | 1092 | -139.67 | -1.3% |
| Time-of-day vol x0.5, skip spikes | 486 | -147.94 | -3.1% |
| Vol x0.5, against the 24h trend | 494 | -161.37 | -3.4% |
| Regime-scaled vol x0.5 | 1128 | -163.05 | -1.5% |
| Vol x0.5, skip spiked markets | 655 | -177.22 | -2.8% |
| Vol x0.5, busy market only | 440 | -211.31 | -4.9% |
| Fat-tail, moves x0.75 | 682 | -237.82 | -3.5% |
| Vol x0.5 | 1041 | -286.63 | -2.8% |
| Vol x0.5, skip news days | 1013 | -293.09 | -3.0% |
| Vol x0.5, skip news in window | 1037 | -304.27 | -3.0% |
| Vol x0.5, weekdays only | 900 | -343.10 | -3.9% |
| Vol x0.75 | 480 | -377.77 | -8.1% |
| v1 + 50% market blend | 98 | -383.34 | -38.8% |
| Heavy-volume move (10c, 5x): follow | 427 | -573.39 | -13.5% |
| Heavy-volume move: follow | 651 | -608.13 | -9.4% |
| Fat-tail (actual past moves) | 349 | -635.29 | -18.4% |
| Options vol x0.85, 5c gap | 397 | -679.38 | -17.1% |
| v1 (what we ran live) | 201 | -707.84 | -34.9% |
| Vol x0.5, take profit 10c | 1041 | -709.73 | -7.0% |
| Vol x0.5, stop loss 25c | 1041 | -743.22 | -7.3% |
| Options vol, 8c gap | 183 | -759.45 | -40.2% |
| Heavy-volume move (10c, 5x): fade | 465 | -764.85 | -16.0% |
| Options vol, NO only | 244 | -886.06 | -35.5% |
| Combined: 5+ strategies agree | 1249 | -983.60 | -8.0% |
| Options vol, 5c gap | 307 | -1026.99 | -32.6% |
| Heavy-volume move: fade | 694 | -1038.91 | -14.6% |
| Vol x0.5, stop loss 10c | 1041 | -1113.88 | -11.0% |
| Vol x0.5, take profit 15c / stop 15c | 1041 | -1152.41 | -11.3% |
| Vol x0.5, limit order | 567 | -1297.02 | -23.7% |
| Vol x0.5, limit order (strict fill) | 548 | -1358.18 | -25.7% |
| Vol x0.5 5c edge, limit order | 613 | -1413.22 | -23.9% |
| Combined: 3+ strategies agree | 1781 | -1977.16 | -11.2% |
| Kalshi price-spike fade (no model) | 719 | -2011.15 | -27.1% |

Sweep: vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1955 | +71.09 | +0.4% |
| 0.5 | 1752 | +75.81 | +0.4% |
| 0.6 | 1385 | -278.47 | -2.1% |
| 0.75 | 780 | -503.01 | -6.6% |
| 1.0 | 444 | -1383.14 | -30.5% |
| 1.25 | 550 | -2453.82 | -42.6% |

Sweep: options vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 1578 | -233.59 | -1.5% |
| 0.7 | 1271 | -717.30 | -5.7% |
| 0.8 | 936 | -886.16 | -9.5% |
| 0.9 | 738 | -1602.35 | -21.4% |
| 1.0 | 680 | -2157.19 | -30.8% |
| 1.1 | 750 | -2879.65 | -36.8% |

Sweep: time-of-day vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1944 | +88.51 | +0.5% |
| 0.5 | 1521 | +305.72 | +2.1% |
| 0.6 | 1006 | +273.26 | +2.8% |
| 0.75 | 408 | -8.10 | -0.2% |
| 1.0 | 328 | -1111.63 | -32.9% |

Sweep: fat-tail

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 2047 | -133.86 | -0.7% |
| 0.5 | 1851 | -83.84 | -0.5% |
| 0.6 | 1608 | -23.24 | -0.1% |
| 0.75 | 1159 | -200.74 | -1.8% |
| 0.9 | 775 | -652.89 | -8.5% |
| 1.0 | 618 | -659.60 | -10.7% |

Rolling best: which strategy it picked each quarter

| Quarter | Picked | Past t |
|---|---|---|
| 2025-Q1 | sat out | – |
| 2025-Q2 | Regime-scaled vol x0.5 | 0.79 |
| 2025-Q3 | Time-of-day vol x0.5, skip spikes | 0.58 |
| 2025-Q4 | sat out | – |
| 2026-Q1 | Vol x0.5, weekends only | 0.02 |
| 2026-Q2 | Vol x0.5, weekends only | 2.23 |
| 2026-Q3 | Time-of-day vol x0.5, against trend + skip spikes | 4.07 |
| 2026-Q4 | Time-of-day vol x0.5, against trend + skip spikes | 3.85 |

Volatility check: real moves vs the 30-day volatility assumed (1.0 = right, 0.5 = moved half as much)

| Quarter | Events | Ratio |
|---|---|---|
| 2025-Q1 | 26 | 0.424 |
| 2025-Q2 | 182 | 1.377 |
| 2025-Q3 | 184 | 1.255 |
| 2025-Q4 | 176 | 1.288 |
| 2026-Q1 | 180 | 1.329 |
| 2026-Q2 | 182 | 0.994 |
| 2026-Q3 | 184 | 1.018 |
| 2026-Q4 | 76 | 1.244 |

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
| Quarter | 2026-Q4 | 43 | +92 | 30% |
| Price paid | 0.00-0.10 | 65 | -414 | 3% |
| Price paid | 0.10-0.30 | 196 | -996 | 8% |
| Price paid | 0.30-0.50 | 3 | -9 | 33% |
| Price paid | 0.50-0.70 | 10 | +10 | 70% |
| Price paid | 0.70-0.90 | 169 | +24 | 82% |
| Price paid | 0.90-1.01 | 1 | +1 | 100% |
| Model vs market gap | 0.05-0.10 | 21 | +189 | 57% |
| Model vs market gap | 0.10-0.20 | 385 | -1300 | 37% |
| Model vs market gap | 0.20-0.35 | 38 | -272 | 24% |
| Side | no | 285 | -837 | 36% |
| Side | yes | 159 | -546 | 38% |

Why: Vol x0.5

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 15 | +9 | 87% |
| Quarter | 2025-Q2 | 245 | -2 | 78% |
| Quarter | 2025-Q3 | 271 | -151 | 74% |
| Quarter | 2025-Q4 | 274 | -143 | 75% |
| Quarter | 2026-Q1 | 298 | +23 | 77% |
| Quarter | 2026-Q2 | 298 | +186 | 82% |
| Quarter | 2026-Q3 | 250 | +76 | 81% |
| Quarter | 2026-Q4 | 101 | +78 | 83% |
| Price paid | 0.00-0.10 | 2 | -21 | 0% |
| Price paid | 0.10-0.30 | 3 | -32 | 0% |
| Price paid | 0.30-0.50 | 2 | +1 | 50% |
| Price paid | 0.50-0.70 | 198 | +146 | 73% |
| Price paid | 0.70-0.90 | 1538 | -17 | 79% |
| Price paid | 0.90-1.01 | 9 | -2 | 89% |
| Model vs market gap | 0.05-0.10 | 15 | -12 | 80% |
| Model vs market gap | 0.10-0.20 | 1225 | +39 | 80% |
| Model vs market gap | 0.20-0.35 | 511 | +45 | 74% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 977 | +0 | 78% |
| Side | yes | 775 | +76 | 79% |

Why: Kalshi price-spike fade (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 28 | -173 | 18% |
| Quarter | 2025-Q2 | 185 | -404 | 28% |
| Quarter | 2025-Q3 | 166 | -575 | 22% |
| Quarter | 2025-Q4 | 188 | -821 | 23% |
| Quarter | 2026-Q1 | 191 | -308 | 32% |
| Quarter | 2026-Q2 | 195 | -521 | 33% |
| Quarter | 2026-Q3 | 201 | -309 | 38% |
| Quarter | 2026-Q4 | 82 | -104 | 34% |
| Price paid | 0.10-0.30 | 688 | -3009 | 12% |
| Price paid | 0.30-0.50 | 294 | -457 | 34% |
| Price paid | 0.50-0.70 | 182 | +135 | 65% |
| Price paid | 0.70-0.90 | 72 | +115 | 89% |
| Model vs market gap | no model | 1236 | -3215 | 30% |
| Side | no | 600 | -1328 | 42% |
| Side | yes | 636 | -1887 | 18% |

Why: Time-of-day vol x0.5, against trend + skip spikes

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 6 | +15 | 100% |
| Quarter | 2025-Q2 | 39 | -9 | 77% |
| Quarter | 2025-Q3 | 67 | -6 | 79% |
| Quarter | 2025-Q4 | 87 | -112 | 69% |
| Quarter | 2026-Q1 | 87 | +60 | 85% |
| Quarter | 2026-Q2 | 103 | +155 | 91% |
| Quarter | 2026-Q3 | 77 | +58 | 86% |
| Quarter | 2026-Q4 | 37 | +34 | 86% |
| Price paid | 0.10-0.30 | 1 | -11 | 0% |
| Price paid | 0.50-0.70 | 38 | +29 | 74% |
| Price paid | 0.70-0.90 | 459 | +194 | 84% |
| Price paid | 0.90-1.01 | 5 | -17 | 60% |
| Model vs market gap | 0.05-0.10 | 12 | -4 | 83% |
| Model vs market gap | 0.10-0.20 | 420 | +160 | 83% |
| Model vs market gap | 0.20-0.35 | 71 | +40 | 79% |
| Side | no | 285 | +120 | 83% |
| Side | yes | 218 | +76 | 82% |

Why: Time-of-day vol x0.5

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 11 | +16 | 91% |
| Quarter | 2025-Q2 | 118 | -2 | 78% |
| Quarter | 2025-Q3 | 185 | -15 | 80% |
| Quarter | 2025-Q4 | 248 | -157 | 74% |
| Quarter | 2026-Q1 | 277 | +80 | 80% |
| Quarter | 2026-Q2 | 298 | +193 | 84% |
| Quarter | 2026-Q3 | 258 | +127 | 83% |
| Quarter | 2026-Q4 | 126 | +65 | 82% |
| Price paid | 0.10-0.30 | 2 | -21 | 0% |
| Price paid | 0.30-0.50 | 2 | +1 | 50% |
| Price paid | 0.50-0.70 | 128 | +125 | 74% |
| Price paid | 0.70-0.90 | 1381 | +215 | 81% |
| Price paid | 0.90-1.01 | 8 | -14 | 75% |
| Model vs market gap | 0.05-0.10 | 22 | -1 | 86% |
| Model vs market gap | 0.10-0.20 | 1238 | +177 | 81% |
| Model vs market gap | 0.20-0.35 | 260 | +126 | 77% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 869 | +205 | 80% |
| Side | yes | 652 | +101 | 80% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 119 | -6 | 92% |
| Quarter | 2025-Q3 | 59 | -31 | 85% |
| Quarter | 2025-Q4 | 38 | -3 | 82% |
| Quarter | 2026-Q1 | 33 | +25 | 97% |
| Quarter | 2026-Q2 | 178 | +34 | 91% |
| Quarter | 2026-Q3 | 229 | +138 | 94% |
| Quarter | 2026-Q4 | 125 | +40 | 93% |
| Price paid | 0.50-0.70 | 10 | +8 | 60% |
| Price paid | 0.70-0.90 | 185 | +140 | 91% |
| Price paid | 0.90-1.01 | 586 | +49 | 92% |
| Model vs market gap | 0.00-0.05 | 436 | +158 | 94% |
| Model vs market gap | 0.05-0.10 | 308 | -8 | 88% |
| Model vs market gap | 0.10-0.20 | 37 | +47 | 92% |
| Side | no | 306 | +131 | 94% |
| Side | yes | 475 | +65 | 90% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 269 | -27 | 77% |
| Quarter | 2025-Q3 | 128 | -48 | 77% |
| Quarter | 2026-Q1 | 52 | +90 | 90% |
| Quarter | 2026-Q2 | 48 | +70 | 90% |
| Quarter | 2026-Q3 | 77 | +58 | 86% |
| Quarter | 2026-Q4 | 37 | +34 | 86% |
| Price paid | 0.30-0.50 | 2 | +1 | 50% |
| Price paid | 0.50-0.70 | 64 | +53 | 73% |
| Price paid | 0.70-0.90 | 542 | +143 | 82% |
| Price paid | 0.90-1.01 | 3 | -19 | 33% |
| Model vs market gap | 0.05-0.10 | 10 | -7 | 80% |
| Model vs market gap | 0.10-0.20 | 434 | +38 | 81% |
| Model vs market gap | 0.20-0.35 | 165 | +132 | 81% |
| Model vs market gap | 0.35-1.01 | 2 | +15 | 100% |
| Side | no | 329 | +179 | 83% |
| Side | yes | 282 | -1 | 79% |

## Weather: daily highs: late entries

2695 events, 2025-03-18 to 2026-11-08.

**Verdict:** Bayes price-level, 95% sure: +37 on 181 trades (+2.1% per $ staked, t=1.02), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Late long-shot fade 1-4c | 966 | 99% | +48.25 | +0.5% | -7 | +55 | – | – | 0.0084 |
| Bayes price-level, 95% sure | 181 | 93% | +36.88 | +2.1% | +26 | +11 | 94% | 0.0668 | 0.0672 |
| Combined: 3+ strategies agree | 700 | 81% | +36.79 | +0.5% | +64 | -27 | 93% | 0.0587 | 0.1452 |
| Late favorite 90-97c | 819 | 95% | +7.03 | +0.1% | -5 | +12 | – | – | 0.0489 |
| Bayes price-level, 99% sure | 49 | 92% | +6.47 | +1.3% | -8 | +15 | 94% | 0.076 | 0.0753 |
| Late long-shot fade | 736 | 95% | -14.72 | -0.2% | -37 | +22 | – | – | 0.0441 |
| Combined: rolling best (past 6 months) | 541 | 97% | -40.54 | -0.8% | -66 | +26 | – | – | 0.0282 |
| Late favorite 80-90c | 436 | 86% | -52.38 | -1.2% | +9 | -61 | – | – | 0.123 |
| Combined: 5+ strategies agree | 436 | 86% | -52.38 | -1.2% | +9 | -61 | – | – | 0.123 |
| Late fav 80-90c, stop loss 25c | 436 | 82% | -88.31 | -2.1% | -18 | -70 | – | – | 0.1466 |
| Late fav 80-90c, stop loss 10c | 436 | 78% | -99.58 | -2.3% | -18 | -81 | – | – | 0.1736 |
| Late fav 80-90c, take profit 15c / stop 15c | 436 | 80% | -118.66 | -2.8% | -37 | -81 | – | – | 0.1593 |
| Late fav 80-90c, take profit 10c | 436 | 86% | -123.21 | -2.9% | -20 | -103 | – | – | 0.1218 |
| Late favorite 50-80c | 546 | 67% | -177.08 | -3.3% | -107 | -70 | – | – | 0.2139 |
| Heavy-volume move (10c, 5x): follow | 847 | 71% | -500.49 | -6.0% | -401 | -100 | – | – | 0.1666 |
| Heavy-volume move: follow | 1315 | 69% | -536.67 | -4.1% | -514 | -23 | – | – | 0.1693 |
| Heavy-volume move (10c, 5x): fade | 1011 | 25% | -2179.54 | -20.8% | -865 | -1314 | – | – | 0.1497 |
| Heavy-volume move: fade | 1587 | 26% | -3614.68 | -22.0% | -2131 | -1484 | – | – | 0.1503 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Combined: 3+ strategies agree | 221 | +17.87 | +0.8% |
| Late long-shot fade 1-4c | 381 | +8.42 | +0.2% |
| Bayes price-level, 99% sure | 5 | +5.15 | +10.3% |
| Bayes price-level, 95% sure | 44 | +0.83 | +0.2% |
| Late favorite 90-97c | 343 | -10.04 | -0.3% |
| Late favorite 80-90c | 159 | -14.09 | -0.9% |
| Combined: 5+ strategies agree | 159 | -14.09 | -0.9% |
| Late fav 80-90c, take profit 10c | 159 | -28.38 | -1.8% |
| Late fav 80-90c, stop loss 25c | 159 | -43.77 | -2.8% |
| Late fav 80-90c, stop loss 10c | 159 | -46.40 | -3.0% |
| Late long-shot fade | 237 | -53.63 | -2.4% |
| Late fav 80-90c, take profit 15c / stop 15c | 159 | -53.98 | -3.5% |
| Combined: rolling best (past 6 months) | 198 | -73.11 | -3.8% |
| Late favorite 50-80c | 169 | -113.02 | -6.8% |
| Heavy-volume move (10c, 5x): follow | 246 | -208.28 | -8.6% |
| Heavy-volume move: follow | 378 | -325.82 | -8.7% |
| Heavy-volume move (10c, 5x): fade | 325 | -861.09 | -25.5% |
| Heavy-volume move: fade | 512 | -1428.41 | -26.9% |

Rolling best: which strategy it picked each quarter

| Quarter | Picked | Past t |
|---|---|---|
| 2025-Q1 | sat out | – |
| 2025-Q2 | sat out | – |
| 2025-Q3 | Late long-shot fade 1-4c | 25.9 |
| 2025-Q4 | Late long-shot fade 1-4c | 29.08 |
| 2026-Q1 | Late long-shot fade | 0.17 |
| 2026-Q2 | sat out | – |
| 2026-Q3 | Late long-shot fade 1-4c | 1.41 |
| 2026-Q4 | Late long-shot fade 1-4c | 1.81 |

Why: Late favorite 80-90c

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 9 | +2 | 89% |
| Quarter | 2025-Q2 | 44 | +5 | 89% |
| Quarter | 2025-Q3 | 34 | -8 | 85% |
| Quarter | 2025-Q4 | 22 | -11 | 82% |
| Quarter | 2026-Q1 | 78 | -4 | 86% |
| Quarter | 2026-Q2 | 105 | +2 | 87% |
| Quarter | 2026-Q3 | 104 | -30 | 84% |
| Quarter | 2026-Q4 | 40 | -8 | 85% |
| Price paid | 0.70-0.90 | 382 | -64 | 85% |
| Price paid | 0.90-1.01 | 54 | +12 | 93% |
| Model vs market gap | no model | 436 | -52 | 86% |
| Side | yes | 436 | -52 | 86% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 10 | -1 | 90% |
| Quarter | 2025-Q3 | 18 | -15 | 83% |
| Quarter | 2025-Q4 | 2 | +2 | 100% |
| Quarter | 2026-Q1 | 20 | +21 | 100% |
| Quarter | 2026-Q2 | 61 | -3 | 90% |
| Quarter | 2026-Q3 | 51 | +27 | 96% |
| Quarter | 2026-Q4 | 19 | +7 | 95% |
| Price paid | 0.70-0.90 | 10 | -18 | 70% |
| Price paid | 0.90-1.01 | 171 | +54 | 94% |
| Model vs market gap | 0.00-0.05 | 73 | +13 | 93% |
| Model vs market gap | 0.05-0.10 | 100 | +36 | 94% |
| Model vs market gap | 0.10-0.20 | 8 | -13 | 75% |
| Side | no | 81 | +18 | 93% |
| Side | yes | 100 | +19 | 93% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 47 | +5 | 100% |
| Quarter | 2025-Q4 | 38 | -25 | 92% |
| Quarter | 2026-Q1 | 172 | -48 | 93% |
| Quarter | 2026-Q3 | 216 | +19 | 100% |
| Quarter | 2026-Q4 | 68 | +9 | 100% |
| Price paid | 0.90-1.01 | 541 | -41 | 97% |
| Model vs market gap | no model | 541 | -41 | 97% |
| Side | no | 541 | -41 | 97% |

## Weather: daily lows: late entries

1793 events, 2025-12-13 to 2026-11-08.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Heavy-volume move: fade (+107 on 716 trades).

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Heavy-volume move: fade | 716 | 34% | +107.35 | +1.5% | +501 | -393 | – | – | 0.1598 |
| Bayes price-level, 99% sure | 17 | 65% | +86.25 | +49.4% | +58 | +28 | 60% | 0.2366 | 0.2998 |
| Bayes price-level, 95% sure | 101 | 67% | -51.84 | -5.1% | -131 | +79 | 77% | 0.1778 | 0.1786 |
| Late favorite 90-97c | 871 | 94% | -69.01 | -0.8% | -48 | -21 | – | – | 0.0535 |
| Heavy-volume move (10c, 5x): fade | 317 | 28% | -199.42 | -6.1% | +155 | -355 | – | – | 0.1506 |
| Late favorite 80-90c | 358 | 82% | -216.55 | -6.2% | -96 | -121 | – | – | 0.1486 |
| Combined: 5+ strategies agree | 358 | 82% | -216.55 | -6.2% | -96 | -121 | – | – | 0.1486 |
| Late long-shot fade 1-4c | 1808 | 98% | -217.99 | -1.2% | -129 | -89 | – | – | 0.0248 |
| Late fav 80-90c, take profit 10c | 358 | 82% | -261.70 | -7.5% | -118 | -144 | – | – | 0.1466 |
| Combined: 3+ strategies agree | 414 | 79% | -287.44 | -7.1% | -163 | -124 | 55% | 0.1985 | 0.163 |
| Heavy-volume move (10c, 5x): follow | 235 | 66% | -297.48 | -12.8% | -179 | -119 | – | – | 0.1696 |
| Combined: rolling best (past 6 months) | 298 | 30% | -308.45 | -10.0% | -454 | +146 | – | – | 0.1477 |
| Late long-shot fade | 1335 | 93% | -357.62 | -2.8% | -279 | -79 | – | – | 0.0634 |
| Late fav 80-90c, stop loss 25c | 358 | 62% | -409.31 | -11.7% | -228 | -182 | – | – | 0.2879 |
| Late fav 80-90c, stop loss 10c | 358 | 40% | -424.56 | -12.1% | -243 | -182 | – | – | 0.4366 |
| Late fav 80-90c, take profit 15c / stop 15c | 358 | 48% | -433.27 | -12.4% | -241 | -192 | – | – | 0.3763 |
| Late favorite 50-80c | 412 | 59% | -551.67 | -13.6% | -201 | -350 | – | – | 0.2361 |
| Heavy-volume move: follow | 559 | 58% | -1157.64 | -20.8% | -539 | -618 | – | – | 0.1736 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Heavy-volume move: fade | 144 | +157.10 | +10.6% |
| Bayes price-level, 99% sure | 0 | +0.00 | – |
| Combined: rolling best (past 6 months) | 0 | +0.00 | – |
| Late favorite 50-80c | 64 | -6.89 | -1.1% |
| Bayes price-level, 95% sure | 24 | -11.52 | -5.0% |
| Late favorite 90-97c | 164 | -31.19 | -2.0% |
| Late long-shot fade 1-4c | 363 | -37.08 | -1.0% |
| Late favorite 80-90c | 58 | -59.55 | -10.5% |
| Combined: 5+ strategies agree | 58 | -59.55 | -10.5% |
| Combined: 3+ strategies agree | 67 | -61.72 | -9.5% |
| Late fav 80-90c, take profit 10c | 58 | -70.59 | -12.5% |
| Heavy-volume move (10c, 5x): follow | 42 | -82.86 | -19.9% |
| Late fav 80-90c, take profit 15c / stop 15c | 58 | -103.31 | -18.3% |
| Late fav 80-90c, stop loss 25c | 58 | -105.82 | -18.7% |
| Late long-shot fade | 258 | -108.97 | -4.4% |
| Late fav 80-90c, stop loss 10c | 58 | -114.36 | -20.3% |
| Heavy-volume move (10c, 5x): fade | 60 | -131.84 | -21.1% |
| Heavy-volume move: follow | 107 | -310.34 | -29.1% |

Rolling best: which strategy it picked each quarter

| Quarter | Picked | Past t |
|---|---|---|
| 2025-Q4 | sat out | – |
| 2026-Q1 | sat out | – |
| 2026-Q2 | sat out | – |
| 2026-Q3 | Heavy-volume move: fade | 0.91 |
| 2026-Q4 | Heavy-volume move: fade | 0.92 |

Why: Late favorite 80-90c

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q4 | 3 | -7 | 67% |
| Quarter | 2026-Q1 | 73 | -36 | 82% |
| Quarter | 2026-Q2 | 102 | -43 | 83% |
| Quarter | 2026-Q3 | 145 | -111 | 81% |
| Quarter | 2026-Q4 | 35 | -20 | 83% |
| Price paid | 0.70-0.90 | 318 | -203 | 81% |
| Price paid | 0.90-1.01 | 40 | -14 | 88% |
| Model vs market gap | no model | 358 | -217 | 82% |
| Side | yes | 358 | -217 | 82% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q1 | 24 | -12 | 92% |
| Quarter | 2026-Q2 | 14 | -145 | 0% |
| Quarter | 2026-Q3 | 54 | +76 | 72% |
| Quarter | 2026-Q4 | 9 | +29 | 78% |
| Price paid | 0.10-0.30 | 7 | -74 | 0% |
| Price paid | 0.30-0.50 | 30 | +91 | 57% |
| Price paid | 0.50-0.70 | 7 | -4 | 57% |
| Price paid | 0.70-0.90 | 3 | -30 | 0% |
| Price paid | 0.90-1.01 | 54 | -36 | 87% |
| Model vs market gap | 0.00-0.05 | 29 | -22 | 86% |
| Model vs market gap | 0.05-0.10 | 31 | -76 | 71% |
| Model vs market gap | 0.10-0.20 | 27 | -24 | 44% |
| Model vs market gap | 0.20-0.35 | 14 | +70 | 64% |
| Side | no | 78 | +60 | 73% |
| Side | yes | 23 | -112 | 48% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2026-Q3 | 224 | -257 | 31% |
| Quarter | 2026-Q4 | 74 | -52 | 27% |
| Price paid | 0.10-0.30 | 207 | -490 | 14% |
| Price paid | 0.30-0.50 | 47 | +142 | 53% |
| Price paid | 0.50-0.70 | 18 | +31 | 72% |
| Price paid | 0.70-0.90 | 23 | +6 | 83% |
| Price paid | 0.90-1.01 | 3 | +3 | 100% |
| Model vs market gap | no model | 298 | -308 | 30% |
| Side | no | 187 | -189 | 34% |
| Side | yes | 111 | -120 | 23% |

## Bitcoin: last 1-3 hours

599 events, 2025-03-19 to 2026-11-08.

**Verdict:** Late long-shot fade 1-4c: +87 on 868 trades (+1.0% per $ staked, t=6.15), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Bayes price-level, 95% sure | 841 | 92% | +322.31 | +4.0% | +69 | +253 | 93% | 0.0748 | 0.0771 |
| Bayes price-level, 99% sure | 407 | 93% | +212.88 | +5.4% | +144 | +69 | 94% | 0.0644 | 0.069 |
| Combined: rolling best (past 6 months) | 758 | 96% | +162.40 | +2.2% | +23 | +139 | 93% | 0.0694 | 0.0332 |
| Late long-shot fade | 732 | 97% | +101.47 | +1.5% | +40 | +61 | – | – | 0.0288 |
| Combined: 3+ strategies agree | 250 | 89% | +92.92 | +3.8% | -13 | +106 | 91% | 0.0919 | 0.0973 |
| Late long-shot fade 1-4c | 868 | 100% | +87.37 | +1.0% | +36 | +52 | – | – | 0.0026 |
| Late favorite 90-97c | 201 | 97% | +32.15 | +1.7% | +28 | +4 | – | – | 0.0303 |
| Late favorite 50-80c | 32 | 69% | +1.97 | +0.6% | -29 | +31 | – | – | 0.2165 |
| Late favorite 80-90c | 46 | 87% | -1.96 | -0.4% | -1 | -1 | – | – | 0.116 |
| Combined: 5+ strategies agree | 46 | 87% | -1.96 | -0.4% | -1 | -1 | – | – | 0.116 |
| Late fav 80-90c, take profit 10c | 46 | 87% | -3.23 | -0.7% | -1 | -2 | – | – | 0.116 |
| Late fav 80-90c, stop loss 25c | 46 | 74% | -31.47 | -7.0% | -34 | +3 | – | – | 0.2045 |
| Late fav 80-90c, stop loss 10c | 46 | 59% | -48.81 | -10.8% | -49 | +1 | – | – | 0.3001 |
| Late fav 80-90c, take profit 15c / stop 15c | 46 | 63% | -50.59 | -11.2% | -49 | -2 | – | – | 0.2749 |
| Heavy-volume move (10c, 5x): follow | 788 | 66% | -651.22 | -8.4% | -335 | -316 | – | – | 0.1776 |
| Heavy-volume move: follow | 1294 | 66% | -987.87 | -7.7% | -620 | -368 | – | – | 0.1693 |
| Heavy-volume move (10c, 5x): fade | 857 | 31% | -1754.26 | -19.9% | -1121 | -633 | – | – | 0.1659 |
| Heavy-volume move: fade | 1377 | 30% | -3550.69 | -25.0% | -2061 | -1490 | – | – | 0.1544 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Late favorite 90-97c | 170 | +39.01 | +2.4% |
| Bayes price-level, 99% sure | 22 | +19.60 | +9.0% |
| Late long-shot fade 1-4c | 156 | +19.08 | +1.2% |
| Late long-shot fade | 238 | +17.95 | +0.8% |
| Combined: rolling best (past 6 months) | 159 | +13.07 | +0.8% |
| Late favorite 80-90c | 41 | -8.95 | -2.2% |
| Combined: 5+ strategies agree | 41 | -8.95 | -2.2% |
| Late fav 80-90c, take profit 10c | 41 | -10.22 | -2.5% |
| Late favorite 50-80c | 28 | -12.99 | -4.7% |
| Bayes price-level, 95% sure | 168 | -37.84 | -2.3% |
| Late fav 80-90c, stop loss 25c | 41 | -38.46 | -9.6% |
| Combined: 3+ strategies agree | 81 | -44.06 | -5.5% |
| Late fav 80-90c, stop loss 10c | 41 | -55.80 | -13.9% |
| Late fav 80-90c, take profit 15c / stop 15c | 41 | -57.58 | -14.3% |
| Heavy-volume move (10c, 5x): follow | 380 | -328.78 | -8.8% |
| Heavy-volume move: follow | 576 | -567.84 | -9.9% |
| Heavy-volume move (10c, 5x): fade | 427 | -1110.90 | -25.3% |
| Heavy-volume move: fade | 638 | -1900.83 | -29.0% |

Rolling best: which strategy it picked each quarter

| Quarter | Picked | Past t |
|---|---|---|
| 2025-Q1 | sat out | – |
| 2025-Q2 | sat out | – |
| 2025-Q3 | Late long-shot fade | 20.62 |
| 2025-Q4 | Late long-shot fade 1-4c | 14.93 |
| 2026-Q1 | Late long-shot fade 1-4c | 19.74 |
| 2026-Q2 | Late long-shot fade 1-4c | 26.72 |
| 2026-Q3 | Bayes price-level, 99% sure | 2.21 |
| 2026-Q4 | Bayes price-level, 95% sure | 5.42 |

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
| Quarter | 2025-Q1 | 6 | +1 | 100% |
| Quarter | 2025-Q2 | 10 | +1 | 100% |
| Quarter | 2025-Q3 | 31 | +4 | 100% |
| Quarter | 2025-Q4 | 29 | +3 | 100% |
| Quarter | 2026-Q1 | 127 | +17 | 100% |
| Quarter | 2026-Q2 | 260 | +14 | 99% |
| Quarter | 2026-Q3 | 281 | +33 | 100% |
| Quarter | 2026-Q4 | 124 | +14 | 100% |
| Price paid | 0.90-1.01 | 868 | +87 | 100% |
| Model vs market gap | no model | 868 | +87 | 100% |
| Side | no | 868 | +87 | 100% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 16 | -6 | 88% |
| Quarter | 2025-Q3 | 36 | +6 | 89% |
| Quarter | 2025-Q4 | 54 | -21 | 83% |
| Quarter | 2026-Q1 | 103 | +18 | 91% |
| Quarter | 2026-Q2 | 247 | +92 | 92% |
| Quarter | 2026-Q3 | 258 | +260 | 96% |
| Quarter | 2026-Q4 | 127 | -25 | 87% |
| Price paid | 0.50-0.70 | 10 | +15 | 70% |
| Price paid | 0.70-0.90 | 396 | +189 | 88% |
| Price paid | 0.90-1.01 | 435 | +118 | 96% |
| Model vs market gap | 0.00-0.05 | 269 | +116 | 98% |
| Model vs market gap | 0.05-0.10 | 490 | +173 | 89% |
| Model vs market gap | 0.10-0.20 | 82 | +34 | 85% |
| Side | no | 218 | +98 | 93% |
| Side | yes | 623 | +225 | 91% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 50 | -0 | 96% |
| Quarter | 2025-Q4 | 29 | +3 | 100% |
| Quarter | 2026-Q1 | 127 | +17 | 100% |
| Quarter | 2026-Q2 | 260 | +14 | 99% |
| Quarter | 2026-Q3 | 165 | +154 | 96% |
| Quarter | 2026-Q4 | 127 | -25 | 87% |
| Price paid | 0.50-0.70 | 4 | -10 | 50% |
| Price paid | 0.70-0.90 | 136 | +70 | 88% |
| Price paid | 0.90-1.01 | 618 | +103 | 98% |
| Model vs market gap | 0.00-0.05 | 95 | +47 | 98% |
| Model vs market gap | 0.05-0.10 | 183 | +67 | 90% |
| Model vs market gap | 0.10-0.20 | 14 | +16 | 86% |
| Model vs market gap | no model | 466 | +33 | 99% |
| Side | no | 554 | +98 | 99% |
| Side | yes | 204 | +65 | 91% |

## Ethereum

594 events, 2025-03-24 to 2026-11-08.

**Verdict:** Market favorite (no model): +127 on 114 trades (+11.1% per $ staked, t=1.43), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Time-of-day vol x0.5, skip spikes | 783 | 82% | +149.25 | +2.0% | -58 | +207 | 92% | 0.1536 | 0.1443 |
| Time-of-day vol x0.5, against trend + skip spikes | 430 | 84% | +148.01 | +3.5% | -29 | +177 | 93% | 0.1428 | 0.1369 |
| Market favorite (no model) | 114 | 68% | +126.64 | +11.1% | +91 | +36 | – | – | 0.2027 |
| Vol x0.5, weekends only | 149 | 83% | +71.91 | +5.0% | +1 | +70 | 92% | 0.1315 | 0.1263 |
| Time-of-day vol x0.5 | 1226 | 81% | +42.72 | +0.4% | -159 | +202 | 92% | 0.1632 | 0.1496 |
| Vol x0.5, skip spiked markets | 915 | 80% | +36.49 | +0.4% | -211 | +247 | 93% | 0.1743 | 0.1582 |
| Bayes price-level, 95% sure | 89 | 79% | +25.96 | +3.0% | -8 | +34 | 84% | 0.1741 | 0.1779 |
| Vol x0.5, against trend + skip spikes | 495 | 80% | +12.81 | +0.3% | -146 | +159 | 93% | 0.1763 | 0.1595 |
| Bayes: market prior + fat-tail | 1 | 100% | +2.38 | +24.7% | +0 | +2 | 90% | 0.009 | 0.065 |
| Bayes: market prior + full vol | 0 | – | +0.00 | – | +0 | +0 | – | – | – |
| Bayes price-level, 99% sure | 12 | 75% | -1.22 | -1.0% | +11 | -12 | 83% | 0.1594 | 0.1512 |
| Long-shot fade (no model) | 597 | 95% | -26.51 | -0.5% | -93 | +66 | – | – | 0.0452 |
| Combined: rolling best (past 6 months) | 261 | 78% | -39.72 | -1.6% | -97 | +57 | 93% | 0.1686 | 0.1567 |
| Vol x0.5, news days only | 81 | 74% | -53.01 | -6.7% | -22 | -31 | 92% | 0.2085 | 0.1774 |
| Fat-tail (actual past moves) | 335 | 66% | -79.37 | -2.4% | -209 | +130 | 78% | 0.1935 | 0.1777 |
| Vol x0.5, against the 24h trend | 693 | 78% | -83.69 | -1.2% | -266 | +182 | 92% | 0.1855 | 0.1652 |
| Vol x0.75 | 394 | 76% | -92.34 | -2.4% | -179 | +87 | 88% | 0.1684 | 0.1532 |
| Vol x0.5, calm market only | 754 | 78% | -101.14 | -1.4% | -227 | +126 | 92% | 0.1804 | 0.1617 |
| Vol x0.5, 5c edge | 1689 | 79% | -118.64 | -0.7% | -388 | +270 | 91% | 0.1773 | 0.1595 |
| Vol x0.5, busy market only | 660 | 77% | -147.83 | -2.3% | -156 | +8 | 93% | 0.1956 | 0.1694 |
| Vol x0.5, with the 24h trend | 721 | 78% | -165.28 | -2.4% | -129 | -37 | 92% | 0.1895 | 0.1654 |
| Regime-scaled vol x0.5 | 1578 | 79% | -184.73 | -1.2% | -323 | +138 | 93% | 0.1822 | 0.1609 |
| Vol x0.5, skip news days | 1333 | 78% | -195.96 | -1.5% | -329 | +133 | 92% | 0.1863 | 0.1646 |
| Full vol + 50% market blend | 97 | 23% | -223.31 | -22.1% | -341 | +117 | 34% | 0.1203 | 0.1089 |
| Fat-tail, moves x0.75 | 864 | 73% | -227.97 | -2.7% | -251 | +23 | 86% | 0.2077 | 0.1889 |
| Vol x0.5, NO only | 893 | 78% | -229.95 | -2.6% | -238 | +8 | 92% | 0.1859 | 0.1638 |
| Vol x0.5, skip news in window | 1391 | 78% | -244.13 | -1.8% | -382 | +138 | 92% | 0.188 | 0.1656 |
| Vol x0.5 (Bitcoin's winner) | 1414 | 78% | -248.97 | -1.8% | -407 | +158 | 92% | 0.1875 | 0.1653 |
| Vol x0.5, weekdays only | 1265 | 77% | -320.88 | -2.6% | -381 | +60 | 93% | 0.1941 | 0.1699 |
| Fat-tail, moves x0.5 | 1693 | 74% | -382.57 | -2.3% | -386 | +3 | 90% | 0.2097 | 0.1831 |
| Options vol x0.85, 5c gap | 429 | 56% | -427.67 | -9.9% | -571 | +144 | 66% | 0.1357 | 0.1209 |
| Heavy-volume move (10c, 5x): follow | 406 | 60% | -506.20 | -12.5% | -259 | -247 | – | – | 0.1828 |
| Options vol, NO only | 216 | 27% | -525.43 | -23.5% | -595 | +70 | 42% | 0.1231 | 0.0982 |
| Options vol, 8c gap | 199 | 17% | -581.15 | -28.0% | -715 | +134 | 36% | 0.1287 | 0.0927 |
| Vol x0.5, take profit 10c | 1414 | 81% | -639.41 | -4.6% | -591 | -48 | 92% | 0.1673 | 0.1546 |
| Combined: 5+ strategies agree | 1685 | 74% | -725.83 | -4.4% | -722 | -4 | 87% | 0.1785 | 0.1606 |
| Vol x0.5, stop loss 25c | 1414 | 64% | -770.63 | -5.6% | -767 | -4 | 92% | 0.3063 | 0.2381 |
| Heavy-volume move (10c, 5x): fade | 456 | 35% | -855.75 | -18.3% | -232 | -624 | – | – | 0.1655 |
| Full vol (v1 rule) | 216 | 28% | -872.28 | -39.2% | -714 | -158 | 46% | 0.1198 | 0.0887 |
| Heavy-volume move: follow | 744 | 57% | -979.87 | -13.2% | -470 | -510 | – | – | 0.1872 |
| Vol x0.5, take profit 15c / stop 15c | 1414 | 57% | -1020.11 | -7.4% | -849 | -171 | 92% | 0.3724 | 0.2817 |
| Heavy-volume move: fade | 807 | 38% | -1046.17 | -12.7% | -312 | -734 | – | – | 0.1734 |
| Vol x0.5, stop loss 10c | 1414 | 47% | -1119.11 | -8.1% | -943 | -176 | 92% | 0.4558 | 0.3317 |
| Options vol, 5c gap | 388 | 22% | -1488.01 | -37.0% | -1224 | -264 | 39% | 0.1177 | 0.0907 |
| Vol x0.5, limit order | 713 | 57% | -1704.34 | -24.8% | -1094 | -610 | 92% | 0.3593 | 0.2694 |
| Vol x0.5, limit order (strict fill) | 692 | 56% | -1756.42 | -26.3% | -1120 | -636 | 92% | 0.37 | 0.2764 |
| Combined: 3+ strategies agree | 2402 | 66% | -1890.57 | -7.9% | -1324 | -566 | 84% | 0.1728 | 0.1583 |
| Vol x0.5 5c edge, limit order | 833 | 58% | -1892.10 | -23.5% | -1221 | -671 | 91% | 0.3442 | 0.2626 |
| Kalshi price-spike fade (no model) | 1049 | 30% | -2292.35 | -21.2% | -924 | -1368 | – | – | 0.1704 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Market favorite (no model) | 64 | +89.35 | +13.9% |
| Bayes price-level, 99% sure | 5 | +5.15 | +10.3% |
| Bayes: market prior + fat-tail | 1 | +2.38 | +24.7% |
| Bayes: market prior + full vol | 0 | +0.00 | – |
| Time-of-day vol x0.5, against trend + skip spikes | 259 | -8.24 | -0.3% |
| Bayes price-level, 95% sure | 44 | -8.34 | -2.0% |
| Vol x0.5, weekends only | 102 | -11.15 | -1.1% |
| Vol x0.5, news days only | 25 | -13.39 | -5.5% |
| Time-of-day vol x0.5, skip spikes | 469 | -55.12 | -1.2% |
| Long-shot fade (no model) | 307 | -88.63 | -3.0% |
| Combined: rolling best (past 6 months) | 159 | -95.16 | -6.1% |
| Time-of-day vol x0.5 | 747 | -127.98 | -1.8% |
| Vol x0.5, with the 24h trend | 472 | -129.90 | -2.8% |
| Vol x0.5, against trend + skip spikes | 311 | -143.61 | -4.7% |
| Vol x0.75 | 255 | -161.63 | -6.5% |
| Vol x0.5, skip spiked markets | 575 | -185.90 | -3.3% |
| Vol x0.5, busy market only | 452 | -186.03 | -4.2% |
| Fat-tail (actual past moves) | 204 | -196.89 | -9.8% |
| Full vol + 50% market blend | 33 | -208.07 | -61.7% |
| Fat-tail, moves x0.75 | 567 | -238.03 | -4.3% |
| Vol x0.5, calm market only | 453 | -242.35 | -5.5% |
| Vol x0.5, against the 24h trend | 433 | -298.48 | -7.1% |
| Vol x0.5, NO only | 614 | -322.81 | -5.4% |
| Heavy-volume move (10c, 5x): follow | 254 | -351.52 | -13.9% |
| Regime-scaled vol x0.5 | 1015 | -354.69 | -3.6% |
| Vol x0.5, 5c edge | 1087 | -373.06 | -3.5% |
| Fat-tail, moves x0.5 | 1071 | -407.95 | -3.9% |
| Vol x0.5, skip news days | 880 | -414.99 | -4.8% |
| Vol x0.5, weekdays only | 803 | -417.23 | -5.3% |
| Heavy-volume move (10c, 5x): fade | 291 | -418.59 | -14.0% |
| Vol x0.5 (Bitcoin's winner) | 905 | -428.38 | -4.9% |
| Vol x0.5, skip news in window | 901 | -441.44 | -5.0% |
| Heavy-volume move: fade | 476 | -475.33 | -9.7% |
| Heavy-volume move: follow | 431 | -519.02 | -12.1% |
| Options vol, NO only | 101 | -521.70 | -50.6% |
| Options vol, 8c gap | 79 | -568.57 | -69.8% |
| Options vol x0.85, 5c gap | 245 | -594.43 | -24.5% |
| Vol x0.5, take profit 10c | 905 | -677.61 | -7.7% |
| Full vol (v1 rule) | 105 | -682.19 | -63.4% |
| Combined: 5+ strategies agree | 1043 | -813.59 | -8.0% |
| Vol x0.5, stop loss 25c | 905 | -849.10 | -9.6% |
| Vol x0.5, take profit 15c / stop 15c | 905 | -985.89 | -11.2% |
| Vol x0.5, stop loss 10c | 905 | -1051.06 | -11.9% |
| Options vol, 5c gap | 170 | -1092.46 | -62.5% |
| Vol x0.5, limit order | 450 | -1324.38 | -30.5% |
| Vol x0.5, limit order (strict fill) | 436 | -1358.44 | -32.3% |
| Kalshi price-spike fade (no model) | 684 | -1370.22 | -19.4% |
| Vol x0.5 5c edge, limit order | 526 | -1456.81 | -28.7% |
| Combined: 3+ strategies agree | 1497 | -1651.57 | -11.2% |

Sweep: vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.3 | 2005 | -124.66 | -0.6% |
| 0.4 | 1771 | -318.19 | -1.8% |
| 0.5 | 1414 | -248.97 | -1.8% |
| 0.6 | 951 | -290.21 | -3.1% |
| 0.75 | 394 | -92.34 | -2.4% |
| 1.0 | 216 | -872.28 | -39.2% |

Sweep: time-of-day vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1681 | -54.04 | -0.3% |
| 0.5 | 1226 | +42.72 | +0.4% |
| 0.6 | 689 | -148.94 | -2.2% |
| 0.75 | 231 | -301.26 | -13.2% |
| 1.0 | 243 | -982.81 | -38.8% |

Sweep: fat-tail

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 1949 | -170.70 | -0.9% |
| 0.5 | 1693 | -382.57 | -2.3% |
| 0.6 | 1357 | -177.53 | -1.3% |
| 0.75 | 864 | -227.97 | -2.7% |
| 0.9 | 488 | -254.62 | -5.3% |
| 1.0 | 335 | -79.37 | -2.4% |

Sweep: options vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 1336 | -423.21 | -3.2% |
| 0.7 | 866 | -402.93 | -4.7% |
| 0.8 | 519 | -451.06 | -8.8% |
| 0.9 | 371 | -673.10 | -17.8% |
| 1.0 | 388 | -1488.01 | -37.0% |
| 1.1 | 525 | -2862.73 | -52.1% |

Rolling best: which strategy it picked each quarter

| Quarter | Picked | Past t |
|---|---|---|
| 2025-Q1 | sat out | – |
| 2025-Q2 | sat out | – |
| 2025-Q3 | Time-of-day vol x0.5, against trend + skip spikes | 1.99 |
| 2025-Q4 | Time-of-day vol x0.5, against trend + skip spikes | 0.57 |
| 2026-Q1 | Bayes price-level, 95% sure | – |
| 2026-Q2 | Market favorite (no model) | 0.89 |
| 2026-Q3 | Time-of-day vol x0.5, against trend + skip spikes | 2.27 |
| 2026-Q4 | Time-of-day vol x0.5, against trend + skip spikes | 2.97 |

Why: Market favorite (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 2 | +11 | 100% |
| Quarter | 2025-Q2 | 19 | +32 | 68% |
| Quarter | 2025-Q3 | 12 | +34 | 83% |
| Quarter | 2025-Q4 | 15 | +6 | 60% |
| Quarter | 2026-Q1 | 21 | +51 | 67% |
| Quarter | 2026-Q2 | 26 | -16 | 62% |
| Quarter | 2026-Q3 | 13 | -9 | 62% |
| Quarter | 2026-Q4 | 6 | +17 | 83% |
| Price paid | 0.30-0.50 | 27 | +39 | 48% |
| Price paid | 0.50-0.70 | 59 | +3 | 63% |
| Price paid | 0.70-0.90 | 28 | +84 | 96% |
| Model vs market gap | no model | 114 | +127 | 68% |
| Side | yes | 114 | +127 | 68% |

Why: Kalshi price-spike fade (no model)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 7 | -26 | 29% |
| Quarter | 2025-Q2 | 109 | -38 | 34% |
| Quarter | 2025-Q3 | 206 | -419 | 29% |
| Quarter | 2025-Q4 | 222 | -468 | 28% |
| Quarter | 2026-Q1 | 173 | -536 | 28% |
| Quarter | 2026-Q2 | 129 | -151 | 36% |
| Quarter | 2026-Q3 | 147 | -445 | 32% |
| Quarter | 2026-Q4 | 56 | -210 | 29% |
| Price paid | 0.10-0.30 | 523 | -1978 | 13% |
| Price paid | 0.30-0.50 | 299 | -326 | 36% |
| Price paid | 0.50-0.70 | 175 | +20 | 60% |
| Price paid | 0.70-0.90 | 52 | -9 | 75% |
| Model vs market gap | no model | 1049 | -2292 | 30% |
| Side | no | 486 | -1267 | 33% |
| Side | yes | 563 | -1026 | 28% |

Why: Time-of-day vol x0.5, against trend + skip spikes

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 2 | +4 | 100% |
| Quarter | 2025-Q2 | 43 | +50 | 88% |
| Quarter | 2025-Q3 | 78 | -9 | 80% |
| Quarter | 2025-Q4 | 81 | -86 | 73% |
| Quarter | 2026-Q1 | 75 | +45 | 87% |
| Quarter | 2026-Q2 | 75 | +74 | 88% |
| Quarter | 2026-Q3 | 46 | +64 | 94% |
| Quarter | 2026-Q4 | 30 | +7 | 83% |
| Price paid | 0.50-0.70 | 34 | +61 | 79% |
| Price paid | 0.70-0.90 | 376 | +89 | 84% |
| Price paid | 0.90-1.01 | 20 | -1 | 90% |
| Model vs market gap | 0.05-0.10 | 7 | +8 | 100% |
| Model vs market gap | 0.10-0.20 | 385 | +143 | 84% |
| Model vs market gap | 0.20-0.35 | 37 | -8 | 73% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 211 | +133 | 87% |
| Side | yes | 219 | +15 | 81% |

Why: Time-of-day vol x0.5

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q1 | 7 | +5 | 86% |
| Quarter | 2025-Q2 | 110 | +16 | 82% |
| Quarter | 2025-Q3 | 219 | -65 | 78% |
| Quarter | 2025-Q4 | 247 | -129 | 76% |
| Quarter | 2026-Q1 | 222 | +73 | 84% |
| Quarter | 2026-Q2 | 207 | +39 | 81% |
| Quarter | 2026-Q3 | 122 | +97 | 88% |
| Quarter | 2026-Q4 | 92 | +7 | 80% |
| Price paid | 0.10-0.30 | 4 | -42 | 0% |
| Price paid | 0.50-0.70 | 134 | +29 | 69% |
| Price paid | 0.70-0.90 | 1046 | +34 | 82% |
| Price paid | 0.90-1.01 | 42 | +21 | 95% |
| Model vs market gap | 0.05-0.10 | 15 | -15 | 80% |
| Model vs market gap | 0.10-0.20 | 1083 | +92 | 82% |
| Model vs market gap | 0.20-0.35 | 127 | -39 | 72% |
| Model vs market gap | 0.35-1.01 | 1 | +4 | 100% |
| Side | no | 615 | -39 | 80% |
| Side | yes | 611 | +82 | 81% |

Why: Bayes price-level, 95% sure

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q2 | 13 | -10 | 85% |
| Quarter | 2025-Q3 | 19 | -2 | 90% |
| Quarter | 2025-Q4 | 12 | +3 | 75% |
| Quarter | 2026-Q2 | 12 | +23 | 75% |
| Quarter | 2026-Q3 | 17 | +25 | 76% |
| Quarter | 2026-Q4 | 16 | -13 | 69% |
| Price paid | 0.50-0.70 | 40 | +55 | 72% |
| Price paid | 0.70-0.90 | 8 | +18 | 100% |
| Price paid | 0.90-1.01 | 41 | -47 | 80% |
| Model vs market gap | 0.00-0.05 | 4 | -29 | 25% |
| Model vs market gap | 0.05-0.10 | 48 | -27 | 81% |
| Model vs market gap | 0.10-0.20 | 37 | +82 | 81% |
| Side | no | 8 | -1 | 62% |
| Side | yes | 81 | +27 | 80% |

Why: Combined: rolling best (past 6 months)

| Split | Group | Trades | P&L | Win % |
|---|---|---|---|---|
| Quarter | 2025-Q3 | 78 | -9 | 80% |
| Quarter | 2025-Q4 | 81 | -86 | 73% |
| Quarter | 2026-Q2 | 26 | -16 | 62% |
| Quarter | 2026-Q3 | 46 | +64 | 94% |
| Quarter | 2026-Q4 | 30 | +7 | 83% |
| Price paid | 0.30-0.50 | 3 | -5 | 33% |
| Price paid | 0.50-0.70 | 28 | -33 | 57% |
| Price paid | 0.70-0.90 | 216 | -5 | 81% |
| Price paid | 0.90-1.01 | 14 | +3 | 93% |
| Model vs market gap | 0.05-0.10 | 6 | +7 | 100% |
| Model vs market gap | 0.10-0.20 | 207 | -11 | 81% |
| Model vs market gap | 0.20-0.35 | 22 | -19 | 68% |
| Model vs market gap | no model | 26 | -16 | 62% |
| Side | no | 116 | +69 | 87% |
| Side | yes | 145 | -109 | 72% |
