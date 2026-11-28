"""Heartbeat: GitHub's cron fires hours late on this repo, so this job stays awake and starts the
time-sensitive workflows itself (workflow_dispatch). Each run lasts ~5h45m and starts the next one."""
import datetime as dt
import json
import os
import subprocess
import time
from zoneinfo import ZoneInfo

NY = ZoneInfo("America/New_York")
REPO = os.environ["GITHUB_REPOSITORY"]
# workflow file -> (hour, minute) in New York time to start it. Each workflow waits for its own exact moment.
TARGETS = {"favorites.yml": (12, 15), "cpi_book.yml": (5, 0)}
RUN_MINUTES = 345


def gh(*args):
    return subprocess.run(["gh", "api", *args], capture_output=True, text=True)


def started_today(wf, since_utc):
    r = gh(f"repos/{REPO}/actions/workflows/{wf}/runs?per_page=20&created=>={since_utc:%Y-%m-%dT%H:%M:%SZ}")
    try:
        return any(x["event"] == "workflow_dispatch" for x in json.loads(r.stdout).get("workflow_runs", []))
    except (ValueError, KeyError):
        return False


def dispatch(wf):
    r = gh("-X", "POST", f"repos/{REPO}/actions/workflows/{wf}/dispatches", "-f", "ref=main")
    print(f"{dt.datetime.now(NY):%Y-%m-%d %H:%M} ET dispatched {wf}: {'ok' if r.returncode == 0 else r.stderr.strip()}", flush=True)


def main():
    stop = time.time() + RUN_MINUTES * 60
    while time.time() < stop:
        now = dt.datetime.now(NY)
        for wf, (h, m) in TARGETS.items():
            t = now.replace(hour=h, minute=m, second=0, microsecond=0)
            if t <= now <= t + dt.timedelta(minutes=40) and not started_today(wf, t.astimezone(dt.timezone.utc) - dt.timedelta(minutes=5)):
                dispatch(wf)
        time.sleep(60)
    dispatch("clock.yml")


if __name__ == "__main__":
    main()
