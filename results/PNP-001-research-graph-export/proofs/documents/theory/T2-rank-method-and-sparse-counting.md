# T2 — The partial-derivative rank method cannot certify hardness of sparse counting polynomials

Status: written proof by Fable, 2026-11-16. Not machine-checked. Elementary and probably folklore; novelty is not claimed.

## Setting
- G is a graph with n vertices, maximum degree Δ and m ≥ n/2 edges.
- The multivariate independence polynomial is Z_G(w) = sum over independent I of prod_{i in I} w_i. It is the weighted counting
  polynomial of the positive 2-CNF F_G of T1, with I = the 0-set.
- For a partition (A, B) of the variables, the coefficient matrix M_{A,B}(Z_G) has rows I_A ⊆ A and columns I_B ⊆ B, with entry
  [I_A ∪ I_B independent]. This is exactly T1's cut matrix.

## Satz 5
For a uniformly random balanced partition (A, B), with probability 1 - exp(-Ω(n)):

    rank M_{A,B}(Z_G) ≤ 2^{n/2} (3/4)^{c n},   c = c(Δ) > 0.

Proof:
1. Rows with I_A not independent in G[A] are zero. So rank ≤ i(G[A]), the number of independent sets of G[A].
2. If a graph H has a matching of size ν, then i(H) ≤ 2^{|V(H)|} (3/4)^ν: each matched edge admits 3 of 4 patterns, and every other
   vertex contributes at most a factor 2.
3. An edge lies inside A with probability ≈ 1/4. So e(G[A]) has mean ≈ m/4 ≥ n/8. It is concentrated by bounded differences, since
   moving one vertex changes it by at most Δ. A graph of maximum degree Δ with e edges has a matching of size ≥ e/(2Δ - 1), so
   ν(G[A]) = Ω(n) with probability 1 - exp(-Ω(n)). ∎

## Consequence
- Raz's multilinear-formula lower bounds (n^{Ω(log n)}) need rank close to full, 2^{n/2 - o(n)}, under random partitions.
- The counting polynomials of bounded-occurrence formulas have a linear deficit (Satz 5, same argument for any CNF with linearly many
  clauses inside a random half).
- So this method cannot certify their hardness.
- Hard polynomials for rank methods need non-local structure (the permanent; full-rank constructions); the reductions from #SAT to
  them create exactly that.

## Literature links (to keep claims honest)
- **T1 Satz 1 is Nisan's theorem (1991, "Lower bounds for non-commutative computation").** The width of a read-once oblivious
  algebraic branching program (ROABP) at layer i equals the rank of the coefficient matrix at cut i.
- **Tensor-train representations along a variable order ARE ROABPs.** For ROABPs both exponential lower bounds (via that rank) and
  quasi-polynomial PIT hitting sets (Forbes–Shpilka 2013) are known. This class is understood; the frontier lies beyond it (sums of
  ROABPs, multilinear formulas, general circuits).
- **Nisan–Wigderson designs and extractors** turn ASSUMED hardness into pseudorandomness. They prove no lower bound.
- **The only rigorous bridge in the other direction is Kabanets–Impagliazzo (2004):** derandomising polynomial identity testing
  implies a circuit lower bound (NEXP ⊄ P/poly, or the permanent has no polynomial-size arithmetic circuits).

## Remark on "efficiently findable structure"
Deciding whether one cut rank of a CNF is ≥ 1 is deciding satisfiability: the matrix is zero iff F is unsatisfiable. So the
structure's size cannot be READ OFF efficiently in general (unless P = NP).

T1 Satz 2 sidesteps this: for GIVEN variable and clause orders it computes the ranks on the way, at cost R*^3. The open part of the
owner's central question is therefore precisely "how to find orders with small R*". That is a search problem over orders, not a
computation of ranks.
