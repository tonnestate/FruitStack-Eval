"""Host check of the Code Mode facade (engineering check, not a result): the QA-2D T arm (ogi013_qa2d.run_T) and the facade duo (ogi013_codemode_duo.run_T_codemode) on the same questions,
one RunBudget for both. usage: hostcheck_codemode.py DATA.jsonl IDS(comma) CAP  (run through the launcher with OGI013_RUNNER=runners/hostcheck_codemode.py)"""
import hashlib
import json
import sys
import time
from pathlib import Path

import ogi013_codemode_duo as cm
import ogi013_qa1 as q1
import ogi013_qa2d as q2
from ogi013_qa1 import Context, attempt, load_jsonl

sent: list = []
arm_now = {"arm": None}


def wrap_luna(fn):
    def inner(ctx, prompt):
        sent.append({"arm": arm_now["arm"], "member": "luna", "chars": len(prompt), "sha": hashlib.sha256(prompt.encode()).hexdigest()})
        return fn(ctx, prompt)
    return inner


def wrap_nemo(fn):
    def inner(ctx, ep, prompt):
        sent.append({"arm": arm_now["arm"], "member": "nemo", "chars": len(prompt), "sha": hashlib.sha256(prompt.encode()).hexdigest()})
        return fn(ctx, ep, prompt)
    return inner


def main(argv) -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--ids", required=True)
    ap.add_argument("--cap", type=int, default=40)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    ctx = Context(a.out, None, 2)
    from plumme.budget import RunBudget
    budget = RunBudget(max_provider_calls=a.cap, max_cost_usd=0.0)
    ctx.stack.svc.set_run_budget(budget)
    ctx.run_budget = budget
    import ogi013_vote
    ogi013_vote.TEXT_CAP_OBJECTION = ogi013_vote.TEXT_CAP_REPLY = 10 ** 6
    q1.luna_step = wrap_luna(q1.luna_step)
    q2.luna_step = wrap_luna(q2.luna_step)
    q2.nemo_step = wrap_nemo(q2.nemo_step)
    qs = {q["id"]: q for q in load_jsonl(a.data)}
    out = []
    for qid in a.ids.split(","):
        q = qs[qid]
        for arm, fn in (("T", q2.run_T), ("TC", cm.run_T_codemode)):
            if ctx.stop:
                break
            arm_now["arm"] = arm
            n0, t0, b0 = len(sent), time.monotonic(), budget.provider_attempt_count
            res = attempt(fn, ctx, q)
            mine = sent[n0:]
            first = [m for m in mine][:2]
            row = {"qid": qid, "arm": arm, "status": res["status"], "detail": res.get("detail"), "letter": res.get("letter"), "key": q["key"], "stop": res.get("stop"), "calls": res.get("calls"),
                   "tokens": res.get("tokens"), "prompt_chars_sent": sum(m["chars"] for m in mine), "n_prompts": len(mine), "seconds": round(time.monotonic() - t0, 1),
                   "provider_attempts": budget.provider_attempt_count - b0, "first_prompt_sha256": sorted({m["sha"] for m in first}), "exchanges": res.get("exchanges"),
                   "communication": res.get("communication"), "mango_writes": res.get("mango_writes"), "mango_reads": res.get("mango_reads"),
                   "provenance_ops": len(res.get("provenance") or []), "answer_changes": res.get("answer_changes"), "objections": res.get("objections")}
            out.append(row)
            print(json.dumps(row, default=str), flush=True)
    shas = {r["arm"] + r["qid"]: r["first_prompt_sha256"] for r in out}
    ident = all(len(v) == 1 for v in shas.values()) and len({v[0] for v in shas.values() if v}) == len({r["qid"] for r in out})
    print(json.dumps({"summary": True, "first_prompt_identical_per_question_across_arms": ident, "provider_attempts_total": budget.provider_attempt_count, "cap": a.cap, "stop": ctx.stop}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
