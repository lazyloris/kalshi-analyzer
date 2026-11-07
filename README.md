# kalshi-analyzer

A paper-trading bot for Kalshi's **daily high temperature** markets. Every hour it:

1. Pulls live prices for 7 cities (NYC, Philadelphia, Miami, Chicago, Austin, Denver, LA) from Kalshi's public API.
2. Pulls the National Weather Service forecast high for each settlement station.
3. Turns the forecast into a probability for every temperature bracket and **paper-buys** a side when the price is off by at least 8 cents after fees.
4. Settles finished trades, writes a plain-English reason each one won or lost, and updates the stats.
5. Saves everything to this repo (`data/`, `reports/`, `dashboard/data/`), and the Vercel dashboard shows it.

Fake money on real prices. A learning project, **not financial advice**. No Kalshi account or API key needed yet.

## The rule (weather-v1)

- Model: the actual high is Normal(NWS forecast, sigma). Sigma is 2.0°F same day, 2.5°F one day ahead, 3.2°F two days ahead (starting guesses; the weekly report measures the real numbers).
- Buy YES or NO when `model chance - (ask + fee per contract) >= 8¢`.
- Skip if the price is under 5¢ or over 90¢, the spread is over 10¢, or it's within 6 hours of the afternoon high.
- At most 2 trades per city-day, never re-buy the same market, $10 paper per trade, hold to settlement.

All settings live in `kalshi_analyzer/config.py`. **Change one thing at a time and bump `STRATEGY_VERSION`** so results stay comparable.

## How it learns: why each trade won or lost

Every settled trade gets a cause tag and a sentence:

| Cause | Meaning |
|---|---|
| `forecast_right` | Forecast was close, market had it mispriced. This is the edge we want. |
| `lucky` | Won despite a big forecast miss. Doesn't count as skill. |
| `close_call` | Lost by 1°F or less at a bracket edge. Normal noise. |
| `forecast_miss` | Forecast off by over 1.5 sigma. Repeats in one city mean a bias fix. |
| `market_smarter` | Ordinary forecast error, but the market's price was closer. |

The stats split wins and losses by cause, city, edge, entry price, bracket distance from the forecast, days ahead, and YES/NO. They also show **calibration** (does "60%" win 60% of the time?), **Brier score** for the model vs market prices, and **NWS forecast bias per city**. Weekly reports end with ranked suggestions for the next single rule change. Nothing changes on its own.

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

**Copy results into Obsidian:** double-click `tools\sync_obsidian.bat`. It pulls the latest results and writes `Live Status.md` plus a `Scorecards` folder into `D:\Obsidian_Vaults\Projects\Kalshi Trader`.

## Dashboard on Vercel

1. vercel.com, then **Add New**, then **Project**, then import `lazyloris/kalshi-analyzer`.
2. Set **Root Directory** to `dashboard`. Framework preset: **Other**. No build command.
3. Deploy. Each hourly commit redeploys it (about 24 deploys a day, under the free plan's limit).

To preview locally: `cd dashboard && python -m http.server` and open http://localhost:8000.

## Files

```
kalshi_analyzer/   config, Kalshi + NWS clients, model, strategy, settlement, explanations, stats, reports
data/              trades.csv, forecasts.csv, actuals.csv, snapshots/<day>.csv (every price seen)
reports/weekly/    YYYY-Www.md scorecards (Obsidian-ready)
dashboard/         static site + data/summary.json, data/trades.json
tools/             sync_obsidian.py / .bat
```
