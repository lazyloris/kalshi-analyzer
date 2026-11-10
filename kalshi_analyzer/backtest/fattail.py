"""Fat-tail model: instead of a bell curve (lognormal), use the actual h-hour moves of the last
90 days. P(price at close in bracket) = share of past h-hour moves that would land there.
Only moves that ended at or before the entry time are used."""
import bisect
import math

from . import engine as E
from . import bayes as B

HOUR = 3600


def attach(events, prices, days=90, min_samples=500):
    hours = sorted(prices)
    for e in events:
        h = max(1, round((e.get("close") or (e["ts"] + e["hours"] * HOUR)) - e["ts"]) // HOUR)
        a = bisect.bisect_left(hours, e["ts"] - days * 86400)
        b = bisect.bisect_right(hours, e["ts"])
        rs = []
        for t in hours[a:b]:
            p0 = prices.get(t - h * HOUR)
            if p0:
                rs.append(math.log(prices[t] / p0))
        e["emp"] = sorted(rs) if len(rs) >= min_samples else None
    return sum(1 for e in events if e.get("emp"))


def p_emp(e, m, mult=1.0):
    rs = e.get("emp")
    if not rs:
        return None
    n = len(rs)
    below = lambda k: bisect.bisect_left(rs, math.log(k / e["spot"]) / mult) / n  # P(price < k)
    st, lo, hi = m["strike_type"], E._f(m["floor"]), E._f(m["cap"])
    if st == "between":
        return max(0.0, below(hi) - below(lo))
    if st in ("greater", "greater_or_equal"):
        return 1 - below(lo)
    if st == "less":
        return below(hi)
    return None


def strategies():
    return [
        ("f_emp", "Fat-tail (actual past moves)", "Odds from the last 90 days of real h-hour moves, 8c edge",
         E.edge_picker(lambda e, m: p_emp(e, m))),
        ("f_emp75", "Fat-tail, moves x0.75", "Same, moves shrunk to 75%", E.edge_picker(lambda e, m: p_emp(e, m, 0.75))),
        ("f_emp50", "Fat-tail, moves x0.5", "Same, moves shrunk to 50%", E.edge_picker(lambda e, m: p_emp(e, m, 0.5))),
        ("f_emp_bayes", "Bayes: market prior + fat-tail", "Start from the market, lean toward the fat-tail odds as earned",
         B.market_prior(lambda e, m: p_emp(e, m))),
    ]


def sweep():
    return [(k, E.edge_picker(lambda e, m, k=k: p_emp(e, m, k))) for k in (0.4, 0.5, 0.6, 0.75, 0.9, 1.0)]
