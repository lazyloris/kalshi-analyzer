"""Plain CSV files, so every change is visible in git history."""
import csv
from pathlib import Path

TRADE_FIELDS = [
    "trade_id", "book", "strategy_version", "opened_at", "series", "city", "ticker", "event_ticker",
    "target_date", "bracket", "strike_type", "floor", "cap", "side", "contracts", "price", "fee",
    "cost", "model_p", "raw_model_p", "market_p", "edge", "forecast", "sigma", "unit", "lead_hours", "lead_days",
    "distance", "spread", "volume", "status", "result", "actual", "won", "payout", "pnl",
    "forecast_error", "cause", "why", "closed_at",
    "closes_at", "results_by", "expected_pnl", "mark_price", "mark_pnl", "marked_at", "cap_key",
]
SNAPSHOT_FIELDS = [
    "time", "series", "ticker", "target_date", "strike_type", "floor", "cap", "yes_bid", "yes_ask",
    "no_bid", "no_ask", "volume", "forecast", "sigma", "model_p",
]
FORECAST_FIELDS = ["time", "series", "target_date", "lead_days", "forecast"]
ACTUAL_FIELDS = ["series", "target_date", "actual", "approx", "source"]

# Column names from weather-v1 files, renamed when read.
RENAMES = {"forecast_high": "forecast", "actual_high": "actual", "distance_f": "distance"}


def read(path: Path, defaults=None):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for old, new in RENAMES.items():
            if old in r:
                r.setdefault(new, r.pop(old))
        for k, v in (defaults or {}).items():
            if not r.get(k):
                r[k] = v
    return rows


def write(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def append(path: Path, rows, fields):
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        if new:
            w.writeheader()
        w.writerows(rows)
