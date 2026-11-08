import json, time, urllib.request, urllib.parse
UA={"User-Agent":"kalshi-analyzer-paper (research)"}
def get(u,p=None):
    if p: u+="?"+urllib.parse.urlencode(p)
    try:
        with urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30) as r: return r.status, json.loads(r.read())
    except Exception as e:
        body=getattr(e,"read",lambda:b"")()[:300]; return str(e), body.decode("utf8","replace")
K="https://api.elections.kalshi.com/trade-api/v2"
def show(name,res,n=1500):
    print("=====",name,res[0]); print(json.dumps(res[1])[:n] if not isinstance(res[1],str) else res[1]); print()
r=get(f"{K}/historical/markets",{"series_ticker":"KXHIGHNY","limit":1000}); ms=r[1]["markets"]
print("hist n",len(ms),"cursor",bool(r[1].get("cursor")),"oldest",min(m["close_time"] for m in ms))
old=ms[-1]["ticker"]; ct=ms[-1]["close_time"]; print(old,ct)
import datetime as dt
e=int(dt.datetime.fromisoformat(ct.replace("Z","+00:00")).timestamp())
show("hist candles", get(f"{K}/historical/markets/{old}/candlesticks",{"start_ts":e-3*86400,"end_ts":e,"period_interval":60}),600)
show("hist candles v2", get(f"{K}/series/KXHIGHNY/markets/{old}/candlesticks",{"start_ts":e-3*86400,"end_ts":e,"period_interval":60}),600)
now=int(time.time())
show("batch candles", get(f"{K}/markets/candlesticks",{"market_tickers":"KXHIGHNY-26NOV07-B61.5,KXHIGHNY-26NOV07-B63.5","start_ts":now-3*86400,"end_ts":now,"period_interval":60}),800)
O="https://previous-runs-api.open-meteo.com/v1/forecast"
for model in ["ncep_nbm_conus","best_match","gfs_seamless"]:
    res=get(O,{"latitude":40.78,"longitude":-73.97,"hourly":"temperature_2m,temperature_2m_previous_day1,temperature_2m_previous_day2","start_date":"2026-09-10","end_date":"2026-09-10","temperature_unit":"fahrenheit","timezone":"America/New_York","models":model})
    if isinstance(res[1],dict) and "hourly" in res[1]:
        h=res[1]["hourly"]; print(model, {k:(max(x for x in v if x is not None) if any(x is not None for x in v) else None) for k,v in h.items() if k!="time"})
    else: show("prev "+model,res,400)
res=get("https://historical-forecast-api.open-meteo.com/v1/forecast",{"latitude":40.78,"longitude":-73.97,"daily":"temperature_2m_max","start_date":"2026-09-10","end_date":"2026-09-10","temperature_unit":"fahrenheit","timezone":"America/New_York","models":"ncep_nbm_conus"}); print("hist nbm",res[1].get("daily") if isinstance(res[1],dict) else res)
for m in ms[:12]:
    if m["event_ticker"]==ms[0]["event_ticker"]: print(m["ticker"], m["expiration_value"], m["result"])
