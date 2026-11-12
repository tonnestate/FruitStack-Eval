# EVAL-006 forensic audit (amendment, 2026-11-12/13)

EVAL-006 (`evidence/EVAL-006/`, raw data `/root/fruits/research/EVAL-006/`) is unchanged. This audit adds no model call, no new task and does
not touch the 110 reserved tasks. Every number below is recomputed from the recorded artifacts.

Files: `contributions_graded.jsonl` (every Brother Mode SOLUTION/CRITIQUE/REVISION with its full receipt text, graded offline by
`runners/eval006_audit.py` with the same grader, interpreter and frozen sources as `evidence/EVAL-006/run.sh`); `accounting_reconciliation.txt`.

## 1. System under test (`runners/fs_runtime.py` `mission()`, config `config/fs_runtime/operational_20261112.toml`)

| mechanism | EVAL-006 ORG arm | adaptive Aurora runtime (`integration/aurora_peach_runtime.py`) |
|---|---|---|
| research activation | unconditional `ResearchPlan` for every task | `research_decision()` after the inquiry: skip / LSD / verify by CherryMe triage |
| CherryMe triage | removed from the frame (`fs_runtime.py:370`) | active |
| orchestrator | forced `Falsify` for every claim (`:374-379`) | CherryMe default |
| LSD Room | always on | only on triage CHALLENGE |
| budgets | fixed: worker 12 calls / 60k tokens, run = 3 x worker | no token ceiling, no cash (`NO_CASH_BUDGET`) |
| executed verification | none (`verifier=None`, no task `check`; PhysalisMe analyses removed) | none for reasoning missions |
| competence | frozen live copy, per-arm state | live PlumMe |
| model-input egress | identity (`authorize_model_input=lambda text, view: text`) | BlueberryMe `protect_text` |
| graded candidate | `brother_summary(brother)`: ROOT investigation only, consensus else first (primary) position | synthesis over findings |

EVAL-006 therefore measured a fixed, non-adaptive configuration of the components, not the adaptive FruitStack.

## 2. Candidate selection and grading
- Recomputed grade of the graded candidate equals the original grade on all 40 task-arms (0 mismatches).
- Oracle bound: across ALL 46 graded ORG codes (35 solutions, 11 revisions, every node, both investigations) exactly the same 8 tasks have any
  passing code. No better selector over the recorded outputs could reach more than 8/20; the selection rule cost nothing here.
- 5 missions ran a second, advice-driven investigation on an LSD hypothesis node; `brother_summary` ignores it. No such code passed.
- ORG and SINGLE both answered with gpt-6-luna in every graded candidate. ORG wins 445, SINGLE wins 654: two samples of the same model.
- The 2 "hidden-pass / all-fail" cases are genuine candidate defects; grader correct:
  - BigCodeBench/1015 `test_empty_table`: empty DataFrame `.to_sql` -> `sqlite3.OperationalError near ")"` (reproduced).
  - BigCodeBench/129 `test_invalid_url`: re-raises `requests.ConnectionError`, not the builtin `ConnectionError` the task specifies
    (`issubclass(requests.ConnectionError, ConnectionError) is False`).
  - The secondary hidden-only grade (ORG 10/20 vs 8/20) counts them only because FSE's visible/hidden split put the discriminating test in
    "visible". It must not be read as an ORG advantage.

## 3. Resource reconciliation (ORG arm; SINGLE: 20 receipts, 20 ok, 345,150 tokens, gpt-6-luna only, 175 s model / 233 s wall)
253 dispatch receipts = 220 executed with usable output + 6 executed, unusable output (SEMANTIC_OUTPUT_FAILURE, 15.9k tokens) + 27 attempts
without inference (rate limit, MODEL_NOT_FOUND, credential exhausted, forbidden, paywall, provider unavailable). The 90 failure receipts are a
separate stream with no dispatch (57 LOCAL_DENIED, 16 MODEL_ERROR, 8 RATE_LIMITED, 4 QUOTA, 4 PROVIDER_DOWN, 1 BUDGET); never double counted.

| stage | receipts | ok | tokens | share | can reach graded candidate |
|---|---|---|---|---|---|
| CherryMe inquiry (forced FALSIFY) | 82 | 80 | 1,404,927 | 39.1% | no |
| LSD Room hypotheses | 80 | 80 | 1,399,018 | 39.0% | only via advice investigations (5/20), which selection ignores |
| Brother SOLUTION | 35 | 35 | 447,901 | 12.5% | yes |
| Brother REVISION | 11 | 11 | 169,082 | 4.7% | yes |
| Brother CRITIQUE | 14 | 14 | 152,830 | 4.3% | via revision |
| unlinked failed attempts | 31 | 0 | 16,156 | 0.5% | no |

gpt-6-luna: 201 receipts, 3,547,039 of 3,589,914 tokens (98.8%). Every gpt-6-luna call bills ~17.7k input tokens (SINGLE: 17.3k/call) while
FruitStack prompts to other models are 2.5-3k: the 10.4x token ratio is an 11x executed-call ratio times a provider-fixed per-call overhead
(cost class INCLUDED, $0). Summed model latency ORG 2,720 s vs 175 s; wall 3,049 s vs 233 s.
"253 calls" is correct as a count of dispatch receipts but not of model executions (220 + 6). Fixed in `runners/eval006.py _accounting`
(additive fields `executed_ok`, `executed_unusable`, `attempted_no_inference`, `local_denials`; verified 220/6/27/57 on the frozen state).

## 4. Collaboration effect (offline grading of every recorded contribution; secondary diagnostics, not the primary metric)
- 7/20 missions had two solvers. Initial solutions: 8/35 pass (all gpt-6-luna; second-lineage solutions 0/10 pass: llama 8b, qwen2.5-vl,
  qwen3.5, nemotron).
- Critiques: 14; 12 report issues, 2 say "ISSUES: NONE" on failing code (720, 916). 0 critiques were run against an executed test.
- Revisions: 11. 0 fixed a failing solution; 1 kept a passing one passing (777); 0 broke a passing solution; hidden-test counts unchanged in
  every pair (e.g. 1015 4/4 -> 4/4, 374 2/4 -> 2/4, 574 3/4 -> 3/4).
- Advice-driven second investigations (5): 0 passing codes; 777's reached 1/4 vs the root's 4/4.
- Result: criticism and revision neither improved nor degraded any solution; without an executed signal the critic had no ground truth and
  the reviser (same gpt model) reproduced its code.

## 5. Missing capabilities: supply vs runtime
| finding | cause class | evidence |
|---|---|---|
| 13 NO_SECOND_SOLVER | SUPPLY + POLICY | every mission retires the first gpt worker WORKER_BUDGET_EXHAUSTED after LSD (4 calls x 17.7k > 60k); the second lineage then fails on supply (MODEL_NOT_FOUND 8, RATE_LIMITED 7, SEMANTIC 6, CREDENTIAL 4, PROVIDER 4, FORBIDDEN 1) until the fixed run budget (3 x 60k) leaves no room for another lease |
| 22 WORKER_BUDGET_EXHAUSTED retirements ("budget failures") | CONFIGURATION | token ceilings sized for ~3k-token prompts against a supplier billing 17.7k/call; Aurora has no token ceiling |
| no executed verification / no feedback | HARNESS + CAPABILITY | `verifier=None`, tests withheld by the prereg, PhysalisMe analyses removed; no worker can run code; so no competence outcome either |
| no cross-task knowledge | CONFIGURATION | one isolated mission per task; nothing verified, so nothing to store |
| 78% of tokens without a path to the answer | HARNESS / DECOMPOSITION | forced FALSIFY inquiry + unconditional LSD; adaptive runtime gates both |
| weak second models | SUPPLY + SELECTION | PlumMe offered competence-UNKNOWN free models; dead catalog entries (MODEL_NOT_FOUND, CREDENTIAL_EXHAUSTED, PAYWALL) are selected before failing |
| no collaboration gain | CAPABILITY | homogeneous effective workforce (one strong lineage) + no executed signal: section 4 |

## 6. Root-cause matrix
| # | code path | cause | consequence | numeric change | correction | status |
|---|---|---|---|---|---|---|
| R1 | `fs_runtime.py:370-379` | triage removed, FALSIFY forced | inquiry spend without effect on answer | 82 receipts, 39.1% tokens | test the adaptive path (`aurora_peach_runtime.research_decision`) in any future eval | OPEN (eval harness; no run authorised) |
| R2 | `operational_20261112.toml` `lsd=true`, fixed budgets | unconditional LSD; token ceilings vs 17.7k/call supplier | LSD spend; worker retirement; second solver starved | 80 receipts, 39.0%; 22 retirements | adaptive LSD + no token ceiling (already Aurora's behaviour) | OPEN (eval config) |
| R3 | `eval006.py _accounting` | receipts counted as "calls" | 253 overstated executions | 253 -> 220 ok + 6 unusable + 27 no inference | split fields added | FIXED |
| R4 | ANALYSIS secondary metric | hidden-only grade depends on FSE split | 10/20 vs 8/20 suggests an ORG gain | none valid | section 2 caveat | DOCUMENTED |
| R5 | `fs_runtime.brother_summary` | selects root investigation only | advice investigations discarded | 0 tasks here (oracle = 8) | select over `investigations` once a verifier exists | OPEN (no gain demonstrable without verifier) |
| R6 | PlumMe selection over free catalog | dead/unknown models leased | 27 no-inference attempts, 13 single-solver missions | see section 5 | catalog health refresh + competence-qualified second lineage | OPEN (needs live supply work) |
| R7 | organisation for code tasks | no executed signal | critique/revision inert | 0/11 revisions changed a grade | executed self-check (PhysalisMe / sandbox) inside the mission | OPEN (capability) |

## 7. Answers
1. No. A fixed configuration with triage removed, FALSIFY forced, LSD always on, fixed token budgets, no verifier and identity egress.
2. Yes. Grades reproduce exactly; the selector could not have done better (oracle 8/20); the two all-fail cases are real defects.
3. No: 220 executions with usable output + 6 executions with unusable output; 27 receipts are attempts without inference.
4. Partly. The tokens are real billed input, but an estimated ~85% of each gpt-6-luna call is provider-fixed overhead (the same prompts bill 2.5-3k tokens on other models), 78% of ORG tokens went to stages
   with no path to the graded answer, and the ratio is fundamentally 11x executed calls.
5. Neither: 0 of 11 revisions changed a grade, 0 fixes, 0 regressions; 2 of 14 critiques missed real failures.
6. Triage, adaptive research activation, adaptive budgets, executed verification, competence feedback, PhysalisMe analyses, cross-task
   knowledge, BlueberryMe egress; advice investigations were run but excluded from selection.
7. Supply: second-lineage failures and weak free models (MODEL_NOT_FOUND, rate limits, credentials, semantic failures). Runtime/config:
   budget retirements, forced inquiry, unconditional LSD, no verifier, root-only selection.
8. Yes, for the exact tested configuration: 8/20 vs 8/20, McNemar p = 1.0, at ~10x tokens and ~13x wall time. It says nothing about the
   adaptive runtime, and with one effective lineage it could not separate organisation from re-sampling the same model.
9. That this fixed configuration on free supply, without executed checks, adds cost and no measurable accuracy on 20 BigCodeBench-Hard tasks;
   that its components run end to end; that its accounting reconciles. Not established: any effect (positive or negative) of the adaptive
   organisation, of collaboration with a competent second lineage, or of executed verification.
10. Repaired: R3 (accounting split), R4 documented. Remaining: R1, R2, R5-R7 (section 6). Per owner decision no stronger model and no new
    benchmark now; production activation is not justified by this evaluation.
