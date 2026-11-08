# kalshi-analyzer

A paper-trading bot for Kalshi. Every hour it reads real Kalshi prices, compares them with a simple model, **paper-buys** when the price looks wrong by at least 8 cents after fees, settles finished trades, explains each win or loss, and updates the stats. Everything is saved to this repo and shown on the Vercel dashboard.

Fake money on real prices. A learning project, **not financial advice**. No Kalshi account or API key needed.

## Books (each has its own $1,000 paper bankroll)

| Book | Kalshi markets | Model | Stops buying |
|---|---|---|---|
| `weather_high` | Daily high temp, 7 cities (KXHIGH*) | v2: long-shot fade (NO when YES is 3-10c). The NWS forecast is still logged and bias/sigma learned per city, but the backtest found no model edge over the market | 6h before close |
| `weather_low` | Daily low temp, same cities (KXLOWT*) | Same as highs | 6h before close |
| `bitcoin` | Bitcoin price at 5pm ET (KXBTCD, daily 5pm contracts only) | Lognormal around Coinbase BTC spot, 30-day realized volatility **x0.5** (backtest winner) | 2h before 5pm ET |
| `gold` | Gold price at 5pm ET (KXGOLDD) | Same, using Coinbase PAXG (gold-backed token) as the price (vol x0.5 not yet backtested on gold) | 2h before 5pm ET |
| `trending` | Spotify #1 artist, Netflix #1, top free app, top YouTube video, Steam top seller | No forecast exists, so a different rule: buy NO on long shots priced 3-10c | 2h before close |

Shared rules (per-book overrides in `config.py`): edge >= 8c after fees, price 5-90c (trending NO up to 97c), spread <= 10c, at most 2 trades per event, $10 per trade, hold to settlement.

All settings live in `kalshi_analyzer/config.py`. **Change one thing at a time and bump that book's `version`** so results stay comparable.

### Backtest
`python -m kalshi_analyzer.backtest` (or GitHub, then **Actions**, then **Backtest**, then **Run workflow**; it also runs every Monday) replays months of real Kalshi hourly prices and settlements against archived NWS-blend (NBM) forecasts and Coinbase prices, for several strategies per book. Results: the dashboard's **Backtest** page, `reports/backtest.md`, and `docs/backtest-log.md` (one entry per decision). Downloads are cached by GitHub Actions, so only new days are fetched. What went wrong with v1 is in `docs/postmortem-2026-11-08.md`.

### When to check back
Every trade records when its market closes and when the result should land (close + Kalshi's usual settle delay: about 8h for weather, which waits for the next-morning NWS report; about 1h for 5pm price markets). Each hour the bot also values open trades at the current bid ("if sold now") next to the model's expected P&L. The dashboard shows a **When to check back** table and a "Results by" column. Delays are estimates in `SETTLE_DELAY_HOURS` in `config.py`.

### Restart a book
GitHub, then **Actions**, then **Reset a book**, then **Run workflow**, then pick a book (or `all`). Its trades move to `data/<book>/archive/` and it starts again at $1,000. Price history is kept. From a laptop: `python -m kalshi_analyzer reset bitcoin`.

## How it learns: why each trade won or lost

Every settled trade gets a cause tag and a sentence:

| Cause | Meaning |
|---|---|
| `forecast_right` | Forecast was close, market had it mispriced. This is the edge we want. |
| `lucky` | Won despite a big forecast miss. Doesn't count as skill. |
| `close_call` | Lost by 1°F or less at a bracket edge. Normal noise. |
| `forecast_miss` | Forecast off by over 1.5 sigma. Repeats in one city mean a bias fix. |
| `market_smarter` | Ordinary forecast error, but the market's price was closer. |
| `longshot_held` / `longshot_hit` | Trending book: the long shot missed (we won) or came in (we lost). |

The stats split wins and losses by cause, city, edge, entry price, bracket distance from the forecast (in sigmas), days ahead, and YES/NO. They also show **calibration** (does "60%" win 60% of the time?), **Brier score** for the model vs market prices, and **NWS forecast bias per city**. Weekly reports end with ranked suggestions for the next single rule change. Nothing changes on its own.

## Running it

**In the cloud (default):** `.github/workflows/hourly.yml` runs every hour at :17. To run it now: GitHub, then **Actions**, then **Hourly paper trade**, then **Run workflow**. That uses about 720 of the 2,000 free Actions minutes a month for a private repo.

**On your laptop (optional, for testing):**

```bat
git clone https://github.com/lazyloris/kalshi-analyzer
cd kalshi-analyzer
pip install -r requirements.txt
python -m kalshi_analyzer run      :: one live run, writes data\ and reports\
python -m kalshi_analyzer report   :: rebuild stats and dashboard data only
python -m pytest -q                :: tests
```

Don't run it on the laptop and on GitHub at the same time with the same repo, or you'll get git conflicts in `data/`.

**Copy results into Obsidian:** double-click `tools\sync_obsidian.bat`. It pulls the latest results and writes `Live Status.md` (all books) plus a `Scorecards/<book>` folder into `D:\Obsidian_Vaults\Projects\Kalshi Trader`.

## Dashboard on Vercel

1. vercel.com, then **Add New**, then **Project**, then import `lazyloris/kalshi-analyzer`.
2. Set **Root Directory** to `dashboard`. Framework preset: **Other**. No build command.
3. Deploy. Each hourly commit redeploys it (about 24 deploys a day, under the free plan's limit).

To preview locally: `cd dashboard && python -m http.server` and open http://localhost:8000.

## Files

```
kalshi_analyzer/          config, Kalshi/NWS/Coinbase clients, models, strategy, settlement, explanations, stats, reports
data/<book>/              trades.csv, forecasts.csv (weather), actuals.csv, snapshots/<day>.csv, archive/ (after resets)
reports/weekly/<book>/    YYYY-Www.md scorecards (Obsidian-ready)
dashboard/                static site; data/books.json + data/<book>/summary.json, trades.json
tools/                    sync_obsidian.py / .bat
```
