#!/usr/bin/env python3
"""Read-only status of the running COLLAB-1 campaign (and any other OGI queue process): process, current task/condition, progress, heartbeat, waiting reason, provider errors, requests/tokens, state.
Writes nothing, touches nothing, calls no provider. usage: status.py [--base DIR] [--campaign NAME] [--json]      continuous view: watch -n 30 'python3 <repo>/evidence/ogi013-collab1/status.py'"""
import argparse
import importlib.util
import json
import os
import subprocess
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013-collab1"
DONE = {"DONE", "BUDGET_STOP", "TIMEOUT"}
FRESH_S, STALE_S = 300, 900


def ps(pattern: str, must: str = "") -> list[dict]:
    out = subprocess.run(["ps", "-eo", "pid,etimes,args"], capture_output=True, text=True).stdout.splitlines()[1:]
    me = os.getpid()
    rows = []
    for line in out:
        pid, et, args = line.strip().split(None, 2)
        if pattern in args and must in args and int(pid) != me and "status.py" not in args and "pgrep" not in args:
            rows.append({"pid": int(pid), "elapsed_s": int(et), "cmd": args[:160], "args": args})
    return rows


def jsonl(p: Path) -> list[dict]:
    try:
        return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
    except (OSError, ValueError):
        return []


def age(ts) -> int | None:
    return None if ts is None else max(0, int(time.time() - ts))


def newest(paths) -> float | None:
    m = [p.stat().st_mtime for p in paths if p.exists()]
    return max(m) if m else None


def main() -> int:
    a = argparse.ArgumentParser()
    a.add_argument("--base", default=BASE)
    a.add_argument("--campaign", default="collab1")
    a.add_argument("--json", action="store_true")
    o = a.parse_args()
    base = Path(o.base)
    R, C = base / "runs", base / "runs" / o.campaign
    manifest = json.loads((HERE / "study_manifest_v2.json").read_text())
    budget = json.loads((HERE / "collab1_budget.json").read_text())
    spec = importlib.util.spec_from_file_location("pilot_guard", HERE.parent / "ogi013-pilot/pilot_guard.py")
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)
    camp = json.loads((C / "campaign.json").read_text()) if (C / "campaign.json").is_file() else {}
    recs = {}
    for f in sorted(C.glob("*/*.episode.json")):
        recs[f.relative_to(C).as_posix()[: -len(".episode.json")]] = json.loads(f.read_text())
    statuses = Counter(r["status"] for r in recs.values())
    total = len(manifest["tasks"]) * len(manifest["conditions"])
    blocks_done = sum(1 for p in C.glob("*/BLOCK_DONE")) + len(list((C / "discarded").glob("*-INFRA_INCOMPLETE.txt")))
    progress = [x for x in (C / "progress.txt").read_text().splitlines()] if (C / "progress.txt").is_file() else []
    last_done = next((x for x in reversed(progress) if " DONE " in x or "BUDGET_STOP" in x or "TIMEOUT" in x), None)
    launchers = [x for x in ps("run_collab1.py", f"--base {base}") if x["args"].startswith(("python", "/usr"))]       # the production launcher of THIS base (not a test copy)
    episodes = [e for e in ps("ogi013_tau2_run.py", str(C))]
    cur = next((k for k, r in recs.items() if r["status"] == "RUNNING"), None)
    cur_info, waiting, errors, heartbeat = {}, [], {}, None
    if cur:
        r = recs[cur]
        d = C / cur
        files = [d / "fruitstack/plumme-state/receipts.jsonl", d / "sim-usage.jsonl", C / f"{cur}.log", *d.glob("tasks/*/fruitstack-events.jsonl")]
        heartbeat = newest(files)
        rc = jsonl(d / "fruitstack/plumme-state/receipts.jsonl")
        errors = dict(Counter(x["failure_class"] for x in rc[-60:] if not x["success"]))
        sim = jsonl(d / "sim-usage.jsonl")
        if sim and sim[-1].get("exception"):
            waiting.append(f"simulator route: {sim[-1]['exception']} {str(sim[-1].get('detail'))[:80]}")
        left = [x["ts"] + x["earliest_retry_s"] - time.time() for x in sim[-3:] if x.get("earliest_retry_s") and x.get("ts")]
        if left and max(left) > 0:
            waiting.append(f"simulator provider cooldown, {int(max(left))}s left of PlumMe's own window")
        if rc and not rc[-1]["success"] and rc[-1]["failure_class"] in ("RATE_LIMITED", "BILLING_OR_CREDIT_EXHAUSTED", "CREDENTIAL_EXHAUSTED") and age(newest([d / "fruitstack/plumme-state/receipts.jsonl"])) < 600:
            waiting.append(f"last request rejected: {rc[-1]['failure_class']} (provider quota)")
        cur_info = {"episode": cur, "task": r["task"], "condition": r["condition"], "attempt": r.get("attempt"), "started_age_s": age(r.get("started_at")), "limit_s": budget["max_episode_minutes"] * 60,
                    "receipts": len(rc), "last_receipt_age_s": age(newest([d / "fruitstack/plumme-state/receipts.jsonl"])), "log_tail": next((x[:140] for x in reversed((C / f"{cur}.log").read_text(errors="replace").splitlines()
                                                                                                                                             if (C / f"{cur}.log").is_file() else []) if x.strip() and "DEBUG" not in x), None)}
    arms = sorted(str(p.with_name(p.name[: -len(".episode.json")]).relative_to(R)) for p in C.rglob("*.episode.json"))
    u = guard.usage(str(R), arms, budget["reserve_tokens_per_dispatch"]) if arms else {"dispatches": 0, "tokens": 0, "cash_usd": 0.0, "entitlement": {}}
    runlog = Path("/root/collab1-run.log")
    exit_line = next((x for x in reversed(runlog.read_text().splitlines()) if x.startswith("EXIT=")), None) if runlog.is_file() else None
    halt = (R / "PILOT_HALT").is_file() or camp.get("halted")
    if halt:
        state = f"HALTED ({camp.get('halt_reason') or 'PILOT_HALT file'})"
    elif launchers:
        hb = age(heartbeat)
        if cur is None:
            state = "RUNNING - between episodes"
        elif hb is not None and hb < FRESH_S:
            state = "PROGRESSING" + (f" (but waiting: {waiting[0]})" if waiting else "")
        elif waiting:
            state = f"WAITING: {waiting[0]}"
        elif hb is not None and hb < STALE_S:
            state = "RUNNING - model call in progress (no new file activity yet)"
        else:
            state = "STALLED? process alive, no file activity for %ss" % hb
    elif "CAMPAIGN_DONE" in "\n".join(progress[-3:]):
        state = "COMPLETED"
    elif exit_line and exit_line != "EXIT=0":
        state = f"STOPPED/FAILED ({exit_line}; see {runlog})"
    else:
        state = "NOT RUNNING"
    rep = {"claude_session": "UNKNOWN (not observable from the VPS; pytest/launcher processes below are what runs on the machine)", "state": state, "launcher": launchers, "episode_processes": episodes,
           "study": manifest["study"], "episodes": {"done": statuses.get("DONE", 0) + statuses.get("BUDGET_STOP", 0) + statuses.get("TIMEOUT", 0), "running": statuses.get("RUNNING", 0), "total": total,
                                                    "statuses": dict(statuses)}, "blocks_done": f"{blocks_done}/{len(manifest['tasks'])}", "current": cur_info, "heartbeat_age_s": age(heartbeat),
           "last_completed": last_done, "last_progress_line": progress[-1] if progress else None, "waiting_reasons": waiting, "recent_provider_errors": errors,
           "campaign_requests": f"{u['dispatches']} / {budget['cumulative']['max_dispatches']}", "campaign_tokens": f"{u['tokens']} / {budget['cumulative']['max_tokens']}", "cash_usd": u["cash_usd"],
           "entitlement": u["entitlement"], "campaign_started_age_s": age(camp.get("started_at")), "other_processes": {"pytest": ps("pytest")[:3], "c3_queue": ps("block_queue.sh")[:2]}}
    if o.json:
        print(json.dumps(rep, indent=1))
        return 0
    print(f"STATE      : {state}")
    print(f"Claude     : {rep['claude_session']}")
    print(f"Launcher   : " + (", ".join(f"PID {x['pid']} (running {x['elapsed_s']}s)" for x in launchers) or "none"))
    print(f"Episode    : " + (", ".join(f"PID {x['pid']}" for x in episodes) or "none") + (f"  -> {cur_info['task']} / {cur_info['condition']} attempt {cur_info['attempt']}, running {cur_info['started_age_s']}s of {cur_info['limit_s']}s" if cur_info else ""))
    print(f"Progress   : episodes {rep['episodes']['done']}/{total} done ({rep['episodes']['statuses']}), blocks {rep['blocks_done']}")
    print(f"Heartbeat  : newest file activity {rep['heartbeat_age_s']}s ago; current episode receipts {cur_info.get('receipts')}, last receipt {cur_info.get('last_receipt_age_s')}s ago")
    print(f"Last done  : {last_done or 'no episode finished yet'}   | last progress line: {rep['last_progress_line']}")
    print(f"Waiting    : {'; '.join(waiting) or 'nothing known'}")
    print(f"Prov.errors: {errors or 'none in the last 60 receipts'}")
    print(f"Resources  : requests {rep['campaign_requests']}, tokens {rep['campaign_tokens']}, cash USD {u['cash_usd']}, entitlement {u['entitlement'] or '-'}")
    print(f"Last log   : {cur_info.get('log_tail')}")
    print(f"Other      : pytest {[x['pid'] for x in rep['other_processes']['pytest']]}, C3 queue {[x['pid'] for x in rep['other_processes']['c3_queue']]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
