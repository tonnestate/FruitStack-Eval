#!/bin/bash
# FruitStack arm on the frozen single coding task (same bootstrap as evidence/ogi013-pilot/run_arm.sh, but the runner is runners/ogi013_code_task.py).
# usage: run_code_arm.sh MODE(single|rg2|single_e) OUTDIR WORKDIR      (OUTDIR must not exist; WORKDIR is a fresh copy of the frozen base checkout)
set -e
MODE=$1; OUT=$2; WORK=$3
PD=/root/fruits/integration/ogi013-collab-proof; B=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013-collab1; T=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/benchmarks/tau2-bench
R=$B/runs; H=/root/fruits/integration/ogi013-hostpython-org/bin/python; CR=/root/fruits/integration/ogi013-org-components
TASKDIR=/root/fruits/research/OGI013-SINGLE-TASK
cd "$PD"; source $B/env.sh
export PYTHONPATH=$PD/runners:$PD:$CR/CherryMe:$CR/PeachMe/src:$CR/PlumMe/src:$CR/AppleMe/src:$CR/MangoMe/src:$CR/OrangeMe/src:$CR/PomeloMe/src ORANGEME_SOURCE_REPO=$T
source $R/work.env
mkdir -p "$OUT/ledgers"
for n in chat project; do git clone -q --bare $B/slots/D/ledgers/$n.git $OUT/ledgers/$n.git; done
mkdir -p $OUT/orangeme-home
export ORANGEME_HOME=$OUT/orangeme-home ORANGEME_CHAT_REPO=$OUT/ledgers/chat.git ORANGEME_PROJECT_REPO=$OUT/ledgers/project.git
unset PLUMME_TRIAL_CREDIT PLUMME_ZERO_CHARGE_DISPATCH
set -a; source /root/.plumme/runtime.env >/dev/null 2>&1; set +a      # FLM_KEY (computed at source time) + the isolated FreeLLMAPI base URL; the cost policy stays as env.sh set it
export PLUMME_COST_POLICY=ANY PLUMME_SHARED_HEALTH_DIR=$R OGI013_PILOT_RUNS=$R
export OGI013_SESSION_MAX_CALLS=110 OGI013_SESSION_MAX_TOKENS=200000 OGI013_SESSION_MAX_COST_USD=0
export OGI013_EFFECT_DB=$OUT/effects.sqlite3 OGI013_SINGLE_E_K=${OGI013_SINGLE_E_K:-2} OGI013_SINGLE_E_SCOPE=writes
[ "$MODE" = rg2 ] && export OGI013_ORG_COLLAB=1 OGI013_ORG_POLICY_MODE=OFF OGI013_ORG_STATE_DIR=$OUT/org
BOOT="$H runners/ogi013_host_bootstrap.py --host-python $H --tau2-checkout $T --components-root $CR"
exec $BOOT --runner runners/ogi013_code_task.py --workdir $WORK --task-json $TASKDIR/agent_task.json --python $TASKDIR/venv38/bin/python --out $OUT/run --mode $MODE
