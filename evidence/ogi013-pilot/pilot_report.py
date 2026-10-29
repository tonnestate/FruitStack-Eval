#!/usr/bin/env python3
"""Comparative report of the OGI-013 pilot: ONE matched SINGLE vs COLLAB episode on the official tau2 benchmark (stdlib only; reads what the run wrote, never calls a model).

  pilot_report.py mark PILOT_DIR ARM start CODE_DIR SLOT_DIR     record the arm's launch conditions (code head, ledger heads, env flags) in PILOT_DIR/conditions-ARM.json
  pilot_report.py mark PILOT_DIR ARM end EXIT_CODE               record when the arm ended and how
  pilot_report.py report RUNS_DIR PILOT_DIR BUDGET               write PILOT_DIR/report.json + report.md and print the markdown

The verdict keeps four things apart: (1) the benchmark executed for both arms, (2) independent review / a collaborative intervention actually took place, (3) an improvement over SINGLE was observed in
this pair with a documented mechanism, (4) statistical evidence - which one paired task can never establish."""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("pilot_guard", HERE / "pilot_guard.py")
guard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(guard)

ARMS = ("single", "collab")
FLAGS = ("OGI013_ORG_COLLAB", "OGI013_ORG_POLICY_MODE", "PILOT_SESSION_MAX_CALLS", "PILOT_SESSION_MAX_TOKENS", "PILOT_SESSION_MAX_COST_USD")


def _jsonl(path):
    out = []
    if Path(path).is_file():
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            try:
                out.append(json.loads(line))
            except ValueError:
                pass
    return out


def _git(*args):
    r = subprocess.run(["git", *args], capture_output=True, text=True, timeout=60)
    return r.stdout.strip() if r.returncode == 0 else None


def mark(pilot_dir, arm, phase, a=None, b=None):
    path = Path(pilot_dir) / f"conditions-{arm}.json"
    rec = json.loads(path.read_text()) if path.is_file() else {}
    if phase == "start":
        rec.update({"arm": arm, "started_at": time.time(), "code_head": _git("-C", a, "rev-parse", "HEAD"),
                    "slot_heads": {n: _git("--git-dir", f"{b}/ledgers/{n}.git", "rev-parse", "HEAD") for n in ("chat", "project")}, "env": {k: os.environ.get(k) for k in FLAGS}})
    else:
        rec.update({"ended_at": time.time(), "exit_code": int(a) if a is not None else None})
    path.write_text(json.dumps(rec, indent=1))


def _arm(runs_dir, pilot_dir, name, reserve):
    rel = f"{Path(pilot_dir).name}/{name}"
    root = Path(runs_dir) / rel
    task_dirs = sorted((root / "tasks").glob("*")) if (root / "tasks").is_dir() else []
    td = task_dirs[0] if task_dirs else root / "tasks" / "_missing"
    official = json.loads((td / "official-result.json").read_text()) if (td / "official-result.json").is_file() else None
    events = _jsonl(td / "fruitstack-events.jsonl")
    rows = guard.dispatches(str(runs_dir), rel)
    u = guard.usage(str(runs_dir), [rel], reserve)
    cond = json.loads((Path(pilot_dir) / f"conditions-{name}.json").read_text()) if (Path(pilot_dir) / f"conditions-{name}.json").is_file() else {}
    ri = (official or {}).get("reward_info") or {}
    calls = [{"name": tc.get("name"), "arguments": tc.get("arguments")} for m in (official or {}).get("messages", []) if m.get("role") == "assistant" for tc in (m.get("tool_calls") or [])]
    last = next((m.get("content") for m in reversed((official or {}).get("messages", [])) if m.get("role") == "assistant" and m.get("content")), None)
    sim_rows = [r for r in _jsonl(root / "sim-usage.jsonl") if "success" in r]
    log = Path(pilot_dir) / f"{name}.log"
    heads = dict(line.split()[1].split("=", 1) for line in (log.read_text(errors="replace").splitlines() if log.is_file() else []) if line.startswith("OGI013_SOURCE "))
    agent = [r for r in rows if not r["simulator"]]
    collabs = [e for e in events if e.get("event") == "ORG_COLLAB"]
    wall = (cond.get("ended_at") - cond["started_at"]) if cond.get("ended_at") and cond.get("started_at") else None
    return {
        "arm": name, "official_result_present": official is not None, "reward": ri.get("reward") if official else None, "termination_reason": (official or {}).get("termination_reason"),
        "action_checks": [{"name": (c.get("action") or {}).get("name"), "matched": c.get("action_match")} for c in (ri.get("action_checks") or [])],
        "task_id": (official or {}).get("task_id"), "seed": (official or {}).get("seed"), "policy_sha256": hashlib.sha256(((official or {}).get("policy") or "").encode()).hexdigest() if official else None,
        "official_duration_s": (official or {}).get("duration"), "wall_clock_s": wall, "interrupted": (td / "RUN_INTERRUPTED.json").is_file(),
        "budget_stops": [e for e in events if e.get("event") == "BUDGET_STOP"], "actions": calls, "final_message": last,
        "conditions": cond, "component_heads": heads, "simulator_model_keys": sorted({str(r.get("model_key")) for r in sim_rows}),
        "resources": {"dispatches": u["dispatches"], "agent_dispatches": len(agent), "simulator_dispatches": len(rows) - len(agent), "successful": sum(1 for r in rows if r["success"]),
                      "failed": sum(1 for r in rows if not r["success"]), "rejected_before_processing": u["rejected_unprocessed"], "tokens_recorded": sum(r["tokens"] for r in rows),
                      "tokens_charged_incl_uncertain_failures": u["tokens"], "successful_without_usage": u["receipts_without_usage"], "uncertain_failures_charged_at_reserve": u["unmetered_failures"],
                      "cash_usd_recorded": u["cash_usd"], "unknown_cash_exposure_dispatches": u["unknown_cash_exposure"], "entitlement_use": u["entitlement"],
                      "dispatches_with_null_cost_usd": sum(1 for r in rows if r["cost_usd"] is None), "cost_classes": dict(Counter(str(r["cost_class"]) for r in rows)),
                      "models": dict(Counter(f"{r['provider']}/{r['model']}" for r in agent)), "agent_lineages": sorted({r["lineage"] for r in agent if r["lineage"]}),
                      "agent_dispatches_with_unknown_lineage": sum(1 for r in agent if not r["lineage"])},
        "collaboration": {"reviews": [{k: e.get(k) for k in ("purpose", "action", "draft", "final", "changed", "improved", "validated", "ungrounded_agreement", "final_reviewed", "independent_review",
                                                              "review_unavailable", "specialist", "calls", "stop", "unresolved", "overruled", "agreement", "attribution", "trail", "failures")} for e in collabs],
                          "revisions": [e for e in events if e.get("event") == "ORG_REVISION"], "skipped": dict(Counter(e.get("reason") for e in events if e.get("event") == "ORG_SKIPPED")),
                          "errors": [e for e in events if e.get("event") == "ORG_ERROR"], "collaboration_calls": sum(int(c.get("calls") or 0) for c in collabs)},
    }


def caveats(arms, identical, reviews):
    """What a single paired episode cannot separate from the effect of the collaboration. Always stated, so a reader never mistakes a pilot result for evidence."""
    s, c = arms["single"]["resources"], arms["collab"]["resources"]
    out = ["n = 1 task, 1 episode per arm: any reward difference may be run-to-run variance of the agent models, the customer simulator or the providers; no effect size or significance can be claimed.",
           "The customer simulator is an LLM: its replies are not identical across the arms, so the two conversations can diverge for reasons unrelated to the agent.",
           f"Fixed arm order (SINGLE first) on shared free-tier quotas: provider rejections before processing were {s['rejected_before_processing']} (SINGLE) vs {c['rejected_before_processing']} (COLLAB); supply conditions may differ.",
           "COLLAB reviews write actions only, and the pilot task has few of them: the opportunity for an intervention is small."]
    if not identical:
        out.append("The controls check FAILED or is incomplete: the arms are not demonstrably comparable.")
    if not reviews:
        out.append("COLLAB performed no collaboration review: this episode tested nothing about the collaboration.")
    return out


def build_report(runs_dir, pilot_dir, budget_path):
    budget = json.loads(Path(budget_path).read_text())
    reserve = int(budget.get("reserve_tokens_per_dispatch") or 0)
    arms = {n: _arm(runs_dir, pilot_dir, n, reserve) for n in ARMS}
    s, c = arms["single"], arms["collab"]
    pinned = budget.get("simulator_model_key")
    checks = {
        "task_id": (s["task_id"], c["task_id"]), "seed": (s["seed"], c["seed"]), "policy_sha256": (s["policy_sha256"], c["policy_sha256"]),
        "simulator_model_keys": (s["simulator_model_keys"], c["simulator_model_keys"]),
        "code_head": (s["conditions"].get("code_head"), c["conditions"].get("code_head")), "component_heads": (s["component_heads"], c["component_heads"]), "ledger_heads_at_start": (s["conditions"].get("slot_heads"), c["conditions"].get("slot_heads")),
    }
    controls = {k: {"single": a, "collab": b, "equal": a == b and a not in (None, [], {}, (None, None))} for k, (a, b) in checks.items()}
    controls["simulator_is_the_pinned_model"] = {"pinned": pinned, "equal": all(arm["simulator_model_keys"] in ([pinned], []) for arm in arms.values()) and bool(s["simulator_model_keys"] or c["simulator_model_keys"])}
    controls["budget_sha256"] = {"value": hashlib.sha256(Path(budget_path).read_bytes()).hexdigest(), "equal": True}
    flags_ok = s["conditions"].get("env", {}).get("OGI013_ORG_COLLAB") in (None, "") and c["conditions"].get("env", {}).get("OGI013_ORG_COLLAB") == "1"
    controls["only_intended_difference"] = {"single_collab_flag": s["conditions"].get("env", {}).get("OGI013_ORG_COLLAB"), "collab_collab_flag": c["conditions"].get("env", {}).get("OGI013_ORG_COLLAB"), "equal": flags_ok}
    identical = all(v["equal"] for v in controls.values())

    reviews = c["collaboration"]["reviews"]
    executed = all(a["official_result_present"] and a["reward"] is not None and not a["interrupted"] and not a["budget_stops"] for a in arms.values())
    independent = any(r.get("independent_review") for r in reviews)
    intervention = any(r.get("improved") for r in reviews) and bool(c["collaboration"]["revisions"])
    if not executed:
        improvement = "NOT_ASSESSABLE (benchmark did not complete in both arms)"
    elif c["reward"] > s["reward"]:
        improvement = "OBSERVED_IN_THIS_PAIR (documented action-changing intervention)" if intervention else "HIGHER_REWARD_WITHOUT_A_DOCUMENTED_INTERVENTION (not attributable to the collaboration)"
    elif c["reward"] == s["reward"]:
        improvement = "NONE_OBSERVED (equal official rewards)"
    else:
        improvement = "NONE_OBSERVED (COLLAB reward is lower)"
    res_s, res_c = s["resources"], c["resources"]
    unknowns = []
    for n, a in arms.items():
        r = a["resources"]
        if r["successful_without_usage"]:
            unknowns.append(f"{n}: {r['successful_without_usage']} successful dispatch(es) without recorded usage (tokens UNKNOWN)")
        if r["uncertain_failures_charged_at_reserve"]:
            unknowns.append(f"{n}: {r['uncertain_failures_charged_at_reserve']} failed dispatch(es) of uncertain outcome charged at the reserve, real usage unknown")
        if r["unknown_cash_exposure_dispatches"]:
            unknowns.append(f"{n}: {r['unknown_cash_exposure_dispatches']} dispatch(es) with unknown cash exposure")
        if r["dispatches_with_null_cost_usd"]:
            paid = sorted(k for k in r["cost_classes"] if k not in guard.ZERO_CASH)
            unknowns.append(f"{n}: cost_usd not reported on {r['dispatches_with_null_cost_usd']} dispatch(es); " + (f"route classes {sorted(r['cost_classes'])} are all zero-cash, so the exposure is bounded at 0.00" if not paid
                            else f"route class(es) {paid} are NOT zero-cash: the cash exposure is NOT bounded"))
        if r["agent_dispatches_with_unknown_lineage"]:
            unknowns.append(f"{n}: {r['agent_dispatches_with_unknown_lineage']} agent dispatch(es) with unknown lineage (independence not provable for them)")
    return {
        "pilot": budget.get("pilot"), "task": budget.get("task"), "controls": {"identical": identical, "checks": controls}, "arms": arms,
        "verdict": {"benchmark_executed_in_both_arms": executed, "independent_review_occurred": independent, "action_changing_intervention_documented": intervention,
                    "improvement_over_single": improvement,
                    "statistical_evidence": "NOT ESTABLISHED - one paired task (n=1); run-to-run variance of either arm is unmeasured; no effect size and no OGI claim"},
        "comparison": {"reward": {"single": s["reward"], "collab": c["reward"]}, "dispatches": {"single": res_s["dispatches"], "collab": res_c["dispatches"], "collab_minus_single": res_c["dispatches"] - res_s["dispatches"]},
                       "tokens_recorded": {"single": res_s["tokens_recorded"], "collab": res_c["tokens_recorded"], "collab_minus_single": res_c["tokens_recorded"] - res_s["tokens_recorded"]},
                       "wall_clock_s": {"single": s["wall_clock_s"], "collab": c["wall_clock_s"]}, "collaboration_calls": c["collaboration"]["collaboration_calls"],
                       "improving_reviews": sum(1 for r in reviews if r.get("improved")), "validated_unchanged_reviews": sum(1 for r in reviews if r.get("validated")),
                       "ungrounded_agreements": sum(1 for r in reviews if r.get("ungrounded_agreement")), "unresolved_objections": sum(len(r.get("unresolved") or []) for r in reviews)},
        "unknowns": unknowns, "caveats": caveats(arms, identical, reviews),
    }


def render(rep):
    v, cmp_ = rep["verdict"], rep["comparison"]
    L = [f"# {rep['pilot']}", "", "## Verdict (four separate questions)",
         f"1. Benchmark executed in both arms: **{v['benchmark_executed_in_both_arms']}**", f"2. Independent review occurred: **{v['independent_review_occurred']}**; action-changing intervention documented: **{v['action_changing_intervention_documented']}**",
         f"3. Improvement over SINGLE: **{v['improvement_over_single']}**", f"4. Statistical evidence: **{v['statistical_evidence']}**", "",
         f"## Controls identical across arms: **{rep['controls']['identical']}**"]
    L += [f"- {k}: " + ("OK" if x["equal"] else "MISMATCH/UNKNOWN") for k, x in rep["controls"]["checks"].items()]
    L += ["", "## Quality and resources", "| | SINGLE | COLLAB |", "|---|---|---|"]
    for key, label in (("reward", "official reward"), ("termination_reason", "termination"), ("wall_clock_s", "wall clock (s)")):
        L.append(f"| {label} | {rep['arms']['single'].get(key)} | {rep['arms']['collab'].get(key)} |")
    for key in ("dispatches", "agent_dispatches", "simulator_dispatches", "successful", "failed", "rejected_before_processing", "tokens_recorded", "tokens_charged_incl_uncertain_failures", "cash_usd_recorded"):
        L.append(f"| {key} | {rep['arms']['single']['resources'][key]} | {rep['arms']['collab']['resources'][key]} |")
    L.append(f"| entitlement use | {rep['arms']['single']['resources']['entitlement_use'] or 'none'} | {rep['arms']['collab']['resources']['entitlement_use'] or 'none'} |")
    L += ["", f"Collaboration overhead: {cmp_['dispatches']['collab_minus_single']:+d} dispatches, {cmp_['tokens_recorded']['collab_minus_single']:+d} recorded tokens, {cmp_['collaboration_calls']} collaboration calls; "
          f"improving reviews={cmp_['improving_reviews']}, validated-unchanged={cmp_['validated_unchanged_reviews']}, ungrounded agreements={cmp_['ungrounded_agreements']}, unresolved objections={cmp_['unresolved_objections']}.", "",
          "## Final actions"]
    for n in ARMS:
        L.append(f"- {n}: " + (", ".join(a["name"] for a in rep["arms"][n]["actions"]) or "(no tool call)") + f"; action checks: {rep['arms'][n]['action_checks']}")
    L += ["", "## Collaboration trace (COLLAB arm)"]
    for i, r in enumerate(rep["arms"]["collab"]["collaboration"]["reviews"], 1):
        L.append(f"### review {i}: purpose={r.get('purpose')} action={r.get('action')} improved={r.get('improved')} validated={r.get('validated')} final_reviewed={r.get('final_reviewed')} independent={r.get('independent_review')}")
        L += [f"- {t['stage']} by {t['model']} (lineage {t['lineage']}): {t['text'][:200]!r}" for t in (r.get("trail") or [])]
        L += [f"- UNRESOLVED: {u}" for u in (r.get("unresolved") or [])] + [f"- OVERRULED: {o}" for o in (r.get("overruled") or [])]
    if not rep["arms"]["collab"]["collaboration"]["reviews"]:
        L.append(f"(no collaboration review took place; skipped: {rep['arms']['collab']['collaboration']['skipped']})")
    L += ["", "## Unknown or unproven values"] + ([f"- {u}" for u in rep["unknowns"]] or ["- none recorded"])
    L += ["", "## Why this is a pilot and not evidence"] + [f"- {c}" for c in rep["caveats"]]
    return "\n".join(L) + "\n"


def main(argv):
    if len(argv) >= 5 and argv[1] == "mark":
        mark(argv[2], argv[3], argv[4], *(argv[5:7] + [None, None])[:2])
        return 0
    if len(argv) == 5 and argv[1] == "report":
        rep = build_report(argv[2], argv[3], argv[4])
        Path(argv[3], "report.json").write_text(json.dumps(rep, indent=1, default=str))
        md = render(rep)
        Path(argv[3], "report.md").write_text(md)
        print(md)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
