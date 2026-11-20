# Operational resilience - working state (order: CONTRACT.md here)

Inspection (unverified subagent inventory, re-check each file:line): `INSPECTION-subagent-2026-11-15.md`.

## Evidence added by Riemann run 6 (5fc8cfb1, 2026-11-15 21:46 CET, 2575 s, COMPLETED UNVERIFIED, no statement proved)
- 63 good / 45 failed research steps: NO_QUALIFIED_WORKER 16, NO_WORKER_SLOT 9, rate limited 8, unusable output 6, provider unavailable 2,
  timeout 2, CANONICAL_CONTEXT_CHANGED 1, CONTEXT_OVERFLOW 1 (a local 4B model leased for a research step).
- Root investigation and 8 of 11 branches ended NO_SECOND_SOLVER. From second 2273 on the pool was EMPTY: 11 lineages retired for the whole
  mission (also for one rate limit, one timeout), 11 more vetoed by tool evidence -> 7 branches "ran" with no worker in two minutes, the
  conjecture stage got NO_WORKER_SLOT. This - not the single failures - is the main operational defect.
- First live rescue injections: 4 x INJECT (mistral, qwen2.5, laguna, meta). Two were triggered in LSD stages with RECURRING_ERROR - check
  whether the errors were infrastructure (contract requirement: infrastructure failures must not use up the rescue allowance).
- Proof report: 49 entries, 12 added (11 approaches, 1 numerical evidence), nothing demonstrated. LSD ideas now include known equivalent
  formulations (Li coefficients, Robin's inequality); method chain SINGLE_METHOD.

## Existing structure to reuse (found 2026-11-16)
PlumMe already issues a structured failure receipt per failed lease execution (`PlumMe-supply/src/plumme/failure_receipt.py`,
`ExecutionResult.failure_receipt`, `service.py:1238-1290`): `failure_class` (RATE_LIMITED, QUOTA_EXHAUSTED, TIMEOUT, PROVIDER_DOWN,
CIRCUIT_OPEN, MODEL_ERROR, LOCAL_DENIED, BUDGET_EXHAUSTED ...), `raw_failure_class`, `retriable_same_worker`, `earliest_retry_at`,
`alternatives`, `state` (FAILED | NO_FREE_CAPACITY). PeachMe does not read it (no occurrence in peach-answer/src). It is the operational
event to hand on; no new event format is needed. The detail text of an unusable output (empty content / truncated / reasoning only) is not
in the receipt log - still to be found for D5.

## Done (all committed with [skip ci] on the feature branches; tests green; deploy status at the end of this file)
PeachMe `/root/fruits/integration/peach-answer` (cc/answer-claims):
- 6391d6b D1: a step waits for an occupied worker (`_slot_wait`, Condition `_free`, RESEARCH_STEP_WAITED); an idle worker that may never
  take the step gives up its place within the lease bound (`_rotate`).
- 47a0fa1 pool exhaustion: a lineage retired for a passing cause cools down (2 x REST_S) and returns once (`cooling`, `readmitted`,
  `_readmit`, RESEARCH_WORKER_READMITTED) - only where the host states the supply (missions; studies and strict pins keep their
  exclusions); an attempt that leased nobody is not a lease; branches are deferred when no worker can be had (`no_supply`,
  RESEARCH_BRANCHES_DEFERRED reason NO_WORKERS). D3: a worker whose stated context window cannot hold prompt + system skill + answer room is
  not asked (RESEARCH_WORKER_SKIPPED) - PeachMe side, from the leased route's own window; unknown windows are not judged.
- 217550c tool gateway: a call waits for the tool's own time limit (`timeout_s` argument, else the server's `tool_timeout_s`) + 45 s,
  bounded at 600 s (`_call_timeout`, MAX_TOOL_S). Cause found 2026-11-16: 16 agent experiments were cut at the flat 60 s.
- 0dd8170 a tool that did not answer (gateway TIMEOUT / SERVER_ERROR) does not count toward the worker's stall and is left out of the
  rescue evidence (`_tool_unanswered`).
- 9a1660d D2: CANONICAL_CONTEXT_CHANGED / STALE_PREPARED_ENVIRONMENT (raised before dispatch) -> the turn is prepared again, twice at most
  (RESEARCH_STEP_REPREPARED).
AppleMe `/root/fruits/integration/apple-refuted` (cc/refuted-held-answers): f3844b7, 730d649, 9862e64 - `appleme/operations.py`
(`classify`, `is_operational`, `tool_infrastructure`, `diagnose(events)` -> status HEALTHY | RECOVERED | DEGRADED | ESCALATE, incidents by
component and failure with recovered / unrecovered, recovery actions, consequences, escalation codes RESEARCH_HALTED, NO_WORKERS,
NO_SECOND_SOLVER, UNRECOVERED_FAILURES); `cognitive.py`: operational ATTEMPT_FAILED codes are no REPEATED_ERROR / STALLED_INVESTIGATION.
Aurora `/root/fruits/integration/Aurora-sync` (cc/decision-contract): 5efd6bb registry `tool_timeout_s` 120 for PhysalisMe; 6df32da
`operations_report`, record / result field `operations`.
AnanasMe `/root/fruits/integration/AnanasMe-perf`: 5aa452d, e485731 - lines "Betrieb", "Selbsthilfe", "Eingriff nötig"; `_SAFE_FIELDS`.

## Still open
- D5 (cause known, not fixed): reasoning uses up the per-response output limit (finish_reason=length, no answer). In run 6 only 6 research
  steps (limit 2000 / 800); the 42 other receipts were PlumMe's own 256-token probes. Fix: PlumMe `_execute_with_continuations` retries once
  with a wider per-response limit when the cut answer was reasoning only - but PeachMe's `reserve_tokens` (= max_total_tokens) must leave
  room for it. Both sides, one change each.
- D4: ROUTE_NO_LONGER_ELIGIBLE is not in `scheduler.FAILOVER_CLASSES` (6 cases in runs 2-5, none in run 6). PeachMe now treats it as a
  passing cause (cool-down + return); a PlumMe-side reselect is still missing.
- From the capability audit: repeat a NO_SECOND_SOLVER investigation once; re-ask an unusable triage once.
- PlumMe's `failure_receipt` (`retriable_same_worker`, `earliest_retry_at`) is still not read by PeachMe; the rest / cool-down times are
  PeachMe's own constants.
- Observation, not acted on: `/root/.plumme/failure_receipts.jsonl*` is ~7 GB and grows ~10 MB per hour without missions (PlumMe's probes).

## Deploy status (2026-11-16 ~03:00 CET, no mission worker running, rollback lines in /root/contracts/longrun-2026-11-15/ROLLBACK.txt)
LIVE: PeachMe-9a1660d, AppleMe-9862e64, AnanasMe-e485731 (page app.js?v=e485731), Aurora aurora_peach_runtime.py = 6df32da.
Verified as www-data: modules import from the live releases, `operations_report` answers, services active.
Riemann run 7 started 03:00 CET to check the repairs on real work: output `/root/contracts/longrun-2026-11-15/riemann-mission20.out`
(look for RESEARCH_STEP_WAITED, RESEARCH_WORKER_READMITTED, RESEARCH_WORKER_SKIPPED, `operations` in the mission record, and whether the
investigations still end NO_SECOND_SOLVER).

## Update 2026-11-16 ~04:10 CET - run 7 and what it exposed
Riemann run 7 (6d828e6c, 1316 s, BLOCKED / UNVERIFIED): 30 good / 42 failed steps; 31 x PRICE_NOT_VERIFIED. Two workers (dva/kimi-k3-high,
minimax-m2.7) were leased on routes without a verified price; PeachMe's existing cost rule (`cost.py`, unchanged - owner 2026-11-15: no
change to cost code) refuses each dispatch, the code was not a known failure, so the workers stayed live and blocked the pool; 10 of 11
investigations had no second solver. Both wordings of the final answer were cut at the 800-token limit inside the model's reasoning.
Repaired and LIVE (PeachMe-d2d9c8b, AppleMe-e1fbbfd, AnanasMe-b38703a, page ?v=b38703a; Aurora unchanged 6df32da):
- 051222f: the cost rule is asked before the step is spent; a worker it refuses is skipped and retired without using a replacement.
- d2d9c8b: a reply cut at the output limit (step ledger: output tokens = limit) is repeated once on the same model with 4 x the limit,
  at most 8000 (RESEARCH_STEP_WIDENED, SYNTHESIS_WIDENED). This closes D5 on the PeachMe side; no PlumMe change.
Full PeachMe suite: 493 tests, only the 10 known test_pomelo_effect_bridge failures.
OWNER DECISION OPEN: PlumMe admits routes of unknown price (provider paywall decides), PeachMe still refuses them (PRICE_NOT_VERIFIED).
With the repair they no longer block missions, but those model families are lost to the research. Lifting the refusal is a change to
cost code and needs the owner's explicit word.
Riemann run 8 started ~04:10 CET: output `/root/contracts/longrun-2026-11-15/riemann-mission21.out`.

## Update 2026-11-16 ~05:00 CET - run 8 and what it exposed
Riemann run 8 (4377b0a0, 3336 s, COMPLETED / UNVERIFIED, nothing proved): 35 good / 8 failed steps (run 7: 30 / 42). The run-7 repairs
held: 4 workers skipped by the cost rule before a step was spent, 8 replies cut at the limit repeated wider (7 then answered), the final
wording answered on the wider repeat, the root investigation had a second solver (stop LOOP_GUARD_ROUNDS), 3 conjectures. Proof report 63
entries, 4 added (3 hypotheses, 1 numerical evidence).
New defects, repaired at the source and LIVE (PhysalisMe-c261036, PeachMe-308dc69; AppleMe-e1fbbfd, AnanasMe-b38703a, Aurora 6df32da unchanged):
- PhysalisMe service blocked from minute 18 to the end (and after it): PARI `lfunzeros` crashed in a worker thread (stack overflow at the
  8 MB default -> segfault caught by cysignals), the next PARI call deadlocked the process with the interpreter lock held. 9 tool calls
  waited 165 s each (~25 min), no branch was opened (RESEARCH_BRANCHES_DEFERRED DEADLINE, 17 remaining). AppleMe reported it correctly
  (TOOL:physalisme NO_ANSWER 9 unrecovered -> ESCALATE UNRECOVERED_FAILURES).
  Fix c261036 (`/root/fruits/integration/physalis-mathverify`, cc/physalis-math-verification): `independent.number_theory` runs each call
  in a child process (`python -m physalisme.independent`), 100 s at most; a crash / hang / backend error is that call's answer. PARI stack
  may grow to 1 GB. `zeta_zero_count` range lowered from 5000 to 1500 (measured: 1000 = 13 s, 1500 = 48 s, 2000 > 85 s - PARI, not Arb).
  sd_notify watchdog thread + unit drop-in `/etc/systemd/system/physalisme-mcp.service.d/watchdog.conf` (WatchdogSec=300): a blocked
  service is restarted by systemd. Tests: 191 passed (run with the service venv:
  `PYTHONPATH=src /opt/fruitstack/venv-physalis/bin/python <script that appends /root/fruits/integration/.venv-fs-test/lib/python3.11/site-packages to sys.path and calls pytest.main>`).
  Verified as www-data over the socket: four parallel calls answer, a refused height returns the tool's own message.
- PeachMe 308dc69: the tool loop names its worker by lineage (`independence_key`), `_pick` matched model keys only -> a solver's loop was
  continued by another worker and 8 workers were rotated out (ROTATED_FOR_ELIGIBLE_WORKER) to make room; now the lineage is resolved to
  the live worker. The wider repeat is bounded by the worker's context window (one repeat came back CONTEXT_WINDOW_EXCEEDED).
  Full PeachMe suite: 499 tests, only the 10 known test_pomelo_effect_bridge failures.
Not done (noted): the tool gateway has no circuit for a server that stopped answering (each call still waits its full limit); the
watchdog bounds the outage to ~5 min instead.
Helper: `/root/contracts/longrun-2026-11-15/run-riemann.sh <N>` starts one Riemann mission through the full stack and prints the evaluation.
Riemann run 9 started ~04:55 CET: output `/root/contracts/longrun-2026-11-15/riemann-mission22.out`.
- PeachMe a6c98c4 (committed, NOT yet live - deploy after run 9 with `deploy.sh peachme`): tool gateway liveness check - after two
  unanswered calls in a row to one server (TIMEOUT / SERVER_ERROR) a 15 s `list_tools` check precedes the next call (`_silent`, PROBE_S);
  a dead server costs 15 s instead of the full wait, a restarted one is used again. Full suite 500 tests, only the 10 known pomelo failures.

## Update 2026-11-16 ~06:00 CET - run 9 confirms the repairs
Riemann run 9 (7d97fd76, 3376 s, COMPLETED / UNVERIFIED, nothing proved): 63 good / 14 failed steps; 53 tool calls, none unanswered
(30 called, 16 rejected as malformed, 7 answered with the tool's own error); root investigation + 2 branches, all with a second solver
(run 6: 8 of 11 without, run 7: 10 of 11); operations status DEGRADED, no escalation (run 7 and 8: ESCALATE); no worker rotated out for a
tool loop; 4 wider repeats; final wording on the wider repeat. Rescue: 2 injections, both NEW_EVIDENCE (first observed effect), 2 x
ESCALATE (one agent stuck again after its one injection, one model without a successful tool step). Proof report 71 entries, 8 added
(3 hypotheses, 3 numerical evidence, 2 approaches), nothing demonstrated; method chain SINGLE_METHOD.
Remaining operational observations (not repaired):
- 11 branches not opened: research deadline (the wall budget, owner: not to be changed). The root investigation alone took 30 min.
- 2 x CONTEXT_OVERFLOW: specialist models with an unstated window were leased for research steps (nvidia/nemotron-parse-2.0,
  openai/gpt-oss-20b); both recovered by replacement. PlumMe side: such routes should state their window or not be offered for REASONING.
- 4 of 8 rate limits unrecovered within their stage (the stage ended before the rest was over).
LIVE now: PeachMe-a6c98c4 (incl. the gateway liveness check), PhysalisMe-c261036 + watchdog, AppleMe-e1fbbfd, AnanasMe-b38703a, Aurora 6df32da.
