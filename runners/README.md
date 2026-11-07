# Harness runners

## OGI-013 tau2 host prototype

`ogi013_tau2_run.py` drives one official tau2 task with the installed FruitStack
components and writes `official-result.json` plus `fruitstack-events.jsonl` under
`--out/tasks/<task>`. Run the same task separately with `--mode single`, `fixed`,
and `adaptive`; each process and output directory must be isolated. The host must
provide the official tau2 checkout (`OGI013_TAU2_ROOT`), product packages on
`PYTHONPATH`, isolated MangoMe/OrangeMe storage, and a host-approved cost budget.
PlumMe qualifies and selects supply under its configured policy, preferring free
or already-covered offers and requiring known cost evidence. The runner's
zero-dollar cap excludes positive-cost dispatch unless the host supplies an
explicitly approved positive budget; unknown cost remains ineligible.
`--max-provider-calls` and
`--max-tool-calls` bound each run. This host code is outside `fruitstack_eval`.

All arms, including `single`, route benchmark tools through the bounded Pomelo
gate. `single` means one reasoning worker without CherryMe review. `fixed`
applies Brother Mode review to each valid action. `adaptive` applies it only
when a predeclared rule detects a write or human transfer; this is a
consequence-triggered heuristic, not a learned competence-composition policy.
The adapter has only passed local import/parser checks; no external provider
task or official grader result has been obtained. Its event log is not yet a
complete `FSE-OGI13-ABC/1` observation export. Do not present it as a validated
OGI comparison.

The invoking host must provide an already admitted MangoMe binding through
`OGI013_WORK_REF`, `OGI013_TURN_ID`, `OGI013_ACTOR_ID`, and
`OGI013_PROJECT_REF`, plus `OGI013_POMELO_AUTHORITY` as host-issued JSON with
the same principal and explicit `tool:<name>` capabilities. The runner neither
creates a WorkIdentity nor mints Pomelo authority; missing or mismatched values
fail closed. Use PlumMe's authorized configured policy and effective budget;
do not source the research `env.sh` blindly. A paid route is usable only with
an explicitly approved positive budget and verified cost data.

Scripts in this directory run **on the host that executes the arms** (the FruitStack VPS). Unlike the evaluator package `fruitstack_eval`, they import the installed PlumMe, because they have to drive its real execution path. The evaluator never imports them; it only reads what they write. `tests/test_cli_gates.py` checks that `fruitstack_eval` imports no product package.

| Script | Gate | Bills anything? | Writes |
| --- | --- | --- | --- |
| `g3_cost_probe.py` | G3 | No. The paid probe offer points at `https://paid-probe.invalid` and is never contacted; real paid offers are only screened and acquisition-tested, never executed. | `g3_probe.json`, three probe DecisionLogs |
| `g2_supply_calibration.py` | G2 | No. It refuses to start unless `PLUMME_COST_POLICY=FREE_ONLY`, executes only offers the hard-eligibility gate admitted under that policy, and re-checks the cost class before every call. It consumes free quota. | `census.json`, `results.jsonl`, `run.json`, the run's DecisionLog |
| `pilot_inquiry.py` | Phase 2 | No. Refuses to start unless `PLUMME_COST_POLICY=FREE_ONLY`, or with fewer than `--min-free-models` (default 50) executable free models (`plumme coverage --free`, PLUMME-FREE-SUPPLY-001); arm A is refused outright and needs a separately approved run. Never reads task references. `--shard K/N` splits the tasks across N parallel processes with separate state directories. CherryMe `INCOMPLETE` is recorded as a system outcome, never as an answer. | `results-<ARM>.jsonl`, `run-<ARM>.json`, the arm's DecisionLog, CherryMe workspaces (F3) |

These FREE_ONLY checks preserve the registered G2/PILOT-PROC/1 comparison
conditions only. They are not PlumMe's general execution policy and do not
constrain the OGI-013 tau2 runner above.
## OGI-013: existing canonical host Python (not the frozen FREE_ONLY pilots)

For OGI-013 only, the executable host bootstrap is
`runners/ogi013_host_bootstrap.py`. The official benchmark checkout and all
FruitStack component checkouts must be **existing, canonical local sources**.
The bootstrap installs them editable in the **same host Python** that will
execute the original OGI-013 runner, so stale/missing `loguru`, `tau2`,
`mangome`, or `orangeme` cannot be mistaken for missing architecture.
It rejects the unrelated `tau2` package from PyPI. No new model credentials,
work identities, authorizations, tool plans, or spending limits are created.

Invoke the bootstrap with the actual host values (do not clone or use an
unverified benchmark revision). The local original benchmark runner is passed
by its actual absolute file path:

```bash
python3 runners/ogi013_host_bootstrap.py \
  --host-python /opt/fruitstack/venv-host/bin/python \
  --tau2-checkout "$EXISTING_OFFICIAL_TAU2_CHECKOUT" \
  --components-root "$CANONICAL_FRUITSTACK_CHECKOUTS" \
  --runner "$EXISTING_OGI013_RUNNER" \
  --task-limit 3
```

The wrapper logs the FruitStack component SHA of each canonical checkout.
The runner itself must continue to use an already host-bound MangoMe EXECUTE
turn and a trusted PomeloMe gateway + real authority and plan providers; it
must not manufacture them. PeachMe's existing
`FruitStackSession.attach_host_effects(...)` accepts these already-authorized
objects when the original host composer creates the session before the effect
bridge. Real provider runs and the independent evaluator are separate
operations, not simulated by this installer.

**Version comparability:** tau2 1.x and 2.x are not equivalent benchmarks.
Record the official tau2 checkout HEAD and use the *same checkout* for all
compared arms; do not silently upgrade a running experiment. The older
FREE_ONLY G2/pilot documentation below describes frozen historical protocols,
not an OGI-013 supply restriction.

## Order on the host

First `fse stack --python /opt/fruitstack/venv-host/bin/python --fetch`: no run starts while a required FruitStack part is missing, stale or hand-patched. For G2/PILOT-PROC/1, use that protocol's recorded FREE_ONLY condition; this is not a global PlumMe requirement. `fse` is this repository's CLI, installed into any Python 3.11+ environment (`pip install -e .`).

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
# Phase 2 (only after G1-G5 pass and the owner registered the approved task set; see PILOT_PROTOCOL.md)
F1=$(python -c "import json;print(json.load(open('$OUT/g2/independence.json'))['best_single_offer']['offer_id'])")
python runners/pilot_inquiry.py --tasks tasks.jsonl --out $OUT/pilot --arm F1 --offer $F1
for k in 0 1 2 3 4 5; do         # F3 in six parallel processes, disjoint task slices, own state directories
  python runners/pilot_inquiry.py --tasks tasks.jsonl --out $OUT/pilot --arm F3 --shard $k/6 \
      --cherryme-skill /root/fruits/sync/CherryMe/skill/ensemble --composer-offer $F1 &
done; wait
cat $OUT/pilot/results-F1*.jsonl $OUT/pilot/results-F3*.jsonl > $OUT/pilot/results.jsonl
fse inquiry grade --tasks tasks.jsonl --results $OUT/pilot/results.jsonl --out $OUT/pilot/graded.jsonl
fse pilot analyze --graded $OUT/pilot/graded.jsonl > $OUT/pilot/estimates.json
```

Commit `$OUT` (or at least the seal, `g3_probe.json`, `census.json`, `independence.json` and `g5_logcheck.json`) to this repository; the commit timestamp makes the seal revision-evident. Exit codes follow the `fse` convention: 0 pass, 1 a check failed.

## What a local run can and cannot show

All three runners were exercised in an isolated environment without provider access, against PlumMe 0.1.8 (`web/claude` `ea01fd2`): the cost probe with the host adapter list plus the synthetic offers, the calibration runner with four synthetic free groups (one a clone of another) and a synthetic paid offer; the pilot runner with real CherryMe ACE (`web/chatgpt` `3b474f3`), PlumMe 0.1.8 (`web/claude`) and AppleMe 0.1.2 on synthetic grounded supply. That proves the mechanics, not the gates: G2 and G3 count only from a run on the host with its real supply and configuration.
