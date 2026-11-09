# Backtest (2026-11-09)

Flat $10 per trade at the ask plus Kalshi fees, held to settlement. Prices are real hourly Kalshi quotes. Forecasts are archived NWS-blend (NBM) runs 1-2 days old. Bias/sigma learned only from earlier days.

## Weather: daily highs

1672 events, 2026-03-13 to 2026-11-07.

**Verdict:** Kalshi price-spike fade (no model): +259 on 260 trades (+9.8% per $ staked), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 260 | 49% | +258.98 | +9.8% | +67 | +192 | – | – | 0.2092 |
| Market favorite YES (no model) | 2201 | 53% | +68.10 | +0.3% | -51 | +119 | – | – | 0.2422 |
| Long-shot fade (no model) | 2755 | 95% | -74.96 | -0.3% | -87 | +12 | – | – | 0.0471 |
| Long-shot fade, limit order | 1653 | 92% | -348.13 | -2.2% | -216 | -132 | – | – | 0.0761 |
| Market favorite, limit order | 1858 | 44% | -2105.02 | -11.5% | -1221 | -884 | – | – | 0.2411 |
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

**Verdict:** Kalshi price-spike fade (no model): +372 on 120 trades (+30.5% per $ staked), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 120 | 58% | +371.72 | +30.5% | +121 | +250 | – | – | 0.2183 |
| Long-shot fade (no model) | 2477 | 96% | +139.98 | +0.6% | +178 | -39 | – | – | 0.0338 |
| Long-shot fade, limit order | 1258 | 93% | -106.19 | -0.9% | +67 | -173 | – | – | 0.0634 |
| Market favorite YES (no model) | 1733 | 47% | -883.86 | -5.0% | -145 | -739 | – | – | 0.2378 |
| Forecast bracket YES | 537 | 14% | -1657.51 | -29.5% | -945 | -713 | 34% | 0.1623 | 0.1218 |
| Market favorite, limit order | 1448 | 36% | -2658.75 | -18.5% | -777 | -1881 | – | – | 0.2259 |
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

**Verdict:** Vol x0.5, weekends only: +93 on 89 trades (+10.7% per $ staked), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Time-of-day vol x0.5 | 742 | 83% | +451.90 | +6.2% | +242 | +210 | 92% | 0.1448 | 0.1422 |
| Vol x0.5 | 707 | 82% | +363.11 | +5.3% | +198 | +165 | 92% | 0.1539 | 0.1463 |
| Vol x0.5, skip news in window | 687 | 82% | +361.35 | +5.4% | +214 | +148 | 92% | 0.1531 | 0.1459 |
| Regime-scaled vol x0.5 | 799 | 81% | +337.77 | +4.3% | +250 | +87 | 92% | 0.1616 | 0.1502 |
| Vol x0.5, skip news days | 634 | 82% | +329.46 | +5.3% | +195 | +135 | 92% | 0.1528 | 0.1452 |
| Vol x0.5, skip spiked markets | 429 | 84% | +316.05 | +7.5% | +206 | +111 | 92% | 0.1353 | 0.1347 |
| Vol x0.5, weekdays only | 618 | 81% | +269.89 | +4.5% | +91 | +179 | 92% | 0.1665 | 0.1546 |
| Vol x0.5, against the 24h trend | 322 | 84% | +261.05 | +8.3% | +192 | +69 | 92% | 0.1305 | 0.1313 |
| Vol x0.5, busy market only | 270 | 83% | +218.46 | +8.3% | +146 | +73 | 92% | 0.1464 | 0.1455 |
| Vol x0.5, calm market only | 437 | 81% | +144.65 | +3.4% | +25 | +119 | 92% | 0.1585 | 0.1468 |
| Long-shot fade (no model) | 779 | 97% | +127.42 | +1.7% | +61 | +67 | – | – | 0.0256 |
| Vol x0.5, with the 24h trend | 385 | 80% | +102.06 | +2.7% | +4 | +98 | 92% | 0.1734 | 0.1589 |
| Vol x0.5, weekends only | 89 | 88% | +93.22 | +10.7% | +56 | +37 | 87% | 0.0663 | 0.0891 |
| Vol x0.5, news days only | 73 | 81% | +33.65 | +4.7% | +5 | +29 | 93% | 0.1629 | 0.1562 |
| Vol x0.75 | 298 | 70% | -128.84 | -4.4% | -1 | -128 | 79% | 0.1212 | 0.1164 |
| Vol x0.5, limit order | 374 | 67% | -410.93 | -11.4% | -233 | -178 | 92% | 0.2788 | 0.22 |
| Vol x0.5, limit order (strict fill) | 356 | 65% | -468.98 | -13.6% | -263 | -206 | 92% | 0.2926 | 0.2279 |
| Options vol x0.85, 5c gap | 407 | 51% | -519.41 | -12.6% | -155 | -364 | 60% | 0.107 | 0.0984 |
| Vol x0.5 5c edge, limit order | 422 | 66% | -531.39 | -13.0% | -286 | -246 | 90% | 0.2762 | 0.2205 |
| Options vol, 8c gap | 232 | 18% | -653.14 | -26.9% | -260 | -394 | 34% | 0.1073 | 0.0802 |
| v1 (what we ran live) | 243 | 28% | -675.30 | -26.9% | -229 | -446 | 43% | 0.1117 | 0.0865 |
| v1 + 50% market blend | 183 | 22% | -748.47 | -39.3% | -434 | -315 | 31% | 0.0762 | 0.0677 |
| Options vol, NO only | 345 | 27% | -878.75 | -24.6% | -664 | -214 | 40% | 0.1125 | 0.0914 |
| Options vol, 5c gap | 373 | 26% | -1130.20 | -29.3% | -527 | -603 | 40% | 0.103 | 0.0826 |
| Kalshi price-spike fade (no model) | 513 | 34% | -1194.03 | -22.6% | -659 | -535 | – | – | 0.1489 |

Sweep: vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 796 | +210.35 | +2.7% |
| 0.5 | 707 | +363.11 | +5.3% |
| 0.6 | 557 | +103.84 | +1.9% |
| 0.75 | 298 | -128.84 | -4.4% |
| 1.0 | 243 | -675.30 | -26.9% |
| 1.25 | 338 | -1404.16 | -39.5% |

Sweep: options vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 692 | +40.59 | +0.6% |
| 0.7 | 598 | -156.88 | -2.7% |
| 0.8 | 464 | -202.79 | -4.4% |
| 0.9 | 380 | -774.15 | -20.0% |
| 1.0 | 373 | -1130.20 | -29.3% |
| 1.1 | 408 | -1234.49 | -28.9% |

Sweep: time-of-day vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 880 | +272.83 | +3.2% |
| 0.5 | 742 | +451.90 | +6.2% |
| 0.6 | 501 | +397.13 | +8.1% |
| 0.75 | 173 | +109.70 | +6.5% |
| 1.0 | 151 | -370.20 | -23.7% |

## Ethereum

235 events, 2026-03-19 to 2026-11-08.

**Verdict:** Vol x0.5, weekends only: +90 on 45 trades (+20.3% per $ staked), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Vol x0.5, 5c edge | 585 | 82% | +241.18 | +4.2% | +67 | +174 | 90% | 0.1465 | 0.1411 |
| Vol x0.5, skip news days | 441 | 83% | +224.32 | +5.2% | +75 | +149 | 92% | 0.1437 | 0.1389 |
| Vol x0.5, against the 24h trend | 253 | 86% | +223.25 | +9.0% | +117 | +106 | 92% | 0.1202 | 0.124 |
| Vol x0.5, skip spiked markets | 331 | 84% | +223.13 | +6.9% | +95 | +129 | 92% | 0.136 | 0.1352 |
| Vol x0.5, skip news in window | 478 | 82% | +202.60 | +4.3% | +78 | +124 | 92% | 0.1506 | 0.1439 |
| Options vol x0.85, 5c gap | 178 | 45% | +193.66 | +10.6% | +66 | +128 | 52% | 0.1174 | 0.11 |
| Regime-scaled vol x0.5 | 548 | 81% | +181.97 | +3.4% | +45 | +136 | 92% | 0.157 | 0.1473 |
| Time-of-day vol x0.5 | 461 | 83% | +179.66 | +4.0% | +67 | +113 | 92% | 0.1397 | 0.135 |
| Vol x0.5 (Bitcoin's winner) | 494 | 82% | +176.85 | +3.7% | +56 | +121 | 92% | 0.153 | 0.145 |
| Vol x0.5, calm market only | 294 | 82% | +133.78 | +4.7% | +46 | +88 | 91% | 0.1476 | 0.1429 |
| Vol x0.5, NO only | 267 | 83% | +113.89 | +4.4% | +46 | +68 | 91% | 0.1374 | 0.1338 |
| Vol x0.5, weekends only | 45 | 89% | +89.62 | +20.3% | +28 | +61 | 88% | 0.0701 | 0.0917 |
| Vol x0.5, weekdays only | 449 | 81% | +87.23 | +2.0% | +16 | +72 | 92% | 0.1614 | 0.1503 |
| Vol x0.75 | 134 | 75% | +71.72 | +5.4% | +22 | +50 | 84% | 0.153 | 0.1476 |
| Long-shot fade (no model) | 285 | 98% | +59.81 | +2.2% | +33 | +27 | – | – | 0.0254 |
| Vol x0.5, busy market only | 200 | 82% | +43.07 | +2.2% | -1 | +44 | 93% | 0.1611 | 0.1479 |
| Options vol, NO only | 111 | 20% | +38.27 | +3.3% | -103 | +141 | 32% | 0.1345 | 0.1146 |
| Market favorite (no model) | 50 | 68% | +37.29 | +7.5% | +20 | +17 | – | – | 0.1987 |
| Options vol, 8c gap | 117 | 14% | +19.07 | +1.6% | +16 | +3 | 30% | 0.1274 | 0.1024 |
| Full vol + 50% market blend | 62 | 19% | +5.85 | +0.9% | +86 | -80 | 26% | 0.1112 | 0.1065 |
| Vol x0.5, with the 24h trend | 241 | 77% | -46.40 | -2.0% | -71 | +24 | 91% | 0.1875 | 0.167 |
| Vol x0.5, news days only | 53 | 72% | -47.47 | -9.2% | -32 | -15 | 92% | 0.2311 | 0.1953 |
| Full vol (v1 rule) | 110 | 28% | -179.63 | -15.8% | -135 | -45 | 41% | 0.109 | 0.0919 |
| Options vol, 5c gap | 213 | 19% | -343.03 | -15.4% | -293 | -50 | 32% | 0.1146 | 0.0963 |
| Vol x0.5, limit order | 254 | 65% | -368.21 | -15.0% | -141 | -227 | 91% | 0.2829 | 0.2263 |
| Vol x0.5, limit order (strict fill) | 247 | 64% | -386.23 | -16.2% | -154 | -233 | 91% | 0.2907 | 0.2315 |
| Vol x0.5 5c edge, limit order | 297 | 65% | -430.60 | -15.0% | -207 | -224 | 89% | 0.2704 | 0.2192 |
| Kalshi price-spike fade (no model) | 355 | 32% | -877.85 | -24.1% | -361 | -517 | – | – | 0.173 |

Sweep: vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.3 | 717 | +229.05 | +3.3% |
| 0.4 | 623 | +237.92 | +3.9% |
| 0.5 | 494 | +176.85 | +3.7% |
| 0.6 | 318 | +95.34 | +3.1% |
| 0.75 | 134 | +71.72 | +5.4% |
| 1.0 | 110 | -179.63 | -15.8% |

Sweep: time-of-day vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 618 | +208.20 | +3.5% |
| 0.5 | 461 | +179.66 | +4.0% |
| 0.6 | 258 | -36.87 | -1.5% |
| 0.75 | 90 | -95.95 | -10.7% |
| 1.0 | 102 | -479.33 | -45.1% |

Sweep: options vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 445 | -23.49 | -0.5% |
| 0.7 | 278 | -75.08 | -2.7% |
| 0.8 | 185 | +9.60 | +0.5% |
| 0.9 | 175 | +30.19 | +1.7% |
| 1.0 | 213 | -343.03 | -15.4% |
| 1.1 | 295 | -1193.08 | -38.5% |
