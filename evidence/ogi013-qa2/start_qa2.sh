#!/bin/bash
# OGI-013 QA-2 (GPQA Diamond replication). DRY-RUN by default: prints the plan and checks nothing that costs supply. `--go` executes it. NOT started; needs the owner's Hugging Face token with GPQA access.
set -e
PD=/root/fruits/integration/ogi013-collab-proof; Q=/root/fruits/research/OGI013-QA2; H=/root/fruits/integration/ogi013-hostpython-org/bin/python
GO=0; [ "$1" = "--go" ] && GO=1
step() { echo "[$1] $2"; }
step 1 "refuse while QA-1 is still running (shared free-tier supply): pid file /root/fruits/research/OGI013-QA1/runs/study.pid"
step 2 "access check: $H $PD/runners/prepare_qa2.py --check   (exit 3 = gated: the owner accepts the GPQA terms and provides a token; this script never does)"
step 3 "prepare data outside the repository: prepare_qa2.py --out $Q/data"
step 4 "S model: run_qa1.sh $Q/data/study.jsonl $Q/runs/select --select-s   (AUTO first rank among models passing a 10-call probe)"
step 5 "lock: write_qa2_lock.py --data-dir $Q/data --s-model <model> --out $PD/evidence/ogi013-qa2/QA2_LOCK.txt; commit and push it before the first call"
step 6 "run: run_qa1.sh $Q/data/study.jsonl $Q/runs/study --s-model <model> --q-par 4   (the sealed QA-1 runner and analysis, unchanged)"
[ $GO = 1 ] || { echo "dry run only (use --go to execute)"; exit 0; }
PID=/root/fruits/research/OGI013-QA1/runs/study.pid
if [ -f $PID ] && kill -0 $(cat $PID) 2>/dev/null; then echo "REFUSED: QA-1 is still running"; exit 2; fi
cd $PD
$H runners/prepare_qa2.py --check || { echo "REFUSED: no GPQA access"; exit 3; }
$H runners/prepare_qa2.py --out $Q/data
SM=$(bash evidence/ogi013-qa1/run_qa1.sh $Q/data/study.jsonl $Q/runs/select --select-s 2>&1 | grep '"s_model"' | tail -1 | $H -c 'import sys,json; print(json.loads(sys.stdin.read())["s_model"])')
[ -n "$SM" ] && [ "$SM" != "None" ] || { echo "REFUSED: no S model passed the availability probe"; exit 4; }
$H runners/write_qa2_lock.py --data-dir $Q/data --s-model "$SM" --out evidence/ogi013-qa2/QA2_LOCK.txt
git add evidence/ogi013-qa2/QA2_LOCK.txt && git -c user.email=c@l -c user.name=Claude commit -q -m "QA-2: lock file [skip ci]" && git push -q https://github.com/tonnestate/FruitStack-Eval.git HEAD:ogi013-collab-proof
setsid nohup bash evidence/ogi013-qa1/run_qa1.sh $Q/data/study.jsonl $Q/runs/study --s-model "$SM" --q-par 4 > $Q/runs/study.log 2>&1 &
echo "QA-2 started (pid $!)"
