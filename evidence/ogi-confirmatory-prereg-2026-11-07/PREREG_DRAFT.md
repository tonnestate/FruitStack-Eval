# OGI confirmatory preregistration — DRAFT 2026-11-07

**Status: DRAFT. Not locked, not authorized, no budget released.** Nothing in this file permits a model or provider call. A study runs only after (1) the lock described in §12 exists and (2) the owner has authorized the budget separately (§11).

- Supersedes nothing. The historical conditions stay archived and unchanged: COLLAB-1 (`evidence/ogi013-phase2/STUDY_LOCK.txt`, `evidence/ogi013-collab1/AMENDMENT_LOCK.txt`) and the earlier draft package `evidence/ogi-study-package/`. This draft reuses the package's statistics, infrastructure-failure classes C1–C5, stopping rule and leak guards by reference, and changes only what is listed here.
- Basis: owner objective `feedback_ogi_research_objective_2026-11-07` (shared memory) and the design audit `/root/contracts/OGI-STUDY-DESIGN-AUDIT-2026-11-07.md` (D1–D8).
- Code: `runners/fs_org_driver.py` on branch `fsi/ogi-study-controls`. Offline tests only: `tests/test_fs_org_driver.py`.
- There is no hash manifest. Nothing in this directory is hashed into any lock yet.

## 1. Question
Does FruitStack's **organization** add capability beyond what the same models produce alone? Organization here means independent solutions, adversarial critique, evidence-based revision, verification, model selection and verified memory. The gain must hold beyond model diversity, extra compute (tokens), repeated sampling, voting, tool access and chance.

## 2. Prior work (precedent, not evidence about FruitStack)
- Anthropic, "How we built our multi-agent research system", 2025-06-13, https://www.anthropic.com/research/multi-agent-research-system. It reports that a lead agent (Claude Opus 4) with Sonnet 4 subagents beat single-agent Opus 4 by 90.2% on an internal research eval. It also reports that token usage alone explained about 80% of the performance variance on BrowseComp.
  Consequence for this study: an apparent organizational gain may be a token effect. Compute matching is therefore on **tokens** (§4).
- Owner-cited and **not independently verified here**:
  - https://code.claude.com/docs/en/agent-teams
  - https://www.anthropic.com/research/multiagent-systems (2026-08-13)
- Internal precedent: in S1, 12 of 16 "multi-model" episodes were Luna twice, and the controller changed answers by registration order. That defect motivates the identity and selector rules in §4 and §6.

## 3. Arms
M = 3 members with pairwise distinct `independence_key` values, pinned at lock. With fewer than 3 qualified lineages, M = 2 is used and the reduction is reported.

| arm | definition | runner (offline-tested) |
|---|---|---|
| S_1..S_M | each member alone, one draft (with the shared tool loop, §4) | `run_samples(arm="S", roster={m: lineage}, cycle=[m], k=1)` |
| R_mono | one pinned member (the best on a *disjoint* dev set, chosen at lock), repeated independent drafts at T's token budget, uniform selector | `run_samples(arm="R_mono", roster={pin: lineage}, cycle=[pin], k, token_budget)` |
| E_div | the same model mix as T: independent drafts round-robin over the members, at T's token budget, with no critique, exchange or revision, and the uniform selector (**diversity-only control**) | `run_samples(arm="E_div", roster=T's roster, cycle=list(roster), k, token_budget)` |
| G_multi | **generic multi-agent control**: a lead/orchestrator plus parallel workers and central synthesis, with the same model mix, tokens and tools. It has no FruitStack mechanisms: no Brother Mode adversarial critique or evidence-based revision, no AppleMe, Research Tree, LSD room or persistent memory. Uniform selector over the synthesized candidates | **not built** (follow-up; required before G_multi hypotheses are locked) |
| T | the organized team: CherryMe Brother Mode, blind parallel first answers, cross-lineage critique backed by executed checks, revision, uniform selector | `run_episode(arm="T", roster=...)` |
| EVAL-002 arms | memory / no-memory / sham-brief (§7) | `run_pair` (memory and no-memory); sham-brief is a follow-up |

Ablations (component attribution, one mechanism per study; full factorial is unaffordable on free supply):
- **T−exec**: critique without executed evidence. Tests whether evidence-based critique matters, or only persuasion. Planned first.
- **T−PlumMe**: fixed roster vs PlumMe AUTO selection. This is meaningful only if AUTO is active in T. While the roster is pinned at lock it is a relabel and is not run.
- **AppleMe, LSD room, Research Tree, memory on/off**: planned follow-ups. They are ablated only after a T arm that actually uses them (the `fs_runtime.py` full stack) has run on real tasks.

## 4. Parity rules (all arms)
- **Tokens.** Compute matching uses input+output tokens taken from PlumMe receipts. Every row logs `tokens` (`fs_org_driver.tokens`). Each control's token budget is T's receipted total on the same task, and drafts are drawn until it is reached (cap 3k calls). If any receipt lacks a token count, the call count k of T is used instead and the row is flagged. Rows outside ±10% of T's tokens are kept, flagged COMPUTE_MISMATCH, and removed only in a labelled sensitivity analysis.
- **Order.** T runs first on every task. The control budgets are derived from T's receipts and are never tuned on outcomes.
- **Tools.** Every arm gets the same tools and executed checks: the visible tests or checker, the sandbox and the same per-call `max_output_tokens`. An arm that cannot use a tool another arm used makes the comparison tool-confounded. That row pair is flagged TOOL_MISMATCH and handled like COMPUTE_MISMATCH.
- **Prompt.** All controls use T's solve prompt (`cherryme.brother.SOLVE`, empty brief).
- **Selector (identical for every arm; `fs_org_driver.select_answer`).** The selector works over the arm's final candidate set, in this order:
  1. the highest score on the task's **visible** checks, when the domain has them (never the hidden grader);
  2. then the plurality of parsed answers;
  3. then the smallest `sha256(task_ref \0 answer)`.
  This rule does not depend on order, model or registration, so the first-solver retention used before is gone. T's old "primary retained" answer is reported only as the descriptive field `primary_retained`.

## 5. Metrics
- **Primary outcome:** the selected answer is correct under the domain's independent grader, read after the episode (§8).
- **Corrected and damage** (`fs_org_driver.grade_after`). "Correct" means grade == 1.0, graded after the episode only, for every member's first answer and for the final answer:
  - CORRECTED: no first answer was correct and the final answer is correct (wrong → right).
  - DAMAGED: at least one first answer was correct and the final answer is wrong (right → wrong). For E_div and R_mono this means a correct draft was not selected, which is the baseline harm rate.
  - HELD: at least one first answer correct and the final correct. UNSOLVED: neither.
  - Member level: `corrected_members` counts members whose first answer was wrong and whose own final position is right. `damaged_members` counts members whose first answer was right and whose final position is wrong.
  - Harm hypothesis (secondary, T only): DAMAGED/(DAMAGED+CORRECTED) < 0.5, exact one-sided binomial.
- **Efficiency:** tokens and calls per arm and per resolved task. Accuracy vs tokens is plotted per arm.

## 6. Row validity (identity)
Validity is enforced in code, not only recorded. `fs_org_driver.identity_check` runs on the executed receipts of every row:
- The successful solve calls must realize **exactly** the declared distinct lineages. A declared multi-model row that ran on one lineage is `INFRA_IDENTITY:SINGLE_LINEAGE_ROW`.
- A call from outside the roster is `LINEAGE_OUTSIDE_ROSTER`.
- For E_div and R_mono, the i-th call must be on the planned member, otherwise `PLAN_MISMATCH`.
- A receipt without a lineage is `RECEIPT_WITHOUT_LINEAGE`.
- Study arms cannot run without a declared roster.

`split_valid` excludes invalid rows and keeps them with their reason. Those rows count as infrastructure failures under the package's §8 rule (C1–C5, pause above 10%).

Note: Brother Mode's specialist tie-break asks a lineage that none of the solvers used. With a roster of M = solver count, that call falls outside the roster and the row is excluded. At lock, either the specialist lineage is a declared roster member for every arm, or the specialist step is disabled through `control`.

## 7. Hypotheses
Each family uses exact two-sided conditional McNemar with Holm, the intersection-union test for "beats every member", and the two-family rule, as in `evidence/ogi-study-package/PREREG_DRAFT.md` §6.

**EVAL-001 (organizational gain). Four layers, each separated by one contrast:**
- **H1 (primary): T vs E_div at matched tokens**, the organizational effect over diversity.
- H2: T vs best single member. T must beat the **best** S_m at matched tokens, through the intersection-union test over all S_m and against R_mono, not the average member. This is the "better individual model" explanation.
- H3 (secondary): E_div vs R_mono (diversity effect). R_mono vs best S_m (compute / repeated-sampling effect).
- H4 (after G_multi exists): G_multi vs E_div (generic multi-agent organization) and T vs G_multi (FruitStack-specific mechanisms).
- Secondary analysis: a logistic model of correctness on arm plus log(tokens), or the accuracy-vs-tokens curves, as a token-covariate check of H1.

**EVAL-002 (organizational learning).** Seeding is done by A's discovery, verified by an executed check:
- `capture_brother` now passes the executed ground. Verification by a *different* lineage or by a grader on another seed task is the stronger rule and is preferred at lock.
- Three arms per transfer task:
  - **memory**: the verified brief is applied.
  - **no-memory**: no brief.
  - **sham-brief**: a verified but non-applicable discovery of equal length.
- **Arm order per task is randomized** by sha256(task_ref, lock salt).
- Eligibility is locked before any transfer run. If fewer than 120 pairs are eligible, the study stops with a report.
- Hypotheses: memory > no-memory, and memory > sham.

**EVAL-003 (emergent capability).** U is the set of tasks on which every member fails all r = 3 solo attempts. Then T, E_div and R_mono (plus V) run fresh on U. The emergent count gets a Clopper-Pearson CI. If |U| < 40, the outcome is INSUFFICIENT_HARD_TASKS. Sampling, voting and chance are controlled by R_mono and E_div on U.

## 8. Domains and independent verification
The grader is read only after the episode. Hidden tests, keys and expected states never enter a prompt, brief or capture (package §10).

| family | dataset (candidates; license and contamination checked at lock) | independent verifier | status |
|---|---|---|---|
| Code debugging | HumanEvalFix (HumanEvalPack), DebugBench, or BigCodeBench with seeded bugs | hidden tests executed in the sandbox. A **visible/hidden split is fixed at lock**; only the visible tests feed the selector and tools | confirmatory |
| Code generation | BigCodeBench-Hard | same | confirmatory |
| Math | MATH-500 level 5 | math-verify (symbolic equivalence) | confirmatory, never the whole verdict |
| Agentic tool use | tau2 airline/retail | official tau2 grader | later stage |
| Science hypotheses / multi-step research | D5 (PhysalisMe-generated data with known ground truth) | a planned grader: the hypothesis is checked against the known generating process | **exploratory** until the grader exists and is validated |
| Architecture | — | none exists. A blinded external rubric with ≥2 raters and agreement reported would be required | **out of scope** for every confirmatory claim (no independent verifier) |
| Cross-session problems | EVAL-002 transfer set | as per domain | via EVAL-002 |

## 9. Statistics, power and pilot
- The tests are those of the package's §6. The analysis script and an independent recomputation in **PhysalisMe** are both hashed into the lock (audit D8). Neither exists yet.
- Power: `evidence/ogi-study-package/power.py` gives n = n_for(p_d, π = 0.75, α, 0.8) for exact McNemar. p_d is **not assumed**: it is measured by the pilot.
- **Pilot OGI-STUDY-0** (descriptive, no confirmatory claim):
  - Tasks: 40 code-debugging/BigCodeBench-Hard and 40 MATH-500 L5 items, disjoint from every OGI-013 task and from the later confirmatory draw.
  - Arms: S_1..3, R_mono, E_div, T (all under §4).
  - Outputs:
    - p_d for T vs E_div per family;
    - infrastructure share by arm;
    - identity-valid rate;
    - the corrected/damage table;
    - tokens per resolved task.
  - Decision rule, fixed now: confirmatory n = n_for(p_d observed). If n > 400 per family, or the infrastructure share is above 10%, the result is "not feasible on current free supply" and the work stops without widening the scope.

## 10. Leakage
Package §10 applies unchanged:
- Grader output is written only to result rows, and `grade_after` runs only after the episode.
- `capture` and `brief` never receive a key or a grade.
- Briefs hold only discoveries verified by an executed check or an official grader on another task.

## 11. Budget (separate owner authorization)
No budget is released by this draft. Rough pilot estimate from the audit: about 2,650 requests and 18M tokens, capped at 1.5×, USD 0, free/local/trial routes only. Dropping R_mono saves about 700 requests. The owner authorizes the budget separately, after reviewing the lock.

## 12. Lock (not produced)
Before the first call, the lock fixes:
- task id lists and their hashes;
- dataset revisions and licenses;
- the visible/hidden split;
- the roster with each member's `independence_key`;
- the R_mono pin and its dev-set evidence;
- the prompt template sha256;
- the `fs_org_driver.py` sha256 and the analysis + PhysalisMe script hashes;
- the EVAL-002 order salt;
- this file's sha256.

The lock follows the approval-by-hash rule and the DIRTY_SOURCE refusal.

## 13. Open prerequisites (not built in this change)
- G_multi runner;
- the sham-brief arm and randomized EVAL-002 order in `run_pair`;
- the T−exec switch;
- dataset adapters and the visible/hidden split;
- the analysis script and the PhysalisMe cross-check;
- the D5 grader;
- a cross-lineage verifier for EVAL-002 discoveries.
