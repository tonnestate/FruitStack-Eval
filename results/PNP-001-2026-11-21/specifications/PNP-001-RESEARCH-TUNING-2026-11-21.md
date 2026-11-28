# PNP-001 research tuning - implementation order (owner approved all 5 measures, 2026-11-21)

Repository: /root/fruits/integration/Aurora-sync (git, branch cc/decision-contract, remote tonnestate/Aurora, private).
Code: integration/lab_tools.py (agent tool broker + session loop `session()`, ~line 766), integration/pnp_desk.py
(desk; `run_research(sid)` ~line 735 runs in a FRESH SUBPROCESS per research session -> changes to pnp_desk.py/lab_tools.py
used there take effect for new sessions without restart; `opportunities()` runs in the desk main process -> NOT active without restart).
Live staging state (read-only for tests!): /tmp/claude-0/-root/5714c268-5024-4035-86e9-ea07eff7a9fa/scratchpad/staging
(desk/state.json: verification_queue with claim states; desk/research/R*.menu.json; lab-tools-trace.jsonl; ledger via lab_tools.ledger()).

## Hard constraints
- Do NOT stop, restart or interrupt any running process or service (no systemctl, no kill). No pkill -f.
- No architecture change, no new service. Smallest diff in the existing files (+ at most one new module).
- PlumMe routing unchanged (no edits under /root/fruits/sync/PlumMe-integration).
- Tests never touch live state: use tmp_path / monkeypatch (see integration/tests/test_spec_read_delivery.py for the pattern).
- Run: /root/fruits/integration/physalis-mathverify/.venv/bin/python -m pytest -q integration/tests/test_spec_read_delivery.py
  integration/tests/test_discovery_contract.py (19 currently pass) - all must pass plus your new tests.
- Commit with "[skip ci]" in the message, push to origin cc/decision-contract. No GitHub Actions.

## Measure 1 - FINAL only after tool results
Problem: sessions R0698, R0700, R0702 ended with a FINAL written beside their own TOOL_CALLs ("provisional; pending tool results");
`session()` accepts a FINAL beside new calls from `min_turns` on, so the last results are never read.
Change: a FINAL in a turn that also requested calls is not accepted (unless it is the last turn); the host replies that the results
are now in the transcript and asks for the FINAL in the next turn. To keep the 2026-11-19 failure (sessions writing FINAL beside
calls every turn until the turn limit) from returning: after 2 such rejections in one session accept it as today.

## Measure 2 - persistent proof state per question
Problem: each session rebuilds from literature (last 30 min: 33 knowledge_search vs 3 physalis_code_run).
Change: one proof-state file per ledger question, e.g. <desk state dir>/proofstate/<Q-id>.json (append-only list of entries).
Two new desk tools for role RESEARCHER in lab_tools (DESK_TOOLS + ROLES + dispatch in `call()`):
- proof_state_read {question}: returns current lemma, last proved steps (with status), the open gap, refuted approaches.
- proof_state_update {question, lemma?, proved_step?, gap?, refuted_approach?, evidence?}: appends an entry (session id + model from agent).
RESEARCH_BRIEF (pnp_desk.py ~line 183): after choosing a question, call proof_state_read FIRST and continue at the recorded gap;
before FINAL record the new state with proof_state_update. session(): for role RESEARCHER, one host objection if a FINAL comes
without any successful proof_state_update (accept on the next FINAL regardless).

## Measure 3 - rank the menu by research yield, not activity
Yield per question and per model = verified general results (FORMALLY_VERIFIED) and validated counterexamples (FAST_REFUTED/REFUTED)
weighted above FINITE_CONFIRMED, per 100 research turns (data: state.json verification_queue `submitted_by` = ".../research/R....:<model>@...",
ledger iterations with mission "research/R....:" name the questions a session worked on, trace AGENT_TURN rows count turns).
There is a draft integration/productivity_report.py (untested) - reuse or replace it.
Apply in run_research() (subprocess, active without restart): reorder the OWNER PRIORITY menu lines: P2 questions first (ids in
/root/contracts/PNP-001-P2-DOSSIER-2026-11-21.md), then by yield; questions with zero yield after many sessions are NOT removed -
their line is tagged "no verified step after N sessions: change the approach or the model" (owner rule: widen, never prune).

## Measure 4 - author / adversary on every proved step
A proved_step recorded via proof_state_update gets status CLAIMED. proof_state_read shows unrefuted CLAIMED steps first with the
instruction: before extending, try to refute each (counterexample via lab, or name the exact gap in the argument), then record
status SURVIVED_REVIEW (with evidence) or REFUTED via proof_state_update. A session may not review a step its own session claimed.
Steps that survive go to submit_claim with a full `candidate.derivation` (existing discovery contract / Lean lane).

## Measure 5 - proof-critical turns to the strongest models by evidence
Client-side only (as the existing EXCLUDED_MODELS in lab_tools.py): compute per-model research statistics at session start (turns,
tool failure rate, confirmed results) and exclude a model from RESEARCHER/FAST_EVALUATOR turns when it has >= 200 turns in 24 h,
tool failure rate >= 20 % and zero confirmed results; nemotron-3.5-bolt-e4b stays excluded. The exclusion list and reason are written
to the trace. Measured 24 h (2026-11-21): claude-haiku-5-5 5 % failures / 89 FINITE_CONFIRMED; nemotron-3.5-bolt-e4b 22 % / 0;
nemotron-3-ultra-550b-a55b 17 % / 2; gemma-4-31b-it 30 % / 1.

## Deliverable
Commit hash, test output, and for each measure the exact functions changed. No report document.
