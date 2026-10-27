#!/bin/bash
# usage: run1.sh OUTNAME TASK DOMAIN MODE PAIRROUTE [SLOT=A|B|C|D]  (one OrangeMe ledger slot per concurrent run)
D=/root/fruits/integration/ogi013-org; T=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/benchmarks/tau2-bench; R=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/runs; H=/root/fruits/integration/ogi013-hostpython-org/bin/python
cd $D; source /root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/env.sh; export PYTHONPATH=$D/runners:$D ORANGEME_SOURCE_REPO=$T; source $R/work.env
S=${6:-A}; O=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/slots/$S
export ORANGEME_HOME=$O/orangeme-home ORANGEME_CHAT_REPO=$O/ledgers/chat.git ORANGEME_PROJECT_REPO=$O/ledgers/project.git
# host authorization of the PeachMe accounting envelope for rg2 sessions (PlumMe still owns route eligibility; usage is recorded, not assumed): calls/tokens are an unreachable
# accounting envelope, USD 0.0 = owner order "no paid execution"
export OGI013_SESSION_MAX_CALLS=1000000 OGI013_SESSION_MAX_TOKENS=1000000000 OGI013_SESSION_MAX_COST_USD=0.0
export PLUMME_TRIAL_CREDIT=off  # owner: only genuinely free routes; trial credit is a finite allowance (set after pair 22 used 1 TRIAL_CREDIT sim call)
export OGI013_EFFECT_DB=$R/$1/effects.sqlite3 OGI013_SIM_ROUTE_FILE=$R/$5.route
exec $H runners/ogi013_host_bootstrap.py --host-python $H --tau2-checkout $T --components-root /root/fruits/integration/ogi013-org-components --runner runners/ogi013_tau2_run.py --task "$2" --domain $3 --mode $4 --out $R/$1 --host-composer ogi013_host_composer --llm-user plumme/auto
