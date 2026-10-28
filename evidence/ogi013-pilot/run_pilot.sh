#!/bin/bash
# OGI-013-PILOT-1: ONE matched SINGLE vs COLLAB (mode rg2 + OGI013_ORG_COLLAB=1) episode on airline task 24, same pinned simulator model, same code checkout. NOT EXECUTED without the owner's approval file.
# usage: PILOT_APPROVAL=/path/to/approval.txt ./run_pilot.sh   (approval.txt = sha256 of pilot_budget.json, written by the owner)
set -u
H=$(cd "$(dirname "$0")" && pwd); CODE=$(cd "$H/../.." && pwd); B=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013; R=$B/runs; P=$R/pilot-1
python3 "$H/pilot_guard.py" verify-approval "$H/pilot_budget.json" "${PILOT_APPROVAL:-/nonexistent}" || exit 2
[ -f "$CODE/runners/ogi013_org_collab.py" ] && [ -f "$CODE/runners/ogi013_pilot_gate.py" ] || { echo "code checkout $CODE lacks the collaboration module or the pre-dispatch gate" >&2; exit 2; }
[ -z "$(git -C "$CODE" status --porcelain)" ] || { echo "code checkout $CODE is not clean" >&2; exit 2; }
[ ! -e "$P" ] || { echo "pilot-1 already exists; archive it first" >&2; exit 2; }
[ ! -e "$R/PILOT_HALT" ] || { echo "stale PILOT_HALT; archive it first" >&2; exit 2; }
mkdir -p "$P"; : > "$P/pids"; git -C "$CODE" rev-parse HEAD > "$P/code-head.txt"
for s in PILOT-SINGLE PILOT-COLLAB; do                                 # isolated OrangeMe ledgers, copies of slot D
  [ -d "$B/slots/D-$s/ledgers/chat.git" ] || { mkdir -p "$B/slots/D-$s/ledgers" "$B/slots/D-$s/orangeme-home"; git clone -q --bare "$B/slots/D/ledgers/chat.git" "$B/slots/D-$s/ledgers/chat.git"; git clone -q --bare "$B/slots/D/ledgers/project.git" "$B/slots/D-$s/ledgers/project.git"; }
done
echo '{"model_key": "gemini-3.1-flash-lite@vision"}' > "$R/pilot-1-task24.route"      # the SAME simulator model for both arms (seeded, not PlumMe-chosen: documented deviation of this exploratory pilot)
export PILOT_CODE="$CODE" OGI013_PILOT_BUDGET="$H/pilot_budget.json" OGI013_PILOT_GUARD="$H/pilot_guard.py" OGI013_PILOT_RUNS="$R" OGI013_PILOT_ARMS="pilot-1/single,pilot-1/collab" OGI013_PILOT_START=$(date +%s)
python3 "$H/pilot_guard.py" watch "$H/pilot_budget.json" "$R" "$P/pids" pilot-1/single pilot-1/collab > "$P/guard.log" 2>&1 &
GUARD=$!
OGI013_PILOT_ARM=pilot-1/single setsid "$H/run_arm.sh" pilot-1/single 24 airline single pilot-1-task24 D-PILOT-SINGLE > "$P/single.log" 2>&1 &
echo $! > "$P/pids"; wait $!
[ -e "$R/PILOT_HALT" ] && { echo "halted by guard" >&2; kill "$GUARD" 2>/dev/null; exit 3; }
OGI013_PILOT_ARM=pilot-1/collab OGI013_ORG_COLLAB=1 OGI013_ORG_POLICY_MODE=OFF OGI013_ORG_STATE_DIR="$P/collab-state" setsid "$H/run_arm.sh" pilot-1/collab 24 airline rg2 pilot-1-task24 D-PILOT-COLLAB > "$P/collab.log" 2>&1 &
echo $! > "$P/pids"; wait $!
kill "$GUARD" 2>/dev/null
[ -e "$R/PILOT_HALT" ] && { echo "halted by guard" >&2; exit 3; }
grep -qh '"event": "ORG_COLLAB"' "$R"/pilot-1/collab/tasks/*/fruitstack-events.jsonl 2>/dev/null && echo "COLLAB path active: yes" | tee "$P/collab-path.txt" || { echo "COLLAB path active: NO (no collaboration review took place: the arm tested nothing)" | tee "$P/collab-path.txt" >&2; }
python3 "$H/pilot_guard.py" usage "$R" pilot-1/single pilot-1/collab | tee "$P/usage.json"
