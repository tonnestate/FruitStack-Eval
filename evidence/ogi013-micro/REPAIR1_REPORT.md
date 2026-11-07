# REPAIR ORDER 1: replay acceptance report (no model episode started)

Commits: FruitStack-Eval `f1ac19a` (+ this report), PlumMe `1aa4fab` (branch `ogi013-org-plum`), MangoMe pinned source `835d8be` (unchanged).

## Results
- Full existing + new suites with real MongoDB: **535 passed, 1 skipped, 2 failed**. The 2 failures (`test_ogi013_collab1_campaign::test_a_multi_task_campaign...`, `test_ogi013_decision_metrics::test_the_collab_study_lock_matches_the_frozen_files`) also fail on a clean worktree of `19bb3c5`; they are not caused by this change.
- New repair tests `tests/test_ogi013_repair1.py` (R1-R6, R8) and `tests/test_ogi013_replay_acceptance.py` (R7): 24 passed. PlumMe `tests/test_ogi013_small_model_eligibility.py`: passed (33 PlumMe eligibility/market tests).
- Replay (stored micro-pilot T records, new logic, driver-run visible checks, no model calls):
  - duration-1: grounded objections = {} after the approval-is-not-an-objection rule (O4 is a suggestion and never enters a revision prompt); S3_rev1 and S3_rev2 `REJECTED_REVISION`; selected output `S3:first` (hidden grade 2/2, resolved).
  - intervals-1: all revisions `REJECTED_REVISION` (`NO_VERIFIED_IMPROVEMENT`); selected output `S1:first` (2/2).
  - lru-1: selected output `S1:first` (3/3).
- Retry analysis of duration-1 T: `RETRY_ANALYSIS.md`.
- MangoMe restart-restore (C.4) still passes; MangoMe checkpoint writes per test: scripted episode + MCP read-back 18, restart test 11 (before the kill), two-episode test 1 + 1. Stack MangoMe use in the replay: none (no stack).

## Interpretations to confirm before Part 4 (also in `PREREG.md`, REPAIR-1)
1. A revision is adopted only for a verified improvement (higher driver-run score, or a claimed reproduction that flips fail -> pass): stricter than "score >= incumbent".
2. Candidate check suite = visible tests + recorded reproductions of grounded objections.
3. Roster pins at first use through AUTO; replacement after 2 consecutive failed steps.
4. Arm N call counts come from T's measured critique/revise calls.
5. Small-model exclusion applies to AUTHOR steps only.

## Untested
A full `main()` episode with real models (static check + import only); the roster pinning against the live PlumMe supply; arm N end to end.
