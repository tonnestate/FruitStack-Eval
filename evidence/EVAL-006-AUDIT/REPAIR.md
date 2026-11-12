# EVAL-006 audit, part 2: research-to-decision repair (2026-11-13)

EVAL-006 (`evidence/EVAL-006/`) and the forensic audit (`AUDIT.md`) are unchanged. This repair ran no benchmark and no model inference, used no reserved task and deployed nothing.
Commit SHAs are listed in section 9.

## 1. Root causes corrected (audit R1, R2, R5, R6, R7, plus the PlumMe forensics)
| # | cause (evidence) | correction (component) |
|---|---|---|
| R5 | only the root Brother result reached the decision: `verify_candidate(brother)` and FSE's `brother_summary(brother)`. AppleMe-driven investigations were discarded | `peachme.research.Consolidation`: every distinct SOLUTION / REVISION / repair of EVERY investigation becomes a CherryMe candidate node with provenance. CherryMe's own unchanged evidence ranking (`ResearchTree._leading`, frozen CAI/1 V14) picks the answer. `run_mission` returns ONE `record['decision']` (PEACH-DECISION/1). FSE's `brother_summary` is deleted |
| R5b | the executed check ran AFTER AppleMe, so the diagnosis never saw refuted answers. AppleMe had no rule for "every held answer refuted"; the tree bridge dropped the answer of candidate evidence | candidates are verified before the diagnosis (PeachMe). The bridge maps candidate evidence to its answer (CherryMe `appleme_bridge`). New detector `HELD_ANSWERS_REFUTED` -> OPEN_ALTERNATIVE_BRANCH (AppleMe) |
| R5c | LSD hypotheses never reached the root solvers | the root investigation's brief carries every hypothesis, labelled UNVERIFIED (PeachMe) |
| R7 | no executed signal for code; critique and revision ungrounded (0/11 revisions changed a grade) | `ResearchPlan.check_author` writes a task-derived executed check through the governed pool (PeachMe). `runners/code_checks.py`: tests are written from the task statement only, validated against a NotImplementedError stub (vacuous tests dropped, non-loading tests -> no check), and run in FSE's official bwrap sandbox. Critics and revisers get the execution report (`Consolidation.feedback_work`; critiques become `executed` level). A repair loop continues while each repair is a NEW candidate that scores strictly better: no count limit, progress bounds it. `run_mission(answer_check=)` verifies a decision that skipped research |
| R1 | FSE removed CherryMe's triage and forced FALSIFY (inquiry 39% of the tokens) | `fs_runtime` builds the engine exactly like Aurora (`triage="auto"`, default orchestrator) |
| R2 | unconditional research + LSD; fixed 60k-token worker ceilings | the research-activation rule moved from Aurora to `peachme.research.research_decision`. Aurora and FSE both call it. Budgets default to no ceiling (accounted, no cash). `config/fs_runtime/adaptive.toml` has no fixed plan |
| R6a | Brother asked ONE replacement for a missing second solver: two zero-cost refusals = NO_SECOND_SOLVER (13/20) | a solver slot is replenished while each refusal-before-processing names a NEW worker. Such refusals do not count as unproductive failures (CherryMe `brother`). The PeachMe pool does not charge them against the replacement allowance and reports the refusing worker's identity |
| R6b | PREFERRED substitution served two solvers the same lineage (1015, 374) | a pinned re-lease excludes every other live worker's lineage (PeachMe) |
| R6c | CherryMe re-staffed a denied CHECK onto a worker that had failed, or onto the ANSWER lineage (57 LOCAL_DENIED; 38/40 inquiries INSUFFICIENT_INDEPENDENT_REVIEW) | a re-staff alternative must have no failure in this run and a lineage no other responsibility of the question uses (CherryMe `engine`) |
| R6d | PlumMe ranked PROVISIONAL like UNKNOWN | competence tiers 0 QUALIFIED, 1 PROVISIONAL, 2 UNKNOWN, 3 WITHDRAWN (PlumMe) |
| R6e | estimate = chars/3. The headless route bills ~17.7k input (14.5k cached harness context); 79/201 output caps were cut | PlumMe adds each route's observed input overhead to the output-cap and room computation (not to the reservation check). PeachMe reserves `out + max(4000, observed input of that worker)` |
| acc | "253 calls" mixed dispatches and refusals | `eval006._accounting` splits executed_ok / executed_unusable / attempted_no_inference / local_denials. The research record carries `pool.opened / refused_before_inference / retired` |

## 2. Verified decision behaviour (deterministic, real components, no model)
- PeachMe `tests/test_research_decision_e2e.py` (real PlumMe scheduler with a scripted adapter, MangoMe, CherryMe tree / LSD / Brother, AppleMe, PeachMe pool):
  - A: the root converges on a refuted answer. AppleMe raises HELD_ANSWERS_REFUTED, CherryMe investigates the LSD hypothesis, and that later branch's executed-supported answer is selected (provenance APPLEME_ADVICE). The two refusing routes are tried once each, accounted as `refused_before_inference = 2`, and the root still gets two solvers.
  - B: a verified solution is revised into a wrong one and both final positions agree on it. The verified earlier candidate stays (revision REGRESSED).
  - C: nothing is supported. The execution report reaches a repair whose output is verified and selected (EXECUTION_REPAIR, SUPPORTED).
  - D: the activation rule. Settled or single-worker triage -> no research; CHALLENGE -> LSD; VERIFY -> no LSD; no ceilings.
- PeachMe `test_research_verifier.py`: executed evidence beats agreement; without a check the earliest investigation's Brother basis holds (UNVERIFIED); all refuted -> REFUTED; a failing verifier is never evidence.
- FSE `test_fs_runtime.py`: an adaptive simple task skips research (CLAIMS_SETTLED_BY_INQUIRY), and its synthesized answer is verified by the same check. One qualified lineage starts the mission (single solver); none = SUPPLY_UNAVAILABLE.
- FSE `test_code_checks.py`: generated tests are validated (vacuous dropped), and syntax/import failure is reported. The recorded EVAL-006 ORG candidate for BigCodeBench/129 fails a test written from its task statement ("raises ConnectionError") - the signal the organization lacked.
- Aurora `test_aurora_decision_contract.py`: Aurora's activation is PeachMe's rule; its synthesis and result come from `record['decision']`.
- EVAL-006 replay (`runners/eval006_replay.py` -> `/root/fruits/research/EVAL-006-AUDIT/replay_decision.json`): every recorded research tree through the repaired Consolidation.
  - Without a check, 20/20 decisions are identical to what EVAL-006 graded: no behaviour change without evidence.
  - With the official grader as a diagnostic oracle check, 8/20 are verified. That is the ceiling of what the organization produced; no later branch held a better answer.

## 3. Executable verification capabilities
Execute candidate code in isolation (bwrap, official in-process semantics, pinned grader interpreter); detect load / syntax / import / timeout failures; task-derived tests
(statement only, validated on a stub); per-test report into critique, revision and repair; revision vs predecessor (`decision.revisions`: IMPROVED / REGRESSED /
UNCHANGED / IDENTICAL / UNVERIFIED); epistemic label VERIFIED / UNVERIFIED / REFUTED plus `unresolved` (e.g. CHECK_IS_TASK_DERIVED_NOT_COMPLETE). Generated checks never feed
PlumMe competence (only HOST_VERIFIER does). Hidden benchmark tests are never available to the organization.

## 4. Remaining, scientifically unproven
- Whether task-derived tests are correct often enough to help. A wrong generated test can refute a correct candidate; the decision then falls back to the best-scoring refuted candidate, labelled REFUTED.
- Whether hypotheses in the brief, executed critique and repair raise accuracy on hard tasks. All mechanisms are shown to RUN and to be USED; no effect is measured.
- Free supply: there is still no QUALIFIED non-gpt REASONING lineage. Independence improves only when supply exists; catalogs still list dead models (MODEL_NOT_FOUND quarantined 6h).
- The headless route's 14.5k harness overhead is real billed (INCLUDED) input. It is now planned for, not removed.
- MODEL_NOT_FOUND durable until rediscovery, `earliest_retry_at` on PlumMe failure receipts and cross-mission unavailability in CherryMe: not done (FUTURE_WORK).

## 5. Readiness conditions for a future independently evaluated experiment
1. Owner approval of the release set below (merge order PlumMe -> CherryMe -> AppleMe -> PeachMe -> FSE -> Aurora). Re-freeze nothing; CherryMe's V14 freeze is intact.
2. Pre-registration before any run: `config/fs_runtime/adaptive.toml` unchanged (never `research = "required"`), the primary metric unchanged (full-suite pass@1 + tamper audit), and new non-reserved tasks or the same 20 with that disclosure. The 110 reserved tasks stay sealed until the confirmatory run.
3. Secondary metrics pre-declared: decision basis / epistemic, executed-check kind, revision outcomes, repairs, research activation reasons, the accounting split.
4. Supply recorded before the run (`workforce_supply`), with the honest expectation of a gpt-dominated workforce. Effects must be attributed to organization only against a SINGLE arm with the same check-and-repair loop (otherwise check-and-repair is confounded with collaboration).
5. Owner decisions already given stand: no stronger paid model for now; production activation is not justified by any evaluation result.

## 9. Changed repositories and commits (all branches pushed, `[skip ci]`; nothing merged or deployed)
| repo | branch | commit | base |
|---|---|---|---|
| PlumMe | cc/selection-recovery | b82dc4d | live 0af278d |
| CherryMe | cc/decision-contract | febf41c | 4abffc6 |
| AppleMe | cc/refuted-held-answers | 05767c8 | aca5f8b |
| PeachMe | cc/research-decision-contract | 0fdb93a | 56764bf |
| FruitStack-Eval | cc/adaptive-decision-repair | 6a724da (+ this report) | da66b95 |
| Aurora | cc/decision-contract | adafbc6 | 96067de |

Tests: PlumMe 989 passed / 24 skipped; CherryMe 818 / 35 skipped (frozen venv, V14 freeze intact); AppleMe green; PeachMe 394 / 1 skipped;
FSE 831 passed, 53 failed - the same 53 fail on the clean baseline (da66b95 with the base components: grader-adversarial sandbox tests, fs_org_team);
Aurora integration 79 passed, 10 failed - the same 10 fail on the clean baseline 96067de.
