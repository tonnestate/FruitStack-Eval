#!/bin/bash
# keeps supervisor.sh alive: restarts after a crash (non-zero exit); a clean exit (finished or recorded BLOCKED) ends the loop.
while true; do /bin/bash "$(dirname "$0")/supervisor.sh"; rc=$?; [ $rc -eq 0 ] && break; echo "$(date -u +%FT%TZ) supervisor exit $rc, respawn in 60s" >> /root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/runs/supervisor/supervisor.log; sleep 60; done
