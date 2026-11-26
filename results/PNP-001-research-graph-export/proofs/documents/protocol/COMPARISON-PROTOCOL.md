# PNP-001 comparison protocol and knowledge history (fixed before the first comparison; owner addendum 3, 2026-11-16)

Version 1, written 2026-11-16 before iteration 1 ran. Changes after this point are appended with date and reason, never overwritten.

## 1. What is compared

| Arm | Who works | Process |
|---|---|---|
| O (organisation) | FruitStack as deployed: idea room, Brother Mode with independent model lineages, conjecture stage | unchanged |
| S (single frontier model) | ONE frontier model, named by the owner, for every role | the same stages: it solves, then criticises its own solution, then revises - as many rounds as arm O's loop guard allows |
| O+ (optional, owner decision) | arm O with the same frontier model admitted as one of its workers | unchanged |

Arm S is not "one model call". It gets the full research process with itself in every role; only the independence of the workers is
removed. This isolates organisation (several independent lineages) from process (critique and revision) and from model strength.
The frontier model is NOT chosen by Claude and not by "strongest free model". Until the owner names it and authorises its use (a
frontier model in PlumMe's market is a subscription route), arm S does not run and no collaboration gain is reported.

Known confound, stated openly: Claude (itself a frontier model) writes the requests and the digests for every arm. Both arms receive
byte-identical requests; Claude takes no part in solving inside an arm.

## 2. Fixed for every arm of one comparison

- Task: the same request file (sha256 recorded), the same problem ledger state at start (copy taken before the first arm runs).
- Tools: the same tool catalogue and limits (PhysalisMe through the gateway; code sandbox; SAT tool; proof tools).
- Resources: the same wall-clock budget, and the same ceiling on model calls and on output tokens. The ceiling is set from arm O's
  run of the same iteration (measured calls and tokens), so the arms are matched on what was actually spent. Recorded per arm:
  calls, input / output tokens, wall time, tool calls.
- Order and repetition: one run per arm per iteration to start with; with a single run nothing is called significant. A difference is
  reported as an observation until it repeats over iterations.

## 3. Evaluation (independent of the agents' own verdicts)

Scored from the mission records by a script and by re-execution, never from an agent's claim about itself:

| Measure | How it is established |
|---|---|
| Statements PROVED | only the host's proof tool / kernel verdict counts (physalis_verify_claim, Lean / Isabelle / Rocq artefacts re-checked) |
| Finite certified results | SAT models re-checked against every clause, UNSAT with a checked DRAT proof, counts reproduced by a second method |
| Hypotheses REFUTED | the counterexample is re-executed by the host; a refutation without a reproducible object does not count |
| False claims | statements an arm reported as supported that fail re-execution or the proof tool |
| Rediscoveries | statements that follow from the seeded known results or are found in the literature (check by Claude, arm identity hidden) |
| New statements surviving | not refuted, not a rediscovery, exact statement with quantifiers; listed, never counted as theorems |
| Cost | calls, tokens, wall time per verified item |

The literature / novelty check is done on statements stripped of the arm that produced them. The owner's reading is the final
independent check; Claude's assessment is labelled as such.

## 4. Five questions answered after every iteration (owner's table)

1. Mathematics - was a new, checked statement found?
2. Research - which hypotheses were refuted, which new questions arose?
3. Learning - did this iteration measurably profit from the previous one? (statements that cite an earlier candidate id; refuted
   hypotheses not proposed again; share of work spent on already-settled items)
4. Organisation - was Brother Mode better than the single model at equal budget? (only when arm S ran)
5. Frontier model - what did only the frontier model solve, what did the stack solve without it?

## 5. Knowledge history (traceability across iterations)

One append-only file `../ledger/candidates.jsonl`; one JSON object per event, never edited. Fields:

- `id` (C-0001 ...), `event` (PROPOSED | REFORMULATED | TESTED | REFUTED | SUPPORTED_FINITE | PROVED | LITERATURE | PI_DECISION),
- `iteration`, `arm`, `mission_id`, `node` (the stack's research-tree node id), `at`,
- `statement` (exact, with quantifiers), `parents` (candidate ids this one was derived from),
- `by` (model lineage and stage: idea room perspective, solver, critic, reviser, conjecture stage),
- `evidence` (tool receipt ids, experiment ids, proof artefact paths), `counterexample` (the explicit object, or the receipt that holds it),
- for PI_DECISION: `action` (PURSUE | DROP | SPLIT | MERGE | HOLD) and `reason` in one or two sentences, written by Claude when the
  next request is composed.

Sources of these events: the mission's `research_tree.jsonl` (hypotheses, derived-from edges, contributions with lineage, failed
attempts), `tool_receipts.jsonl`, the record's proof ledger delta, and Claude's digest. The digest of iteration N names the candidate
ids it carries into the request of iteration N+1, so a lemma of iteration 4 can be followed back to the idea of iteration 1, the
brother who changed it and the counterexample that shaped it.
