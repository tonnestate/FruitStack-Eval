# F1-DEV vs F3-DEV (development run, NOT the registered confirmatory experiment)
Date 2026-10-14 02:35 UTC. Registered G2/F2/F3 workflow untouched (failed qualification attempt `../20261014T001500Z-DEV-PILOT`, independence blockers TOO_FEW_QUALIFIED_GROUPS / NO_INDEPENDENT_SET_OF_REQUIRED_SIZE).
Manifest: tasks/dev/pilot_inquiry_tasks_DRAFT.jsonl (50 tasks, no owner-approved references). `--skip-supply-gate`, FREE_ONLY, per-request cost gate active.
F1-DEV control offer: offer_fc7ca07fd8b8b98b659d7857 — most correct answers on G2 calibration tasks (7/8), chosen before any dev result; does NOT satisfy the registered F1 rule.
## Results (pilot/estimates.json, descriptive only)
- F1-DEV: 32/50 success (0.64), 9 no answer (4 HARNESS_PinnedWorkerUnavailable, 4 SEMANTIC_OUTPUT_FAILURE, 1 RATE_LIMITED), 6 unstructured; mean utility 0.65; wall 302 s total (6.0 s/task); cost 0 EUR (FREE_ONLY; cost_usd unreported, null mapped to 0.0 only for the analyzer, see graded_costnum.jsonl).
- F3-DEV: 0/50. Every task INCOMPLETE (cause SUPPLY): CherryMe stopped at `NO_COMPATIBLE_PROVIDER` (require_grounding, capability SCIENCE) and `NO_ELIGIBLE_INDEPENDENT_WORKERS`; 0 provider calls. The runner recorded these as COMPLETED/UNKNOWN (runner predates CherryMe 0.3.4 terminal outcome); read as INCOMPLETE. This measures missing grounded supply, not F3 quality.
- F3-F1: success rate -0.64 [-0.78, -0.48]; utility -0.65 [-0.79, -0.49] (cluster bootstrap by subfamily). Not a statement about FruitStack: F3 never ran its chain.
## Component participation (runtime evidence)
PlumMe (pinned + AUTO decisions logged), CherryMe 0.3.4 engine, AppleMe assurance (events present) executed. CogC/PomeloMe/PeachMe: no runtime evidence in this run; fse stack install check only. Partial chain, not full FruitStack.
## Limitations
Draft tasks/no approved references; control offer not by registered rule; n=50 single run; F3 arm void for supply reasons; Arm A missing; logcheck G5 blocker NO_EXECUTED_OUTCOMES on F3 state; costaudit F1 passed (46 choices, no violations).
