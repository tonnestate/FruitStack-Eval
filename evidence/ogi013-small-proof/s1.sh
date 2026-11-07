#!/bin/bash
# S1 small advantage test: 16 items x (T, SN), hard run-cap 500, no retries. Based on evidence/ogi013-single-task/run_team.sh bootstrap.
set -e
OUT=/root/fruits/research/OGI013-QA1/runs/s1/run1; rm -rf "$OUT"; mkdir -p "$OUT"
PD=/root/fruits/integration/ogi013-collab-proof/evidence/ogi013-small-proof
timeout 3300 $H runners/ogi013_s1.py --data /root/fruits/research/OGI013-QA1/data/qa2d_items.jsonl --selection $D/selection.json --out $OUT/out --run-cap 500 > $OUT/run.log 2>&1; echo exit=$?
