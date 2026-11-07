# OGI-013 donor reconciliation — 2026-11-02

Scope: offline source/code comparison only. This is not an OGI outcome study and does not certify a collective-intelligence benefit.

## Decision matrix

| DONOR | MECHANISM | BEREITS VORHANDEN | REPRODUZIERBARE LÜCKE | MESSBARER MEHRWERT | ENTSCHEIDUNG |
|---|---|---|---|---|---|
| Cloudflare Code Mode | Progressive tool discovery | PlumMe `SkillCatalog`/task skill resolution, CogC context compilation, MCP discovery, `fs_codemode.Facade`, deterministic bounded `parallel`/`chain`, Sieve compaction with invariant fallback | The fixed duo does not expose a progressive runtime tool catalog or execute model-authored tool-composition programs. No local controlled comparison shows these are needed for the current fixed workflow. | None measured; no comparable prompt/token/roundtrip replay was run. | `REUSE_EXISTING` for bounded fixed workflows; `PARK_NO_EVIDENCE` for broader progressive discovery or model-authored composition. No donor runtime added. |
| Reason Network | Addressable live-session messaging, receipt states, idempotency | CherryMe Brother rounds exchange first answers, objections and replies inside an admitted claim; ContributionLedger preserves independent alternatives, provenance, identity, disposition and resources. Peach/Mango hold task/session state. | No existing adapter transports messages between separately running Codex/Claude sessions. The deterministic offline fixture below exercises existing contribution exchange, not Reason Network transport. | No transport overhead, delivery reliability, recovery or task-quality comparison measured. | `PARK_NO_EVIDENCE`; do not add a second router, work state or memory. |
| Vercel durable-harness | Durable turn/tool journal and resume | Peach step/governance state, Mango checkpoints, Pomelo pre-dispatch authority guard, idempotency key and transactional receipt outbox | A snapshot followed by dispatch is not atomic. A journal alone does not fix the existing authority/dispatch race; no new donor test establishes that it does. | No replay-cost or duplicate-effect comparison measured. Existing tests cover bounded dispatch/idempotency paths. | `REJECT_DUPLICATION`; any proven race must be fixed at the existing Pomelo authority boundary. |

## Reproducible offline session-exchange fixture

Ran a local Python fixture through CherryMe `ContributionLedger` and `consolidate`: two simulated sessions added independent, unverified first proposals; a later exchanged contribution extended the second proposal. The consolidation retained all three contributions, reported both alternatives unresolved, and did not promote either to truth. Output:

```text
PASS: simulated independent proposals and exchanged correction; 3 contributions retained; 2 alternatives unresolved; no truth promotion
```

This verifies the existing task-scoped exchange/evidence path. It does not exercise cross-process transport, delivery receipts, retries, or Reason Network. No external donor repository was installed or run.

## Source references

- [Cloudflare Code Mode](https://developers.cloudflare.com/agents/tools/codemode/)
- [Cloudflare Code Mode MCP server guide](https://developers.cloudflare.com/agents/model-context-protocol/guides/build-codemode-mcp-server/)
- [Cloudflare Agents source](https://github.com/cloudflare/agents)
- [Reason Network source](https://github.com/reason-machines/reason-network)
- [Vercel durable-harness source](https://github.com/vercel-labs/durable-harness)

## Constraints and status

- No provider/model call, token, quota, or provider cost was used for this comparison.
- No donor dependency, runtime, gateway, repository, credential store, or persistence authority was added.
- The requested FruitStack-Eval issue review comment `6573607459` was later retrieved through the connected read-only GitHub integration and reconciled below.
- Cloudflare runtime savings, Reason Network transport reliability, and durable resume advantages remain unmeasured. Any of these claims requires an offline deterministic comparison first, then separate owner approval for provider experiments if needed.

## Existing cross-task feedback path (P0.4 boundary)

PlumMe already persists/replays `ReviewFeedback` in its append-only `DecisionLog` and exposes `record_review_feedback`; CherryMe's host bridge restricts writing it to the trusted host after independent verification. `KerasShadowPolicy` can report reviewer precision, recall and outcome-improvement rates from those events. This is a reusable storage and feedback path, not yet a valid OGI-013 weight source: `ogi013_brother_loop.make_control` does not bind a PlumMe decision to the cooperation round, and OGI-013 currently has no independent per-review verifier that can safely populate those labels. The current `classify_argument`/`Facade.verify` path emits `formal`, `reproduced`, `suggestion` or failure; it cannot emit `independently_confirmed`. Thus the controller's confirmed-evidence path and positive weight update are exercised by injected offline fixtures, not by an available production verifier. Mapping unverified `hit`/revision events into `ReviewFeedback` would violate its evidence contract. Therefore cross-question controller-weight persistence remains open; no second weight database or unverified feedback adapter was added.

## Auftragstreue / Completion Inspector (P0.3/P0.5 integration boundary)

CherryMe already contains a deterministic `CompletionInspector` that checks canonical claim state, accepted baseline question types, stop conditions and owner acceptance. FruitStack's current `runners/ogi013_qa1.py` path does not call it; its controlled closing validates only the decision rule/model presence and that the chosen letter is among current candidates. The existing inspector also does not compare a broad accepted work objective with the semantic relevance of a completed subtask. Therefore the required regression (“Shapley-only diagnostic must not satisfy a Brother-Mode repair assignment”) is **not proven by this integration**. No second completion checker was added: the existing inspector needs a caller bound to the accepted work objective and acceptance evidence before it can enforce this case. Goal-level acceptance remains open.

## P0.2 evidence semantics and P0.6 action costs — offline follow-up

The OGI controller now distinguishes `formal`, `reproduced`, and `independently_confirmed`. The current host argument checker can emit only formal completeness or successful sandbox reproduction; it explicitly marks relevance and independent confirmation false. Therefore neither a reproduced calculation nor formal completeness can update competence, override a candidate, or receive independent-confirmation authority. Controller events record those separate checks. A repeated critique row id is applied once per controller instance and audited as a duplicate.

Current executable actions are only the paths exposed by CherryMe's `run_rounds`: `CRITIQUE`, `REPLY` (the revision call), `SPECIALIST`, and `FINISH`. The first independent critique is mandatory in this two-position path; EVC can choose whether to continue afterward. EVC parameters and token/time costs are fixed a-priori estimates, logged with `calibrated: false` and `cost_basis: A_PRIORI_ESTIMATE`; they are not empirically optimal and do not include a trained policy. No independent research/verifier action is advertised because this adapter does not provide one.

Focused offline re-verification after these changes: FruitStack integrated tests `85 passed, 2 skipped`; CherryMe Brother/parallel/handoff/completion tests `33 passed`. These are implementation tests, not benchmark evidence. The duplicate guard is instance-local; process-restart reconstruction and cross-task learned weights remain unimplemented because no permissible, independently verified feedback source is connected to this control path.

## Test-suite boundary (2026-11-02)

- FruitStack-Eval full suite: `623 passed, 13 skipped, 2 failed, 7 errors`. Seven end-to-end errors and one campaign failure could not connect to local MongoDB (`127.0.0.1:27017`, `EPERM` in this sandbox). The other failure is `test_ogi013_decision_metrics::test_the_collab_study_lock_matches_the_frozen_files`: the already-dirty `runners/ogi013_tau2_agent.py` hash differs from the frozen lock (`8ae2c…` vs `214652…`). The lock and frozen artifact were not changed to mask this.
- CherryMe full suite: `390 passed, 4 skipped, 10 failed`. Failures were in unrelated ExperimentalModelPolicy environment assumptions, an integrity truncation metadata assertion, and a responsibility-graph `competence_gate_enabled` expectation. There was no pristine baseline run, so these are not labeled pre-existing.
- Focused integration suites remain green: FruitStack-Eval `85 passed, 2 skipped`; CherryMe Brother/parallel/handoff/completion `33 passed`.
- `git diff --check` is clean in both working repositories. No commit, push, merge, or canonical-branch mutation was made.

## Offline re-verification after evidence-label hardening (2026-11-02)

- FruitStack focused integrated path, Python 3.11 offline environment: `53 passed, 3 skipped, 1 deselected`. The deselected test requires the unavailable `tau2` package; the three skips are existing optional-dependency skips. Command covered `test_fs_codemode.py`, `test_fs_codemode_loop.py`, `test_ogi013_argument.py`, `test_ogi013_integrated_runtime.py`, and `test_ogi013_qa1.py`.
- CherryMe Brother/parallel/handoff/completion subset: `32 passed, 1 deselected`; the deselected schema-validation test requires unavailable `jsonschema`.
- This re-run includes a regression that rejects a bare `independently_confirmed` label without explicit relevance and independent-confirmation checks. The direct test first failed on the old behavior and passed after the contract change. The production QA1 argument checker still emits no independent confirmation, so controller-weight learning from real QA1 evidence remains unavailable.
- `git diff --check` passed in both checkouts after this follow-up.

## Independent review reconciliation — issue comment 6573607459

The review audited FSE commit `86fb488` and identified four integration blockers and two policy/evidence defects. This offline follow-up addresses the answer-selection bypass (P0.1), blocks naked `independently_confirmed` labels without relevance and independent-confirmation checks (P0.2), and makes the first independent critique mandatory (P0.3). The CherryMe controller commit `33c3d77` is present locally but not published on the reviewed remote branch; it remains unreproducible from the public branch until the authorized CherryMe truth writer reconciles it. The normal QA-1 T arm now dispatches through `run_T_brother(...)->run_T(loop=True)`, so the controller and controller-derived closing are active in the regular code path; deterministic offline dispatch coverage passes. This does not make its policy calibrated. Cross-task learned-weight restoration remains open (P0.4): the available QA-1 argument checker does not produce independent confirmation, and no per-review verifier-to-PlumMe decision linkage is present. Goal-level completion inspection is also not bound to the accepted work objective. These open points prevent acceptance of the end-to-end organization loop.

Review reference: https://github.com/tonnestate/FruitStack-Eval/issues/2#issuecomment-6573607459.

## Normal QA-1 dispatch activation (2026-11-02)

- `process_question()` now sends the ordinary T arm through `run_T_brother`, which calls the existing `run_T(..., loop=True)` path. There is no second closing rule: `controlled_answer` consumes the controller's recorded closing, rejects invalid/missing decisions, and accepts only an answer in the existing admissible candidate set. The non-controller `run_T(..., loop=False)` path still uses the original `final_answer` function.
- New regression `test_normal_team_arm_activates_brother_controller` passes against the normal `process_question()` dispatch.
- Integrated offline re-run (Python 3.12, with local CherryMe/PlumMe source paths): 56 passed, 5 skipped, 1 deselected. The deselected `test_qa_budget_profile_reserves_room_for_the_system_preamble_and_longer_answers` cannot import the optional `tau2` package, which is absent from available local environments. No packages were installed.
- CherryMe Brother round, handoff, parallel, hardening and completion-inspector subset: 33 passed.
- MangoMe host authorization and runtime activation were not exercised. Cross-task persistent Brother weights and accepted-work-objective completion binding remain open; no host-verified or scientific OGI claim follows from these offline tests.

## Donor source review

- Cloudflare's Code Mode docs describe programmatic composition of tools through generated code and an isolated execution environment; its MCP guide shows the server/tool boundary. FruitStack already has bounded local facade/chain/parallel/sieve mechanisms for the current fixed workflow. No local matched replay measured fewer tokens or model round-trips, so broader progressive discovery and model-authored composition stay parked. Sources: https://developers.cloudflare.com/agents/tools/codemode/ and https://developers.cloudflare.com/agents/model-context-protocol/guides/build-codemode-mcp-server/.
- Reason Network's README describes a separate daemon, encrypted peer-to-peer/relay delivery, session discovery, delivery stages, idempotency keys, and message status; it also states acceptance is not agent consumption and a reply is not task completion. This confirms that it could provide a missing transport, but there is no controlled transport need or FruitStack adapter test showing a benefit over current in-task contribution exchange. No network, daemon, or private content was used. Source: https://github.com/reason-machines/reason-network.
- durable-harness describes journaling conversations, in-flight turns, model/tool calls, and resuming after crashes while suppressing unsafe repeated tool calls; the project labels itself experimental (`0.0.x`). FruitStack already has Peach/Mango checkpoints plus Pomelo authority/idempotency boundaries. No replay fixture demonstrates an uncovered safe-recovery case, and journaling alone does not make dispatch atomic with authority checks. Source: https://github.com/vercel-labs/durable-harness.
- The review comment `6573607459` was retrieved using the read-only GitHub integration; its findings and disposition are summarized above.

## Übernommene Git-Stände und lokale Abweichungen

- FruitStack-Eval Checkout: branch `ogi013-collab-proof`, HEAD `86fb48877686647e2803ea86a2526c2baed076d5`; dieser Stand ist die Ausgangsbasis der lokalen OGI-013-Arbeitsänderungen. `main`/`sync/local-truth` wurden nicht verändert.
- CherryMe Checkout: lokaler Branch `ogi013-org-cherry`, Commit `33c3d772a89efdd00e03430ce6c4eaced846281e`, Parent `c9055391a7879b77f709b275671c3fab828c8bbb`. Der Commit liegt lokal vor; er ist nicht mit einem Remote-Tracking-Branch verbunden und seine Veröffentlichung auf GitHub konnte hier nicht bestätigt werden. `cherryme/brother.py` hat zusätzlich 21 geänderte Zeilen im Arbeitsbaum; diese sind uncommitted und bleiben vom Commit unterscheidbar.
- Keine neuen Commits, Pushes, Merges oder Änderungen an `main` beziehungsweise `sync/local-truth` wurden vorgenommen.

## Adaptive-controller reach

The controller adapter `ogi013_brother_loop.make_control` is called by `runners/ogi013_qa1.py` only. Existing coding-task runners (`ogi013_team_code.py`, `ogi013_code_task.py`, and the single-solver `ogi013_tau2_agent.py`) call CherryMe `run_rounds` without this controller; their code acceptance/release paths have separate test-gate and grounded-review rules. The CherryMe exchange itself remains product-agnostic, but adaptive EVC/weight steering has not been integrated or verified on code, research, or open-ended tasks. This is an explicit scope limitation, not evidence that those task classes benefit from the controller. Extending it requires matching task-specific evidence and release checks; no generic adapter was added.
