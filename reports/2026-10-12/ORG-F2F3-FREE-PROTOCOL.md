# ORG-F2F3-FREE/1 — FREE_ONLY comparison of a fixed two-model baseline (F2) and the full FruitStack organization (F3)

Status: **PREPARED, NOT YET REGISTERED.** It becomes the registered protocol when (1) the F2 pair has been selected by the rule below, (2) this file plus `frozen-config.json` are committed with the final
candidate hashes, and (3) that commit exists before the first confirmatory provider call. No timestamp here is a registration timestamp. The historical PILOT-PROC/1 (with its paid Arm A and F1) is
preserved unchanged and is not amended by this document.

## Question
Does the fully organized FruitStack architecture (F3) answer more inquiry tasks correctly than a fixed, non-organizational two-model baseline (F2) when both have the same FREE_ONLY external supply,
the same information-access rights (web search) and comparable, explicitly measured resources?

## Frozen material
- Tasks: owner-approved manifest `proposed-tasks.jsonl`, sha256 `4be706c405390869…` (50 tasks, FSE-INQUIRY/1; approval record `APPROVAL-RECORD.json`, provenance verified from the session transcript).
  Order = file order; arm order alternates per task (F2,F3 / F3,F2 ...). The runner reads only task_id, claim, question; references stay with the grader.
- Calibration (disjoint, FSE-CALIB/2 seed 20261014) is used only for the F2 pair.
- Candidates: PlumMe, CherryMe, AppleMe, FruitStack-Eval exact commits, the web-search adapter file (sha256 pinned), the capability snapshot (sha256 pinned) and Python/Keras versions are written into
  `frozen-config.json` by `f2f3_epoch2.py init`; the file is immutable afterwards and every step re-verifies the task and adapter hashes.

## Arms (component configuration, fixed before execution)
**F2** — PlumMe only. Two cognitive models from different vendor lineages (pair rule below). Information access: ONE fixed web search per task using the same search runtime, query construction and
top-5 truncation as F3's grounding adapter; the results are appended to the task prompt for both models (context, not proof). Each model answers once (PINNED_MODEL lease, same-model route failover,
max 2 attempts, 1024 output tokens). Composition: unanimity of VERDICT (SUPPORTED/REFUTED) -> answer = first-listed model's VERDICT/KEY block; otherwise abstain (graded 0). No orchestration, no Keras, no review.
**F3** — CherryMe 0.3.0 with the ACE ensemble skill (question budget 3, provider-call cap 4, plus one final synthesis call), PlumMe federated supply with model-level identities and route failover,
AppleMe assurance tier, MangoMe only as the local evidence outbox (no canonical authority is available for this research run, so no MangoMe governance claim is made), live web grounding (adapter inside
CherryMe's own questioning), Keras SHADOW_ONLY (records recommendations, acts on nothing). Final answer: one pinned authorized model call over the evidence (corrected synthesis: claim status alone never produces an answer).
Both: FREE_ONLY (hard gate), research runtime (no local inference, no Ollama), no paid route, no key rotation, no retry beyond the lease, state directory and supply regime per arm, owner free-tier confirmations only via environment.

## F2 pair (registered rule, applied before registration)
Shortlist (one model per lineage, general text >= 20B, route executable now): gpt-oss-120b, qwen3.6-27b or qwen3.8-27b (whichever has a text profile), llama-3.3-70b, mistral-small-3.2-24b, nemotron-3-super-120b,
gemma-4-31b. Each answers the first 24 calibration tasks once (`runners/f2_pair_select.py select`). Eligible = delivery >= 0.8; pair = the two highest accuracies (over all 24 tasks) from different
lineages; ties -> delivery, then name. The ranking and pair are stored in `pair-decision.json`. Two routes to one underlying model, or two models of one lineage, are never counted as independent workers.

## Endpoints
**Primary:** per task, correct = grade 1.0 (VERDICT and KEY right). Missing answer, abstention, failure, unreconciled call = not correct. F3 vs F2, exact two-sided McNemar on discordant pairs, alpha 0.05;
risk difference with 2 000-resample task bootstrap 95% interval (seed 20261013). `SUPPORTED` only for a positive difference with p < 0.05; otherwise `NOT_SUPPORTED` (not 'no effect'); an incomplete run gives no decision.
**Secondary (reported whatever the sign):** mean graded utility (0/0.5/1) and its interval; abstention, no-answer and failure rates; each F2 member model graded on its own answer; calls, tokens, wall time,
correct-per-1k-tokens (efficiency is reported SEPARATELY from quality and F3 is not credited for using more calls); route reliability and failover counts; response-integrity failures; F3 verifier/reviewer
contribution from the ACE decision log; cost evidence (cost_usd null = unknown, never zero); human interventions (none planned; any is logged).
**Descriptive only:** per subfamily; no subgroup is promoted to primary after the data are seen.
**Sensitivity:** primary analysis repeated without tasks hit by quota exhaustion or an unreconciled call in either arm.

## Power and sample size
n = 50 paired tasks. With discordance <= 0.2 a 20-point difference is detectable (needs 40); at discordance 0.3 about 59 are needed; smaller effects are NOT detectable. An inconclusive result is a valid outcome.

## Execution, pause and resume
`f2f3_epoch2.py` (`status|step`) with a driver loop; one arm-task at a time; started marker -> result file; an interrupted arm-task is recorded as IN_FLIGHT_UNRECONCILED and never repeated;
rate-limit/credential exhaustion/no route -> the failed observation is recorded, a bounded backoff (15, 30, 60, 120 min, Retry-After if later) suspends the run; nothing is bypassed, no paid or local substitute.
Quota-failure observations recorded before a pause stay in the data. The run is complete when all 100 arm-tasks have result files and `fse inquiry grade` has graded all of them.

## Validity conditions
Invalid for the primary analysis if the frozen configuration or task hash changed, arms received different tasks or search access, an answer violating the integrity rules was delivered, or the independent
grading disagrees with the arm's own parse for reasons other than grading. Invalidation is reported, not repaired by dropping data; a corrected measurement would be a new, separately versioned epoch.

## Known limitations (stated now)
Tasks drafted by Claude and audited by a second model instance, not by a person; claims restate the key in 13/25 SUPPORTED tasks; web search can retrieve the cited primary pages themselves, so the tasks measure
evidence use more than recall; only two models, one time window, shared free quota; n = 50; gateway models carry no independence-group metadata (lineage is taken from the registered table);
the search adapter lives in the release payload, not in a candidate repository (hash-pinned); MangoMe adds no governance effect here.

## Reproduction
`F2F3_RUN=<dir> python runners/f2f3_epoch2.py init --config cfg.json`; repeat `step` until exit 30; `f2f3_analyze.py --run <dir>`; seals via `fse seal create`; `fse costaudit`.
