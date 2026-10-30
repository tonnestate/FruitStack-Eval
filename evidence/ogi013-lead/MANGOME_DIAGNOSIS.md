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

---
# Repair log (owner/lead order 2026-10-30; MangoMe branch `fix/dirty-source-provenance-2026-10-30`)

## D4 — dirty source (done)
- Backup before any change: `/root/backups/mangome-dirty-2026-10-30/` (tracked.diff, stash0.patch, stash.list, nested_src_MangoMe.tar, the untracked test, status.txt) with `SHA256SUMS`:
  `3aa6c66a…a912d tracked.diff`, `c5b580e0…aa947 stash0.patch`, `08cbe3bc…aa947 nested_src_MangoMe.tar` (full list in the backup folder).
- Failing test first: `tests/test_mcp_service_api_contract.py` on a clean `git archive HEAD` copy fails with `TypeError("_Service.prepare_assignment() got an unexpected keyword argument 'work_id'")` (reported as `INPUT_INVALID`). The committed advanced MCP tools forwarded `work_id`/`turn_id` that the service does not accept. Fix = the previously uncommitted `mcp_server.py` change, now committed with the test (`6424c04`).
- The nested untracked copy `src/MangoMe/` (179 entries, stale duplicate) was removed from the working tree after backup; the stash `codex-uncommitted-vor-handover-001` is untouched (not dropped).
- Provenance now: component checkouts used by the evaluations are logged with `git describe --always --dirty` and a `-dirty` tree refuses to start (`DIRTY_SOURCE`, `ogi013_host_bootstrap.py`, test `tests/test_ogi013_dirty_source.py`). The evaluation component link `ogi013-org-components/MangoMe` now points to a pinned clean worktree `ogi013-mangome-pinned` (detached at the fixed commit), and the host Python is reinstalled editable from it (`mangome-mcp 0.3.23`).
- Note for earlier evidence: "MangoMe source was dirty; logged commit does not identify the code that ran" (applies to every run logged `mangome=98009461…`).

## C.1 deployment check (raw outputs in `evidence/ogi013-lead/mangome-c1/`)
| check | result |
|---|---|
| `mangome health` | OK, version 0.3.23, schema 6, database `mangome` state `BOUND` (`health.txt`) |
| `mangome` on PATH | not on PATH; only in the managed venv `bin/` (used by absolute path) |
| `importlib.metadata.version('mangome-mcp')` in the managed venv | **0.3.17 (stale dist-info) while the code is 0.3.23** -> defect; fixed by `uv pip install --no-deps -e <source>` (now 0.3.23) |
| source commit imported by the managed runtime | `/root/tonnestate-repos/MangoMe` at `98009461…` when checked (dirty), now branch `fix/dirty-source-provenance-2026-10-30` |
| `mangome attest-client claude-code`, workspace `/root` | `CLIENT_READINESS_FAILED: SKILL_VERSION_MISMATCH` (installed skill text older than the source) -> defect; fixed with `mangome doctor --repair --workspace /root --client claude-code` (backup of the skill and `~/.claude.json` in `/root/backups/`); afterwards `PASS`, warning `MONGODB_CREDENTIAL_SOURCE_MISSING` (default loopback, no credential file: informational) |
| `mangome attest-client claude-code`, workspace = the FruitStack-Eval worktree | `CLIENT_READINESS_FAILED: MCP_NOT_REGISTERED, SKILL_NOT_INSTALLED, AUTOMATIC_INSTRUCTIONS_MISSING, CONFIGURATION_NOT_EFFECTIVE` -> the binding is per workspace; the operator's session binds at `/root` (PASS). Not repaired in the worktree (project-scope files would be written into the evaluation repository). |
| Mongo integration tests (real MongoDB, loopback) | `tests/test_mongo_integration.py`, `tests/test_mongo_wire.py`: all pass (7 before, 9 after the new tests) |
| MCP transport behaviour (H6) | not tested in this pass (client/transport concern, out of MangoMe scope per order) |

## H5 — `families.admission_key` (confirmed, fixed)
Real MongoDB: second keyless family -> `E11000 duplicate key ... index: admission_key_1`. Fix `9dc334f`: partial unique index on string values (`families_admission_key_string_unique_v1`), legacy sparse index dropped by the index bootstrap, keyless families omit the field, `scripts/migrate_admission_key_index.py --collection families`. Tests: two keyless families coexist; migration over a legacy index with an explicit null keeps both documents.

## H1-H3 regression tests on real MongoDB (`f7a1295`, `tests/test_mongo_host_regressions.py`)
- H1: two concurrent processes, own database and own turn each, 15 authorization re-reads each: both stay authorized; `claim_database` refuses a name held by a live process (`DATABASE_IN_USE`) and releases dead holders. (No failure reproduced: the historical collision remains unidentified.)
- H2: a second host run on the same work: `RECONCILE_ASSIGNMENT` returns MATCHED with the same WorkIdentity; WorkIdentity count stays 1.
- H3: failing before the fix (`recommended_next_action` was `RETURN_TO_USER`). Now `RECOVERY_CONTEXT` on admitted work returns `BIND_OR_RECONCILE_CURRENT_TURN`, `current_turn_execution_authorized: false` plus a next-step text; `ENTER_WORK` with `work_ref` binds a current EXECUTE turn without a CONTROL `BIND_WORK_TURN`.
- Full suite: memory backend all pass; with `MANGOME_TEST_MONGO_URI` all pass.
