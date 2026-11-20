# Scientific Discovery Enforcement — implementation report (2026-11-20)

Owner DIRECTOR COMMAND "Scientific Discovery Enforcement". Basis: RH evidence archive FruitStack-Eval `cc/rh-evidence-archive-20261120`
@ `e47ed7a681b521c1fe13a0c881bf8e20b617d519`.

## 1 RH failure mechanisms (from the archived records) and where they come from
| # | Record | Code path |
|---|---|---|
| F1 | 25 of 44 APPROACH entries: `NOT_INVESTIGATED`, "no second agent was available for an independent solution" | `cherryme/brother.py:222-224, 399-404` stops with `NO_SECOND_SOLVER` (the lone solution is kept in `positions`, by design and by test); `Aurora-sync/integration/aurora_peach_runtime.py:977` mapped that stop to NOT_INVESTIGATED and recorded nothing to continue - the researcher's work counted as not done |
| F2 | 13 entries: `INVESTIGATED_NO_PROOF`, "rounds of criticism were used up" | approaches were prose (e.g. seq 13 "a hidden symmetry ... reveals a periodicity aligned with the critical line"); no exact statement, so criticism had nothing to prove or refute |
| F3 | 6 entries: "critics raised no objection; nothing was proved" | same cause as F2: nothing exact to object to |
| F4 | numerical evidence never checked (15 entries, `checked` empty), faulty computations recorded as evidence (seq 67-69) | no promotion gate between a computation and a claim |
| F5 (PNP, today) | agents saw 6000 characters of the 52 kB binding specification; R0543 fell back to unrelated census work | `lab_tools.py` transcript cut (`json.dumps(...)[:6000]`) + unpaged `spec_read` |

The live PNP research path (pnp_desk research sessions -> `submit_claim` -> independent fast validator / Lean + fidelity review) already
separates research from verification; the RH campaign ran on the older mission route (PeachMe -> CherryMe brother). Both are covered.

## 2 Changes (working code, committed and pushed, [skip ci], private repositories)
| Repository / branch | Commit | Change |
|---|---|---|
| tonnestate/Aurora `cc/decision-contract` | `b2f63508acf4cd0c89f72618d9ee4c8340cb0249` | `integration/discovery_contract.py` (new): structured candidate fields, `contract_status` (EXPLORATORY / FORMALIZED / DERIVED), `ladder` over the existing queue verdicts (VERIFIED / NOVELTY_REVIEWED / PROOF_INTEGRATED / REFUTED), `promotion_allowed` gates; `pnp_desk.submit_claim` takes `candidate`, stores contract fields and status, answers with the missing fields; `claim_status` returns the ladder; tool schema documents `candidate`; `aurora_peach_runtime`: NO_SECOND_SOLVER -> `PENDING_VERIFICATION` + a scheduled MISSING_PROOF question "INDEPENDENT CHECK PENDING" |
| same | `236bca7`, `d065c7a`, and `b2f6350` | `spec_read`: pages of 3600 characters, long lines split not cut, exact reconstruction asserted, sha256 digest in every reply (recorded per session in the tool trace), query with or without a name |
| tonnestate/PhysalisMe `cc/algo-evolution` | `7cb1bccc5658edb068fcf31f4f237aefa1ca1c5e` | algoevolve: verdicts bound to the reference digest (the archive cache cannot return a verdict computed on an older reference); every front member attacked; front re-evaluated after a counterexample round; holdout never used for selection (unchanged) |

Gates enforced by `promotion_allowed` / `ladder`: a numerical test never makes a universal statement VERIFIED (a FINITE_CONFIRMED claim
whose declared scope is universal stays FORMALIZED); the author's own lineage or the same routine is not independent; a formal proof
needs a semantic audit; KNOWN is VERIFIED but never a discovery; NOVELTY_REVIEWED needs compared literature; PROOF_INTEGRATED needs a
recorded implication to the target; REFUTED stays visible. Exploratory prose is accepted, checked, and told what is missing - never
promoted.

## 3 Regression tests (pass)
Aurora `integration/tests/test_discovery_contract.py` (10) + `test_spec_read_delivery.py` (3): lone researcher not discarded (F1, desk and
mission route), prose stays EXPLORATORY and cannot be promoted (F2/F3), numbers never verify a universal statement (F4), finite
recomputation verifies a finite statement, same lineage / same routine not independent, formal proof needs semantic audit, KNOWN is not
a discovery, refuted stays visible, novelty needs literature, scope governs universality (live false positive found and fixed: 21
claims), every specification reconstructs exactly and fits, long lines split. PhysalisMe `tests/test_algoevolve.py` (6) incl. reference
binding. Pre-existing: 10 failures in `tests/test_aurora_peach_runtime.py`, identical before and after the change (AppleMe ledger
unreadable in this test environment); not caused and not fixed here.

## 4 End-to-end demonstration (live PNP path, real independent verification)
1. Lab computation through the agent tool path: `physalis_code_run` -> `cm-b5548a784c2d498a`.
2. Structured candidate with all fields and a derivation: `submit_claim` -> `claim:f53ba8f51dab`, contract status DERIVED (passed the
   host evidence gate; the cited id is host-observed).
3. Independent validator session F0489 recomputed with its own code and a mutant control (`cm-8f4396c7099d4996`):
   **FINITE_CONFIRMED** - "exhaustive enumeration ... 0 failures, 3(n-1) gates, exactly n-2 gates with fan-out > 1; a mutant control
   fails parity on thousands of inputs".
4. Ladder: VERIFIED (finite scope, independent recomputation), novelty UNREVIEWED, discovery = false (correct: the circuit is standard;
   it certifies the parity-witness premise of Proposition R1).

## 5 Live queue under the ladder (432 claims, read-only, 2026-11-20 ~21:40)
VERIFIED 331 (finite recomputations, Lean proofs, KNOWN), EXPLORATORY 82, REFUTED 19; NOVELTY_REVIEWED 0, PROOF_INTEGRATED 0 ->
**discoveries counted: 0**. This is the honest baseline the new process has to improve.

## 6 Not done / unproven (explicit)
- **Controlled comparison old vs new workflow: NOT RUN.** It needs frozen tasks with hidden answers and equal model budgets over many
  sessions; not done in this slice. Therefore it is **not shown** that the enforced workflow improves verified productivity.
- Novelty review and proof integration have gates but no producer yet (no tool writes `novelty_review` / `integrated_by`).
- CherryMe `brother.py` itself unchanged; the mission-route fix is in the Aurora mapping. Mission-route changes take effect for Aurora
  missions only after the guarded deploy (`deploy.sh aurora ...`, restarts ananasme) - not deployed (no restart authorisation).
  The PNP desk changes take effect for new research sessions without a restart.
- Agent-session test of spec access: R0554 used `spec_read` query after the fix; a dedicated recorded agent-session acceptance test is
  still to be run.
- Proof-producing evolution (Track B, candidate -> derivation -> verifier) not implemented; algoevolve still evolves decision procedures.

## 7 algoevolve re-evaluation, live evidence (isolated run evo-run3, seed 3, started from the original 786-instance reference)
Generation 0: 19 enumerated programs (11 SOUND, 6 VACUOUS, 2 INCORRECT) on reference digest `656c0b506f7d`. Generation 1: every front member
attacked; 5 WRONG counterexamples against the density-0.5 candidate entered the reference (new digest `9b472d47283c`); the front was
re-evaluated automatically: `density 0.5` and `density 0.5 + detB` -> INCORRECT (5 wrong each); `anneal 20000 + branch 4`,
`branch 4 + detB`, `branch 4`, `detB` -> SOUND. Before this change the unsound candidate stayed SOUND on the cached verdict (evo-run2).
Log: scratchpad evo-run3/state/evolution.jsonl (field `reference` on every row), adversarial.jsonl.

## 8 Operations note (same evening)
Between 21:30 and 22:15, 8 sessions ended at turn 0 with "the model supply gave no answer" while free providers answered 429
(NVIDIA, OVH; 14 in 30 min). The session design ends on silence to free the slot (2026-11-20 fix for sessions that sat 13-57 min
without a turn); the slot is refilled at once and the question re-offered (EXHAUSTED: MODEL_SUPPLY_SILENT). PlumMe unchanged by owner
decision.
