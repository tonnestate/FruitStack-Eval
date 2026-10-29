#!/usr/bin/env python3
"""Writes the VALIDATION-1 manifest and budget from the frozen COLLAB-1 budget (per-episode ceilings copied UNCHANGED; only the number of episodes and the cumulative totals shrink) and the cohort
chosen by select_tasks.py. Conditions: FIXED (one pinned ChatGPT-headless model), SINGLE-E (equal-resource, non-organised, PlumMe AUTO supply), COLLAB (FruitStack organisation, PlumMe AUTO)."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
C1 = HERE.parent / "ogi013-collab1"
cohort = json.loads((HERE / "cohort.json").read_text())["cohort"]
v2 = json.loads((C1 / "study_manifest_v2.json").read_text())
orders = [["FIXED", "SINGLE-E", "COLLAB"], ["SINGLE-E", "COLLAB", "FIXED"], ["COLLAB", "FIXED", "SINGLE-E"]]      # cyclic Latin square over the three cohort tasks
tasks = [{**next(t for t in v2["tasks"] if t["task_ref"] == ref), "stratum": "validation-mechanism-sensitive", "order": orders[i]} for i, ref in enumerate(cohort)]
manifest = {"study": "OGI-013-VALIDATION-1", "seed": v2["seed"], "selection_rule": "evidence/ogi013-validation1/select_tasks.py (outcome-independent, fixed before any episode)", "n_tasks": 3,
            "n_write_opportunity": 3, "conditions": ["FIXED", "SINGLE-E", "COLLAB"], "tasks": tasks, "version": 1, "amends": "none (separate prospective cohort; COLLAB-1, C1, C2, C3 untouched)",
            "single_e": v2["single_e"], "fixed_model": "gpt-6-luna",
            "fixed_model_note": "Owner preference Terra 6.0 is NOT executable with this ChatGPT login ('The gpt-6-terra model is not supported when using Codex with a ChatGPT account', verified 2026-10-29); the permitted alternative Luna 6.0 (codex model gpt-6-luna) is verified."}
mp = HERE / "study_manifest.json"
mp.write_text(json.dumps(manifest, indent=1))
b = json.loads((C1 / "collab1_budget.json").read_text())
n = len(tasks) * 3
cap = b["default_arm_cap"]
b.update({"study": "OGI-013-VALIDATION-1 (small prospective cohort: FIXED single model vs equal-resource control vs FruitStack organisation)", "status": "AUTHORISED by the owner's written order of 2026-10-29 (max 3 tasks, zero cash, existing ceilings); executable only with an approval file for exactly this file",
          "manifest": "evidence/ogi013-validation1/study_manifest.json", "manifest_sha256": hashlib.sha256(mp.read_bytes()).hexdigest(), "episodes_planned": n,
          "cumulative": {"max_dispatches": n * cap["max_dispatches"], "max_tokens": n * cap["max_tokens"], "max_cash_usd": 0.0, "max_wall_minutes": n * b["max_episode_minutes"]},
          "request_breakdown": {"base_ceiling": f"{n} episodes x {cap['max_dispatches']} requests; {n} x {cap['max_tokens']} tokens", "note": "per-episode ceilings identical to COLLAB-1"}})
(HERE / "validation1_budget.json").write_text(json.dumps(b, indent=1))
print(n, "episodes;", b["cumulative"], [t["task_ref"] + ":" + ">".join(t["order"]) for t in tasks])
