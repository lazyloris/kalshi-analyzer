import json, time, urllib.request, urllib.parse
UA={"User-Agent":"kalshi-analyzer-paper (research)"}
def get(u,p=None):
    if p: u+="?"+urllib.parse.urlencode(p)
    t=time.time()
    try:
        with urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60) as r: b=r.read(); return r.status, json.loads(b), len(b), round(time.time()-t,2)
    except Exception as e:
        return str(e), getattr(e,"read",lambda:b"")()[:300].decode("utf8","replace"),0,0
K="https://api.elections.kalshi.com/trade-api/v2"
s,d,n,t=get(f"{K}/series",{"limit":1000}); print("series",s,n,t, list(d.keys()) if isinstance(d,dict) else d)
if isinstance(d,dict):
    ss=d.get("series") or []; print("count",len(ss),"cursor",bool(d.get("cursor"))); print(json.dumps(ss[0])[:800])
    import collections; print(collections.Counter(x.get("category") for x in ss).most_common(30))
s,d,n,t=get(f"{K}/series",{"include_volume":"true","limit":5}); print("series vol",s,json.dumps(d)[:600])
now=int(time.time())
s,d,n,t=get(f"{K}/events",{"status":"settled","limit":200,"min_close_ts":now-86400}); print("events",s,n,t)
if isinstance(d,dict): ev=d.get("events") or []; print(len(ev), bool(d.get("cursor"))); print(json.dumps(ev[0])[:700] if ev else "")
s,d,n,t=get(f"{K}/markets",{"status":"settled","limit":1000,"min_close_ts":now-86400}); print("markets 1d",s,n,t)
if isinstance(d,dict):
    ms=d["markets"]; print(len(ms), bool(d.get("cursor")))
    import collections; print(collections.Counter(m["event_ticker"].split("-")[0] for m in ms).most_common(15))
pages=0; cur=None; cnt=0; t0=time.time()
while pages<15:
    p={"status":"settled","limit":1000,"min_close_ts":now-86400}
    if cur: p["cursor"]=cur
    s,d,n,t=get(f"{K}/markets",p); 
    if not isinstance(d,dict): break
    cnt+=len(d["markets"]); pages+=1; cur=d.get("cursor")
    if not cur: break
print("1-day settled markets >=",cnt,"pages",pages,"more",bool(cur),"secs",round(time.time()-t0))
