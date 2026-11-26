# T9 — O1: The extremal Hessian rank on the permanent's singular locus (torus bound; M_4 = 10) (PI, 2026-11-17)

Owner-driven; PI-verified (exact). Continues T8. The extremal quantity is M_n := max over X ∈ Sing(V(perm_n)) of rank Hess(perm_n)(X),
Sing = {perm_n(X)=0 AND ∇perm_n(X)=0}. Result: **M_n = Θ(n²)**, tightly bracketed; **M_4 = 10 exactly**. char 0 / exact field arithmetic.

## 0. Admissibility gate (binding rule for every candidate, before any rank computation)
A candidate X ∈ 𝔽^{n×n} is a singular point ONLY if, in **exact** field arithmetic (cyclotomic field for roots of unity — never
floating-point zero tolerances), **perm_n(X) = 0 AND all n² first derivatives ∂perm_n/∂x_ij (X) = 0** (the (n−1)-sub-permanents). Fourier
matrices are a cautionary case: F_4, F_5 have perm = 0 but ∇perm ≠ 0 (e.g. ∂perm_4/∂x_00(F_4) = −2) — NOT singular; only F_6 is singular,
with rank Hess(perm_6)(F_6) = 16 < 20 (below the block construction). (Owner, exact in cyclotomic fields.)

## 1. Torus-kernel Lemma (owner; PI-verified exactly) — the upper bound

**Lemma T9-A.** For X ∈ Sing(V(perm_n)) let c = number of connected components of the bipartite graph of X (rows ∪ cols, edge iff
X_ij ≠ 0), counting only non-isolated vertices. Then **rank Hess(perm_n)(X) ≤ n² − 2n + c.**

**Derivation.** perm is torus-invariant: perm(D_L X D_R) = (∏_i α_i)(∏_j β_j)·perm(X), D_L=diag(α), D_R=diag(β). Differentiate in x_kl:
perm'_{kl}(D_L X D_R) = (∏_{s≠k}α_s)(∏_{t≠l}β_t)·perm'_{kl}(X). Differentiate again in α_i at α=β=1: the left side gives
[Hess·vec(E_ii X)]_{(k,l)} (where E_ii X = the matrix carrying only row i of X); the right side is a multiple of perm'_{kl}(X) = 0 at a
singular point. Hence **Hess(perm_n)(X)·vec(E_ii X) = 0** for every row i, and likewise **Hess·vec(X E_jj) = 0** for every column j. The 2n
vectors {vec(E_ii X)}, {vec(X E_jj)} satisfy Σ_i E_ii X = X = Σ_j X E_jj per connected component, i.e. c independent relations, so they span
a subspace of ker Hess of dimension 2n − c. Therefore rank Hess ≤ n² − (2n − c) = n² − 2n + c. ∎
*Verified exactly* (sympy): at X = diag([[1,1],[1,−1]],[[1,1],[1,−1]]) (n=4, c=2) the 8 identities Hess·vec(E_ii X)=0, Hess·vec(X E_jj)=0
hold, ker dim = 6 = 2n − c, rank = 10 = n²−2n+c (tight).

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
  In every case some first derivative is nonzero, so X is not singular. Hence c ≤ 2, and Lemma T9-A gives rank Hess ≤ 4²−2·4+2 = **10**.
  (Independently re-verified: adversarial search found max rank 10, 0 singular points among the non-square c=3 family.)
Maximum over both cases is 10.

**Lower bound.** X_4 = diag(B,B), B = [[1,1],[1,−1]] (perm B = 0), is singular with rank Hess(perm_4)(X_4) = 10 (T8 §7; c=2, torus bound
tight). Hence **M_4 = 10.** ∎ (C_4 over ℚ(i) also achieves 10 but is row/col-permutation-equivalent to diag(B,B).)

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
- **Square two-block family (PROVEN = 14):** rank Hess(diag(B_k,C_ℓ)) = 2kℓ+2 (T8 §7, structural derivation independently verified),
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

## 4. Consequence for pc, and the real next lever (T9 obligation)
**Conditional bound.** If a block singular point (rank Hess = ⌊n²/2⌋+2 > 6) is realized as a **corank-2** point of a Pfaffian representation
F = perm_n, then by T8-B 4m−4 ≥ ⌊n²/2⌋+2, so pc(perm_n) = 2m ≥ ⌊n²/4⌋ + 3 — **quadratic**, below Sheshadri's cubic.

**The blind spot (the genuine open frontier — Satz T9).** A representation A(X) could try to push every point of Sing(V(perm_n)) into the
**intrinsic corank-≥4 locus** {rank A(X) ≤ 2m−4} (codim 6 in alternating matrices), where T8-B does NOT apply (there rank Hess ≤ 6 by T8 §8).
Whether it CAN is a **dimension/incidence** question: a component Z ⊆ Sing(V(perm_n)) (e.g. the block-diagonal variety, codim 4n−6 for the
k=2 family) would have to pull back entirely into the codim-6 locus. Linearizing rank A(X) ≤ 2m−4 along Z couples dim Z (a component of the
permanent's singular locus — whose geometry/codimension is itself open, 2024 literature) to the minimal corank of the bundle A(X) on Z.
**This is the next proof obligation:** does such an embedding exist, or is it obstructed (giving the quadratic pc bound unconditionally)?

## 5. Status
PROVEN & verified THREE ways (PI derivation + exact sympy + independent reasoning model gpt-oss-120b): **Lemma T9-A** (torus-kernel bound
rank ≤ n²−2n+c, including isolated nodes) and **Satz T9-B** (M_4 = 10, full case analysis). The admissibility gate. M_n = Θ(n²) (lower ½,
upper ≤ n²−n−1). **WITHDRAWN (false):** the general upper bound M_n ≤ n²−⌈3n/2⌉ and the step c ≤ ⌊n/2⌋ (owner's n=5 counterexample
diag(1,B,B): c=3, rank 10). OPEN: exact M_5 ∈ [14,17] (needs the correct c-stratification incl. decomposable c=3 points); the
component-incidence obstruction (T8 §7 / the next Satz). Novelty of T9-A / 2kℓ+2 vs. literature: not settled — NOT claimed as published-new.
Independent adversarial review of T9-A and T9-B (separately): pending.

## 3a. Non-equidimensionality of Σ(perm_5) — cleaned theorem, witnesses, literature (2026-11-17)

**Theorem.** The critical scheme Σ(perm_5) ⊂ 𝔸²⁵_ℂ is **NOT equidimensional over ℂ**: it has smooth irreducible components of dimension 11
and 15. Verified three ways (PI exact sympy; gpt-oss-120b reasoning; CherryMe adversarial exact).

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
  rank Hess(perm_5)(X_C) = 10, dim T = 15 — a separate smooth 15-dim component (one zero row + one zero col + perm_4(D)=0), NOT a
  two-zero-rows component.

**Literature / novelty (owner survey, to double-check).** The 15-dim components are known: the Type-C family (vanishing row + vanishing col
+ vanishing complementary permanent) appears in Bläser–Ikenmeyer–Jindal–Lysikov, *Ulrich complexity* (2017), used for the codim-2n lower
bound; the two-zero-rows family is the trivial lower-bound family in Xie (arXiv:2609.27320). What is **not** in the surveyed literature
(Bläser et al. 2017; Kirkup 2005; Boralevi–Carlini–Michałek–Ventura arXiv:2402.17839; Xie 2026): the **11-dim block component V_{2,3}** and
the resulting **non-equidimensionality of Σ(perm_5)**. Those references study only the global/maximal dimension (codim 2n) or minimal
primes for 2×2, 3×3 sub-permanents; none constructs multi-block diag(B,C) components or addresses equidimensionality for n=5. So the 11-dim
component and the non-equidimensionality conclusion are the standalone new contribution; full-literature novelty remains to be confirmed.

**Generalization (next step).** For any k+ℓ=n, k,ℓ≥2: V_{k,ℓ} = {diag(B,C): perm_k(B)=perm_ℓ(C)=0} is irreducible of dim (k²−1)+(ℓ²−1)
= k²+ℓ²−2; the block formula rank Hess(diag(B,C)) = 2kℓ+2 gives dim T = n²−2kℓ−2 = (k+ℓ)²−2kℓ−2 = k²+ℓ²−2 = dim V_{k,ℓ} — EQUAL, so
every V_{k,ℓ} is a smooth component. Since k²+ℓ²−2 < n(n−2) whenever kℓ > n (true for k,ℓ≥2, n≥5), V_{k,ℓ} is strictly below the maximal
dimension ⟹ **Σ(perm_n) is non-equidimensional for every n ≥ 5** (indeed n ≥ 4), ONCE the general 2kℓ+2 formula is proven for all
k,ℓ≥2 (verified for (2,2),(2,3),(3,3); general proof is the pending obligation).
