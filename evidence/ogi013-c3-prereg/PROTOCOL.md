# OGI-013 c3 - controlled organisation study: SINGLE / FIXED / ADAPTIVE-RG2 (+ learner, + ablations)  [PRE-REGISTRATION, written 2026-10-27, no c3 data exists]
Status: Pre-registration must be sealed BEFORE the first c3 exploratory task: supervisor/prereg writes PREREG_LOCK.txt with the committed protocol revision, protocol SHA-256, and fixed task-split SHA-256. Phase A then explores only under these locked hypotheses, outcomes, split and exclusions. After Phase A, FREEZE.txt records the learner verdict, SINGLE-E k and repository revisions BEFORE confirmatory Phase B. After the pre-registration lock: hypotheses, outcome rules, task splits and tests are immutable; any deviations must be reported. After FREEZE: trained-arm decisions and k are also immutable.
c1 and c2 remain separate historical evidence (their conditions: FIXED vs ADAPTIVE-write-gated, free-only/trial-off supply,
mis-fed sensor in c1) and are not relabelled as RG/2.

## Hypotheses (Tonn-AGI / AOR operationalised; each is falsifiable here and a negative result is a valid result)
H1 organisation beats its constituents: RG2-OFF > SINGLE on unseen tasks.
H1c organisation beats mere extra sampling: RG2-OFF > SINGLE-E (equal-effort single model: same AUTO pool, k independent drafts per decision, majority canonical action, no critique/verification/cooperation; k = integer median provider dispatches per decision observed in phase A, fixed and recorded at the start of phase B, env OGI013_SINGLE_E_K).
H2 adaptive beats fixed organisation: RG2-OFF > FIXED (always-on peer review, existing ADAPTIVE-v1 write-gated rule is NOT a comparator here: it was shown to be a static rule).
H3 persistence/cross-task transfer: RG2-OFF with the arm's shared organisational state (knowledge store, claim/inquiry state) > RG2-OFF-NOPERSIST (fresh state per task), same task order.
H4 learning: RG2-LEARNED > RG2-OFF on held-out tasks - testable ONLY if the learner passes ORG-GATE/1 (evidence/ogi013-learning/ORG_GATE_V1.json) and the owner authorises the learner-on arm; else H4 is reported "not testable: gate not met".
H5 mechanism ablations (descriptive, not confirmatory): RG2-OFF vs {no triage, no verification, no knowledge store}. Recovery is not ablatable without an engine change and is reported descriptively
   from traces (SWITCH_WORKER events and what followed).

## Stack and supply (identical for every condition)
FSE ogi013-org-bridge, CherryMe ogi013-org-cherry, PlumMe ogi013-org-plum, PeachMe ogi013-org-peach, AppleMe/MangoMe/OrangeMe/PomeloMe as installed; commit hashes recorded in FREEZE.txt.
PlumMe budget-aware AUTO over ALL eligible authorized supply (no FREE_ONLY, no trial-credit exclusion, no zero-charge gate); cash is spent only within an owner-approved budget (none assumed:
without it, billed routes are refused and credit/free/included capacity is used). Per-response limits are negotiated by PlumMe. The user simulator is pinned to ONE PlumMe-chosen model per task
for ALL conditions of that task (same tau2 simulator model; pair/block discarded and rerun, max 3, on simulator-route failure only, logged).
Constituent pool control: AUTO drifts. Conditions of one task run as a BLOCK back-to-back in a seeded random order; every receipt (provider, model, cost class, tokens, entitlement/cash
dimension) is exported; per-condition model-family mix is reported and a pre-registered sensitivity analysis repeats each primary test on blocks whose conditions share >= 50% of
successful-receipt model families (Jaccard of family sets).

## Tasks, splits, phases
Benchmark: official tau2 (sierra-research checkout recorded by commit), grader = official evaluator, reward in {0,1} (success = reward 1.0).
Learning phase A (structure exploration, RANDOMIZED structure arms S0-S3, propensity 0.25, verified labels from the official grade): airline test split (20) + retail tasks in the TRAIN side of a
task-hash split (plumme.keras_data.task_group, seed 1013, holdout 0.3). Evaluation phase B: retail tasks on the HELD-OUT side (never run in phase A or in learner training), all conditions.
Cross-domain transfer is therefore tested (airline+retail-train -> retail-heldout) and a second, descriptive transfer check runs the final conditions on the airline test split only after
phase B is analysed (already seen by c1/c2; reported as "previously seen domain, new organisation").

## Primary endpoint and inference (fixed now)
Unit = task block. Outcome = official success (unknown/incomplete = non-success, reported). Pairwise comparisons by EXACT McNemar on discordant pairs, two-sided alpha 0.05, Holm correction over
the confirmatory family {H1, H1c, H2, H3, H4 if testable}; effect size = paired risk difference with exact (Clopper-Pearson on discordant) CI. Independent evaluator: `fse ogi13 compare` run per pair
(the condition pair is mapped onto its FIXED/ADAPTIVE roles by the exporter and the mapping is part of the exported evidence); causal flags stay false unless this protocol's own tests and
randomisation checks are satisfied AND reported; no causal claim is made from a significance test alone.
Power statement (honest): with n_eval held-out tasks the confirmatory tests detect only large effects (e.g. n=24 blocks: >= 7 discordant pairs all in one direction for alpha 0.05 before Holm).
A non-significant result is a null result at this n, not evidence of equivalence.
Resources (secondary): provider dispatches, tokens, wall seconds, cash (known only), entitlement value estimate, per-verified-success only if every dimension is complete; unknown stays unknown.
Learner secondary: held-out log-loss/ECE from the attestation, decision-level structure distribution, regret against the best fixed structure.

## Exclusions and integrity
No post-hoc exclusion except the whole-block simulator-route discard above. No threshold, task list, split seed or test is changed after FREEZE. Discarded attempts and every run log are archived with
sha256 manifests (as c1). Trial-credit/entitlement consumption and cash are reported separately and never merged. Grader provenance stays "hash, not signature" (grader_provenance_attested=false).

## Conditions list (all share tools, tasks, policy text, simulator, AUTO supply)
SINGLE | SINGLE-E | FIXED | RG2-OFF | RG2-OFF-NOPERSIST | RG2-NO-TRIAGE | RG2-NO-VERIFY | RG2-NO-KNOWLEDGE | RG2-LEARNED (conditional on gate + owner authorisation) | RG2-RANDOMIZED (phase A only)
Implementation status before FREEZE (see FREEZE.txt checklist): SINGLE-E mode = done offline (runners/ogi013_single_e.py); NOPERSIST + per-block queue = evidence/ogi013-c3-prereg/queue; pairwise exporter = runners/export_pair_rows.py; trace report = runners/rg2_trace_report.py; c2 must be finished and evaluated first.

## Consistency with the existing research protocol (checked 2026-10-27)
- OGI013_EVALUATION.md (OGI13-PAIRED/1): the independent evaluator is unchanged and still two-arm (FIXED/ADAPTIVE roles); c3 maps each condition pair onto those roles per comparison (exporter mapping file is evidence)
  and adds NO threshold to it. That document states a cause can be considered only under a separately registered inference/ablation protocol: this file is that registration; it was written before any c3 data.
- PILOT-PROC/1 (OGI-012 inquiry pilot F1/F3/A) is historical and untouched. Its FREE_ONLY requirement (`PLUMME_COST_POLICY=FREE_ONLY`, `fse logcheck --expect-cost-policy FREE_ONLY`) belongs to that pilot and its
  cost gate only; c3 runs budget-aware AUTO, so c3 seals use `fse seal create` over each condition's DecisionLog + results and `fse logcheck --expect-cost-policy AUTO`. PILOT-PROC/1 analysis is descriptive; c3's confirmatory tests are new and stated above.
- ORG-GATE/1 vs MQ-GATE/1 (PlumMe keras_model.py): same structure and the same ECE bound (0.10), same min_test_tasks (12) and min_tasks (40), same "CI lower bound of the gain above 0" rule; ORG-GATE adds
  min_rows_per_structure (40) because the target is structure-specific, uses log-loss (binary outcome) instead of RMSE, and requires 300 rows (MQ: 200) because labels are episode-level and rows within a task are correlated.
  Like MQ-GATE, a permitting verdict never activates anything: activation needs the separate host authorisation flag of the registered learner-on arm (owner order 2026-10-27 authorises that arm's comparison once the gate permits).
- Supply: PlumMe AUTO over ALL eligible authorized supply (free tiers, free/promotional/trial credits, included, prepaid, and paid routes only within real approved spending). c1/c2's trial-off / zero-charge settings are recorded historical conditions only.
- Learned-policy claims: SHADOW_ONLY recording is never reported as organisational learning; only the registered learner-on vs learner-off held-out comparison (H4) counts, and only if the gate permits.
