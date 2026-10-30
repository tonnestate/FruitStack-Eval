#!/bin/bash
# OGI-013 micro pilot: 3 tasks x 3 arms (T team, S solo sticky author, L Luna), one start each, no restart, no FIX. Per episode: 300,000 tokens, 30 min.
PD=/root/fruits/integration/ogi013-collab-proof; R=/root/fruits/research/OGI013-MICRO; H=/root/fruits/integration/ogi013-hostpython-org/bin/python
cd $PD
for t in micro__intervals-1 micro__duration-1 micro__lru-1; do
  for arm in T S L; do
    OUT=$R/runs/$t/$arm; mkdir -p $R/runs/$t
    echo "$(date -u +%FT%TZ) START $t $arm" >> $R/pilot.log
    if [ $arm = L ]; then
      timeout 2100 $H runners/ogi013_micro_luna.py $R/$t $OUT > $R/runs/$t/$arm.log 2>&1; rc=$?
    else
      MODE=team; [ $arm = S ] && MODE=solo
      TASKDIR_OVERRIDE=$R/$t EXTRA="--max-tokens 300000 --wall-seconds 1800" timeout 2400 bash evidence/ogi013-single-task/run_team.sh $MODE $OUT > $R/runs/$t/$arm.log 2>&1; rc=$?
    fi
    echo "$(date -u +%FT%TZ) END $t $arm rc=$rc" >> $R/pilot.log
    [ -f $OUT/run/run.json -o -f $OUT/run.json ] || echo "INFRA_FAILED" > $R/runs/$t/$arm.INFRA_FAILED
  done
done
echo "$(date -u +%FT%TZ) PILOT_DONE" >> $R/pilot.log
