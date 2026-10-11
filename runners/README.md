# Harness runners

Scripts in this directory run **on the host that executes the arms** (the FruitStack VPS). Unlike the evaluator package `fruitstack_eval`, they import the installed PlumMe, because they have to drive its real execution path. The evaluator never imports them; it only reads what they write. `tests/test_cli_gates.py` checks that `fruitstack_eval` imports no product package.

| Script | Gate | Bills anything? | Writes |
| --- | --- | --- | --- |
| `g3_cost_probe.py` | G3 | No. The paid probe offer points at `https://paid-probe.invalid` and is never contacted; real paid offers are only screened and acquisition-tested, never executed. | `g3_probe.json`, three probe DecisionLogs |
| `g2_supply_calibration.py` | G2 | No. It refuses to start unless `PLUMME_COST_POLICY=FREE_ONLY`, executes only offers the hard-eligibility gate admitted under that policy, and re-checks the cost class before every call. It consumes free quota. | `census.json`, `results.jsonl`, `run.json`, the run's DecisionLog |

## Order on the host

Run from a checkout of this repository with the host's PlumMe environment loaded (`/opt/fruitstack/venv-host`, the usual `PLUMME_*` variables, `PLUMME_COST_POLICY=FREE_ONLY`). `fse` is this repository's CLI, installed into any Python 3.11+ environment (`pip install -e .`).

```bash
OUT=evidence/$(date -u +%Y%m%dT%H%M%SZ)
# G3: paid route attempted and denied, positive control proves the probe can see a leak
python runners/g3_cost_probe.py --out $OUT/g3 --production-credentials
fse costaudit --log $OUT/g3/state-fallback/decisions.jsonl        # must pass
fse costaudit --log $OUT/g3/state-positive-control/decisions.jsonl  # must FAIL (control)

# G2: census, calibration, independence
fse calib generate --n 60 --seed 20261011 --out $OUT/g2/calib60.jsonl
python runners/g2_supply_calibration.py --tasks $OUT/g2/calib60.jsonl --out $OUT/g2 --census-only
python runners/g2_supply_calibration.py --tasks $OUT/g2/calib60.jsonl --out $OUT/g2 --pause 2
fse calib score --tasks $OUT/g2/calib60.jsonl --results $OUT/g2/results.jsonl --out $OUT/g2/scored.jsonl
fse independence --scored $OUT/g2/scored.jsonl > $OUT/g2/independence.json

# G5: intervention log, seal, completeness
fse interventions add --log $OUT/interventions.jsonl --actor owner --kind AUTHORITY \
    --intervention APPROVE_EFFECT --minutes 1 --phase DEVELOPMENT --note "G2/G3 run started"
fse seal create --seal $OUT/seal.json \
    --log decisions=$OUT/g2/state/decisions.jsonl:decisionlog \
    --log results=$OUT/g2/results.jsonl:jsonl --log interventions=$OUT/interventions.jsonl:jsonl
fse logcheck --log $OUT/g2/state/decisions.jsonl --interventions $OUT/interventions.jsonl \
    --seal $OUT/seal.json --expect-cost-policy FREE_ONLY > $OUT/g5_logcheck.json
```

Commit `$OUT` (or at least the seal, `g3_probe.json`, `census.json`, `independence.json` and `g5_logcheck.json`) to this repository; the commit timestamp makes the seal revision-evident. Exit codes follow the `fse` convention: 0 pass, 1 a check failed.

## What a local run can and cannot show

Both runners were exercised in an isolated environment without provider access, against PlumMe 0.1.8 (`web/claude` `ea01fd2`): the cost probe with the host adapter list plus the synthetic offers, the calibration runner with four synthetic free groups (one a clone of another) and a synthetic paid offer. That proves the mechanics, not the gates: G2 and G3 count only from a run on the host with its real supply and configuration.
