#!/bin/bash
# OGI-013 post-c2 supervisor: runs RUNBOOK.md steps 1-7 in order, idempotent (stage markers), restart-safe (systemd Restart=on-failure).
# It never touches c2 (read-only until all three QUEUE_DONE lines exist) and never starts a stage whose prerequisite is not true.
# Exit 0 = pipeline finished OR halted on a recorded BLOCKED reason (status.txt); exit 1 = crash, systemd restarts and the stage resumes.
set -u -o pipefail
R=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/runs; O=/root/fruits/integration/ogi013-org; EV=$O/evidence
SUP=$R/supervisor; ST=$SUP/stages; LOG=$SUP/supervisor.log; mkdir -p "$ST"
PY=/root/fruits/integration/ogi013-hostpython-org/bin/python; KPY=/root/SUPPLY-001/venv3.12/bin/python
P=$EV/ogi013-c3-prereg; Q=$P/queue; export RUNS_DIR=$R
log() { echo "$(date -u +%FT%TZ) $*" | tee -a "$LOG"; }
status() { echo "$(date -u +%FT%TZ) $*" > "$SUP/status.txt"; log "STATUS $*"; }
done_() { [ -f "$ST/$1.done" ]; }
mark() { date -u +%FT%TZ > "$ST/$1.done"; }
halt() { status "BLOCKED $1: $2"; exit 0; }

# The evaluator's --require-complete also demands COMPLETE RESOURCE USAGE (cost is unknown on free/credit routes), so its exit code 1 is a finding, not an execution failure
# (c1 had missing usage for 20/20 pairs). Run the evaluator without the flag; record the strict verdict next to the result; fail only if no valid result was produced.
compare_recorded() {  # rows out
  (cd /root/fruits/integration/ogi013-fse && "$PY" -m fruitstack_eval.cli ogi13 compare --observations "$1" > "$2" 2> "$2.err") || return 1
  "$PY" -c 'import json,sys; j=json.load(open(sys.argv[1])); assert "paired_tasks" in j and "complete_pairs_only" in j' "$2" || return 1
  (cd /root/fruits/integration/ogi013-fse && "$PY" -m fruitstack_eval.cli ogi13 compare --observations "$1" --require-complete > /dev/null 2>&1; echo "strict_require_complete_rc=$?" > "$2.strict")
  log "compare $(basename "$2"): $(cat "$2.strict") $("$PY" -c 'import json,sys; j=json.load(open(sys.argv[1])); print("paired=%s incomplete_grade=%s confounded=%s unmatched=%s" % (j["paired_tasks"], len(j["incomplete_grade_tasks"]), len(j["confounded_tasks"]), len(j["unmatched_tasks"])))' "$2")"
}
stage_wait_c2() {
  while [ "$(grep -c QUEUE_DONE "$R/c2-airline-test/progress.txt" 2>/dev/null)" != 3 ]; do
    status "WAITING_C2 queues_done=$(grep -c QUEUE_DONE "$R/c2-airline-test/progress.txt" 2>/dev/null) results=$(ls "$R"/c2-airline-test/*-fixed/tasks 2>/dev/null | wc -l)"; sleep 120
  done
}
stage_c2_eval() {  # RUNBOOK 2: unchanged interpretation, read-only on c2
  local C=$R/c2-airline-test D=$EV/ogi013-c2-airline-test S=$EV/ogi013-c1-airline-test
  mkdir -p "$D" || return 1
  cd "$O" && "$PY" "$R/export_rows.py" "$C" --out "$D/rows.jsonl" > "$D/export.log" 2>&1 || return 1
  compare_recorded "$D/rows.jsonl" "$D/compare.json" || return 1
  cd "$D" || return 1   # the c1 evidence scripts read their inputs from the current directory
  "$PY" "$S/classify_failures.py" "$C" "$D/failure_table.json" > "$D/classify.txt" 2>&1 || log "classify_failures failed (descriptive evidence only)"
  local CP=/root/fruits/integration/ogi013-org-components; PYTHONPATH="$CP/CherryMe:$CP/AppleMe/src:$CP/PlumMe/src" "$PY" "$S/replay_assurance.py" "$C" "$D/replay_assurance.json" > "$D/replay.txt" 2>&1 || log "replay_assurance failed (cause attribution limited)"
  "$PY" "$S/attribute_causes.py" "$C" > "$D/cause_attribution.txt" 2>&1 || log "attribute_causes failed: the c1 scripts assume every arm has an official result (c2 has gaps); descriptive evidence only"
  "$PY" "$S/integrity.py" "$C" > "$D/integrity.txt" 2>&1 || return 1
  (cd "$R" && find c2-airline-test -type f -print0 | sort -z | xargs -0 sha256sum > "$D/c2-airline-test.SHA256SUMS")
  cp "$C/progress.txt" "$D/progress.txt" || return 1
}
# Fixed c1/c2 protocol: 20 airline test IDs. Never select phase-A tasks by c2
# directories, as infrastructure failures could otherwise silently change the cohort.
airline_tasks() { printf '%s\n' '2 6 8 13 16 18 19 22 24 25 26 29 30 31 32 35 37 44 45 48'; }
validate_airline_cohort() {
  local task actual expected
  expected="$(airline_tasks)"
  actual="$(find "$R/c2-airline-test" -mindepth 1 -maxdepth 1 -type d -name '*-fixed' -printf '%f\n' | sed 's/-fixed$//' | sort -n | tr '\n' ' ')" || return 1
  # Compare sets, not whitespace formatting.
  [ "$(echo "$actual" | xargs)" = "$expected" ] || { log "c2 airline cohort differs from 20 preregistered IDs: actual=$actual"; return 1; }
  # Missing c2 official results are an infrastructure finding about c2 (c2 is never rerun): RECORDED and reported; they cannot shrink c3, whose cohort is the pinned list.
  : > "$SUP/c2_missing_official_results.txt"
  for task in $expected; do
    [ -s "$R/c2-airline-test/$task-fixed/tasks/$task/official-result.json" ] || echo "$task-fixed" >> "$SUP/c2_missing_official_results.txt"
    [ -s "$R/c2-airline-test/$task-adaptive/tasks/$task/official-result.json" ] || echo "$task-adaptive" >> "$SUP/c2_missing_official_results.txt"
  done
  [ ! -s "$SUP/c2_missing_official_results.txt" ] || log "c2 arms without official result (infrastructure, recorded): $(wc -l < "$SUP/c2_missing_official_results.txt")"
}
retail_side() {  # train|test (held-out) per plumme.keras_data.task_group(seed 1013, holdout 0.3)
  "$KPY" - "$1" "$R/retail_test_tasks.txt" <<'PY'
import hashlib, sys
want = sys.argv[1]
for t in open(sys.argv[2]).read().splitlines()[1].split():
    g = int(hashlib.sha256(f"1013|{t}".encode()).hexdigest()[:12], 16) / float(16 ** 12)
    if ("test" if g < 0.3 else "train") == want: print(t, end=" ")
PY
}
stage_prereg() {  # Seal the already-committed protocol/split BEFORE demo and any c3 data.
  validate_airline_cohort || return 1
  local lock="$P/PREREG_LOCK.txt" ph th
  [ -s "$P/PROTOCOL.md" ] && [ -s "$R/retail_test_tasks.txt" ] || return 1
  ph=$(sha256sum "$P/PROTOCOL.md" | cut -d' ' -f1) || return 1
  th=$(sha256sum "$R/retail_test_tasks.txt" | cut -d' ' -f1) || return 1
  if [ -f "$lock" ]; then
    grep -Fxq "protocol_sha256=$ph" "$lock" &&
      grep -Fxq "retail_task_split_sha256=$th" "$lock"
    return $?
  fi
  [ ! -e "$R/c3-phaseA/progress.txt" ] && [ ! -e "$R/c3-phaseB/progress.txt" ] || return 1
  git -C "$O" diff --quiet HEAD -- evidence/ogi013-c3-prereg/PROTOCOL.md || return 1
  {
    echo "protocol_sha256=$ph"
    echo "retail_task_split_sha256=$th"
    echo "protocol_commit=$(git -C "$O" rev-parse HEAD)"
    echo "sealed_at=$(date -u +%FT%TZ)"
  } > "$lock" || return 1
  log "c3 preregistration locked before experimental execution"
}

run_demo_once() {  # Never silently accept a failed subprocess. A discarded attempt is archived (never deleted) and the shared organisational state is restored to its pre-attempt content.
  local k rc ts ST="$R/org-demo/state" SNAP="$R/org-demo/.snap-$1"
  for k in 1 2 3; do
    [ ! -e "$R/org-demo/$1" ] || return 1          # a previous attempt directory must already have been archived
    rm -rf "$SNAP"; mkdir -p "$R/org-demo" || return 1
    if [ -d "$ST" ]; then cp -a "$ST" "$SNAP" || return 1; else mkdir -p "$SNAP" || return 1; fi
    OGI013_ORG_STATE_DIR=$ST OGI013_ORG_POLICY_MODE=OFF "$R/run_org.sh" "org-demo/$1" "$2" airline rg2 "org-demo-$1" D > "$R/org-demo/$1.log" 2>&1
    rc=$?
    if [ "$rc" -eq 0 ] && [ -s "$R/org-demo/$1/tasks/$2/official-result.json" ] && ! grep -q SIM_ROUTE_FAILED "$R/org-demo/$1.log"; then
      rm -rf "$SNAP"; return 0                      # success: the state persists into the next demo run (intended)
    fi
    ts=$(date -u +%Y%m%dT%H%M%SZ)
    log "demo $1 attempt $k not validated (rc=$rc), archived as $1-discarded-$ts, state restored"
    mv "$R/org-demo/$1" "$R/org-demo/$1-discarded-$ts" || return 1
    mv "$R/org-demo/$1.log" "$R/org-demo/$1-discarded-$ts.log" || return 1
    if [ -d "$ST" ]; then mv "$ST" "$R/org-demo/state-discarded-$1-$ts" || return 1; fi
    if [ -f "$R/org-demo-$1.route" ]; then mv "$R/org-demo-$1.route" "$R/org-demo-$1.route.discarded-$ts" || return 1; fi   # the whole block is discarded: the retry selects its simulator model afresh
    if [ -d "$SNAP" ]; then mv "$SNAP" "$ST" || return 1; fi
    grep -q SIM_ROUTE_FAILED "$R/org-demo/$1-discarded-$ts.log" || return 1      # only a simulator-route failure may be retried
  done
  return 1
}
stage_demo() {  # RUNBOOK 3
  set -- $(airline_tasks); local t1=$1 t2=$2
  run_demo_once d1 "$t1" || return 1
  run_demo_once d2 "$t2" || return 1
  cd "$O" || return 1
  mkdir -p "$EV/ogi013-rg2-demo" || return 1
  for d in d1 d2; do
    "$PY" runners/rg2_trace_report.py "$R/org-demo/$d" --out "$EV/ogi013-rg2-demo/report-$d.json" > "$SUP/trace-$d.txt" 2>&1 || return 1
  done
  "$PY" - "$EV/ogi013-rg2-demo/report-d1.json" "$EV/ogi013-rg2-demo/report-d2.json" > "$SUP/demo_success.txt" <<'PY'
import json, sys
reports = [json.load(open(path)) for path in sys.argv[1:]]
def verified(r):
    return r.get("organisational_success", r.get("verdict", {}).get("organisational_success")) is True
print(any(verified(r) for r in reports))
PY
  [ "$?" -eq 0 ] || return 1
  log "demo organisational_success(either)=$(cat "$SUP/demo_success.txt")"
  [ "$(cat "$SUP/demo_success.txt")" = "True" ] || halt demo "no verified multi-agent contribution; preventing Phase A and Keras training"
}
pending() {  # A directory is NOT evidence of completion. Require an explicit validated BLOCK_DONE.
  local C=$1 t; shift
  for t in "$@"; do
    if [ -f "$C/$t/BLOCK_DONE" ]; then continue; fi
    if [ -d "$C/.snap-$t" ]; then
      mkdir -p "$C/discarded" || return 1
      if [ -d "$C/$t" ]; then mv "$C/$t" "$C/discarded/$t-interrupted$(date +%s)" || return 1; fi
      rm -rf "$C/state"
      [ ! -d "$C/.snap-$t/state" ] || cp -a "$C/.snap-$t/state" "$C/state" || return 1
      rm -rf "$C/.snap-$t"
    elif [ -d "$C/$t" ]; then
      mkdir -p "$C/discarded" || return 1
      mv "$C/$t" "$C/discarded/$t-unvalidated$(date +%s)" || return 1
    fi
    echo "$t"
  done | tr '\n' ' '
}
stage_phaseA() {  # RUNBOOK 4: domain-qualified keys, shared organisational learning store.
  stage_prereg || return 1
  local t tasks=() todo
  for t in $(airline_tasks); do tasks+=("airline:$t"); done
  for t in $(retail_side train); do tasks+=("retail:$t"); done
  [ "${#tasks[@]}" -gt 0 ] || return 1
  todo="$(pending "$R/c3-phaseA" "${tasks[@]}")" || return 1
  [ -z "$todo" ] || CONDITIONS="RG2-RANDOMIZED" "$Q/block_queue.sh" c3-phaseA mixed D 1013 $todo || return 1
}
stage_train() {
  cd "$O" && KERAS_BACKEND=jax PYTHONPATH=runners:.:/root/fruits/integration/ogi013-cherry-org:/root/fruits/integration/ogi013-plum-org/src "$KPY" runners/train_org_policy.py \
    --store "$R/c3-phaseA/state/RG2-RANDOMIZED" --gate "$EV/ogi013-learning/ORG_GATE_V1.json" --out "$R/c3-phaseA/learned" > "$SUP/train.log" 2>&1
}
stage_freeze() {  # RUNBOOK 5: locks learner and SINGLE-E k before confirmatory Phase B
  stage_prereg || return 1
  [ "$(cat "$SUP/demo_success.txt" 2>/dev/null)" = "True" ] || halt freeze "no verified multi-agent contribution (demo organisational_success != True); needs owner decision, see $SUP/trace-d1.txt"
  [ -f "$R/c3-phaseA/learned/attestation.json" ] || halt freeze "no ORG-GATE/1 attestation"
  local K; K=$("$PY" - "$O/runners" "$R/c3-phaseA/state/RG2-RANDOMIZED" <<'PY'
import statistics, sys
sys.path.insert(0, sys.argv[1])
from ogi013_org_learning import load_training_table
values = []
for row in load_training_table(sys.argv[2]):
    result = row.get("result") or {}
    dispatches = result.get("provider_dispatches")
    if row.get("eligible_for_training") and isinstance(dispatches, int) and not isinstance(dispatches, bool):
        values.append(dispatches)
print(max(1, round(statistics.median(values))) if values else "")
PY
) || return 1
  [ -n "$K" ] || halt freeze "k for SINGLE-E not derivable from phase A completion rows"
  echo "$K" > "$SUP/single_e_k.txt"
  { echo "FREEZE $(date -u +%FT%TZ) k=$K"; for r in ogi013-fse ogi013-org ogi013-cherry-org ogi013-plum-org ogi013-peach-org; do echo "$r $(git -C /root/fruits/integration/$r rev-parse HEAD)"; done
    echo "retail_train: $(retail_side train)"; echo "retail_heldout: $(retail_side test)"; echo "gate: $(cat "$R/c3-phaseA/learned/attestation.json" | tr -d '\n' | cut -c1-400)"; } > "$P/FREEZE.txt"
}
stage_phaseB() {  # RUNBOOK 6
  stage_prereg || return 1
  local conds="SINGLE SINGLE-E FIXED RG2-OFF RG2-OFF-NOPERSIST RG2-NO-TRIAGE RG2-NO-VERIFY RG2-NO-KNOWLEDGE" K; K=$(cat "$SUP/single_e_k.txt")
  if grep -q LEARNED_POLICY_PERMITTED_FOR_AUTHORIZED_ARM "$R/c3-phaseA/learned/attestation.json"; then   # PROTOCOL: owner order authorises the learner-on arm only when the gate permits
    conds="$conds RG2-LEARNED"; export OGI013_ORG_LEARNED_DIR=$R/c3-phaseA/learned OGI013_ORG_LEARNED_AUTHORIZED=1
  fi
  local todo
  todo="$(pending "$R/c3-phaseB" $(retail_side test))" || return 1
  [ -z "$todo" ] || OGI013_SINGLE_E_K=$K CONDITIONS="$conds" "$Q/block_queue.sh" c3-phaseB retail D 2026 $todo || return 1
}
stage_eval() {  # RUNBOOK 7
  stage_prereg || return 1
  local D=$EV/ogi013-c3-results; mkdir -p "$D"; cd "$O"
  for pair in "RG2-OFF SINGLE" "RG2-OFF SINGLE-E" "RG2-OFF FIXED" "RG2-OFF RG2-OFF-NOPERSIST" "RG2-LEARNED RG2-OFF"; do set -- $pair
    if [ "$1" = "RG2-LEARNED" ] && ! grep -q LEARNED_POLICY_PERMITTED_FOR_AUTHORIZED_ARM "$R/c3-phaseA/learned/attestation.json"; then
      echo "NOT_TESTABLE: learner gate did not permit this arm" > "$D/RG2-LEARNED-vs-RG2-OFF.NOT_TESTABLE"
      continue
    fi
    "$PY" runners/export_pair_rows.py --campaign "$R/c3-phaseB" --cond-a "$1" --cond-b "$2" --out "$D/rows-$1-vs-$2.jsonl" --mapping-out "$D/map-$1-vs-$2.json" > "$D/export-$1-vs-$2.log" 2>&1 || return 1
    compare_recorded "$D/rows-$1-vs-$2.jsonl" "$D/compare-$1-vs-$2.json" || return 1
  done
  local d found=0
  for d in "$R"/c3-phaseB/*/RG2-OFF; do
    [ -d "$d" ] || continue
    found=1
    "$PY" runners/rg2_trace_report.py "$d" --out "$D/trace-$(basename "$(dirname "$d")").json" > /dev/null 2>&1 || return 1
  done
  [ "$found" -eq 1 ] || return 1
}
for s in wait_c2 c2_eval prereg demo phaseA train freeze phaseB eval; do
  done_ $s && continue
  [ "$s" != phaseA ] || [ -f "$SUP/PHASE_A_RELEASE" ] || halt phaseA "held: infrastructure release marker $SUP/PHASE_A_RELEASE not set (owner order: no Phase A before a stable live simulator is demonstrated)"
  status "RUNNING $s"
  for try in 1 2 3; do "stage_$s" && { mark $s; break; }; log "stage $s failed try $try"; sleep 60; done
  done_ $s || halt "$s" "failed 3 times, see $LOG"
done
status "PIPELINE_COMPLETE"
