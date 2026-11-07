import json, urllib.request, urllib.parse
B="https://api.elections.kalshi.com/trade-api/v2"
def g(path, **p):
    u=B+path+("?"+urllib.parse.urlencode(p) if p else "")
    return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"kalshi-analyzer"}),timeout=30))
for st in ["KXGOLD","GOLD","KXSILVER","KXSILVERD","KXGOLDD"]:
    try:
        ms=g("/markets", series_ticker=st, status="open", limit=200).get("markets",[])
        print("SERIES",st,len(ms), sorted({m["event_ticker"] for m in ms})[:6])
        for m in ms[:3]:
            print("   ",json.dumps({k:m.get(k) for k in ["ticker","title","strike_type","floor_strike","cap_strike","close_time","yes_ask_dollars","yes_bid_dollars","volume_fp","rules_primary"]})[:700])
    except Exception as e: print("ERR",st,e)
for cat in ["Entertainment","Mentions","Social","Culture","Tech & Science","Companies"]:
    try:
        s=g("/series", category=cat).get("series",[])
        print("CAT",cat,len(s))
        for x in s:
            if (x.get("frequency") in ("daily","weekly")): print("  ",x["ticker"],"|",x.get("title"),"|",x.get("frequency"))
    except Exception as e: print("ERR",cat,e)
for s in ["PAXG-USD","XAU-USD"]:
    try: print(s, json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.exchange.coinbase.com/products/{s}/ticker",headers={"User-Agent":"kalshi-analyzer"}),timeout=20))["price"])
    except Exception as e: print("ERR coinbase",s,e)
