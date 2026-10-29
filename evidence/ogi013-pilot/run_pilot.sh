#!/bin/bash
# OGI-013-PILOT-1: ONE matched SINGLE vs COLLAB (mode rg2 + OGI013_ORG_COLLAB=1) episode on airline task 24 of the official tau2 benchmark: same code checkout, same task/policy/tools/seed, same pinned
# simulator model, fresh isolated organisational state per arm cloned from the same ledger snapshot. NOT EXECUTED without the owner's approval file for exactly pilot_budget.json.
# usage: PILOT_APPROVAL=/path/to/approval.txt ./run_pilot.sh        exit: 0 both arms complete | 2 refused (nothing started) | 3 halted by the budget guard | 4 simulator not executable | 5 an arm failed | 130 interrupted
# Nothing here retries or restarts: an existing run directory of the same pilot id (any state) refuses the next start. The first attempt (pilot-1, stopped by LEASE_BUDGET_EXPANSION before any inference) is preserved as evidence;
# the next attempt runs as pilot-2 (PILOT_ID) under the SAME approved budget file: its limits are keyed by arm role (pilot_guard.arm_cap).
set -u
H=$(cd "$(dirname "$0")" && pwd); CODE=$(cd "$H/../.." && pwd); B=${PILOT_BASE:-/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013}; R=$B/runs; ID=${PILOT_ID:-pilot-3}; P=$R/$ID; BUDGET="$H/pilot_budget.json"
REAL_BASE=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013
if [ -n "${PILOT_OFFLINE_TRANSPORT:-}" ]; then      # the offline provider transport exists for the end-to-end simulation only: never against the real evaluation base, which is where live inference happens
  [ -n "${PILOT_BASE:-}" ] && [ "$(cd "$PILOT_BASE" 2>/dev/null && pwd -P)" != "$(cd "$REAL_BASE" 2>/dev/null && pwd -P)" ] || { echo "PILOT_OFFLINE_TRANSPORT is only allowed with a PILOT_BASE other than the real evaluation base" >&2; exit 2; }
fi
python3 "$H/pilot_guard.py" verify-approval "$BUDGET" "${PILOT_APPROVAL:-/nonexistent}" || exit 2
[ -f "$CODE/runners/ogi013_org_collab.py" ] && [ -f "$CODE/runners/ogi013_pilot_gate.py" ] && [ -f "$CODE/runners/ogi013_lineage_heart.py" ] || { echo "code checkout $CODE lacks the collaboration module, the lineage heart or the pre-dispatch gate" >&2; exit 2; }
[ -z "$(git -C "$CODE" status --porcelain)" ] || { echo "code checkout $CODE is not clean" >&2; exit 2; }
case "$ID" in pilot-1|pilot-2) echo "$ID is a preserved failed attempt and is never reused" >&2; exit 2;; esac
[ ! -e "$P" ] || { echo "$ID already exists; it is never restarted automatically (choose a new PILOT_ID)" >&2; exit 2; }
[ ! -e "$R/PILOT_HALT" ] || { echo "stale PILOT_HALT; archive it first" >&2; exit 2; }
ROUTE="$R/$ID-task24.route"
echo '{"model_key": "gemini-3.1-flash-lite@vision"}' > "$ROUTE"                  # the SAME simulator model for both arms (seeded, not PlumMe-chosen: documented deviation of this exploratory pilot)
export PILOT_CODE="$CODE" PILOT_BASE="$B"
"$H/run_arm.sh" --verify-components > "$R/$ID-components.json" 2>&1 || { echo "components do not resolve from the canonical checkouts (see $R/pilot-1-components.json); refusing rather than installing into the shared host venv" >&2; exit 2; }
"$H/run_arm.sh" --contract "$BUDGET" "$H/pilot_guard.py" > "$R/$ID-contract.json" 2>&1 || { echo "lease-contract check failed: an execution would be refused by PlumMe's lease contract (see $R/$ID-contract.json); nothing was dispatched" >&2; exit 2; }
PRE="$R/$ID-preflight-$(date +%s)"; mkdir -p "$PRE"
"$H/run_arm.sh" --preflight "$ROUTE" "$PRE" > "$PRE/preflight.json" 2> "$PRE/preflight.err" || { echo "pinned simulator model is not executable right now (see $PRE/preflight.json); nothing was dispatched to the arms" >&2; exit 4; }
mkdir -p "$P"; : > "$P/pids"; git -C "$CODE" rev-parse HEAD > "$P/code-head.txt"; cp "$BUDGET" "$P/pilot_budget.json"; cp "$PRE/preflight.json" "$P/"
for a in single collab; do                                                      # fresh, isolated organisational state per arm, both cloned from the same slot-D snapshot
  mkdir -p "$P/slots/$a/ledgers" "$P/slots/$a/orangeme-home" "$P/$a-state"
  git clone -q --bare "$B/slots/D/ledgers/chat.git" "$P/slots/$a/ledgers/chat.git" && git clone -q --bare "$B/slots/D/ledgers/project.git" "$P/slots/$a/ledgers/project.git" || { echo "could not clone the ledger snapshot" >&2; echo "ledger clone failed" > "$P/NOT_STARTED"; exit 2; }
done
export OGI013_PILOT_BUDGET="$BUDGET" OGI013_PILOT_GUARD="$H/pilot_guard.py" OGI013_PILOT_RUNS="$R" OGI013_PILOT_ARMS="$ID/single,$ID/collab" OGI013_PILOT_START=$(date +%s)
unset OGI013_ORG_COLLAB OGI013_ORG_ECONOMY OGI013_ORG_POLICY_MODE OGI013_ORG_LEARNED_AUTHORIZED          # a stray export in the owner's shell must not skew either arm
python3 "$H/pilot_guard.py" watch "$BUDGET" "$R" "$P/pids" $ID/single $ID/collab > "$P/guard.log" 2>&1 &
GUARD=$!
CURRENT=""
report() { python3 "$H/pilot_report.py" report "$R" "$P" "$BUDGET" > "$P/report.stdout" 2> "$P/report.err"; }
interrupted() {                                                                  # keep every file, stop the running arm, say so; never restart
  echo "interrupted by $1 at $(date -u +%FT%TZ) during arm ${CURRENT:-none}" > "$P/INTERRUPTED"
  for pid in $(cat "$P/pids" 2>/dev/null); do kill -TERM -- "-$pid" 2>/dev/null || kill -TERM "$pid" 2>/dev/null; done
  [ -n "$CURRENT" ] && python3 "$H/pilot_report.py" mark "$P" "$CURRENT" end 130
  kill "$GUARD" 2>/dev/null; report; exit 130
}
trap 'interrupted TERM' TERM; trap 'interrupted INT' INT
run_arm() {                                                                      # run_arm NAME MODE [ENV=VALUE ...]
  local name=$1 mode=$2; shift 2
  CURRENT=$name
  eval "$(python3 "$H/pilot_guard.py" env "$BUDGET" "$ID/$name" | sed 's/^export OGI013_/export PILOT_/')"     # PeachMe session ceilings for this arm, from the same budget file
  env "$@" python3 "$H/pilot_report.py" mark "$P" "$name" start "$CODE" "$P/slots/$name"                                  # records the arm's launch conditions INCLUDING the flags it is about to get
  env "$@" OGI013_PILOT_ARM="$ID/$name" OGI013_ORG_STATE_DIR="$P/$name-state" setsid "$H/run_arm.sh" "$ID/$name" 24 airline "$mode" $ID-task24 "$P/slots/$name" > "$P/$name.log" 2>&1 &
  echo $! > "$P/pids"; wait $!; local rc=$?
  python3 "$H/pilot_report.py" mark "$P" "$name" end "$rc"; CURRENT=""
  return $rc
}
run_arm single single; rc=$?
if [ -e "$R/PILOT_HALT" ]; then echo "halted by the budget guard during SINGLE" >&2; kill "$GUARD" 2>/dev/null; report; exit 3; fi
if [ $rc -ne 0 ]; then echo "SINGLE arm failed (exit $rc); evidence kept, the collaboration arm was not started" >&2; kill "$GUARD" 2>/dev/null; report; exit 5; fi
run_arm collab rg2 OGI013_ORG_COLLAB=1 OGI013_ORG_POLICY_MODE=OFF; rc=$?
kill "$GUARD" 2>/dev/null
report
if [ -e "$R/PILOT_HALT" ]; then echo "halted by the budget guard during COLLAB" >&2; exit 3; fi
[ $rc -eq 0 ] || { echo "COLLAB arm failed (exit $rc); evidence kept" >&2; exit 5; }
cat "$P/report.stdout"
