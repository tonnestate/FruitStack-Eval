# PNP-001 Research Assignment — Algebraic Computation, Bit-Level Compression and General Complexity (owner, 2026-11-19, binding)

Operational boundary: no new infrastructure, no FruitStack service reorganisation, no mission-control redesign, no replacement of
validation workflows. Use the established research organisation and its evidence procedures.

## Objective
Investigate whether combined use of addition, multiplication, XOR, squaring, square roots, bit/byte representations, and graph-based joining
and filtering yields a mathematically meaningful advance in solving or understanding NP-complete problems. Primary objective remains
P != NP, but results are evaluated in either direction without assuming the conclusion. Not restricted to one proof system, representation
or technique. Goal: does the interaction of linear and nonlinear operations reveal a generalisable computational mechanism, a new
structural invariant, a provable algorithmic improvement, or a meaningful computational obstruction?

## 1. Starting point (finite observations, to be reproduced independently)
Per positive 1-in-3 clause: a+b+c = 1  <=>  (a xor b xor c = 1) and (ab = 0). The system splits into linear XOR equations and quadratic
Boolean conditions. Reported (external, unverified): n=6: all 900 minimal GF(3)-consistent Boolean-UNSAT cores give constant contradictions
after XOR elimination + quadratic-condition reduction; n=7: of 62,370 minimal blind cores, 61,110 do, 1,260 need additional linear
polynomial consequences; n=8: explicit core F8 = {146, 012, 036, 256, 234, 045, 157} has a degree-two algebraic refutation not obtained
from degree-0/1 consequences: after XOR elimination 3 free variables remain and the seven quadratic conditions satisfy
q1 xor ... xor q7 = 1, contradicting q_i = 0 for all i.
Artifacts named (pnp_xor_carry_exact_experiment.py, pnp_full_n7.py, PNP-001_XOR_Carry_Exact_Results_2026-11-19.json): finite evidence,
NOT on this machine as of 2026-11-19 19:40 - reproduce from the definitions.

## 2. Full mechanism
Do not assume XOR elimination + quadratic linearisation is the best representation. Examine arithmetic/Boolean/algebraic operations on
bits, bytes, vectors, matrices, dependency graphs; whether x -> x^2, x -> sqrt(x) with +, *, xor give smaller exact representations.
Distinguish integer arithmetic, Boolean algebra, finite fields, matrix operations, state-space cardinality transforms. For each
transformation: what it preserves, what it discards, the cost of recovering it. No reduction of work may be inferred from smaller numbers
or smaller encodings.

## 3. Beyond existing algebraic proof systems (comparisons, not a checklist)
Boolean polynomial systems, ANF, polynomial calculus, Groebner bases, XL, Crossbred, 2-XNF; coding theory, syndrome methods, algebraic
cryptanalysis; representation technique, generalized birthday, asymmetric/multi-way meet-in-the-middle; Fourier/Walsh-Hadamard/Moebius,
subset convolution, fast matrix operations; tensor networks, holographic algorithms, matchgates, cancellation; graph decomposition,
propagation, variable elimination, decision diagrams, shared-state compression; arithmetic/Boolean circuit complexity, communication
complexity, barriers. Every transfer justified mathematically including representation and reconstruction costs.

## 4. Central question: collective evaluation of nonlinear constraints
After XOR elimination: q_i(z) = l_i1(z) * l_i2(z) = 0. Can these be evaluated, simplified, combined or refuted collectively without
enumerating all 2^d free assignments? Does their origin in positive 1-in-3-SAT give structure absent from arbitrary quadratic systems?
Distinguish EXISTENCE (compact representation/certificate), CONSTRUCTION (efficiently), DECISION (every instance), COMPLEXITY (bound on an
unbounded family). Keep every restriction (proof system, solver class, parameter regime, distribution) explicit.

## 5. Graph-tree and temporal perspective
Reuse H-CONSTRUCT-002 definitions (no new scheduling framework). Measure W, M, D (dependency depth), T_wall separately, including costs of
polynomial transformations, hashing, equivalence checks, representation construction, joins, projections, synchronisation, verification.
Scheduling improvements are not reductions of problem complexity.

## 6. Independent validation
Reproduce the XOR/carry results first; exact arithmetic, independent oracles. Compare on identical instances with: GF(3) coset approach,
direct XOR-candidate enumeration, algebraic solvers, OBDD construction, SAT baselines; include positive 1-in-3 and 2-SAT/XOR-SAT controls.
General claims: quantifiers + proof. Counterexamples: minimal explicit witness + checkable certificate. Binding evidence rule: state the gain
over Gaussian elimination (existence of two-valued points, cost of finding them, cost of certifying absence). A re-expression of the same
NP-complete condition is not an algorithmic improvement.

## 7. Relation to P vs NP — three levels
(1) finite finding / identity; (2) uniform asymptotic result for a specified class of algorithms/representations; (3) result about
unrestricted polynomial-time computation (needs a valid non-circular argument for arbitrary algorithms). Barriers (relativization, natural
proofs, algebrization) are to be investigated where relevant, not treated as universal prohibitions on algebra.

## 8. Required outcome (one consolidated report)
known vs possibly original mechanisms; what the XOR/carry experiments establish after validation; exploitable structure of the special
quadratic systems beyond Gaussian elimination; measurable fully costed improvement or not; extension to an unbounded family or not;
rigorous limitation/counterexample where a mechanism fails; whether anything is a genuine step toward the general question. Exact
mathematics and asymptotic analysis over further enumeration without defined gain. Do not stop at "still NP-complete"; do not force the
first available proof system. "No general advantage demonstrated" is a legitimate conclusion only from concrete analysis, proof or
counterexample.

## Director's reproduction note (2026-11-19, exhaustive, n=8 only)
F8: 0 Boolean solutions; 3 GF(3) solutions (GF(3)-consistent = blind); 8 GF(2) solutions (XOR coset dimension 3); with
q_c = ab+ac+bc mod 2 (= 1 iff clause weight 3 on the XOR coset), XOR over all seven q_c equals 1 on all 8 coset points. The n=8 claim is
reproduced for this instance; the n=6/n=7 counts are not yet reproduced.
Director's framing for the organisation (to be checked): a refutation of this form is a polynomial-calculus refutation over GF(2) of degree
2 relative to the linear XOR ideal. Bounded-degree PC refutations are FOUND in n^O(d) time (Clegg-Edmonds-Impagliazzo); hence, unless P = NP,
the required degree cannot stay bounded on all UNSAT instances - the decisive quantity is how the needed degree grows on blind cores
(same "cheap to check / expensive to find" structure as the CG discovery question).

## Owner clarification 2026-11-19 (binding; no new assignment, comparison frame for ALG-BIT-001)
- Frame: Impagliazzo-Pudlak-Sgall size-degree relation, d <= k + O(sqrt(n log S)), i.e. S >= exp(Omega((d-k)^2/n)); a linear degree lower
  bound gives exponential PC size. This bounds the PROOF SYSTEM (and degree-bounded Groebner search, Clegg-Edmonds-Impagliazzo), not
  arbitrary algorithms.
- Distinguish THREE degrees, never conflate them: (i) degree after XOR elimination (relative to the linear GF(2) coset), (ii) minimal degree
  in the extended XOR/carry system (XOR + quadratic axioms), (iii) minimal PC degree of the ORIGINAL CNF encoding (contains e.g. the cubic
  (1+a)(1+b)(1+c) = 0; deriving the XOR equations may itself need higher intermediate degree). The F8 degree-2 certificate is of type (i).
- Priority method for a lower bound: Alekhnovich-Razborov, extended by Miksa-Nordstrom (expansion of the clause-variable graph PLUS
  properties of the local constraints; expansion alone is insufficient - inconsistent GF(2) XOR systems are easy by Gaussian elimination).
  Concrete question: can the quadratic carry conditions force a provably growing PC degree on an explicit infinite family of GF(3)-blind
  positive 1-in-3 formulas, with the actual XOR/multiplication axioms? Such a result bounds that algebraic proof system only.
- Director note (logic direction): if every UNSAT instance had a certificate of degree <= d in a system computable from the formula, the
  n^O(d) search would decide the problem (so bounded degree everywhere implies P = NP); the CONVERSE is not valid - growing degree says
  nothing about arbitrary algorithms.
- No unverified claims into the paper; prove within the fixed algebraic model first.
