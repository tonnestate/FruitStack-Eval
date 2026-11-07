# e2e_offline_2026-11-07_v3 — OFFLINE / SCRIPTED WORKERS

**Label:** offline fixture with scripted workers. The provider texts behind PlumMe are scripted (fixed answer per task, identical in applied and control runs) through
PlumMe's public `ProviderAdapter` interface. Every other component runs its real code path. This is evidence that the integrated path executes and records what it did.
It is **not a live result** and **not scientific evidence** of model capability or organizational gain.

Command: `python runners/fs_runtime.py --config config/fs_runtime/offline_fixture.toml OUT` (mode offline-fixture), exit code 0.

Component commits: FruitStack-Eval `fsi/acceptance` (this change on top of eed0717); PeachMe `fsi/acceptance` 25d0e3b (ResearchPlan.verifier, unchanged here);
CherryMe 11675ee; PlumMe ccee075; AppleMe aca5f8b; OrangeMe c0beb27; MangoMe f9fcb63 (in-memory backend); PhysalisMe 448a3b1 (synthetic dataset).

## What changed against v2

v2: every mission ended UNRESOLVED. `peachme.mission.run_mission` decides the state (mission.py:140-142) from CherryMe's claim statuses and the responsibility
consolidation. The claim only receives evidence from the investigator (the fixture investigator answers UNKNOWN with no evidence, so ANSWER = NO_DELIVERABLE and
CHECK = BLOCKED) or from CherryMe deterministic tools, and `fs_runtime` registered none (`responsibility_runtime(tools=())`). The host's executed check was offered only
to the Research Tree (`ResearchPlan.verifier`), whose evidence never reaches a claim.

v3: the task's executed check is also registered as a CherryMe deterministic tool (`fs_runtime.ExecutedCheckTool`). It applies only to a claim naming exactly one
runnable candidate, executes it and hands CherryMe one grounded PASS/CONTRADICT item (source_ref = the executed check's evidence id). CherryMe's own evidence gate
settles the claim (zero provider calls for the inquiry). The scripted investigator is unchanged: a model statement still settles nothing.

## Result

| mission | state | mission_success | claim | research verifier |
|---|---|---|---|---|
| A | COMPLETED | true | SUPPORTED (EXEC-97fca40870b5cc70) | math.isqrt SUPPORTS, node SUPPORTED |
| B | COMPLETED | true | SUPPORTED (EXEC-a61be837bbeb5517) | math.comb SUPPORTS, node SUPPORTED |
| B-control | COMPLETED | true | SUPPORTED (EXEC-a61be837bbeb5517) | math.comb SUPPORTS, node SUPPORTED |

- integration_path_ok: true for all three (all stages, MangoMe checkpoint, 1 PhysalisMe tool receipt and 8 research steps each, executed verifier ran).
- The claim's evidence id equals the Research Tree verification's evidence id (same check, same candidate).
- Learning ledger (7 rows): DISCOVERY + VERIFICATION (executed) for A's `math.isqrt` → RETRIEVAL + APPLICATION in B → DISCOVERY + VERIFICATION for B's `math.comb`
  → OUTCOME B vs B-control: reward 1.0 vs 1.0 → `NO_EFFECT_OBSERVED`; `math.comb` is `STORED_NOT_REUSED`. The ledger `task` field now holds the host task id (`B`),
  not the mission id. The equal rewards are expected: the scripted answers are identical in both arms.

Not shown here (covered by `tests/test_fs_runtime.py`): a claim naming a candidate the check contradicts becomes REFUTED (run_mission COMPLETED, mission_success false);
a task without a check and the UNKNOWN investigator stays UNRESOLVED.

Files: `summary.json`, `stdout.json`, `learning.jsonl` (hash-chained ledger), `mission_<tag>.json`, `research_tree_<tag>.jsonl`, `tool_receipts_<tag>.jsonl`.
