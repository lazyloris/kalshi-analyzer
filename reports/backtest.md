# Backtest (2026-11-09)

Flat $10 per trade at the ask plus Kalshi fees, held to settlement. Prices are real hourly Kalshi quotes. Forecasts are archived NWS-blend (NBM) runs 1-2 days old. Bias/sigma learned only from earlier days.

## Weather: daily highs

1679 events, 2026-03-13 to 2026-11-08.

**Verdict:** Kalshi price-spike fade (no model): +259 on 260 trades (+9.8% per $ staked, t=1.1), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 260 | 49% | +258.98 | +9.8% | +67 | +192 | – | – | 0.2092 |
| Market favorite YES (no model) | 2211 | 53% | +71.81 | +0.3% | -47 | +118 | – | – | 0.2422 |
| Long-shot fade (no model) | 2762 | 95% | -71.74 | -0.3% | -105 | +33 | – | – | 0.047 |
| Long-shot fade, limit order | 1655 | 92% | -346.57 | -2.2% | -216 | -131 | – | – | 0.076 |
| Market favorite, limit order | 1867 | 44% | -2101.83 | -11.4% | -1226 | -876 | – | – | 0.2412 |
| Forecast bracket YES | 731 | 10% | -3501.21 | -45.5% | -1857 | -1644 | 33% | 0.1453 | 0.0884 |
| v2 + disagreement cap | 3203 | 33% | -8460.37 | -25.8% | -4292 | -4169 | 54% | 0.2014 | 0.1572 |
| v2 + 50% market blend | 3539 | 31% | -9190.90 | -25.3% | -4231 | -4960 | 46% | 0.1906 | 0.1645 |
| v1 (what we ran live) | 4389 | 34% | -9421.96 | -20.9% | -4338 | -5084 | 63% | 0.263 | 0.1644 |
| v2 calibrated | 3995 | 32% | -10355.64 | -25.3% | -4952 | -5403 | 58% | 0.245 | 0.167 |

Sweep: sigma

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 3973 | -9722.92 | -23.9% |
| 0.8 | 3830 | -9874.47 | -25.1% |
| 1.0 | 3995 | -10355.64 | -25.3% |
| 1.25 | 4252 | -9010.07 | -20.7% |
| 1.5 | 4398 | -7802.42 | -17.4% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 4874 | -11935.47 | -23.9% |
| blend 0.0, edge 0.05 | 4569 | -11364.42 | -24.2% |
| blend 0.0, edge 0.08 | 3995 | -10355.64 | -25.3% |
| blend 0.25, edge 0.03 | 4615 | -11430.42 | -24.1% |
| blend 0.25, edge 0.05 | 4130 | -10506.73 | -24.8% |
| blend 0.25, edge 0.08 | 3234 | -8845.93 | -26.6% |
| blend 0.5, edge 0.03 | 3972 | -10273.89 | -25.2% |
| blend 0.5, edge 0.05 | 3061 | -8258.67 | -26.2% |
| blend 0.5, edge 0.08 | 1844 | -4652.67 | -24.5% |
| blend 0.75, edge 0.03 | 1844 | -5473.73 | -28.8% |
| blend 0.75, edge 0.05 | 788 | -1952.79 | -23.9% |
| blend 0.75, edge 0.08 | 207 | -650.07 | -30.2% |

Forecast error (actual minus NBM forecast)

| City | Entry | n | Bias | RMSE |
|---|---|---|---|---|
| Austin | day before 10am | 239 | +1.85 | 3.3 |
| Austin | same day 8am | 241 | +1.55 | 2.94 |
| Chicago | day before 10am | 239 | +1.45 | 3.44 |
| Chicago | same day 8am | 237 | +1.27 | 2.86 |
| Denver | day before 10am | 240 | +1.75 | 3.42 |
| Denver | same day 8am | 237 | +1.68 | 2.97 |
| Los Angeles | day before 10am | 238 | +2.30 | 3.89 |
| Los Angeles | same day 8am | 240 | +2.31 | 3.63 |
| Miami | same day 8am | 240 | +2.05 | 2.67 |
| New York | same day 8am | 238 | -0.26 | 2.46 |
| Philadelphia | same day 8am | 238 | +1.74 | 2.88 |

## Weather: daily lows

1685 events, 2026-03-13 to 2026-11-08.

**Verdict:** Kalshi price-spike fade (no model): +372 on 120 trades (+30.5% per $ staked, t=2.12), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 120 | 58% | +371.72 | +30.5% | +121 | +250 | – | – | 0.2183 |
| Long-shot fade (no model) | 2479 | 96% | +140.52 | +0.6% | +179 | -38 | – | – | 0.0337 |
| Long-shot fade, limit order | 1258 | 93% | -106.19 | -0.9% | +67 | -173 | – | – | 0.0634 |
| Market favorite YES (no model) | 1738 | 47% | -878.62 | -5.0% | -127 | -752 | – | – | 0.2379 |
| Forecast bracket YES | 538 | 14% | -1636.91 | -29.0% | -955 | -682 | 34% | 0.1626 | 0.1226 |
| Market favorite, limit order | 1451 | 36% | -2658.34 | -18.5% | -787 | -1871 | – | – | 0.2261 |
| v2 + 50% market blend | 1832 | 29% | -3923.53 | -20.7% | -1183 | -2741 | 41% | 0.1567 | 0.1413 |
| v2 calibrated | 2540 | 31% | -5606.99 | -21.5% | -1600 | -4007 | 52% | 0.201 | 0.1502 |
| v2 + disagreement cap | 2206 | 31% | -6183.28 | -27.3% | -2029 | -4154 | 50% | 0.178 | 0.1427 |
| v1 (what we ran live) | 3750 | 32% | -10430.97 | -27.1% | -4437 | -5994 | 57% | 0.2259 | 0.1474 |

Sweep: sigma

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 3294 | -5351.45 | -16.0% |
| 0.8 | 2614 | -5175.87 | -19.3% |
| 1.0 | 2540 | -5606.99 | -21.5% |
| 1.25 | 2974 | -6727.78 | -22.0% |
| 1.5 | 3487 | -8610.94 | -24.1% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 3929 | -9268.47 | -23.0% |
| blend 0.0, edge 0.05 | 3374 | -8034.75 | -23.2% |
| blend 0.0, edge 0.08 | 2540 | -5606.99 | -21.5% |
| blend 0.25, edge 0.03 | 3359 | -7999.22 | -23.2% |
| blend 0.25, edge 0.05 | 2639 | -5687.59 | -20.9% |
| blend 0.25, edge 0.08 | 1695 | -3582.36 | -20.5% |
| blend 0.5, edge 0.03 | 2292 | -5185.41 | -21.9% |
| blend 0.5, edge 0.05 | 1472 | -3067.69 | -20.2% |
| blend 0.5, edge 0.08 | 710 | -600.31 | -8.2% |
| blend 0.75, edge 0.03 | 607 | -610.00 | -9.7% |
| blend 0.75, edge 0.05 | 242 | -526.67 | -20.9% |
| blend 0.75, edge 0.08 | 53 | -353.47 | -64.0% |

Forecast error (actual minus NBM forecast)

| City | Entry | n | Bias | RMSE |
|---|---|---|---|---|
| Austin | day before 10am | 239 | -2.63 | 4.09 |
| Austin | day before 8pm | 241 | -2.73 | 3.98 |
| Chicago | day before 10am | 239 | -1.61 | 3.04 |
| Chicago | day before 8pm | 241 | -1.38 | 2.67 |
| Denver | day before 10am | 240 | -3.92 | 5.2 |
| Denver | day before 8pm | 241 | -3.81 | 5.06 |
| Los Angeles | day before 10am | 239 | +0.37 | 1.72 |
| Los Angeles | day before 8pm | 241 | +0.49 | 1.61 |
| Miami | day before 8pm | 239 | -0.99 | 2.39 |
| New York | day before 8pm | 241 | -1.67 | 2.7 |
| Philadelphia | day before 8pm | 241 | +0.42 | 2.21 |

## Crypto: Bitcoin 5pm price

239 events, 2026-03-14 to 2026-11-08.

**Verdict:** Time-of-day vol x0.5, against trend + skip spikes: +289 on 234 trades (+12.7% per $ staked, t=4.87), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Time-of-day vol x0.5 | 742 | 83% | +451.90 | +6.2% | +242 | +210 | 92% | 0.1448 | 0.1422 |
| Time-of-day vol x0.5, skip spikes | 465 | 86% | +418.25 | +9.2% | +253 | +165 | 92% | 0.1216 | 0.1275 |
| Vol x0.5 | 707 | 82% | +363.11 | +5.3% | +198 | +165 | 92% | 0.1539 | 0.1463 |
| Vol x0.5, skip news in window | 687 | 82% | +361.35 | +5.4% | +214 | +148 | 92% | 0.1531 | 0.1459 |
| Regime-scaled vol x0.5 | 799 | 81% | +337.77 | +4.3% | +250 | +87 | 92% | 0.1616 | 0.1502 |
| Vol x0.5, skip news days | 634 | 82% | +329.46 | +5.3% | +195 | +135 | 92% | 0.1528 | 0.1452 |
| Vol x0.5, skip spiked markets | 429 | 84% | +316.05 | +7.5% | +206 | +111 | 92% | 0.1353 | 0.1347 |
| Time-of-day vol x0.5, against trend + skip spikes | 234 | 89% | +289.08 | +12.7% | +201 | +88 | 92% | 0.0932 | 0.1071 |
| Vol x0.5, weekdays only | 618 | 81% | +269.89 | +4.5% | +91 | +179 | 92% | 0.1665 | 0.1546 |
| Vol x0.5, against the 24h trend | 322 | 84% | +261.05 | +8.3% | +192 | +69 | 92% | 0.1305 | 0.1313 |
| Vol x0.5, busy market only | 270 | 83% | +218.46 | +8.3% | +146 | +73 | 92% | 0.1464 | 0.1455 |
| Vol x0.5, against trend + skip spikes | 216 | 85% | +171.79 | +8.2% | +152 | +20 | 93% | 0.1268 | 0.1271 |
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

**Verdict:** Time-of-day vol x0.5, against trend + skip spikes: +174 on 163 trades (+11.0% per $ staked, t=3.54), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Vol x0.5, 5c edge | 585 | 82% | +241.18 | +4.2% | +67 | +174 | 90% | 0.1465 | 0.1411 |
| Vol x0.5, skip news days | 441 | 83% | +224.32 | +5.2% | +75 | +149 | 92% | 0.1437 | 0.1389 |
| Vol x0.5, against the 24h trend | 253 | 86% | +223.25 | +9.0% | +117 | +106 | 92% | 0.1202 | 0.124 |
| Vol x0.5, skip spiked markets | 331 | 84% | +223.13 | +6.9% | +95 | +129 | 92% | 0.136 | 0.1352 |
| Time-of-day vol x0.5, skip spikes | 301 | 86% | +206.84 | +7.0% | +106 | +101 | 92% | 0.1236 | 0.1264 |
| Vol x0.5, skip news in window | 478 | 82% | +202.60 | +4.3% | +78 | +124 | 92% | 0.1506 | 0.1439 |
| Options vol x0.85, 5c gap | 178 | 45% | +193.66 | +10.6% | +66 | +128 | 52% | 0.1174 | 0.11 |
| Regime-scaled vol x0.5 | 548 | 81% | +181.97 | +3.4% | +45 | +136 | 92% | 0.157 | 0.1473 |
| Time-of-day vol x0.5 | 461 | 83% | +179.66 | +4.0% | +67 | +113 | 92% | 0.1397 | 0.135 |
| Vol x0.5 (Bitcoin's winner) | 494 | 82% | +176.85 | +3.7% | +56 | +121 | 92% | 0.153 | 0.145 |
| Time-of-day vol x0.5, against trend + skip spikes | 163 | 90% | +174.20 | +11.0% | +104 | +70 | 93% | 0.0956 | 0.1067 |
| Vol x0.5, against trend + skip spikes | 179 | 87% | +170.24 | +9.8% | +95 | +75 | 93% | 0.1181 | 0.1213 |
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
