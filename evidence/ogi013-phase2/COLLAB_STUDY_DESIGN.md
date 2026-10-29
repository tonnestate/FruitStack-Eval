# OGI-013-COLLAB-1 — prospective, multi-task evaluation of the COLLAB mechanism (FROZEN design)

Status: **design frozen before any data exists** (`STUDY_LOCK.txt`, hashes of this file, `study_manifest.json`, the generator, the metrics module and the implementation files). It is **separate from, and replaces no condition of, the registered C3 study**
(different tasks, different conditions, its own lock). Not executed. A change after the lock is an amendment, dated and justified before the affected data exist.

## Question
Does adding independent critique/revision/re-review (`OGI013_ORG_COLLAB=1`, as run in PILOT-4: lineage-excluded reviewers, author-pinned revision, re-review by a not-yet-used lineage, agreement counts only with stated grounds) to the same FruitStack agent make its **decisions** better and its
**tasks** more often succeed, and at what cost? Not asked: whether more models are better, or whether the organisation learns (that is C3 / ORG-GATE/1; nothing here trains or enables a learned policy).

## Population and selection (mechanical; `make_study_manifest.py`, seed 4242; no earlier outcome is read)
- Official tau2 **train** splits only (C1/C2/C3 and all pilots use the test splits, so there is no overlap by construction; checked by a test).
- Write-opportunity stratum (40 tasks): airline train — **all 13** tasks with ≥1 expected write action (7, 11, 12, 14, 15, 17, 20, 21, 23, 33, 39, 40, 42); retail train — the first **27** of the 68 write tasks ordered by sha256("4242|retail|id").
- No-write control stratum (8 tasks): airline train tasks with zero expected writes, first 8 by sha256("4242|airline|id") (0, 1, 3, 4, 5, 41, 47, 49). COLLAB reviews only consequential writes, so this stratum measures unnecessary interventions and wasted effort.
- No task is chosen for having shown a benefit; PILOT-4's task 24 (test split) is excluded.

## Conditions (each task is one block; same pinned simulator model, same ledger snapshot, isolated state per arm)
SINGLE (control) · COLLAB (`OGI013_ORG_COLLAB=1`, mode rg2, `OGI013_ORG_POLICY_MODE=OFF`) · **SINGLE-E** equal-effort sampling (the registered C3 implementation) with k = ceil(median agent requests per COLLAB write-stratum episode), fixed after all COLLAB episodes are done and before the first SINGLE-E episode.
Arm order SINGLE/COLLAB per task by hash parity (`first_arm` in the manifest; 29 SINGLE-first, 19 COLLAB-first); SINGLE-E last. Supply: the **full eligible PlumMe supply**, budget-aware AUTO, cash USD 0.00 — no vendor shortlist. Per-episode caps: 110 provider requests, 200,000 tokens, 24,000 tokens per agent step (whole step incl. continuations), 90 minutes.
Replicates: 1 per task × condition. Infrastructure failures: as C3 (whole-block discard only for SIM_ROUTE_FAILED, ≤3 attempts, then INFRA_INCOMPLETE = non-success).

## Measures
**Decision quality (mechanical, `decision_metrics.py`, against the task's official reference actions):** per reviewed write — draft/final class (MATCH_EXPECTED, WRONG_ARGS, UNEXPECTED_WRITE, UNEXPECTED_TRANSFER, SAFE_NON_WRITE) and outcome (PREVENTED_WRITE_ERROR, ERROR_REPLACED_BY_DIFFERENT_ERROR, ERROR_NOT_FIXED, CORRECT_BLOCKED, VALIDATED_CORRECT, UNNECESSARY_CHANGE, NO_CHANGE_SAFE) — i.e. incorrect actions prevented, correct actions wrongly blocked, necessary corrections, unnecessary interventions;
per episode — unexpected writes and transfers executed (policy compliance), expected actions completed / expected (completion of the remaining objectives).
**Organisational performance:** official success; paired differences vs SINGLE and vs SINGLE-E; added provider requests, tokens, wall time (recorded usage; cash known/unknown); lineage and vendor of every request and review (independent lineages per review, share of reviews with a non-author vendor); reviewer failures (`review_unavailable`, rejected requests) and the outcome conditional on them; per-domain and per-stratum results.
Covariate: `premature_stop` (final user message carries the stop token while a confirmed write is pending) — recorded, never excluded, never repaired.

## Confirmatory endpoints (write-opportunity stratum, 40 pairs; exact two-sided McNemar on discordant pairs, **Holm over three**, α = 0.05; CI: Clopper-Pearson on the discordant proportion)
- E1: official success, COLLAB vs SINGLE.
- E2: official success, COLLAB vs SINGLE-E (improvement beyond equal-effort sampling).
- E3: harmful-action episode (≥1 unexpected write or unexpected transfer executed), COLLAB vs SINGLE (decision-quality endpoint; lower is better).
Everything else — the decision-outcome counts, cost differences, vendor/lineage analyses, no-write stratum, robustness, domain splits, premature-stop analysis — is **exploratory/descriptive** and is reported as such with no p-values presented as confirmatory.

## Interpretation rules (fixed now)
- Power is limited: with 40 pairs only a large, one-sided pattern is detectable (e.g. ≥6 discordant pairs all in one direction gives exact p ≈ 0.031 before Holm). Baseline success on these domains with free-tier models can be low (C1: 3/20), so few discordant pairs are plausible; **an inconclusive result is a valid, reportable outcome**. No extension, no re-selection, no post-hoc tasks.
- One study ≠ organisational intelligence: a significant E1/E2 would show that this review workflow helped on this task population; learning/adaptation claims require C3 / ORG-GATE/1. A caution recorded from PILOT-4: stated grounds ≠ correctness; E3 and the decision outcomes exist to catch review that replaces one error by another.
- Model-family and vendor diversity are recorded for every review as evidence and analysed descriptively; the workforce is not restricted.

## Not decided here / required before the first episode
A multi-task launcher and campaign-level guard generalising the PILOT launcher (new files only), the evaluator for E1–E3 (hash-frozen before launch), and an owner authorization covering `RESOURCE_PLAN.md` (R3). The implementation files that define COLLAB are hashed in `STUDY_LOCK.txt`; a launch on different bytes is an amendment.
