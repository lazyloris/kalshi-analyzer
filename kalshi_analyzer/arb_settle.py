"""Did any locked Kalshi/Polymarket pair from the scanner lose on both legs? Read-only."""
import collections
import glob
import json

from . import config as C
from .http import get_json

GAMMA = "https://gamma-api.polymarket.com"


def main():
    real = []
    for f in sorted(glob.glob("data/arb/*.jsonl")):
        for l in open(f):
            r = json.loads(l)
            if r["kind"] == "pair" and r["edge"] > 0 and (r.get("yes_depth") or 0) >= 1 and (r.get("no_depth") or 0) >= 1:
                real.append(r)
    ep = collections.defaultdict(list)
    for r in real:
        ep[(r["yes_venue"], r["yes_id"], r["no_venue"], r["no_id"], r["close"])].append(r)
    kal, pol = {}, {}

    def k_res(t):
        if t not in kal:
            try:
                kal[t] = get_json(f"{C.KALSHI_API}/markets/{t}")["market"].get("result")
            except Exception as e:
                kal[t] = f"err {str(e)[:40]}"
        return kal[t]

    def p_res(slug):
        if slug not in pol:
            try:
                m = get_json(f"{GAMMA}/markets", {"slug": slug})[0]
                px = [float(x) for x in json.loads(m.get("outcomePrices") or "[]")]
                pol[slug] = "yes" if px and px[0] > 0.99 else "no" if px and px[0] < 0.01 else f"open {px}"
            except Exception as e:
                pol[slug] = f"err {str(e)[:40]}"
        return pol[slug]

    out = collections.Counter()
    pnl = 0.0
    bad = []
    for (yv, yid, nv, nid, close), v in ep.items():
        b = max(v, key=lambda r: r["edge"] * min(r["yes_depth"], r["no_depth"]))
        ry = k_res(yid) if yv == "kalshi" else p_res(yid)
        rn = k_res(nid) if nv == "kalshi" else p_res(nid)
        if ry not in ("yes", "no") or rn not in ("yes", "no"):
            out["unknown"] += 1
            continue
        paid = (ry == "yes") + (rn == "no")
        out[f"legs won {paid}"] += 1
        size = min(b["yes_depth"], b["no_depth"])
        cost = b["yes_ask"] + b["no_ask"] + 0.07 * b["yes_ask"] * (1 - b["yes_ask"]) + 0.07 * b["no_ask"] * (1 - b["no_ask"])
        pnl += size * (paid - cost)
        if paid == 0:
            bad.append((close, b["asset"], yv, b["yes_strike"], nv, b["no_strike"], b["room_usd"], round(size * cost, 2)))
    print("sample kalshi:", list(kal.items())[:3]); print("sample poly:", list(pol.items())[:3])
    print(len(ep), "episodes:", dict(out))
    print("P&L if every episode was taken once at its best snapshot and full depth:", round(pnl, 2))
    for x in bad:
        print("BOTH LOST:", x)


if __name__ == "__main__":
    main()
