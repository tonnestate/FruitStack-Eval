#!/usr/bin/env python3
"""Fail-closed resource guard for the OGI-013 pilot (stdlib only, no inference).

  pilot_guard.py verify-approval BUDGET APPROVAL        exit 0 only if APPROVAL holds the sha256 of BUDGET (the owner's explicit approval of exactly this budget)
  pilot_guard.py usage RUNS_DIR ARM [ARM ...]           print cumulative dispatches/tokens of the arm directories under RUNS_DIR
  pilot_guard.py watch BUDGET RUNS_DIR PIDFILE ARM...   poll every 10 s; when any cap is exceeded: write HALT, SIGTERM the pids in PIDFILE, exit 3
Dispatches = receipt rows + simulator call rows; tokens = recorded input+output usage. A missing budget, a missing/mismatched approval or an unreadable directory is a refusal (exit 2)."""
import hashlib
import json
import os
import signal
import sys
import time


def _rows(path):
    if not os.path.isfile(path):
        return []
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except ValueError:
                pass
    return out


def usage(runs_dir, arms):
    dispatches = tokens = no_usage = 0
    per_arm = {}
    for arm in arms:
        d = os.path.join(runs_dir, arm)
        rc = _rows(os.path.join(d, "fruitstack/plumme-state/receipts.jsonl"))
        sim = [r for r in _rows(os.path.join(d, "sim-usage.jsonl")) if "success" in r]
        a_tok = sum(((r.get("usage") or {}).get("input_tokens") or 0) + ((r.get("usage") or {}).get("output_tokens") or 0) for r in rc)
        a_tok += sum((r.get("input_tokens") or 0) + (r.get("output_tokens") or 0) for r in sim)
        no_usage += sum(1 for r in rc if not (r.get("usage") or {}).get("input_tokens") and not (r.get("usage") or {}).get("output_tokens"))
        per_arm[arm] = {"dispatches": len(rc) + len(sim), "tokens": a_tok}
        dispatches += len(rc) + len(sim)
        tokens += a_tok
    return {"dispatches": dispatches, "tokens": tokens, "receipts_without_usage": no_usage, "per_arm": per_arm}


def exceeded(budget, u, started_at=None, now=None):
    c = budget["cumulative"]
    why = []
    if u["dispatches"] > c["max_dispatches"]:
        why.append(f"dispatches {u['dispatches']} > {c['max_dispatches']}")
    if u["tokens"] > c["max_tokens"]:
        why.append(f"tokens {u['tokens']} > {c['max_tokens']}")
    for arm, a in u["per_arm"].items():
        cap = budget["arms"].get(arm)
        if cap and (a["dispatches"] > cap["max_dispatches"] or a["tokens"] > cap["max_tokens"]):
            why.append(f"arm {arm} over its cap ({a})")
    if started_at is not None and ((now or time.time()) - started_at) / 60 > c["max_wall_minutes"]:
        why.append("wall clock over the cap")
    return why


def verify_approval(budget_path, approval_path):
    if not (os.path.isfile(budget_path) and os.path.isfile(approval_path)):
        return False
    return open(approval_path).read().split()[0:1] == [hashlib.sha256(open(budget_path, "rb").read()).hexdigest()]


def main(argv):
    if len(argv) >= 4 and argv[1] == "verify-approval":
        ok = verify_approval(argv[2], argv[3])
        print("APPROVED" if ok else "REFUSED: no approval for exactly this budget")
        return 0 if ok else 2
    if len(argv) >= 4 and argv[1] == "usage":
        print(json.dumps(usage(argv[2], argv[3:])))
        return 0
    if len(argv) >= 6 and argv[1] == "watch":
        budget = json.load(open(argv[2]))
        start = time.time()
        while True:
            u = usage(argv[3], argv[5:])
            why = exceeded(budget, u, start)
            if why:
                open(os.path.join(argv[3], "PILOT_HALT"), "w").write(json.dumps({"why": why, "usage": u}))
                for pid in open(argv[4]).read().split():
                    try:
                        os.killpg(os.getpgid(int(pid)), signal.SIGTERM)       # the run was started with setsid: its whole process group (bootstrap + runner) stops
                    except OSError:
                        pass
                print("HALT", why)
                return 3
            time.sleep(10)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
