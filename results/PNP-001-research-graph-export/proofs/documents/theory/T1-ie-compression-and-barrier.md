# T1 — Compressing the inclusion–exclusion sum along variable cuts: a law and a barrier

Status: written proofs by Fable (2026-11-16), to be checked line by line. No proof tool has checked them. Finite computations below test
the steps where a proof could fail; they prove nothing about all n. Novelty is NOT claimed: Satz 1 is the TT / weighted-automaton
minimality theorem; Satz 3/4 are probably known in substance in knowledge compilation (rank / rectangle lower bounds, mim-width of
expanders). The literature check is pending (see the end).

## 0. Setting

F is a CNF over x_1..x_n with clauses C_1..C_m, and f_F : {0,1}^n -> {0,1} is its indicator.

The owner's formula (inclusion–exclusion over the clauses that are falsified):

    #F = sum over S ⊆ {1..m} of (-1)^{|S|} N(S),

where N(S) = 2^{n - |V(S)|} if no variable occurs positively in one clause of S and negatively in another ("S consistent"), and 0
otherwise. The proof is the usual sieve: N(S) counts the assignments that falsify every clause in S. The sum has up to 2^m terms.

**Question:** can the terms be grouped by their algebraic structure, so that the sum is computed without generating them?

For a bipartition (L, R) of the variables, M_{L,R}(F) is the 0/1 matrix with rows = assignments of L, columns = assignments of R,
entry f_F. For an order x_1..x_n, cut i is L = {x_1..x_i}, and r_i(F) = rank_K M_i(F).

## 1. Why the cut rank IS the compression of the sum

    f_F(x) = prod_j (1 - φ_j(x)),   φ_j(x) = prod over literals l in C_j of [l false under x].

Each φ_j is a product of single-variable factors (rank 1 across every cut), so 1 - φ_j has rank at most 2 across every cut.
Expanding the product gives exactly the inclusion–exclusion terms.

Across cut i, a term S factorises as (left part) x (right part). The left part depends only on S ∩ (clauses with a variable left of
the cut). Grouping the terms by the pattern on the clauses that cross the cut gives at most 2^{c_i} groups (c_i = number of crossing
clauses). The linear dependencies among the groups' left vectors reduce them to r_i independent ones. So:

**Grouping the inclusion–exclusion terms along cut i cannot use fewer than r_i(F) independent classes, and r_i classes suffice** (Satz 1).

## Satz 1 (representation, minimal) — known

For any order there are matrices G_k[b] (b = 0, 1) of size r_{k-1} x r_k with r_0 = r_n = 1 and

    f_F(x) = G_1[x_1] G_2[x_2] ... G_n[x_n],   r_k = rank_K M_k(F),

and no such representation has a smaller r_k. Then

    #F = prod_k (G_k[0] + G_k[1]),

in O(n R^2) field operations, R = max r_k.

Proof: the TT-SVD / minimal weighted automaton construction (Oseledets 2011; Fliess 1974, Carlyle–Paz 1971). Over any field K, by
Hankel-matrix factorisation M_k = A_k B_k with inner dimension rank M_k.

## Satz 2 (an algorithm whose cost is the largest INTERMEDIATE cut rank) — proof below

Let F_j = C_1 ∧ ... ∧ C_j (clause order chosen freely), p a prime, and

    R*_p = max over j and k of rank over GF(p) of M_k(F_j)   (≤ the same over Q).

Then #F mod p is computable in O(m n (R*_p)^3) operations mod p. #F exactly follows by the CRT from O(n / log n) primes of O(log n)
bits.

Proof:
1. **Induction on j.** Maintain a minimal TT T_j of f_{F_j} mod p; its ranks are rank_GF(p) M_k(F_j) ≤ R*_p. T_0 is the all-ones TT
   (ranks 1).
2. **Multiply by the next clause.** Build the TT of 1 - φ_{j+1} with ranks ≤ 2: the sum of the all-ones TT and minus the rank-1 TT of
   φ_{j+1}. The pointwise product of two TTs is the TT of Kronecker-multiplied cores, so its ranks are ≤ 2 R*_p.
3. **Minimise.** Two Gaussian-elimination sweeps (left-to-right: remove dependent left states; right-to-left: remove unobservable
   ones), as in weighted-automaton minimisation over a field (Schützenberger; Cardon–Crochemore). This yields a TT whose ranks equal
   the cut ranks of the represented function, i.e. of f_{F_{j+1}}. Each sweep costs O(n (2R*_p)^3).
4. **Count.** After step m, #F mod p is the product of the summed cores.

Every intermediate representation is exact, so the result is exact modulo p.

**Note.** Satz 2 is an upper bound on the cost of ONE method. Its cost is governed by R*, which depends on both orders and is at least
max_k r_k(F).

## Satz 3 (lower bound by induced matchings) — proof below

For a graph G = (V, E) let F_G = AND over uv in E of (x_u ∨ x_v): the positive 2-CNF whose models are exactly the assignments whose
0-sets are independent. For every bipartition (L, R) of V and every field K:

    rank_K M_{L,R}(F_G) ≥ 2^{μ(L,R)},

where μ(L,R) is the largest t such that G has an INDUCED matching u_1v_1, ..., u_tv_t with all u_s in L and all v_s in R.

Proof:
1. **Restrict to the matched variables.** Set every variable outside {u_s, v_s} to 1: every clause containing one of them is
   satisfied. Since the matching is induced, the only remaining clauses are (x_{u_s} ∨ x_{v_s}).
2. **The submatrix is a Kronecker power.** On the rows "u-part arbitrary, other left variables = 1" and the columns "v-part arbitrary,
   other right variables = 1", M restricts to the Kronecker product of t copies of

       B = [[0, 1], [1, 1]]   (rows x_u = 0, 1; columns x_v = 0, 1),

   with det B = -1 ≠ 0 in every field.
3. **Conclude.** The Kronecker power has full rank 2^t, and a submatrix's rank bounds the matrix's rank.

## Satz 4 (barrier for every tree-shaped grouping) — proof below

Let G have maximum degree Δ and edge expansion h > 0: every S ⊆ V with |S| ≤ |V|/2 has at least h|S| edges to V \ S. Let n = |V|.

(a) **Every linear order** of the variables has a cut with

    rank M_k(F_G) ≥ 2^{h n / (4 Δ^2)}.

(b) **Every tree-shaped exact decomposition** has a bond whose dimension is at least

    2^{h n / (6 Δ^2)}.

   The decompositions covered are a tree tensor network or a branch decomposition: a cubic tree whose leaves are the variables, every
   tree edge inducing a bipartition, the bond dimension at an edge ≥ the rank of that bipartition.

Proof:
1. **Many crossing edges.** (a) Take k = ⌊n/2⌋; the cut has e ≥ h n/2 crossing edges. (b) Every cubic tree with n leaves has an edge
   whose smaller side has between n/3 and n/2 leaves; there e ≥ h n/3.
2. **A large induced matching across the cut.** Pick crossing edges greedily. After choosing uv, discard every crossing edge with an
   endpoint in N[u] ∪ N[v] (at most 2Δ vertices, each with at most Δ edges, so at most 2Δ^2 edges). The chosen edges form an induced
   matching across the cut of size ≥ e / (2Δ^2).
3. **Rank.** Apply Satz 3.

Bounded-degree expanders exist (e.g. random 3-regular graphs, h > 0 with high probability; explicit Ramanujan graphs).

**Consequence (exact, unconditional, limited to this method family):**
- Every compression of the inclusion–exclusion sum that groups terms along the cuts of a variable order, or of a tree decomposition,
  needs 2^{Ω(n)} classes on F_G for a bounded-degree expander G.
- F_G is a monotone 2-CNF. Counting its models is counting independent sets, which is #P-complete already on bounded-degree graphs
  (as far as I know: Greenhill 2000 for degree 3; to be checked).
- So the barrier is consistent with complexity theory and says nothing about P vs NP. It says which kind of compression cannot be the
  general law.

## 5. What remains open, precisely

Compressions that do not follow a tree of variable cuts:
- **Tensor networks with cycles.** Their exact contraction cost is again governed by cut ranks of a contraction order, so Satz 4
  applies to every contraction order of a network whose bonds are variable cuts.
- **General arithmetic circuits** for the polynomial sum_x prod_j (1 - φ_j(x)). Proving super-polynomial lower bounds there is the
  algebraic counterpart of P vs NP / VP vs VNP (Valiant 1979), with the known barriers.

T1 therefore sharpens the owner's question into a formal dichotomy for one broad method class, and names the boundary where the real
difficulty starts.

## 6. Checks of proof steps (PhysalisMe cm-79b294b8605b4c9e, checks/t1_checks.py; tool call only, no model call)

| Item | Result |
|---|---|
| (i) Satz 3, rank ≥ 2^μ on every bipartition | 0 violations on 4,038 bipartitions (Petersen 637, 3x3 grid 255, cubic n=10 637, cubic n=12 2,509), ranks over GF(2) and GF(1000003), μ by exhaustive search; the bound is attained in 475 of them |
| (ii) Satz 2, clause-incremental TT with two elimination sweeps mod p | #F correct on all 10 instances (implication chain, Petersen 2-CNF, K8 2-CNF, 6 random 3-CNF n ≤ 12, one unsatisfiable); the final ranks equal the true cut ranks mod p in every case, so the minimality step of the proof holds there; R* = 2, 12, 3, 10-27, 1 |
| (iii) Satz 4 step 2, greedy induced matching | 30 random balanced cuts of random cubic graphs n = 40: the greedy set is always an induced matching of size ≥ e/(2Δ^2) |

These are finite checks of the proof steps, not proofs.

## 7. Literature (first check, 2026-11-16)

- **Satz 4 is known in substance, in a stronger form** for Boolean compilation targets: Bova, Capelli, Mengel, Slivovsky, "Expander CNFs
  have Exponential DNNF Size". The OBDD version is in Bova & Slivovsky, "On Compiling Structured CNFs to OBDDs": the hard family has
  clauses of two positive literals, each variable in at most 3 clauses, and the proof uses expanders.
- **What T1 adds at most:**
  - the RANK version (Satz 3), which also covers linear representations with cancellation (weighted automata / tensor trains over any
    field), which Boolean DNNF bounds do not directly cover;
  - the exact identification of the owner's inclusion–exclusion grouping with the cut rank (section 1);
  - the clause-incremental upper bound (Satz 2).
  Whether these are new is NOT established. The rank-of-disjointness argument is classical in communication complexity.
- **mim-width of bounded-degree expanders:** linear by the same greedy argument; a source stating it directly was not found yet.
- **Still to check:** TT / weighted-automata minimality references, #IS hardness on bounded degree, tensor-network #SAT.

## 8. Literature list to complete

- TT / weighted automata minimality (Oseledets 2011; Carlyle–Paz 1971; Fliess 1974).
- Rank / rectangle lower bounds for compiled CNFs (Bova, Capelli, Mengel, Slivovsky 2016, "Knowledge compilation meets communication
  complexity").
- mim-width of expanders / grids (Mengel 2018; Brettell et al.).
- #IS hardness on bounded degree (Greenhill 2000; Vadhan 2001).
- Tensor-network #SAT (Biamonte, Morton, Turner 2015; Kourtis et al. 2019).
