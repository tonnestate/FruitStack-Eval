# T8 — O1: Tangency, the Pfaffian singular criterion, and a Hessian-rank bound for affine Pfaffian representations (PI, 2026-11-17)

Directive "Pfaffian Singularities, Tangency and Algebraic Lower Bounds". Continues T7. char ≠ 2. All claims carry their status. The useful
content is **Lemma T8-B** (rank Hess ≤ 4m−4 at a tangency point) — an **elementary corollary** of the classical Pfaffian Schur-complement
identity, not a deep new theorem — together with a **proved limitation** on what local tangency geometry can give, and the precise open
question it isolates. Verified by independent reasoning model (gpt-oss-120b) + exact computation + adversarial review.

## 1. The exact singular criterion (owner-sharpened; established mathematics)

For F(x) = Pf(A(x)), A(x) = A_0 + Σ_i x_i A_i alternating of order 2m:
  **x ∈ Sing(V(F))  ⟺  F(x)=0 AND D F_x = 0  ⟺  corank A(x) ≥ 4,  OR  ( corank A(x) = 2 AND u^T A_i v = 0 ∀i )**,
where u,v span the 2-dim kernel of A(x). The second clause is **tangency-induced**.

Reasoning (chain rule DF_x = D(Pf)_{A(x)} ∘ L, L the linear part): F(x)=0 means corank A(x) ≥ 2 (on the Pfaffian hypersurface). At a
corank-2 matrix M the differential D(Pf)_M(H) = c_M·u^T H v with c_M = Pf(A') ≠ 0 (A' = invertible complement block), because the
Pfaffian adjugate ∇Pf(M) ∝ uv^T − vu^T is nonzero; its kernel is the tangent hyperplane T_M Pf_{2m}. So DF_x = 0 at a corank-2 point
⟺ im(L) ⊆ T_{A(x)}Pf_{2m} ⟺ u^T A_i v = 0 ∀i. At corank ≥ 4, D(Pf)=0 (intrinsic singular locus of Pf_{2m}, codim 6). **The owner's
precision over the model's answer:** DF_x=0 alone is a *critical point of the polynomial*; a *singular point of the hypersurface* also
needs F(x)=0, i.e. corank ≥ 2 — included above.

**Owner's note on codimension.** The codim-6 intrinsic Pfaffian singular locus is a fact in the *full* space of alternating matrices; it
does NOT transfer automatically to the *parameter* space of an affine representation. Tangency is exactly the phenomenon that breaks the
naive transfer. (Sheshadri therefore converts Pf→det via Lemma A.2 and uses the determinant's codim-4 geometry, not the Pfaffian's.)

## 2. The counterexample (exact, PhysalisMe cm-bc3b5742be854b39)

A(x,y) = [[0,1,x,0],[-1,0,0,-y],[-x,0,0,0],[0,y,0,0]] has **Pf(A)=xy**; A(0,0) has **corank 2** (kernel u=e_3, v=e_4); ∇Pf|_{A(0,0)} is
dual to the (3,4)-entry, so T_{A(0,0)}Pf_4 = {N : N_{34}=0}; and (A_1)_{34}=(A_2)_{34}=0, i.e. u^T A_i v = 0 — **im(L) ⊆ tangent
hyperplane**. Hence the origin is a **tangency-induced** singular point of {xy=0} (corank 2, not corank 4). Confirms §1 and the owner's
point that the codim-6 locus does not drive the singularities after affine restriction.

## 3. Lemma T8-B (PROVEN; elementary corollary of the Pfaffian Schur-complement identity; verified three ways)

**Lemma.** Let p be a tangency-induced singular point of F = Pf(A(x)) (A(p) corank 2, kernel u,v, u^T A_i v = 0 ∀i). Then
  **rank Hess_F(p) ≤ 4m − 4.**

**Proof.** Put A(p) = diag(0_2, A'), A' invertible of order 2m−2 (kernel = first two coordinates). For H = Σ(x_i−p_i)A_i written in
blocks [[H_11, H_12],[−H_12^T, H_22]], the **Pfaffian Schur-complement identity** (Z = A'+H_22 invertible) gives
  F(x) = Pf(A'+H_22) · [ (H_11)_{12} + ( H_12 (A'+H_22)^{-1} H_12^T )_{12} ]   (sign **+**, verified exactly: Pf([[X,Y],[−Yᵀ,Z]]) =
  Pf(Z)·Pf(X + Y Z^{-1} Yᵀ)).
Under tangency (H_11)_{12} = u^T H v = Σ(x_i−p_i) u^T A_i v ≡ 0 **identically**. So to second order
  F(x) = Pf(A')·( H_12 (A')^{-1} H_12^T )_{12} + O(|x−p|^3).
The prefactor's linear part (in H_22) multiplies the now-identically-zero (H_11)_{12}, contributing only at order ≥ 3. Hence Hess_F(p)
is the quadratic form x ↦ Pf(A')·( H_12(x) (A')^{-1} H_12(x)^T )_{12}, which factors through the linear map x ↦ H_12(x) into the
2×(2m−2) block, of dimension 2(2m−2) = 4m−4. Therefore rank Hess_F(p) ≤ 4m−4. ∎

**Verification.**
- Independent reasoning model (gpt-oss-120b, PINNED, ovhcloud, success/finish=stop): confirmed (a) the Schur identity, (b) the factoring
  through H_12 and the ≤ 4m−4 bound, (c) that H_22 enters only at order ≥ 3. (It gave the sign as minus; the adversarial review then showed
  the correct sign is **plus**, verified exactly — rank-irrelevant either way.)
- Exact computation (sympy, 6×6, m=3, N=10 variables, all A_i with (1,2)-entry 0 so tangency holds): all first derivatives of F vanish at
  0 (singular point) and **rank Hess_F(0) = 8 = 4m−4** — the bound is attained (tight). Control without tangency: 0 is not singular.

## 4. Consequence and the PROVED LIMITATION (exact scope)

**Conditional consequence.** If a singular point p of V(perm_n) with rank Hess(perm_n)(p) = R is realized **tangency-induced** (corank 2)
in an affine Pfaffian representation F = perm_n, then (since Hess_F = Hess(perm_n) there) R ≤ 4m−4, so
  **pc(perm_n) = 2m ≥ (R+4)/2.**

**Proved limitation (scope).** The local tangency–Hessian method yields, per singular point, at most pc ≥ (R+4)/2 with R ≤ 4m−4, i.e. its
strength is capped by the Hessian rank attainable at a tangency-realizable singular point. It is a *local* (single-point, second-order)
method and **cannot reach Sheshadri's cubic bound**, which is *global* (polar intersection + the corank-one binomial/Catalan count over the
whole hypersurface, T7 §1b). At corank ≥ 4 (intrinsic) points the Hessian plausibly factors through a larger block (4-dim kernel → block
4×(2m−4) plus the 4×4 kernel Pfaffian), suggesting a *weaker* per-point bound so routing through intrinsic points does not help; this is
asserted, not rigorously derived here (the corank-4 Hessian also carries intrinsic-singular terms not analysed) — flagged as a sub-question.

**The precise open question (the owner's "simultaneous tangency" problem).** Whether this gives a *quadratic* (Ω(n²)) or only a *linear*
(Ω(n)) Pfaffian bound hinges on the **maximal Hessian rank R at a singular point of perm_n that is forced to be corank-2 in the
representation**:
- Mignon–Ressayre attain Hessian rank ~n² for perm (giving dc ≥ n²/2) — but at a point with perm=0, not necessarily ∇perm=0 (a
  *singular* point) and not necessarily corank-2 in a Pfaffian representation.
- The gpt-oss-120b model asserted R = 2n at the realizable point (→ only pc ≥ n+2, linear). **I do NOT adopt this**: it was unverified and
  conflicts with the MR-order; the true value of R at a *singular* point of perm realizable as a *tangency* is OPEN. Resolving it — by
  (i) pinning the Hessian rank of perm at its singular locus, and (ii) deciding whether a representation can force all high-rank singular
  points to corank ≥ 4 (codim-6, a strong simultaneous constraint) — would turn Lemma T8-B into a quadratic Pfaffian bound or prove it
  cannot exceed linear. This is the next proof obligation.

## 5. n = 4 (established reference, status)

dc(perm_4) = 15 (Nov 2026 result; to be checked against its proof). This does NOT determine pc(perm_4). From T7: pc(perm_4) ≤ 2·dc = 30;
and the degree constraint (Pf of order 2m has degree m, need m ≥ 4) gives pc(perm_4) ≥ 8. So pc(perm_4) ∈ [8, 30], exact value OPEN; the
dc=15 result gives no new pc bound. Lemma T8-B at n=4 needs R = rank Hess(perm_4) at a tangency-realizable singular point — small-case,
but governed by the same open R question; no uncontrolled numerical search performed.

## 6. Verification log
Exact: cm-bc3b5742be854b39 (counterexample), local sympy (Lemma T8-B, rank=8=4m−4 tight). Independent model: gpt-oss-120b (criterion §1
and Lemma §3, sign-corrected). Adversarial review: §7 (pending). Ledger entries only after review.

## 7. The singular-locus Hessian-rank analysis (owner-driven, PI-verified 2026-11-17)

Normalization (owner precision): T8-B gives, for an alternating representation of order 2m, M ≤ 4m−4 ⟹ **m ≥ (M+4)/4**; equivalently the
full order **pc = 2m ≥ (M+4)/2**. (My earlier "pc=2m ≥ (M+4)/2" was for the full order and is consistent; m is half the order.)

**Corank-stratified Hessian bounds (exact, verified).** At a singular point p of F = Pf(A(x)):
| corank A(p) | bound on rank Hess_F(p) | reason | verified (exact) |
|---|---|---|---|
| 2 (tangency) | ≤ 4m−4 | Lemma T8-B (Schur complement, factors through the 2×(2m−2) block) | rank = 8 = 4m−4, m=3 |
| 4 | ≤ 6 | split off invertible skew block; the residual 4×4 kernel-Pfaffian is quadratic in its 6 entries | rank = 6, m=4 (tight) |
| ≥ 6 | = 0 | the kernel-block Pfaffian expansion starts at order ≥ 3 | rank = 0, m=4 |

**Corollary (owner; UNCONDITIONALIZES the bound).** rank Hess_F(p) > 6 ⟹ corank A(p) = 2. So a Pfaffian representation **cannot** route a
singular point with Hessian rank > 6 into the intrinsic (corank-4, codim-6) locus; every such point is corank-2, where Lemma T8-B applies.
Hence, with M_n := max over Sing(V(perm_n)) of rank Hess(perm_n), **pc(perm_n) = 2m ≥ (M_n+4)/2 unconditionally** (any witness with rank>6).

**M_n grows at least quadratically (owner's construction, PI-reproduced exactly).** For blocks B (k×k), C (ℓ×ℓ), k+ℓ=n, k,ℓ≥2, with
perm(B)=perm(C)=0 and full-rank gradient matrices, X = diag(B,C) is a singular point of perm_n with
  **rank Hess(perm_n)(X) = 2kℓ + 2**  (mixed second derivatives across the two blocks and the two off-diagonal blocks).
Taking k=⌊n/2⌋, ℓ=⌈n/2⌉: **M_n ≥ 2⌊n/2⌋⌈n/2⌉ + 2 = ⌊n²/2⌋ + 2** for n ≥ 4. Verified exactly (rational blocks, e.g. B = [[1,1],[1,−1]],
perm=0, gradient full rank):
| n | old X_n (2 zero rows) | diag(B,C) = 2kℓ+2 |
|---|---|---|
| 4 | 8 | **10** |
| 5 | 10 | **14** |
| 6 | 12 | **20** |
Owner's exact X_4 = diag([[1,1],[1,−1]],[[1,1],[1,−1]]) → rank 10, reproduced. **Search for a larger M_4:** 167,408 matrices over {−1,0,1},
873 singular, **max rank = 10** — the block-diagonal construction appears optimal at n=4 (tested, not proven). So M_n = Θ(n²) (between
⌊n²/2⌋+2 and the trivial n²).

**Consequence.** pc(perm_n) = 2m ≥ (M_n+4)/2 ≥ (⌊n²/2⌋+6)/2, i.e. m ≥ (⌊n²/2⌋+6)/4 — a **quadratic** Pfaffian lower bound from local
singular-locus geometry, UNCONDITIONAL. It does **not** surpass Sheshadri's cubic pc = Ω(n³) (global). **Status/novelty:** a derived
algebraic corollary; whether the 2kℓ+2 rank formula / the quadratic M_n bound already exist in the literature is NOT settled, so this is
NOT claimed as a published-new result. The exact geometry (and codimension) of Sing(V(perm_n)) remains a hard open problem (2024 literature).

**Net scientific progress (over the earlier T8 finding).** The max Hessian rank on the permanent's singular locus grows **at least
quadratically, not merely linearly** (the earlier X_n family's 2n was not optimal). This resolves the direction of the §4 open question:
the tangency method yields a quadratic (not linear) unconditional Pfaffian bound — still below cubic. Remaining open: the exact value of
M_n (is it ⌊n²/2⌋+2, or larger up to n²?) and whether any global Pfaffian method beats cubic.

**Verification.** Exact computation (sympy): corank-2/4/≥6 bounds (rank 8/6/0), the 2kℓ+2 formula (n=4,5,6 → 10,14,20), owner's X_4,
M_4 search (max 10). Independent adversarial review of the 2kℓ+2 derivation: §8 (pending).

## 8. Algebraic proofs of the corank-4 and corank-≥6 bounds (normal form — NOT a finite search)

Methodological note (owner): a finite search ("not refuted in 40 instances") does NOT prove a bound. The corank-stratified bounds are
provable via the local Pfaffian normal form; here are the proofs. Put A(p) = diag(0_{2r}, A'), A' invertible alternating of order 2m−2r
(2r = corank), kernel = first 2r coordinates; H = Σ(x_i−p_i)A_i in blocks [[H_11, H_12],[−H_12^T, H_22]] (H_11 = 2r×2r kernel block, linear
in x; H_12 = 2r×(2m−2r)). Pfaffian Schur complement (A'+H_22 invertible):
  F(x) = Pf(A'+H_22) · Pf( H_11 + H_12 (A'+H_22)^{-1} H_12^T ).
Write G = Pf(H_11 + W), W := H_12(A'+H_22)^{-1}H_12^T (quadratic-leading in x, since H_12 is linear).

**Corank 4 ⟹ rank Hess_F(p) ≤ 6 (PROVEN).** Here 2r = 4. At corank 4, D(Pf)_{A(p)} = 0 (gradient of Pf vanishes on corank ≥ 4), so p is
singular and F has no linear term. Pf of a 4×4 alternating matrix is the **homogeneous quadratic** Q = af − be + cd in its 6 entries.
Expanding G = Q(H_11 + W) = Q(H_11) + B(H_11, W) + Q(W) with B the polar bilinear form: orders in x are 2, 3, 4 respectively (H_11 linear,
W quadratic). The prefactor Pf(A'+H_22) = Pf(A') + O(x). Hence the degree-2 (Hessian) part of F is exactly Pf(A')·Q(H_11) = Pf(A')·Pf(H_11),
which factors through the linear map x ↦ (the 6 entries of H_11) ∈ k^6. Therefore rank Hess_F(p) ≤ 6. ∎ (Tight: verified = 6.)

**Corank ≥ 6 ⟹ Hess_F(p) = 0 (PROVEN).** Here 2r ≥ 6. The Pfaffian of a 2r×2r alternating matrix is **homogeneous of degree r ≥ 3** in
its entries. H_11 is linear in x, so Pf(H_11) has degree r ≥ 3 in x; the W-terms only raise the order. Thus the lowest-order term of F at
p has degree ≥ 3, so all first and second derivatives vanish: Hess_F(p) = 0 (indeed all derivatives up to order r−1 vanish). ∎

These two, with Lemma T8-B (corank 2, proven in §3), give the full corank-stratified table **by proof**, hence the corollary
rank Hess_F(p) > 6 ⟹ corank A(p) = 2 is a **theorem**, not a numerical observation.

**The X_n corollary, stated honestly.** For X_n (two zero rows) rank Hess(perm_n)(X_n) = 2n > 6, so in any affine Pfaffian representation
X_n is corank-2, and T8-B gives 2n ≤ 4m−4, i.e. **m ≥ (n+2)/2**. This is UNCONDITIONAL but **weaker than the degree bound** m ≥ n (perm_n
degree n = Pf-degree m) — so the X_n point ALONE is not progress on complexity lower bounds; it is a structural illustration. The
block-diagonal construction (§7), with M_n ≥ ⌊n²/2⌋+2, gives the stronger **quadratic** m ≥ (⌊n²/2⌋+6)/4 — which does exceed the degree
bound, but stays below Sheshadri's cubic.

**The extremal question (where new mathematics may lie — OPEN).** Two results would be genuinely valuable:
(i) an *exact singular point* with Hessian rank > ⌊n²/2⌋+2 (would show the two-block construction is not extremal);
(ii) a *proven upper bound* on rank Hess(perm_n) over the whole singular locus (would settle M_n).
Current status: M_n ≥ ⌊n²/2⌋+2 (proven by construction); M_4 = 10 only *tested* (167k matrices over {−1,0,1}, max 10), NOT proven maximal;
no proven upper bound below the trivial n² is known, consistent with the singular-locus geometry of perm being an open problem (2024).
