# Backtest (2026-11-08)

Flat $10 per trade at the ask plus Kalshi fees, held to settlement. Prices are real hourly Kalshi quotes. Forecasts are archived NWS-blend (NBM) runs 1-2 days old. Bias/sigma learned only from earlier days.

## Weather: daily highs

1677 events, 2026-03-12 to 2026-11-07.

**Verdict:** No strategy made money in both halves with 30+ trades. Least bad: Market favorite YES (no model) (+8 on 2208 trades).

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Market favorite YES (no model) | 2208 | 53% | +7.98 | +0.0% | -89 | +97 | – | – | 0.2419 |
| Long-shot fade (no model) | 2768 | 95% | -68.67 | -0.3% | -75 | +6 | – | – | 0.0469 |
| Forecast bracket YES | 735 | 10% | -3360.27 | -43.4% | -1690 | -1670 | 33% | 0.1468 | 0.0918 |
| v2 + disagreement cap | 3202 | 33% | -8329.30 | -25.4% | -4199 | -4130 | 54% | 0.2009 | 0.1571 |
| v2 + 50% market blend | 3540 | 31% | -9207.15 | -25.3% | -4240 | -4967 | 46% | 0.1901 | 0.1643 |
| v1 (what we ran live) | 4382 | 34% | -9286.34 | -20.7% | -4213 | -5074 | 63% | 0.2625 | 0.1645 |
| v2 calibrated | 3994 | 32% | -10152.65 | -24.8% | -4652 | -5501 | 58% | 0.2441 | 0.167 |

Sweep: sigma

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 3975 | -9458.19 | -23.3% |
| 0.8 | 3836 | -9814.62 | -24.9% |
| 1.0 | 3994 | -10152.65 | -24.8% |
| 1.25 | 4254 | -8793.22 | -20.2% |
| 1.5 | 4403 | -7760.07 | -17.3% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 4874 | -11626.06 | -23.3% |
| blend 0.0, edge 0.05 | 4568 | -11009.66 | -23.5% |
| blend 0.0, edge 0.08 | 3994 | -10152.65 | -24.8% |
| blend 0.25, edge 0.03 | 4618 | -11386.96 | -24.0% |
| blend 0.25, edge 0.05 | 4135 | -10474.74 | -24.7% |
| blend 0.25, edge 0.08 | 3232 | -8685.58 | -26.2% |
| blend 0.5, edge 0.03 | 3976 | -10259.10 | -25.1% |
| blend 0.5, edge 0.05 | 3062 | -8196.11 | -26.0% |
| blend 0.5, edge 0.08 | 1841 | -4552.96 | -24.0% |
| blend 0.75, edge 0.03 | 1836 | -5127.04 | -27.1% |
| blend 0.75, edge 0.05 | 783 | -1966.19 | -24.3% |
| blend 0.75, edge 0.08 | 208 | -695.48 | -32.2% |

Forecast error (actual minus NBM forecast)

| City | Entry | n | Bias | RMSE |
|---|---|---|---|---|
| Austin | day before 10am | 239 | +1.86 | 3.29 |
| Austin | same day 8am | 241 | +1.56 | 2.93 |
| Chicago | day before 10am | 239 | +1.44 | 3.43 |
| Chicago | same day 8am | 237 | +1.26 | 2.86 |
| Denver | day before 10am | 240 | +1.74 | 3.41 |
| Denver | same day 8am | 237 | +1.67 | 2.97 |
| Los Angeles | day before 10am | 238 | +2.30 | 3.89 |
| Los Angeles | same day 8am | 240 | +2.31 | 3.63 |
| Miami | same day 8am | 240 | +2.05 | 2.67 |
| New York | same day 8am | 237 | -0.26 | 2.46 |
| Philadelphia | same day 8am | 237 | +1.74 | 2.89 |

## Weather: daily lows

1685 events, 2026-03-12 to 2026-11-07.

**Verdict:** No strategy made money in both halves with 30+ trades. Least bad: Long-shot fade (no model) (+135 on 2489 trades).

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Long-shot fade (no model) | 2489 | 96% | +134.94 | +0.6% | +170 | -36 | – | – | 0.034 |
| Market favorite YES (no model) | 1740 | 47% | -822.86 | -4.7% | -76 | -747 | – | – | 0.2381 |
| Forecast bracket YES | 538 | 14% | -1727.60 | -30.6% | -1015 | -713 | 34% | 0.1607 | 0.12 |
| v2 + 50% market blend | 1838 | 29% | -3880.06 | -20.4% | -1119 | -2762 | 41% | 0.1566 | 0.1415 |
| v2 calibrated | 2549 | 31% | -5661.71 | -21.6% | -1537 | -4125 | 52% | 0.2002 | 0.1494 |
| v2 + disagreement cap | 2219 | 31% | -6125.05 | -26.9% | -2087 | -4038 | 50% | 0.1778 | 0.1427 |
| v1 (what we ran live) | 3761 | 32% | -10502.00 | -27.2% | -4465 | -6037 | 57% | 0.2266 | 0.1476 |

Sweep: sigma

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.6 | 3307 | -5191.07 | -15.4% |
| 0.8 | 2615 | -4948.25 | -18.5% |
| 1.0 | 2549 | -5661.71 | -21.6% |
| 1.25 | 2972 | -6757.75 | -22.1% |
| 1.5 | 3489 | -8681.92 | -24.3% |

Sweep: blend

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| blend 0.0, edge 0.03 | 3929 | -9156.45 | -22.7% |
| blend 0.0, edge 0.05 | 3369 | -8073.81 | -23.3% |
| blend 0.0, edge 0.08 | 2549 | -5661.71 | -21.6% |
| blend 0.25, edge 0.03 | 3363 | -7951.52 | -23.0% |
| blend 0.25, edge 0.05 | 2636 | -5773.55 | -21.3% |
| blend 0.25, edge 0.08 | 1695 | -3533.39 | -20.2% |
| blend 0.5, edge 0.03 | 2301 | -5016.64 | -21.1% |
| blend 0.5, edge 0.05 | 1472 | -3072.47 | -20.2% |
| blend 0.5, edge 0.08 | 713 | -511.91 | -6.9% |
| blend 0.75, edge 0.03 | 613 | -584.70 | -9.2% |
| blend 0.75, edge 0.05 | 242 | -526.36 | -20.9% |
| blend 0.75, edge 0.08 | 53 | -353.82 | -64.0% |

Forecast error (actual minus NBM forecast)

| City | Entry | n | Bias | RMSE |
|---|---|---|---|---|
| Austin | day before 10am | 239 | -2.68 | 4.15 |
| Austin | day before 8pm | 241 | -2.78 | 4.01 |
| Chicago | day before 10am | 239 | -1.62 | 3.04 |
| Chicago | day before 8pm | 241 | -1.39 | 2.67 |
| Denver | day before 10am | 240 | -3.94 | 5.21 |
| Denver | day before 8pm | 241 | -3.82 | 5.06 |
| Los Angeles | day before 10am | 239 | +0.36 | 1.72 |
| Los Angeles | day before 8pm | 241 | +0.48 | 1.61 |
| Miami | day before 8pm | 239 | -1.00 | 2.39 |
| New York | day before 8pm | 241 | -1.68 | 2.71 |
| Philadelphia | day before 8pm | 241 | +0.42 | 2.21 |

## Crypto: Bitcoin 5pm price

239 events, 2026-03-13 to 2026-11-07.

**Verdict:** Vol x0.5: +3257 on 828 trades (+39.4% per $ staked), profitable in both halves.

| Strategy | Trades | Win % | P&L | Return/$ | 1st half | 2nd half | Claimed win % | Brier model | Brier market |
|---|---|---|---|---|---|---|---|---|---|
| Vol x0.5 | 828 | 77% | +3256.70 | +39.4% | +1651 | +1605 | 85% | 0.1688 | 0.2057 |
| Vol x0.75 | 730 | 66% | +2645.42 | +35.9% | +1484 | +1162 | 71% | 0.1664 | 0.2091 |
| v1 + 50% market blend | 589 | 46% | +1868.41 | +30.7% | +1309 | +559 | 42% | 0.1726 | 0.204 |
| v1 (what we ran live) | 671 | 45% | +1544.49 | +22.3% | +1162 | +383 | 53% | 0.172 | 0.1996 |
| Long-shot fade (no model) | 775 | 97% | +127.56 | +1.7% | +61 | +66 | – | – | 0.0258 |

Sweep: vol

| Setting | Trades | P&L | Return/$ |
|---|---|---|---|
| 0.4 | 869 | +3066.39 | +35.4% |
| 0.5 | 828 | +3256.70 | +39.4% |
| 0.6 | 793 | +2937.18 | +37.0% |
| 0.75 | 730 | +2645.42 | +35.9% |
| 1.0 | 671 | +1544.49 | +22.3% |
| 1.25 | 731 | +591.31 | +7.8% |
