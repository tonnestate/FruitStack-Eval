# MANGOME_DIAGNOSIS (read-only, 2026-10-30; no MangoMe code was changed)

Versions: MangoMe 0.3.23 (MCP `mangome_status`), source `/root/tonnestate-repos/MangoMe`, branch `main`, HEAD `9800946`, schema 6, canonical database `mangome` (MongoDB, loopback), 4 managed `worker_mcp_server` processes, 0 stale, trust boundary MTB/2 LOCAL_HOST.

## What works (reproduced)
- `mangome_status` -> `ok: true`, `database_ready: true`, `canonical_indexes_ready: true`.
- Unit tests: `cd /root/tonnestate-repos/MangoMe && MANGOME_BACKEND=memory PYTHONPATH=src <host python> -m pytest -q -p no:cacheprovider tests` -> every test passes except 6 skipped (Mongo-marked tests need `MANGOME_TEST_MONGO_URI`, not configured; the Mongo paths are untested here).
- The FruitStack stack binds MangoMe in-process: `ogi013_tau2_agent.py:140,174` (`mangome.runtime.get_service()`, `MangoWorkAdapter`); every episode needs host-admitted `OGI013_WORK_REF/TURN_ID/ACTOR_ID/PROJECT_REF` (`Stack.project`, `Episode.__init__` -> `bind_turn_authority`). PeachMe re-verifies the turn authority at every context read. Episodes start and run, so this path functions today.

## Numbered defects / findings

### D1. Evaluation work is invisible to the canonical MangoMe (isolated database by configuration)
- Evidence: `ogi-013-collab1/env.sh` sets `MANGOME_DATABASE=mangome_ogi013_collab1 MANGOME_BACKEND=mongo`; the MCP server serves database `mangome`.
- Reproduction (MCP): `mangome_query WORK_CONTEXT {"work_ref":"01M5W4V5PRCXDWPFATSTZ46ZMZ"}` -> `KeyError: unknown work identity 01M5W4V5PRCXDWPFATSTZ46ZMZ`; `mangome_query PROJECT_OVERVIEW {"project_ref":"WS-CA6D7A081C41"}` -> `INPUT_INVALID: unknown project WS-CA6D7A081C41`.
  In-process against the isolated database the same work resolves (`get_service().work_context(OGI013_WORK_REF)` returns the WorkIdentity).
- Impact: the work ledger the MCP/agents see has no record of any evaluation episode. Not a code defect; an earlier order required isolation. Whether evaluations should write to the canonical database is a decision for the owner/lead.

### D2. Coding and team episodes never write to MangoMe's work graph
- Evidence: `checkpoint_continuity` (`ogi013_tau2_agent.py:304`, calls `fs.mango.checkpoint(...)`) is invoked only from the tau2 path (line 631). `ogi013_code_task.py` and `ogi013_team_code.py` never call it. Event log of `dev04` and `gdev1-crash` runs: `CONTINUITY_CHECKPOINT` count 0 and 0.
- Isolated database collections (read via pymongo): `work_checkpoints` 3, `work_identities` 10, `work_turn_bindings` 16, versus dozens of coding episodes since `4d75a49`. The only durable record of those episodes is each run's `fruitstack-events.jsonl`.
- Impact: MangoMe is used as an authority gate (work identity + active turn), not as an event ledger, for the coding/team driver. Repair would be in the FruitStack driver (frozen by the owner's stop order), not in MangoMe.

### D3. One WorkIdentity and one turn for every episode
- Evidence: all 9 `EPISODE_OPENED` events across the development runs carry `"work": "01M5W4V5PRCXDWPFATSTZ46ZMZ"` (single `work.env`).
- Impact: no per-episode work identity; episodes cannot be told apart in the MangoMe graph. Same repair scope as D2 (driver/launcher).

### D4. The MangoMe source used by evaluations is not a clean commit (provenance mismatch)
- Evidence: `OGI013_SOURCE mangome=98009461693d...` is printed by every run, but `git -C /root/tonnestate-repos/MangoMe status` shows `M src/mangome/mcp_server.py`, untracked `src/MangoMe/` (a nested stale copy of the repository; its `mcp_server.py` differs from `src/mangome/mcp_server.py`), untracked `tests/test_mcp_service_api_contract.py`, and a stash `codex-uncommitted-vor-handover-001`. `$CR/MangoMe` (the components symlink used by the runs) resolves to this live working tree.
- The tracked modification removes the `work_id`/`turn_id` parameters from `mcp_server.prepare_assignment` and `begin_work`. At HEAD those parameters exist in the advanced MCP server, but `service.GovernedMangoMeService.begin_work/prepare_assignment` have no such parameters (checked with `inspect.signature` on a clean `git archive HEAD` copy: tool-only params `turn_id`, `work_id`). I could not trigger a runtime `TypeError` because `prepare_assignment` is blocked earlier by `WORK_IDENTITY_ADMISSION_REQUIRED` for a legacy family; the mismatch is therefore a reproduced signature inconsistency, not a reproduced crash.
- Impact: results cannot be reproduced from the logged commit hash; the working tree contains uncommitted behaviour.

### D5. MCP argument shape is easy to get wrong (usability, not a fault)
- Reproduction: `mangome_query {operation: WORK_CONTEXT, work_ref: ...}` (top-level) -> `INVALID_CAPABILITY_ARGUMENTS: missing a required argument: 'work_ref'`; the same call with `payload: {"work_ref": ...}` works. The worker surface takes `operation` + `payload` (`worker_mcp_server.py:541`).
- Impact: low; a misleading message for an unknown top-level key.

## Which FruitStack paths depend on MangoMe, and what happens there today
| path | dependency | state today |
|---|---|---|
| `Stack.__init__` (`get_service`, `MangoWorkAdapter`) | in-process MangoMe service on database `mangome_ogi013_collab1` | works |
| `Episode.__init__` (`bind_turn_authority`) | admitted WorkIdentity + active turn from `work.env` | works; single shared work/turn (D3) |
| PeachMe context reads | re-verifies turn authority each read | works |
| `Episode.checkpoint_continuity` | MangoMe `checkpoint_work` | used only by tau2 runs; not by coding/team runs (D2) |
| canonical MCP (`mangome` database) | none from FruitStack | not connected (D1) |

## Needs an architectural change?
No defect found so far needs a MangoMe architectural change. D1 is a deployment/config decision; D2 and D3 are driver/launcher changes (not MangoMe); D4 is a repository hygiene fix (decide which working-tree content is intended, commit it with a test, remove the nested copy); D5 is cosmetic.

## Proposed repair scope for 3b (not started; awaiting the report)
- D4 only, in the MangoMe repository on a new working branch: failing test first (an assertion that the MCP tools' parameters match the service signatures they forward to), then commit the intended `mcp_server.py` change. D1-D3 need an owner decision because they touch the frozen driver or the isolation rule.
