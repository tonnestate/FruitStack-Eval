# OGI-013-PILOT-1 — execution package (NOT executed; the budget below is a proposal, not an authorization)

One matched **SINGLE vs RG2-COLLAB** episode on the official tau2 benchmark (airline task 24, a write task), exploratory and separate from the preregistered OGI-013 study (its protocol, locks, evidence and
worktrees are untouched). n = 1 pair: it can show whether the integration works and what it costs, never an effect.

## 1. The runtime path and what proves each step
`run_pilot.sh` → `run_arm.sh` (pinned components via the shared bootstrap) → `ogi013_tau2_run` → `FruitStackTau2Agent` → `Episode.step` → PeachMe `FruitStackSession` → `LineageHeart` → PlumMe selection.
With `OGI013_ORG_COLLAB=1` (COLLAB arm only) a write is routed to `_org_collab` (economy gate decides *whether*, purpose recorded) → `collaborate()` → CherryMe Brother Mode: draft → independent challenge → revision →
renewed challenge → specialist for an unresolved objection → renewed review of the specialist → consolidation. The legacy RG/2 FALSIFY path (`_org_decide`) is not run in that arm.
Proof: `tests/test_ogi013_integrated_runtime.py` drives the real agent/episode/session/budget/heart/Brother Mode with scripted providers (flag on → collaboration runs and the legacy path is never called; flag off → the reverse).

## 2. Integration defects found in that path and corrected
| defect | effect | correction |
|---|---|---|
| `Episode.step` set `heart.exclude_independence_keys` / `prefer_model_key`, which nothing reads | a "different-lineage" reviewer could be the author's own model | `LineageHeart` (`runners/ogi013_lineage_heart.py`) passes the exclusion in PlumMe's `request.metadata` and pins the author's model for a revision |
| PeachMe stores only a whitelist of lease fields in the session environment | every step's `independence_key` / `model_key` was `None` (lineage unprovable, exclusion list empty) | the heart keeps the lineage per lease; `Episode.step` reads it from there |
| a budget stop inside the collaboration was caught as `ORG_ERROR` and the unreviewed draft went on | acting after the budget said stop | stops (`SESSION_BUDGET_*`, `BUDGET_*`, reflex, pilot gate) propagate; `BUDGET_STOP` event; episode closes as `BUDGET_STOP` |
| a failed/unavailable reviewer raised through `collaborate` | the whole review was dropped as an error | returned as a failed attempt: Brother Mode's loop guards apply, `review_unavailable`, never counted as agreement |
| PeachMe session budget configured only for `rg2` | SINGLE ran without the shared budget control | configured for both arms whenever a pilot budget is set |
| guard counted every simulator call twice (receipt + sim-usage row) | dispatch/token numbers (and the earlier budget basis) inflated | one dispatch list keyed by receipt |
| per-arm caps keyed `SINGLE`/`RG2-ECONOMY`, looked up as `pilot-1/single|econ` | per-arm caps never enforced | keyed by the real arm directories; an arm without a cap halts |
| missing usage counted as 0; unknown cash not considered | silent zero | see §4 |
| `ogi013_sim_supply`: `f.write` outside its `with` | a failed pinned simulator crashed with "I/O on closed file" instead of recording the exhausted model | indented into the `with` |
| the agent reserved prompt + 2,048 tokens per step and PlumMe stops continuations at the reservation | a longer (reasoning) answer was refused `BUDGET_EXHAUSTED` and abandoned in both arms | pilot reservation from the route's output limit, bounded by budget facts only (§4); proven on the real PlumMe scheduler |
| `train_org_policy._versions()` imported Keras unconditionally | an `INSUFFICIENT_EVIDENCE` refusal crashed on a host without Keras | version recorded as `None` when Keras is absent |
| `env.sh` assigns `D=<research dir>`; the arm launcher used `$D` after sourcing it | wrong code path for the preflight / `PYTHONPATH` | the pilot checkout lives in `PD` (found by the dry-run test against the real env files) |
| the earlier pilot ran the shared `ogi013-org` checkout (no collaboration module), never set `OGI013_ORG_COLLAB`, and used task 6 (read-only: the gate would only log `ORG_SKIPPED`) | it could not have tested the collaboration | `run_arm.sh` runs this checkout; COLLAB arm = `rg2` + flag; task 24 |

## 3. Matched controls (verified from the evidence in the report, not assumed)
Same code checkout (clean, head recorded), same task/domain/seed/policy hash/tools (one tau2 build), same pinned simulator model (preflighted), same pinned component heads (from the bootstrap log), same
ledger snapshot (each arm gets its own fresh bare clones of slot D, heads compared), own PlumMe/PeachMe/AppleMe state under the arm directory, own `OGI013_ORG_STATE_DIR`, same supply policy: the full eligible PlumMe pool,
no model or provider restriction, AUTO. The only intended difference is mode and `OGI013_ORG_COLLAB=1`.

## 4. Resource authorization — three layers, all before the next dispatch
1. **PeachMe session budget** (the shared execution-budget control), configured for BOTH arms from `pilot_budget.json` (`pilot_guard.py env`): calls, tokens, cash 0.00. Reservation before every agent-side dispatch;
   a step without reported usage keeps its reservation (never 0); a route with unknown cost class, or a billed route with no cash authorized, is refused before the provider is called.
2. **Pre-dispatch gate** (`runners/ogi013_pilot_gate.py`) before every agent step AND every simulator attempt: all dispatches of the arm and the pilot incl. reviewer/specialist/retry/simulator, tokens + reserve, cash,
   unknown usage, unknown cash exposure, failure streak, wall clock. Over any → `PILOT_HALT`, `BUDGET_STOP`, no further dispatch, evidence untouched.
3. **`pilot_guard.py watch`** as a backstop.
Rules: a *successful* dispatch without usage halts; a failure rejected before processing (PlumMe's own `REJECTION_CLASSES`) is known-zero tokens; any other failure without usage is charged the reserve; a route class that is
not zero-cash (`ANONYMOUS_FREE FREE_TIER LOCAL TRIAL_CREDIT INCLUDED`) without a recorded cost halts; `TRIAL_CREDIT`/`INCLUDED` use is reported as entitlement; 20 failed dispatches in a row halt (observed worst streak in
the archived runs: 17); rejected attempts count as dispatches. No fixed output cap in the pilot: each agent step's reservation is sized from the route's published output limit (PlumMe continues a longer answer) and capped only by budget facts — the owner-approved `max_tokens_per_step` (24,000), PeachMe's remaining session tokens and the ledger's remaining headroom (agent + simulator); a step that cannot afford 2,048 answer tokens is a budget stop before dispatch, never a truncated answer. Outside the pilot the old 2,048 rule is unchanged.

## 5. Estimated budget (ESTIMATE from archived runs, recounted without the double count — see `pilot_budget.json`)
| scope | max dispatches | max tokens |
|---|---|---|
| SINGLE | 70 | 100,000 |
| COLLAB | 110 | 180,000 |
| pilot | 180 | 280,000 |
Cash 0.00 USD, wall clock 90 min, reserve 4,000 tokens per dispatch. Expected SINGLE ~48 dispatches / ~70k tokens, COLLAB ~70 / ~115k (each reviewed write adds ≤ 5 calls; 50-70 % of archived dispatches were provider
rejections that cost no tokens). Task 24 itself was never run to completion under these conditions; the estimate may be off in either direction, which is why every cap fails closed.

## 6. What the run produces (`runs/pilot-1/`)
`report.md` + `report.json` (official reward per arm, final actions, drafts/revisions/reviews with text, objections left, overruled positions, models and lineages, dispatches and tokens split agent/simulator/successful/
rejected, wall clock, cash and entitlement with unknowns listed, controls check, overhead of the collaboration), `conditions-<arm>.json`, `<arm>.log`, `pilot_budget.json` (as run), `code-head.txt`,
`preflight.json`, the arms' receipts/events/official results. Report verdict, four separate questions: (1) benchmark executed in both arms, (2) independent review / a documented action-changing intervention,
(3) improvement over SINGLE observed in this pair (with or without a documented mechanism), (4) statistical evidence — always "not established" for one pair.

## 7. Limitations
- `LineageHeart` and the whole collaboration flow are proven offline on the REAL PlumMe service/scheduler/receipt store (scripted provider adapter, `tests/test_ogi013_real_plumme.py`); live provider behaviour is first seen in the pilot (the report shows each step's lineage and `prefer_met`).
- A long answer can use up to `max_tokens_per_step` in one step, so token use per step is less predictable than before; every cap still fails closed.
- The MangoMe database (`mangome_ogi013_eval`) and the host-bound work/turn identity are shared by both arms by design; the ledgers, PlumMe/PeachMe/AppleMe state and organisational state are isolated.
- `PLUMME_COST_POLICY=ANY` comes from the shared `env.sh`; zero cash is enforced by layers 1-2, not by PlumMe's policy.
- The caps count completed dispatches (receipts are written after the call); the reserve covers the one in flight.
- The preflight performs provider metadata discovery (network, no inference, no tokens).
- The collaboration only reviews write actions; if the agent never proposes one, the report says the arm tested nothing.

## 8. Commands
- offline proof (no inference): `evidence/ogi013-pilot/offline_tests.sh`
- exact commands per arm, nothing executed: `PILOT_DRY_RUN=1 PILOT_CODE=$PWD evidence/ogi013-pilot/run_arm.sh pilot-1/collab 24 airline rg2 pilot-1-task24 /tmp/slot`
- owner approval of exactly this budget: `sha256sum evidence/ogi013-pilot/pilot_budget.json > /root/pilot-approval.txt` (any edit of the file invalidates it)
- run after approval: `PILOT_APPROVAL=/root/pilot-approval.txt /root/fruits/integration/ogi013-collab-proof/evidence/ogi013-pilot/run_pilot.sh`
  exit codes: 0 complete · 2 refused (nothing started) · 3 halted by the budget · 4 simulator not executable · 5 an arm failed · 130 interrupted. Nothing is ever restarted or resumed automatically.
