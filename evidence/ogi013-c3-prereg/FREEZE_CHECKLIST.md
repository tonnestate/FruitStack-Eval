# c3 FREEZE checklist (FREEZE.txt is created only when every item is true; it records the commit hashes of all stack repos and this protocol)
- [ ] c2 finished, exported with the c1/c2 exporter, evaluated with the strict evaluator, results and discarded attempts archived with a sha256 manifest (unchanged interpretation)
- [x] SINGLE-E mode (offline): tests pass
- [ ] pairwise exporter (runners/export_pair_rows.py) tested
- [ ] block queue (evidence/ogi013-c3-prereg/queue) tested in DRY_RUN
- [ ] cross-process persistence of worker-behaviour memory (CherryMe) tested; knowledge reuse across processes tested
- [ ] rg2 trace report tested (real-data negative control: org-smoke t1 -> organisational_success false)
- [ ] one live RG/2 task with verified worker contributions (rg2_trace_report: organisational_success true) after c2 ends
- [ ] phase A (RANDOMIZED structure exploration) executed and trained: ORG-GATE/1 verdict recorded (H4 testable only if LEARNED_POLICY_PERMITTED_FOR_AUTHORIZED_ARM)
- [ ] k for SINGLE-E fixed from phase A and recorded; split digests (train/held-out tasks) recorded
