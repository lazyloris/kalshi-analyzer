import sys, json, glob
for f in glob.glob("data/arb/*.jsonl"):
    for l in open(f):
        r = json.loads(l)
        if r["kind"] == "loop":
            print("LOOP", r["t"][11:], r["kalshi_event"], r["poly_slug"], r["n_kalshi"], r["n_poly"], r["best_edge"], r.get("spot_coinbase"), r.get("spot_binance"))
        elif r["kind"] == "pair" and r["edge"] > 0:
            print(" ", r["t"][11:], r["yes_venue"], r["yes_strike"], r["yes_ask"], r["no_venue"], r["no_strike"], r["no_ask"], r["edge"], "top", r.get("yes_top_size"), r.get("no_top_size"), "depth", r.get("yes_depth"), r.get("no_depth"))
        elif r["kind"] == "error":
            print("ERR", r)
