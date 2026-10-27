#!/bin/bash
# usage: run1.sh OUTNAME TASK DOMAIN MODE PAIRROUTE [SLOT=A|B|C|D]  (one OrangeMe ledger slot per concurrent run)
D=/root/fruits/integration/ogi013-org; T=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/benchmarks/tau2-bench; R=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/runs; H=/root/fruits/integration/ogi013-hostpython-org/bin/python
cd $D; source /root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/env.sh; export PYTHONPATH=$D/runners:$D ORANGEME_SOURCE_REPO=$T; source $R/work.env
S=${6:-A}; O=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/slots/$S
export ORANGEME_HOME=$O/orangeme-home ORANGEME_CHAT_REPO=$O/ledgers/chat.git ORANGEME_PROJECT_REPO=$O/ledgers/project.git
# PlumMe runs budget-aware AUTO over ALL eligible, authorized supply (free tiers, trial credit, included/prepaid entitlements, paid routes inside the host-approved budget).
# env.sh carries c1/c2 recorded conditions (PLUMME_ZERO_CHARGE_DISPATCH); they are NOT part of AUTO and are removed for rg2. No cost-class restriction is set here.
unset PLUMME_TRIAL_CREDIT PLUMME_ZERO_CHARGE_DISPATCH
# The host-approved session budget is an owner input (PeachMe needs a configured envelope for child-call accounting): $R/host_budget.env must define
# OGI013_SESSION_MAX_CALLS, OGI013_SESSION_MAX_TOKENS, OGI013_SESSION_MAX_COST_USD. No defaults are invented here.
[ -f "$R/host_budget.env" ] || { echo "HOST_BUDGET_REQUIRED: owner must provide $R/host_budget.env" >&2; exit 2; }
source "$R/host_budget.env"
: "${OGI013_SESSION_MAX_CALLS:?}" "${OGI013_SESSION_MAX_TOKENS:?}" "${OGI013_SESSION_MAX_COST_USD:?}"
export OGI013_SESSION_MAX_CALLS OGI013_SESSION_MAX_TOKENS OGI013_SESSION_MAX_COST_USD
export OGI013_EFFECT_DB=$R/$1/effects.sqlite3 OGI013_SIM_ROUTE_FILE=$R/$5.route
exec $H runners/ogi013_host_bootstrap.py --host-python $H --tau2-checkout $T --components-root /root/fruits/integration/ogi013-org-components --runner runners/ogi013_tau2_run.py --task "$2" --domain $3 --mode $4 --out $R/$1 --host-composer ogi013_host_composer --llm-user plumme/auto
