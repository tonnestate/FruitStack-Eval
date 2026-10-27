#!/bin/bash
# OGI-013 post-c2 supervisor: runs RUNBOOK.md steps 1-7 in order, idempotent (stage markers), restart-safe (systemd Restart=on-failure).
# It never touches c2 (read-only until all three QUEUE_DONE lines exist) and never starts a stage whose prerequisite is not true.
# Exit 0 = pipeline finished OR halted on a recorded BLOCKED reason (status.txt); exit 1 = crash, systemd restarts and the stage resumes.
set -u
R=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/runs; O=/root/fruits/integration/ogi013-org; EV=$O/evidence
SUP=$R/supervisor; ST=$SUP/stages; LOG=$SUP/supervisor.log; mkdir -p "$ST"
PY=/root/fruits/integration/ogi013-hostpython-org/bin/python; KPY=/root/SUPPLY-001/venv3.12/bin/python
P=$EV/ogi013-c3-prereg; Q=$P/queue; export RUNS_DIR=$R
log() { echo "$(date -u +%FT%TZ) $*" | tee -a "$LOG"; }
status() { echo "$(date -u +%FT%TZ) $*" > "$SUP/status.txt"; log "STATUS $*"; }
done_() { [ -f "$ST/$1.done" ]; }
mark() { date -u +%FT%TZ > "$ST/$1.done"; }
halt() { status "BLOCKED $1: $2"; exit 0; }

stage_wait_c2() {
  while [ "$(grep -c QUEUE_DONE "$R/c2-airline-test/progress.txt" 2>/dev/null)" != 3 ]; do
    status "WAITING_C2 queues_done=$(grep -c QUEUE_DONE "$R/c2-airline-test/progress.txt" 2>/dev/null) results=$(ls "$R"/c2-airline-test/*-fixed/tasks 2>/dev/null | wc -l)"; sleep 120
  done
}
stage_c2_eval() {  # RUNBOOK 2: unchanged interpretation, read-only on c2
  local C=$R/c2-airline-test D=$EV/ogi013-c2-airline-test S=$EV/ogi013-c1-airline-test
  cd "$O" && "$PY" "$R/export_rows.py" "$C" --out "$D/rows.jsonl" > "$D/export.log" 2>&1 || return 1
  (cd /root/fruits/integration/ogi013-fse && "$PY" -m fruitstack_eval.cli ogi13 compare --observations "$D/rows.jsonl" --require-complete > "$D/compare.json" 2> "$D/compare.err"); true
  "$PY" "$S/classify_failures.py" "$C" "$D/failure_table.json" > "$D/classify.txt" 2>&1
  "$PY" "$S/attribute_causes.py" "$C" > "$D/cause_attribution.txt" 2>&1
  "$PY" "$S/integrity.py" "$C" > "$D/integrity.txt" 2>&1
  (cd "$R" && find c2-airline-test -type f -print0 | sort -z | xargs -0 sha256sum > "$D/c2-airline-test.SHA256SUMS")
  cp "$C/progress.txt" "$D/progress.txt"
}
airline_tasks() { ls "$R/c2-airline-test" | grep -E '^[0-9]+-fixed$' | sed 's/-fixed//' | sort -n | tr '\n' ' '; }
retail_side() {  # train|test (held-out) per plumme.keras_data.task_group(seed 1013, holdout 0.3)
  "$KPY" - "$1" "$R/retail_test_tasks.txt" <<'PY'
import hashlib, sys
want = sys.argv[1]
for t in open(sys.argv[2]).read().splitlines()[1].split():
    g = int(hashlib.sha256(f"1013|{t}".encode()).hexdigest()[:12], 16) / float(16 ** 12)
    if ("test" if g < 0.3 else "train") == want: print(t, end=" ")
PY
}
run_demo_once() {  # $1 outname $2 task ; retry only on simulator-route failure (RUNBOOK 3)
  local k
  for k in 1 2 3; do
    rm -rf "$R/org-demo/$1"; mkdir -p "$R/org-demo"
    OGI013_ORG_STATE_DIR=$R/org-demo/state OGI013_ORG_POLICY_MODE=OFF "$R/run_org.sh" "org-demo/$1" "$2" airline rg2 "org-demo-$1" D > "$R/org-demo/$1.log" 2>&1
    grep -q SIM_ROUTE_FAILED "$R/org-demo/$1.log" || return 0
    log "demo $1 attempt $k simulator route failed, retrying"; mv "$R/org-demo/$1" "$R/org-demo/$1-discarded$k" 2>/dev/null
  done
}
stage_demo() {  # RUNBOOK 3
  set -- $(airline_tasks); local t1=$1 t2=$2
  run_demo_once d1 "$t1"; run_demo_once d2 "$t2"
  cd "$O" && for d in d1 d2; do "$PY" runners/rg2_trace_report.py "$R/org-demo/$d" --out "$EV/ogi013-rg2-demo/report-$d.json" > "$SUP/trace-$d.txt" 2>&1; done
  "$PY" -c "import json,sys;r=json.load(open('$EV/ogi013-rg2-demo/report-d1.json'));print(r.get('organisational_success') if 'organisational_success' in r else r.get('verdict',{}).get('organisational_success'))" > "$SUP/demo_success.txt" 2>&1
  log "demo organisational_success(d1)=$(cat "$SUP/demo_success.txt")"
}
pending() {  # $1 campaign dir, rest tasks -> tasks without a complete block; an interrupted block is discarded and its state snapshot restored (resume after a crash)
  local C=$1 t; shift
  for t in "$@"; do
    if [ -d "$C/.snap-$t" ]; then mkdir -p "$C/discarded"; mv "$C/$t" "$C/discarded/$t-interrupted$(date +%s)" 2>/dev/null; rm -rf "$C/state"; [ -d "$C/.snap-$t/state" ] && cp -a "$C/.snap-$t/state" "$C/state"; rm -rf "$C/.snap-$t"; echo "$t"
    elif [ ! -d "$C/$t" ]; then echo "$t"; fi
  done | tr '\n' ' '
}
stage_phaseA() {  # RUNBOOK 4
  local tasks; tasks="$(pending "$R/c3-phaseA" $(airline_tasks) $(retail_side train))"
  [ -z "$tasks" ] || CONDITIONS="RG2-RANDOMIZED" "$Q/block_queue.sh" c3-phaseA mixed D 1013 $tasks || return 1
}
stage_train() {
  cd "$O" && KERAS_BACKEND=jax PYTHONPATH=runners:.:/root/fruits/integration/ogi013-cherry-org:/root/fruits/integration/ogi013-plum-org/src "$KPY" runners/train_org_policy.py \
    --store "$R/c3-phaseA/state/RG2-RANDOMIZED" --gate "$EV/ogi013-learning/ORG_GATE_V1.json" --out "$R/c3-phaseA/learned" > "$SUP/train.log" 2>&1
}
stage_freeze() {  # RUNBOOK 5: refuses unless the prerequisites are really true
  [ "$(cat "$SUP/demo_success.txt" 2>/dev/null)" = "True" ] || halt freeze "no verified multi-agent contribution (demo organisational_success != True); needs owner decision, see $SUP/trace-d1.txt"
  [ -f "$R/c3-phaseA/learned/attestation.json" ] || halt freeze "no ORG-GATE/1 attestation"
  local K; K=$("$PY" - "$R/c3-phaseA/state/RG2-RANDOMIZED/training/decisions.jsonl" <<'PY'
import json, statistics, sys
v = []
for l in open(sys.argv[1]):
    r = json.loads(l) if l.strip() else {}
    c = r.get("result") or r
    d = c.get("provider_dispatches")
    if isinstance(d, int): v.append(d)
print(max(1, round(statistics.median(v))) if v else "")
PY
)
  [ -n "$K" ] || halt freeze "k for SINGLE-E not derivable from phase A completion rows"
  echo "$K" > "$SUP/single_e_k.txt"
  { echo "FREEZE $(date -u +%FT%TZ) k=$K"; for r in ogi013-fse ogi013-org ogi013-cherry-org ogi013-plum-org ogi013-peach-org; do echo "$r $(git -C /root/fruits/integration/$r rev-parse HEAD)"; done
    echo "retail_train: $(retail_side train)"; echo "retail_heldout: $(retail_side test)"; echo "gate: $(cat "$R/c3-phaseA/learned/attestation.json" | tr -d '\n' | cut -c1-400)"; } > "$P/FREEZE.txt"
}
stage_phaseB() {  # RUNBOOK 6
  local conds="SINGLE SINGLE-E FIXED RG2-OFF RG2-OFF-NOPERSIST RG2-NO-TRIAGE RG2-NO-VERIFY RG2-NO-KNOWLEDGE" K; K=$(cat "$SUP/single_e_k.txt")
  if grep -q LEARNED_POLICY_PERMITTED_FOR_AUTHORIZED_ARM "$R/c3-phaseA/learned/attestation.json"; then   # PROTOCOL: owner order authorises the learner-on arm only when the gate permits
    conds="$conds RG2-LEARNED"; export OGI013_ORG_LEARNED_DIR=$R/c3-phaseA/learned OGI013_ORG_LEARNED_AUTHORIZED=1
  fi
  OGI013_SINGLE_E_K=$K CONDITIONS="$conds" "$Q/block_queue.sh" c3-phaseB retail D 2026 $(pending "$R/c3-phaseB" $(retail_side test)) || return 1
}
stage_eval() {  # RUNBOOK 7
  local D=$EV/ogi013-c3-results; mkdir -p "$D"; cd "$O"
  for pair in "RG2-OFF SINGLE" "RG2-OFF SINGLE-E" "RG2-OFF FIXED" "RG2-OFF RG2-OFF-NOPERSIST" "RG2-LEARNED RG2-OFF"; do set -- $pair
    "$PY" runners/export_pair_rows.py --campaign "$R/c3-phaseB" --cond-a "$1" --cond-b "$2" --out "$D/rows-$1-vs-$2.jsonl" --mapping-out "$D/map-$1-vs-$2.json" > "$D/export-$1-vs-$2.log" 2>&1 || continue
    (cd /root/fruits/integration/ogi013-fse && "$PY" -m fruitstack_eval.cli ogi13 compare --observations "$D/rows-$1-vs-$2.jsonl" --require-complete > "$D/compare-$1-vs-$2.json" 2>&1)
  done
  for d in "$R"/c3-phaseB/*/RG2-OFF; do "$PY" runners/rg2_trace_report.py "$d" --out "$D/trace-$(basename "$(dirname "$d")").json" > /dev/null 2>&1; done
}
for s in wait_c2 c2_eval demo phaseA train freeze phaseB eval; do
  done_ $s && continue
  status "RUNNING $s"
  for try in 1 2 3; do "stage_$s" && { mark $s; break; }; log "stage $s failed try $try"; sleep 60; done
  done_ $s || halt "$s" "failed 3 times, see $LOG"
done
status "PIPELINE_COMPLETE"
