#!/bin/bash
# usage: block_queue.sh CAMPAIGN DOMAIN SLOT SEED TASK...
# One BLOCK per task: every condition in $CONDITIONS (space separated) back to back, in a seeded random order.
# One simulator route file per task, shared by its conditions (set in run_condition.sh).
# Whole-block discard to <campaign>/discarded/<task>-attemptK and retry (max 3) when any condition log has SIM_ROUTE_FAILED.
# env: CONDITIONS (required), RUNS_DIR, SIM_MODEL_KEY (optional, recorded in BLOCK.json), DRY_RUN=1 (passed through).
set -u
# A live run must name its runs directory explicitly (the default location also holds the historical c1/c2 evidence); DRY_RUN may use the default.
if [ -z "${RUNS_DIR:-}" ] && [ "${DRY_RUN:-0}" != "1" ]; then echo "RUNS_DIR must be set explicitly for a live run" >&2; exit 2; fi
RUNS_DIR=${RUNS_DIR:-/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/runs}
HERE=$(cd "$(dirname "$0")" && pwd)
C=${1:?campaign}; DOM=${2:?domain}; S=${3:?slot}; SEED=${4:?seed}; shift 4
[ $# -gt 0 ] || { echo "no tasks given" >&2; exit 2; }
case "$C" in c1-*|c2-*) echo "refusing historical campaign $C" >&2; exit 2 ;; esac
: "${CONDITIONS:?set CONDITIONS to a space-separated list}"
export RUNS_DIR
CDIR="$RUNS_DIR/$C"; PROG="$CDIR/progress.txt"
mkdir -p "$CDIR/discarded"

write_block() {  # path task order seed attempt simkey
  python3 - "$@" <<'PY'
import datetime, json, sys
p, t, order, seed, k, sk = sys.argv[1:7]
json.dump({"task": t, "condition_order": order.split(), "seed": seed, "attempt": int(k),
           "sim_model_key": sk, "started_at": datetime.datetime.now(datetime.timezone.utc).isoformat()},
          open(p, "w"), indent=2)
PY
}

# Persistent organisational state (shared across the tasks of one arm) is snapshotted before every block and restored when the block is discarded, so a discarded block
# leaves no trace in knowledge/claims/training rows and the retry sees exactly the state the first attempt saw.
snapshot_state() {  # task
  rm -rf "$CDIR/.snap-$1"; mkdir -p "$CDIR/.snap-$1"
  [ -d "$CDIR/state" ] && cp -a "$CDIR/state" "$CDIR/.snap-$1/state"
  return 0
}
restore_state() {  # task
  rm -rf "$CDIR/state"
  [ -d "$CDIR/.snap-$1/state" ] && cp -a "$CDIR/.snap-$1/state" "$CDIR/state"
  return 0
}
record_sim_key() {  # block-dir ; the pinned simulator model is only known after the first simulator call wrote the route file
  [ -f "$1/sim_route.txt" ] && python3 - "$1" <<'PY'
import json, pathlib, sys
b = pathlib.Path(sys.argv[1]); meta = json.loads((b / "BLOCK.json").read_text())
try: meta["sim_model_key"] = json.loads((b / "sim_route.txt").read_text()).get("model_key") or meta["sim_model_key"]
except ValueError: pass
(b / "BLOCK.json").write_text(json.dumps(meta, indent=2))
PY
  return 0
}

for T in "$@"; do
  ORDER=$(python3 -c 'import random, sys
c = sys.argv[1].split()
random.Random(f"{sys.argv[2]}|{sys.argv[3]}").shuffle(c)
print(" ".join(c))' "$CONDITIONS" "$SEED" "$T")
  BLOCK="$CDIR/$T"
  for k in 1 2 3; do
    rm -f "$RUNS_DIR/$C-$T.route"
    snapshot_state "$T"
    mkdir -p "$BLOCK"
    write_block "$BLOCK/BLOCK.json" "$T" "$ORDER" "$SEED" "$k" "${SIM_MODEL_KEY:-pending}"
    echo "$T block attempt=$k order=$ORDER slot=$S" >> "$PROG"
    for COND in $ORDER; do
      "$HERE/run_condition.sh" "$C" "$T" "$DOM" "$COND" "$S" > "$BLOCK/$COND.log" 2>&1
      echo "$T $COND attempt=$k exit=$? slot=$S" >> "$PROG"
    done
    [ -f "$RUNS_DIR/$C-$T.route" ] && cp "$RUNS_DIR/$C-$T.route" "$BLOCK/sim_route.txt"
    record_sim_key "$BLOCK"
    if [ $k -lt 3 ] && grep -q SIM_ROUTE_FAILED "$BLOCK"/*.log 2>/dev/null; then
      echo "$T discarded attempt=$k simulator route failed" >> "$PROG"
      mv "$BLOCK" "$CDIR/discarded/$T-attempt$k"
      restore_state "$T"
    else
      grep -q SIM_ROUTE_FAILED "$BLOCK"/*.log 2>/dev/null && echo "$T route failed after attempt $k, kept" >> "$PROG"
      break
    fi
  done
  rm -rf "$CDIR/.snap-$T"
done
echo "QUEUE_DONE slot=$S" >> "$PROG"
