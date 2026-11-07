#!/bin/bash
# S1 small advantage test: 16 items x (T, SN), hard run-cap 500, no retries. Based on evidence/ogi013-single-task/run_team.sh bootstrap.
set -e
OUT=/root/fruits/research/OGI013-QA1/runs/s1/run1; rm -rf "$OUT"; mkdir -p "$OUT"
PD=/root/fruits/integration/ogi013-collab-proof; B=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013-collab1; T=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/benchmarks/tau2-bench
R=$B/runs; H=/root/fruits/integration/ogi013-hostpython-org/bin/python; CR=/root/fruits/integration/ogi013-org-components
cd "$PD"; source $B/env.sh
export PYTHONPATH=$PD/runners:$PD:$CR/CherryMe:$CR/PeachMe/src:$CR/PlumMe/src:$CR/AppleMe/src:$CR/MangoMe/src:$CR/OrangeMe/src:$CR/PomeloMe/src ORANGEME_SOURCE_REPO=$T
mkdir -p "$OUT/ledgers"
for n in chat project; do git clone -q --bare $B/slots/D/ledgers/$n.git $OUT/ledgers/$n.git; done
mkdir -p $OUT/orangeme-home
export ORANGEME_HOME=$OUT/orangeme-home ORANGEME_CHAT_REPO=$OUT/ledgers/chat.git ORANGEME_PROJECT_REPO=$OUT/ledgers/project.git
eval "$($H runners/ogi013_bind_work.py "OGI-013 open collab $(date -u +%Y%m%dT%H%M%SZ)")"
unset PLUMME_TRIAL_CREDIT PLUMME_ZERO_CHARGE_DISPATCH
set -a; source /root/.plumme/runtime.env >/dev/null 2>&1; set +a
export PLUMME_COST_POLICY=ANY PLUMME_SHARED_HEALTH_DIR=$R OGI013_SESSION_MAX_COST_USD=0
echo "bound work=$OGI013_WORK_REF"
D=/root/fruits/integration/ogi013-collab-proof/evidence/ogi013-small-proof
timeout 3300 $H runners/ogi013_s1.py --data /root/fruits/research/OGI013-QA1/data/qa2d_items.jsonl --selection $D/selection.json --out $OUT/out --run-cap 500 > $OUT/run.log 2>&1; echo exit=$?
