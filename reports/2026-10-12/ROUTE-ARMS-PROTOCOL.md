# ROUTE-ARMS-ABC/1 — pilot-grade controlled comparison (written and committed BEFORE any arm ran)

Date 2026-10-12. Contract FRUITSTACK-KERAS-SCIENTIFIC-CLOSURE-003, gate G12. Evaluator commit at registration: `662a611` (branch `cc/model-ope-003`).
**Status: PILOT-GRADE, exploratory. Not the pre-registered 50-task inquiry pilot (PILOT-PROC/1), which cannot run: no owner-approved 50 references exist.**

## Question
Does route diversity (A -> B) change task delivery and verified answer quality, and do randomized model choices (C) give enough logged support to evaluate alternative
cognitive-model policies (`fse ope-model`)? No claim is made about an online Keras advantage: Keras is SHADOW_ONLY and acts on nothing.

## Task material (frozen)
`fse calib generate --n 48 --seed 20261012` (FSE-CALIB/1, six kinds x four levels, exact answers checked by the harness, HARNESS_OBSERVED).
task_set_digest `640ddd244ca53e284e462db97125d996bd82682fc13a0a32e533b71e074d8335`; file `route-arms-tasks.jsonl` (sha256 recorded in the run manifest).
Task class = `CALIB-<kind>`; task identity = `task_id`. Calibration tasks are exact-answer arithmetic/text tasks: they test delivery and correctness, not organizational intelligence.

## Cognitive-model pool (fixed for all arms)
`gpt-oss-20b@default`, `gpt-oss-120b@default`: the models that currently have both a direct Groq route and a gateway route (FreeLLMAPI). The pool is the same in every arm;
B and C add ROUTES only. (`qwen3.8-27b` is excluded: Groq's is a VISION-profile model, a different cognitive worker than the gateway's text model.)

## Arms (interleaved task by task, rotating order, one PlumMe state directory and one supply regime per arm)
- **A** regime `ARM-A-DIRECT-FREE-20261012`: direct routes only (no gateway adapters). Model policy: CherryMe deterministic plan = first candidate of the registry ranking inside the pool.
- **B** regime `ARM-B-FEDERATED-20261012`: A plus the FreeLLMAPI gateway (keyless platforms kilo, ovh, aihorde). SAME deterministic model policy; same-model failover inside the lease.
- **C** regime `ARM-C-HIER-SHADOW-20261012`: supply of B. Model choice by the authorized experimental behavior policy (uniform epsilon=1.0 over the pool, seed 20261012, draw index = task order),
  propensity logged at decision time; Keras SHADOW_ONLY recommendations recorded (statistical per-model means; the neural scorer is not ready and not used).
Common: `FREE_ONLY`, research runtime (no local inference), role REASONING, max_calls 2 per lease, max_output_tokens 400, >= 5 s pause per call, no key rotation.
Account entitlement: owner confirmed on 2026-10-12 that the Google and Groq keys are free tier without billing; routes are admitted by that confirmation or by route-level price evidence.
`cost_usd` stays unknown (null) and is never reported as an observed zero; billing evidence = the free-tier confirmation + route price evidence + per-provider call/token counts.

## Bounds and stopping
Per arm: <= 48 decisions, <= 110 provider attempts, <= 60 000 tokens, <= 3 h wall time. An arm stops after 5 consecutive tasks that fail with credential/quota-pool exhaustion (the shared free quota is
spent; nothing is retried or rotated). Unserved tasks stay unlabelled (censored), never zero.

## Verification
Per task, the harness (`fse calib score`) compares the parsed `ANSWER:` line with the exact answer. verified_utility = 1 correct, 0 executed and wrong/unparsed; no label when not executed.
Feedback is recorded into PlumMe with verifier `fse-calib/1:HARNESS_OBSERVED`.

## Analysis (fixed now)
1. Per arm: tasks, served, refused, delivery rate, accuracy among served, accuracy over all tasks (unserved counted as failures for the A/B comparison only), median latency, failovers, tokens, provider attempts.
2. A vs B on identical tasks: discordant pairs on `correct`, exact two-sided sign test; no confidence claim beyond what 48 tasks allow (`fse power paired --margin 0.10 --discordance 0.2` = 157 tasks needed).
3. C: `fse ope-model --regime ARM-C... --min-tasks 20 --min-support 10 --min-ess 10` for targets first_ranked, recorded_shadow and fixed per model. These pilot thresholds are fixed here;
   a result is reported identifiable only if they hold. Otherwise: NON_IDENTIFIABLE, no IPS/SNIPS.
4. Keras: the neural lifecycle is exercised on this run's verified rows through `evaluate_mq` and its gate (expected: INSUFFICIENT_EVIDENCE at n=48); the verdict is reported as it comes out.
## Allowed conclusions
Descriptive operational differences; support/identifiability diagnostics; the gate verdict. NOT allowed: any Keras online advantage; any claim of superiority from A vs B at n=48; any extrapolation to organizational tasks.

## Amendment 1 (ROUTE-ARMS-ABC/1.1), written before the real run, after a 2-task smoke test (6 real calls, rows archived in `smoke-discarded/`, not analysed)
The smoke test showed that PlumMe's route ordering placed the FreeLLMAPI gateway route BEFORE the direct Groq route of the same model in arms B and C (5.2 s vs 0.5 s), because the market-wide adapter
priority was ranked ahead of reliability. That is a defect of the route stage, not a property under test. PlumMe commit "route-stage ordering by evidence" orders routes of one model by health, quota pressure,
observed reliability, hop count (direct before gateway), latency, and only then adapter priority. The arms, pool, tasks, bounds and analysis are unchanged. Consequence: in B and C a gateway route is used
when the direct route fails or has worse observed reliability; with a healthy direct route B and A are expected to behave alike. The smoke rows are excluded from all results.
