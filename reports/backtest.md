# Backtest (2026-11-09)

Flat $10 per trade at the ask plus Kalshi fees, held to settlement. Prices are real hourly Kalshi quotes. Forecasts are archived NWS-blend (NBM) runs 1-2 days old. Bias/sigma learned only from earlier days.

## Weather: daily highs

3731 events, 2025-03-18 to 2026-11-08.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Kalshi price-spike fade (no model) (+114 on 484 trades).

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 484 | 44% | +114.33 | +2.3% | -204 | +318 | – | – | 0.195 |
| Long-shot fade (no model) | 4930 | 95% | +26.45 | +0.1% | +41 | -14 | – | – | 0.0436 |
| Market favorite YES (no model) | 4569 | 50% | -180.22 | -0.4% | -134 | -46 | – | – | 0.2425 |
| Long-shot fade, limit order | 2821 | 92% | -482.16 | -1.8% | -220 | -262 | – | – | 0.0734 |
| Forecast bracket YES | 739 | 10% | -3397.55 | -43.7% | -1711 | -1686 | 33% | 0.1466 | 0.0915 |
| Market favorite, limit order | 3719 | 39% | -6414.99 | -17.5% | -4312 | -2103 | – | – | 0.2359 |
| v2 + disagreement cap | 3213 | 33% | -8369.79 | -25.4% | -4217 | -4153 | 54% | 0.2012 | 0.1572 |
| v2 + 50% market blend | 3555 | 31% | -9247.46 | -25.3% | -4237 | -5011 | 46% | 0.1904 | 0.1646 |
| v1 (what we ran live) | 4401 | 34% | -9383.88 | -20.8% | -4259 | -5125 | 63% | 0.2626 | 0.1645 |
| v2 calibrated | 4011 | 32% | -10187.19 | -24.8% | -4702 | -5485 | 58% | 0.2445 | 0.1673 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| v2 calibrated | 15 | +151.03 | +99.4% |
| v2 + 50% market blend | 13 | +130.80 | +99.7% |
| Forecast bracket YES | 4 | +104.20 | +249.3% |
| Long-shot fade (no model) | 2168 | +98.19 | +0.5% |
| v1 (what we ran live) | 12 | +38.08 | +31.2% |
| v2 + disagreement cap | 12 | +37.79 | +31.2% |
| Long-shot fade, limit order | 1166 | -135.59 | -1.2% |
| Kalshi price-spike fade (no model) | 224 | -144.65 | -6.3% |
| Market favorite YES (no model) | 2358 | -252.03 | -1.1% |
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

**Verdict:** Long-shot fade (no model): +100 on 3196 trades (+0.3% per $ staked, t=0.92), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 152 | 53% | +257.44 | +16.7% | -53 | +310 | – | – | 0.2106 |
| Long-shot fade (no model) | 3196 | 96% | +99.61 | +0.3% | +78 | +21 | – | – | 0.0367 |
| Long-shot fade, limit order | 1689 | 93% | -204.21 | -1.3% | -71 | -134 | – | – | 0.0667 |
| Market favorite YES (no model) | 2094 | 47% | -614.23 | -2.9% | +458 | -1073 | – | – | 0.2394 |
| Forecast bracket YES | 540 | 14% | -1717.56 | -30.3% | -1026 | -692 | 34% | 0.1609 | 0.1206 |
| Market favorite, limit order | 1741 | 36% | -2965.32 | -17.2% | -795 | -2171 | – | – | 0.226 |
| v2 + 50% market blend | 1842 | 29% | -3901.93 | -20.5% | -1126 | -2776 | 41% | 0.1562 | 0.1411 |
| v2 calibrated | 2557 | 31% | -5643.92 | -21.5% | -1580 | -4064 | 52% | 0.1998 | 0.1494 |
| v2 + disagreement cap | 2226 | 31% | -6118.05 | -26.8% | -2100 | -4018 | 50% | 0.1775 | 0.1426 |
| v1 (what we ran live) | 3767 | 32% | -10461.69 | -27.0% | -4429 | -6032 | 57% | 0.2259 | 0.1473 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Market favorite YES (no model) | 356 | +264.39 | +7.3% |
| Forecast bracket YES | 7 | +73.31 | +99.5% |
| v2 + disagreement cap | 17 | +62.01 | +36.3% |
| v2 + 50% market blend | 17 | -18.42 | -10.6% |
| v2 calibrated | 18 | -28.84 | -15.7% |
| v1 (what we ran live) | 17 | -30.72 | -17.7% |
| Long-shot fade (no model) | 717 | -40.91 | -0.6% |
| Long-shot fade, limit order | 431 | -98.02 | -2.4% |
| Kalshi price-spike fade (no model) | 32 | -114.28 | -35.2% |
| Market favorite, limit order | 290 | -306.98 | -10.7% |

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
