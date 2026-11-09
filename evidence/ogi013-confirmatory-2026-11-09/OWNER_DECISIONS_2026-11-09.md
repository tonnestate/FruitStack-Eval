# Owner decisions 2026-11-09 (answers given in the Claude Code session, recorded verbatim)

| id | question (short) | owner answer (verbatim option) |
|---|---|---|
| D2 | BigCodeBench-Hard grader for the lock | "Official semantics (Recommended)" |
| D3 | push + merge the OGI PRs in STAGE_BUDGET §3 order, no deploy | "Push + merge all" |
| D4 | subscription headless routes gpt-6-luna / claude-haiku-5-5 in the roster | "Both allowed" |
| D1+D5 | S0 budget (≤ 360 calls, ≤ 1.1 M tokens, USD 0) and dataset licences (BCB-Hard Apache-2.0, MATH-500 MIT, inferred) | "Approve S0 + licences" |

Execution record:
- D3: merged PlumMe main fast-forward to the canonical local main (f41c772, contains #25); CherryMe #14, #15; PeachMe #37 (#36 closed), #38; FruitStack-Eval #14, #15, #16, #19, #21, #18, #17 (retargeted to main), #20, #23. No deploy, no restart.
  PeachMe #39 (a defect found afterwards: pinned calls reached the wrong worker) is pushed but NOT merged; the auto-mode permission check refused a self-merge outside the approved list. Owner merge required.
- D2: official semantics implemented (`runners/ogi_tasks/code.py::run_tests_official`, `tamper_audit`); eligibility re-derived in the pinned grader venv: **130 / 148 ELIGIBLE** (`eligibility.json`; the boundary manifest is kept as `eligibility_boundary.json`, 16 / 148).
- D1: licences confirmed by the owner for this study; `datasets.json` keeps the inferred-licence evidence.
- D5: S0 is bound to `STAGE_BUDGET.md` and `PROTOCOL.md` at the sha256 recorded in `S0_START.sha256`, written immediately before the first S0 call.
