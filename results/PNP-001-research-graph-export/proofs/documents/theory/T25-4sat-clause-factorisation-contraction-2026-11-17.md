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
- **[CORRECTED 2026-11-28 — three graphs, not one.]** (i) tw_primal (variables adjacent iff they share a clause) bounds variable elimination on the hypergraph network;
  (ii) tw_inc (variable–clause incidence graph) bounds elimination after the rank-2 clause factorisation; (iii) the Markov–Shi theorem is stated for networks whose indices join two
  tensors and gives cost 2^{tw(L(G))} with the **line graph** L(G) of the network graph G; a variable of occurrence degree D is a tensor of degree D, so L(G) contains a clique K_D and
  tw(L(G)) ≥ D−1. The statements "cost 2^{Θ(tw)}" are upper bounds for the stated elimination orders; matching lower bounds hold for generic tensors only, **not** for COPY (δ) tensors or
  clause tensors of CP rank 2, which are far from generic. Explicit family: F_m = ⋀_{i≤m} (x ∨ a_i ∨ b_i ∨ c_i). Incidence graph = tree (tw 1); primal graph: x joined to all 3m
  other variables, each clause a K_4 ⇒ tw_primal = 3; line graph of the incidence graph ⊇ K_m ⇒ tw ≥ m−1. Exact count: x = 1 satisfies every clause (8^m assignments of the a,b,c),
  x = 0 leaves 7 assignments per triple ⇒ **#F_m = 8^m + 7^m** (poly time by conditioning on the single high-degree variable, i.e. cutset size 1). Hence a width parameter of the *line graph*
  does not measure the cost; a high-degree variable has the COPY tensor δ_D (CP rank 2): splitting it into its two basis terms (a cutset of size 1) removes the degree. The cost-relevant graph is the one
  **after** COPY decomposition: tw_inc (here 1), or more precisely the cutset-conditioned width (tw of the incidence graph after deleting a conditioning set C, plus |C|). Not rejected: the COPY rank-2
  decomposition (still valid and is what makes tw_inc ≤ tw_primal+1 and the cutset reading possible); recomputed: which graph governs the exponent.
- **[CORRECTED 2026-11-28 — random 4-CNF.]** The previous claim "incidence graph is an expander w.h.p." is false for the whole graph: for m = αn clauses of 4 uniform variables a given variable is absent with
  probability (1−4/n)^{αn} → e^{−4α}, so ≈ n·e^{−4α} variables are isolated (linear number for every fixed α), and the graph has isolated vertices, hence is not connected, hence not an expander.
  Correct scope: (a) α below the giant-component threshold of the random 4-uniform hypergraph (α_c = 1/(4·3) = 1/12 [R]) all components have size O(log n): tw = O(log n) and contraction is poly;
  (b) above it there is a giant component and a 2-core (variables of degree ≥ 2 after iterated removal of degree-1 variables and pendant clauses); a linear-treewidth/expansion statement can be
  asserted for that **core** only, for densities where known results apply [R: not re-read in this session]; the exponential contraction exponent is then Θ(|core|), i.e. proportional to the core fraction,
  which is a function of α. The general sentence "2^{Θ(n)} for every contraction-order method on random 4-CNF at constant density" is therefore **not established**; established: it holds with n replaced by the
  core size once core expansion is available, and not below the threshold.

## 3. What the new algorithms actually exploit (OpenAI manuscript, §2.1–2.2, read in source)
- Start: #F = Σ_x Π_e Φ_e(x), Φ_e = 1 − Π_{v∈e}(1 − L_{e,v}(X_v)) — the same rank-2 clause factorisation.
- The lever: after disjoint sparsification and variable copying, every variable occurs in <= 3 clauses, so the product has total
  degree <= 3n (linear); interpolation in an auxiliary parameter then recovers the exact count from sums over small variable groups.
  Appendix D implements the bounds by tensor contraction — of the TRANSFORMED (interpolated) network, not of the original one.
- Consequence (scope corrected: on the expanding **core** of instances where core expansion is known, see §2): the algorithms beat every contraction-order method there (2^{o(n)} vs 2^{Θ(n)}). Their gain is
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
