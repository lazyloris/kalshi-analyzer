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
show("settled markets", get(f"{K}/markets",{"series_ticker":"KXHIGHNY","status":"settled","limit":3}))
r=get(f"{K}/markets",{"series_ticker":"KXHIGHNY","status":"settled","limit":1000})
if isinstance(r[1],dict):
    ms=r[1]["markets"]; print("n settled page1",len(ms),"cursor",bool(r[1].get("cursor")), "oldest", min(m["close_time"] for m in ms) if ms else None)
show("historical cutoff", get(f"{K}/historical/cutoff"))
show("historical markets", get(f"{K}/historical/markets",{"series_ticker":"KXHIGHNY","limit":3}))
now=int(time.time())
tk="KXHIGHNY-26NOV07-B61.5"
show("candles", get(f"{K}/series/KXHIGHNY/markets/{tk}/candlesticks",{"start_ts":now-4*86400,"end_ts":now,"period_interval":60}),2500)
show("hist candles", get(f"{K}/historical/markets/KXHIGHNY-25JUN07-B85.5/candlesticks",{"start_ts":now-200*86400,"end_ts":now,"period_interval":60}),800)
show("trades", get(f"{K}/markets/trades",{"ticker":tk,"limit":3}))
show("series weather", get(f"{K}/series/KXHIGHNY"))
O="https://previous-runs-api.open-meteo.com/v1/forecast"
show("openmeteo prev", get(O,{"latitude":40.78,"longitude":-73.97,"daily":"temperature_2m_max,temperature_2m_min","hourly":"temperature_2m_previous_day1","start_date":"2026-10-01","end_date":"2026-10-03","temperature_unit":"fahrenheit","timezone":"America/New_York"}),1200)
show("openmeteo hist forecast nbm", get("https://historical-forecast-api.open-meteo.com/v1/forecast",{"latitude":40.78,"longitude":-73.97,"daily":"temperature_2m_max,temperature_2m_min","start_date":"2025-06-01","end_date":"2025-06-03","temperature_unit":"fahrenheit","timezone":"America/New_York","models":"ncep_nbm_conus"}),800)
show("iem nbm", get("https://mesonet.agron.iastate.edu/api/1/nws/afos/list.json",{"pil":"CLINYC","date":"2026-11-07"}),600)
show("coinbase hourly", get("https://api.exchange.coinbase.com/products/BTC-USD/candles",{"granularity":3600,"start":"2026-06-01T00:00:00Z","end":"2026-06-02T00:00:00Z"}),300)
show("btc settled", get(f"{K}/markets",{"series_ticker":"KXBTCD","status":"settled","limit":2}),1500)
