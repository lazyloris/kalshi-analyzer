"""Plain-English reason each settled trade won or lost, plus a short cause tag for stats."""
from .model import distance_to_edge


def _fmt(v, unit):
    return f"${v:,.2f}" if unit == "$" else f"{v:g}{unit}"


def explain(t):
    side, bracket, unit = t["side"].upper(), t["bracket"], t.get("unit", "F")
    p, price = float(t["model_p"]), float(t["price"])
    won = t["won"] == "1"
    head = f"{'Won' if won else 'Lost'} {side} on {bracket}. Model {p:.0%} vs price {price:.0%}."
    if str(t.get("strategy_version", "")).startswith("btc-fav"):
        cause = "favorite_held" if won else "favorite_lost"
        return cause, head + (" The favorite held, as the rule expects." if won
                              else " The favorite lost. One loss here costs several wins.")
    if t.get("book") == "trending" or t.get("forecast") in (None, ""):
        cause = "longshot_held" if won else "longshot_hit"
        return cause, head + (" The long shot missed, as the rule expects." if won
                              else " The long shot came in. One of these wipes out several small wins.")
    if t.get("actual") in (None, ""):
        return "unknown_actual", head + " Final value not reported, so the reason can't be measured."

    f, a, sigma = float(t["forecast"]), float(t["actual"]), float(t["sigma"])
    err = a - f
    z = abs(err) / sigma if sigma else 0
    landed = "landed in" if t["result"] == "yes" else "missed"
    word = "Forecast" if unit == "F" else "Price at entry"
    sign = "+" if err >= 0 else "-"
    body = f" {word} {_fmt(f, unit)}, actual {_fmt(a, unit)} ({sign}{_fmt(abs(err), unit)}, {z:.1f} sigma). It {landed} {bracket}."
    edge = distance_to_edge(t["strike_type"], _n(t["floor"]), _n(t["cap"]), a)
    close = edge is not None and sigma and edge / sigma <= 0.4

    if won:
        if z <= 1:
            cause, why = "forecast_right", " The model was close and the market had it priced wrong."
        else:
            cause, why = "lucky", " Won despite a big miss, so count this as luck, not skill."
    else:
        if z > 1.5:
            cause, why = "forecast_miss", " Unusually large move or forecast error. If it repeats, widen sigma or add a bias."
        elif close:
            cause, why = "close_call", f" Missed by {_fmt(edge, unit)} at the bracket edge: normal noise."
        else:
            cause, why = "market_smarter", " The miss was ordinary but the market price was closer. The market may know more."
    return cause, head + body + why


def _n(v):
    return None if v in (None, "") else float(v)
