#!/bin/bash
# usage: block_queue.sh CAMPAIGN DOMAIN SLOT SEED TASK...
# One BLOCK per task: every condition in $CONDITIONS (space separated) back to back, in a seeded random order.
# One simulator route file per task, shared by its conditions (set in run_condition.sh).
# Whole-block discard to <campaign>/discarded/<task>-attemptK and retry (max 3) when any condition log has SIM_ROUTE_FAILED.
# env: CONDITIONS (required), RUNS_DIR, SIM_MODEL_KEY (optional, recorded in BLOCK.json), DRY_RUN=1 (passed through).
set -u
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

for T in "$@"; do
  ORDER=$(python3 -c 'import random, sys
c = sys.argv[1].split()
random.Random(f"{sys.argv[2]}|{sys.argv[3]}").shuffle(c)
print(" ".join(c))' "$CONDITIONS" "$SEED" "$T")
  BLOCK="$CDIR/$T"
  for k in 1 2 3; do
    rm -f "$RUNS_DIR/$C-$T.route"
    mkdir -p "$BLOCK"
    write_block "$BLOCK/BLOCK.json" "$T" "$ORDER" "$SEED" "$k" "${SIM_MODEL_KEY:-pending}"
    echo "$T block attempt=$k order=$ORDER slot=$S" >> "$PROG"
    for COND in $ORDER; do
      "$HERE/run_condition.sh" "$C" "$T" "$DOM" "$COND" "$S" > "$BLOCK/$COND.log" 2>&1
      echo "$T $COND attempt=$k exit=$? slot=$S" >> "$PROG"
    done
    [ -f "$RUNS_DIR/$C-$T.route" ] && cp "$RUNS_DIR/$C-$T.route" "$BLOCK/sim_route.txt"
    if [ $k -lt 3 ] && grep -q SIM_ROUTE_FAILED "$BLOCK"/*.log 2>/dev/null; then
      echo "$T discarded attempt=$k simulator route failed" >> "$PROG"
      mv "$BLOCK" "$CDIR/discarded/$T-attempt$k"
    else
      grep -q SIM_ROUTE_FAILED "$BLOCK"/*.log 2>/dev/null && echo "$T route failed after attempt $k, kept" >> "$PROG"
      break
    fi
  done
done
echo "QUEUE_DONE slot=$S" >> "$PROG"
