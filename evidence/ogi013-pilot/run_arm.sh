#!/bin/bash
# Pilot arm launcher: identical to ogi-013/runs/run_org.sh EXCEPT that the code checkout is PILOT_CODE (this repository's worktree) instead of the shared ogi013-org worktree, which has no
# collaboration module, and that the OrangeMe ledger slot is a directory of its own. Both modes go through the same bootstrap (pinned components, same host python).
# usage: PILOT_CODE=<checkout> run_arm.sh OUTNAME TASK DOMAIN MODE PAIRROUTE SLOT_DIR
#        PILOT_CODE=<checkout> run_arm.sh --preflight ROUTE_FILE STATE_DIR        (simulator preflight, no inference)
#        PILOT_CODE=<checkout> run_arm.sh --contract BUDGET_FILE PILOT_GUARD_PY    (offline lease-contract check, no inference)
#        PILOT_CODE=<checkout> run_arm.sh --verify-components                      (read-only: every component resolves from the canonical checkout, nothing would be installed)
PD=${PILOT_CODE:?PILOT_CODE is required}; B=${PILOT_BASE:-/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013}; T=$B/benchmarks/tau2-bench; R=$B/runs; H=${PILOT_HOSTPY:-/root/fruits/integration/ogi013-hostpython-org/bin/python}
cd "$PD" || exit 2; source $B/env.sh; CR=${PILOT_COMPONENTS:-/root/fruits/integration/ogi013-org-components}
# The canonical component sources go FIRST on the path (they win over the shared venv's editable installs), so the bootstrap's own check passes and NO `pip install -e` ever touches the shared host venv,
# and both arms run exactly these sources (their heads are logged by the bootstrap as OGI013_SOURCE lines).
export PYTHONPATH=${PILOT_OFFLINE_TRANSPORT:+$PILOT_OFFLINE_TRANSPORT:}$PD/runners:$PD:$CR/CherryMe:$CR/PeachMe/src:$CR/PlumMe/src:$CR/AppleMe/src:$CR/MangoMe/src:$CR/OrangeMe/src:$CR/PomeloMe/src ORANGEME_SOURCE_REPO=$T; source $R/work.env
BOOT="$H runners/ogi013_host_bootstrap.py --host-python $H --tau2-checkout $T --components-root $CR"
if [ "${1:-}" = "--verify-components" ]; then
  [ -n "${PILOT_DRY_RUN:-}" ] && { echo "COMMAND=$H $PD/evidence/ogi013-pilot/verify_components.py $CR $T"; exit 0; }
  exec $H "$PD/evidence/ogi013-pilot/verify_components.py" "$CR" "$T"
fi
if [ "${1:-}" = "--contract" ]; then                                         # offline: would PlumMe's lease contract refuse any execution the arms will make? (no service, no network, no inference)
  [ -n "${PILOT_DRY_RUN:-}" ] && { echo "COMMAND=$BOOT --runner $PD/evidence/ogi013-pilot/sim_preflight.py --contract $2 $3"; exit 0; }
  exec $BOOT --runner "$PD/evidence/ogi013-pilot/sim_preflight.py" --contract "$2" "$3"
fi
if [ "${1:-}" = "--preflight" ]; then
  [ -n "${PILOT_DRY_RUN:-}" ] && { echo "COMMAND=$BOOT --runner $PD/evidence/ogi013-pilot/sim_preflight.py $2 $3"; exit 0; }
  exec $BOOT --runner "$PD/evidence/ogi013-pilot/sim_preflight.py" "$2" "$3"
fi
O=$6
export ORANGEME_HOME=$O/orangeme-home ORANGEME_CHAT_REPO=$O/ledgers/chat.git ORANGEME_PROJECT_REPO=$O/ledgers/project.git
unset PLUMME_TRIAL_CREDIT PLUMME_ZERO_CHARGE_DISPATCH                      # as run_org.sh: budget-aware AUTO over all authorized supply; no cost-class restriction and no model restriction is set here
[ -f "$R/host_budget.env" ] && source "$R/host_budget.env"                 # (the pilot's own session ceilings below are exported by run_pilot.sh AFTER this and win)
export OGI013_SESSION_MAX_CALLS=${PILOT_SESSION_MAX_CALLS:-$OGI013_SESSION_MAX_CALLS} OGI013_SESSION_MAX_TOKENS=${PILOT_SESSION_MAX_TOKENS:-$OGI013_SESSION_MAX_TOKENS} OGI013_SESSION_MAX_COST_USD=${PILOT_SESSION_MAX_COST_USD:-$OGI013_SESSION_MAX_COST_USD}
export OGI013_EFFECT_DB=$R/$1/effects.sqlite3 OGI013_SIM_ROUTE_FILE=$R/$5.route
CMD="$BOOT --runner runners/ogi013_tau2_run.py --task $2 --domain $3 --mode $4 --out $R/$1 --host-composer ogi013_host_composer --llm-user plumme/auto"
if [ -n "${PILOT_DRY_RUN:-}" ]; then                                         # print what WOULD run (no secrets, nothing executed): the exact command and the variables that decide the arm
  echo "CODE=$PD"; echo "COMMAND=$CMD"; for v in PYTHONPATH OGI013_SIM_ROUTE_FILE OGI013_EFFECT_DB OGI013_SESSION_MAX_CALLS OGI013_SESSION_MAX_TOKENS OGI013_SESSION_MAX_COST_USD ORANGEME_CHAT_REPO ORANGEME_PROJECT_REPO \
    OGI013_ORG_COLLAB OGI013_ORG_POLICY_MODE OGI013_ORG_STATE_DIR OGI013_PILOT_ARM OGI013_PILOT_BUDGET PLUMME_ZERO_CHARGE_DISPATCH PLUMME_TRIAL_CREDIT; do echo "$v=${!v-<unset>}"; done; exit 0
fi
exec $CMD
