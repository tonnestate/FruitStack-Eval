# D. FruitStack installed-system inventory (2026-11-14)

Method: read-only. Operational state (systemd, /opt/fruitstack, /root/.plumme) is source of truth; repos are history. No tests run, no secrets read
(`/root/.plumme/runtime.env` deliberately not opened; the PlumMe service env `PLUMME_EXTRA_SKILL_DIRS` could not be confirmed, see 3).
Status vocabulary: PRESENT (live and imported on live path) / PARTIAL / DOCUMENTED_ONLY / ABSENT. "UNVERIFIED" = not confirmed by me.
Paths: `R=/opt/fruitstack/releases`, `I=/opt/fruitstack/integration`, `PI=/root/fruits/sync/PlumMe-integration`.

## 0. What is installed and live

Services active (2026-11-14): plumme-mcp (127.0.0.1:8791, since 07:06 today), fruitstack-longrunner, ananasme@www-data, freellmapi-3101, omniroute-donor-20128, aurora-stt.
Timers: aurora-kiwime-recovery, aurora-receipt-verifier, fruitstack-system-test, plumme-acceptance, plumme-models-refresh.
FAILED units: fruitstack-truth-writer.service, run-u1258/1260/1261/1262.service (ogi-final venv runs).

| Component | `*-current` target | Live use |
|---|---|---|
| CherryMe | `R/CherryMe-029ed42` (installed 06:54 today) | imported by Aurora mission worker via PYTHONPATH (`I/mission_facade.py:485-493`) |
| PeachMe | `R/PeachMe-b4bd852` | same (mission.py, research.py, tool_gateway.py) |
| PlumMe client | `R/PlumMe-c0e7edd` | mission worker (PYTHONPATH `AURORA_PLUMME_SRC`, mission_facade.py:488) |
| PlumMe MCP service | NOT `R/`: `PI` (commit 823e867, 2026-11-13) via `/root/.local/share/tonnestate-mcp/plumme/bin/python` | systemd plumme-mcp. `diff -rq` shows `R/PlumMe-current` differs from `PI` (execution_view.py only in PI; service.py, receipts.py, mcp_server.py, diagnostics.py differ): client and service are not the same build |
| AppleMe | `R/AppleMe-05767c8` | via PeachMe `appleme=True` default |
| MangoMe | `R/MangoMe-8a69f30` | mission worker PYTHONPATH |
| OrangeMe | `R/OrangeMe-366b450` | mission worker |
| BlueberryMe | `R/BlueberryMe-ddd8f79` (policies/eu-business.yaml, mission_facade BBM_POLICY) | mission worker |
| AnanasMe | `R/AnanasMe-eeab9c8` (15 old releases kept) | ananasme@www-data.service |
| KIwiMe | `R/KIwiMe-cb64748` (= repo `/root/fruits/kiwime-work/KIwiMe-recovery` HEAD cb64748, 2026-11-14) | timer aurora-kiwime-recovery; `I/kiwime_recovery.py` |

Aurora integration (`I/`): mission_facade.py, aurora_peach_runtime.py, aurora_chat.py, aurora_mission_worker.py, interaction_lane.py, fruit_adapter_registry.py,
grounded_search_adapter.py (LiveWebSearchAdapter), kiwime_recovery.py, aurora_voice*.py. Dozens of `.bak-*` copies sit in the live dir.

Python environments: `/opt/fruitstack/venv`, `venv-3.11.16`, `venv-host`, `venv-voice` have NO pip. Mission worker runs `venv-host/bin/python` (mission_facade.py:95).
venv-3.11.16 site-packages (listed): appleme 0.1.1, cherryme_private 0.2.5 (old), plumme 0.1.7 (old), mcp 2.2.0, pydantic, jsonschema, httpx, cryptography. No numpy/keras.

### Other components (path, commit, live import?)
| Component | Real location | HEAD | Imported by live path? |
|---|---|---|---|
| PomeloMe | `/root/fruits/fsi6/PomeloMe` (main 054bf47, 2026-11-07, 1 dirty); `/root/tonnestate-repos/PomeloMe` (b62f64b, 2026-10-05, 2 dirty); editable install under `/root/.local/share/tonnestate-mcp/pomelome` (pomelome-0.1.0) | | NO. Only `R/PeachMe/src/peachme/pomelo.py` (duck-typed `PomeloEffectBridge(gateway, authority_provider, plan_provider)`; needs a host-supplied gateway). No bridge construction in `I/*.py` (grep). Seam/offline only. |
| PhysalisMe | `/root/fruits/ogi-final/PhysalisMe`, `/root/fruits/fsi6/PhysalisMe` (main 448a3b1, 2026-11-07, clean); `/root/.local/share/tonnestate-mcp/physalisme` is a venv skeleton with no physalisme package | | NO on Aurora mission path. Referenced only by KIwiMe (`kiwime/physalis_export.py`, `research_bridge.py`). Needs numpy (pyproject), absent from live venvs. Tools physalis_discover/profile/correlations/explore/analyze/claim_gate = statistical exploration, not solvers. |
| KIwiMe | `/root/fruits/kiwime-work/KIwiMe-recovery`, release R/KIwiMe-cb64748 | cb64748 | YES host-side via recovery timer; not in mission research path (other hooks UNVERIFIED) |
| CogC | repo `/root/CogC` (0934376, 2026-10-10, 5 dirty); installed `/root/.claude/skills/cogc/scripts/compile_context.py` exists | | PARTIAL, see 6 |

## 1. Organization selection

| Mechanism | Status | Evidence |
|---|---|---|
| CherryMe triage (single vs multi) | PRESENT, LLM-judged | `R/CherryMe-current/cherryme/triage.py:1-100` (CHERRY-TRIAGE/1,/2); invoked `engine.py:925-956` (`_triaged_context`), gated by `_needs_triage` (`engine.py:918`, mode "auto"): runs only if claim CONFLICT, >1 judged verdict, earlier failure, or importance >= top band; else `SKIPPED_SIMPLE_TASK` (no call). Enabled live by `responsibility_runtime(triage="auto", ...)` at `I/aurora_peach_runtime.py:184`. |
| Features used | | Triage model sees only claim text (<=4000 chars) and objective (<=1000) (triage.py prompt_for); returns single_worker_sufficient, task_class (extraction/computation/diagnosis/synthesis/other), challenge, independent_verification, specialist_skill, optional free responsibilities. Pre-gate uses claim status, evidence verdicts, importance. Parse failure -> single PRIMARY. |
| research_decision | PRESENT | `R/PeachMe-current/src/peachme/research.py:67-85`; used live `I/aurora_peach_runtime.py:80-84,203`. None if claims settled, no parsed triage record, or all triage answers "single yes, no challenge, no verify". Else ResearchPlan(lsd=challenge, risk HIGH/MEDIUM). Only feature: triage record. No score, no cost term. |
| EVC / value of computation | ABSENT as code | grep 'EVC\|value of computation\|expected value of' over R/*-current, I/*.py, PI/src: only comments in `cherryme/problem_context_runtime.py:3,75`, `problem_context_snapshot.py:326,360` stating they do NOT implement EVC. /root/AGENTS.md (OGI-013 decision) = documented future work. |
| Keras ensemble policy shadow | PARTIAL (shadow only) | PI `keras_model.py` (316 lines, KERAS_BACKEND=jax, PLUMME-KERAS-MQ-MODEL/1, gate_verdict can only say "shadow scoring permitted"); `service.py:218` KerasShadowPolicy, `:739-745` optional `load_keras_shadow_model` (whether a trained model is loaded live: UNVERIFIED); `mcp_server.py:222,334` reports SHADOW_ONLY. The plumme-mcp venv site-packages (listed) has no jax/keras/numpy, so a trained scorer likely cannot load there (inference from package list). Proposals never change selection. |
| interaction_lane | PRESENT | `I/interaction_lane.py:36-60`: regex cues -> L0 CONTROL / L1 CHAT / L2 COGNITIVE / L3 MISSION; >120 words -> L3, >30 -> L2; ambiguity falls upward; used `I/mission_facade.py:15,353`. German-only cues. No calibration. |
| room_activation / problem_assessment | DOCUMENTED_ONLY on live path | `cherryme/room_activation.py`, `problem_assessment.py` ("PROPOSAL"); imported only by problem_contract.py / each other; no import from engine.py, brother.py, `I/` or PeachMe (grep). |
| Calibration vs outcomes | PARTIAL, off the decision path | PlumMe worker competence: Beta-Bernoulli posterior, admission by credible lower bound (PI `competence.py:1-30`, config/qualification_policy.json); `/root/.plumme/competence.jsonl` 354 rows, `decisions.jsonl` 136 rows. Selects WORKERS, not organization size. Triage/research decision is NOT calibrated: no code compares triage output to outcomes. Eval-side `fruitstack_eval/calibration.py` is offline. |
| Observed live behaviour | | fse-eval006b HEAD 90b7cda: "triage skipped research in all 18 missions" (PILOT-B addendum 3, stopped at 9/40 tasks, not graded). |

## 2. Deterministic execution before LLM

| Mechanism | Status | Evidence |
|---|---|---|
| claim_check RECOMPUTE | PRESENT | `cherryme/claim_check.py:1-60`; `engine.py:207 check_claims`; called before any model by PeachMe `mission.py:117` (`_check_claims`, default `claim_check=True`). Plain-integer `a op b = c` only; stdlib; wrong -> REFUTED, pure correct arithmetic -> SUPPORTED (`objection_check.py:91 recompute_arithmetic`). |
| COMPUTED_CHECK | PRESENT, model-formulated | `claim_check.py:267 check_claim`: quorum=2 workers from different independence groups write boolean assertions; host evaluates with restricted AST evaluator (numbers, arithmetic, round/abs/min/max/is_prime). File states its limitation: both workers can formulate the same wrong check. Consumes LLM calls. |
| Aurora pre-filter | PRESENT | `I/aurora_chat.py:120,150` META_CLAIM regex drops meta statements before claim extraction (max 3 claims). |
| PomeloMe deterministic tools | ABSENT on live path | PomeloMe = effect authorization/receipts, not a solver. |
| PhysalisMe tools | ABSENT on live path | see 0. |
| Solvers in live venvs | ABSENT | importing sympy, z3, flint, pyproj, osgeo, shapely, mpmath, numpy, keras fails in venv, venv-3.11.16, venv-host; system python3 has no sympy; `which lean z3 gdalinfo` empty. Only stdlib arithmetic. (pip absent, so import test used instead of pip list.) |
| Solvers elsewhere | research-only | `/root/fruits/research/erdos64`: pure-python CNF/CEGAR/DRUP checker; pysat, cadical, kissat, drat-trim not found. Referenced only by evidence script `R/CherryMe-current/evidence/cai_repair_live/run.py:33`. |

## 3. Capability / tool catalogue

| Item | Status | Evidence |
|---|---|---|
| PlumMe skills | PRESENT, coarse | `plum_skill_status` -> `service.skills.doctor()` (PI mcp_server.py:127; skills.py:80) = required-skill readiness per role. `/opt/fruitstack/skills/SKILL_CATALOG.json`: 135 entries {skill_id, source: ruflo, source_revision, path, collision, available, active_by_default: false}; ruflo skills are generic `agent-*` markdown stubs ("Agent skill for coder - invoke with $agent-coder"). Built-in: PI `default_skills/{falsify,provoke,reasoning,reuse,science}`. `PLUMME_EXTRA_SKILL_DIRS` read at `config.py:255`; whether live service sets it to /opt/fruitstack/skills/ruflo: UNVERIFIED (/proc environ gave no match; runtime.env unread). |
| Capability metadata | PARTIAL | RoleSpec (models.py:164): role_id, description, skill_ids, allowed_tools, allow_external_side_effects, quality_gates. RouteOffer has cost_class (PREMIUM/INCLUDED/ANONYMOUS_FREE/UNKNOWN). No version, determinism, latency or I/O-contract fields on skills. |
| ToolGateway registry | PRESENT in code | `R/PeachMe-current/src/peachme/tool_gateway.py`: host-pinned registry {servers:{name:{command,args,cwd,env,env_allowlist,tools:{tool:declaration}}}}; declaration keys read in `request_for` (~44-58): effect_class, external_effect, credentials_required, data_egress, sensitive_data, estimated_cost_usd, estimated_tokens. Undeclared tool = IRREVERSIBLE, never autonomous. `autonomy.decide` (autonomy.py:99) is the pure policy. No purpose/IO/version/determinism/latency fields. |
| Registry live? | PARTIAL / UNVERIFIED | `ResearchPlan.registry` default None = no tools; Aurora `plan_kwargs` (`I/aurora_peach_runtime.py:201`) passes no registry, web or analyses -> Aurora research uses no ToolGateway tools. Web search goes through `I/grounded_search_adapter.py` in the PlumMe adapter list (fruit_adapter_registry.py). |
| PomeloMe effect authorization | DOCUMENTED_ONLY / seam | peachme/pomelo.py; providers must be host supplied; not constructed in `I/`. |
| Deferred schema loading | PARTIAL | `ToolGateway.discover()` lists tools with full input_schema at call time (tool_gateway.py ~64-80): on-demand discovery but all schemas at once. PlumMe MCP exposes ~45 tools, no lazy tool search. |

## 4. Verification separation

| Mechanism | Status | Evidence |
|---|---|---|
| Claim freezing / amendment | PARTIAL | `Question`, `AgentCard` frozen dataclasses (models.py:143,165); claim status changes only via `ClaimStore.apply_investigation -> derive_status` (claim_check docstring; engine.py:207). No explicit claim-amendment API or spec-hash freeze found (grep amend/frozen in engine.py/state.py/models.py). FruitStack-Eval freezes studies by seal/hash (`study_gate.py`, `seal.py`), offline. |
| Executed-check evidence path | PRESENT | `peachme/research.py:98-` `Consolidation`: executed check once per distinct candidate (`_check`, ~121); SUPPORTS->SUPPORTED, CONTRADICTS->FALSIFIED; failing/malformed verifier = `VERIFIER_FAILED`, never evidence (`_check_result` line 88). Labels VERIFIED/UNVERIFIED/REFUTED (~331). |
| verifier vs check_author | PRESENT in code, not wired in Aurora | `ResearchPlan.verifier`, `check_author` (research.py:43-49). Aurora `plan_kwargs` (aurora_peach_runtime.py:201) sets neither -> live research decisions carry `unresolved: NO_EXECUTED_CHECK` (research.py ~314), UNVERIFIED unless claim_check settled earlier. |
| Generated checks never feed competence | PRESENT | `_TRUSTED_KINDS = ('HOST_VERIFIER',)` research.py:64, enforced `_feedback` research.py:346; task-derived check adds `CHECK_IS_TASK_DERIVED_NOT_COMPLETE`. PlumMe competence demotes to DIAGNOSTIC when verifier is the model itself, HELDOUT, or ensemble credit lacks lineage (competence.py:1-30). |
| Self-reported success refusal | PRESENT | `cognitive.py:9,153` majority counts and self-reported confidence are IGNORED inputs; engine.py:2171 stores confidence as "self_reported"; lsd_room.py:870 uses OUTCOMES, not self confidence. |
| Receipts | PRESENT | PlumMe `/root/.plumme/receipts.jsonl` (65,542 lines), rotated failure_receipts; PeachMe ToolGateway hash-chained fsynced JSONL with `verify_journal` (tool_gateway.py:63-76, `_append` ~170-186), mirrored to MangoMe; OrangeMe ledger = git store (gitstore.py:101-108 checks branch/origin; chain integrity not verified by me); timer aurora-receipt-verifier exists (content UNVERIFIED). |
| Non-vacuity | PARTIAL | META_CLAIM filter (aurora_chat.py:120,150). claim_check requires every claim number in an assertion, every number sourced from task/claim, one side computed, covers_whole_claim. No general "can this check fail" negative control. `code_checks`/stub validation: no match in PeachMe/src (grep). |
| FruitStack-Eval study_gate | OFFLINE ONLY | `/root/fruits/integration/fse-eval006b`, branch cc/superiority-evidence-2026-11-14, HEAD 90b7cda; `fruitstack_eval/study_gate.py` (grader_run, record_outcome, exact_mcnemar, bootstrap analyze, ContractError); also calibration.py, ope.py, protected.py, independence.py, power.py. Not imported by Aurora. |

## 5. Generator-verifier-reviser loops and stopping

| Mechanism | Status | Evidence |
|---|---|---|
| Brother Mode stops | PRESENT | `cherryme/brother.py`: MAX_CONSECUTIVE_FAILURES=3 (line 27); stop_reason CONVERGED / NO_ISSUES / NO_CHANGE / LOOP_GUARD_ROUNDS / LOOP_GUARD_FAILURES / NO_SECOND_SOLVER / CONTROL_FINISH / DEADLINE (54, 218-281, 402-472). Defaults n_solvers=2, max_rounds=2 (research.py:33-36). Pre-processing refusals not counted as failures (185,342). |
| AppleMe NO_PROGRESS | PRESENT, advisory | `R/AppleMe-current/src/appleme/engine.py:41,555,678`; advisory handed to CherryMe `apply_advice`, `advice_rounds=1` (research.py:50). |
| Repair loop | PRESENT | `Consolidation.repair` research.py:232; recorded as decision `repairs`. |
| Failure admission/labels | PRESENT | basis EXECUTED_EVIDENCE / SPECIALIST_ADJUDICATION / EARLIEST_UNREFUTED / BEST_REFUTED; `unresolved` flags ALL_CANDIDATES_REFUTED, SEVERAL_SUPPORTED_CANDIDATES, VERIFIER_FAILED:n (research.py:288-320). |
| Preserve failed attempts | PRESENT | research_tree.py:9,158-161,251: FALSIFIED nodes kept as qualified negative knowledge; ExperienceLibrary (peachme/experience.py:50); cherryme/experience.py:40-50 relations REFUTED_UNDER_ASSUMPTIONS / FAILED_UNDER / INVALIDATES; failed nodes retrieved as "possibly reusable" (experience.py:355). Live: `tree_path` and `learning: experience` in plan_kwargs (aurora_peach_runtime.py:201). |

## 6. Context efficiency

- `cherryme/cogc.py` is NOT the CogC skill: a local visibility-policy packet compiler ("CHERRY-COGC/1": GROUNDED/REASONING/PROVOCATION hide origin answer, others' opinions, evidence verdicts; cogc.py:52-75, docstring "mirrors CogC's compile contract at a smaller scope"). Used by engine.py:11,2024. PRESENT as role-visibility, not compression of large outputs.
- Real CogC skill: `cherryme/coupling.py:59,154-185 compile_with_cogc` shells out to `/root/.claude/skills/cogc/scripts/compile_context.py` (exists) with explicit `fallback:tree-knowledge`; used inside problem->solution Coupling reassessment (whether on the Aurora live path: UNVERIFIED; `problem_context_runtime.py` is imported at brother.py:158). PARTIAL.
- Worker -> lead: PeachMe returns a typed PEACH-DECISION/1 dict; check summaries cut with `_short` (160/240 chars); tool errors cut to 500 chars (tool_gateway.py:78,190); per-call `max_output_tokens=2000` (research.py:46). MCP tool results returned in full (no size cap seen in `_result_data`).
- PlumMe MCP sizes: `plum_market_status` was ~16 s / ~400 MB receipt scan per call; fixed in PI commit 823e867 (2026-11-13, "0.3 ms"). Service restarted 2026-11-14 07:06, presumably includes it, but I did NOT call it (UNVERIFIED). Response is a monolithic dict (mcp_server.py:93-97), no pagination; `plum_keras_rooms` limit capped at 100.
- No spill-to-file or summarize-on-overflow for large tool output found in PeachMe/CherryMe.

## 7. Parallelism

- Brother Mode: ThreadPoolExecutor(max_workers=max(1, max_workers, n_solvers)) (brother.py:307-314); brother default `parallel=False` (152) but PeachMe `ResearchPlan.parallel=True`, `max_workers=3` (research.py:27-28), width passed at research.py:602-608. LSD Room perspectives run concurrently under the same pool. Consolidation uses an RLock so parallel critics write the hash-chained tree one at a time (research.py:106-111).
- Hard bounds: max_workers live workers; max_workers + max_replacements(2) leases per run (research.py:403,453); one run budget carved across child sessions (434). Budgets default NO_CEILING (accounted, no cap); Aurora uses NO_CASH_BUDGET (aurora_peach_runtime.py:84).
- Claim checks: `asyncio.gather` over claims (engine.py ~226-232).
- PlumMe: native pool lib `libplumme_pool.so`, lease fence, capacity fence (native_pool.py, lease_fence.py, capacity_fence.py); per-route limits in route_capacity.sqlite3 (values not inspected).

## 8. Mathematical / geographical / ZOMBIE work state

- "Project ZOMBIE": no project by that name found. In memory, ZOMBIE = a PlumMe bug (codex client `scope_file` in `/root/.plumme/mcp_clients.json` pointing at a 1-route grant; memory/fruitstack_recovery_2026-11-11.md:16; fix awaited owner go; current live state not re-checked). Greps of contracts/, memory dir, fruits/{integration,sync,research} for 'ZOMBIE' hit only Aurora mission-control app.js/apache conf; broader grep over fruits/ timed out (not exhaustive).
- Math: (a) `/root/fruits/research/erdos64` (HEAD 2ac9f42, 2026-11-08): Erdos #64 methods study with own CNF, CEGAR, DRUP checker, prior-art certificate checker; README: "methods study and reproduction, not a mathematical result"; pure python, offline, certified static n=9. (b) `/root/fruits/research/eg-paper-upstream` (Ducoffe-Dumitru Erdos-Gyarfas verification code, upstream copy). (c) `/root/fruits/ogi-tasks/data/math-500` dataset (FruitStack-Eval fixtures). None on Aurora live path; no competition-style (IMO/Putnam/Lean) pipeline; no formal prover installed.
- Geographical competition (GeoGuessr/image geolocation): not found (ABSENT as far as searched; greps over memory/contracts/frontier/research hit nothing before partial timeouts, not exhaustive). Only GEO hits are marketing GEO (memory tonnestate_geo_*.md) and TonnEstate map contracts (`TE-GEO-MAP-001-*`, `TE_GEO_EXTRACT_001.md`; real-estate). No GDAL/PROJ/pyproj installed.
- `/root/fruits/frontier/` holds copies of CherryMe (027fcc6, 2026-11-08) and OrangeMe-isolation, not competition work. `/root/contracts/frontier-2026-11-14/` has A/B/C notes from sibling tasks.

## 9. Live defects / hygiene observed

1. fruitstack-truth-writer.service failed; run-u1258/1260/1261/1262 failed (ogi-final runs).
2. Live PlumMe MCP service source (PI 823e867) differs from `R/PlumMe-current` (c0e7edd) used by the mission worker; old plumme 0.1.7 / cherryme_private 0.2.5 remain in venv-3.11.16.
3. Aurora research path supplies no verifier/check_author/registry (aurora_peach_runtime.py:201): no executed check, no tools; results end UNVERIFIED with NO_EXECUTED_CHECK. Triage skipped research in 18/18 pilot-B missions.
4. EVC, Keras active selection, room_activation/problem_assessment, PomeloMe, PhysalisMe are not on the live decision path.
5. Triage, claim_check formulation and lane cues are LLM- or German-regex-bound; the research decision is uncalibrated.
6. The 135-entry ruflo catalogue is generic persona stubs (active_by_default false); no purpose/IO/determinism/latency metadata.
7. Many `.bak-*` files in the live integration directory.
