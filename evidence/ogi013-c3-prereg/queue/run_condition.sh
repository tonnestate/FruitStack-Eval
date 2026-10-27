#!/bin/bash
# usage: run_condition.sh CAMPAIGN TASK DOMAIN CONDITION SLOT
# Sets the per-condition environment for one c3 run, then execs the launcher ($LAUNCHER, default $RUNS_DIR/run_org.sh).
# DRY_RUN=1: prints ENV / UNSET / CMD lines instead of launching. Exit 2 = configuration error, nothing launched.
# Conditions: see conditions.md.
set -u
RUNS_DIR=${RUNS_DIR:-/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/runs}
LAUNCHER=${LAUNCHER:-$RUNS_DIR/run_org.sh}
C=${1:?campaign}; T=${2:?task}; DOM=${3:?domain}; COND=${4:?condition}; S=${5:?slot}
# The mixed exploratory campaign uses domain-qualified task keys to prevent
# collisions (airline:ID versus retail:ID) while the official runner receives
# its canonical domain and unqualified task id.
RAW_TASK=$T
if [ "$DOM" = mixed ]; then
  case "$T" in
    airline:*) DOM=airline; RAW_TASK=${T#airline:} ;;
    retail:*)  DOM=retail; RAW_TASK=${T#retail:} ;;
    *) echo "mixed campaign requires airline:ID or retail:ID" >&2; exit 2 ;;
  esac
  [ -n "$RAW_TASK" ] || { echo "empty mixed task id" >&2; exit 2; }
fi

# caller values, read before the c3 environment is reset
K_IN=${OGI013_SINGLE_E_K:-}; LD_IN=${OGI013_ORG_LEARNED_DIR:-}; LA_IN=${OGI013_ORG_LEARNED_AUTHORIZED:-}
UNSET="PLUMME_TRIAL_CREDIT PLUMME_ZERO_CHARGE_DISPATCH OGI013_ORG_POLICY_MODE OGI013_ORG_ABLATE OGI013_ORG_STATE_DIR OGI013_SINGLE_E_K OGI013_ORG_LEARNED_DIR OGI013_ORG_LEARNED_AUTHORIZED"
for v in $UNSET; do unset "$v"; done

ENVV=("OGI013_SIM_ROUTE_FILE=$RUNS_DIR/$C-$T.route")
STATE=""
case "$COND" in
  SINGLE) MODE=single ;;
  FIXED) MODE=fixed ;;
  SINGLE-E)
    [ -n "$K_IN" ] || { echo "SINGLE-E requires OGI013_SINGLE_E_K" >&2; exit 2; }
    MODE=single_e; ENVV+=("OGI013_SINGLE_E_K=$K_IN") ;;
  RG2-*)
    MODE=rg2; POLICY=OFF; ABLATE=""; STATE="$RUNS_DIR/$C/state/$COND"
    case "$COND" in
      RG2-OFF) ;;
      RG2-OFF-NOPERSIST) STATE="$RUNS_DIR/$C/state-fresh/$COND-$T" ;;
      RG2-NO-TRIAGE) ABLATE=triage ;;
      RG2-NO-VERIFY) ABLATE=verify ;;
      RG2-NO-KNOWLEDGE) ABLATE=knowledge ;;
      RG2-RANDOMIZED) POLICY=RANDOMIZED ;;
      RG2-LEARNED)
        [ -n "$LD_IN" ] && [ "$LA_IN" = 1 ] || { echo "RG2-LEARNED requires OGI013_ORG_LEARNED_DIR and OGI013_ORG_LEARNED_AUTHORIZED=1" >&2; exit 2; }
        POLICY=LEARNED; ENVV+=("OGI013_ORG_LEARNED_DIR=$LD_IN" "OGI013_ORG_LEARNED_AUTHORIZED=1") ;;
      *) echo "unknown RG2 condition $COND" >&2; exit 2 ;;
    esac
    ENVV+=("OGI013_ORG_POLICY_MODE=$POLICY" "OGI013_ORG_STATE_DIR=$STATE")
    [ -n "$ABLATE" ] && ENVV+=("OGI013_ORG_ABLATE=$ABLATE") ;;
  *) echo "unknown condition $COND" >&2; exit 2 ;;
esac

OUTARG="$C/$T/$COND"; PAIR="$C-$T"; SLOTARG="$S-$COND"
if [ -n "${DRY_RUN:-}" ]; then
  for kv in "${ENVV[@]}"; do echo "ENV $kv"; done
  echo "UNSET $UNSET"
  echo "CMD $LAUNCHER $OUTARG $RAW_TASK $DOM $MODE $PAIR $SLOTARG"
  exit 0
fi
[ -n "$STATE" ] && mkdir -p "$STATE"
for kv in "${ENVV[@]}"; do export "$kv"; done
exec "$LAUNCHER" "$OUTARG" "$RAW_TASK" "$DOM" "$MODE" "$PAIR" "$SLOTARG"
