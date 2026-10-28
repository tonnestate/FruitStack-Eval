#!/bin/bash
# OGI-013-PILOT-1: ONE matched SINGLE vs RG2-ECONOMY episode on airline task 6, same pinned simulator model. NOT EXECUTED without the owner's approval file.
# usage: PILOT_APPROVAL=/path/to/approval.txt ./run_pilot.sh   (approval.txt = sha256 of pilot_budget.json, written by the owner)
set -u
H=$(cd "$(dirname "$0")" && pwd); B=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013; R=$B/runs; P=$R/pilot-1; ORG=/root/fruits/integration/ogi013-org
python3 "$H/pilot_guard.py" verify-approval "$H/pilot_budget.json" "${PILOT_APPROVAL:-/nonexistent}" || exit 2
[ ! -e "$P" ] || { echo "pilot-1 already exists; archive it first" >&2; exit 2; }
mkdir -p "$P"; : > "$P/pids"
for s in PILOT-SINGLE PILOT-ECON; do                                   # isolated OrangeMe ledgers, copies of slot D
  [ -d "$B/slots/D-$s/ledgers/chat.git" ] || { mkdir -p "$B/slots/D-$s/ledgers" "$B/slots/D-$s/orangeme-home"; git clone -q --bare "$B/slots/D/ledgers/chat.git" "$B/slots/D-$s/ledgers/chat.git"; git clone -q --bare "$B/slots/D/ledgers/project.git" "$B/slots/D-$s/ledgers/project.git"; }
done
echo '{"model_key": "gemini-3.1-flash-lite@vision"}' > "$R/pilot-1-task6.route"      # the SAME simulator model for both arms (seeded, not PlumMe-chosen: documented deviation of this exploratory pilot)
ARMS="single econ"
python3 "$H/pilot_guard.py" watch "$H/pilot_budget.json" "$R" "$P/pids" pilot-1/single pilot-1/econ > "$P/guard.log" 2>&1 &
GUARD=$!
cd "$ORG"
setsid "$R/run_org.sh" pilot-1/single 6 airline single pilot-1-task6 D-PILOT-SINGLE > "$P/single.log" 2>&1 &
echo $! > "$P/pids"; wait $!
[ -e "$R/PILOT_HALT" ] && { echo "halted by guard" >&2; exit 3; }
OGI013_ORG_ECONOMY=1 OGI013_ORG_POLICY_MODE=OFF OGI013_ORG_STATE_DIR="$P/econ-state" setsid "$R/run_org.sh" pilot-1/econ 6 airline rg2 pilot-1-task6 D-PILOT-ECON > "$P/econ.log" 2>&1 &
echo $! > "$P/pids"; wait $!
kill "$GUARD" 2>/dev/null
python3 "$H/pilot_guard.py" usage "$R" pilot-1/single pilot-1/econ | tee "$P/usage.json"
