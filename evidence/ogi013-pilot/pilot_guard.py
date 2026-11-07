#!/usr/bin/env python3
"""Fail-closed resource guard for the OGI-013 pilot (stdlib only, no inference).

  pilot_guard.py verify-approval BUDGET APPROVAL        exit 0 only if APPROVAL holds the sha256 of BUDGET (the owner's explicit approval of exactly this budget)
  pilot_guard.py usage RUNS_DIR ARM [ARM ...]           print the cumulative accounting of the arm directories under RUNS_DIR
  pilot_guard.py env BUDGET ARM                         print the PeachMe session ceilings (OGI013_SESSION_MAX_*) for ARM, derived from the same budget file
  pilot_guard.py watch BUDGET RUNS_DIR PIDFILE ARM...   poll (PILOT_POLL_S, default 10 s); when a stop condition holds: write PILOT_HALT, SIGTERM the pids in PIDFILE, exit 3

Accounting unit = one provider dispatch = one row of <arm>/fruitstack/plumme-state/receipts.jsonl (agent, reviewer, specialist, retry AND simulator dispatches all land there; a simulator row in
sim-usage.jsonl that has a receipt is the SAME dispatch and is never counted twice). Fail closed:
  - a SUCCESSFUL dispatch without recorded usage halts (its cost is unknown); a FAILED one is charged `reserve_tokens_per_dispatch`, never 0;
  - a dispatch whose cash exposure is unknown (no cost class, UNKNOWN or paid class without a recorded cost) halts; known cash above `max_cash_usd` halts; entitlement use (TRIAL_CREDIT / INCLUDED) is reported;
  - an arm without a cap halts; `max_consecutive_failures` failed dispatches in a row halt (a failing route is not retried without bound);
  - precheck() is the pre-dispatch check (runners/ogi013_pilot_gate.py calls it before every agent step and simulator attempt); `watch` is only the backstop.
A missing budget, a missing/mismatched approval or an unreadable directory is a refusal (exit 2)."""
import hashlib
import json
import os
import signal
import sys
import time

ZERO_CASH = frozenset({"ANONYMOUS_FREE", "FREE_TIER", "LOCAL", "TRIAL_CREDIT", "INCLUDED"})       # no cash leaves the owner's account on these route classes
NOT_PROCESSED = frozenset({"BILLING_OR_CREDIT_EXHAUSTED", "CREDENTIAL_EXHAUSTED", "RATE_LIMITED", "AUTH_FAILED", "AUTH_EXPIRED", "FORBIDDEN", "MODEL_NOT_FOUND", "PROVIDER_UNAVAILABLE", "CONTEXT_WINDOW_EXCEEDED"})   # PlumMe's own REJECTION_CLASSES (service.py):
#  a provider answer of this class means nothing was processed -> no tokens, no cash; any OTHER failure without recorded usage (TIMEOUT, PROVIDER_UNAVAILABLE, ...) is UNCERTAIN and is charged the reserve
ENTITLEMENT = frozenset({"TRIAL_CREDIT", "INCLUDED"})                                           # ... but they consume a credit / prepaid entitlement, which is reported


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


def _requests(receipt):
    """Provider requests behind ONE receipt: PlumMe counts every adapter call of an execution (continuations of a truncated answer, credential-rotation retries) in metadata.provider_attempt_count.
    A receipt that records none (refused before egress, or an older record) still counts as one dispatch, as before - never fewer."""
    try:
        return max(1, int((receipt.get("metadata") or {}).get("provider_attempt_count") or 0))
    except (TypeError, ValueError):
        return 1


def dispatches(runs_dir, arm):
    """The arm's provider dispatches in order, each once. `simulator` marks the customer-simulator calls (their receipts are listed in sim-usage.jsonl)."""
    d = os.path.join(runs_dir, arm)
    receipts = _rows(os.path.join(d, "fruitstack/plumme-state/receipts.jsonl"))
    sim = [r for r in _rows(os.path.join(d, "sim-usage.jsonl")) if "success" in r]
    sim_ids = {r.get("receipt_id") for r in sim if r.get("receipt_id")}
    known = {r.get("receipt_id") for r in receipts}
    out = [{"receipt_id": r.get("receipt_id"), "simulator": r.get("receipt_id") in sim_ids, "success": bool(r.get("success")), "tokens": _tokens(r.get("usage")),
            "input_tokens": (r.get("usage") or {}).get("input_tokens"), "output_tokens": (r.get("usage") or {}).get("output_tokens"), "cost_usd": (r.get("usage") or {}).get("cost_usd"),
            "cost_class": r.get("cost_class"), "failure_class": r.get("failure_class"), "model": r.get("model"), "provider": r.get("provider"), "lineage": r.get("independence_key"),
            "started_at": r.get("started_at"), "finished_at": r.get("finished_at"),
            "requests": _requests(r)} for r in receipts]
    out += [{"receipt_id": r.get("receipt_id"), "simulator": True, "success": bool(r.get("success")), "tokens": _tokens(r), "input_tokens": r.get("input_tokens"),
             "output_tokens": r.get("output_tokens"), "cost_usd": r.get("cost_usd"), "cost_class": None, "failure_class": r.get("failure_class"), "model": r.get("model"), "provider": r.get("provider"), "lineage": None,
             "started_at": None, "finished_at": None, "requests": 1} for r in sim if r.get("receipt_id") not in known]            # no receipt on record: counted, and its cash exposure is unknown
    return out


def usage(runs_dir, arms, reserve=0):
    total = {"dispatches": 0, "tokens": 0, "receipts_without_usage": 0, "unmetered_failures": 0, "rejected_unprocessed": 0, "cash_usd": 0.0, "unknown_cash_exposure": 0, "entitlement": {}, "consecutive_failures": 0}
    per_arm = {}
    for arm in arms:
        a_tok, streak = 0, 0
        rows = dispatches(runs_dir, arm)
        for extra in _rows(os.path.join(runs_dir, arm, "step-accounting.jsonl")):      # tokens of requests whose execution ended in a failed receipt without usage (see ogi013_pilot_gate)
            a_tok += int(extra.get("charged_tokens") or 0) + (int(extra.get("unknown_usage_attempts") or 0) * reserve)
        for r in rows:
            if r["tokens"]:
                a_tok += r["tokens"]
            elif r["success"]:
                total["receipts_without_usage"] += 1           # succeeded but nothing recorded: the cost is unknown -> exceeded() halts
            elif r["failure_class"] in NOT_PROCESSED:
                total["rejected_unprocessed"] += 1             # rejected before processing (PlumMe's certainty NOT_EXECUTED): known zero tokens, still a dispatch and still part of a failure streak
            else:
                a_tok += reserve                               # an uncertain failure may still have been processed / billed: charged conservatively, never 0
                total["unmetered_failures"] += 1
            if isinstance(r["cost_usd"], (int, float)) and not isinstance(r["cost_usd"], bool):
                total["cash_usd"] += float(r["cost_usd"])
            elif r["cost_class"] not in ZERO_CASH:
                total["unknown_cash_exposure"] += 1            # no cost class on record, UNKNOWN, or a paid class without a recorded cost
            if r["cost_class"] in ENTITLEMENT:
                e = total["entitlement"].setdefault(r["cost_class"], {"dispatches": 0, "tokens": 0})
                e["dispatches"] += 1
                e["tokens"] += r["tokens"]
            streak = 0 if r["success"] else streak + 1
        n = sum(r["requests"] for r in rows)                  # provider REQUESTS, not receipts
        per_arm[arm] = {"dispatches": n, "tokens": a_tok, "consecutive_failures": streak}
        total["dispatches"] += n
        total["tokens"] += a_tok
        total["consecutive_failures"] = max(total["consecutive_failures"], streak)
    return {**total, "per_arm": per_arm}


def exceeded(budget, u, started_at=None, now=None):
    c = budget["cumulative"]
    why = []
    if u["dispatches"] > c["max_dispatches"]:
        why.append(f"dispatches {u['dispatches']} > {c['max_dispatches']}")
    if u["tokens"] > c["max_tokens"]:
        why.append(f"tokens {u['tokens']} > {c['max_tokens']}")
    if u.get("receipts_without_usage"):
        why.append(f"MISSING_USAGE: {u['receipts_without_usage']} successful dispatch(es) recorded no token usage (fail closed)")
    if u.get("unknown_cash_exposure"):
        why.append(f"UNKNOWN_CASH_EXPOSURE: {u['unknown_cash_exposure']} dispatch(es) with no known zero-cash route class and no recorded cost (fail closed)")
    if c.get("max_cash_usd") is not None and u.get("cash_usd", 0.0) > c["max_cash_usd"] + 1e-9:
        why.append(f"cash {u['cash_usd']:.6f} USD > {c['max_cash_usd']}")
    limit = budget.get("max_consecutive_failures")
    if limit and u.get("consecutive_failures", 0) >= limit:
        why.append(f"{u['consecutive_failures']} consecutive failed dispatches (limit {limit}): the failing route is not retried further")
    for arm, a in u["per_arm"].items():
        cap = arm_cap(budget, arm)
        if cap is None:
            why.append(f"arm {arm} has no cap in the budget (fail closed)")
        elif a["dispatches"] > cap["max_dispatches"] or a["tokens"] > cap["max_tokens"]:
            why.append(f"arm {arm} over its cap ({a})")
    if started_at is not None and ((now or time.time()) - started_at) / 60 > c["max_wall_minutes"]:
        why.append("wall clock over the cap")
    return why


def precheck(budget, runs_dir, arms, arm, started_at=None, now=None):
    """Reasons to refuse the NEXT provider dispatch of `arm` (empty = allowed): the pilot is already halted or over a cap, usage or cash exposure is unknown, or the next dispatch plus its token
    reserve would cross a cap."""
    if os.path.exists(os.path.join(runs_dir, "PILOT_HALT")):
        return ["PILOT_HALT exists"]
    reserve = budget.get("reserve_tokens_per_dispatch")
    if not isinstance(reserve, int) or reserve <= 0:
        return ["budget declares no reserve_tokens_per_dispatch (fail closed)"]
    u = usage(runs_dir, arms, reserve)
    why = exceeded(budget, u, started_at, now)
    if why:
        return why
    c, cap, a = budget["cumulative"], arm_cap(budget, arm), u["per_arm"].get(arm, {"dispatches": 0, "tokens": 0})
    if cap is None:
        return [f"arm {arm} has no cap in the budget (fail closed)"]
    for scope, used, limit in (("pilot", u, c), (f"arm {arm}", a, cap)):
        if used["dispatches"] + 1 > limit["max_dispatches"]:
            why.append(f"{scope}: next dispatch would exceed {limit['max_dispatches']} dispatches")
        if used["tokens"] + reserve > limit["max_tokens"]:
            why.append(f"{scope}: next dispatch (reserve {reserve}) would exceed {limit['max_tokens']} tokens")
    return why


def arm_cap(budget, arm):
    """The cap of an arm. The approved budget names its arms by role under its own label (pilot-1/single); another run of the SAME plan lives under another pilot id (pilot-2/single) with the same approved
    limits and the same file hash, so a cap is found by the exact name first, else by the arm's role (the part after the last '/') when that role is unique in the budget. None = no cap (fail closed)."""
    caps = budget["arms"]
    if arm in caps:
        return caps[arm]
    hits = [v for k, v in caps.items() if k.rsplit("/", 1)[-1] == arm.rsplit("/", 1)[-1]]
    if len(hits) == 1:
        return hits[0]
    return budget.get("default_arm_cap") if not hits else None          # a campaign of many episodes declares ONE per-episode cap for all of them; an ambiguous role is still no cap


def session_env(budget, arm):
    """PeachMe's shared execution-budget ceilings for the arm's agent-side dispatches (the simulator is covered by precheck). Cash: the budget's max_cash_usd (0 = no cash authorised)."""
    cap = arm_cap(budget, arm)
    return {"OGI013_SESSION_MAX_CALLS": str(cap["max_dispatches"]), "OGI013_SESSION_MAX_TOKENS": str(cap["max_tokens"]),
            "OGI013_SESSION_MAX_COST_USD": repr(float(budget["cumulative"].get("max_cash_usd") or 0.0))}


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
    if len(argv) == 4 and argv[1] == "env":
        for k, v in session_env(json.load(open(argv[2])), argv[3]).items():
            print(f"export {k}={v}")
        return 0
    if len(argv) >= 6 and argv[1] == "watch":
        budget = json.load(open(argv[2]))
        start = time.time()
        poll = float(os.environ.get("PILOT_POLL_S", "10"))
        while True:
            u = usage(argv[3], argv[5:], budget.get("reserve_tokens_per_dispatch") or 0)
            why = exceeded(budget, u, start)
            if why:
                if not os.path.exists(os.path.join(argv[3], "PILOT_HALT")):
                    open(os.path.join(argv[3], "PILOT_HALT"), "w").write(json.dumps({"why": why, "usage": u, "by": "watch"}))
                for pid in open(argv[4]).read().split():
                    try:
                        os.killpg(os.getpgid(int(pid)), signal.SIGTERM)       # the run was started with setsid: its whole process group (bootstrap + runner) stops
                    except OSError:
                        pass
                print("HALT", why)
                return 3
            time.sleep(poll)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
