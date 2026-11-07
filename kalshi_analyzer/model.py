import math


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bracket_probability(strike_type, floor, cap, mu, sigma):
    """Chance the whole-degree high lands in the market's range.

    Kalshi temperature markets use whole degrees:
      between floor..cap  -> floor <= high <= cap
      greater floor       -> high > floor   (so >= floor+1)
      less cap            -> high < cap     (so <= cap-1)
    A continuous normal is rounded with a 0.5 degree continuity correction.
    """
    z = lambda t: norm_cdf((t - mu) / sigma)
    if strike_type == "between":
        return max(0.0, z(cap + 0.5) - z(floor - 0.5))
    if strike_type == "greater":
        return 1.0 - z(floor + 0.5)
    if strike_type == "less":
        return z(cap - 0.5)
    raise ValueError(f"unknown strike_type {strike_type}")


def taker_fee(contracts: int, price: float, rate: float) -> float:
    """Kalshi taker fee in dollars, rounded up to the next cent."""
    raw = rate * contracts * price * (1 - price)
    return math.ceil(raw * 100 - 1e-9) / 100


def bracket_label(strike_type, floor, cap):
    if strike_type == "between":
        return f"{floor:g}-{cap:g}F"
    if strike_type == "greater":
        return f">{floor:g}F"
    return f"<{cap:g}F"


def bracket_center(strike_type, floor, cap):
    if strike_type == "between":
        return (floor + cap) / 2
    if strike_type == "greater":
        return floor + 1
    return cap - 1


def outcome_in_bracket(strike_type, floor, cap, actual):
    if strike_type == "between":
        return floor <= actual <= cap
    if strike_type == "greater":
        return actual > floor
    return actual < cap
