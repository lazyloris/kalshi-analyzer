import math


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bracket_probability(strike_type, floor, cap, mu, sigma):
    """Weather: chance the whole-degree reading lands in the market's range.

      between floor..cap  -> floor <= t <= cap
      greater floor       -> t > floor   (so >= floor+1)
      greater_or_equal    -> t >= floor
      less cap            -> t < cap     (so <= cap-1)
    A continuous normal is rounded with a 0.5 degree continuity correction.
    """
    z = lambda t: norm_cdf((t - mu) / sigma)
    if strike_type == "between":
        return max(0.0, z(cap + 0.5) - z(floor - 0.5))
    if strike_type == "greater":
        return 1.0 - z(floor + 0.5)
    if strike_type == "greater_or_equal":
        return 1.0 - z(floor - 0.5)
    if strike_type == "less":
        return z(cap - 0.5)
    raise ValueError(f"unknown strike_type {strike_type}")


def lognormal_probability(strike_type, floor, cap, spot, vol_year, hours):
    """Crypto: chance the price at expiry is in range, with no drift and yearly volatility vol_year."""
    s = vol_year * math.sqrt(max(hours, 0.01) / (24 * 365))
    F = lambda k: norm_cdf((math.log(k / spot) + 0.5 * s * s) / s)  # P(price < k)
    if strike_type == "between":
        return max(0.0, F(cap) - F(floor))
    if strike_type in ("greater", "greater_or_equal"):
        return 1.0 - F(floor)
    if strike_type == "less":
        return F(cap)
    raise ValueError(f"unknown strike_type {strike_type}")


def price_sigma(spot, vol_year, hours):
    """One standard deviation of the price move by expiry, in dollars."""
    return spot * vol_year * math.sqrt(max(hours, 0.01) / (24 * 365))


def taker_fee(contracts: int, price: float, rate: float) -> float:
    """Kalshi taker fee in dollars, rounded up to the next cent."""
    raw = rate * contracts * price * (1 - price)
    return math.ceil(raw * 100 - 1e-9) / 100


def bracket_label(strike_type, floor, cap, unit="F"):
    f = (lambda v: f"${v:,.0f}") if unit == "$" else (lambda v: f"{v:g}F")
    if strike_type == "between":
        return f"{f(floor)}-{f(cap)}" if unit == "$" else f"{floor:g}-{cap:g}F"
    if strike_type == "greater":
        return f">{f(floor)}"
    if strike_type == "greater_or_equal":
        return f">={f(floor)}"
    return f"<{f(cap)}"


def bracket_center(strike_type, floor, cap):
    if strike_type == "between":
        return (floor + cap) / 2
    if strike_type in ("greater", "greater_or_equal"):
        return floor
    return cap


def distance_to_edge(strike_type, floor, cap, actual):
    """How far the actual value landed from the nearest edge of the bracket."""
    if strike_type == "between":
        return min(abs(actual - floor), abs(actual - cap))
    if strike_type in ("greater", "greater_or_equal"):
        return abs(actual - floor)
    return abs(actual - cap)


def calibrate_errors(errors, default_sigma, prior_n=10, floor=1.0):
    """Bias and sigma from past misses (actual - forecast), shrunk toward (0, default) when data is thin.
    With n misses, the data gets weight n / (n + prior_n). Used live and by the backtester."""
    n = len(errors)
    if not n:
        return 0.0, default_sigma, 0
    mean = sum(errors) / n
    bias = mean * n / (n + prior_n)
    var = sum((x - bias) ** 2 for x in errors) / n
    sigma = math.sqrt((n * var + prior_n * default_sigma ** 2) / (n + prior_n))
    return bias, max(sigma, floor), n
