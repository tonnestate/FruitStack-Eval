# PNP-001 — RESEARCH ADDENDUM: REPRESENTATION-INDEPENDENT UPDATE LOWER BOUNDS
Owner addendum 2026-11-21 (~21:05; authoritative text: the owner's message; this file is its working copy for agents). BINDING addendum
to PNP-001-UNAVOIDABLE-COMPUTATION-CONTRACT-2026-11-21.md; same programme as PNP-001-ALGEBRAIC-STATE-INVARIANTS-CONTRACT-2026-11-21.md.
Execution: PhysalisMe with independent mathematical criticism. Priority high.

## Mapping to existing research questions (do not duplicate)
- sec. 3 state-degree audit -> Q-b5eddd829d (this addendum ADDS: evaluate separately correctness / novelty / quantitative strength /
  relevance to update-time bounds; a correct weak theorem must not be overstated).
- sec. 7 degree/semantics -> update work -> Q-18a621cf3e; sec. 11 gate elimination -> Q-6ff2acc0cc; sec. 12 SAT Pareto -> Q-a23f0770f8.
- NEW: sec. 4-6 compatible encodings + partial-transition optimisation G*(S,D); sec. 10 communication complexity / Gemini's claim.

## 1. Mission
Does the complete family of search-MCSP prefix-distinguishability AND transition-consistency constraints yield a
REPRESENTATION-INDEPENDENT lower bound on update cost - for every admissible encoding, including nonlinear, redundant, shared
intermediates, recurrent causal computation? Do not dismiss algebraic approaches only because one representation changes under
recoding; do not infer computational complexity from distinguishability alone. Goal: strongest proved connection, or a minimal
counterexample explaining why it fails.

## 3. State-degree candidate (audit, do not accept)
E_t: {0,1}^t -> {0,1}^S; 0^N has a valid witness; output determined by the final state. CANDIDATE sum_j deg(E_{t,j}) >= t, via: the
zero prefix's state differs from every other prefix's, so the zero-code indicator equals prod_i (1 + x_i) over F_2, degree t. Check
witness semantics, threshold, Boolean quotient ring, determinism, time-dependent encodings, arbitrary nonlinear recodings; known result?
stronger representation-independent versions? Report correctness, novelty, strength, relevance separately.

## 4. Syntactic invariance vs universal lower bound
A: one algebraic quantity is numerically unchanged under every recoding. B: every admissible recoding satisfies a common lower bound.
Failure of A does not imply failure of B. For every inequality state its quantifier: one chosen representation / all bijective recodings
of a fixed state space / all admissible representations incl. redundant states / all compatible encoding sequences / all deterministic
streaming algorithms meeting the search-MCSP specification. Only the universal quantifiers can support Lemma M.

## 5. Compatible state encodings
Necessary condition: E_t(p) = E_t(q) => E_{t+1}(pb) = E_{t+1}(qb) for all length-t prefixes p, q and bits b. Prove the characterisation:
compatible sequences induce well-defined deterministic PARTIAL transition functions on reachable states; conversely compatible encodings
plus a suitable final-output map define an exact streaming transducer (prove output correctness). State the optimisation over all
compatible encodings and all completions of their partial transitions. Distinguish fixed vs variable width, reachable vs unreachable
codes, redundant states, uniform vs nonuniform transition circuits, bounded vs unbounded decoder complexity.

## 6. Partial-circuit complexity
F_t(E_t(p), b) = E_{t+1}(pb), constrained only on reachable (state, bit) pairs; free elsewhere. Does
  G*(S, D) = min over compatible, search-correct (E_t) with CC(D_N) <= D of max_{t<N} CC_partial(F_t)
correctly characterise optimal worst-case transition-gate complexity in the stated nonuniform circuit model? Check initial state,
indexing, decoder circuits, basis, fan-in, fan-out, constants, wiring; correct the formulation if incomplete before using it. Connect to
FSM state assignment, incompletely specified Boolean functions, partial MCSP, convergent gate elimination.

## 7. Missing transfer
Semantic prefix constraints => worst-case transition computation? Use the FULL collection of compatible prefix transitions. Not
sufficient alone: number of distinguishable states, degree of one state bit, rank of one fixed cut, size of one dependency graph, one
particular state assignment, the canonical minimal automaton (necessary conditions at most). Find a property constraining EVERY
admissible transition implementation.

## 8. Mandatory falsification controls (every candidate)
A OR accumulator: one OR accumulator per input block gives sum_j deg(E_{t,j}) = t with one OR per update (not full search-MCSP, but
shows the degree bound alone cannot force expensive updates). B parity sketches (cheap affine updates must not be classed expensive).
C redundant/nonlinear encodings reducing gate cost with exact semantics. D decoder displacement. E shared intermediates, arbitrary DAG
fan-out; no circuit bound from formula bounds without an explicit simulation theorem. F recurrent causal graphs: count all activations,
temporary memory, scheduling, graph updates; no savings from static node count. G MMW oracle constructions: exactly where the oracle
changes the obligations (proof-state oracle_stress).

## 9. Correct target
The MMW streaming lower-bound premise - NOT a direct lower bound for general Boolean circuits (general circuits have arbitrary input
access; a one-pass machine has access restrictions but general computation inside updates). Read MMW's exact statement, quantifiers,
oracle results, uniformity, decoder/output conventions from the primary source; reproduce any transfer chain exactly; never invent a
stronger transfer theorem than the published one.

## 10. Communication complexity - test Gemini's claim
Claim: "only semantic communication measures survive arbitrary nonlinear recoding, and they give width bounds, not work bounds". Test,
do not accept/reject by analogy: (1) distinguish deterministic and nondeterministic communication complexity, matrix rank, fooling sets;
(2) which are invariant under change of state representation; (3) which apply directly to ordered streaming; (4) does the semantic
transition relation carry information beyond the number of distinguishable futures; (5) known models where information-transfer
arguments give time/operation lower bounds; (6) why they do or do not transfer to search-MCSP. Compare Karchmer-Wigderson, Neciporuk,
information-transfer bounds, circuit lower-bound literature. Do not conclude communication complexity is the only representation-
independent technique without proof.

## 11. Gate elimination / causal rewriting (-> Q-6ff2acc0cc)
2026 convergent gate elimination / constructive lower bounds adapted to PARTIAL transition functions: local rules, semantic
preservation, termination, confluence, elimination under arbitrary fan-out, shared intermediates, recoding, exact accounting; a theorem
independent of the initial state assignment. C_{n+1} >= C_n + Delta(n) only with proved hypotheses; confluence is not a lower bound.

## 12. SAT Pareto (-> Q-a23f0770f8)
Do not restart. With certified SC_{3,1}, S=6 and S=7: optimal transitions, ANF, allowable compatible assignments, nonlinear gates,
reuse, decoder costs, test all candidate invariants against all certified optima, search alternative encodings that break structural
explanations. Incomplete frontier: report the limit, use only independently confirmed data. Timeout != UNSAT.

## 13. Verification and status
Separate constructor, counterexample generator, certificate verifier, critic (checks the FIRST potentially invalid inference). Status of
every result: PROVED / CONDITIONALLY_PROVED / EXACT_FINITE_VERIFICATION / OBSERVED / REFUTED / OPEN. Model agreement never gives PROVED.
Use PhysalisMe verification and the proof ledger.

## 14. Deliverable (one consolidated report)
A correctness + novelty of the state-degree theorem; B characterisation of compatible encodings; C partial-transition optimisation and
its resource assumptions; D strongest valid algebraic-to-computational transfer; E assessment of Gemini's claims with explicit
counterexamples; F gate elimination + causal graph results; G smallest counterexamples to failed lemmas; H exact relevance to the MMW
streaming premise; I independent critic's verdict. Every failed route: earliest invalid implication. Every surviving theorem: complete
proof + reproducible evidence.

## 15. Constraints
No interruption of research sessions; no restart of the SAT Pareto run; no production architecture change; no new graph services; no
CI; preserve ledger history and evidence classes; current infrastructure only.

## Final objective
Prove or falsify a representation-independent connection between the complete search-MCSP transition relation and unavoidable update
computation, exploiting the distinction between representation-dependent measures and universal bounds over all recodings - a genuine
theorem, a strictly stronger verified bound, or a decisive counterexample; not a new description of the open problem.
