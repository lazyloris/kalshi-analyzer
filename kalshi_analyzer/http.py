import json
import time
import urllib.error
import urllib.parse
import urllib.request

from .config import USER_AGENT


def get_json(url, params=None, retries=3, timeout=20):
    if params:
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            last = e
            if isinstance(e, urllib.error.HTTPError) and e.code == 404:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError(f"GET {url} failed: {last}")
