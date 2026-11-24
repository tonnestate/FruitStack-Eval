# FruitStack runtime truth and critical path (2026-11-11, Phase 1)

Method: GitHub source first (tonnestate/Aurora `import/aurora-vps-source`, tonnestate/AnanasMe `main`), then the VPS runtime, then the
system's own records (Aurora interaction log, mission results, live PlumMe receipts). Provider calls made for this report: ONE
(`plum_run_neuron`, 2026-11-11T07:47:19Z, receipt_84d0f56d9135430f8307e39e6348c05a, failed MODEL_NOT_FOUND, INCLUDED, no cash).
Local measurements used a copy of `/var/lib/plumme` and an instant local stub gateway (no provider).

## A. RUNTIME_TRUTH

| Component | Running as | Source actually executed | Status |
|---|---|---|---|
| Owner entry (Aurora bridge) | `tonn-crm.service` gunicorn ×3, user `www-data`, `/var/www/tonnestate-crm/app/api/tonnair_bridge_api.py` | `/opt/fruitstack/integration/*` (no git). `interaction_lane.py`, `aurora_chat.py` = GitHub sha; `mission_facade.py`, `aurora_mission_worker.py` differ from GitHub | **BLOCKED** (see B1) |
| AnanasMe | not running (no unit, no process) | — | **PLANNED/not live** |
| L1 chat worker | new process per request: `/opt/fruitstack/venv-host/bin/python aurora_chat.py` | venv-host → editable `/root/fruits/sync/{PlumMe,CherryMe,PeachMe,AppleMe}` (mode 0700 parent `/root`) | **BLOCKED** |
| L2/L3 missions | new process per mission: `aurora_mission_worker.py` | same venv-host | **BLOCKED** (7/7 latest: PermissionError) |
| PlumMe shared service | `plumme-mcp.service` pid 34052, root, `:8791`, RSS 10.4 GB | `/root/fruits/sync/PlumMe-integration` `integration/stability-001` e0e68ca (pushed; not main) | **LIVE** |
| PlumMe native C11 pool | loaded in pid 34052: `/root/fruits/sync/PlumMe-integration/native/libplumme_pool.so` | — | LIVE in the service; **not on the Aurora path** (Aurora never calls the service) |
| fruitstack-longrunner | `/root/HANDOVER-002/live/fruitstack_longrunner.py` | — | running (not on owner path) |
| CherryMe / PeachMe / AppleMe / MangoMe / PhysalisMe / PomeloMe / CogC | only as libraries inside the per-request processes (MangoMe also as MCP worker servers for agents) | — | **not reachable by the service user** |

## B. CRITICAL_PATH_PROFILE (ranked by measured effect)

1. **The owner path does not run at all.** `sudo -u www-data /opt/fruitstack/venv-host/bin/python -c "import <component>"`: plumme/peachme/appleme/mangome ModuleNotFoundError, cherryme PermissionError (`/root/fruits/sync/CherryMe/cherryme/__init__.py`). The editable `.pth` files were rewritten 2026-11-09 15:37–18:32 to `/root/fruits/sync/*`. Aurora's own records: 13 interactions, both L1 = **DEGRADED** (1735 ms, 280 ms; canned "Chat-Modell nicht erreichbar"); 37 missions with result: **0 provider calls in all 37** — 30 BLOCKED/UNRESOLVED (from 2026-10-06, earlier cause, not re-diagnosed), 7 ERROR `PermissionError` (latest 2026-11-03).
2. **Most owner messages become missions.** 11/13 interactions classified L2 `ambiguous->up` (`interaction_lane.classify`: L1 only for greetings / "was ist…" / arithmetic; everything else ≥ L2 → new mission process, CherryMe inquiry, budget 4 questions, call_budget 2). This is the likely driver of the owner-observed ~20× when the path worked; not measurable now because no mission has reached a model.
3. **L1 worker design: cold process + full history replay per request.** Measured with an instant stub (5 runs): 1.41–2.11 s wall per request, of which imports 410–440 ms and `PlumMeService()` 810–860 ms (cProfile: `DecisionStore._replay` of the 18 MB `decisions.jsonl` 503 ms, policy replay 308 ms). Grows with history. Bypasses the warm service and the C11 pool.
4. **L1 route contract drift.** `aurora_chat.GatewayRoute` declares one NVIDIA route as `CostClass.PREMIUM` without text-generation capability; PlumMe 0.2.0 screen: `TEXT_GENERATION_UNKNOWN` → `NO_ELIGIBLE_NEURONS`. Even with imports fixed, L1 returns no answer.
5. **Warm-service selection picks a slow subscription CLI route for plain reasoning.** `plum_run_neuron` REASONING → `codex-headless > chatgpt-codex > gpt-6-luna` (INCLUDED, `local://codex-exec`, one CLI process per call): 10,259 ms then MODEL_NOT_FOUND; 12.2 s wall at the MCP client; failure receipt 87 KB (`alternatives`). Latency evidence since 2026-11-09 (successful calls): codex-headless p50 4,356 ms / p95 11,581 ms vs nvidia laguna-xs p50 1,009 ms, freellmapi qwen2.5-vl-72b p50 1,652 ms, kilo north-mini-code p50 1,771 ms.
6. **Background spend.** Live receipts, last 48 h: 31,516 provider attempts, **55.3 M tokens** (TRIAL_CREDIT 35.2 M, FREE_TIER 18.3 M, ANONYMOUS_FREE 1.1 M, INCLUDED 0.64 M, UNKNOWN 0.04 M). 2026-11-10: 32.6 M tokens of agent tool-action JSON (coding loops; the runner then hid models' own calls, see 4e06e34) + 4.4 M failed. Ongoing now: ~450 attempts/h from the service's own qualification/capacity loops (`PLUMME_QUALIFY_PER_CYCLE` default 12, owner order 2026-11-09), incl. 65/h failing UNKNOWN-cost llm7 attempts (missing API key) and TRIAL_CREDIT nvidia probes.

Matched direct-vs-L1 latency (target p50 ≤ 1.25×): **NOT MEASURABLE** — the L1 path returns no answer (B1, B4).

## C. LIMIT_REGISTER (executed owner path)

| Limit | Value | Where | Provenance | Effect / proposal |
|---|---|---|---|---|
| L1 output | `max_output_tokens=300`, system prompt "max. 3 Sätze" | `integration/aurora_chat.py` | convenience | answers mutilated by design; make task-dependent, let PlumMe apply route limits |
| L1 timeouts | adapter 5 s, wall 5 s, `wait_for` 6 s, facade `subprocess.run(timeout=7)` | aurora_chat.py, mission_facade.py | convenience | below codex-headless p50+start-up; any slow route → CHAT_TIMEOUT |
| L1 calls | `max_calls=2` | aurora_chat.py | convenience | fine once routes are eligible |
| L1 route | pinned NVIDIA gateway `:8317`, PREMIUM | aurora_chat.py | obsolete (pre-0.2.0) | violates FREE_ONLY default; refused by PlumMe 0.2.0 |
| Mission | `budget 4`, `call_budget 2` (L2) / `4` (L3) | mission_facade.py | bootstrap convention | fixed caps; replace by incremental ADD_WORKER/VERIFY/STOP (not done) |
| Lane split | L1 only on narrow regexes, `words>30`→L2, `>120`→L3 | interaction_lane.py | heuristic | sends ordinary chat to missions |
| Qualification output cap | 256 tokens per probe | live receipts | operational | fine for probes |
| AnanasMe history 10 turns / 3,500 chars, ACE 256..8192 vs 2,048 host ceiling | — | READMEs | not on a running path | NOT VERIFIED (AnanasMe not running) |

## D. INTEGRATION_MATRIX (live outcome)

AnanasMe→Aurora: no live process. Aurora→PlumMe: per-request library instance, never the shared service; blocked by imports. Aurora→CherryMe missions: blocked (PermissionError), 0 provider calls in 37 missions. PlumMe service→C11: loaded (process-local). CherryMe→PhysalisMe via PeachMe ToolGateway: no live caller found. MangoMe/AppleMe/PomeloMe/CogC on the owner path: unreachable (imports). FruitStack-Eval: offline only.

## F. E2E_ACCEPTANCE

FAST_TRACK_PASS NOT_PROVEN (B1, B4) · RESEARCH_PASS NOT_PROVEN (B1) · PHYSALIS_PASS NOT_PROVEN (no live caller) · RECOVERY_PASS NOT_PROVEN · EVALUATOR_PASS NOT_PROVEN.
100-worker pool capacity (live service, last 48 h): attempted routes 578, executed routes 69, canonical models 58, lineages 31 (heuristic), max successful calls starting within one second 4; authorized/administrative cap not measured.

## G. NEXT_ACTION (one)

Make the component sources readable by the service user without exposing `/root`: pinned checkouts (GitHub main commits) under `/opt/fruitstack/src/<Component>` owned root, mode 755; rewrite the venv-host editable `.pth` files to them; verify `sudo -u www-data /opt/fruitstack/venv-host/bin/python -c "import plumme, cherryme, peachme, appleme, mangome"`; then one owner L1 request through the bridge. **Production change — needs owner authorization.** L1 must then call the shared PlumMe service (B3/B4/B5), which needs an `aurora` MCP client whose token the service user can read — a credential grant, also owner-authorized.
