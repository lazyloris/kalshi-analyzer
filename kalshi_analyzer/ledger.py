"""Plain CSV files, so every change is visible in git history."""
import csv
from pathlib import Path

TRADE_FIELDS = [
    "trade_id", "strategy_version", "opened_at", "series", "city", "ticker", "event_ticker",
    "target_date", "bracket", "strike_type", "floor", "cap", "side", "contracts", "price", "fee",
    "cost", "model_p", "market_p", "edge", "forecast_high", "sigma", "lead_hours", "lead_days",
    "distance_f", "spread", "volume", "status", "result", "actual_high", "won", "payout", "pnl",
    "forecast_error", "cause", "why", "closed_at",
]
SNAPSHOT_FIELDS = [
    "time", "series", "ticker", "target_date", "strike_type", "floor", "cap", "yes_bid", "yes_ask",
    "no_bid", "no_ask", "volume", "forecast_high", "sigma", "model_p",
]
FORECAST_FIELDS = ["time", "series", "target_date", "lead_days", "forecast_high"]
ACTUAL_FIELDS = ["series", "target_date", "actual_high", "approx", "source"]


def read(path: Path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


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
