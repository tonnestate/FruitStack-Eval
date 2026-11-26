# T39 — Transfer of an algebraic observable invariant to general bounded-depth circuits and to SAT (PI, 2026-11-18)

STATUS: owner request 2026-11-18. The owner asks for a theorem about a much more general class of nonlinear computations, not just a
minimal representation inside a restricted model, which TRANSFERS to circuits or SAT instances.
Components are classical (Razborov 1987, Smolensky 1987, Tseitin encoding, projection reductions); the assembly and the explicit
projection are checked by the PI (scratchpad proj.py). No novelty is claimed. Not in the ledger. Verification is to be queued after
iteration 9.

## 1. From exact degree (T38 O6) to approximate degree
O6 needs exact low degree of all of V_F. That fails for most nonlinear systems (O2, O8). The invariant that survives arbitrary
nonlinear composition is APPROXIMATE degree: f is ε-approximated by a polynomial p ∈ 𝔽_2[x] of degree ≤ D if Pr_x[p(x) ≠ f(x)] ≤ ε.

## 2. Theorem T39 (statement)
Class: AC^0[⊕] = circuits of constant depth d with unbounded fan-in AND, OR, NOT and PARITY gates. These are arbitrary nonlinear
Boolean computations, with no restriction on gate placement, order, reuse or representation. Their only restriction is depth.
Theorem. For every fixed d there is c_d > 0 such that every depth-d AC^0[⊕] circuit family deciding CNF-SAT on encodings of length N
has size ≥ exp(c_d · (N / log² N)^{1/(2d)}) for infinitely many N; in particular superpolynomial.

## 3. Proof
Step A (invariant under composition; Razborov–Smolensky). Every depth-d AC^0[⊕] circuit of size s is (1/10)-approximated over
uniform x by a polynomial over 𝔽_2 of degree ≤ (C log s)^d. Mechanism: replace each OR/AND of fan-in m by a random 𝔽_2-polynomial of
degree O(log s) that is correct with probability ≥ 1 − 1/(10s) (random parities of subsets, OR(y) ≈ 1 − Π_j (1 − Σ_{i∈S_j} y_i)).
PARITY gates are linear (degree 1). NOT is 1 + y. Degrees multiply along each path, so they multiply over d layers. A union bound
over s gates and averaging fix one polynomial. This is the step at which ARBITRARY nonlinear composition is controlled: the invariant
is closed under the gate operations, not tied to a variable order or a state space.
Step B (MAJ is far from low degree; Smolensky). MAJ_n has no (1/10)-approximation over 𝔽_2 of degree o(√n). Proof via the
algebraic counting argument: a low-degree approximation would let every function on most of {0,1}^n be written as a polynomial of
degree ≤ n/2 + O(√n), which is too few by dimension count. Hence depth-d AC^0[⊕] size for MAJ_n is ≥ exp(Ω(n^{1/(2d)})).
Step C (transfer to SAT by projection). There is a fixed CNF G_n (Tseitin encoding of a counting circuit plus comparator,
O(n log n) clauses) and n unit-clause slots. Slot i contains the literal v_i with sign bit ¬x_i. Hence every bit of the encoding of
the formula Φ_x is a constant or a literal of x (a PROJECTION), and Φ_x ∈ SAT ⇔ MAJ_n(x) = 1.
Computed (proj.py, DPLL, all x): equivalence holds for n = 1..9; 290 clauses at n = 9.
Step D (assembly). A depth-d AC^0[⊕] circuit of size S for SAT on length N = O(n log² n) (O(n log n) clauses, O(log n)-bit literals) becomes, after substituting the
projection (constants and literals), a depth-d circuit of size ≤ S for MAJ_n. Step B gives S ≥ exp(Ω(n^{1/(2d)})). Rewriting n in
terms of N gives the bound. ∎

## 4. Why this transfers, and why the same route stops before P/poly (the precise missing transfer)
- Transfer works because the invariant (approximate 𝔽_2-degree) is (i) preserved, with a controlled loss, under EVERY gate of the
  class, and (ii) preserved under projections. Every reduction used is a projection, and SAT is complete under such reductions
  (Immerman: first-order projections). The construction above is explicit.
- Frontier: ACC^0 (all MOD_m gates) has NO known lower bound for SAT. Williams (2011/14) and Murray–Williams (2018) give
  NEXP ⊄ ACC^0 and NQP ⊄ ACC^0, which are not NP statements. General circuits: the best explicit bounds are linear
  (≈ 3.1 n − o(n), Li–Yang 2022).
- Barrier (Razborov–Rudich 1997). Every invariant of this kind is NATURAL: it is computable from the truth table in 2^{O(n)} time
  and holds for a large fraction of functions. If pseudorandom function families of exponential security exist in P/poly (implied
  by standard cryptographic assumptions), no natural property is useful against P/poly. So the observable invariants of T38 (d, N,
  exact or approximate degree, ranks of observation matrices) can NEVER be lifted to P/poly in this way, unless strong pseudorandom
  functions do not exist. The missing transfer is therefore not a missing lemma of PNP-001. It is the known natural-proofs barrier.
  A transfer to general circuits needs an invariant that is non-natural: not large, or not efficiently checkable. The only known
  non-natural route is Williams' algorithmic method, which yields NEXP-type, not NP, lower bounds (T23, T34 J5).

## 5. Placement
T38 O6 is the exact (degree-bounded) special case. T39 is the approximate version that transfers to an unrestricted-composition
class and to SAT. T36 Lemma N plus §4 locate the exact obstacle for P/poly. No new hypothesis is opened.
