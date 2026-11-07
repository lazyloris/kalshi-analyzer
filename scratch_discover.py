import json, urllib.request, urllib.parse
B="https://api.elections.kalshi.com/trade-api/v2"
def g(path, **p):
    u=B+path+("?"+urllib.parse.urlencode(p) if p else "")
    return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"kalshi-analyzer"}),timeout=30))
ser=[]; cur=None
for cat in ["Climate and Weather","Crypto","Financials","Economics"]:
    try:
        d=g("/series", category=cat)
        s=d.get("series",[])
        print("CAT",cat,len(s))
        for x in s:
            t=x["ticker"]; ti=x.get("title","")
            if any(k in (t+ti).upper() for k in ["LOW","BTC","ETH","BITCOIN","ETHEREUM","INX","NASDAQ","S&P","HIGH","RAIN","SNOW","GAS","WTI","GOLD","EUR","USDJPY"]):
                print("  ",t,"|",ti,"|",x.get("frequency"))
    except Exception as e: print("ERR",cat,e)
for st in ["KXLOWTNYC","KXLOWNY","KXBTCD","KXBTC","KXETHD","KXETH","KXINXU","KXINX"]:
    try:
        d=g("/markets", series_ticker=st, status="open", limit=3)
        ms=d.get("markets",[])
        print("SERIES",st,len(ms))
        for m in ms[:2]:
            print("   ",json.dumps({k:m.get(k) for k in ["ticker","event_ticker","title","strike_type","floor_strike","cap_strike","close_time","yes_ask_dollars","yes_bid_dollars","volume","volume_fp","expiration_value"]}))
    except Exception as e: print("ERR",st,e)
for s in ["BTC-USD","ETH-USD"]:
    try: print(s, json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.exchange.coinbase.com/products/{s}/ticker",headers={"User-Agent":"kalshi-analyzer"}),timeout=20))["price"])
    except Exception as e: print("ERR coinbase",e)
