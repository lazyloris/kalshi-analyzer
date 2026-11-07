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
    idx = json.loads((ROOT / "dashboard" / "data" / "books.json").read_text(encoding="utf-8"))
    lines = ["---", "project: Kalshi Trader", "tags: [status, trading]", f"updated: {idx['generated_at'][:10]}", "---", "",
             "# Live status", "", f"Synced from GitHub. Last bot run: {idx['generated_at']} (UTC).",
             "Dashboard: https://kalshi-analyzer-dashboard.vercel.app/", "",
             "| Book | Bankroll | Settled | Open | Win rate | P&L | Brier model / market |", "|---|---|---|---|---|---|---|"]
    suggestions = []
    for b in idx["books"]:
        s = json.loads((ROOT / "dashboard" / "data" / b["id"] / "summary.json").read_text(encoding="utf-8"))
        t = s.get("totals", {})
        wr = f"{t['win_rate']:.0%}" if t.get("n") else "-"
        pnl = f"${t['pnl']:+.2f}" if t.get("n") else "-"
        br = f"{t['brier_model']} / {t['brier_market']}" if t.get("n") else "-"
        lines.append(f"| {s['name']} | ${s['bankroll']:.2f} | {t.get('n', 0)} | {s['open_count']} | {wr} | {pnl} | {br} |")
        if s.get("suggestions"):
            suggestions.append(f"- **{s['short']}:** {s['suggestions'][0]['text']}")
        src = ROOT / "reports" / "weekly" / b["id"]
        dest = vault / "Scorecards" / s["short"]
        dest.mkdir(parents=True, exist_ok=True)
        for f in sorted(src.glob("*.md")) if src.exists() else []:
            shutil.copy2(f, dest / f.name)
    lines += ["", "## Top suggestion per book", ""] + (suggestions or ["- None yet"]) + ["", "Weekly scorecards: Scorecards folder.", ""]
    (vault / "Live Status.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Synced {len(idx['books'])} books into {vault}")


if __name__ == "__main__":
    main()
