# FruitStack P2 — known-failure suppression, acquisition contention, Skills, fast path + eskalieren (2026-11-11)

Live service `plumme-mcp.service` (pid 1499376, restarted once at 2026-11-11T14:06:01Z on PlumMe 495fe0b). Aurora files edited in place
under `/opt/fruitstack/integration` (no git there; backups `*.bak-20261111T135726Z`, full diff `aurora_p2.diff`). Nothing pushed.

## Commits
| Repo / branch | Commit | Change |
|---|---|---|
| PlumMe-integration `integration/stability-001` | a4e4310 | 401/403 backoff that survives cooldown expiry (10 min doubling to 24 h, never permanent), model-scoped for FORBIDDEN or a key that works elsewhere, cleared on success, requalified at once when the credential file changes; per-screen memo for credential lookups and one pool-state refresh per screen; P1 non-generative cache made safe (string-keyed) |
| same | 935e894 | test: a required Skill reaches a lean Claude headless worker (stdin) with receipt skill ids + sha256 |
| same | 495fe0b | `plumme.remote.RemotePlumMe` (consumer handle on the one running service) + MCP tools `plum_record_ensemble_decision`, `plum_competence_profiles` |
| Aurora (live dir) | — | `aurora_chat.py` fast worker with self-assessed ESKALIEREN packet; `mission_facade.py` B/C/D routing + escalation hand-over; `aurora_mission_worker.py` CherryMe RG/2 (`triage="auto"`) on the shared service via RemotePlumMe; synthesis without the 250-word/800-token cap |

Boundary change (owner awareness): `record_consumer_ensemble_decision` was documented as "trusted-host Python API, not an MCP tool". It is now an MCP tool for authenticated clients; it only appends a typed ENSEMBLE record (service-side validation), never routes or executes.

## Tests
PlumMe 982 passed / 11 skipped; CherryMe 514 passed / 6 skipped (unchanged code); Aurora `tests/test_fast_path_escalation.py` 6/6 (A deterministic no model, B one fast worker, C packet reaches CherryMe with one PRIMARY worker per question and no triage call, D straight to CherryMe; real CherryMe engine + real RemotePlumMe, MCP transport faked). `test_accepted_source_truth` passes with the Aurora venv.

## Live checks (real models, zero added cost: subscription INCLUDED Luna, free llm7)
| Case | Path | Result | Time |
|---|---|---|---|
| B simple question | www-data → facade → aurora_chat → PlumMe | "Paris." (gpt-6-luna, codex-headless) | 7.18 s total = 5.40 s provider/CLI + ~1.23 s per-request subprocess start/imports + ~0.36 s MCP/PlumMe + ~0.2 s facade |
| Mandatory Skill | aurora_chat, `required_skill_ids=["falsify"]` | receipt `effective_skill_ids=["reasoning","falsify"]`, correct answer | 4.59 s (provider 4.26 s) |
| C escalation | www-data facade: fast worker returned ESKALIEREN with grund/offene_frage/teilergebnis/randbedingungen + its receipt/decision/lease refs | mission spawned as www-data → `PermissionError` (Decision 1: CherryMe under /root) | fast worker 10.2 s |
| C continued by CherryMe (same request, run as root) | CherryMe RG/2 → RemotePlumMe → live service | ENSEMBLE decision logged in the live decision log (14:09:15Z); GAP question, 2 dispatches (llm7 codestral-latest); CherryMe stopped UNKNOWN: no live price source → BLOCKED/UNRESOLVED, no answer | 8.96 s |

## Concurrent acquisition (5 × plum_query_supply = full market screen, no model call, 3 repetitions; MCP session per call)
| | Before (old process) | After |
|---|---|---|
| sequential p50 / p95 | 178 / 200 ms | 126 / 166 ms |
| 5 concurrent, per call p50 / p95 | 752 / 772 ms | 542 / 557 ms |
| 5 concurrent, total | 781–829 ms | 586–621 ms |
Remaining (py-spy, live): screens still serialize on the single event loop; per screen 49 % static capability/role checks over ~2,900 offers (offers are mutated in place by discovery and the billing guard, so these verdicts cannot be cached by object identity), 11 % the requalify pass.

## Known-failure suppression
See the final report for the before/after window measured after deployment.
