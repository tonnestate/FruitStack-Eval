# PNP-001 — INDEPENDENT PROOF SYNTHESIS: ALGEBRAIC STATE INVARIANTS AND CAUSAL GATE ELIMINATION
Owner assignment 2026-11-21 (~21:00; authoritative text: the owner's message; this file is its working copy for agents).
Execution: FruitStack research organisation / PhysalisMe. Priority high. No theorem accepted in advance.
Companion: /root/contracts/PNP-001-UNAVOIDABLE-COMPUTATION-CONTRACT-2026-11-21.md (same programme; do not duplicate its questions).

## 1. Mission
Combine established PNP-001 results to find a valid lower-bound mechanism for exact search-MCSP streaming. Central question: can a
property of the ALGEBRAIC ENCODING of streaming states be converted into unavoidable computational work, even with arbitrary nonlinear
encodings, redundant states, shared intermediates and recurrent causal computation? Candidate techniques: proof-preserving circuit
transformations, convergent graph rewriting. Acceptable outcomes: a rigorous theorem for an infinite family; a strictly stronger finite
theorem with complete certificates; a structural impossibility result for a precisely defined model; a minimal independently verified
counterexample naming the first invalid inference. A reformulation of Lemma M is not progress. Never claim P != NP.

## 2. Recover the state first
Read the companion contract, PNP-001-LEMMA-M-EXPERIMENT-2026-11-21.md, QE-STAR-CANDIDATE-FIRST-FALSE-LINE.md, EGC-001-SIMULATION.md,
research/PNP-001-LEMMA-M/REPORT.md. Compare the local proof ledger with GitHub tonnestate/FruitStack-Eval branch
cc/pnp001-results-20261118 (commit fcd0108). Review: prefix distinguishability + corrected state bound; S0011, S0024, S0043 (affine
encodings, limits); the running exact SAT synthesis of (S, G_max, D); Theorem 12, Theorem 14, Lemma 15, Theorem 16 with their exact
proof-system restrictions; REUSE-MCSP-NOTE.md (open R-MCSP hypothesis); D-013 (matroid-port obstruction); refuted transfers of formula,
rank, pebbling, local-cut bounds to general circuits. Identify related active questions before adding new ones; no duplicate work.

## 3. First candidate (NOT assumed correct)
E_t: {0,1}^t -> {0,1}^S reachable state encoding of a deterministic exact one-pass search-MCSP algorithm after t bits. Assume 0^N has an
admissible witness circuit and the final output is a function of the final state. With ANF over F_2 of each coordinate E_{t,j}:
  CANDIDATE: sum_{j=1..S} deg(E_{t,j}) >= t.
Proposed proof: (1) the all-zero prefix must be distinguished from every other prefix (appending the zero suffix needs a different final
result); (2) P(x) = prod_j (1 + E_{t,j}(x) + E_{t,j}(0^t)) is the indicator of the zero prefix's code; (3) P = prod_i (1 + x_i) as a
Boolean function; (4) t = deg P <= sum_j deg E_{t,j}.
Check every premise: witness-output semantics, admissible threshold, dependence of the state on the full prefix, Boolean quotient algebra
(multilinear reduction), zero-degree coordinates, nonuniform / time-dependent encodings. Is it a known consequence of an existing
algebraic theorem? Improve strength or generality. If verified: independent formal check (Lean). Record novelty separately from
correctness.

## 4. Degree -> update cost
The bound is about the prefix-to-state map, not one update. For E_{t+1}(xb) = F_t(E_t(x), b) in a fixed basis, derive exact upper bounds
on the degree of the composition from: previous degrees, number/arrangement of nonlinear gates in F_t, reuse of intermediates, S, t. Does
the accumulated degree force any nontrivial WORST-CASE UPDATE-gate lower bound? Mandatory test constructions: OR accumulation, parity
sketches, balanced nonlinear updates, redundant auxiliary state, time-dependent recoding, deferral to the decoder. If only a constant or
logarithmic nonlinear-cost requirement follows, state that precisely. Never substitute total circuit cost for worst-case update cost
without a proved conversion.

## 5. Causal gate elimination
Retrieve and verify the complete statements of the 2026 papers on convergent gate elimination and constructive circuit lower bounds.
Check whether their rewriting rules (1) preserve Boolean function, (2) respect general DAG fan-out, (3) terminate, (4) are confluent and
under which assumptions, (5) give QUANTIFIED gate elimination, not just simplification, (6) stay valid for algebraically encoded states.
Investigate analogous rules for exact streaming transducers: an explicit resource inequality C_{n+1} >= C_n + Delta_n for a precisely
defined joint memory/update/decoder resource C_n - proved, or a counterexample. Confluence alone is not evidence of a lower bound.

## 6. Escalating causal graphs
Model any update as a finite terminating causal computation graph allowing nonlinear encodings, persistent redundant state, recurrence,
local cascades, shared intermediates, bounded fan-out and reconvergence, dynamic rewiring; count all memory and all work. Question: is a
proposed causal invariant unavoidable over EVERY implementation of the same exact search relation? For each, try to synthesize an
equivalent implementation where it disappears. Mandatory controls: encoded-pebbling and circuit-rewriting counterexamples.

## 7. SAT laboratory as falsifier
Do not restart the Pareto synthesis. When available, inspect exact optimal transducers for SC_{3,1} (S=6, S=7), SC_{4,1} if certified,
others only with sufficient exact evidence: ANF of state bits, multiplicative complexity, transition dependencies, redundancy, decoder
cost, causal event graph. Smallest counterexample to every mechanism; keep the exact SAT witness and drop the universal form of a failed
invariant. UNSAT needs an independently checkable certificate in the same resource model. Timeout != UNSAT.

## 8. Mandatory model-transfer checks per candidate
Representation independence; uniformity (uniform machines vs nonuniform transition circuits); decoder (can the work be postponed to the
output?); relativisation (exact inference that fails with MMW oracle gates - proof-state field oracle_stress); locality (ordered cuts,
bounded fan-out, restricted communication, fixed DAG?); natural proofs (check the hypotheses: constructive, large, against a class with
suitable PRFs - do not invoke without checking); asymptotics (infinite family or enumerated examples only); target transfer (which
published theorem turns it into a separation - exact quantifiers and parameter range).

## 9. Roles
Separate: mathematical constructor; computational falsifier; formal proof verifier; independent critical reviewer (tries to invalidate
the best result without the constructor's interpretation). Use PhysalisMe evidence + lab IDs. Agreement of models promotes nothing.
Report conditional, finite, solver-asserted and kernel-verified findings separately.

## 10. Deliverable (one consolidated report)
A reconstruction of prior results; B proof audit of the state-degree statement; C strongest valid degree-to-computation transfer;
D causal gate-elimination / rewriting analysis; E smallest counterexamples and failed implications; F strongest new theorem with full
assumptions; G exact relation to Lemma M and the MMW transfer; H independent critic's verdict + remaining obligations. If nothing
nontrivial survives: earliest failed inference + most informative counterexample. Keep sources, certificates, proof scripts, IDs.

## 11. Constraints
Do not interrupt PNP-001 sessions or the SAT Pareto run; no refactoring/orchestration change/new graph service; no CI; preserve ledger,
authority boundaries, evidence classes. Additive research only.

## Final directive
Attempt the transition from unavoidable state information to unavoidable computational work with algebraic invariants, causal graph
structure and constructive gate elimination; SAT lab as adversarial falsifier. A narrow genuine theorem beats a broad conditional
conjecture; a decisive counterexample beats another unverified sketch.
