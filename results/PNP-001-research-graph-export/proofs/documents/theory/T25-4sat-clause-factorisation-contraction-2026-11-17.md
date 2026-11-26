# T25 — 4-SAT: axis SWAP, rank-2 clause factorisation and contraction width — analytic comparison (PI, 2026-11-17)

STATUS: analytic; standard facts cited, no computation, no new dependency (TensorFlow/opt_einsum/cotengra not installed and not
needed for this question). Owner question: can an optimised 4-SAT tensor factorisation reduce the effective contraction width
enough that the technique transfers to circuits with high fan-out?

## 1. Local facts
- An OR clause on k literals is the k-way tensor T = 1⊗...⊗1 − u_1⊗...⊗u_k (u_i = indicator of the falsifying value of literal i).
  Its CP rank is exactly 2 for every k >= 2 — independent of any grouping. The owner's 4x4 reshaping (rank 2) is one view of this.
- Axis permutation (SWAP) changes no rank (CP rank invariant; matrix ranks only depend on the chosen bipartition, and for a clause
  every 2+2 bipartition gives rank 2). SWAP is a memory-layout operation, not a complexity lever.
- Fan-out (COPY) tensors δ on d legs are also CP rank 2 (e_0^{⊗d} + e_1^{⊗d}) for every d; high fan-out costs nothing locally.

## 2. Global cost: direct vs factorised contraction
- Direct contraction of the clause network (hyperedges = clauses on the variables): exact cost 2^{Θ(tw of the primal graph)}·poly
  for the best order (Markov–Shi for tensor networks).
- Rank-2 factorisation puts one bond of dimension 2 per clause: the network becomes the variable–clause INCIDENCE graph.
  Cost 2^{Θ(tw_inc)}. Standard relations (Kolaitis–Vardi; Szeider): tw_inc <= tw_primal + 1 and, for clause width k,
  tw_primal <= k(tw_inc + 1) − 1. For 4-SAT: the factorisation lowers the exponent by at most a constant factor ≈ 4, never more.
- Summing all clause bonds first is inclusion–exclusion: #F = Σ_{S ⊆ clauses} (−1)^{|S|} #{x falsifying all of S}, cost 2^m.
- For random 4-CNF at constant clause density the incidence graph is an expander w.h.p., so tw_inc and tw_primal are Θ(n):
  every contraction-order method (factorised or not) is 2^{Θ(n)} on such instances.

## 3. What the new algorithms actually exploit (OpenAI manuscript, §2.1–2.2, read in source)
- Start: #F = Σ_x Π_e Φ_e(x), Φ_e = 1 − Π_{v∈e}(1 − L_{e,v}(X_v)) — the same rank-2 clause factorisation.
- The lever: after disjoint sparsification and variable copying, every variable occurs in <= 3 clauses, so the product has total
  degree <= 3n (linear); interpolation in an auxiliary parameter then recovers the exact count from sums over small variable groups.
  Appendix D implements the bounds by tensor contraction — of the TRANSFORMED (interpolated) network, not of the original one.
- Consequence: the algorithms beat every contraction-order method on expander instances (2^{o(n)} vs 2^{Θ(n)}). Their gain is
  not contraction width; it is low total degree under bounded occurrence plus interpolation.

## 4. Transfer to circuits with high fan-out
- High fan-out is not the obstacle: copying makes occurrence bounded (as the paper does for k-CNF) at the cost of more variables.
- The obstacle is the number of variables N: a circuit as a product of LOCAL factors needs one variable per internal gate
  (N = n + s), and the bound 2^{O(N/sqrt(log N))} beats 2^n only for N <= n·sqrt(log n)/C. Eliminating internal variables
  instead produces non-local factors (the circuit's function has degree up to n in all inputs), which the grouping/interpolation
  step cannot use.
- So the transfer question is exactly T24's encoding question: a product of local, bounded-occurrence factors over
  n·polylog variables for every size-n^k circuit. Local tensor rank, axis order and fan-out do not enter.

## Decision (gate)
SWAP / 2+2 factorisation: NO ASYMPTOTIC LEVER — constant factor (<= k) in the contraction exponent at best; already the first
step of the published algorithm. Not computed (no GPU run). If an exact implementation is ever wanted for validation: integer
arithmetic (int64 suffices only for n <= 62; otherwise Python integers or modular arithmetic), not float32/float64.
The live question remains T24 (variable-efficient local encodings of circuits).
