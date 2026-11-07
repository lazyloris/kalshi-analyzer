"""All settings in one place. Change one thing at a time and bump a book's version when you do."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DASHBOARD_DATA = ROOT / "dashboard" / "data"
REPORTS_DIR = ROOT / "reports" / "weekly"

# Public data, no account or key needed.
KALSHI_API = "https://api.elections.kalshi.com/trade-api/v2"
NWS_API = "https://api.weather.gov"
COINBASE_API = "https://api.exchange.coinbase.com"
USER_AGENT = "kalshi-analyzer paper-trading research (github.com/lazyloris/kalshi-analyzer)"

FEE_RATE = 0.07

# Rough hours from a market's close until Kalshi posts the result (so you know when to check back).
# Weather waits for the NWS daily climate report the next morning; 5pm prices settle within the hour.
# Estimates, refined once we see real settle times.
SETTLE_DELAY_HOURS = {"weather": 8, "crypto": 1, "fade": 12}  # Kalshi taker fee: ceil(0.07 * contracts * p * (1-p)) to the cent

# Settlement stations (NWS Daily Climate Report). Used to ask NWS for the point forecast.
STATIONS = {
    "NY":   {"city": "New York",     "station": "KNYC", "lat": 40.7789, "lon": -73.9692,  "tz": "America/New_York"},
    "PHIL": {"city": "Philadelphia", "station": "KPHL", "lat": 39.8721, "lon": -75.2407,  "tz": "America/New_York"},
    "MIA":  {"city": "Miami",        "station": "KMIA", "lat": 25.7881, "lon": -80.3169,  "tz": "America/New_York"},
    "CHI":  {"city": "Chicago",      "station": "KMDW", "lat": 41.7861, "lon": -87.7522,  "tz": "America/Chicago"},
    "AUS":  {"city": "Austin",       "station": "KAUS", "lat": 30.1831, "lon": -97.6799,  "tz": "America/Chicago"},
    "DEN":  {"city": "Denver",       "station": "KDEN", "lat": 39.8466, "lon": -104.6562, "tz": "America/Denver"},
    "LAX":  {"city": "Los Angeles",  "station": "KLAX", "lat": 33.9382, "lon": -118.3866, "tz": "America/Los_Angeles"},
}

# Shared trading rules. A book can override any of these in its "rules".
DEFAULT_RULES = {
    "MIN_EDGE": 0.08,             # model chance minus (price + fee per contract) must be >= 8 cents
    "MIN_PRICE": 0.05,            # skip lottery tickets
    "MAX_PRICE": 0.90,            # skip near-certainties
    "MAX_SPREAD": 0.10,           # skip markets with a bid/ask spread wider than 10 cents
    "MIN_LEAD_HOURS": 6,          # stop buying this many hours before the outcome is mostly known
    "MAX_POSITIONS_PER_EVENT": 2,
    "STAKE_DOLLARS": 10.0,        # paper dollars per trade
}

# Each book trades separately with its own $1,000 paper bankroll, ledger, stats and scorecard.
BOOKS = {
    "weather_high": {
        "name": "Weather: daily highs", "short": "Highs", "kind": "weather", "extreme": "high",
        "version": "weather-v1", "bankroll": 1000.0, "unit": "F",
        "series": {"KXHIGHNY": "NY", "KXHIGHPHIL": "PHIL", "KXHIGHMIA": "MIA", "KXHIGHCHI": "CHI",
                   "KXHIGHAUS": "AUS", "KXHIGHDEN": "DEN", "KXHIGHLAX": "LAX"},
        # Normal(forecast + bias, sigma). Sigma (deg F) by days ahead: starting guesses, measured weekly.
        "sigma_by_lead_days": {0: 2.0, 1: 2.5, 2: 3.2},
        "bias": {},          # e.g. {"KXHIGHDEN": -1.0} once data shows NWS runs warm/cold
        "peak_hour": 16,     # highs usually happen mid-afternoon local time
        "rules": {},
    },
    "weather_low": {
        "name": "Weather: daily lows", "short": "Lows", "kind": "weather", "extreme": "low",
        "version": "weather-low-v1", "bankroll": 1000.0, "unit": "F",
        "series": {"KXLOWTNYC": "NY", "KXLOWTPHIL": "PHIL", "KXLOWTMIA": "MIA", "KXLOWTCHI": "CHI",
                   "KXLOWTAUS": "AUS", "KXLOWTDEN": "DEN", "KXLOWTLAX": "LAX"},
        "sigma_by_lead_days": {0: 2.0, 1: 2.5, 2: 3.2},
        "bias": {},
        "peak_hour": 6,      # lows usually happen around sunrise
        "rules": {},
    },
    "bitcoin": {
        "name": "Crypto: Bitcoin 5pm price", "short": "Bitcoin", "kind": "crypto", "asset": "BTC-USD",
        "version": "crypto-v1", "bankroll": 1000.0, "unit": "$",
        "series": {"KXBTCD": "BTC"},
        "event_suffix": "17",          # only the daily 5pm ET contracts, not every hourly one
        "fallback_vol": 0.50,          # yearly volatility if live estimate fails (guess)
        "rules": {"MIN_LEAD_HOURS": 2},
    },
    "gold": {
        "name": "Commodity: gold 5pm price", "short": "Gold", "kind": "crypto", "asset": "PAXG-USD",
        "version": "gold-v1", "bankroll": 1000.0, "unit": "$",
        # Price proxy: PAXG on Coinbase is a token backed 1:1 by gold. It can sit slightly above or
        # below spot gold, so watch the forecast-bias stats for a constant gap.
        "series": {"KXGOLDD": "GOLD"},
        "event_suffix": "17",
        "fallback_vol": 0.18,
        "rules": {"MIN_LEAD_HOURS": 2},
    },
    "trending": {
        "name": "Trending: Spotify, Netflix, apps, YouTube, Steam", "short": "Trending", "kind": "fade",
        "version": "fade-v1", "bankroll": 1000.0, "unit": "",
        # No forecast exists for these, so this book tests a different rule: cheap long shots
        # (YES at 3-10c) tend to be overpriced, so buy NO on them.
        "series": {"KXSPOTIFYARTIST": "Spotify artist #1", "KXNETFLIXRANKING": "Netflix #1",
                   "KXAPPRANKFREE2": "Top free app", "KXYTDAILYTOPVIDEO": "Top YouTube video",
                   "KXTOPSELLERS": "Steam top seller"},
        "fade_min_yes": 0.03, "fade_max_yes": 0.10,
        "rules": {"MAX_PRICE": 0.97, "MIN_LEAD_HOURS": 2, "MAX_SPREAD": 0.05},
    },
}
ASSET_NAMES = {"BTC": "Bitcoin", "ETH": "Ethereum", "GOLD": "Gold"}


def rules(book_id):
    return {**DEFAULT_RULES, **BOOKS[book_id].get("rules", {})}


def paths(book_id):
    d = DATA_DIR / book_id
    return {
        "dir": d, "trades": d / "trades.csv", "forecasts": d / "forecasts.csv",
        "actuals": d / "actuals.csv", "snapshots": d / "snapshots",
        "dash": DASHBOARD_DATA / book_id, "reports": REPORTS_DIR / book_id,
    }
