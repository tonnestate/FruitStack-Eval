#!/usr/bin/env python3
"""QA-1 progress line: rows done / 792, rows per hour, ETA, infrastructure-failure count. Counts only; NO outcome data (no correctness, no letters). usage: qa1_progress.py RESULTS.jsonl STARTED_ISO [TOTAL]"""
import json
import sys
from datetime import datetime, timezone


def progress(path: str, started: str, total: int = 792, now: datetime | None = None) -> str:
    rows = [json.loads(l) for l in open(path) if l.strip()] if path else []
    now = now or datetime.now(timezone.utc)
    hours = max((now - datetime.fromisoformat(started.replace("Z", "+00:00"))).total_seconds() / 3600, 1e-9)
    done = len(rows)
    rate = done / hours
    eta = f"{(total - done) / rate:.1f} h" if rate > 0 and done < total else ("done" if done >= total else "n/a")
    infra = sum(1 for r in rows if r.get("status") != "OK")
    per_arm = {a: sum(1 for r in rows if r["arm"] == a) for a in "TESL"}
    return f"QA-1 progress {now.strftime('%Y-%m-%dT%H:%MZ')}: rows {done}/{total} ({per_arm}), {rate:.1f} rows/h, ETA {eta}, infra failures {infra} (rows with status != OK after the rerun)"


if __name__ == "__main__":
    print(progress(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 792))
