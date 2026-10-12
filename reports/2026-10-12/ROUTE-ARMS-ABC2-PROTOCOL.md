# ROUTE-ARMS-ABC/2 — prospective controlled comparison (registered before any confirmatory call)

Date 2026-10-12. Contract FRUITSTACK-REPAIR-AND-FINAL-EVALUATION-004. This protocol is committed to the evaluator repository before the first confirmatory provider call;
the run's `frozen-config.json` records the commits, task hash and capability-snapshot hash and a resume is refused if any of them differ.
It is a NEW experiment. The 48-task ROUTE-ARMS-ABC/1 pilot (run with the defects listed below) stays in `route-arms-2026-10-12/` unchanged and is not pooled with this run.
It is NOT the 50-task inquiry pilot PILOT-PROC/1 (F2/F3): that one needs owner-approved inquiry references and is a separate experiment.

## What changed since ABC/1 (all found by independent verification of ABC/1, each with a regression test)
1. Truncated provider output (`finish_reason=length`/`max_tokens`/`incomplete`) is a SEMANTIC_OUTPUT_FAILURE even if some text exists; usage, request id and finish reason stay on the failed receipt.
2. A rate limit or credit exhaustion never rotates to another credential of the same provider (quota circumvention); only AUTH_FAILED/AUTH_EXPIRED may.
3. Task generation FSE-CALIB/2 is stable across Python hash seeds (word_sort order was not).
4. The runner is resumable: durable per-arm results, an intent journal (an in-flight call at a crash is recorded as IN_FLIGHT_UNRECONCILED, charged at its worst case and never repeated),
   cumulative bounds rebuilt from rows, a frozen configuration, a frozen capability snapshot, a global pause (exit 75) on free-quota exhaustion or an empty supply.
5. The analyzer rescoring compares recorded and independent scores before replacing; provider attempts and charges come from receipts; the analyzer imports no product code.
6. Live check before freezing: a gateway probe with a 48-token cap returned SEMANTIC_OUTPUT_FAILURE (REASONING_LEAKED_AS_CONTENT, finish_reason=length) with usage retained; a 6-task x 3-arm smoke
   run (separate task seed 20261099, not in this data) delivered and graded correctly. Acceptance evidence: `/root/fruits/research/FRUITSTACK-EVAL-004/`.

## Question and hypotheses
Does adding keyless gateway routes (same models, same deterministic model policy) change the proportion of tasks that end with a verified correct answer, compared with direct free routes alone?
- **H1 (primary, the only confirmatory hypothesis):** P(correct | task, arm B) differs from P(correct | task, arm A), unserved tasks counting as not correct. H0: no difference.
- Secondary (descriptive, Holm-adjusted over the three pairwise comparisons, reported even if negative): C vs B and C vs A on the same endpoint; delivery rate; answer-bearing rate; accuracy among
  executed (conditional on delivery, therefore not causal); median latency; failovers; tokens; route mix.
- C's purpose is data for model-level off-policy evaluation, not a performance claim. The Keras ensemble stays SHADOW_ONLY and acts on nothing.

## Task material (frozen)
`fse calib generate --n 160 --seed 20261013` (FSE-CALIB/2: six kinds x four levels, exact answers, HARNESS_OBSERVED grading, no overlap with ABC/1 or smoke prompts).
File `reports/2026-10-12/route-arms-abc2-tasks.jsonl` sha256 `c8662e2cb29e5d417879b06ba91f75cd3d9f41f82214c800c8847fc3bec11771`, task_set_digest `bc6359993377b809479c26ffd3d4213939be6b42652883f59c3971e11ae1d177`.
Sample size: `fse power paired --margin 0.10 --discordance 0.2` = 157 tasks (alpha 0.05, power 0.8). If the true discordance exceeds 0.2 (e.g. 0.3 needs 236), the run is underpowered and says so.
These are calibration tasks (arithmetic/text with exact answers): they measure delivery and correctness of the supply chain, not organizational intelligence.

## Arms (interleaved task by task with rotating order; one state directory and supply regime per arm)
- **A** `ARM-A-DIRECT-FREE-20261012`: direct routes only; CherryMe deterministic plan (first-ranked candidate inside the pool).
- **B** `ARM-B-FEDERATED-20261012`: A plus the isolated FreeLLMAPI instance (keyless kilo, ovh, aihorde); same deterministic model policy; same-model failover inside the lease.
- **C** `ARM-C-HIER-SHADOW-20261012`: supply of B; model drawn by the authorized experimental policy (epsilon 1.0 uniform over the pool, seed 20261013, draw index = decision count, logged propensity).
Pool for all arms: `gpt-oss-20b@default`, `gpt-oss-120b@default`. Common: FREE_ONLY, research runtime (no local inference, no Ollama), role REASONING, max_calls 2, **max_output_tokens 1024** (ABC/1 used 400; the
reasoning models spent it on reasoning; identical for all arms), pause 10 s per call, no key rotation, no retry beyond the lease budget.
Entitlement: owner confirmed on 2026-10-12 that the Google and Groq keys are free tier without billing (env confirmations only, never written to configuration). `cost_usd` is null and stays UNKNOWN.

## Bounds, pause and resume
Per arm: decisions <= 160, provider attempts <= 400, tokens <= 240 000, cumulative active wall time <= 24 h. Five consecutive quota-exhausted observations in any arm pause the WHOLE run (exit 75, state kept);
an empty supply pauses without writing any observation. Resuming is a new invocation of the same command; it continues at the first task without a result, under the frozen configuration. Outage observations
that were recorded before a pause stay in the data as failures to deliver (negative outcomes are retained); a sensitivity analysis excludes tasks whose failure class is quota exhaustion.
No quota is bypassed, no key rotated, no observation is fabricated. If bounds are reached before all 160 tasks are done the result is reported as incomplete with the actual n.

## Analysis (fixed now)
1. Independent rescoring with the evaluator's grader (`runners/route_arms_analyze.py`); any disagreement with the in-run score is reported and the independent score is used.
2. H1: exact McNemar (two-sided binomial on discordant pairs) at alpha 0.05, plus the paired risk difference with a task-bootstrap 95% interval (2 000 resamples, fixed seed). Decision: H1 supported only if p < 0.05;
   otherwise "not supported" (not "no effect"). The interval is reported either way.
3. Secondary comparisons: same test per pair, Holm-adjusted over three; descriptive statistics as listed. No subgroup mining beyond the six task kinds, reported descriptively.
4. C: `fse ope-model` with min_tasks 20, min_support 10, min_ess 10 and the route-dependence validity check. Targets first_ranked, recorded_shadow, fixed per model. If not identifiable: NON_IDENTIFIABLE, no IPS/SNIPS.
5. Keras: `plumme keras-lifecycle` on arm C's verified rows (task-disjoint holdout, baselines, calibration, gate MQ-GATE/1), exported as data and embedded by the analyzer. Gate result reported as is.
6. Billing/quota: per-provider attempts, tokens, rate-limit headers, failure classes from receipts; unknown charges are counted as unknown.

## Validity conditions
The run is invalid for H1 if: the independent rescoring disagrees on more than 2 observations that cannot be explained, a provider returns an answer that violates the integrity rules and is delivered anyway,
the frozen configuration changed, or arms received different tasks. Invalidation is reported, not repaired by dropping data.

## Reproducibility package
tasks, frozen-config.json, protocol, results-*.jsonl, journal-*.jsonl, run-state.json, state-*/ receipts and decisions, seals (`fse seal create`), cost audit (`fse costaudit`), analysis.json and its stdout,
keras-lifecycle export, command lines, commits, environment (python 3.11.16, Keras 3.15.1 + JAX CPU), the capability snapshot (sha256 0e9ba5a2...), the isolated gateway instance commit a701ab6.
