# Backtest (2026-11-09)

Flat $10 per trade at the ask plus Kalshi fees, held to settlement. Prices are real hourly Kalshi quotes. Forecasts are archived NWS-blend (NBM) runs 1-2 days old. Bias/sigma learned only from earlier days.

## Weather: daily highs

1672 events, 2026-03-13 to 2026-11-07.

**Verdict:** No strategy made money in both halves with 30+ trades. Least bad: Market favorite YES (no model) (+68 on 2201 trades).

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Market favorite YES (no model) | 2201 | 53% | +68.10 | +0.3% | -51 | +119 | – | – | 0.2422 |
| Long-shot fade (no model) | 2755 | 95% | -74.96 | -0.3% | -87 | +12 | – | – | 0.0471 |
| Forecast bracket YES | 726 | 10% | -3493.55 | -45.7% | -1836 | -1658 | 33% | 0.145 | 0.088 |
| v2 + disagreement cap | 3192 | 33% | -8419.21 | -25.8% | -4308 | -4111 | 54% | 0.2014 | 0.1573 |
| v2 + 50% market blend | 3523 | 31% | -9136.90 | -25.2% | -4180 | -4957 | 46% | 0.1906 | 0.1645 |
| v1 (what we ran live) | 4370 | 34% | -9361.31 | -20.9% | -4298 | -5063 | 62% | 0.263 | 0.1645 |
| v2 calibrated | 3977 | 32% | -10325.89 | -25.3% | -4860 | -5466 | 58% | 0.2448 | 0.1669 |

Sweep: sigma

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 3955 | -9754.23 | -24.1% |
| 0.8 | 3812 | -9844.72 | -25.2% |
| 1.0 | 3977 | -10325.89 | -25.3% |
| 1.25 | 4236 | -8956.83 | -20.7% |
| 1.5 | 4380 | -7728.72 | -17.3% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 4855 | -11895.85 | -23.9% |
| blend 0.0, edge 0.05 | 4551 | -11334.67 | -24.3% |
| blend 0.0, edge 0.08 | 3977 | -10325.89 | -25.3% |
| blend 0.25, edge 0.03 | 4597 | -11400.67 | -24.2% |
| blend 0.25, edge 0.05 | 4112 | -10476.98 | -24.8% |
| blend 0.25, edge 0.08 | 3218 | -8791.93 | -26.6% |
| blend 0.5, edge 0.03 | 3954 | -10244.14 | -25.2% |
| blend 0.5, edge 0.05 | 3045 | -8204.67 | -26.2% |
| blend 0.5, edge 0.08 | 1830 | -4619.88 | -24.5% |
| blend 0.75, edge 0.03 | 1831 | -5418.17 | -28.7% |
| blend 0.75, edge 0.05 | 782 | -1970.05 | -24.3% |
| blend 0.75, edge 0.08 | 203 | -666.42 | -31.6% |

Forecast error (actual minus NBM forecast)

| City | Entry | n | Bias | RMSE |
|---|---|---|---|---|
| Austin | day before 10am | 238 | +1.87 | 3.3 |
| Austin | same day 8am | 240 | +1.57 | 2.94 |
| Chicago | day before 10am | 238 | +1.45 | 3.44 |
| Chicago | same day 8am | 236 | +1.27 | 2.86 |
| Denver | day before 10am | 239 | +1.75 | 3.42 |
| Denver | same day 8am | 236 | +1.68 | 2.98 |
| Los Angeles | day before 10am | 237 | +2.30 | 3.89 |
| Los Angeles | same day 8am | 239 | +2.31 | 3.63 |
| Miami | same day 8am | 239 | +2.05 | 2.67 |
| New York | same day 8am | 237 | -0.26 | 2.46 |
| Philadelphia | same day 8am | 237 | +1.74 | 2.89 |

## Weather: daily lows

1678 events, 2026-03-13 to 2026-11-07.

**Verdict:** No strategy made money in both halves with 30+ trades. Least bad: Long-shot fade (no model) (+140 on 2477 trades).

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Long-shot fade (no model) | 2477 | 96% | +139.98 | +0.6% | +178 | -39 | – | – | 0.0338 |
| Market favorite YES (no model) | 1733 | 47% | -883.86 | -5.0% | -145 | -739 | – | – | 0.2378 |
| Forecast bracket YES | 537 | 14% | -1657.51 | -29.5% | -945 | -713 | 34% | 0.1623 | 0.1218 |
| v2 + 50% market blend | 1828 | 29% | -3909.24 | -20.7% | -1162 | -2747 | 41% | 0.1565 | 0.1412 |
| v2 calibrated | 2531 | 31% | -5637.22 | -21.7% | -1585 | -4052 | 52% | 0.2009 | 0.1499 |
| v2 + disagreement cap | 2198 | 31% | -6196.67 | -27.5% | -2188 | -4009 | 50% | 0.1778 | 0.1424 |
| v1 (what we ran live) | 3741 | 32% | -10462.59 | -27.2% | -4428 | -6035 | 57% | 0.2259 | 0.1472 |

Sweep: sigma

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 3287 | -5361.25 | -16.0% |
| 0.8 | 2607 | -5173.00 | -19.4% |
| 1.0 | 2531 | -5637.22 | -21.7% |
| 1.25 | 2965 | -6727.67 | -22.1% |
| 1.5 | 3477 | -8617.05 | -24.2% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 3917 | -9279.63 | -23.1% |
| blend 0.0, edge 0.05 | 3363 | -8055.65 | -23.3% |
| blend 0.0, edge 0.08 | 2531 | -5637.22 | -21.7% |
| blend 0.25, edge 0.03 | 3348 | -8020.12 | -23.3% |
| blend 0.25, edge 0.05 | 2631 | -5728.27 | -21.2% |
| blend 0.25, edge 0.08 | 1691 | -3568.07 | -20.5% |
| blend 0.5, edge 0.03 | 2286 | -5149.98 | -21.9% |
| blend 0.5, edge 0.05 | 1468 | -3053.40 | -20.1% |
| blend 0.5, edge 0.08 | 708 | -606.66 | -8.3% |
| blend 0.75, edge 0.03 | 605 | -616.35 | -9.8% |
| blend 0.75, edge 0.05 | 242 | -526.67 | -20.9% |
| blend 0.75, edge 0.08 | 53 | -353.47 | -64.0% |

Forecast error (actual minus NBM forecast)

| City | Entry | n | Bias | RMSE |
|---|---|---|---|---|
| Austin | day before 10am | 238 | -2.64 | 4.1 |
| Austin | day before 8pm | 240 | -2.75 | 3.99 |
| Chicago | day before 10am | 238 | -1.62 | 3.04 |
| Chicago | day before 8pm | 240 | -1.39 | 2.68 |
| Denver | day before 10am | 239 | -3.93 | 5.21 |
| Denver | day before 8pm | 240 | -3.82 | 5.07 |
| Los Angeles | day before 10am | 238 | +0.36 | 1.72 |
| Los Angeles | day before 8pm | 240 | +0.49 | 1.61 |
| Miami | day before 8pm | 238 | -1.00 | 2.4 |
| New York | day before 8pm | 240 | -1.67 | 2.71 |
| Philadelphia | day before 8pm | 240 | +0.42 | 2.22 |

## Crypto: Bitcoin 5pm price

239 events, 2026-03-14 to 2026-11-08.

**Verdict:** Vol x0.5: +363 on 707 trades (+5.3% per $ staked), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Vol x0.5 | 707 | 82% | +363.11 | +5.3% | +198 | +165 | 92% | 0.1539 | 0.1463 |
| Long-shot fade (no model) | 779 | 97% | +127.42 | +1.7% | +61 | +67 | – | – | 0.0256 |
| Vol x0.75 | 298 | 70% | -128.84 | -4.4% | -1 | -128 | 79% | 0.1212 | 0.1164 |
| v1 (what we ran live) | 243 | 28% | -675.30 | -26.9% | -229 | -446 | 43% | 0.1117 | 0.0865 |
| v1 + 50% market blend | 183 | 22% | -748.47 | -39.3% | -434 | -315 | 31% | 0.0762 | 0.0677 |

Sweep: vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 796 | +210.35 | +2.7% |
| 0.5 | 707 | +363.11 | +5.3% |
| 0.6 | 557 | +103.84 | +1.9% |
| 0.75 | 298 | -128.84 | -4.4% |
| 1.0 | 243 | -675.30 | -26.9% |
| 1.25 | 338 | -1404.16 | -39.5% |

## Ethereum

235 events, 2026-03-19 to 2026-11-08.

**Verdict:** Market favorite (no model): +37 on 50 trades (+7.5% per $ staked), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Vol x0.5, 5c edge | 585 | 82% | +241.18 | +4.2% | +67 | +174 | 90% | 0.1465 | 0.1411 |
| Vol x0.5 (Bitcoin's winner) | 494 | 82% | +176.85 | +3.7% | +56 | +121 | 92% | 0.153 | 0.145 |
| Vol x0.5, NO only | 267 | 83% | +113.89 | +4.4% | +46 | +68 | 91% | 0.1374 | 0.1338 |
| Vol x0.75 | 134 | 75% | +71.72 | +5.4% | +22 | +50 | 84% | 0.153 | 0.1476 |
| Long-shot fade (no model) | 285 | 98% | +59.81 | +2.2% | +33 | +27 | – | – | 0.0254 |
| Market favorite (no model) | 50 | 68% | +37.29 | +7.5% | +20 | +17 | – | – | 0.1987 |
| Full vol + 50% market blend | 62 | 19% | +5.85 | +0.9% | +86 | -80 | 26% | 0.1112 | 0.1065 |
| Full vol (v1 rule) | 110 | 28% | -179.63 | -15.8% | -135 | -45 | 41% | 0.109 | 0.0919 |

Sweep: vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.3 | 717 | +229.05 | +3.3% |
| 0.4 | 623 | +237.92 | +3.9% |
| 0.5 | 494 | +176.85 | +3.7% |
| 0.6 | 318 | +95.34 | +3.1% |
| 0.75 | 134 | +71.72 | +5.4% |
| 1.0 | 110 | -179.63 | -15.8% |
