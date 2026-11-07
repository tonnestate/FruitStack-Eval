#!/bin/bash
# FruitStack arm on the frozen single coding task (same bootstrap as evidence/ogi013-pilot/run_arm.sh, but the runner is runners/ogi013_code_task.py).
# usage: run_team.sh MODE(team|indep|solo) OUTDIR     (OUTDIR must not exist)
set -e
MODE=$1; OUT=$2
PD=/root/fruits/integration/ogi013-collab-proof; B=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013-collab1; T=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/benchmarks/tau2-bench
R=$B/runs; H=/root/fruits/integration/ogi013-hostpython-org/bin/python; CR=/root/fruits/integration/ogi013-org-components
TASKDIR=/root/fruits/research/OGI013-SINGLE-TASK
cd "$PD"; source $B/env.sh
export PYTHONPATH=$PD/runners:$PD:$CR/CherryMe:$CR/PeachMe/src:$CR/PlumMe/src:$CR/AppleMe/src:$CR/MangoMe/src:$CR/OrangeMe/src:$CR/PomeloMe/src ORANGEME_SOURCE_REPO=$T
mkdir -p "$OUT/ledgers"
for n in chat project; do git clone -q --bare $B/slots/D/ledgers/$n.git $OUT/ledgers/$n.git; done
mkdir -p $OUT/orangeme-home
export ORANGEME_HOME=$OUT/orangeme-home ORANGEME_CHAT_REPO=$OUT/ledgers/chat.git ORANGEME_PROJECT_REPO=$OUT/ledgers/project.git
# D3: one WorkIdentity and one EXECUTE turn PER EPISODE, admitted by the host before the episode starts (the shared work.env of the earlier runs is not used)
eval "$($H runners/ogi013_bind_work.py "OGI-013 episode $(basename $OUT) $(date -u +%Y%m%dT%H%M%SZ) mode=$MODE")"
echo "OGI013_EPISODE_WORK work=$OGI013_WORK_REF turn=$OGI013_TURN_ID project=$OGI013_PROJECT_REF"
unset PLUMME_TRIAL_CREDIT PLUMME_ZERO_CHARGE_DISPATCH
set -a; source /root/.plumme/runtime.env >/dev/null 2>&1; set +a      # FLM_KEY (computed at source time) + the isolated FreeLLMAPI base URL; the cost policy stays as env.sh set it
export PLUMME_COST_POLICY=ANY PLUMME_SHARED_HEALTH_DIR=$R OGI013_PILOT_RUNS=$R
export OGI013_SESSION_MAX_COST_USD=0     # call/token ceilings come from --max-calls/--max-tokens (frozen default 110/200000 is NOT applied to team episodes; see Addendum 3 F)
export OGI013_EFFECT_DB=$OUT/effects.sqlite3 OGI013_SINGLE_E_K=${OGI013_SINGLE_E_K:-2} OGI013_SINGLE_E_SCOPE=writes
BOOT="$H runners/ogi013_host_bootstrap.py --host-python $H --tau2-checkout $T --components-root $CR"
# Experiment B team episode (Addendum 3). env: TASKDIR (task dir with base/ agent_task.json venv38/), MODE team|indep|solo, EXTRA (extra runner args)
TD=${TASKDIR_OVERRIDE:-$TASKDIR}
exec $BOOT --runner runners/ogi013_team_code.py --base $TD/base --task-json $TD/agent_task.json --python $TD/venv38/bin/python --out $OUT/run --mode $MODE $EXTRA
