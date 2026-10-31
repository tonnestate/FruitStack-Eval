"""Exact compatibility check before QA-1 L rows are reused as QA-2D SL rows (no model call): same items, same prompt bytes, same Codex invocation, all rows usable.
usage: check_sl_reuse.py QA2D_ITEMS.jsonl QA1_STUDY.jsonl QA1_RESULTS.jsonl"""
import json
import subprocess
import sys
from types import SimpleNamespace

import ogi013_qa1 as q1
import ogi013_qa2d as q2


def main(items_p, study_p, results_p) -> int:
    items, study = q1.load_jsonl(items_p), q1.load_jsonl(study_p)
    l_rows = [r for r in q1.load_jsonl(results_p) if r["arm"] == "L"]
    report = {}
    first = items[: len(study)]
    report["same_ids_in_order"] = [q["id"] for q in first] == [q["id"] for q in study]
    report["same_question_text_options_key"] = all((a["question"], a["options"], a["key"]) == (b["question"], b["options"], b["key"]) for a, b in zip(first, study))
    report["prompt_bytes_identical"] = all(q2.answer_prompt(q) == q1.question_prompt(q) + q1.ANSWER_SUFFIX for q in study)
    report["l_rows"] = len(l_rows)
    report["l_rows_all_ok"] = all(r["status"] == "OK" for r in l_rows)
    report["l_ids_match"] = sorted(r["qid"] for r in l_rows) == sorted(q["id"] for q in study)
    # the Codex invocation of run_L and luna_step: same argv, same stdin, same environment home
    calls = []
    real = subprocess.run

    def fake(args, **kw):
        args = [("<tmpdir>" if args[i - 1] == "-C" else a) for i, a in enumerate(args)]      # the working directory is a fresh temp dir per call
        calls.append({"args": args, "input": kw.get("input"), "codex_home": (kw.get("env") or {}).get("CODEX_HOME"), "timeout": kw.get("timeout")})
        ev = json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "ANSWER: A"}})
        return SimpleNamespace(returncode=0, stdout=ev, stderr="")
    q1.subprocess.run = fake
    try:
        ctx = SimpleNamespace(stop=None, run_budget=None, luna_tokens=0)
        q = study[0]
        q1.run_L(SimpleNamespace(), q)
        q1.luna_step(ctx, q2.answer_prompt(q))
    finally:
        q1.subprocess.run = real
    report["codex_invocation_identical"] = len(calls) == 2 and calls[0] == calls[1]
    ok = all(v for k, v in report.items() if k != "l_rows") and report["l_rows"] == len(study)
    report["compatible"] = ok
    print(json.dumps(report, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(*sys.argv[1:4]))
