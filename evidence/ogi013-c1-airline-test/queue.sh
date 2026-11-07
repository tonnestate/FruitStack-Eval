#!/bin/bash
# OGI-013 per-slot queue. usage: queue.sh CAMPAIGN DOMAIN SLOT TASKID...   (one OrangeMe ledger slot, tasks strictly sequential)
# Per task one PAIR with the same PlumMe-selected simulator MODEL in both arms; arm order alternates by task-id parity (even: fixed first).
# A pair whose simulator route fails (SIM_ROUTE_FAILED) in either arm is discarded as a whole (kept under $C/discarded with arm + route) and re-run, max 3 attempts.
R=/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/runs; C=${1:?}; DOM=${2:?}; S=${3:?}; shift 3
mkdir -p "${R:?}/$C/discarded"
for T in "$@"; do
  ORDER="fixed adaptive"; [ $((T % 2)) -eq 1 ] && ORDER="adaptive fixed"
  for k in 1 2 3; do
    rm -f "${R:?}/$C-$T.route"
    for M in $ORDER; do
      timeout 3000 "$R/run1.sh" "$C/$T-$M" "$T" "$DOM" "$M" "$C-$T" "$S" > "$R/$C/$T-$M.log" 2>&1
      echo "$T $M attempt=$k exit=$? slot=$S" >> "$R/$C/progress.txt"
    done
    if grep -q SIM_ROUTE_FAILED "$R/$C/$T-fixed.log" "$R/$C/$T-adaptive.log" 2>/dev/null && [ $k -lt 3 ]; then
      for M in $ORDER; do
        grep -q SIM_ROUTE_FAILED "$R/$C/$T-$M.log" && echo "$T discarded attempt=$k simulator route failed in arm=$M route=$(cat "$R/$C-$T.route" 2>/dev/null)" >> "$R/$C/progress.txt"
        mv "$R/$C/$T-$M" "$R/$C/discarded/$T-$M-attempt$k" 2>/dev/null; mv "$R/$C/$T-$M.log" "$R/$C/discarded/$T-$M-attempt$k.log"
      done
      mv "$R/$C-$T.route" "$R/$C/discarded/$T-attempt$k.route" 2>/dev/null
    else break; fi
  done
done
echo "QUEUE_DONE slot=$S" >> "$R/$C/progress.txt"
