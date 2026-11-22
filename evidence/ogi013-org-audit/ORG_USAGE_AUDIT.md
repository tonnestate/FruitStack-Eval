# OGI-013 organisation-usage audit (2026-10-27, from executing code + c1 traces; c2 addendum pending)
Sources: runners/ogi013_tau2_agent.py, c1 fruitstack-events.jsonl (40 arms), component inventory (CherryMe/PeachMe/PlumMe/PomeloMe/AppleMe/MangoMe/OrangeMe).
Reading aid: facts below are from code and logs; interpretation is marked.

## What the "organisation" in the experiment actually is
- Both arms call exactly one organisational mechanism: cherryme.brother.run_rounds(n_solvers=1, review_single=True, max_rounds=2): a draft, one reviewer from another lineage,
  critique, revision, tie-break. FIXED runs it on every valid action (91 organised calls in c1); ADAPTIVE only when the action is a write tool or a human transfer (13 calls).
- Q1 agents/competences activated: only model lineages as workers (draft author + reviewer). No responsibility nodes, no competence-scored staffing, no specialist roles.
- Q2 decomposition/distribution: none. No task was split. (CherryMe triage/responsibility graph unused.)
- Q3/Q4 second-agent gain / error caught: in c1 organised calls, issues were raised in 8/13 (ADAPTIVE) and 39/91 (FIXED) calls and a revision followed in 7 / 36, but 0 of
  all contribution rows are VERIFIED (all UNVERIFIED or DISSENT). Whether any critique changed the official outcome is NOT established by c1: the only 3 successes (tasks 6,13,19)
  occurred in both arms, and ADAPTIVE solved 6/13/19 with 0-2 escalations. No causal credit to the review mechanism is possible from c1.
- Q5 strategy replacement: not implemented (no recovery/strategy switch beyond per-step retry and format retry). Q6 organisational knowledge stored/reused: none; logs show no
  memory/knowledge read or write (OrangeMemoryAdapter wired, never queried; KnowledgeStore unused). Q7 structure change from difficulty/results: none (activation is a static rule).
- Q8 existing but unused (exist as code, not called by the runner): CherryMe RG/2 responsibility graph (responsibility.py: make_node/accept_delegations/next_action/consolidate),
  choose_ensemble competence staffing (ensemble.py:357), KerasOrchestrator/KerasEnsemblePolicy, KnowledgeStore + KnowledgeFirstGrounder (knowledge.py), RecoveryCoordinator and
  WorkerBehaviorMemory (recovery.py/behavior.py), organization_record (engine.py:195), PlumMe acquire_workforce/fan/run_room, MangoMe delegation, EvidenceVerifier/FALSIFY.
- Q9 why unsolved despite many agents: c1 = 27/34 failing arms cut by the sensor fault (see CAUSES_AND_INTEGRITY.md), so the organisation seldom reached a decision that mattered.
- Q10 waste: FIXED spent ~4x the escalations and provider calls for the same 3 successes (descriptive; confounded by AUTO model mix and earlier stops in ADAPTIVE).

## Conclusion (technical, not yet scientific)
The current ADAPTIVE arm is a static write-gated peer review, i.e. "FIXED with a trigger rule". It does not exercise the specified FruitStack organisation capabilities.
A FIXED-vs-ADAPTIVE null result with this arm says nothing about adaptive organisational intelligence. c2 answers only the sensor-fix question and stays unchanged.

## Integration gap to repair (next, separately pre-registered; no second engine)
CherryMeEngine (claim inquiry with RG/2, ensemble staffing, knowledge store, recovery) is claim/evidence oriented; the tau2 agent is a turn-level tool dialogue.
Smallest real bridge: express each consequential decision point (a write tool, a policy question, a repeated failure) as a CherryMe claim with environment-observed evidence
(tool results, policy text) and let CherryMeEngine under responsibility_runtime() decide staffing (1..n workers via choose_ensemble over PlumMe competence), falsification
(FALSIFY with independence groups), recovery and knowledge persistence (KnowledgeStore across tasks), with activation decided by its own triage/need signals, not a write rule.
Conditions for the follow-on study (pre-register before running): SINGLE (one model, no org), FIXED (always peer review, equal pool/budget), ADAPTIVE (RG/2 bridge), plus ablations
(no dynamic staffing, no mutual review, no persistence, no recovery) on the same tasks, simulator model pinned per task across all arms, agent-model pool controlled/recorded.
