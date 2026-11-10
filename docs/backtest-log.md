# Backtest log

One entry per backtest run that led to a decision. Raw results for the latest run are in
`reports/backtest.md` and on the dashboard's Backtest page. Git history has every weekly run.

How to read the numbers: flat $10 per trade at the ask plus the Kalshi taker fee, held to
settlement. "Return per $" is P&L divided by money staked. A strategy counts only if it made
money in **both halves** of the period with 30+ trades.

---

## 2026-11-08: first backtest, v1 to v2

- **Data:** Mar 12 to Nov 7, 2026. Highs had 1,677 events, lows 1,685, Bitcoin 239 (5pm ET only, strikes within 4% of the price).
- **Entries tested:** highs at 8am on the day and 10am the day before. Lows at 8pm and 10am the day before. Bitcoin 8h and 4h before the close.
- **Forecasts:** Open-Meteo NBM runs made 1-2 days earlier. These are staler than live NWS forecasts, so the weather results lean pessimistic.

| Book | Best | Worst | Live v1 equivalent |
|---|---|---|---|
| Highs | Market favorite, +$8 / 2,208 trades (0%) | v2 calibrated, -24.8% | v1, -20.7% |
| Lows | Long-shot fade, +$135 / 2,489 (+0.6%, but lost in the 2nd half) | v1, -27.2% | v1, -27.2% |
| Bitcoin | Vol x0.5, +$360 / 711 (+5.2%, both halves, t=2.75) | Blend, -43.5% | v1, -29.8% |

**Findings**
- Weather markets are well calibrated, and our forecast model's accuracy score (Brier) is worse than the market's on every strategy. A sigma sweep (0.6x-1.5x) and a blend sweep (0-75% market weight) were all negative.
- NBM daily max/min from hourly values runs about 1.5-2F cold on highs and warm on lows. The learned bias absorbs this.
- Bitcoin YES long shots are overpriced and favorites are underpriced (a favorite-longshot bias). A lower volatility exploits that.
- Bug fixed during this run: a 1-hour look-ahead in Coinbase prices had inflated Bitcoin to +39%.

**Decision (v2):** weather books switch to the long-shot fade while forecasts keep being logged. Bitcoin and gold use vol x0.5. All books reset.

**Next ideas to test:** a fresher forecast source for weather (live NWS hourly plus same-day observations); Bitcoin vol x0.5 with the fade combined; a gold backtest; trending fade on settled history.

---

## 2026-11-08: market scanner, first run

- **Data:** the 115 most-traded series across 10 categories (Sports 76, Commodities 6, Economics 6, Weather 6, Financials 5, Science 5, Mentions 4, Politics 3, Elections 2, Entertainment 2). Sampled 10 recent events each (about 45 days), giving 27,569 price snapshots at 24h, 6h and 1h before close.
- **Arbitrage:** 0 real opportunities in 351 one-winner events. The first run showed 162, but those were false positives from ladders where several markets can win. Fixed by only using events Kalshi marks mutually exclusive.
- **Sports:** very well calibrated, so it's hard to beat on price alone. The fade was -1.3%, favorites -2.9%, and the price-correction rule -19.5% on the holdout.
- **Commodities (gold, oil):** the same pattern as Bitcoin. Mid-priced YES on price ranges wins less often than priced (25-35c contracts won about 17%), and favorites win more (94c+ won 100%). This points to markets overpricing big moves.
- **Entry timing:** buying favorites 24h out lost 4.8%. In the last hour it made +1.8% (90% range -0..+4). That's borderline and needs care, because the last hour can overlap with games already underway.
- **Price-correction rule (holdout):** failed in Sports. Too few trades elsewhere to judge.

**Decision:** no live change. Next, test the Bitcoin-style model (lognormal with reduced volatility) on other price markets: gold, WTI and Brent oil, Ethereum, and S&P 500 / Nasdaq daily ranges, with full history.

---

## 2026-11-09: other price markets (run 42569514706, main)

- **Data:** Mar 13 to Nov 8, 2026. Bitcoin and weather were re-run on the same history. Ethereum (KXETHD, 5pm events only, Coinbase prices) had 235 events.
- **Yahoo blocked us:** gold, silver, WTI, Brent, natural gas, S&P 500 and Nasdaq all got HTTP 429 (Too Many Requests) from Yahoo on GitHub's servers, so they have no results yet. The options-implied indexes on Yahoo (VIX, OVX, GVZ) are affected too. A data source that allows automated access is needed.
- **Ethereum confirms the Bitcoin pattern:** vol x0.5 with a 5c edge made +$241 on 585 trades (+4.2%/$), and vol x0.5 made +3.7% on 494. Both were profitable in both halves. Full vol (v1) lost 15.8%. The vol sweep is positive from 0.3 to 0.75 and negative at 1.0.
- **Bitcoin (re-run):** vol x0.5 made +$363 on 707 trades (+5.3%), in both halves. Unchanged.
- **Weather:** still no strategy made money in both halves.
- The verdict line picked "Market favorite" (+7.5% on only 50 trades). The more trustworthy result is vol x0.5 with its 10x larger sample.

**Decision:** no live change yet. Next: an Ethereum paper book with vol x0.5 + 5c edge alongside Bitcoin, a replacement price source for commodities and indexes, and the options-implied check (PR #10).

---

## 2026-11-09: options check and extra signals (runs 42591766920 main, 42597467743 branch more-signals)

- **Options-implied volatility (Deribit DVOL) lost.** Bitcoin lost 29%/$ at 1.0x, and the sweep was only positive at 0.6x. Options price bigger moves than Kalshi does. Ethereum x0.85 showed +10.6% on 178 trades, but its neighbouring settings were around zero, so it's treated as noise.
- **Limit orders lost badly** (Bitcoin -11%, Ethereum -15%, weather fade -2%, weather favorite -12 to -19%). Fills only happen when the price moves against us (adverse selection). Keep paying the ask.
- **News days (CPI, jobs, Fed):** skipping them changed almost nothing.
- **Kalshi price-spike fade:** a big loser on crypto (-23%; crypto spikes carry real information), but positive on weather (highs +9.8% on 260 trades, t=1.1; lows +30.5% on 120, t=2.1). Small samples, to watch.
- **Helped on both Bitcoin and Ethereum:**
  - Time-of-day/weekend volatility: BTC +6.2% on 742 trades (t=3.5); its sweep is smooth from 0.5 to 0.75.
  - Skipping markets that just moved 15c+: BTC +7.5%, ETH +6.9%.
  - Trading against the last 24h move (BTC +8.3%, ETH +9.0%). Going with the trend was weak.
- **Combined:**
  - Time-of-day vol x0.5 + skip spikes: BTC +9.2% on 465 trades (t=4.5, last 60 days +4.4%); ETH +7.0% on 301 (t=2.7, last 60 days +8.8%).
  - Adding "against trend": BTC +12.7% on 234 (t=4.9); ETH +11.0% on 163 (t=3.5).
- **Caveat:** about 25 variants were tried on the same data, so part of this gain is selection luck. The only real test is live paper trading.
- The verdict now picks the highest t-stat strategy with 50+ trades that was profitable in both halves.

**Decision (proposed):** paper-trade "time-of-day vol x0.5 + skip spikes" on Bitcoin and Ethereum alongside the current vol x0.5 book, and compare weekly.

## 2026-11-09 — Older-data test (run 42602772002)

**Setup:** Bitcoin and Ethereum history pulled back to 2025-03 (about 600 days; Kalshi KXBTCD/KXETHD history starts around 2025-03-19). We picked strategies on 2026-03-13 onward, then scored them on the year before, which they had never seen.

**Result: the crypto edge did not hold.** On the older data:
- BTC time-of-day vol: -1.8% (775 trades).
- BTC tod + skip spikes: -3.1% (486).
- BTC combo_all: -3.7% (268).
- ETH tod: -1.8% (747).
- ETH combo_tod: -1.2% (469).
- ETH combo_all: -0.3% (259).
- Plain vol x0.5: -2.8% (BTC) and -4.9% (ETH).

Over the full 600 days, BTC tod is +2.1% and combo_all is +4.0%, but the first half lost money and all the profit came from the last 8 months. Weekend-only BTC was +4.1% older (141 trades) and +6.7% overall (230). It's small, and it came out of about 25 variants, so treat it as unproven. The model's Brier score is worse than the market's in every book except BTC weekends.

**Conclusion:** we found no reliable crypto edge. The tod paper books keep running as a free live check, but no live money should follow them. Next research: the weather spike fade (only 8 months of data) and a Polymarket price comparison.

## 2026-11-09 — Older weather test (run 42642594204)

**Setup:** Kalshi weather prices were pulled back about 600 days. Highs go back to 2025-03 (3,731 events). Lows only go back to 2025-12 (2,193 events), because the lows series is newer. Forecasts still only cover 2026-03 onward, so the forecast models have almost no older trades.

**Result: the spike fade did not hold.**
- Daily highs: -6.3% on 224 older trades. The full period is +2.3% on 484, and all of it came from the second half.
- Daily lows: -35% on 32 older trades. That's a tiny sample, but it's negative.
- Long-shot fade: about break-even everywhere (+0.5% older highs, -0.6% older lows).
- Market favorite on older lows: +7.3% on 356 trades, but it's -2.9% over the full period, so that's noise.

**Conclusion:** same story as crypto. Every edge we found on 2026-03 to 2026-11 disappears on the earlier data. Kalshi weather and crypto prices look efficient at hourly resolution after fees.

## 2026-11-09 — Minute-level lag test v2 (run 42697790490, branch minute-lag)

**Setup:** 1-minute Kalshi quotes and 1-minute Coinbase prices over the last 6 hours before 5pm ET, about 400 days, for Bitcoin (KXBTCD) and Ethereum (KXETHD). Strikes within 2% of the price. Signal: the coin moved X% in 5 minutes and Kalshi is below a lognormal fair value by the edge, in the direction of the move. Taker fees are included. Fill delay is 0, 1 or 2 minutes (the order fills at that later quote). There are 72 settings per coin. We report both a per-trade t-stat and a per-day t-stat.

**Result:**
- **BTC: holding to settlement after a 0.2% move, 5c edge, vol x0.5:**
  - No delay: +2.2% on 5,907 trades. t = 3.4 per trade, 2.5 per day.
  - 1-2 minute delay: +1.8%. t = 2.3 per day.
  - Both halves and the older year are positive.
  - Every vol x0.5 row is positive, and every vol x0.75 or x1.0 row loses.
- **ETH:** the same setting is +2.0% on 2,027 trades, but the per-day t is only 0.5, and +1.2% with a 2-minute delay. Positive but not significant.
- **15-minute exit (pure lag capture):** loses in every setting on both coins.

**Conclusion:** this is the first crypto signal that survives the older year and a fill delay, but only on Bitcoin. With 144 settings tried, a per-day t of 2.3 is borderline. It also depends entirely on vol x0.5, which failed at hourly resolution on the older year. Treat it as a candidate for a small paper book, not as proven.

## 2026-11-09 — Swing pairing test v1 (branch minute-lag)

**Setup:** buy the side that dropped D cents in 5 minutes. If it swings back X cents, buy the other side so the pair costs under $1; otherwise hold to settlement. 1-minute quotes over the last 4 hours of trading, sports *GAME series, 90 days.

**Result:** every setting lost, -11.5% to -20%. Locks made +700 to +1,200, but positions that never locked lost more. Coverage was bad: 240 markets, mostly eSoccer (KXESOCCERGAME has 45k markets and filled the download cap). The crypto group had 0 markets because the minute caches weren't restored.

**Fix:** v2 takes major leagues first, caps each series at 400 markets, and restores the crypto minute data.

## 2026-11-09 — Polymarket top-wallet study (wallet-study branch)

**Setup:** Top 30 all-time wallets by P&L, plus swisstony. Read-only public data (Data API v2, CLOB). For each wallet we read the latest 10,000 trades. The copy test buys 150 of their recent resolved buys at the price 1, 10 and 60 minutes later, with a 1c worse fill, held to resolution.

**Findings:**
- **Two kinds of top wallets.** Most of the list are a few huge one-off bets (e.g. Theo4 and Fredi9999 on the 2024 election), which can't be repeated. The rest are high-frequency sports traders: swisstony made 10,000 trades in about two days (2026-08-25 to 08-26), so it's almost certainly a bot.
- **Both-sides buying is real but mixed.** swisstony bought both sides in 43% of its markets. 42% of those pairs cost under $1 (locked profit), but the average pair cost $1.03. RN1 averaged $0.97 with 53% locked.
- **Copying the sports bots loses.** Held to the end, swisstony's own buys were -5%; copying them was -8.7% at 1 or 10 minutes and -14% at 60 minutes. RN1: 0% for them, -15% to -34% for copiers. Their profit comes from pairing sides and trading speed, not from the individual bets.
- **Copying big one-off bettors looks great** (+60% to +140%), but 150 buys there are often 1 to 3 markets, so the real sample is tiny. That's luck or conviction, not a repeatable edge.

**Caveats:** returns are per buy and not weighted by dollars. Position totals from the API were capped and inconsistent, so they were dropped. No fees assumed.

**Next:** the swisstony-style swing pairing (buy one side after a drop, the other side after the opposite swing, aiming for under $1 combined) can be tested on Kalshi 1-minute data for live sports.

## 2026-11-09 — Swing pairing test v2 (run 42716975260, branch minute-lag)

**Setup:** same rules as v1. Major leagues come first, capped at 400 markets per series. That gives 5,220 sports markets: NBA, MLB, NHL, NCAAF, MLS, NCAAMB, NFL and La Liga. It also adds 4,688 Bitcoin and Ethereum daily markets from the minute-lag data.

**Result: it loses everywhere.**
- Sports: -13% to -14.5% in all 9 settings, with t from -14 to -28. 56-72% of trades locked, and the locks made +$18k to +$30k. Trades that never locked lost $31k to $46k.
- Crypto: -11% to -15%. 66-82% locked, with the same pattern.
- Both halves are negative.

**Conclusion:** "buy the dip, lock the other side on the rebound" loses as a taker. The dips that never come back cost more than the locks earn. This is the same adverse selection as before. swisstony-style profits, if real, would need maker fills (earning the spread), which candles can't test. Swing pairing is closed.

## 2026-11-09 — 600-day replay: late entries, Bayesian, fat-tail, exits, volume, combined (run 42689764374)

**Data:** Bitcoin and Ethereum 2025-03 to 2026-11 (about 600 days), weather highs 2025-03 onward, lows 2025-12 onward. The history is now also kept permanently as GitHub release `backtest-data`.

**Results:**
- **Late Bitcoin long-shot fade (NO on 1-4c strikes, 1-3h before close):** +1.0% on 868 trades. It won 867 of them, was positive in every quarter, and was +1.2% on the older year. That's the most consistent result so far, but it's tiny ($87 on about $8,700 staked) and one loss wipes out about 30 wins.
- **Late Bitcoin favorite 90-97c:** +1.7% on 201 (older +2.4%). Small sample.
- **Bayes price-level (95% sure):** BTC +2.6% on 781, profitable in both halves. On the late book it was -2.3% on the older year. Mixed.
- **Fat-tail model:** -0.5% (x0.5) and worse at larger multipliers. No edge.
- **Take-profit / stop-loss exits:** worse than holding in every book (you pay the spread twice).
- **Heavy-volume follow/fade:** noise (weather lows fade -393 in the 2nd half).
- **Combined rolling-best:** BTC +3.0% overall but -0.3% older. Consensus of 3+ strategies: -11% to -14% on weather (the strategies agree when they're all wrong).
- **Volatility check:** BTC's real moves were 1.0-1.4x the 30-day volatility in most quarters. The "calm 2026" theory is wrong.

**Conclusion:** no model-based edge. The one consistent pattern is a structural one: very cheap Bitcoin long shots near the close are slightly overpriced, which is the favorite-longshot bias. It's worth a live paper book at small size.

## 2026-11-10 — Independent review and price-level ladder test (local replay of the `backtest-data` release)

**Setup:** a fresh review session replayed the 600-day Bitcoin/Ethereum/weather history from the GitHub release with no changes to the engine, then ran a new no-model test (`python -m kalshi_analyzer.backtest ladder`, `reports/ladder.md`): for every market, the quote H hours before close goes in a YES-ask bucket, and buying YES or buying NO at that quote is scored per **event** (all strikes of one day count as one bet). Full write-up: `docs/review-2026-11-10.md`.

**Audit results:** no look-ahead found in `quote()`, `crypto_events`, the signals, Bayes, fat-tail, minute or swing code. Fees match Kalshi's published per-order formula; KXBTCD/KXETHD/weather are standard-fee series with no maker fee. Quote staleness is negligible (99.9% of quotes are 0h old). Corrections: the late 1-4c fade lost 2 of 868 trades (both strikes of 2026-05-23), not 1; its per-day t is 3.1, not 6.2, and the event-level confidence interval includes zero. The in-sample crypto winners have per-day t of 2.0-2.8 on Mar-Nov and lost on the older year. With 450+ variants tried, a result needs |t| around 3.5 before it means anything. The hourly cron actually fires every ~6h (10 scheduled runs in 55h).

**New result (candidate, found by scanning ~60 cells per asset, so discount it):** Bitcoin 4h moves are fat-tailed (82% inside 1σ vs 68% for a normal) and the ladder is priced as if normal. Buying YES on favorites 3-4h before the 5pm close: 75-88c made +8.7% on 374 trades (330 days, t_event 4.4, older +5.7%, newer +10.9%, positive 8/8 quarters); 93-96c made +4.4% on 254 (t 5.8, older +4.7%, newer +4.2%, 8/8 quarters). Pooled 75-99c at 4h: +2.7% on 2,114 trades, 4 a day, positive both periods. Mirror: NO on 12-25c at 6h +4.9%. Ethereum shows the same shape weakly (93-96c at 4h +4.4%, t 3.5). 2026-Q4 so far is negative in the pooled cells. Median post-entry volume 10k-58k contracts, so tens of contracts per trade should fill.

**Decision (proposed, no live change in this PR):** stop model work (weather, volatility variants, minute lag, swing); run a pre-registered paper book "BTC favorites 75-88c and 93-96c at 4h and 3h before close" for 60 days with kill criteria written down first; test the maker version from the public trade feed. Engine change: `metrics` now reports `events` and `t_event`, shown in `reports/backtest.md`.

## 2026-11-10: pre-registered paper book "bitcoin_fav" (owner approved)

**Rule (fixed for 60 days, 2026-11-10 to 2027-01-09):** buy YES at the ask on KXBTCD 5pm strikes priced 75-88c or 93-96c, when 3.5-4.5 hours are left, with a spread of 5c or less. $10 a trade, one strike per price band per day (2 at most), held to settlement, taker fee. There's no model.

**Where it comes from:** the 2026-11-10 review's ladder test, which was independently recomputed from the raw history and matched:
- 75-88c at 4h: +8.7% on 374 trades (older year +5.7%, newer +10.9%).
- 93-96c at 4h: +4.4% on 254 trades (older +4.7%, newer +4.2%).
- Pooled 75-96c: +5.8% on 867 trades, day-level t 3.9.

It was found by scanning about 60 cells, so expect it to shrink.

**Kill rules (written before the first trade, checked by code before each new trade):**
- Return per dollar is below 0 once 60 days have passed or 120 trades have settled.
- 3 losing days within any 10 trading days.

**Timing:** a separate workflow (favorites.yml) tries every 15 minutes from 16:00 to 18:59 UTC, because the hourly cron fires only about every 6 hours. It trades only this book.

## 2026-11-10: favorite follow-ups (run 42754016870, branch fav-extra)

**1. Limit order instead of paying the ask** (Kalshi trade feed, 1,142 BTC and 385 ETH entries, all with trade data). Rest a YES bid 1-3c below the ask at the entry time. A fill counts only if a later trade printed below our bid ("through") or a seller hit our price ("touch").
- **BTC 4h, 75-88c:**
  - Taker: +8.7% on 374, +$314.
  - Bid 1-2c lower, through: 80-86% filled, +9.5% to +9.9%, +$286 to +$291.
  - Touch: +10.2% to +10.7%, +$323 to +$333.
- **BTC 4h, 93-96c:**
  - Taker: +4.4%, +$107.
  - Maker: 52-83% filled, +5.5% to +7.6%, +$90 to +$114.
- The filled orders win slightly less often than the ones that miss (adverse selection), but the cheaper price more than pays for it per dollar staked. Total profit is about the same as the taker version. Both years are positive.
- **ETH:** maker is worse than taker (75-88c at 4h: +2-3% vs +4.7%). Adverse selection is stronger there.

**Conclusion:** on Bitcoin a limit order earns more per dollar for about the same total profit, so it's a modest improvement, not a new edge. The pre-registered book stays taker. A maker version can be tested after the 60 days.

**2. Same ladder on other daily price markets** (strikes near the previous settle, so no look-ahead).
- Gold and silver: mostly negative, no pattern.
- WTI oil: mixed, around 0.
- Brent: positive in most cells (+3% to +12% at 3-4h), but small samples: under 100 days, no older year, t up to 2.5.
- Natural gas: mildly positive (+1% to +7%), no cell above t 1.8.
- The S&P (KXINXU) has about 500k markets (hourly events). It used up the time budget, so KXINX, Nasdaq and other coins weren't tested.

**Conclusion:** the favorite pattern is clearly present only in crypto (BTC strongly, ETH at 93-96c). Elsewhere it's weak or missing. This is consistent with the fat-tail explanation for crypto, but it adds no confirmation from other assets.
