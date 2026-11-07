"""Weekly scorecard as Markdown (Obsidian-friendly)."""
import datetime as dt

from . import analysis


def _table(groups, title):
    if not groups:
        return ""
    lines = [f"### By {title}", "", "| Group | Trades | Win rate | P&L | ROI | Brier model / market |", "|---|---|---|---|---|---|"]
    for k, v in groups.items():
        lines.append(f"| {k} | {v['n']} | {v['win_rate']:.0%} | ${v['pnl']:+.2f} | {v['roi']:.0%} | {v['brier_model']} / {v['brier_market']} |")
    return "\n".join(lines) + "\n"


def scorecard(book_id, trades, forecasts, actuals, now, week_start: dt.date, week_end: dt.date):
    in_week = [t for t in trades if t["status"] == "settled"
               and week_start.isoformat() <= t["target_date"] <= week_end.isoformat()]
    s = analysis.build(book_id, in_week, forecasts, actuals, now)
    all_s = analysis.build(book_id, trades, forecasts, actuals, now)
    tot = s["totals"]
    out = [
        "---", "project: Kalshi Trader", "tags: [scorecard, trading]", f"book: {s['name']}",
        f"week: {week_start} to {week_end}", f"strategy: {s['strategy_version']}", "---", "",
        f"# {s['name']}: scorecard {week_start} to {week_end}", "",
        "Paper trading with real Kalshi prices and fake money. Not financial advice.", "",
        "## This week",
    ]
    if not tot["n"]:
        out += ["No trades settled this week.", ""]
    else:
        out += [
            f"- Trades settled: **{tot['n']}**, wins {tot['wins']} (**{tot['win_rate']:.0%}**)",
            f"- Profit after fees: **${tot['pnl']:+.2f}** (ROI {tot['roi']:.0%}, fees ${tot['fees']:.2f})",
            f"- Brier score, lower is better: model **{tot['brier_model']}** vs market prices {tot['brier_market']}",
            f"- Average edge at entry: {tot['avg_edge']*100:.1f}c", "",
        ]
    at = all_s["totals"]
    out += ["## All time", f"- Paper bankroll: **${all_s['bankroll']:.2f}** (started ${s['starting_bankroll']:.0f})",
            f"- Settled trades: {at.get('n', 0)}, open: {all_s['open_count']}", ""]
    if at.get("n"):
        out.append(f"- Win rate {at['win_rate']:.0%}, P&L ${at['pnl']:+.2f}, Brier model {at['brier_model']} vs market {at['brier_market']}\n")

    out += ["## Why trades won or lost", ""]
    for name, title in (("cause", "cause"), ("city", "city"), ("edge", "edge at entry"),
                        ("price", "entry price"), ("bracket_distance", "bracket distance from forecast (in sigmas)"),
                        ("days_ahead", "days ahead"), ("side", "side")):
        t = _table(all_s["breakdowns"].get(name, {}), title)
        if t:
            out += [t]

    if all_s["calibration"]:
        out += ["### Calibration (all time)", "", "| Model said | Trades | Predicted | Actually won |", "|---|---|---|---|"]
        out += [f"| {c['bucket']} | {c['n']} | {c['predicted']:.0%} | {c['actual']:.0%} |" for c in all_s["calibration"]]
        out.append("")

    if all_s["forecast_accuracy"]:
        out += ["## NWS forecast accuracy", "", "| City | Days ahead | Days | Bias (actual - forecast) | Avg miss | Spread | Sigma used |", "|---|---|---|---|---|---|---|"]
        out += [f"| {a['city']} | {a['days_ahead']} | {a['n']} | {a['bias']:+.1f}F | {a['mae']:.1f}F | {a['stdev'] if a['stdev'] is not None else '-'} | {a['sigma_used']} |"
                for a in all_s["forecast_accuracy"]]
        out.append("")

    out += ["## Trades this week", ""]
    for t in sorted(in_week, key=lambda t: t["target_date"]):
        out.append(f"- {t['target_date']} {t['city']}: {t['why']} P&L ${float(t['pnl']):+.2f}")
    if not in_week:
        out.append("- None")
    out += ["", "## Suggested next change (pick one, at most)", ""]
    out += [f"{i}. {x['text']}" for i, x in enumerate(all_s["suggestions"][:5], 1)] or ["- No suggestions yet."]
    out.append("")
    return "\n".join(out)
