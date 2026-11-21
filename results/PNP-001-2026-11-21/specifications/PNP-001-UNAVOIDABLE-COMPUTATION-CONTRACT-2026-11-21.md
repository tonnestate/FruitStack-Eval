# PNP-001 — RESEARCH CONTRACT: FROM STATE LOWER BOUNDS TO UNAVOIDABLE COMPUTATION
Owner assignment 2026-11-21 (authoritative text: the owner's message of 2026-11-21 ~20:30; this file is its working copy for agents).
Recipient: Claude Code / FruitStack research organisation. Execution: PhysalisMe laboratory + independent critical verification.
Priority: high. Type: addendum to the Lemma M experiment (/root/contracts/PNP-001-LEMMA-M-EXPERIMENT-2026-11-21.md).

## 1. Mission
Investigate whether the exact finite Search-MCSP results reveal a structural principle connecting (1) required state information,
(2) state representation and nonlinear compression, (3) the computational cost of maintaining that representation, (4) causal
dependencies and escalating graph computations. Find, formulate, falsify and if possible prove a nontrivial statement about
UNAVOIDABLE STATE-TRANSITION COMPUTATION. Do not merely reproduce state counting (done); the missing part is the computational lower
bound. Do not claim a proof of P != NP.

## 2. Read first
/root/contracts/PNP-001-LEMMA-M-EXPERIMENT-2026-11-21.md; /root/fruits/integration/Aurora-sync/research/PNP-001-LEMMA-M/REPORT.md;
/root/fruits/research/PNP-001/theory/oracle-elimination/QE-STAR-CANDIDATE-FIRST-FALSE-LINE.md; .../EGC-001-SIMULATION.md.
Inspect current PhysalisMe research/verification interfaces; identify all ongoing experiments and owners before new computation.
DO NOT interrupt, restart, duplicate or interfere with the running exact Pareto-front synthesis (gate_pareto_sat.py, Codex); its
results take precedence.

## 3. Established finite evidence (inspect verification artifacts before relying on them)
| class | #functions | min state bits | truth-table length |
| depth-2 decision trees, n=3 | 62 | 6 | 8 |
| SC_{3,1} | 38 | 6 | 8 |
| SC_{4,1} | 70 | 7 | 16 |
| SC_{4,2} | 526 | 10 | 16 |
| read-once formulas, n=4 | 2,680 | 12 | 16 |
SC_{3,s}, s=0..4: 3, 38, 152, 232, 256. Constants-and-literals mask algorithm: widths 6, 8, 10 bits, update-gate costs 7, 9, 11.
These are finite information bounds + concrete algorithms, NOT a transition-gate lower bound. Full Search-MCSP semantics: distinct live
prefixes stay distinguishable whenever needed for the correct final witness. Corrected bound:
S_t >= ceil(log2(L_t + 1[L_t < 2^t])). The full-input-buffer construction (S >= N) is not evidence of nontrivial compression.

## 4. Central question
Required distinguishability -> unavoidable computational dependencies. C5 ("an update that preserves live/dead distinction must
decide liveness") is FALSE - never reuse it. Seek a property of the transition relation that stays hard under: arbitrary nonlinear
encodings, redundant state, time-dependent encodings, shared intermediate computation, persistent auxiliary information, alternative
decoders, recurrent and escalating internal computation.

## 5. Exact Pareto frontier (S, G_max, D)
After the SAT synthesis finishes: SC_{3,1} at S=6 and S=7. Per S separate: proven minimum update-gate cost; decoder cost; jointly
feasible combinations; SAT candidates only; cases with independently checkable UNSAT evidence; incomplete/timeouts. Moving complexity
into the decoder is not a saving; never compare different decoder constraints as equal budgets. A claimed optimum needs a verified
satisfying construction AND a separately checked lower-bound certificate under the same circuit encoding. Record gate basis, fan-in,
fan-out, constants, wiring, time dependence, output encoding.

## 6. Representation trade-offs
Per certified result: what is stored explicitly / encoded nonlinearly; shared intermediates; does redundant state reduce update cost;
does state minimisation raise transition cost; repeated recomputation; does the decoder compensate. Compare adjacent memory budgets,
in particular S=6 vs S=7 for SC_{3,1}. Record a negative result if no difference. No general pattern from one example.

## 7. Escalating graphs (hypothesis: computation organised as an escalating causal process, not visual power)
Study causal event graphs of synthesized transitions: activation cascades, fan-out/reconvergence, reused intermediates, dependency
depth, repeated evaluation, local vs global propagation, representation change across updates. The object is the COMPUTATION on the
graph, not topology. DragonFruitMe escalation, CherryMe graph activation, PhysalisMe ProofGraph = technical references only; do not
conflate semantics; do not modify them.

## 8. Unavoidability test (most important)
Per candidate property: state formally; encoding dependence?; search another correct implementation avoiding it; allow extra state
bits within budget; allow nonlinear/recurrent computation; build the smallest counterexample; verify exhaustively; keep the first false
inference if the lemma fails. Target: a property of EVERY admissible implementation within stated bounds. Shared intermediates can
collapse large apparent dependency graphs. Mandatory stress tests: parity, full-input buffering, MMW oracle-assisted construction
(proof-state field oracle_stress {a, b_rules_out_oracle, b, c} for every LOWER_BOUND step).

## 9. Lower-bound theory (each source -> usable technique, specific obstruction, or explicit reason transfer fails)
Valdats (state assignment / transition complexity of automata); time-space trade-offs and pebbling; information-transfer bounds for
online algorithms; causal graph dynamics / asynchronous rewriting; incremental computation / change propagation; hardness
magnification, locality barriers, MMW Search-MCSP streaming. Pebbling for a fixed DAG != all algorithms; information transfer needing
intermediate outputs != Search-MCSP; conditional != unconditional; a bound surviving oracle augmentation unchanged cannot give the
oracle-sensitive separation. No disconnected literature summary.

## 10. Smallest defensible theorem
Strongest statement justified by evidence; narrow and proved beats ambitious. Acceptable: certified exact time-memory-decoder
trade-off; counterexample to an assumed structural necessity; theorem for a restricted nontrivial class of nonlinear transducers;
equivalence/simulation lemma with full resource accounting; necessary condition for any future Lemma M proof. A definition is not a
theorem; a finite pattern is not asymptotic; one graph implementation's bound is not universal.

## 11. Independent criticism
Author and final critic separate. Critic inspects: formal statement; Search-MCSP witness correctness; exhaustive coverage; SAT encodings
and UNSAT certificates; uniformity assumptions; state/decoder budgets; whether structural claims cover all representations; oracle
stress test; improper generalisation. Use existing PhysalisMe lab IDs and evidence classes - no parallel evidence system. Agreement of
two agents promotes nothing. Unresolved = OPEN.

## 12. Deliverables (one consolidated report)
A evidence inventory (reproduced / certified / observed / incomplete); B Pareto-front analysis; C representation analysis; D escalating
causal-graph analysis; E falsification results (smallest counterexamples, first invalid inference); F strongest theorem with all
restrictions; G relation to Lemma M (advances the universal bound or only clarifies the finite problem); H independent critic's verdict
with unresolved obligations. Keep source refs, lab IDs, solver artifacts, reproduction instructions.

## 13. Boundaries
Do not interfere with the Codex Pareto run or active research sessions; no mission-architecture/orchestration changes; no CI; no new
graph-processing services; use current PhysalisMe lab and verification infrastructure; additive investigation only.

## Final directive
Find the computational principle behind the exact finite state bounds: do transition structures require different amounts of
computation, why, and does the difference survive arbitrary nonlinear and redundant representations? Treat escalating causal graphs as
a serious candidate. Falsify aggressively. Target: the strongest independently defensible mathematical insight.
