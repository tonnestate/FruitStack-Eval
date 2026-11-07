# OGI study package: preregistration DRAFT for EVAL-001, EVAL-002 and EVAL-003

Status: **DRAFT, not locked, not authorized.** Written 2026-11-07 offline, with no provider call and no experiment. The study must not start without an explicit owner authorization of `budget.md` (section 0). The frozen protocols below are referenced and remain unchanged.

Package files: `task_domains.md` (domains, datasets, licenses, graders), `arms.json` (arms and compute matching), `budget.md` (calls, tokens, caps, authorization), `runner_config.template.json` (wiring to `runners/fs_org_driver.py` and the intended entrypoint `runners/fs_runtime.py`), `power.py` (sample-size table in section 5), and `route_classes.py` with its output `route_classes.json` (offline PlumMe cost-class count).

## 0. Authorization
No call of any arm, no pilot and no dataset download for study items is permitted until the owner signs an approval file containing the sha256 of the locked `budget.md` and `runner_config.json`, as with COLLAB-1. An approval covers exactly one stage of `budget.md`. Any edit after approval invalidates it.

## 1. Inherited frozen protocols (read, unchanged)
- `evidence/ogi013-lead/PREREG.md`: claim boundary (task performance only, never "intelligence"); the two-family rule; N token matching within +-10%; circuit breakers.
- `evidence/ogi013-lead/OGI013_QA1_PREREG.md` and `OGI013_QA2D_PREREG.md`: arm definitions T, E, S and L; exact McNemar with Holm; INFRA_FAILED counted as incorrect; no hidden retries; the pause rule.
- `evidence/ogi013-small-proof/PREREG.md`: Clopper-Pearson reporting; worst-case sensitivity for infrastructure failures.
- `evidence/ogi013-qa2d-v2-closure/QA2D_V2_CLOSURE_REPORT.md`: infrastructure-failure reconciliation (section 8 below), the CLOSED_INFRASTRUCTURE_INFEASIBLE outcome, labelled sensitivity views, and the disagreement-rate planning estimate.
- `evidence/ogi013-research-status/OGI013_RESEARCH_STATUS.md`: the structural limit of multiple choice (no executable objection), which is why every domain here has an executable or official grader; the learning-ledger lifecycle and leak guards (section G).

## 2. Questions and hypotheses
**EVAL-001: organizational gain.** On tasks graded independently of every model, does the organized team T resolve more tasks than (a) each roster member alone (S per member, with L = Luna alone) and (b) the same members at equal compute without organization (E)?
- H1-S (per family): T vs every single arm. This is an intersection-union test: reject only if every pairwise exact McNemar (T vs S_m, for every m) rejects at level alpha with more T-only than comparator-only tasks. The IUT holds level alpha without adjustment.
- H1-E (per family): T vs E, exact McNemar.
- Family: {H1-S, H1-E}, Holm at alpha = 0.05 two-sided, applied separately in D1 (tau2) and D2 (BigCodeBench). A claim beyond one family requires the same hypothesis to be rejected in the same direction in both D1 and D2 (`PREREG.md` two-family rule).

**EVAL-002: verified knowledge transfer.** Does showing discoveries that were independently verified on OTHER tasks (applied arm) raise the success rate over the identical episode without them (control arm)?
- H2: applied vs control on eligible D2 transfer tasks, exact McNemar, alpha = 0.05 two-sided. Eligibility is decided before the pair runs: the task is eligible when `Ledger.retrievable(task_ref, run, task_text)` is non-empty at pair start (a read-only call, so no RETRIEVAL is recorded). It is therefore pre-treatment.
- Transfer is claimed only if H2 rejects with more applied-only than control-only successes AND at least one applied-only task has a complete ledger chain DISCOVERY -> VERIFICATION (`executed` or `official_grader`, from a different task) -> RETRIEVAL -> APPLICATION -> OUTCOME (`runners/ogi013_org_discoveries.py`).

**EVAL-003: tasks no single member solves.** Are there tasks the team solves that no member solves alone, beyond what extra compute (E) and majority voting (V) achieve?
- Phase 1 (before any T run): each member makes r = 3 independent attempts on every D2-hard task. U is the set of tasks where all M x r attempts fail (union oracle: an upper bound on what any selection over member samples could reach).
- Phase 2 on U only: T, E (fresh, compute-matched) and V (vote over E's drafts). Fresh E on U measures regression to the mean: tasks selected by phase-1 failure can be solved by chance in a new sample.
- H3-E: T vs E on U; H3-V: T vs V on U. Exact McNemar, Holm over the two, alpha = 0.05.
- Reported with every result: emergent count = tasks in U solved by T while E and V both failed, with a Clopper-Pearson 95% CI over |U|. A count without a rejected H3-E is reported as "not separated from sampling variance".

## 3. Arms
As in `arms.json`. T runs first on every task, and E's budget is derived from T's receipts. S_luna and L coincide whenever Luna is a roster member.

## 4. Primary outcomes
- Binary task success from the domain grader (`task_domains.md`): D1 tau2 reward = 1; D2 all hidden tests pass; D4 math-verify equivalent. An unparsable final answer counts as failure.
- An infrastructure-failed or identity-invalid arm-row counts as failure in the primary view (sections 8 and 9).
- Secondary (descriptive, outside the families): tokens and calls per arm and per resolved task; corrected, degraded and unchanged primary answers; objection counts by evidence level; COMPUTE_MISMATCH share; for EVAL-002, retrieval and application counts and the eligibility share.

## 5. Sample size
Planning inputs, from archived data only:
- Disagreement: QA-2D v2 T first answers differed on 4/40 = 10.0% [2.8, 23.7], and SL vs SN on 6/42 = 14.3% [5.4, 28.5]. These come from multiple choice. Executable-task disagreement is unknown and is assumed to be 20%; this assumption is stated, not measured.
- Effect: QA-2D complete cases T vs SL 4 T-only : 2 SL-only (pi = 0.67); T vs SN 0 : 2 (pi = 0); research-status net 3 corrections : 2 harmful concessions (pi = 0.60). The observed multiple-choice effect is too small to power at any affordable n (pi = 0.60 needs n of 1,030 or more at p_d = 0.20).
- Design effect of interest: pi = 0.75 (three T-only for every comparator-only discordant task), with p_d = 0.20.

Exact McNemar, two-sided, power 0.80 (`python power.py`; n rounded up to a multiple of 10):

| alpha | p_d | pi = 0.60 | 0.67 | 0.75 | 0.80 |
|---|---|---|---|---|---|
| 0.05 | 0.10 | 2050 | 720 | 340 | 240 |
| 0.05 | 0.143 | 1430 | 510 | 240 | 170 |
| 0.05 | 0.20 | 1030 | 360 | 170 | 120 |
| 0.05 | 0.30 | 690 | 240 | 120 | 80 |
| 0.025 | 0.10 | 2460 | 860 | 400 | 280 |
| 0.025 | 0.143 | 1720 | 600 | 280 | 190 |
| 0.025 | 0.20 | 1230 | 430 | 200 | 140 |
| 0.025 | 0.30 | 820 | 290 | 140 | 90 |

Fixed sample sizes:
- EVAL-001 D2: n = 200 tasks, which gives power 0.80 at Holm's first step (alpha 0.025) for p_d 0.20 and pi 0.75.
- EVAL-001 D1: all tau2 airline and retail test tasks, about 164 (counted at lock), one episode per arm. This gives about 0.79 power at alpha 0.05 and less at 0.025. The shortfall is stated in advance, and a non-rejection in D1 is reported as "not established", never as "no effect".
- EVAL-001 D4 (secondary, descriptive): all MATH-500 level-5 items, budgeted at 150.
- EVAL-002: 200 D2 transfer tasks. Power applies to the eligible subset. If fewer than 120 tasks are eligible (power 0.63 or less at p_d 0.2, pi 0.75, alpha 0.05), EVAL-002 is reported as descriptive only. Eligibility is known before any transfer episode runs.
- EVAL-003: pool = all D2-hard tasks (148 at the time of writing; counted at lock). If |U| < 40, H3 is not tested and EVAL-003 is reported as INSUFFICIENT_HARD_TASKS. This is fixed now, before phase 1. On U, discordance should be high because E rarely succeeds there. At |U| = 40, power is 0.82 for p_d 0.5 and pi 0.85, but only 0.36 for p_d 0.3 and pi 0.8 (alpha 0.025).

No sample-size re-estimation, no interim efficacy look and no continuation beyond the fixed n.

## 6. Analysis plan (exact; `analyze.py` is written and hashed into the lock before the first call)
- Pairwise tests: exact two-sided conditional McNemar (binomial test of b against b + c with pi0 = 0.5), as in QA-2D.
- Effect estimates: the conditional odds ratio b/c with an exact Clopper-Pearson 95% CI for b/(b+c), transformed; the paired risk difference (b - c)/n with the Tango score 95% CI. Marginal success rates use Clopper-Pearson 95% CIs.
- Multiplicity: IUT inside H1-S, Holm over each listed family, and nothing else confirmatory. Every other number is descriptive and carries no p-value.
- Sensitivity, labelled and never replacing the primary result: (i) complete cases, where all compared arm-rows are infrastructure-OK; (ii) worst case, where infrastructure failures count against T only (as in S1); (iii) COMPUTE_MISMATCH rows excluded.
- Report every 2x2 table (both, A only, B only, neither) for every pair, as in the QA-2D closure report.

## 7. Stopping rule
Each stage runs to its fixed n or stops for one of these reasons:
1. A campaign cap of `budget.md` is reached: halt with exit 3, and the stage is reported as BUDGET_STOP with the data so far marked descriptive.
2. The pause rule (section 8): pause with exit 76, then resume on the same lock.
3. An owner stop.

Nothing is stopped or extended because of observed outcomes. A circuit breaker hit twice in one stage stops that stage and is reported as a defect (`PREREG.md`).

## 8. Infrastructure failures (as in the QA-2D v2 closure)
- An arm-row is INFRA_FAILED when any of its calls fails without a model decision. The causes, reconciled row by row with the gateway extract: C1 no provider call (429, no capacity); C2 refusal during cooldown after an upstream timeout; C3 call made but output unusable (for example REASONING_LEAKED_AS_CONTENT at the length cap); C4 INFRA_MANGOME_FAILED; C5 INFRA_IDENTITY (section 9).
- There are no hidden retries and no reruns. A row interrupted by a subscription or provider limit message is discarded and re-run once, as QA-2D allowed. PlumMe cooldown scheduling (one wait for a short retry window of 300 s or less) is not a retry.
- Pause when any arm's infrastructure-failure share exceeds 10% after 40 tasks of the current process. Resume on the same lock without re-running finished rows. If the stage cannot resume within the lock's validity (30 days), close it as CLOSED_INFRASTRUCTURE_INFEASIBLE: no confirmatory test, descriptive tables only, and the verbatim conclusion form of the QA-2D closure.
- Exposure asymmetry is disclosed: T and E need several successful calls per task, while S and L need one or a few. The cause-by-arm table and the per-process table are always reported.

## 9. Identity verification (PlumMe receipts)
Every provider call has a PlumMe receipt with `canonical_model_id`, `independence_key`, `cost_class` and `offer_id`. Receipt ids are stored in the result rows, and the receipt-window id hash goes into the closing manifest.
- A T row is valid only if its SOLUTION rows carry at least 2 distinct `independence_key` values. This prevents the S1 defect, where 12 of 16 episodes were "Luna twice".
- An S_m row is valid only if every receipt matches the pinned `canonical_model_id`. An E row is valid only if its receipt identities are a subset of T's roster for that task. An L row requires the subscription-route receipt.
- Any mismatch, or a receipt without identity, makes the row INFRA_IDENTITY: fail-closed and counted as an infrastructure failure, consistent with `INFRA_INCOMPLETE` in the research status.

## 10. No answer-key leakage
- Hidden tests, keys and expected DB states live outside every workspace and prompt and are read only by the grader after the episode. The study prompt template sha256 goes into the lock.
- The learning brief contains only discoveries VERIFIED by `executed` or `official_grader` on another task. `dataset_key` (post-hoc) verifications, own-task items, ASSERTED, FALSIFIED and same-run items are never shown (`LearningHook`; `tests/test_ogi013_learning_hook.py`).
- Grader results go into result rows only. `capture` never receives a key or a grade.
- Committed files contain ids and hashes, never task texts.

## 11. Claim boundary (inherited, verbatim in substance)
Allowed statements have the form: "On <domain> (<dataset>, n = <n>, <date>), T resolved x% vs y% (S_m) and z% (E); paired differences with CI and Holm-adjusted p." No sentence says that the organization "is intelligent", "helps" or "adds value" beyond the rejected hypotheses, and there is no ranking wording. A model's claim to be right is never evidence.

## 12. Lock (to be produced before the first study call; nothing is locked by this draft)
`STUDY_LOCK.txt` records: the id lists and their sha256 per domain and position range; dataset file hashes, revisions and fetched license texts; prompt template sha256; sha256 of this file (as locked), `arms.json`, `budget.md`, `runner_config.json` and `analyze.py`; component commits (CherryMe, PlumMe, PeachMe, MangoMe, FruitStack-Eval), all clean (DIRTY_SOURCE refuses); the roster with its `independence_key` values; and the PlumMe supply snapshot hash.

## 13. Limitations of this draft
- p_d = 0.20 for executable tasks is an assumption, not a measurement. If the true discordance is near 10%, D2 (n = 200) has power below 0.5 at pi 0.75.
- D1 is constrained to about 164 tasks by the dataset size.
- EVAL-002 eligibility depends on the term-overlap retrieval (`retrievable`, min_overlap 0.34), which is crude (research status M2). Low eligibility makes EVAL-002 descriptive.
- `official_grader` verification of a tau2 discovery certifies the episode outcome, not the general rule. That is why D1 is secondary for EVAL-002.
- `analyze.py`, the BigCodeBench, MATH and tau2 adapters for `fs_runtime.py`, and the D5 grader do not exist yet. They are prerequisites before lock, not part of this package.
- There is no sham-brief control (an irrelevant verified brief of equal length), so EVAL-002 cannot separate "more context" from "relevant knowledge". Adding one needs a driver change and is not proposed here.
