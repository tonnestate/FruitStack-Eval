#!/bin/bash
# OGI-013 QA-1b supervisor (deviation D4): restarts the runner fresh after a systemic outage (exit 75), logs every restart, resumes from results.jsonl.
# usage: run_qa1b.sh DATA.jsonl OUTDIR [runner args...]
D=$(dirname "$0"); n=0
while true; do
  bash "$D/run_qa1.sh" "$@"; rc=$?
  if [ $rc -ne 75 ]; then exit $rc; fi
  n=$((n+1)); echo "$(date -u +%FT%TZ) supervisor: systemic outage restart #$n" | tee -a "$2/supervisor.log"
  if [ $n -ge 30 ]; then echo "supervisor: restart cap 30 reached" | tee -a "$2/supervisor.log"; exit 75; fi
  sleep 60
done
