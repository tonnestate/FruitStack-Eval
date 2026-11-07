# OGI-013 organisational learning loop - implementation contract (2026-10-27)
Reuses: PlumMe DecisionLog + record_decision_feedback (scope ENSEMBLE) + keras_data splits (split_by_task) + keras_model MQEnsemble style (Keras 3, JAX backend, pure-Python gate),
CherryMe RG/2 + the trusted host `responsibility_context` frame (the ONLY designed channel by which a host influences staffing; the engine reads it per question), engine accounting.
No second engine. CherryMe keeps cognitive authority: the host policy only sets structure REQUIREMENTS (challenge / verify), exactly as the responsibility skill documents.

## Precise gap this closes (code facts)
1. ensemble.py: in RG/2 graph mode a Keras policy_proposal is only recorded; skill policy_mode is BOOTSTRAP -> Keras cannot influence RG/2 staffing today.
2. ENSEMBLE decisions are logged with propensity 1.0 (deterministic) -> effects of team structure are not identifiable without randomised exploration.
3. keras_model/keras_data train ONE target: single-worker verified_utility. build_ensemble exists as a dataset builder but has no trainer, no gate, no weights path.
4. KerasRoomRecord is in-memory and belongs to PlumMe rooms, not to RG/2 teams. DecisionRecord has no structure/responsibility/recovery/cost fields.
5. Verified outcomes: the official tau2 grader is the independent verifier at task level; nothing connects its reward to the ENSEMBLE decisions.

## Structure arms (what the learned policy chooses among; discrete, all inside the skill contract)
S0 = PRIMARY only: responsibility_context {}   (engine may still add roles on CONFLICT)
S1 = PRIMARY + CHALLENGE: {"challenge": true}
S2 = PRIMARY + VERIFY: {"verify": true}
S3 = PRIMARY + CHALLENGE + VERIFY: {"challenge": true, "verify": true}
Modes of the host structure policy: OFF (no responsibility_context: engine triage 'auto' decides = learner-off baseline), FIXED (always one named arm), RANDOMIZED (uniform over arms
via cherryme.experiment.epsilon_floor_draw, seed = sha256(task_ref|question index), propensity logged), LEARNED (loads gated weights; refuses to run without a gate attestation file
whose verdict permits it AND an explicit host authorization flag; otherwise raises).

## Decision-time features (structured only; no worker self-assessment, no model identity)
importance (float), kind in {READ, WRITE, TRANSFER, MESSAGE} (from tool type), step_index (agent turn), prior_alerts (0..3 from the bridge), n_prior_org_decisions, n_prior_dissents,
domain_id_hash is NOT a feature (cross-domain transfer must be possible).

## Store (append-only JSONL under OGI013_ORG_STATE_DIR/training/, one file per kind)
decisions.jsonl rows (schema OGI013-ORG-DECISION/1): task_ref, domain, arm_mode, structure, propensity (null when not randomised), features{}, claim_id, plumme_ensemble_decision_id,
  accounting{responsibility_count, unique_workers, activation_count, dispatches_by_responsibility, delivered, unfilled_mandatory} (from engine events routing.ensemble.accounting),
  contributions{by_kind_status counts from the engine ledger for this claim}, revised(bool), action_changed(bool), provider_calls, provider_dispatches, created_at.
outcomes.jsonl rows (schema OGI013-ORG-OUTCOME/1): task_ref, domain, reward (official tau2), grader ("tau2-official-grader" + result sha256), decision_ids[], tokens, calls, wall_seconds,
  economic{cash_known_usd|null, entitlement_value_usd_est|null}, created_at.
Attribution (PlumMe): for every decision of the episode call service.record_decision_feedback(decision_id, epistemic_state="VERIFIED", verified_utility=reward, verifier="tau2-official-grader",
  scope="ENSEMBLE", attribution_basis="EPISODE_OFFICIAL_GRADER"). Episode-level credit is a stated limitation (all decisions of an episode share the label).

## Learner (Keras 3 + JAX; run with /root/SUPPLY-001/venv3.12/bin/python and PYTHONPATH=<plum-org>/src)
Input: features + one-hot(structure) -> small MLP ensemble (5 members, bootstrap by TASK) -> predicted success probability, split-conformal calibrated (reuse MQEnsemble pattern).
Policy: argmax over the four structures of predicted success (cost term lambda = 0 as primary; resources reported separately). Unseen feature support -> falls back to engine triage (OFF).
Training data: ONLY RANDOMIZED-mode decisions with VERIFIED outcomes (propensity known). Split by task (keras_data.split_by_task, seed fixed in the pre-registration), held-out tasks never trained on.
Gate ORG-GATE/1 (thresholds in evidence/ogi013-learning/ORG_GATE_V1.json, fixed BEFORE any training): min_rows, min_tasks, min_test_tasks, per-structure minimum rows, held-out
log-loss better than the best of {global-mean, structure-mean, logistic-on-features} baselines with task-bootstrap CI low > 0, ECE <= max. Verdict values: INSUFFICIENT_EVIDENCE,
NOT_BETTER_THAN_BASELINE_OR_MISCALIBRATED, LEARNED_POLICY_PERMITTED_FOR_AUTHORIZED_ARM. The attestation file records verdict, data hashes, split digests, thresholds, weights hash.
Nothing is activated by a verdict alone; activation needs the host authorization flag of the registered learner-on arm.
