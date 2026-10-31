"""DETERMINISTIC REPLAY of a recorded disagreement (integration test only, NOT benchmark evidence): the QA-2D T arm and the Code Mode facade arm on the real stack (MangoMe, ledger, sandbox
verifier) with scripted member outputs taken from a recorded exchange. No model call is made. usage (via the launcher): replay_disagreement.py --data D.jsonl --out O --qid 8512 --recorded EXCHANGE.json"""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import ogi013_codemode_duo as cm
import ogi013_qa1 as q1
import ogi013_qa2d as q2
from ogi013_qa1 import Context, attempt, load_jsonl


def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--qid", required=True)
    ap.add_argument("--recorded", type=Path, required=True)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    rec = json.loads(a.recorded.read_text())
    q = next(x for x in load_jsonl(a.data) if x["id"] == a.qid)
    luna_first, nemo_first = rec["first_answers"][0]["text"], rec["first_answers"][1]["text"]
    objection = rec["objections"][0]["text"]                                  # nemotron's objection against Luna's answer
    reply = rec["objections"][0]["replies"][0]["text"]                        # Luna's concession
    ctx = Context(a.out, None, 2)
    import ogi013_vote
    ogi013_vote.TEXT_CAP_OBJECTION = ogi013_vote.TEXT_CAP_REPLY = 10 ** 6
    sent, arm_now = [], {"arm": None}

    def script(member: str, prompt: str) -> dict:
        sent.append({"arm": arm_now["arm"], "member": member, "chars": len(prompt), "sha": hashlib.sha256(prompt.encode()).hexdigest()})
        if prompt.startswith(q2.answer_prompt(q)) and "colleague" not in prompt:
            out = luna_first if member == "luna" else nemo_first
        elif "A colleague's answer to this question" in prompt:
            out = "ISSUES: NONE" if member == "luna" else objection
        elif "Objection O1 against your answer" in prompt:
            out = reply
        else:
            raise RuntimeError(f"unscripted prompt for {member}: {prompt[:80]!r}")
        return {"success": True, "output": out, "model_key": q1.LUNA_KEY if member == "luna" else q1.NEMO_KEY,
                "independence_key": q1.LUNA_LINEAGE if member == "luna" else q1.NEMO_LINEAGE}
    q1.luna_step = lambda c, p: script("luna", p)
    q2.luna_step = lambda c, p: script("luna", p)
    q2.nemo_step = lambda c, ep, p: script("nemo", p)
    rows = []
    for arm, fn in (("T", q2.run_T), ("TC", cm.run_T_codemode)):
        arm_now["arm"] = arm
        n0, t0 = len(sent), time.monotonic()
        res = attempt(fn, ctx, q)
        mine = sent[n0:]
        rows.append({"arm": arm, "status": res["status"], "detail": res.get("detail"), "letter": res.get("letter"), "key": q["key"], "stop": res.get("stop"), "calls": res.get("calls"),
                     "n_prompts": len(mine), "prompt_chars_sent": sum(m["chars"] for m in mine), "first_prompt_sha256": sorted({m["sha"] for m in mine[:2]}),
                     "objections": res.get("objections"), "verified_objections": res.get("verified_objections"), "formal_objections": res.get("formal_objections"),
                     "accepted_concessions": res.get("accepted_concessions"), "answer_changes": res.get("answer_changes"),
                     "objection_states": res.get("objection_states"), "mango_writes": res.get("mango_writes"), "provenance_ops": len(res.get("provenance") or []),
                     "communication": res.get("communication"), "ops": [e.get("op") for e in (res.get("provenance") or [])], "seconds": round(time.monotonic() - t0, 1)})
        print(json.dumps(rows[-1], default=str), flush=True)
    print(json.dumps({"summary": True, "label": "DETERMINISTIC_REPLAY (integration test, not benchmark evidence)", "model_calls": 0,
                      "first_prompts_identical": rows[0]["first_prompt_sha256"] == rows[1]["first_prompt_sha256"] and len(rows[0]["first_prompt_sha256"]) == 1}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
