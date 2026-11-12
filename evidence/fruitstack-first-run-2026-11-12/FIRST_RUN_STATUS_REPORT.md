# FRUITSTACK FIRST-RUN STATUS REPORT

Version FR/1, 2026-11-12, host tonnestate.de (Linux 5.15), Claude Code session 5714c268. Read-only inspection plus offline test runs;
no source, configuration or deployment was changed for this report. Preserved before any implementation work of the mandate
"FruitStack OGI-013: Complete Integration, Improve Organizational Intelligence, and Establish Scientific Advantage".

## A. Repository and deployment inventory

| repo | GitHub default @ SHA | open PRs | installed runtime (what really loads) | repo vs runtime |
|---|---|---|---|---|
| CherryMe | main @ e118dbe (2026-11-12) | #3 | venv-host editable `/root/fruits/sync/CherryMe` @ e118dbe, clean | same commit; **unreadable for www-data** (missions) |
| PlumMe | main @ d73e2f0 (2026-11-09) | #31 #30 #29 #28 #14 #10 #6 #5 | service `plumme-mcp` = `/root/fruits/sync/PlumMe-integration` branch integration/stability-001 @ 0af278d (only on PR branch #31, not main); venv-host library @ d73e2f0 | **service ≠ main**; two PlumMe versions live |
| PeachMe | main @ 4d1a2ba | #42 | venv-host editable @ 4d1a2ba, clean | same; not on the Aurora mission path |
| AppleMe | main @ aca5f8b | #2 | venv-host editable @ aca5f8b (9 tracked .pyc dirty); stale `/opt/fruitstack/releases/AppleMe-current` dir @ 66ad8dd | www-data loads **66ad8dd**, not aca5f8b |
| MangoMe | main @ f9fcb63 | #5 | MCP worker `/root/tonnestate-repos/MangoMe` @ 8a69f30 (= PR #5 head) | runtime ahead of main (PR open) |
| OrangeMe | main @ c0beb27 | #5 #1 | not installed in venv-host or any MCP venv; used only in eval workspaces (`/root/fruits/ogi-final/OrangeMe` @ c0beb27) | not in any live path |
| PomeloMe | main @ 054bf47 | #1 | venv-host editable `/root/tonnestate-repos/PomeloMe` @ b62f64b | runtime **behind** main |
| CogC | main @ 0934376 | – | skill copies (`/root/.claude/skills/cogc`, `/root/.codex/skills/cogc`); `cherryme/cogc.py` imported by engine | same |
| FruitStack-Eval | `web/claude` @ 6d36774 (default branch is not main); main @ a3cc090 | #25 #22 #8 #6 #5 | venv-host editable `/root/tonnestate-repos/FruitStack-Eval` @ ab6cabe (ancestor of main, README dirty) | runtime behind main |

Deployment truth: `deployment/fruitstack-drift-check.py` (Aurora `076071e`) reports **7 drifts**: CherryMe/PlumMe/AppleMe not importable
as www-data from the mission PYTHONPATH (PermissionError / ModuleNotFoundError / stale release), Aurora facade, worker and MangoMe link
not at `cf63044`, no system-test verdict. Repair is staged (`deployment/install-core-releases.sh`), denied twice for the agent by the
auto-mode classifier; owner must run it.

## B. Capability status (one primary status each)

| component / capability | status | evidence |
|---|---|---|
| Aurora deep mission (CherryMe→PlumMe→AppleMe) | **BROKEN** | 38 result files since 2026-10-04: 0 COMPLETED, 30 BLOCKED (9 with 0 provider calls), 8 ERROR (all `PermissionError` since 2026-10-07); reproduced as www-data |
| CherryMe Brother Mode / adversarial rounds | INTEGRATION TESTED | executed in S1/QA-2D and tau2 pilots (FSE evidence); 909/910 unit tests |
| CherryMe Research Tree, backward decomposition | IMPLEMENTED / UNVERIFIED | `research_tree.py` exists; `ResearchTree(` is constructed nowhere outside its module, not in Aurora worker or FSE runners |
| CherryMe LSD room, continuity | IMPLEMENTED / UNVERIFIED | `lsd_room.py`, `continuity.py` imported by no other module |
| CherryMe KnowledgeStore (negative knowledge, reuse) | INTEGRATION TESTED | worker wiring tested (Aurora tests); F3-DEV: 18 findings published, 0 reused |
| CherryMe problem-context snapshot + CogC | IMPLEMENTED / UNVERIFIED | `problem_context_runtime` used by `brother.py`; no run evidence with CogC |
| CherryMe lineage-aware independence | UNIT TESTED | `independence_key` in 10 modules; no live measurement |
| PlumMe discovery, qualification, receipts | VERIFIED LIVE | `/root/.plumme/receipts.jsonl` 102 MB; last 3000 receipts 2026-11-12, 64 % success |
| PlumMe provider diversity (gateway concentration) | VERIFIED LIVE (resolved at receipt level) | last 3000: nvidia 1065, freellmapi 1052, ovhcloud 528, groq 197, llm7 74, pollinations 73 (2026-10-14 before repair: 57/57 kilo-gateway) |
| PlumMe cost/token accounting | BROKEN for task-level accounting | last 20000 receipts: cost_usd null 18217 (91 %), input_tokens null 7549 (38 %), **0** carry mission/task/work attribution in metadata |
| PeachMe session governance, parent/child budget | UNIT TESTED | 379 passed; live only in eval tau2 path (2026-11-11 episodes produced no patch); not on Aurora path |
| AppleMe trajectory assurance | INTEGRATION TESTED | events present in F3-DEV runs; effect on outcomes never measured |
| MangoMe work/checkpoints | INTEGRATION TESTED | eval episodes write TEAM_* checkpoints; Aurora link `aurora_mangome.py` tested against real in-memory service; live mission path BLOCKED (www-data cannot reach MangoMe) |
| OrangeMe ledger/handoffs | INTEGRATION TESTED | per-episode memory in eval runs; KIwiMe dispatcher (PR #2) tested; no live path |
| PomeloMe effects | IMPLEMENTED / UNVERIFIED | integrated in eval code arm; no executed effect found |
| CogC compilation | UNIT TESTED | 27/28 tests; compile 20–50 µs measured 2026-11-11; raw-vs-summary-vs-CogC comparison never run in FruitStack |
| FruitStack-Eval grading, seals, blind export | INTEGRATION TESTED | used in DEV pilots 2026-10-14; registered pilot never run |
| OGI-013 confirmatory study | BLOCKED | QA-2D v2 closed `CLOSED_INFRASTRUCTURE_INFEASIBLE`; S0 rows: 99 (86 graded) and 132 (114 INFRA) |

## C. OGI-013 integration boundaries

| boundary | expected | actual | verified by | outcome | corrective action |
|---|---|---|---|---|---|
| 1 CherryMe→PlumMe child inference | every worker call via the PlumMe service with receipts | `RemotePlumMe` in worker; FSE runners use PlumMe AUTO | code + receipts | works in eval, broken in Aurora (imports) | run install-core-releases.sh |
| 2 PeachMe parent/child budget | child calls reserve/settle against parent | implemented (ParentBudget, #37/#39) | unit tests | not live on mission path | wire only if a mission path needs PeachMe; measure in eval |
| 3 receipt/usage reconciliation | every call → receipt with tokens, cost or UNKNOWN | receipts exist; cost null = UNKNOWN (allowed), tokens null on 38 %, task id never in metadata | receipt scan | **gap: attribution** | Aurora sets `mission_id` (live after repair); FSE runners must stamp `run_id/task_ref` |
| 4 UNKNOWN / interrupted execution | UNKNOWN never counted as 0 | F3-DEV analyzer mapped null cost to 0 "only to run the tool" (documented) | report text | partial | analyzer must keep UNKNOWN |
| 5 authorization/policy | owner→mission→agent→action | PeachMe #42 not merged; PlumMe host admission `shadow` | config | not enforced | after shadow log review |
| 6 AppleMe intervention | diagnose + act | events recorded; intervention effect unmeasured | F3-DEV | unmeasured | ablation in pilot |
| 7 MangoMe state | mission = work + checkpoint | code ready (`AURORA_MANGOME=off`) | tests | not live | owner decision: MangoMe as local service |
| 8 OrangeMe handoffs | durable, delivered, processed distinguished | ledger only; delivery ≠ processing not modelled | code | gap (unverified) | – |
| 9 PomeloMe effects | all side effects through PomeloMe | no effect bound | code | not integrated | first real effect |
| 10 FSE independent verification | deterministic grader blind to arm | `fse inquiry grade` | DEV runs | works | – |

## D. First-run test results (offline, installed commits, python 3.12 venv `/root/fruits/ogi-final/.venv`, `pytest -q`)

| suite @ commit | result | note |
|---|---|---|
| CherryMe e118dbe | 909 passed, 1 failed, 1 skipped | `test_the_learning_audit_states_what_actually_runs`: assumes Keras absent; this venv has Keras (environment, not defect) |
| PlumMe 0af278d (live service) | 1006 passed, 6 skipped | |
| PeachMe 4d1a2ba | 379 passed, 1 skipped | |
| AppleMe aca5f8b | 136 passed | |
| MangoMe 8a69f30 | 272 passed, 12 skipped | |
| OrangeMe c0beb27 | 20 passed, 1 failed | `test_cli_validates_inputs_without_mutation` (known pre-existing) |
| PomeloMe b62f64b | 13 passed | |
| CogC 0934376 | 27 passed, 1 failed | GitHub mirror layout ≠ visible skill (packaging) |
| FruitStack-Eval ab6cabe | 170 passed | |
| Aurora `integration/tests/test_system_test.py` | 4 passed | |

All of these are unit/offline tests with fakes or in-memory stores. **No genuine end-to-end evidence exists for the current
installed stack.** Logs: scratchpad `baseline/*.log` (session-local); commands in this section.

## E. Scientific evidence status

| claim | experiment | n | comparator | result | status |
|---|---|---|---|---|---|
| independent research improves correctness | F3-vs-AUTO-CONTROL-DEV (2026-10-14) | 50 draft tasks | single AUTO call, same retrieval | F3 9/50 vs control 37/50; F3−control −0.56 [−0.74, −0.42] | NOT YET DEMONSTRATED (opposite observed, exploratory) |
| adaptive model selection improves outcomes | – | – | – | – | NOT YET DEMONSTRATED |
| multi-model collaboration > single model | QA-2D v2 | 53 questions | SL single Luna | SL 41/53, SN 39/53, T 36/53, E 36/53; closed infra-infeasible | NOT YET DEMONSTRATED |
| progress monitoring reduces waste | – | – | – | – | NOT YET DEMONSTRATED |
| context compression preserves quality | COGC-OMNIROUTE-EVAL-003 (2026-09-19) | 96 runs | no CogC | +9 % single-agent effect, outside FruitStack | NOT YET DEMONSTRATED in FruitStack |
| persistent memory improves multi-session work | F3-DEV | 18 findings | – | 0 reused | NOT YET DEMONSTRATED |
| budget enforcement prevents unaccounted execution | receipt scan | 20000 | – | cost unknown 91 %, no task attribution | NOT YET DEMONSTRATED |
| FruitStack > Anthropic reference | – | 0 | – | never run | NOT YET DEMONSTRATED |

## F. Blockers

| P | blocker | verified? |
|---|---|---|
| P0 | deep missions cannot import their components as www-data; repair script ready, agent denied by classifier | verified |
| P0 | no receipt carries a task/mission attribution → per-task tokens/cost not reconstructable from PlumMe alone | verified |
| P0 | integrated chain abstains under free supply (F3-DEV 31/50 abstentions: FORBIDDEN 61, RATE_LIMITED 51, SEMANTIC_OUTPUT_FAILURE 37, BILLING 27) | verified 2026-10-14; current rate unknown |
| P1 | pilot preconditions: 50 references not owner-approved (`tasks/dev/pilot_inquiry_tasks_DRAFT.jsonl`, drafted by Claude), salts with owner, arm A needs cost approval | verified (PILOT_PROTOCOL.md) |
| P1 | Anthropic reference arms A/B need Claude Opus/Sonnet calls: paid or subscription routes that require owner approval (Sol/Opus only with owner approval, 2026-11-11) | verified (policy) |
| P1 | Research Tree / LSD room / continuity never on a runtime path → their ablation is impossible until wired | verified |
| P1 | PlumMe service runs a branch that is not main (stability-001, PR #31) | verified |
| P1 | owner order 2026-11-11 "no further live runs" vs this mandate; I treat the mandate as lifting it for FREE_ONLY runs only | interpretation, stated |
| P2 | CogC mirror test, OrangeMe CLI test, CherryMe Keras-environment test | verified |
| P2 | FSE default branch is `web/claude`, not main | verified |

## G. Immediate execution plan

1. **Aurora mission path** — owner runs `sudo bash /root/fruits/integration/Aurora-sync/deployment/install-core-releases.sh`; acceptance = system test PASS (`/var/lib/aurora/system-test.json`), drift check 0. Blocked on owner.
2. **Receipt attribution (PlumMe/FSE)** — verify that FSE runners and the Aurora worker stamp `run_id/task_ref/mission_id` into PlumMe call metadata and that it reaches the receipt; smallest fix in the caller (no new component). Test: one receipt with attribution. Can proceed now.
3. **Exploratory baseline rerun** (Phase 3) — rerun `F3` vs `AUTO control` on the 50 DEV tasks with today's stack, FREE_ONLY, same runners as 2026-10-14, independent grader; measures whether the abstention bottleneck persists. Can proceed now (free).
4. **Abstention bottleneck** (Phase 4/5) — from the rerun's receipts, classify why verification lacks delivered answers; fix inside CherryMe/PlumMe only if measured.
5. **Wire Research Tree** only when an experiment needs it (ablation G7).
6. **Arms A/B, registered pilot, confirmatory G8** — need owner: reference approval + salts, Claude model/cost approval.

## H. Gate snapshot

| gate | status | basis |
|---|---|---|
| G1 repository/runtime integrity | FAIL | 7 drifts; PlumMe service off-main; stale AppleMe release |
| G2 real end-to-end execution | FAIL | 0 completed missions; last integrated eval run 9/50 |
| G3 complete accounting | FAIL | 0/20000 receipts attributable to a task; tokens null 38 % |
| G4 independent verification | NOT TESTED (on current stack) | grader exists and worked in DEV runs |
| G5 organizational continuity | NOT TESTED | |
| G6 pilot completion | BLOCKED | references not approved; arm A cost not approved |
| G7 causal evaluation | NOT TESTED | |
| G8 confirmatory advantage vs Anthropic | BLOCKED | no approved Claude reference budget |
| G9 reproducibility | NOT TESTED | |
