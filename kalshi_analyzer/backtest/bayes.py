"""Bayesian strategies, walk-forward (each decision only uses markets that had settled before it).

1. bucket_posterior: for every price level (e.g. "YES at 85-90c"), keep a Beta posterior of how often
   that bet actually won. The prior is centred on the price itself (the market is right until shown
   otherwise). Trade only when the posterior is >= `conf` sure the true win rate beats price + fee.
2. market_prior: start from the market's price, then move toward the model only as much as the model
   has earned. The weight w (0 = trust market, 1 = trust model) is picked from past settled markets by
   log loss, combined in log-odds space.
"""
import datetime as dt
import heapq
import math

from .. import config as C
from ..model import taker_fee
from . import engine as E

DAY = 86400


def _settle_ts(e):
    """Conservative: assume we only learn the outcome 2 days after the event date."""
    d = dt.date.fromisoformat(e["date"]) + dt.timedelta(days=2)
    return int(dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc).timestamp())


def _betacf(a, b, x, itmax=200, eps=3e-12):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > 1e-300 else 1e-300)
    h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1 + aa / c if abs(1 + aa / c) > 1e-300 else 1e-300
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        d = 1 / (d if abs(d) > 1e-300 else 1e-300)
        c = 1 + aa / c if abs(1 + aa / c) > 1e-300 else 1e-300
        de = d * c
        h *= de
        if abs(de - 1) < eps:
            break
    return h


def beta_cdf(x, a, b):
    """Regularized incomplete beta I_x(a, b) (standard library only)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbt = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x)
    if x < (a + 1) / (a + b + 2):
        return math.exp(lbt) * _betacf(a, b, x) / a
    return 1 - math.exp(lbt) * _betacf(b, a, 1 - x) / b


class _Pending:
    """Outcomes we may only use once they've settled (by time)."""
    def __init__(self):
        self.q, self.n = [], 0

    def add(self, ts, item):
        self.n += 1
        heapq.heappush(self.q, (ts, self.n, item))

    def pop_ready(self, now):
        while self.q and self.q[0][0] <= now:
            yield heapq.heappop(self.q)[2]


def bucket_posterior(conf=0.95, k=20, width=0.05, lo=0.03, hi=0.97, max_spread=0.10, max_per_event=2):
    stats = {}  # (side, bucket) -> [wins, n, sum_price]
    pending = _Pending()

    def pick(e):
        for key, won, price in pending.pop_ready(e["ts"]):
            s = stats.setdefault(key, [0, 0, 0.0])
            s[0] += won
            s[1] += 1
            s[2] += price
        cands, seen = [], []
        for m in e["markets"]:
            if m["ask"] - m["bid"] > max_spread:
                continue
            for side in ("yes", "no"):
                ask = m["ask"] if side == "yes" else 1 - m["bid"]
                if not (lo <= ask <= hi):
                    continue
                key = (side, int(ask / width))
                won = m["won_yes"] if side == "yes" else not m["won_yes"]
                seen.append((key, int(won), ask))
                w, n, sp = stats.get(key, (0, 0, 0.0))
                if n < 30:
                    continue
                p0 = sp / n  # prior centre = average price paid in this bucket
                a, b = p0 * k + w, (1 - p0) * k + (n - w)
                c = max(1, math.floor(E.STAKE / ask))
                be = ask + taker_fee(c, ask, C.FEE_RATE) / c
                p_beat = 1 - beta_cdf(be, a, b)
                if p_beat >= conf:
                    cands.append((p_beat, m, side, a / (a + b)))
        for key, won, ask in seen:
            pending.add(_settle_ts(e), (key, won, ask))
        cands.sort(key=lambda x: -x[0])
        out, used = [], set()
        for _, m, side, p in cands:
            if m["ticker"] in used:
                continue
            used.add(m["ticker"])
            out.append(E._trade(e, m, side, p))
            if len(out) >= max_per_event:
                break
        return out
    return pick


def _logit(p):
    p = min(max(p, 1e-4), 1 - 1e-4)
    return math.log(p / (1 - p))


def _sig(x):
    return 1 / (1 + math.exp(-x))


def market_prior(prob, grid=tuple(i / 10 for i in range(11)), min_obs=200, min_edge=0.05):
    """Combine market and model in log-odds: logit(p) = logit(mkt) + w * (logit(model) - logit(mkt)).
    w is the grid value with the lowest log loss on markets that had already settled."""
    loss = [0.0] * len(grid)
    nobs = [0]
    pending = _Pending()
    state = {"w": 0.0}

    def p_post(e, m):
        pm = prob(e, m)
        if pm is None:
            return None
        lm = _logit(E.mid(m))
        return _sig(lm + state["w"] * (_logit(pm) - lm))

    inner = E.edge_picker(p_post, min_edge=min_edge)

    def pick(e):
        for lm, d, y in pending.pop_ready(e["ts"]):
            nobs[0] += 1
            for i, w in enumerate(grid):
                p = min(max(_sig(lm + w * d), 1e-6), 1 - 1e-6)
                loss[i] -= math.log(p if y else 1 - p)
        state["w"] = grid[min(range(len(grid)), key=lambda i: loss[i])] if nobs[0] >= min_obs else 0.0
        st = _settle_ts(e)
        for m in e["markets"]:
            pm = prob(e, m)
            if pm is None or m["ask"] - m["bid"] > 0.10:
                continue
            lm = _logit(E.mid(m))
            pending.add(st, (lm, _logit(pm) - lm, bool(m["won_yes"])))
        return inner(e) if state["w"] > 0 else []
    pick.state = state
    return pick


def strategies(prob=None, prob_name="model"):
    out = [
        ("b_bucket95", "Bayes price-level, 95% sure", "Trade a price level only when 95% sure it wins more than its price + fee",
         bucket_posterior(0.95)),
        ("b_bucket99", "Bayes price-level, 99% sure", "Same, 99% sure", bucket_posterior(0.99)),
    ]
    if prob is not None:
        out.append(("b_mkt_prior", f"Bayes: market prior + {prob_name}",
                    "Start from the market price, lean toward the model only as much as it has earned", market_prior(prob)))
    return out
