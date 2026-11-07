#!/bin/bash
# OGI-013 QA-1 launcher. usage: run_qa1.sh DATA.jsonl OUTDIR [runner args...]   (OUTDIR is created; reuse it to resume)
set -e
DATA=$1; OUT=$2; shift 2
PD=${OGI013_PD:-/root/fruits/integration/ogi013-collab-proof}; B=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013-collab1; T=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/benchmarks/tau2-bench
R=$B/runs; H=/root/fruits/integration/ogi013-hostpython-org/bin/python; CR=/root/fruits/integration/ogi013-org-components
cd "$PD"; source $B/env.sh
export PYTHONPATH=$PD/runners:$PD:$CR/CherryMe:$CR/PeachMe/src:$CR/PlumMe/src:$CR/AppleMe/src:$CR/MangoMe/src:$CR/OrangeMe/src:$CR/PomeloMe ORANGEME_SOURCE_REPO=$T
mkdir -p "$OUT/ledgers"
if [ ! -d "$OUT/ledgers/chat.git" ]; then for n in chat project; do git clone -q --bare $B/slots/D/ledgers/$n.git $OUT/ledgers/$n.git; done; fi
mkdir -p $OUT/orangeme-home
export ORANGEME_HOME=$OUT/orangeme-home ORANGEME_CHAT_REPO=$OUT/ledgers/chat.git ORANGEME_PROJECT_REPO=$OUT/ledgers/project.git
unset PLUMME_TRIAL_CREDIT PLUMME_ZERO_CHARGE_DISPATCH
set -a; source /root/.plumme/runtime.env >/dev/null 2>&1; set +a
export PLUMME_COST_POLICY=ANY PLUMME_SHARED_HEALTH_DIR=$R OGI013_PILOT_RUNS=$R OGI013_SESSION_MAX_COST_USD=0
export OGI013_EFFECT_DB=$OUT/effects.sqlite3 OGI013_SINGLE_E_K=2 OGI013_SINGLE_E_SCOPE=writes
# the Stack needs one admitted work to start; every (question, arm) then gets its own WorkIdentity + turn from the runner
eval "$($H runners/ogi013_bind_work.py "OGI-013 QA-1 stack start $(date -u +%FT%TZ)")"
exec $H runners/ogi013_host_bootstrap.py --host-python $H --tau2-checkout $T --components-root $CR --runner ${OGI013_RUNNER:-runners/ogi013_qa1.py} --data $DATA --out $OUT/run "$@"
