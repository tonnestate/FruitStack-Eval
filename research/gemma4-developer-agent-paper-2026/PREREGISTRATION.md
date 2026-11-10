# Preregistration — SER study, H3 localization (own benchmark)

Committed **before** any confirmatory H3 outcome was computed. Date: 2026-11-09 (Europe/Berlin).
Applies to `PAPER.md` v0.2 §3.2, §4, §5.1. H1/H2 are preregistered separately before their first episode.

## Data (deviation from PAPER v0.2 §3.1, stated in the paper)

- **Not the Kaggle competition data.** No Kaggle credentials, mounts or competition graph exist on the execution
  host (see `EXECUTION_REPORT_2026-11-09.md`). Per owner order 2026-11-09 the study uses an own benchmark:
  SWE-bench Verified, test split, 500 instances, local parquet
  (sha256 `a45b1fe4e2f0c839…`, full hash in `h3_eval/TASK_MANIFEST.json`).
- Graph: rebuilt per task with Python `ast` at the task's `base_commit` (`h3_eval/swebench_adapter.py`).
  Node type: function/method/class with file, qualname, signature, source span.
  Edge types: `contains` (lexical nesting) and `calls` (call-name resolution: same file first, otherwise
  global name with ≤ 3 definitions; ambiguous names unlinked). No `imports`/`inherits` edges.
- `dense_ranking` omitted for **all** tasks (no competition encoder). Arm A is therefore BM25 only.
- Gold patch is read only by the scorer.

## Tasks

- Deterministic draw: `swebench_adapter.draw(rows, 500)` (stratified by repo, order by sha256 of salt `GEMMA4-SER|` + id).
- **Pilot (excluded from all results):** first 3 of the draw — `astropy__astropy-14369`, `django__django-14089`,
  `matplotlib__matplotlib-24627`. Disclosure: the pilot summary (recall values on these 3 tasks) was printed
  during the smoke run, so pilot outcomes were seen, not only wall time. They carry no weight in any result.
- Pilot timing (per task, 8-core CPU, no GPU): adapter ≈ 10 s; arm A 2.4–6.4 s; arm B 0.1–0.4 s.
  Hence no compute constraint on n.
- **Confirmatory n = 497**: the remaining draw, in manifest order (`h3_eval/TASK_MANIFEST.json`).
  Exclusion rule: a task whose snapshot cannot be built or whose symbol table is empty is excluded and listed.
  Tasks without gold symbols stay in for file recall only (evaluator rule).

## Evaluator and frozen parameters

- `h3_eval/ser_h3.py` unchanged, config `ser-h3-1.0`,
  digest `f02603adcd3a70e984b420b098826b7039cb8003e0a44756613929c54066b8dd` (covers CONFIG and FILTER_PROMPT).
- α 0.5 · 10 top seeds + ≤ 10 verbatim-name seeds · RRF k 60 · arm-A top-3 protected in top 10 ·
  all edge types are content edges.
- Runtime: Python 3.12.14, numpy 2.5.4, scipy 1.18.1 (venv `/root/fruits/research/GEMMA4-SER/.venv`).

## Arm C (Gemma recognition filter)

- **C (confirmatory, locked model `gemma-4-31b-it-qat-w4a16-ct`, greedy):** not executable on this host
  (no GPU; no available route serves this checkpoint). Reported as *not run* unless that runtime becomes available.
- **C′ (exploratory, labelled deviation):** same prompt, parser and fallback, model `gemma-4-31b-it`
  (same base model, not the QAT W4A16 checkpoint) via an authorized PlumMe route, temperature 0, max 512
  output tokens, one call per task. Provider, route and raw response are logged per task. C′ is never
  reported as C, never pooled with C, and carries no confirmatory claim.

## Analysis (as PAPER §4)

- Primary: symbol Recall@10, B vs A (and C vs B if C runs): Wilcoxon signed-rank + paired bootstrap 95 % CI
  (10,000 resamples, seed 0). Non-inferiority (margin 0.02) on the direct subset (A has a gold symbol in top 10).
- Secondary: file Recall@1/@5, per-repo breakdown (descriptive), wall time per arm.
- Everything reported as observed; no outcome-dependent change of parameters, tasks or metrics.

## Amendment A1 — arm C (2026-11-09 ~23:30 UTC, before any arm-C outcome)

Owner direction 2026-11-09: the Paper Track research runs on the full FruitStack multi-model system; only explicitly
isolated arms are Gemma-only. Arm C is such an isolated arm. It replaces the "C / C′" split above:

- **Model:** Gemma 4 31B instruction-tuned (`gemma-4-31b-it`), served through FruitStack PlumMe on authorized
  cost-0 routes (OpenRouter free tier, NVIDIA). Not the QAT W4A16 checkpoint; stated as such in the paper.
  Decoding is the route default (PlumMe exposes no temperature), max 512 output tokens — **not guaranteed greedy**.
  Every call (offer, provider, model, receipt, raw output) is logged.
- **Driver:** `h3_eval/run_c.py` with `h3_eval/plumme_gemma.py`. Prompt, parser and fallback are the frozen
  `ser_h3.py` ones. A *supply* failure (no model answer at all) is not a filter fallback: the task waits and is retried.
  An answer that is empty/unparseable or removes all seeds is the preregistered fallback and is counted.
- **Sample:** confirmatory manifest order; C covers the longest prefix completed by **2026-11-12 12:00 UTC**
  (supply-bound: free-tier rate limits). C vs B is tested on exactly that prefix (same tests as the primary endpoint).
  B vs A on all 497 remains the primary H3 result.

## H1/H2 (2026-11-09 ~22:00 UTC, before any confirmatory episode)

- **System.** FruitStack as the research executor: the unchanged coding runner `ogi013_code_task.py` in mode `single`
  (one author role; PlumMe AUTO selects and hands over among authorized cost-0 models; PeachMe episode; Pomelo-gated tools;
  CodingGate submit check), wrapped by `h1_eval/ser_episode.py`. Components at the pinned commits listed by
  `git describe` in `/root/fruits/research/GEMMA4-SER/components` (AppleMe c2ee35a, CherryMe 33c3d77, MangoMe 835d8be,
  OrangeMe 953e725, PeachMe efa9bab, PlumMe a81546c, PomeloMe 348975e). Models are **not** fixed; the participating
  models per step are logged (PlumMe receipts) and reported.
- **Arms.** E, E⁻ (`EM`), D* (`DS`) exactly as `ser_episode.py` at this commit: same task text, same initial top-10
  localization list (H3 arm B), same tools, budgets (110 calls, 200k tokens, 3600 s wall), packet size 3 from one shared
  candidate pool (B top 20 ∪ PPR from failure-trace symbols). D*: full history, frozen cap 120k chars.
- **Pairing.** The three arms of a task run **concurrently** (same supply conditions, same model pool); fresh workdir each.
- **Tasks.** Django tasks of the H3 manifest, manifest order, Django ≠ 5.0 (Python 3.8 grader), calibrated valid
  (base unresolved, gold resolved under `evaluate_v2.1`). Pilot `django__django-13569` excluded.
  **Stopping rule (time, not outcome):** triplets start in order until **2026-11-12 12:00 UTC**; n = completed triplets.
- **Outcome.** `resolved` from `evaluate_v2.1` run outside the agent process on the final workdir (only `django/` changes
  applied; F2P and P2P must pass). Infra stops (no model step at all) are rerun once; otherwise counted unresolved by class.
- **Analysis.** H1: E vs E⁻, H2: E vs D*; exact McNemar, Holm across the two; paired risk difference with 95% CI.
  Too few discordant pairs ⇒ "inconclusive", never "no effect". Secondaries (from `ser_ledger.jsonl`, gold from H3
  scoring only after the run): trigger rate, gold symbol in the eligible pool at trigger, wrong-trigger rate (refuted
  symbol was gold), persistence (edits to a symbol after PATCH_NO_EFFECT on it), steps, model mix, wall time.
- **Pilot (excluded).** `django__django-13569`, arm E, 2026-11-09 21:48–21:55 UTC: 309 s, 23 steps on 6 router-chosen
  models, 2 checkpoints, no event, runner stop `NO_PROGRESS` (existing guard, identical in all arms). Graded on the final
  workdir as specified (runner status is recorded alongside). No harness change after the pilot.

## Amendment H1-A1 (2026-11-09 ~22:20 UTC) — full FruitStack organisation mode

Owner direction (2026-11-09): use the complete FruitStack, including CherryMe's critical review. After 2 tasks
(4 completed single-author episodes, all unresolved; outcomes seen) the campaign was stopped and restarted in runner mode
`rg2` for **all three arms**: author → independent CherryMe Brother critic (different model, read-only copy, runs tests) →
reviser on the author's workspace (the runner's existing organisation, settings as in `run_code_arm.sh`).
The SER ledger and packets apply to the editing roles (author, reviser); the read-only critic gets neither, in every arm.
The critic only runs when the author submits a patch (existing runner behaviour).
The 4 single-mode episodes (`h1/runs_single_mode_disclosed`, tasks django__django-11211/-11292) are reported separately
and excluded from H1/H2. The confirmatory set restarts at the beginning of the manifest order, including those two tasks.
Everything else in the H1/H2 section is unchanged.

## Amendment A2 (2026-11-09 ~22:25 UTC) — PlumMe budget-aware AUTO (correction)

The driver had copied OGI-013 session ceilings (110 calls, 200k tokens, **USD 0**) and the arm-C adapter passed
`max_cost_usd=0`. Both contradict the standing owner order of 2026-10-27 (PlumMe budget-aware AUTO over all authorized
supply; no zero-dollar, call or token ceilings) and pushed PlumMe onto free tiers. Removed: no session ceilings; free,
trial-credit and included supply are eligible; cash routes stay off because no owner-approved cash budget exists.
The wall-clock limit (3600 s per episode) is unchanged and identical across arms. Episodes running under the ceilings were
aborted after a few steps with no outcome inspected (`h1/runs_aborted_costcap_20261109`); arm C had produced no
completed task (`h3c/out_aborted_costcap`). Both restart from the beginning of their manifest order.

## Amendment A3 (2026-11-09 ~22:35 UTC, before any arm-C outcome) — arm C model chosen by PlumMe

Correction of A1 per owner: pinning arm C to Gemma 4 31B was an unrequested restriction. Arm C's recognition filter
is served by PlumMe in budget-aware AUTO (`h3_eval/plumme_filter.py`): PlumMe selects and routes the model per call;
no model pin, no output or cost ceiling in the adapter. Provider, model, receipt and raw output of every call are logged
and reported. Prompt, parser, fallback, supply-wait rule, sample (manifest prefix by 2026-11-12 12:00 UTC) and tests
are as in A1. The paper names the arm "LLM recognition filter (PlumMe-routed)", not "Gemma filter".

Note (2026-11-10, disclosure, no rule change): grader calibration had initially been run only for the first 80 Django
tasks in manifest order (53 valid). It was extended in the same order to all 206 Django ≠ 5.0 tasks of the manifest
(130 valid, `h1/tasks/calibration.json`) before the campaign reached task 80, so the preregistered task rule
(calibrated-valid, manifest order, time stop) applies unchanged.

## Amendment A4 (2026-11-10 ~04:10 UTC) — earlier arm-C cutoff (time only)

Owner decision 2026-11-10 (submission timeline): the arm-C sample is the manifest prefix completed by
**2026-11-11 06:00 UTC** (was 2026-11-12 12:00 UTC). Decided on time grounds only, while no arm-C outcome had been
computed or inspected (158 tasks done, no C-vs-B statistic run). A task still in progress at the cutoff is not counted.
Prompt, parser, fallback, supply-wait rule and tests are unchanged. H1/H2 stopping rule unchanged.

Note (2026-11-10 ~07:05 UTC, disclosure, no rule change): arm C has waited on `pytest-dev__pytest-7236` since ~03:30 UTC
(the router offers one route for this role and it rejects this prompt; all other picks report no eligible model). Per the
supply-wait rule the task is retried, not skipped, so the C prefix may stay at 158 tasks by the A4 cutoff. While diagnosing
this (after A4 was committed), the per-task C recall lines of 4 earlier tasks were seen in the run log; no C summary statistic
has been computed.
