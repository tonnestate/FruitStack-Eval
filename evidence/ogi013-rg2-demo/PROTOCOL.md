# OGI-013 RG/2 demonstration protocol (written 2026-10-27, before any live run of it)
Purpose: show on real official benchmark tasks that CherryMe's RG/2 workers make an observable, separately reported contribution. This is a mechanism demonstration,
not the registered FIXED-vs-ADAPTIVE comparison and not a success-rate claim. c1/c2 remain historical evidence, untouched.

Stack: FSE ogi013-org-bridge, CherryMe ogi013-org-cherry, PlumMe ogi013-org-plum (response-limit negotiation, AUTO, no caller output cap), PeachMe/AppleMe/MangoMe/OrangeMe/PomeloMe as in c2.
No FastTrack component exists in any CherryMe checkout; the reused fast path is triage `auto` (simple tasks skip the triage call, status SKIPPED_SIMPLE_TASK).
Run only after c2 has finished (c2 shares the provider supply). The rg2 launcher requires the owner's host-approved budget (runs/host_budget.env); no cost-class restriction, trial-credit exclusion or zero-dollar limit is applied. c1/c2's TRIAL_CREDIT exclusion and zero-charge setting are recorded historical conditions only.

## Contribution is counted only if the trace shows it (all from existing ledgers: cherry contributions.jsonl, cherry events.jsonl, ORG_* events)
1. Worker contribution: a CherryMe contribution row of kind PROPOSAL/CANDIDATE/VERIFIER with a delivered answer (not ATTEMPT_FAILED).
2. Independent verification: an Evidence PASS or CONTRADICT promoted by EvidenceVerifier with >=2 distinct independence keys and verbatim quotes (verifier.log).
3. Causal effect on the decision: an ORG_REVISION event with action_changed=true after worker/verified dissent. A draft that was accepted unchanged is reported as
   "original draft accepted", never as organisational success, even if the task reward is 1.0.
4. Productive recovery: a SWITCH_WORKER (or recompose) intervention followed, within the same question or the next, by an attempt on another worker with outcome PROGRESS.
5. Persistence: in a second task run with the same OGI013_ORG_STATE_DIR, a ZERO_CALL VERIFIED_KNOWLEDGE hit or a knowledge lead (UNVERIFIED_FOR_THIS_CLAIM) appears in the engine's
   events/claims; arms never share a state dir.
6. Learning: reported only as "not demonstrated" unless worker-behaviour evidence demonstrably changes a later staffing decision (WorkerBehaviorMemory is in-memory per process).

## Procedure
- Task A then task B (airline test split, tasks sharing policy rules), same arm state dir, simulator model pinned per task, PlumMe AUTO, host-authorized envelope from run_org.sh.
- Report per decision: draft action, engine status, workers (model keys), rows by kind/status, revision (changed or not), tokens/calls, plus every capability not demonstrated.
- Failures (supply, semantic output) are reported with their codes; no run is repeated to cherry-pick a favourable trace except whole-pair simulator-route failures (logged).
