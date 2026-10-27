# OGI-013 campaign c2 - airline test split, instrument-corrected rerun (pre-registered 2026-10-27, before any c2 run)

Status: c1 (evidence/ogi013-c1-airline-test) stays unchanged and is NOT overwritten. c2 is a separate, new experiment.

## Why c2 exists (concrete fault hypothesis, from c1 evidence)
- c1: 17/20 tasks failed in both arms. Rule-based attribution (cause_attribution.json): 27 of 34 failing arms were stopped by an AppleMe
  LOOPING/THRASHING/STALLED assessment -> PeachMe HEALTH_WARNING BLOCK, while the conversation was still making real progress.
- Cause (verified in code): the runner sent AppleMe events carrying only question_type ACT/SAY and outcome PROGRESS (no information gain),
  so consecutive ordinary tool lookups looked like "same action repeating without information gain". Offline replay of the recorded
  transcripts (replay_assurance.json) shows that with environment-observed gain reported, the sensor stays HEALTHY through every
  pre-block turn in the 27 arms; later unhealthy flags in the replay come from the artificial blocked-transfer tail and are not counted.
- Second defect: after a reflex stop the runner issued transfer_to_human_agents, which the same reflex refused, so tau2 ended with
  "too_many_errors" instead of a clean stop.

## Change (the only intervention; identical for both arms)
1. AppleMe events now name the tool (ACT:<tool>) and report verified_evidence_total = count of distinct non-error environment tool
   results seen so far (environment output, not model claims).
2. Reflex stop returns a plain ###STOP### message (no refused tool call).
Not changed: AppleMe thresholds, Pomelo authority/policy, PeachMe reflexes, PlumMe routing (AUTO, free routes only,
PLUMME_TRIAL_CREDIT=off), CherryMe, prompts, simulator handling (one PlumMe-chosen simulator model per pair, pair discarded and
re-run on simulator-route failure, max 3 attempts), grading (official tau2 grader), task order irrelevant.

## Design
- Tasks: all 20 airline test-split tasks (ids as in c1). Pairs FIXED vs ADAPTIVE, arm order alternating by task-id parity.
- Primary outcome: official tau2 reward (success = 1.0), paired per task, evaluator ogi13 compare --require-complete.
- Secondary (descriptive only): resources per task (provider calls, tokens, wall time); reflex-block rate; share of episodes ended by REFLEX_BLOCKED;
  escalations/challenges/revisions used by ADAPTIVE (to see whether the organisation could act at all).
- Pre-stated reading: if reflex-block rate falls substantially vs c1 and success counts rise, the sensor was a dominant confound of c1.
  If ADAPTIVE and FIXED still tie, that is a result about this organisation on this task slice, not proof of equivalence in general.
- Known uncontrolled factors, reported not hidden: AUTO routing picks different free agent models per arm (c1: model mix differed);
  cost per success undefined (free routes report null cost); grader provenance hash only; no randomisation attestation.
- No post-hoc task or arm exclusion except whole-pair discard on simulator-route failure (logged in progress.txt and discarded/).
- Next (separate pre-registration, only if c2 is interpretable): retail test split (40 tasks) with the same instrument.
