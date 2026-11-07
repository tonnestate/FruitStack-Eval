# OGI-013 post-c2 runbook (exact order; nothing here may run while c2 is running: shared provider supply)
Environment common to all steps: R=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/runs ; stack worktrees ogi013-org (FSE ogi013-org-bridge), ogi013-cherry-org, ogi013-plum-org, ogi013-peach-org via
/root/fruits/integration/ogi013-org-components ; venv /root/fruits/integration/ogi013-hostpython-org ; trainer venv /root/SUPPLY-001/venv3.12 ; launcher $R/run_org.sh (PlumMe AUTO, no cost-class filter;
optional $R/host_budget.env is the OWNER's approved ceilings - absent means no cash authorised, credit/free/included capacity still usable).

1. Detect c2 end: all three `QUEUE_DONE` lines in $R/c2-airline-test/progress.txt. Do not modify c2. After c2 evaluation, the supervisor must seal the pre-existing committed protocol and task split in PREREG_LOCK.txt BEFORE any c3 exploratory run. FREEZE.txt later seals learned/gate details and SINGLE-E k before confirmatory Phase B.
2. c2 evaluation (unchanged interpretation): `python3 $R/export_rows.py $R/c2-airline-test > rows.jsonl` (as for c1), `cd ogi013-fse && python -m fruitstack_eval.cli ogi13 compare --observations rows.jsonl --require-complete`,
   run evidence scripts classify_failures.py / attribute_causes.py / integrity.py (evidence/ogi013-c1-airline-test) with the c2 path, sha256 manifest of the whole c2 dir (find ... sha256sum), copy small results to
   evidence/ogi013-c2-airline-test/. Cause attribution for c2 compares reflex-block rate with c1 (instrument-fix question only).
3. Live RG/2 demonstration (single task, slot D): `$R/run_org.sh org-demo/d1 <task> airline rg2 org-demo-1 D` with OGI013_ORG_STATE_DIR=$R/org-demo/state OGI013_ORG_POLICY_MODE=OFF ; retry on SIM_ROUTE_FAILED
   (whole run). Second related task with the SAME state dir for the persistence check. Evaluate: `python runners/rg2_trace_report.py $R/org-demo/d1 --out report.json` -> organisational_success must be true to
   count (otherwise report the failure codes; do not repeat to cherry-pick, except simulator-route failures).
4. Phase A (structure exploration): block_queue with CONDITIONS="RG2-RANDOMIZED" over the registered phase-A tasks; each episode's official grade is attributed automatically (ogi013_tau2_run end hook ->
   training/outcomes.jsonl + PlumMe DecisionLog feedback). Train: `KERAS_BACKEND=jax PYTHONPATH=runners:.:<cherry-org>:<plum-org>/src /root/SUPPLY-001/venv3.12/bin/python runners/train_org_policy.py --store <arm state dir>
   --gate evidence/ogi013-learning/ORG_GATE_V1.json --out <weights dir>` -> attestation.json verdict recorded verbatim.
5. Fix k for SINGLE-E = integer median provider_dispatches per decision (training/decisions.jsonl completion rows) ; record it. Create FREEZE.txt (all checklist boxes true, commit hashes of all repos, split digests). Only then:
6. Phase B (confirmatory): block_queue.sh with CONDITIONS per PROTOCOL.md on the held-out tasks, explicit RUNS_DIR, OGI013_SINGLE_E_K set, LEARNED only if the verdict permits AND the owner authorises
   (OGI013_ORG_LEARNED_AUTHORIZED=1 for that condition only).
7. Evaluate: runners/export_pair_rows.py per registered pair -> `fse ogi13 compare ... --require-complete` ; exact McNemar/Holm per PROTOCOL.md; rg2_trace_report per RG2 run for contribution/causal evidence; fse seal create + logcheck --expect-cost-policy AUTO.
8. Report positive AND negative results without reinterpretation; list every limitation (episode-level credit, small n, AUTO supply drift, recovery not persisted, no standby pool).
