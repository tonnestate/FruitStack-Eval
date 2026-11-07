#!/usr/bin/env python3
"""QA-1 descriptive T trace, addendum (lead decision 2026-10-31; separate from the sealed analyze_qa1.py, outside the confirmatory family). usage: analyze_qa1_trace.py RESULTS.jsonl S_MODEL
Reports: distribution of T's stop reasons per question; questions on which T's final answer differs from both solvers' first answers; the number of discordant pairs per comparison;
whether the S model was pinned as T's solver 1 on every question."""
import json
import sys
from collections import Counter


def stop_class(r: dict) -> str:
    if r.get("status") != "OK":
        return "infrastructure_failed"
    stop, how, firsts = r.get("stop"), r.get("how"), r.get("first_letters") or {}
    if stop == "NO_SECOND_SOLVER":
        return "NO_SECOND_SOLVER"
    if stop == "NO_ISSUES" and len(set(firsts.values())) == 1 and not r.get("answer_changes"):
        return "both_solvers_agreed_challenge_found_nothing"
    if r.get("answer_changes"):
        return "revision_changed_an_answer"
    if how == "specialist" or r.get("specialist_letter"):
        return "specialist_decided"
    if stop in ("CONVERGED", "NO_CHANGE", "LOOP_GUARD_ROUNDS", "LOOP_GUARD_FAILURES"):
        return stop.lower()
    return "other"


def trace(path: str, s_model: str) -> dict:
    rows = {}
    for l in open(path):
        if l.strip():
            r = json.loads(l)
            rows[(r["qid"], r["arm"])] = r
    qids = sorted({q for q, a in rows if a == "T"})
    t = {q: rows[(q, "T")] for q in qids}
    differs = sum(1 for q, r in t.items() if r.get("status") == "OK" and r.get("letter") and r.get("first_letters")
                  and all(r["letter"] != l for l in r["first_letters"].values() if l))
    pinned = [q for q, r in t.items() if r.get("status") == "OK" and (r.get("roster") or {}).get("roster", {}).get("solver1") == s_model or
              any(c.get("role") == "solver1" for c in (r.get("roster") or {}).get("changes", []))]
    ok_rows = [r for r in t.values() if r.get("status") == "OK"]
    solver1_models = Counter(((r.get("roster") or {}).get("roster") or {}).get("solver1") for r in ok_rows)
    disc = {}
    for other in ("S", "E", "L"):
        b = sum(1 for q in qids if (q, other) in rows and t[q]["correct"] and not rows[(q, other)]["correct"])
        c = sum(1 for q in qids if (q, other) in rows and rows[(q, other)]["correct"] and not t[q]["correct"])
        disc[f"T vs {other}"] = {"T_only": b, "other_only": c, "discordant_pairs": b + c}
    return {"questions": len(qids), "t_stop_reasons": dict(Counter(stop_class(r) for r in t.values())), "final_differs_from_both_first_answers": differs,
            "discordant_pairs": disc, "solver1_model_on_ok_T_questions": dict(solver1_models), "s_model": s_model,
            "s_pinned_as_solver1_on_every_ok_question": all(m == s_model for m in solver1_models) if solver1_models else None,
            "roster_changes_on_solver1": sum(1 for r in ok_rows for c in (r.get("roster") or {}).get("changes", []) if c.get("role") == "solver1")}


if __name__ == "__main__":
    print(json.dumps(trace(sys.argv[1], sys.argv[2]), indent=1))
