# Backtest (2026-11-09)

Flat $10 per trade at the ask plus Kalshi fees, held to settlement. Prices are real hourly Kalshi quotes. Forecasts are archived NWS-blend (NBM) runs 1-2 days old. Bias/sigma learned only from earlier days.

## Weather: daily highs

1672 events, 2026-03-13 to 2026-11-07.

**Verdict:** Kalshi price-spike fade (no model): +259 on 260 trades (+9.8% per $ staked, t=1.1), profitable in both halves.

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

**Verdict:** Kalshi price-spike fade (no model): +372 on 120 trades (+30.5% per $ staked, t=2.12), profitable in both halves.

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

599 events, 2025-03-19 to 2026-11-08.

**Verdict:** Vol x0.5, weekends only: +150 on 230 trades (+6.7% per $ staked, t=2.15), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Time-of-day vol x0.5 | 1521 | 80% | +305.72 | +2.1% | -138 | +444 | 92% | 0.1714 | 0.1587 |
| Time-of-day vol x0.5, skip spikes | 952 | 82% | +272.57 | +2.9% | -150 | +423 | 92% | 0.1613 | 0.1525 |
| Time-of-day vol x0.5, against trend + skip spikes | 503 | 82% | +195.64 | +4.0% | -113 | +309 | 92% | 0.1523 | 0.1457 |
| Regime-scaled vol x0.5 | 1931 | 78% | +174.05 | +0.9% | -216 | +390 | 93% | 0.1882 | 0.1668 |
| Vol x0.5, weekends only | 230 | 84% | +149.69 | +6.7% | +17 | +132 | 91% | 0.1219 | 0.1265 |
| Vol x0.5, skip spiked markets | 1085 | 79% | +141.09 | +1.3% | -163 | +304 | 93% | 0.1805 | 0.1617 |
| Vol x0.5, against the 24h trend | 819 | 79% | +108.88 | +1.4% | -169 | +278 | 93% | 0.1828 | 0.1635 |
| Vol x0.5, against trend + skip spikes | 575 | 80% | +104.82 | +1.9% | -73 | +178 | 93% | 0.1734 | 0.1566 |
| Vol x0.5 | 1752 | 78% | +75.81 | +0.4% | -288 | +364 | 93% | 0.1887 | 0.1666 |
| Vol x0.5, calm market only | 1040 | 79% | +75.58 | +0.8% | -94 | +169 | 92% | 0.1779 | 0.1605 |
| Long-shot fade (no model) | 1276 | 96% | +59.14 | +0.5% | -52 | +111 | – | – | 0.0356 |
| Vol x0.5, skip news in window | 1728 | 78% | +56.41 | +0.3% | -287 | +343 | 93% | 0.1892 | 0.1668 |
| Vol x0.5, news days only | 101 | 79% | +40.11 | +4.1% | -10 | +50 | 93% | 0.1772 | 0.166 |
| Vol x0.5, skip news days | 1651 | 78% | +35.70 | +0.2% | -290 | +326 | 93% | 0.1894 | 0.1666 |
| Vol x0.5, busy market only | 712 | 77% | +0.23 | +0.0% | -206 | +206 | 93% | 0.2045 | 0.1755 |
| Vol x0.5, with the 24h trend | 933 | 78% | -33.07 | -0.4% | -110 | +76 | 93% | 0.1939 | 0.1693 |
| Vol x0.5, weekdays only | 1522 | 77% | -73.88 | -0.5% | -316 | +243 | 93% | 0.1988 | 0.1726 |
| Vol x0.75 | 780 | 72% | -503.01 | -6.6% | -313 | -190 | 85% | 0.1707 | 0.153 |
| v1 + 50% market blend | 281 | 30% | -1131.81 | -39.1% | -642 | -489 | 41% | 0.1107 | 0.0982 |
| Options vol x0.85, 5c gap | 806 | 56% | -1195.19 | -14.8% | -706 | -489 | 65% | 0.1218 | 0.1107 |
| v1 (what we ran live) | 444 | 37% | -1383.14 | -30.5% | -929 | -454 | 53% | 0.127 | 0.0986 |
| Options vol, 8c gap | 415 | 24% | -1412.59 | -32.8% | -1012 | -400 | 40% | 0.1097 | 0.0822 |
| Vol x0.5, limit order | 944 | 60% | -1711.15 | -18.8% | -1109 | -602 | 93% | 0.3416 | 0.2537 |
| Options vol, NO only | 590 | 31% | -1763.26 | -29.0% | -1340 | -424 | 45% | 0.1247 | 0.1031 |
| Vol x0.5, limit order (strict fill) | 907 | 59% | -1830.36 | -20.9% | -1149 | -681 | 92% | 0.3553 | 0.2615 |
| Vol x0.5 5c edge, limit order | 1038 | 60% | -1947.81 | -19.4% | -1204 | -743 | 91% | 0.3326 | 0.2495 |
| Options vol, 5c gap | 680 | 31% | -2157.19 | -30.8% | -1286 | -872 | 44% | 0.1143 | 0.0934 |
| Kalshi price-spike fade (no model) | 1236 | 30% | -3214.89 | -25.2% | -1654 | -1561 | – | – | 0.1513 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Vol x0.5, weekends only | 141 | +56.47 | +4.1% |
| Vol x0.5, news days only | 28 | +6.46 | +2.4% |
| Vol x0.5, against trend + skip spikes | 358 | -69.23 | -2.0% |
| Long-shot fade (no model) | 493 | -70.03 | -1.5% |
| Vol x0.5, calm market only | 601 | -75.32 | -1.3% |
| Time-of-day vol x0.5, against trend + skip spikes | 268 | -95.70 | -3.7% |
| Vol x0.5, with the 24h trend | 547 | -125.26 | -2.3% |
| Time-of-day vol x0.5 | 775 | -132.17 | -1.8% |
| Time-of-day vol x0.5, skip spikes | 486 | -147.94 | -3.1% |
| Vol x0.5, against the 24h trend | 494 | -161.37 | -3.4% |
| Regime-scaled vol x0.5 | 1128 | -163.05 | -1.5% |
| Vol x0.5, skip spiked markets | 655 | -177.22 | -2.8% |
| Vol x0.5, busy market only | 440 | -211.31 | -4.9% |
| Vol x0.5 | 1041 | -286.63 | -2.8% |
| Vol x0.5, skip news days | 1013 | -293.09 | -3.0% |
| Vol x0.5, skip news in window | 1037 | -304.27 | -3.0% |
| Vol x0.5, weekdays only | 900 | -343.10 | -3.9% |
| Vol x0.75 | 480 | -377.77 | -8.1% |
| v1 + 50% market blend | 98 | -383.34 | -38.8% |
| Options vol x0.85, 5c gap | 397 | -679.38 | -17.1% |
| v1 (what we ran live) | 201 | -707.84 | -34.9% |
| Options vol, 8c gap | 183 | -759.45 | -40.2% |
| Options vol, NO only | 245 | -884.51 | -35.3% |
| Options vol, 5c gap | 307 | -1026.99 | -32.6% |
| Vol x0.5, limit order | 567 | -1297.02 | -23.7% |
| Vol x0.5, limit order (strict fill) | 548 | -1358.18 | -25.7% |
| Vol x0.5 5c edge, limit order | 613 | -1413.22 | -23.9% |
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
| Vol x0.5, against trend + skip spikes | 495 | 80% | +12.81 | +0.3% | -146 | +159 | 93% | 0.1763 | 0.1595 |
| Long-shot fade (no model) | 597 | 95% | -26.51 | -0.5% | -93 | +66 | – | – | 0.0452 |
| Vol x0.5, news days only | 81 | 74% | -53.01 | -6.7% | -22 | -31 | 92% | 0.2085 | 0.1774 |
| Vol x0.5, against the 24h trend | 693 | 78% | -83.69 | -1.2% | -266 | +182 | 92% | 0.1855 | 0.1652 |
| Vol x0.75 | 394 | 76% | -92.34 | -2.4% | -179 | +87 | 88% | 0.1684 | 0.1532 |
| Vol x0.5, calm market only | 754 | 78% | -101.14 | -1.4% | -227 | +126 | 92% | 0.1804 | 0.1617 |
| Vol x0.5, 5c edge | 1689 | 79% | -118.64 | -0.7% | -388 | +270 | 91% | 0.1773 | 0.1595 |
| Vol x0.5, busy market only | 660 | 77% | -147.83 | -2.3% | -156 | +8 | 93% | 0.1956 | 0.1694 |
| Vol x0.5, with the 24h trend | 721 | 78% | -165.28 | -2.4% | -129 | -37 | 92% | 0.1895 | 0.1654 |
| Regime-scaled vol x0.5 | 1578 | 79% | -184.73 | -1.2% | -323 | +138 | 93% | 0.1822 | 0.1609 |
| Vol x0.5, skip news days | 1333 | 78% | -195.96 | -1.5% | -329 | +133 | 92% | 0.1863 | 0.1646 |
| Full vol + 50% market blend | 97 | 23% | -223.31 | -22.1% | -341 | +117 | 34% | 0.1203 | 0.1089 |
| Vol x0.5, NO only | 893 | 78% | -229.95 | -2.6% | -238 | +8 | 92% | 0.1859 | 0.1638 |
| Vol x0.5, skip news in window | 1391 | 78% | -244.13 | -1.8% | -382 | +138 | 92% | 0.188 | 0.1656 |
| Vol x0.5 (Bitcoin's winner) | 1414 | 78% | -248.97 | -1.8% | -407 | +158 | 92% | 0.1875 | 0.1653 |
| Vol x0.5, weekdays only | 1265 | 77% | -320.88 | -2.6% | -381 | +60 | 93% | 0.1941 | 0.1699 |
| Options vol x0.85, 5c gap | 429 | 56% | -427.67 | -9.9% | -571 | +144 | 66% | 0.1357 | 0.1209 |
| Options vol, NO only | 216 | 27% | -525.43 | -23.5% | -595 | +70 | 42% | 0.1231 | 0.0982 |
| Options vol, 8c gap | 199 | 17% | -581.15 | -28.0% | -715 | +134 | 36% | 0.1287 | 0.0927 |
| Full vol (v1 rule) | 216 | 28% | -872.28 | -39.2% | -714 | -158 | 46% | 0.1198 | 0.0887 |
| Options vol, 5c gap | 388 | 22% | -1488.01 | -37.0% | -1224 | -264 | 39% | 0.1177 | 0.0907 |
| Vol x0.5, limit order | 713 | 57% | -1704.34 | -24.8% | -1094 | -610 | 92% | 0.3593 | 0.2694 |
| Vol x0.5, limit order (strict fill) | 692 | 56% | -1756.42 | -26.3% | -1120 | -636 | 92% | 0.37 | 0.2764 |
| Vol x0.5 5c edge, limit order | 833 | 58% | -1892.10 | -23.5% | -1221 | -671 | 91% | 0.3442 | 0.2626 |
| Kalshi price-spike fade (no model) | 1049 | 30% | -2292.35 | -21.2% | -924 | -1368 | – | – | 0.1704 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Market favorite (no model) | 64 | +89.35 | +13.9% |
| Time-of-day vol x0.5, against trend + skip spikes | 259 | -8.24 | -0.3% |
| Vol x0.5, weekends only | 102 | -11.15 | -1.1% |
| Vol x0.5, news days only | 25 | -13.39 | -5.5% |
| Time-of-day vol x0.5, skip spikes | 469 | -55.12 | -1.2% |
| Long-shot fade (no model) | 307 | -88.63 | -3.0% |
| Time-of-day vol x0.5 | 747 | -127.98 | -1.8% |
| Vol x0.5, with the 24h trend | 472 | -129.90 | -2.8% |
| Vol x0.5, against trend + skip spikes | 311 | -143.61 | -4.7% |
| Vol x0.75 | 255 | -161.63 | -6.5% |
| Vol x0.5, skip spiked markets | 575 | -185.90 | -3.3% |
| Vol x0.5, busy market only | 452 | -186.03 | -4.2% |
| Full vol + 50% market blend | 33 | -208.07 | -61.7% |
| Vol x0.5, calm market only | 453 | -242.35 | -5.5% |
| Vol x0.5, against the 24h trend | 433 | -298.48 | -7.1% |
| Vol x0.5, NO only | 614 | -322.81 | -5.4% |
| Regime-scaled vol x0.5 | 1015 | -354.69 | -3.6% |
| Vol x0.5, 5c edge | 1087 | -373.06 | -3.5% |
| Vol x0.5, skip news days | 880 | -414.99 | -4.8% |
| Vol x0.5, weekdays only | 803 | -417.23 | -5.3% |
| Vol x0.5 (Bitcoin's winner) | 905 | -428.38 | -4.9% |
| Vol x0.5, skip news in window | 901 | -441.44 | -5.0% |
| Options vol, NO only | 101 | -521.70 | -50.6% |
| Options vol, 8c gap | 79 | -568.57 | -69.8% |
| Options vol x0.85, 5c gap | 245 | -594.43 | -24.5% |
| Full vol (v1 rule) | 105 | -682.19 | -63.4% |
| Options vol, 5c gap | 170 | -1092.46 | -62.5% |
| Vol x0.5, limit order | 450 | -1324.38 | -30.5% |
| Vol x0.5, limit order (strict fill) | 436 | -1358.44 | -32.3% |
| Kalshi price-spike fade (no model) | 684 | -1370.22 | -19.4% |
| Vol x0.5 5c edge, limit order | 526 | -1456.81 | -28.7% |

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

Sweep: options vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 1336 | -423.21 | -3.2% |
| 0.7 | 866 | -402.93 | -4.7% |
| 0.8 | 519 | -451.06 | -8.8% |
| 0.9 | 371 | -673.10 | -17.8% |
| 1.0 | 388 | -1488.01 | -37.0% |
| 1.1 | 525 | -2862.73 | -52.1% |
