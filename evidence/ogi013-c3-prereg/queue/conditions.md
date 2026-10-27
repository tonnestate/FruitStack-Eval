# OGI-013 c3 block queue - condition table

Source of truth: `evidence/ogi013-c3-prereg/PROTOCOL.md`. `SINGLE-K` in the protocol is named `SINGLE-E` here (per the queue spec).

Each task runs as one BLOCK: all conditions in `$CONDITIONS`, back to back, in a seeded order
`random.Random(f"{SEED}|{TASK}").shuffle`. One simulator route file per task (`<runs>/<campaign>-<task>.route`), shared by its conditions.
A block with `SIM_ROUTE_FAILED` in any condition log is discarded as a whole (`<campaign>/discarded/<task>-attemptK`) and retried, max 3 attempts.

| Condition | run_org mode | OGI013_ORG_POLICY_MODE | OGI013_ORG_ABLATE | OGI013_ORG_STATE_DIR | Extra requirement |
|---|---|---|---|---|---|
| SINGLE | single | - | - | - | - |
| SINGLE-E | single_e | - | - | - | `OGI013_SINGLE_E_K` (else exit 2) |
| FIXED | fixed | - | - | - | - |
| RG2-OFF | rg2 | OFF | - | `<campaign>/state/RG2-OFF` (shared by all tasks of the arm) | - |
| RG2-OFF-NOPERSIST | rg2 | OFF | - | `<campaign>/state-fresh/RG2-OFF-NOPERSIST-<task>` (fresh per task) | - |
| RG2-NO-TRIAGE | rg2 | OFF | triage | `<campaign>/state/RG2-NO-TRIAGE` | - |
| RG2-NO-VERIFY | rg2 | OFF | verify | `<campaign>/state/RG2-NO-VERIFY` | - |
| RG2-NO-KNOWLEDGE | rg2 | OFF | knowledge | `<campaign>/state/RG2-NO-KNOWLEDGE` | - |
| RG2-LEARNED | rg2 | LEARNED | - | `<campaign>/state/RG2-LEARNED` | `OGI013_ORG_LEARNED_DIR` and `OGI013_ORG_LEARNED_AUTHORIZED=1` (else exit 2) |
| RG2-RANDOMIZED | rg2 | RANDOMIZED | - | `<campaign>/state/RG2-RANDOMIZED` | phase A only |

Common to all rows:
- `OUTDIR` = `<campaign>/<task>/<condition>` (under `RUNS_DIR`); the per-condition log is `<campaign>/<task>/<condition>.log`.
- ORANGEME slot arg = `<SLOT>-<condition>`, so no two conditions share an OrangeMe ledger.
- `OGI013_SIM_ROUTE_FILE` = `<RUNS_DIR>/<campaign>-<task>.route`.
- Unset before setting: `PLUMME_TRIAL_CREDIT`, `PLUMME_ZERO_CHARGE_DISPATCH` and all `OGI013_ORG_*` / `OGI013_SINGLE_E_K` variables.
- Launcher call: `$LAUNCHER OUTDIR TASK DOMAIN MODE PAIRROUTE SLOTARG` (default `LAUNCHER=$RUNS_DIR/run_org.sh`).

Campaign names `c1-*` and `c2-*` are refused by `block_queue.sh` (historical arms, live c2 run).

Dry run: `DRY_RUN=1` prints `ENV`, `UNSET` and `CMD` lines instead of launching.
