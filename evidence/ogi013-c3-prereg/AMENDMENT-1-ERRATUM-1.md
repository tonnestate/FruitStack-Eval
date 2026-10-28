# AMENDMENT-1 ERRATUM-1 — measurement-implementation defect in rg2_trace_report.py (2026-10-28)

Defect: `organisational_success` was computed as worker_contribution AND (causal_effect OR independent_verification) AND reward 1.0, so a verification alone (e.g. a provenance confirmation of an id that is present in the data)
established success although the draft was accepted unchanged. This contradicts the frozen evidence/ogi013-rg2-demo/PROTOCOL.md (criterion 3: "A draft that was accepted unchanged is reported as 'original draft accepted',
never as organisational success, even if the task reward is 1.0"). The "original draft accepted" note was also attached to the wrong condition (worker contribution instead of causal effect).
Found by: examination of the completed Phase A task airline:2 (reward 1.0, 0 revisions, one quorum-verified provenance claim) which the reporter labelled success.

Correction (no change of hypotheses, thresholds, sample, criteria text or quorum): organisational_success = worker_contribution AND causal_effect_on_decision (ORG_REVISION with action_changed=true) AND official reward 1.0;
False when any of the three is known to fail; None when unknown. Independent verification, worker contribution, recovery, knowledge reuse and reward remain separately reported observations (nothing discarded).
Regression test: tests/test_ogi013_measurement_amendment.py::test_unchanged_accepted_draft_is_never_organisational_success (reward 1.0 + valid verification + worker contribution + zero revisions => False).

Offline re-evaluation from stored traces (evidence/ogi013-rg2-demo/reeval-ERRATUM-1/, originals report-*.json and run*/ untouched):
- airline:2 (phase A): True -> False (verification only, 0 revisions). - final demo d2 (task 6): True -> True (quorum-verified CONTRADICTS, 1 VERIFIED_DISSENT revision with action_changed=true). - final demo d1: None -> False.
- earlier diagnostic runs run1..run3 d1/d2: None -> False (zero revisions now known); run4, run5: unchanged.
- Demo gate (organisational_success of either demo task): UNCHANGED, True via d2 (task 6).
Historical reports stay as produced by the defective formula and are superseded by the re-evaluation files for the organisational_success field only.
