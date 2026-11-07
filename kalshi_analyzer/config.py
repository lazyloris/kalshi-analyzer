"""All settings in one place. Change one thing at a time and bump STRATEGY_VERSION when you do."""
from pathlib import Path

STRATEGY_VERSION = "weather-v1"

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
SNAPSHOT_DIR = DATA_DIR / "snapshots"
TRADES_CSV = DATA_DIR / "trades.csv"
FORECASTS_CSV = DATA_DIR / "forecasts.csv"
DASHBOARD_DATA = ROOT / "dashboard" / "data"
REPORTS_DIR = ROOT / "reports" / "weekly"

# Public market data (no account needed). Prices are the real exchange's live prices.
KALSHI_API = "https://api.elections.kalshi.com/trade-api/v2"
NWS_API = "https://api.weather.gov"
USER_AGENT = "kalshi-analyzer paper-trading research (github.com/lazyloris/kalshi-analyzer)"

# Daily high temperature markets. Settlement uses the NWS Daily Climate Report for each station.
# Coordinates are the settlement stations, used to ask NWS for the point forecast.
CITIES = {
    "KXHIGHNY":   {"city": "New York",     "station": "KNYC", "lat": 40.7789, "lon": -73.9692,  "tz": "America/New_York"},
    "KXHIGHPHIL": {"city": "Philadelphia", "station": "KPHL", "lat": 39.8721, "lon": -75.2407,  "tz": "America/New_York"},
    "KXHIGHMIA":  {"city": "Miami",        "station": "KMIA", "lat": 25.7881, "lon": -80.3169,  "tz": "America/New_York"},
    "KXHIGHCHI":  {"city": "Chicago",      "station": "KMDW", "lat": 41.7861, "lon": -87.7522,  "tz": "America/Chicago"},
    "KXHIGHAUS":  {"city": "Austin",       "station": "KAUS", "lat": 30.1831, "lon": -97.6799,  "tz": "America/Chicago"},
    "KXHIGHDEN":  {"city": "Denver",       "station": "KDEN", "lat": 39.8466, "lon": -104.6562, "tz": "America/Denver"},
    "KXHIGHLAX":  {"city": "Los Angeles",  "station": "KLAX", "lat": 33.9382, "lon": -118.3866, "tz": "America/Los_Angeles"},
}

# --- Model: actual high ~ Normal(forecast + bias, sigma) ---
# Sigma (deg F) by how many days ahead the target date is. Starting guesses, not measured yet;
# the weekly report measures real forecast error so these can be tuned.
SIGMA_BY_LEAD_DAYS = {0: 2.0, 1: 2.5, 2: 3.2}
CITY_BIAS_F = {}  # e.g. {"KXHIGHDEN": -1.0} once the data shows NWS runs warm/cold for a city

# --- Strategy rules (weather-v1) ---
MIN_EDGE = 0.08            # model probability minus (price + fee) must be at least 8 cents
MIN_PRICE = 0.05           # skip lottery tickets
MAX_PRICE = 0.90           # skip near-certainties (tiny upside)
MAX_SPREAD = 0.10          # skip markets where bid/ask spread is wider than 10 cents
MIN_LEAD_HOURS = 6         # don't trade within 6 hours of the expected afternoon high
MAX_POSITIONS_PER_EVENT = 2
STAKE_DOLLARS = 10.0       # paper dollars per trade
STARTING_BANKROLL = 1000.0
FEE_RATE = 0.07            # Kalshi taker fee: ceil(0.07 * contracts * p * (1-p)) to the cent
