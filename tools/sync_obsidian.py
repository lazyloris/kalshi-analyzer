"""Copy the latest scorecards and a status note into your Obsidian vault.

Run on your laptop from a clone of this repo:
    python tools/sync_obsidian.py "D:\\Obsidian_Vaults\\Projects\\Kalshi Trader"
It runs `git pull` first so you get the newest hourly results.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    vault = Path(sys.argv[1] if len(sys.argv) > 1 else r"D:\Obsidian_Vaults\Projects\Kalshi Trader")
    subprocess.run(["git", "-C", str(ROOT), "pull", "--quiet"], check=False)
    dest = vault / "Scorecards"
    dest.mkdir(parents=True, exist_ok=True)
    for f in sorted((ROOT / "reports" / "weekly").glob("*.md")):
        shutil.copy2(f, dest / f.name)
    s = json.loads((ROOT / "dashboard" / "data" / "summary.json").read_text(encoding="utf-8"))
    t = s.get("totals", {})
    lines = [
        "---", "project: Kalshi Trader", "tags: [status, trading]", f"updated: {s['generated_at'][:10]}", "---", "",
        "# Live status", "",
        f"Synced from GitHub. Last bot run: {s['generated_at']} (UTC). Strategy: {s['strategy_version']}.", "",
        f"- Paper bankroll: **${s['bankroll']:.2f}** (started $1000)",
        f"- Settled trades: {t.get('n', 0)}, open: {s['open_count']}",
    ]
    if t.get("n"):
        lines += [f"- Win rate {t['win_rate']:.0%}, P&L ${t['pnl']:+.2f}, ROI {t['roi']:.0%}",
                  f"- Brier: model {t['brier_model']} vs market {t['brier_market']} (lower is better)"]
    lines += ["", "## Suggested next change", ""]
    lines += [f"{i}. {x['text']}" for i, x in enumerate(s.get("suggestions", [])[:5], 1)] or ["- None yet"]
    lines += ["", "Weekly scorecards: see the Scorecards folder.", ""]
    (vault / "Live Status.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Synced {len(list(dest.glob('*.md')))} scorecards and Live Status.md to {vault}")


if __name__ == "__main__":
    main()
