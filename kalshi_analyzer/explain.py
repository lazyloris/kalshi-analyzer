"""Plain-English reason each settled trade won or lost, plus a short cause tag for stats."""


def explain(t):
    side, bracket = t["side"].upper(), t["bracket"]
    p, price = float(t["model_p"]), float(t["price"])
    won = t["won"] == "1"
    f = float(t["forecast_high"])
    sigma = float(t["sigma"])
    head = f"{'Won' if won else 'Lost'} {side} on {bracket}. Model {p:.0%} vs price {price:.0%}."
    if t.get("actual_high") in (None, ""):
        cause = "unknown_actual"
        return cause, head + " Actual high not reported, so the reason can't be measured."

    a = float(t["actual_high"])
    err = a - f
    z = abs(err) / sigma if sigma else 0
    landed = "landed in" if t["result"] == "yes" else "missed"
    body = f" Forecast {f:g}F, actual {a:g}F ({err:+g}F, {z:.1f} sigma). The high {landed} {bracket}."
    edge_dist = _distance_to_edge(t, a)

    if won:
        if z <= 1:
            cause, why = "forecast_right", " The forecast was close and the market had it priced wrong."
        else:
            cause, why = "lucky", " Won despite a big forecast miss, so count this one as luck, not skill."
    else:
        if z > 1.5:
            cause, why = "forecast_miss", " Unusually large forecast error. If this repeats for a city, add a bias or widen sigma."
        elif edge_dist is not None and edge_dist <= 1:
            cause, why = "close_call", f" Missed by {edge_dist:g}F at the bracket edge: normal noise on a narrow bracket."
        else:
            cause, why = "market_smarter", " The forecast error was ordinary but the market price was closer. The market may use better info (models, live obs)."
    return cause, head + body + why


def _distance_to_edge(t, a):
    st = t["strike_type"]
    lo = float(t["floor"]) if t["floor"] not in (None, "") else None
    hi = float(t["cap"]) if t["cap"] not in (None, "") else None
    if st == "between":
        return min(abs(a - lo), abs(a - hi)) if not (lo <= a <= hi) else min(a - lo, hi - a) + 1
    if st == "greater":
        return abs(a - lo)
    return abs(a - hi)
