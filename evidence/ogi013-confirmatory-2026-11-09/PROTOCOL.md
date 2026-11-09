# OGI-013 confirmatory protocol — reconciled 2026-11-09 (PRE-LOCK)

**Status: PRE-LOCK.** No study call is permitted. The lock (§12) is produced only after the owner decisions in `STAGE_BUDGET.md` §0. Every observation from any earlier OGI study stays archived unchanged; nothing here re-labels it.

## 0. Provenance of this protocol
| source | status here |
|---|---|
| `evidence/ogi-study-package/PREREG_DRAFT.md` (package, 2026-11-07) | **inherited** for: §1 frozen inherited protocols, §6 analysis plan (exact McNemar, Holm, IUT, CP CIs, paired RD with Tango CI, labelled sensitivity views, all 2×2 tables), §7 stopping rule, §8 infrastructure classes C1–C5 and pause rule, §10 leakage, §11 claim boundary |
| `evidence/ogi-confirmatory-prereg-2026-11-07/PREREG_DRAFT.md` (draft, 2026-11-07) | **inherited** for: §3 arm definitions (S_m, R_mono, E_div, G_mas, T), §4 parity (tokens ±10 %, order, tools, prompt, uniform selector), §5 corrected/damaged metrics, §6 row-level identity rules incl. specialist, §7 hypothesis layers H1–H4, EVAL-002 three-arm design |
| this file | **resolves** the conflicts in §1 and adds the changes in §2. Every resolution is made before any confirmatory observation exists. |

## 1. Conflicts between the two drafts and their resolution
| topic | package | 11-07 draft | resolution (reason) |
|---|---|---|---|
| confirmatory families | D1 tau2 + D2 BCB | code + MATH; tau2 "later" | **F1 MATH-500 L5, F2 BigCodeBench-Hard.** tau2 and SWE-bench Verified are not confirmatory (§4). |
| T-row validity | ≥2 distinct lineages | exactly the declared roster | **11-07 rule** (strictly stronger; prevents partial-roster rows) |
| hypotheses | H1-S (IUT), H1-E | H1 T vs E_div primary, H2–H4 | **11-07 layers**; package H1-S is H2's IUT, package H1-E is H1 |
| sample size | fixed n (D2 = 200) | pilot OGI-STUDY-0 sets n | **fixed n = the whole eligible pool** per family, no pilot. The pools (134 / ≤148) cannot supply a disjoint pilot *and* a confirmatory draw; a pilot that sets n would also consume the only tasks. Power is stated in advance (§9). |
| T implementation | `fs_runtime.py` intended | `run_episode` (Brother Mode only) | **`run_team(research=peach_host(...))`**: the real `peachme.research.run_research` path (§3) |

## 2. Changes against both drafts (engineering made before lock)
1. T runs on the real PeachMe research path. PeachMe branch `fsi/ogi-research-injection` (101bb18): `ResearchPlan.wrap_work` (host metering wraps PeachMe's own WorkerPool), step tokens in every worker result, `ResearchPlan.appleme` switch, all investigations passed to `after`. FruitStack-Eval `fs_org_driver.peach_host` / `run_team(research=)`; tests `tests/test_fs_org_team_peach.py`.
2. `T-research_tree` cannot be expressed on that path (run_research is tree-bound). It is **exploratory only**, run on the mirrored path, and never enters a confirmatory family.
3. `T-plumme_selection` is not run: with a roster pinned at lock it is a relabel (11-07 draft §3), so it would test nothing.

## 3. Arms (per task, T first)
Roster: M = 3 solvers + 1 specialist, pairwise distinct `independence_key`, all with PlumMe status QUALIFIED for REASONING from stage S0 (`STAGE_BUDGET.md`), pinned at lock. If S0 qualifies fewer than 3 distinct lineages, the study does **not** start (multi-model claim impossible) and that is the reported outcome.
- **T**: `run_team(task, research=peach_host(svc, ...), roster, components=TEAM_COMPONENTS)` — Research Tree, LearningHook brief (EVAL-002 only; empty brief in EVAL-001 because the ledger is empty at lock), LSD Room, Brother Mode (blind parallel solve, cross-lineage challenge, revision, specialist), AppleMe diagnosis + `apply_advice` + prioritized re-investigation, finalize; executed visible checks before each challenge (code only; MATH has no visible check → `NO_VISIBLE_CHECK`).
- **S_1..S_M** (incl. specialist), **R_mono**, **E_div**, **G_mas**, **V** (plurality vote over E_div's drafts, the same selector minus the visible-check step): as in the 11-07 draft §3/§4.
- **Ablations (confirmatory family A):** T-appleme, T-lsd, T-executed_critique (F2 only). T-memory is part of EVAL-002 (memory/no-memory), not repeated here.
- **Activation precondition (fixed now):** an ablation is tested only if the component was active in ≥ 50 % of identity-valid T rows of that family: AppleMe = an `ADVICE_APPLIED` event with ≥1 action; LSD = `hypotheses ≥ 1`; executed critique = ≥1 `EXECUTED_CRITIQUE` event. Otherwise the ablation is reported as `COMPONENT_INACTIVE` with the activation rate and no test.

## 4. Domains
| family | dataset (pinned in `runners/ogi_tasks/datasets.json`) | grader | n | status |
|---|---|---|---|---|
| F1 | MATH-500 level 5, rev 6e4ed1a2 | math-verify 0.9.0 equivalence to the boxed key, after the episode | 134 (all) | confirmatory |
| F2 | BigCodeBench-Hard v0.1.4, rev 298d2cc7 | hidden tests (2/3 of methods, fixed split), official in-process semantics in bwrap + static tamper audit (owner D2), after the episode; the visible-check selector and executed critique use the same semantics | 130 ELIGIBLE (`runners/ogi_tasks/eligibility.json`) | confirmatory |
| tau2 airline/retail | — | official | — | **excluded**: run_team answers a single prompt; the interactive tool loop is not wired into T or the controls. Not substituted. |
| SWE-bench Verified | — | official harness | — | **excluded**: no harness, no per-instance container environment on this host. Not substituted. |
| PhysalisMe D5 / scientific claims | — | none validated | — | **excluded** from confirmatory; exploratory only |
| OGI-RH (PR #20) | — | Lean absent | — | separate exploratory track, no shared budget |

Licences: confirmed by the owner 2026-11-09 (D1, `OWNER_DECISIONS_2026-11-09.md`).

## 5. Hypotheses (confirmatory; α = 0.05 two-sided; exact McNemar; Holm within each listed family)
Per family F ∈ {F1, F2}:
- **H1 (primary): T vs E_div.**
- H2: T vs every S_m (IUT, each pairwise exact McNemar must reject in T's favour) and T vs R_mono.
- H3: E_div vs R_mono; R_mono vs best S_m (best = highest on the S0 dev set, fixed at lock).
- H4: G_mas vs E_div; T vs G_mas.
- Holm family per F: {H1, H2-IUT, H2-R_mono, H3a, H3b, H4a, H4b}. Family A per F: {T vs T-c for each active component}.
- **Two-family rule:** a claim beyond one family requires the same hypothesis rejected in the same direction in F1 and F2.
- EVAL-002 and EVAL-003: exactly as 11-07 draft §7 (EVAL-002: memory vs no-memory, memory vs sham, Holm over the two; <120 eligible pairs → descriptive. EVAL-003: r = 3 per member, U frozen before phase 2, fresh T, E_div, R_mono, V on U; |U| < 40 → `INSUFFICIENT_HARD_TASKS`; Holm over T vs E_div, T vs R_mono, T vs V).

## 6. Primary outcome, metrics, compute
Outcome: graded correctness of the selected answer, read only after the episode. Metrics, token parity (±10 %, `COMPUTE_MISMATCH` flagged and kept), corrected/damaged, tokens per solved task, tools, identity violations, selection errors: 11-07 draft §4–§5 unchanged. Efficiency is reported as accuracy and tokens per arm, never folded into the test.

## 7. Failures and validity
Package §8 (C1–C5, no hidden retries, pause at > 10 % infra share after 40 tasks, resume on the same lock, 30-day validity → `CLOSED_INFRASTRUCTURE_INFEASIBLE`) and §9 identity, tightened by the 11-07 §6 roster rule. Additional class: **C6 RESEARCH_HALTED** — `run_team` returns `infra_error` (unresolved step, no lease): an infrastructure failure, never a wrong answer. Primary view counts infra and identity failures as incorrect; sensitivity views (complete cases, worst case against T, COMPUTE_MISMATCH excluded) are labelled and never replace it.

## 8. Mechanism evidence (descriptive, every T row)
Recorded from the row: PeachMe events (`PEACHME:*`), receipts with lineage/tokens, LSD hypotheses, Brother Mode rows (first answers, challenges, revisions, specialist), AppleMe advisory and actions, Research Tree file (`research_tree.jsonl`, negative knowledge kept), memory retrieval/application. Every CORRECTED and DAMAGED task is listed with its row chain. No mechanism is credited for a row whose event is absent.

## 9. Power (stated, not adjusted later)
`evidence/ogi-study-package/power.py`, exact McNemar, α = 0.05, π = 0.75: n = 170 for p_d = 0.20, n = 120 for p_d = 0.30. F1 n = 134 gives ≈ 0.70 power and F2 n = 130 ≈ 0.68 at p_d 0.20. A non-rejection is reported as "not established", never as "no effect". No re-estimation, no interim efficacy look.

## 10. Leakage — package §10 unchanged. Grader material lives in `ogi_tasks` registries, never in `Task`; tested by the leak-guard tests of #18.

## 11. Analysis code — `analysis/ogi_analyze.py` (PR #17) and the rows adapter; hashed into the lock. The PhysalisMe independent recomputation of the 11-07 draft is dropped as unbuilt; instead the lock pins `analysis/ogi_analyze.py` and its 151-test suite.

## 12. Lock contents
`STUDY_LOCK.txt` = sha256 of: this file, `STAGE_BUDGET.md`, `runners/fs_org_driver.py`, `runners/ogi_tasks/*.py`, `runners/ogi_tasks/datasets.json`, `runners/ogi_tasks/eligibility.json`, `analysis/ogi_analyze.py`, CherryMe `brother.py` prompt templates, the task id lists per family, the S0 qualification report, the roster (model_key → independence_key, specialist, G_mas lead, R_mono pin); clean commits of FruitStack-Eval, CherryMe, PeachMe, PlumMe, AppleMe, OrangeMe, MangoMe; seed/salt. `MANIFEST_PRELOCK.sha256` in this directory is the pre-lock hash snapshot of the code as of this commit.

## 13. Pre-outcome clarification A1 (2026-11-09T08:57:50Z, written while S0 runs, before any S0 row was read)
Roster lineage rule. PlumMe's `independence_key` is version-level (`qwen3.8` and `qwen3.5` are distinct keys). The mandate requires genuinely different
model lineages, so roster members must differ in **vendor lineage** = the independence_key with trailing version digits/dots removed
(`qwen3.8`, `qwen3.5` → `qwen`). Among qualified candidates of the same vendor lineage only the one with the higher S0 accuracy is eligible
(ties: smaller sha256 of model_key). Roster order after that: S0 accuracy, descending; the first three are solvers, the fourth the specialist;
the R_mono pin and "best S_m" are the first solver; the G_mas lead is the first solver. This rule uses only S0 outcomes, never study outcomes.
