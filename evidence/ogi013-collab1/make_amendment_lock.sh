#!/bin/bash
# Writes AMENDMENT_LOCK.txt: the hashes of every file the COLLAB-1 study depends on AFTER AMENDMENT-1 (later entries supersede the entries of ../ogi013-phase2/STUDY_LOCK.txt). Run once, before the first study episode.
cd "$(dirname "$0")/../.." || exit 2
{
  echo "# OGI-013-COLLAB-1 AMENDMENT-1 lock - $(date -u +%FT%TZ) - written BEFORE any study episode (no runs/collab1 directory exists). Supersedes same-path entries of evidence/ogi013-phase2/STUDY_LOCK.txt."
  sha256sum evidence/ogi013-collab1/AMENDMENT-1.md evidence/ogi013-collab1/CALIBRATION.md evidence/ogi013-collab1/make_manifest_v2.py evidence/ogi013-collab1/study_manifest_v2.json evidence/ogi013-collab1/collab1_budget.json \
    evidence/ogi013-collab1/run_collab1.py evidence/ogi013-collab1/analyze_study.py evidence/ogi013-phase2/decision_metrics.py evidence/ogi013-pilot/pilot_guard.py evidence/ogi013-pilot/sim_preflight.py \
    evidence/ogi013-pilot/run_arm.sh evidence/ogi013-pilot/pilot_report.py runners/ogi013_tau2_agent.py runners/ogi013_org_collab.py runners/ogi013_lineage_heart.py runners/ogi013_sim_supply.py \
    runners/ogi013_pilot_gate.py runners/ogi013_tau2_run.py runners/ogi013_single_e.py runners/ogi013_confirmatory.py
} > evidence/ogi013-collab1/AMENDMENT_LOCK.txt
