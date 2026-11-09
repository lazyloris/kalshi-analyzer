# Backtest (2026-11-09)

Flat $10 per trade at the ask plus Kalshi fees, held to settlement. Prices are real hourly Kalshi quotes. Forecasts are archived NWS-blend (NBM) runs 1-2 days old. Bias/sigma learned only from earlier days.

## Weather: daily highs

3731 events, 2025-03-18 to 2026-11-08.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Kalshi price-spike fade (no model) (+114 on 484 trades).

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 484 | 44% | +114.33 | +2.3% | -204 | +318 | – | – | 0.195 |
| Long-shot fade (no model) | 4928 | 95% | +35.53 | +0.1% | +40 | -5 | – | – | 0.0434 |
| Market favorite YES (no model) | 4569 | 50% | -180.22 | -0.4% | -134 | -46 | – | – | 0.2425 |
| Long-shot fade, limit order | 2820 | 92% | -472.94 | -1.8% | -211 | -262 | – | – | 0.0732 |
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
| Long-shot fade (no model) | 2166 | +107.27 | +0.5% |
| Forecast bracket YES | 4 | +104.20 | +249.3% |
| v1 (what we ran live) | 12 | +38.08 | +31.2% |
| v2 + disagreement cap | 12 | +37.79 | +31.2% |
| Long-shot fade, limit order | 1165 | -126.37 | -1.2% |
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

**Verdict:** Long-shot fade (no model): +100 on 3197 trades (+0.3% per $ staked, t=0.92), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Kalshi price-spike fade (no model) | 152 | 53% | +257.44 | +16.7% | -53 | +310 | – | – | 0.2106 |
| Long-shot fade (no model) | 3197 | 96% | +100.17 | +0.3% | +79 | +22 | – | – | 0.0367 |
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
| Long-shot fade (no model) | 718 | -40.35 | -0.6% |
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
| Long-shot fade (no model) | 1275 | 96% | +58.49 | +0.5% | -52 | +111 | – | – | 0.0356 |
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
| Options vol, NO only | 589 | 31% | -1764.81 | -29.1% | -1341 | -424 | 45% | 0.1249 | 0.1033 |
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
| Long-shot fade (no model) | 492 | -70.68 | -1.5% |
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
| Options vol, NO only | 244 | -886.06 | -35.5% |
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

## Weather: daily highs: late entries

2695 events, 2025-03-18 to 2026-11-08.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Late long-shot fade 1-4c (+48 on 966 trades).

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Late long-shot fade 1-4c | 966 | 99% | +48.25 | +0.5% | -7 | +55 | – | – | 0.0084 |
| Late favorite 90-97c | 819 | 95% | +7.03 | +0.1% | -5 | +12 | – | – | 0.0489 |
| Late long-shot fade | 736 | 95% | -14.72 | -0.2% | -37 | +22 | – | – | 0.0441 |
| Late favorite 80-90c | 436 | 86% | -52.38 | -1.2% | +9 | -61 | – | – | 0.123 |
| Late favorite 50-80c | 546 | 67% | -177.08 | -3.3% | -107 | -70 | – | – | 0.2139 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Late long-shot fade 1-4c | 381 | +8.42 | +0.2% |
| Late favorite 90-97c | 343 | -10.04 | -0.3% |
| Late favorite 80-90c | 159 | -14.09 | -0.9% |
| Late long-shot fade | 237 | -53.63 | -2.4% |
| Late favorite 50-80c | 169 | -113.02 | -6.8% |

## Weather: daily lows: late entries

1793 events, 2025-12-13 to 2026-11-08.

**Verdict:** No strategy made money in both halves with 50+ trades. Least bad: Late favorite 90-97c (-69 on 871 trades).

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Late favorite 90-97c | 871 | 94% | -69.01 | -0.8% | -48 | -21 | – | – | 0.0535 |
| Late favorite 80-90c | 358 | 82% | -216.55 | -6.2% | -96 | -121 | – | – | 0.1486 |
| Late long-shot fade 1-4c | 1808 | 98% | -217.99 | -1.2% | -129 | -89 | – | – | 0.0248 |
| Late long-shot fade | 1335 | 93% | -357.62 | -2.8% | -279 | -79 | – | – | 0.0634 |
| Late favorite 50-80c | 412 | 59% | -551.67 | -13.6% | -201 | -350 | – | – | 0.2361 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Late favorite 50-80c | 64 | -6.89 | -1.1% |
| Late favorite 90-97c | 164 | -31.19 | -2.0% |
| Late long-shot fade 1-4c | 363 | -37.08 | -1.0% |
| Late favorite 80-90c | 58 | -59.55 | -10.5% |
| Late long-shot fade | 258 | -108.97 | -4.4% |

## Bitcoin: last 1-3 hours

599 events, 2025-03-19 to 2026-11-08.

**Verdict:** Late long-shot fade 1-4c: +87 on 868 trades (+1.0% per $ staked, t=6.15), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Late long-shot fade | 732 | 97% | +101.47 | +1.5% | +40 | +61 | – | – | 0.0288 |
| Late long-shot fade 1-4c | 868 | 100% | +87.37 | +1.0% | +36 | +52 | – | – | 0.0026 |
| Late favorite 90-97c | 201 | 97% | +32.15 | +1.7% | +28 | +4 | – | – | 0.0303 |
| Late favorite 50-80c | 32 | 69% | +1.97 | +0.6% | -29 | +31 | – | – | 0.2165 |
| Late favorite 80-90c | 46 | 87% | -1.96 | -0.4% | -1 | -1 | – | – | 0.116 |

Before 2026-03-13 (fresh test: strategies were picked on later data)

| Strategy | Trades | P&L | Return/$ |
|---|---|---|---|
| Late favorite 90-97c | 170 | +39.01 | +2.4% |
| Late long-shot fade 1-4c | 156 | +19.08 | +1.2% |
| Late long-shot fade | 238 | +17.95 | +0.8% |
| Late favorite 80-90c | 41 | -8.95 | -2.2% |
| Late favorite 50-80c | 28 | -12.99 | -4.7% |

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
