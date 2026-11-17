# Bitcoin favorite: falling-market filter (2026-11-17T03:18+00:00)

Main test, picked before looking: skip the day when BTC is down 3% or more over the 24h before entry.

| Set | Trades | Days | Win | P&L | Return/$ | Older | Newer | Losing days | Worst day | t (day) |
|---|---|---|---|---|---|---|---|---|---|---|
| All trades (no filter) | 638 | 380 | 93% | $378.57 | +6.2% | +5.1% | +6.9% | 36 | $-38.52 | 4.19 |
| Kept (filter on) | 576 | 346 | 93% | $344.33 | +6.2% | +4.2% | +7.7% | 34 | $-19.51 | 4.31 |
| Skipped (down >=3%) | 62 | 34 | 92% | $34.24 | +5.8% | +15.6% | +0.8% | 2 | $-38.52 | 0.8 |

## Other cutoffs (context only, don't pick the best)

| Set | Trades | Days | Win | P&L | Return/$ | Older | Newer | Losing days | Worst day | t (day) |
|---|---|---|---|---|---|---|---|---|---|---|
| Skip when down >= 2% | 506 | 309 | 92% | $259.1 | +5.3% | +3.2% | +6.8% | 33 | $-19.51 | 3.31 |
| Skip when down >= 4% | 620 | 369 | 94% | $406.94 | +6.8% | +4.8% | +8.2% | 34 | $-19.51 | 5.05 |
| Skip when down >= 5% | 632 | 376 | 93% | $369.4 | +6.1% | +4.9% | +6.9% | 36 | $-38.52 | 4.09 |

## Kill-rule calibration (60-day stretches of history)

Windows: 329. Old rule (3 losing days in 10) would have tripped in 0.307 of them.
Worst drop from peak per window: median $18.99, 90th $27.53, 95th $28.03, 99th $28.03, max $49.360000000000014.

## By BTC 24h change

| Set | Trades | Days | Win | P&L | Return/$ | Older | Newer | Losing days | Worst day | t (day) |
|---|---|---|---|---|---|---|---|---|---|---|
| -100% to -5% | 6 | 4 | 100% | $9.17 | +16.1% | +13.5% | +21.4% | 0 | $0.65 | 3.29 |
| -5% to -3% | 56 | 30 | 91% | $25.07 | +4.7% | +16.1% | -0.3% | 2 | $-38.52 | 0.59 |
| -3% to -1% | 139 | 80 | 95% | $108.87 | +8.2% | +4.7% | +11.3% | 6 | $-18.82 | 3.22 |
| -1% to +1% | 242 | 154 | 93% | $152.89 | +6.6% | +2.9% | +8.4% | 13 | $-19.51 | 2.81 |
| +1% to +3% | 125 | 77 | 90% | $18.53 | +1.5% | +3.1% | +0.2% | 13 | $-10.08 | 0.47 |
| +3% to +100% | 70 | 35 | 96% | $64.04 | +9.5% | +7.9% | +11.1% | 2 | $-19.03 | 2.38 |
