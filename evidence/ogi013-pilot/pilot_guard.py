#!/usr/bin/env python3
"""Fail-closed resource guard for the OGI-013 pilot (stdlib only, no inference).

  pilot_guard.py verify-approval BUDGET APPROVAL        exit 0 only if APPROVAL holds the sha256 of BUDGET (the owner's explicit approval of exactly this budget)
  pilot_guard.py usage RUNS_DIR ARM [ARM ...]           print cumulative dispatches/tokens of the arm directories under RUNS_DIR
  pilot_guard.py watch BUDGET RUNS_DIR PIDFILE ARM...   poll every 10 s; when any cap is exceeded: write HALT, SIGTERM the pids in PIDFILE, exit 3
Dispatches = receipt rows + simulator call rows; tokens = recorded input+output usage. A missing budget, a missing/mismatched approval or an unreadable directory is a refusal (exit 2).
Fail closed: a SUCCESSFUL dispatch that recorded no usage halts the pilot (its cost is unknown); a failed dispatch without usage is charged `reserve_tokens_per_dispatch`, never 0; an arm without a cap
in the budget halts. precheck() is the pre-dispatch check (runners/ogi013_pilot_gate.py calls it before every provider dispatch); `watch` stays as the backstop."""
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


def _tokens(u):
    u = u or {}
    return (u.get("input_tokens") or 0) + (u.get("output_tokens") or 0) or (u.get("total_tokens") or 0)


def usage(runs_dir, arms, reserve=0):
    dispatches = tokens = missing = unmetered = 0
    per_arm = {}
    for arm in arms:
        d = os.path.join(runs_dir, arm)
        rows = [(r.get("success"), _tokens(r.get("usage"))) for r in _rows(os.path.join(d, "fruitstack/plumme-state/receipts.jsonl"))]
        rows += [(r.get("success"), _tokens(r)) for r in _rows(os.path.join(d, "sim-usage.jsonl")) if "success" in r]
        a_tok = 0
        for ok, t in rows:
            if t:
                a_tok += t
            elif ok:
                missing += 1                                   # succeeded but nothing recorded: the cost is unknown -> exceeded() halts
            else:
                a_tok += reserve                               # a failure may still have been billed: charged conservatively, never 0
                unmetered += 1
        per_arm[arm] = {"dispatches": len(rows), "tokens": a_tok}
        dispatches += len(rows)
        tokens += a_tok
    return {"dispatches": dispatches, "tokens": tokens, "receipts_without_usage": missing, "unmetered_failures": unmetered, "per_arm": per_arm}


def exceeded(budget, u, started_at=None, now=None):
    c = budget["cumulative"]
    why = []
    if u["dispatches"] > c["max_dispatches"]:
        why.append(f"dispatches {u['dispatches']} > {c['max_dispatches']}")
    if u["tokens"] > c["max_tokens"]:
        why.append(f"tokens {u['tokens']} > {c['max_tokens']}")
    if u.get("receipts_without_usage"):
        why.append(f"MISSING_USAGE: {u['receipts_without_usage']} successful dispatch(es) recorded no token usage (fail closed)")
    for arm, a in u["per_arm"].items():
        cap = budget["arms"].get(arm)
        if cap is None:
            why.append(f"arm {arm} has no cap in the budget (fail closed)")
        elif a["dispatches"] > cap["max_dispatches"] or a["tokens"] > cap["max_tokens"]:
            why.append(f"arm {arm} over its cap ({a})")
    if started_at is not None and ((now or time.time()) - started_at) / 60 > c["max_wall_minutes"]:
        why.append("wall clock over the cap")
    return why


def precheck(budget, runs_dir, arms, arm, started_at=None, now=None):
    """Reasons to refuse the NEXT provider dispatch of `arm` (empty = allowed): the pilot is already halted or over a cap, usage is missing, or the next dispatch plus its token reserve would cross a cap."""
    if os.path.exists(os.path.join(runs_dir, "PILOT_HALT")):
        return ["PILOT_HALT exists"]
    reserve = budget.get("reserve_tokens_per_dispatch")
    if not isinstance(reserve, int) or reserve <= 0:
        return ["budget declares no reserve_tokens_per_dispatch (fail closed)"]
    u = usage(runs_dir, arms, reserve)
    why = exceeded(budget, u, started_at, now)
    if why:
        return why
    c, cap, a = budget["cumulative"], budget["arms"].get(arm), u["per_arm"].get(arm, {"dispatches": 0, "tokens": 0})
    if cap is None:
        return [f"arm {arm} has no cap in the budget (fail closed)"]
    for scope, used, limit in (("pilot", u, c), (f"arm {arm}", a, cap)):
        if used["dispatches"] + 1 > limit["max_dispatches"]:
            why.append(f"{scope}: next dispatch would exceed {limit['max_dispatches']} dispatches")
        if used["tokens"] + reserve > limit["max_tokens"]:
            why.append(f"{scope}: next dispatch (reserve {reserve}) would exceed {limit['max_tokens']} tokens")
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
            u = usage(argv[3], argv[5:], budget.get("reserve_tokens_per_dispatch") or 0)
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
