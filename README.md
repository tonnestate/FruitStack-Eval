# FruitStack-Eval

Independent research instrumentation for the protocol *Zero-Marginal-Cost Organizational Intelligence* (Tonn-AGI research series).

The evaluator sits **outside** the system under test. It never imports PlumMe, CherryMe or any other FruitStack package; it reads exported logs and git history only. That separation is the point: the system must not grade itself.

**Status: proposal v0.1.0 on `web/claude`.** Standard library only, Python 3.11 or newer. Nothing here has evaluated a real confirmatory run yet.

## What it does

| Command | Purpose | Protocol reference |
| --- | --- | --- |
| `fse power` | Sample sizes for the paired or unpaired non-inferiority test | §5.4 |
| `fse ope evaluate` / `fse ope review` | Independent IPS/SNIPS over a PlumMe DecisionLog export, with weight clipping, minimum support per action, effective sample size, seeded bootstrap interval, and evaluation of ensemble worker counts | §5.3, H1, H3 |
| `fse costaudit` | Post-hoc zero-cost audit: every chosen offer must have an allowed cost class, no outcome may be billed | Gate G3 |
| `fse drift` | Drift epochs per offer from the per-call `model_fingerprint`; a fingerprint change opens a new epoch | Threat 1 |
| `fse interventions add` / `summary` | Typed log of human acts: AUTHORITY (allowed) vs COGNITIVE (a deviation in the confirmatory phase), with minutes | Threat 3, H8, gate G5 |
| `fse tasks validate` / `commit` / `verify` | Task registry; prompts and references are published only as hashes and salted commitments | Gate G4 |
| `fse compare` | Recomputes utilities from raw evidence with rubric FSE-RUBRIC/1 and tests H4 with a paired cluster bootstrap | Gate G6, H4 |
| `fse ablation` | Which organizational component causes which gain: leave-one-out effects with Holm-adjusted bootstrap p-values, an interaction residual, and Shapley values that add up exactly to the total gain (full factorial, up to 6 components) | §5.6, Tonn-AGI §11.4 |
| `fse attribution` | Share of the current code written by each builder (git blame), separately for critical modules | Threat 4 |
| `fse protected` | Rejects system-authored commits on protected paths; lists builder commits there for host review | Learning loop 4 |
| `fse lite check` | Verifies that FruitStack-Lite clones sit at their pinned commits | Gate G6 |

All commands print JSON. Exit codes: `0` success, `1` a check failed, `2` invalid input.

## Install and test

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e '.[dev]'
python -m pytest -q
```

## Examples

```bash
fse power paired --margin 0.10 --discordance 0.2          # 157 tasks
fse ope evaluate --log ~/.plumme/decisions.jsonl --family INQUIRY \
    --target '{"selector": "fixed_count", "count": 3}'
fse costaudit --log ~/.plumme/decisions.jsonl
fse interventions add --log interventions.jsonl --actor owner \
    --kind AUTHORITY --intervention PROMOTE_POLICY --minutes 4 --phase PILOT
fse attribution --repo ../cherryme --rev origin/web/chatgpt \
    --range origin/main..origin/web/chatgpt=CHATGPT
fse protected --repo ../plumme --name plumme --base origin/main --head origin/web/chatgpt
```

## File formats

- **DecisionLog:** PlumMe's append-only JSONL rows `{"type": "decision" | "outcome" | "feedback", "data": {...}}`, including rotated segments `<file>.1`, `<file>.2`. Compatibility was checked against logs written by PlumMe's own `DecisionLog` (proposal branch `web/chatgpt`, commit `06ff53e`); SNIPS, IPS and effective sample size matched PlumMe's evaluator exactly on that log.
- **Results for `fse compare`:** one JSON line per task and arm with `task_id`, `arm`, `family`, `subfamily`, raw `evidence`, `quota_units`, `cost_eur`, `wall_seconds`.
- **Tasks:** one JSON line per task with `task_id`, `family` (INQUIRY, SOFTWARE, RESEARCH, ECONOMIC), `subfamily`, `split` (TRAIN, HELDOUT), `prompt`, `reference`. A subfamily is entirely TRAIN or entirely HELDOUT.

## Ablation input

`fse ablation` reads the same result rows as `fse compare` plus a TOML file that maps each arm to the components switched on:

```toml
[arms]
BASE = []
ENSEMBLE = ["adaptive_ensemble"]
ASSURANCE = ["trajectory_assurance"]
FULL = ["adaptive_ensemble", "trajectory_assurance"]
```

Only tasks run in every listed arm are used. `config/components.toml` lists the organizational components and whether their OFF switch was verified in code; only components with a verified switch should enter an ablation.

## Interpretation rules

- Only `HARNESS_OBSERVED` or `EXTERNALLY_VERIFIED` evidence becomes a label. Worker claims never do.
- Clipping importance weights biases estimates toward the behavior policy; every clipped estimate says so.
- `fse ope review` only reports whether a candidate is **eligible for host review**: its SNIPS lower bound must exceed the incumbent's SNIPS estimate, with enough effective sample size and action support. Promotion stays a host decision.
- H4 parity needs non-inferiority on verified success **and** a lower cost per verified success.

## Known limits

- **Attribution:** today most commits carry no builder identity. Proposal commits pushed through web connectors appear under the owner's name, so the report needs `--range` for open proposal branches. From now on every commit should carry `FruitStack-Builder: <name>`. Shallow clones leave boundary lines unknown; use full clones for confirmatory reports.
- **Protected paths:** entries exist for PlumMe, CherryMe, AppleMe, PeachMe, PomeloMe and this repository. MangoMe, SPARI, IntakeGov and further repositories still need entries. The check runs here; wiring it into each product repository's CI is a separate, governed change.
- **FruitStack-Lite:** every component is still `UNPINNED`, so gate G6 is closed until gate G1 (merges, `main == sync/local-truth`) passes.
- **Cost audit:** it verifies after the fact. Enforcement belongs in the labor market's own eligibility gate; PlumMe's `FREE_ONLY` cost policy is proposed on its `web/claude` branch (`f8fad50`).
- **Drift:** needs DecisionLog outcomes with `model_fingerprint`, which PlumMe records only from that same proposal on. Older outcomes are counted as `outcomes_without_fingerprint`, never guessed. An end-to-end run (PlumMe `f8fad50` writing the log, this evaluator reading it) detected a simulated provider model swap as one change and two epochs, and confirmed that a present paid offer was never chosen under `FREE_ONLY`.

## Governance

See `AGENTS.md`. This repository is entirely protected: system-authored commits may never change it.
