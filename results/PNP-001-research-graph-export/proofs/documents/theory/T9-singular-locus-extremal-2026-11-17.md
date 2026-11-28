# T9 — O1: The extremal Hessian rank on the permanent's singular locus (torus bound; M_4 = 10) (PI, 2026-11-17)

Owner-driven; PI-verified (exact). Continues T8. The extremal quantity is M_n := max over X ∈ Sing(V(perm_n)) of rank Hess(perm_n)(X),
Sing = {perm_n(X)=0 AND ∇perm_n(X)=0}. Result: **M_n = Θ(n²)**, tightly bracketed; **M_4 = 10 exactly**. char 0 / exact field arithmetic.

## 0. Admissibility gate (binding rule for every candidate, before any rank computation)
A candidate X ∈ 𝔽^{n×n} is a singular point ONLY if, in **exact** field arithmetic (cyclotomic field for roots of unity — never
floating-point zero tolerances), **perm_n(X) = 0 AND all n² first derivatives ∂perm_n/∂x_ij (X) = 0** (the (n−1)-sub-permanents). Fourier
matrices are a cautionary case: F_4, F_5 have perm = 0 but ∇perm ≠ 0 (e.g. ∂perm_4/∂x_00(F_4) = −2) — NOT singular; only F_6 is singular,
with rank Hess(perm_6)(F_6) = 16 < 20 (below the block construction). (Owner, exact in cyclotomic fields.)

## 1. Torus-kernel Lemma (owner; PI-verified exactly) — the upper bound

**Lemma T9-A (corrected 2026-11-28).** For X ∈ Sing(V(perm_n)) let r, s = number of nonzero rows, nonzero columns of X, and c = number of
connected components of the bipartite support graph of X (rows ∪ cols, edge iff X_ij ≠ 0), counting only non-isolated vertices. Then
**rank Hess(perm_n)(X) ≤ n² − r − s + c.** In particular, if X has no zero row and no zero column (r = s = n), rank ≤ n² − 2n + c.
*(The earlier universal form n² − 2n + c, "including isolated nodes", was wrong when X has zero rows/columns: a zero row i gives vec(E_ii X) = 0,
which adds nothing to the kernel. Exact invalid step: counting 2n generators instead of r+s. Valid parts kept: the identities
Hess·vec(E_ii X)=0, Hess·vec(X E_jj)=0 and the component relations. Every use of the lemma in this file has r = s = n, or uses the separate
zero-row Case A, so no theorem below changes; only the stated scope.)*

**Derivation.** perm is torus-invariant: perm(D_L X D_R) = (∏_i α_i)(∏_j β_j)·perm(X), D_L=diag(α), D_R=diag(β). Differentiate in x_kl:
perm'_{kl}(D_L X D_R) = (∏_{s≠k}α_s)(∏_{t≠l}β_t)·perm'_{kl}(X). Differentiate again in α_i at α=β=1: the left side gives
[Hess·vec(E_ii X)]_{(k,l)}; the right side is a multiple of perm'_{kl}(X) = 0 at a singular point. Hence **Hess·vec(E_ii X) = 0** for every row i and
**Hess·vec(X E_jj) = 0** for every column j. These are r + s nonzero vectors (zero rows/columns give the zero vector). Their span is the image of the
torus Lie algebra, (a,b) ↦ Σ a_i E_ii X + Σ b_j X E_jj. Its kernel is {(a,b): a_i + b_j = 0 on every support edge}: a constant t_C on the rows and −t_C
on the columns of each component C, dimension exactly c on the r+s non-isolated vertices. So the span has dimension **r + s − c** and lies in ker Hess,
hence rank Hess ≤ n² − r − s + c. ∎
*Verified exactly (rational arithmetic, 2026-11-28):* X = diag(B,B), B=[[1,1],[1,−1]] (n=4, r=s=4, c=2): kernel dim 6, rank 10 = n²−r−s+c (tight).
X = the same with row 3 zeroed (r=3, s=4, c=2): gradient 0, the 8 identities hold, the span has dimension 5 = r+s−c (not 2n−c = 6), rank Hess = 6 ≤ 11.

## 1′. General block family (proved 2026-11-28; closes the pending obligation of §3a)

For k ≥ 2 put B_k = [[−(k−1), 1ᵀ],[1, I_{k−1}]] (k×k).
**(a)** perm B_k = 0: expand along row 1: −(k−1)·perm I + Σ_{j≥2} perm(B_k minus row 1, col j). In each such minor row j has lost its identity entry, so it is
forced to column 1 and the rest is the identity: perm = 1. Total −(k−1)+(k−1) = 0.
**(b)** G_k(a,b) := perm(B_k minus row a, col b) gives G_k = [[1,1ᵀ],[1, J_{k−1} − 2I_{k−1}]]. Entries: (1,1): perm I = 1; (1,j): 1 as in (a); (i,1): row 1 is forced to
column i, rest identity: 1; (i,i), i≥2: −(k−1)+(k−2) = −1; (i,j), i≠j≥2: row j forced to column 1, column i forced to row 1: 1.
**(c)** det G_k = (−2)^{k−1}: the Schur complement of the entry 1 is (J − 2I) − 11ᵀ = −2I_{k−1}. So G_k is invertible in every characteristic ≠ 2.

**Theorem T9-C.** Let P (k×k), Q (l×l), k,l ≥ 1, perm P = perm Q = 0, X = diag(P,Q), n = k+l. Then X ∈ Σ(perm_n) and Hess(perm_n)(X) is a direct sum of
two interaction blocks:
 – 𝒫×𝒬 (entries of P against entries of Q): the rank-one matrix vec(G_P) vec(G_Q)ᵀ and its transpose, a contribution of rank 2 when G_P, G_Q ≠ 0;
 – 𝒪₁×𝒪₂ (entry (a,d), a∈P rows, d∈Q cols, against entry (c,b), c∈Q rows, b∈P cols): value G_P(a,b)·G_Q(c,d), i.e. G_P ⊗ G_Qᵀ up to reordering of
   indices, with its transpose: a contribution 2·rank(G_P)·rank(G_Q), which is 2kl when both are invertible;
 – every other pair of index classes (𝒫×𝒫, 𝒬×𝒬, 𝒪₁×𝒪₁, 𝒪₂×𝒪₂, 𝒫×𝒪_i, 𝒬×𝒪_i) is 0.
Hence **rank Hess(perm_n)(X) = 2 + 2·rank(G_P)·rank(G_Q)** (G_P, G_Q ≠ 0), and **= 2kl + 2 for P = B_k, Q = B_l (k,l ≥ 2).**
*Proof.* H[(a,b),(c,d)] = perm of X with rows a,c and columns b,d removed (a≠c, b≠d; else 0). The remainder is block diagonal with a P-part and a Q-part and has
nonzero permanent only if both parts are square. Counting removed rows/columns per block: 𝒫×𝒫 leaves perm(P minor)·perm Q = 0; 𝒬×𝒬 likewise; 𝒫×𝒬 leaves
G_P(a,b)G_Q(c,d); 𝒪₁×𝒪₂ leaves G_P(a,b)G_Q(c,d); every other pair leaves a non-square block. The two nonzero blocks sit on disjoint index sets. ∎
*Exact check (rational arithmetic, 2026-11-28):* (k,l) = (2,2),(2,3),(3,3),(2,4),(3,4): ranks 10, 14, 20, 18, 26 = 2kl+2; det G_k = (−2)^{k−1} confirmed.
For k = 1, P = [0] (zero row and column, G_P = [1]) the formula gives 2l+2, consistent with the zero-row bound 2n.
**Consequence.** M_n ≥ max_{k+l=n}(2kl+2) = ⌊n²/2⌋ + 2 for every n ≥ 4: a theorem now for all n (before: verified only for (2,2),(2,3),(3,3)).
The formula depends on G only through its rank; block pairs with singular G_P or G_Q give smaller ranks and are not covered.

## 2. Satz T9-B: M_4 = 10 (PROVEN — full case analysis; owner, PI-verified exactly)

**Upper bound.** Let X be a singular point of perm_4.
- **Case A: X has a zero row (or column).** Say row i = 0. Then the second derivative ∂²perm/∂x_{ab}∂x_{cd} vanishes whenever both index
  pairs avoid row i, and whenever both lie in row i; only cross terms (one variable in row i, one outside) survive, giving the block form
  Hess = [[0, B],[Bᵀ, 0]] with B ∈ ℂ^{4×12}. Hence rank Hess ≤ 2·4 = **8**. (Verified: max rank over zero-row singular points = 8.)
- **Case B: X has no zero row and no zero column.** Every connected component of the bipartite graph has ≥1 row and ≥1 col node. A singular
  point must have c(X) ≤ 2. **[Clean argument, review-supplied — covers non-square components too.]** In any pattern with c ≥ 3 components and
  no zero row/col, there is a 3×3 sub-permanent (delete two rows and two columns suitably) that reduces to a **single uncancellable transversal
  term** — a product of 3 nonzero entries, hence ≠ 0. Concretely: c = 4 ⟹ generalized permutation matrix, perm ≠ 0; c = 3 with the square
  partition (2,2)+(1,1)+(1,1) ⟹ ∂perm/∂(2×2 entry) = (opposite entry)·e·f, a single term, whose vanishing forces a zero row; c = 3 with a
  non-square partition such as (2,1)+(1,2)+(1,1) ⟹ the 3×3 sub-permanent deleting the extra row and extra column is a single product a·c·e ≠ 0.
  In every case some first derivative is nonzero, so X is not singular. Hence c ≤ 2, and Lemma T9-A (here r = s = 4) gives rank Hess ≤ 4²−4−4+2 = **10**.
  (Independently re-verified: adversarial search found max rank 10, 0 singular points among the non-square c=3 family.)
Maximum over both cases is 10.

**Lower bound.** X_4 = diag(B,B), B = [[1,1],[1,−1]] (perm B = 0), is singular with rank Hess(perm_4)(X_4) = 10 (T8 §7; c=2, torus bound
tight; B = B_2, the case k=l=2 of Theorem T9-C). Hence **M_4 = 10.** ∎ (C_4 over ℚ(i) also achieves 10 but is row/col-permutation-equivalent to diag(B,B).)

**[Correction of an auxiliary claim.]** An intermediate argument asserted that for a *rectangular* c=2 structure like (1,3)+(3,1) the Hessian
vanishes. That is FALSE. Owner counterexample, verified exactly: X = [[1,1,1,0],[0,0,0,1],[0,0,0,1],[0,0,0,1]] is singular with rank Hess = 9
(e.g. ∂²perm/∂x₂₁∂x₃₂ = 1, 0-based). This does NOT affect Satz T9-B: X has c=2, so Lemma T9-A already gives rank ≤ 10; its actual rank 9 is
below the balanced diag(B,B) value 10. Rectangular (unbalanced-component) c=2 singular points exist and must be handled by the torus bound,
not by any "H=0" claim. M_4=10 is additionally confirmed EXHAUSTIVELY (all 3¹⁶ {−1,0,1} matrices: 220,737 singular points, max rank 10).

## 3. M_n = Θ(n²) — the general upper bound WITHDRAWN; asymptotics still hold

**[CORRECTION, owner 2026-11-17.]** My earlier general bound "M_n ≤ n²−⌈3n/2⌉" via "c ≤ ⌊n/2⌋" is **FALSE and withdrawn**: a 1×1 block
with a *nonzero* entry is a valid component, so c is not bounded by ⌊n/2⌋. Counterexample (owner, verified exactly): for n=5,
X = diag(1, B, B) has no zero row/column, is singular, but c = 3 > ⌊5/2⌋ = 2, with rank Hess(perm_5)(X) = 10. The n=4 proof (Satz T9-B)
does NOT use that false step — it uses the complete case analysis above, valid because at n=4 a c=3 no-zero-row/col point cannot be singular
(the second singular 2×2 block that kills the derivative at n=5 has no analogue at n=4). 

**Corrected general bound (owner, PI-verified): M_n ≤ n²−n−2 (n ≥ 4).** Proof via Lemma T9-A: if X has a zero row/column its Hessian has the
block form [[0,B],[Bᵀ,0]], rank ≤ 2n ≤ n²−n−2 (n ≥ 4). Otherwise the nonzero graph has no isolated node, and a singular point must have
c ≤ n−2: c = n is a generalized permutation matrix (perm ≠ 0, not singular); c = n−1 forces either a 2×2 component (⟹ a nonzero first
derivative inside it, as in §2 Case B) or a pair of unbalanced complementary components of sizes k and n−k (an unbalanced bipartite
component has no perfect matching, and yields a nonzero sub-permanent derivative) — neither is singular. So c ≤ n−2 and T9-A gives
rank ≤ n²−2n+(n−2) = n²−n−2. ∎ Combined with the construction:
  **⌊n²/2⌋ + 2 ≤ M_n ≤ n²−n−2** (n ≥ 4) — Θ(n²) (lower ½, upper 1); the upper bound is not claimed optimal.

**n=5: M_5 ∈ [14, 18] (PROVEN bracket); exact value OPEN.** What is and is NOT established:
- **Square two-block family (PROVEN = 14):** rank Hess(diag(B_k,C_ℓ)) = 2kℓ+2 (Theorem T9-C, any k,ℓ),
  maximized over k+ℓ=5 at (2,3) → 14. This is ONLY the square two-block family.
- **NOT yet bounded ≤14 (open):** rectangular (unbalanced-component) c=2 points — T9-A gives only ≤ 17 — and c=3 points — T9-A gives only
  ≤ 18. So the earlier inference "only a connected point can exceed 14" is **WITHDRAWN**: decomposable points with rectangular components
  or three components are a priori allowed up to 17/18 and must be bounded algebraically, not assumed. Tested exactly: rectangular c=2
  (owner's X = [[0,1,−1,0,0],[1,−1,−1,0,0],[0,−1,−1,0,0],[−1,−1,−1,0,0],[0,0,0,1,1]], sizes (4,3)+(1,2)) → rank 8; c=3 diag(1,B,B) → 10;
  connected c=1 → ≤12 found. Nothing exceeds 14 yet, but no proof for the rectangular/c=3/connected cases.
- **The connected case (Fall D) — the key tool.** Σ(perm_n) = {∇perm_n = 0} is the critical (singular) locus; the Hessian H is the Jacobian
  of ∇perm_n, so the Zariski tangent space satisfies T_X Σ = ker H, giving **dim ker H ≥ dim_X Σ**, i.e. **rank H ≤ n² − dim_X Σ**. The
  torus orbit of X has dimension ≤ 2n−1 = 9 (and lies in Σ), recovering rank ≤ 16 for connected X. A PROOF of M_5 = 14 would follow if
  every connected singular point lies in a component of Σ(perm_5) of dimension ≥ 11 (⟹ rank ≤ 14). Whether dim Σ(perm_5) ≥ 11 on every
  connected component is the exact open obligation (ties to the open singular-locus geometry of the permanent, 2024 literature).
- **Next task:** bound the rectangular-c=2, c=3, and connected-c=1 cases algebraically (not by random matrices); or construct a singular
  point with rank ≥ 15.

## 4. Consequence for pc — the corank obstruction is RESOLVED (integrated with T8 §8, 2026-11-28)

(Earlier version of this section presented "push every singular point into the intrinsic corank-≥4 locus" as an open dimension/incidence question. It is closed by
T8 §8: corank 4 ⟹ rank Hess_F ≤ 6 and corank ≥ 6 ⟹ Hess_F = 0, hence **rank Hess_F(p) > 6 ⟹ corank A(p) = 2**, where Lemma T8-B gives rank ≤ 4m−4.)

**Theorem (unconditional modulo T8 §3, §8).** Let F = perm_n = Pf(A(x)) with A affine alternating of size 2m. The block point X = diag(B_k,B_l), k+l = n ≥ 4, is a singular
point of V(perm_n) with rank Hess(perm_n)(X) = 2kl+2 ≥ 10 > 6 (Theorem T9-C). By T8 §8, A(X) has corank exactly 2 (it is tangency-induced by T8 §1), so T8-B applies:
2kl+2 ≤ 4m−4. With k = ⌊n/2⌋: **2m ≥ (⌊n²/2⌋+6)/2**, i.e. pc(perm_n) ≥ ⌈(⌊n²/2⌋+6)/2⌉ (= n²/4+3 for even n, (n²+11)/4 for odd n): **quadratic in n**, unconditionally on the corank question.
Status: the dependence is on the proofs in T8 §3 (Schur-complement identity, rank ≤ 4m−4) and T8 §8 (corank 4/≥6 normal forms), which are stated there and were read
(not independently re-derived) in this session; novelty versus the literature on Pfaffian lower bounds is NOT settled. What it does NOT give: a bound beyond quadratic, since
M_n ≤ n²−n−2 (§3) and Hessian rank at singular points is the only input used.
**What stays open (replacing the former "blind spot"):** whether a *non-block* singular point of Σ(perm_n) (connected support, c=1) can have Hessian rank larger than 14 (n=5)
or ⌊n²/2⌋+2 in general — M_n exact. That is a question about Σ(perm_n) alone, not about Pfaffian embeddings.

## 5. Status
PROVEN & verified THREE ways (PI derivation + exact sympy + independent reasoning model gpt-oss-120b): **Lemma T9-A** (torus-kernel bound
rank ≤ n²−r−s+c, = n²−2n+c without zero rows/columns; corrected 2026-11-28, §1) and **Theorem T9-C** (rank 2kl+2, §1′) and **Satz T9-B** (M_4 = 10, full case analysis). The admissibility gate. M_n = Θ(n²) (lower ½,
upper ≤ n²−n−1). **WITHDRAWN (false):** the general upper bound M_n ≤ n²−⌈3n/2⌉ and the step c ≤ ⌊n/2⌋ (owner's n=5 counterexample
diag(1,B,B): c=3, rank 10). OPEN: exact M_5 ∈ [14,17] (needs the correct c-stratification incl. decomposable c=3 points); the
(the component-incidence obstruction is RESOLVED by T8 §8 + Theorem T9-C, see §4; exact M_n for connected points remains open). Novelty of T9-A / 2kℓ+2 vs. literature: not settled — NOT claimed as published-new.
Independent adversarial review of T9-A and T9-B (separately): pending.

## 3a. Non-equidimensionality of Σ(perm_5) — cleaned theorem, witnesses, literature (2026-11-17)

**Theorem.** The critical scheme Σ(perm_5) ⊂ 𝔸²⁵_ℂ is **NOT equidimensional over ℂ**: it has irreducible components of dimension 11
and 15, each generically smooth (smooth where the relevant gradient matrices are invertible; not smooth as varieties). Verified three ways (PI exact sympy; gpt-oss-120b reasoning; CherryMe adversarial exact).

**11-dim component V_{2,3} (new).** V_{2,3} = {diag(B,C) : perm_2(B)=0, perm_3(C)=0}, with perm_2, perm_3 irreducible over ℂ, is irreducible
of dim (4−1)+(9−1)=11 and ⊆ Σ (every 4×4 submatrix of a block-diagonal contains all of B or all of C ⟹ all 4-sub-permanents vanish).
Witness X_A = diag(B_0, C_0), B_0=[[1,1],[1,−1]], C_0=[[−2,−2,2],[−2,0,−1],[0,2,1]]. **Corrected gradient matrices** (exact):
G(B_0) = [[−1,1],[1,1]], det −2; **G(C_0) = [[−2,−2,−4],[2,−2,−4],[2,−2,4]], det 64** (both ≠ 0). rank Hess(perm_5)(X_A) = 2·2·3+2 = 14,
so 11 = dim V_{2,3} ≤ dim_{X_A}Σ ≤ dim T_{X_A}Σ = 25−14 = 11 ⟹ dim_{X_A}Σ = 11, smooth point of the unique 11-dim component.
(Local dimension of an irreducible variety is constant at every point, smooth or not — no gap.)

**15-dim components (two types, both KNOWN in the literature).**
- Type B: two zero rows (or two zero cols); linear, dim 15. Witness X_B (rows 0,1 zero, rows 2–4 ones): rank Hess = 10, dim T = 15.
- Type C (1×4 block split, complementary permanent): W_{1,4} = {diag(0,D) : D∈ℂ^{4×4}, perm_4(D)=0}, dim 16−1 = 15, ⊆ Σ. Witness
  X_C = diag(0, D_0), D_0 = [[−1,−1,1,−1],[−1,0,0,1],[1,0,−1,−1],[1,−1,0,−1]]: perm_4(D_0)=0, det G(D_0)=−32 (≠0),
  rank Hess(perm_5)(X_C) = 10, dim T = 15 — a separate generically smooth 15-dim component (one zero row + one zero col + perm_4(D)=0), NOT a
  two-zero-rows component.

**Literature / novelty (owner survey, to double-check).** The 15-dim components are known: the Type-C family (vanishing row + vanishing col
+ vanishing complementary permanent) appears in Bläser–Ikenmeyer–Jindal–Lysikov, *Ulrich complexity* (2017), used for the codim-2n lower
bound; the two-zero-rows family is the trivial lower-bound family in Xie (arXiv:2609.27320). What is **not** in the surveyed literature
(Bläser et al. 2017; Kirkup 2005; Boralevi–Carlini–Michałek–Ventura arXiv:2402.17839; Xie 2026): the **11-dim block component V_{2,3}** and
the resulting **non-equidimensionality of Σ(perm_5)**. Those references study only the global/maximal dimension (codim 2n) or minimal
primes for 2×2, 3×3 sub-permanents; none constructs multi-block diag(B,C) components or addresses equidimensionality for n=5. So the 11-dim
component and the non-equidimensionality conclusion are the standalone new contribution; full-literature novelty remains to be confirmed.

**Generalization (PROVED 2026-11-28 via Theorem T9-C).** For k+ℓ=n, k,ℓ≥2: V_{k,ℓ} = {diag(B,C): perm_k(B)=perm_ℓ(C)=0} is irreducible of dim
(k²−1)+(ℓ²−1) = k²+ℓ²−2 (perm_k, perm_ℓ irreducible). It lies in Σ. At the witness X = diag(B_k,B_ℓ) (G_k, G_ℓ invertible) T9-C gives
dim T_XΣ = n²−2kℓ−2 = k²+ℓ²−2 = dim V_{k,ℓ}. Let Z be an irreducible component of Σ containing V_{k,ℓ}; then dim V ≤ dim Z = dim_X Z ≤ dim T_XΣ = dim V, so Z = V:
**V_{k,ℓ} is an irreducible component of Σ(perm_n)**, and Σ is smooth (reduced, of dimension dim V) at every point of V where det G_B · det G_C ≠ 0. That set is open
and nonempty in the irreducible V, hence dense. **Scope:** V_{k,ℓ} is generically smooth, NOT smooth as a whole: at points where B or C is a singular point of perm_k / perm_ℓ
the variety V is singular, and the Hessian-rank formula changes. (Earlier wording "smooth components" here and in the 11/15-dim theorem above means generically smooth.)
Non-equidimensionality: Σ contains the linear space of matrices with two zero rows, of dimension n(n−2), so some component has dimension ≥ n(n−2). Since
k²+ℓ²−2 < n(n−2) ⇔ kℓ ≥ n, true for k,ℓ ≥ 2 and n ≥ 4 (kℓ ≥ 2(n−2) ≥ n), the component V_{k,ℓ} is strictly smaller: **Σ(perm_n) is not equidimensional for every n ≥ 4.**
(n=4: V_{2,2} has dimension 6 < 8.)
