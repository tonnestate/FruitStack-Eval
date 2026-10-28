#!/bin/bash
# Pilot arm launcher: identical to ogi-013/runs/run_org.sh EXCEPT that the code checkout is PILOT_CODE (this repository's worktree) instead of the shared ogi013-org worktree,
# which has no collaboration module. usage: PILOT_CODE=<checkout> run_arm.sh OUTNAME TASK DOMAIN MODE PAIRROUTE SLOT
D=${PILOT_CODE:?PILOT_CODE is required}; B=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013; T=$B/benchmarks/tau2-bench; R=$B/runs; H=/root/fruits/integration/ogi013-hostpython-org
cd "$D" || exit 2; source $B/env.sh; export PYTHONPATH=$D/runners:$D ORANGEME_SOURCE_REPO=$T; source $R/work.env
S=$6; O=$B/slots/$S
export ORANGEME_HOME=$O/orangeme-home ORANGEME_CHAT_REPO=$O/ledgers/chat.git ORANGEME_PROJECT_REPO=$O/ledgers/project.git
unset PLUMME_TRIAL_CREDIT PLUMME_ZERO_CHARGE_DISPATCH                      # as run_org.sh: budget-aware AUTO over all authorized supply; no cost-class restriction is set here
[ -f "$R/host_budget.env" ] && source "$R/host_budget.env"
export OGI013_SESSION_MAX_CALLS OGI013_SESSION_MAX_TOKENS OGI013_SESSION_MAX_COST_USD
export OGI013_EFFECT_DB=$R/$1/effects.sqlite3 OGI013_SIM_ROUTE_FILE=$R/$5.route
exec $H runners/ogi013_host_bootstrap.py --host-python $H --tau2-checkout $T --components-root /root/fruits/integration/ogi013-org-components --runner runners/ogi013_tau2_run.py --task "$2" --domain $3 --mode $4 --out $R/$1 --host-composer ogi013_host_composer --llm-user plumme/auto
