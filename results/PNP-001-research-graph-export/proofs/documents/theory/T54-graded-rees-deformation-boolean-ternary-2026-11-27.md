# T54 — Graded deformation (Rees algebra) of Boolean and ternary existential algebra (owner's proposal; PI check, 2026-11-27)

Status: CLAIMED (Claude family only); cross-family review pending.
Scope: symbolic work only; no enumeration, no runs, the Lean build was not touched.
Prerequisites: T48 §3/§9, T49 Lemmas 2–4, T50 B1/§4 (MT ⇔ VP=VNP), T51 T-D/E2, T52 (§2–§5 rewritten 2026-11-28), T53.
Proofbook check: no earlier entry on Rees algebras, homogenization of I, or the Frobenius form. The grep hits were the substring "degrees".
External sources read for task 4:
- `ant_paper/ant.txt`, Lemma E.4 (lines 1885–1910) and Lemma K.2 (lines 3213–3240), plus §2.5 (lines 550–575);
- the OAI Lean hypothesis `hpoly` in CompressorLabelEvaluator.lean.

Notation: p ∈ {2,3}, B = F_p[X]/I with I = (x_i^p − x_i), and f̄ is the reduced representative (exponents < p).
R = R_{p,n} = F_p[t,X]/J, with J = (x_i² − t x_i) for p = 2 and J = (x_i³ − t² x_i) for p = 3.

## 1. Structure (owner task 1). This is standard material and not new.
**Theorem 1.1.** The following hold.
- (a) J is homogeneous (deg t = deg x_i = 1). The generators form a Gröbner basis: their leading terms x_i^p are pairwise coprime. So R is graded and free over F_p[t] with basis x^α, α ∈ {0,…,p−1}^n.
- (b) ρ: R → B[t], x_i ↦ t x_i, is well-defined, since (tx)^p − t^{p−1}(tx) = t^p(x^p − x). It is injective with image ⊕_D F_D B · t^D, where F_D = span of the reduced monomials of degree ≤ D. Hence R ≅ Rees(B, F) for the degree filtration.
- (c) R/(t−1) ≅ B, and R/(t) ≅ gr_F B = F_p[X]/(x_i^p). Also R/(t−c) ≅ B for all c ≠ 0, via x = c·y. Finally R[t⁻¹] ≅ B[t^{±1}].

*Proof.* For (a): Buchberger's coprime criterion. For (b): ρ sends the basis t^{D−|α|}x^α of R_D to x^α t^D, and these are linearly independent. Relation check: x^p ↦ t^p x^p and t^{p−1}x ↦ t^p x, which are equal in B[t]. ∎
This is the flat degeneration to the initial ideal (in(x^p − x) = x^p) and is standard; the literature is cited from memory.

**Lemma 1.2 (saturation).** Every homogeneous u ∈ R \ {0} is uniquely t^k·u°, where u° is t-saturated (u°|_{t=0} ≠ 0).
For g ∈ F_p[X] with g ≡ f mod I, write g^h = t^{deg g} g(X/t). Then
  **g^h = t^{deg g − deg f̄} · f̄^h   in R,**
and f̄^h is saturated, with f̄^h|_{t=0} = the top form of f̄.
*Proof.* ρ(g^h) = t^{deg g}·g = t^{deg g}·f̄ = t^{deg g − deg f̄}·ρ(f̄^h) in B[t], and ρ is injective. ∎
Consequence: the homogenization of I is J (I^h = J). For every W, Φ_W ∈ I ⇔ Φ_W^h = 0 in R. This is an exact reformulation (see §5).

## 2. Graded functional QE over F3 (owner task 2): verified
**Lemma 2.1.** For a ∈ F3, ev_a: z ↦ t·a is a well-defined F3[t,X]-algebra map R_{n+1} → R_n, because (ta)³ − t²(ta) = t³(a³ − a) = 0.
So the sum is independent of the representative, and the canonical representative is needed only to read off coefficients.

**Theorem 2.2 (owner's identity).** Let Q ∈ R_{n+d}. Since R_{n+d} is free over R_n with basis z^β, β ∈ {0,1,2}^d, it has a unique reduced z-expansion Q = Σ_β Q_β z^β. Then
  Σ_{a∈F3^d} ev_a(Q) = (−t²)^d · C_Q,   where C_Q := Q_{(2,…,2)}.
*Proof.* Σ_{a∈F3} (ta)^b = t^b Σ_a a^b. This is 0 for b = 0 (3 = 0), 0 for b = 1, and 2t² = −t² for b = 2. Take the product over the coordinates. ∎

**Properties.**
- (i) Grading. If Q is homogeneous of degree D, then the sum is homogeneous of degree D, and C_Q is homogeneous of degree D − 2d. T52(b) is exactly this degree statement:
  - Q^h = Π_{i≤m} (y_i^h − 2t) is homogeneous of degree m;
  - F_red = (−1)^d C_{Q^h}|_{t=1} where F_red is the *reduced* representative of F in F3[x]/(x³ − x) (functions on F3^n); (corrected 2026-11-28)
  - hence deg F_red ≤ m − 2d (the bound for the formal F is T52(b), proved directly). With input-only rows the satisfiability polynomial is F_corr of T52 §1′, degree ≤ m − 2d + 2r; Theorem 2.2 applies to Q_corr = Π(1 − r_j²)·Q.
- (ii) Specialization.
  - t = 1: the sum is T52's F.
  - t = 0: the sum vanishes identically (d ≥ 1), so the QE sum itself carries no information at t = 0. Only the "divided" coefficient C_Q carries information there.
- **Corollary 2.3.** C_{Q^h}|_{t=0} = (−1)^d·(degree-e component of F) = [z^{2…2}] Π_i (L_i(x) + ℓ_i(z)) in F3[X,z]/(x³, z³). Here L_i is the linear part of a_i; the constants are multiples of t and vanish. So **C|_{t=0} ≠ 0 ⇒ the T52 bound deg F ≤ e is tight; the converse is FALSE** (correction 2026-11-28).
  - Reason: in R the relation x³ = t²x holds, so a monomial of F with an exponent ≥ 3 (e.g. x³, arising when one variable occurs in ≥ 3 factors L_i) is replaced by t²x and vanishes at t = 0. C|_{t=0} sees only the *cube-free* part (all exponents ≤ 2) of the degree-e component of F, i.e. the degree of the reduced representative, not of the formal polynomial.
  - Counterexample: Q = x³z², d = 1: formal F = Σ_z x³z² = −x³ has formal degree 3 = e (tight), but C_Q = x³ = t²x ≡ 0 at t = 0. Reduced F = −x (modulo x³ − x), degree 1.
  - Likewise "F = (−1)^d C|_{t=1}" holds for the *reduced* F in F3[x]/(x³ − x) (a function on F3^n), so "hence deg F ≤ e" via this route is a statement about the reduced degree; T52(b) for the formal polynomial rests on its own direct proof.
  - Tightness of the *formal* bound is NOT detected by the t = 0 fibre.
- (iii) Multiplication. C is not multiplicative. It is multiplicative only when the eliminated variables are disjoint (C_{Q1Q2} = C_{Q1}C_{Q2}, the tensor case). With shared z there is no product rule.
- (iv) Composition (corrected 2026-11-28). The factor is (−t²)^d with d = d1 + d2 − c, but the degree of the satisfiability polynomial is governed by e* = m − 2d + 2r, which is subadditive and has the ±2c terms cancelling (T52 Prop 2.1*). The earlier "e = e1 + e2 + 2c" concerns m − 2d only.
- (v) Cost. C has no smaller circuits than F, since C|_{t=1} = ±F. The formal QE is VNP-complete (T53), so the graded QE is no cheaper. The division by t^{2d} is free on coefficients but not on circuits.

## 3. Frobenius pairing (owner task 3): verified; it is an instance of a known structure
One variable, p = 3: T(Q) := −[z²]Q. In the basis 1, z, z² we have z³ = t²z and z⁴ = t²z², so the Gram matrix is
M(t) = [[0,0,−1],[0,−1,0],[−1,0,−t²]], and **det M = 1** (checked by expanding along the first row).

**Proposition 3.1.**
- (a) T is a perfect, associative (Frobenius) form over F3[t]. Because det M is a unit, it stays perfect under every base change t ↦ c, including c = 0.
- (b) n variables: R ≅ ⊗_{F3[t]} of the one-variable algebras, with T_n = ⊗T = (−1)^n [x^{(2…2)}]. The Gram matrix is the Kronecker product, with det = 1. So the form is perfect for every n and every t.
- (c) At t = 1, T_n(f) = Σ_{a∈F3^n} f(a): this is the counting pairing ⟨f,g⟩ = Σ f·g. At t = 0 it is the socle (Poincaré-duality) pairing of F3[X]/(x³).
- (d) Relation to QE: Σ_a ev_a(Q) = t^{2d} · T_d(Q) in the eliminated variables.
- (e) p = 2 analogue: T = [x], with Gram matrix [[0,1],[1,t]] and det = −1 = 1. At t = 1, T_n(f) = ⊕_a f(a).

So the deformation interpolates between counting (t = 1) and Poincaré duality (t = 0). For a monic f, A[z]/(f) is Frobenius via the coefficient of z^{deg f − 1} (Euler/Tate trace, cited from memory). Neither the perfectness nor the det = 1 result is specific to QE.
Complexity: evaluating T_n on circuit-given elements at t = 1 is ⊕P-hard (p = 2) or Mod_3P-hard (p = 3). The pairing is a counting object.

## 4. Transfer of the external mechanism (owner tasks 4 and 5)
**What the external steps actually assume (read at the source):**
- **E.4 (lem_balanced)** works over any commutative coefficient ring. It uses:
  - (E4a) an N^k block multigrading of the ring the circuit computes in, with variables of degree e_b and constants of degree 0;
  - (E4b) a target component of degree 1_{[k]} ∈ {0,1}^k, so that the component of a product splits **only into set partitions** A ⊔ B = S. That is the step "the larger part has > k/3 blocks";
  - (E4c) exact computation of the polynomial in that ring.
- **K.2 (lem_lowdeg)** uses a polynomial ring over an A-algebra R, its **X-grading** (recursion for g^{(i)} at product gates), and exact computation.
- **OAI compressor**: `hpoly : circuit.polynomial = map (Int.castRingHom k) (P n)`, an exact equality in MvPolynomial.
- **No pairing anywhere.** None of the three steps uses a bilinear form on the variable algebra. Proposition 3.1 therefore replaces no assumption of theirs.

**What R provides.**
- K.2: R has no X-grading, because x² − t x and x³ − t²x are not X-homogeneous. The only grading is the total degree including t.
- E4a: with one t per block, R^{(k)} = F[t_1..t_k, X]/(x² − t_{b(x)}x) is N^k-graded. So E4a is satisfiable.

**Theorem 4.1 (exactly where the transfer breaks).** Let C be a Boolean circuit computing g ≡ f mod I, with f block-multilinear (e.g. HC_m). In R^{(k)}, C induces only:
- (i) **the unhomogenized lift ĝ** (constants 1). J is multihomogeneous, so its components in R^{(k)} are the images of the formal components of g. Its 1_{[k]} component is the formal block-linear part of g; the monomials of that part are already J-reduced.
  - This is B1 unchanged. Anthropic's example (x_{1,1}² − x_{1,1})x_{2,1}⋯x_{k,1} equals (t_1 − 1)x_{1,1}x_{2,1}⋯ ≠ 0 in R. Its block-linear part is −x_{1,1}⋯x_{k,1}.
  - Boolean correctness is congruence mod J + (t_b − 1), and **(t_b − 1) is not homogeneous**. The inhomogeneity moves from (x² − x) to (t − 1); it does not disappear.
- (ii) **the homogenized lift ĝ^h = t^κ·f^h** (block version of Lemma 1.2), with κ_b = D_b − deg_b f.
  - The formal block degree D_b of a Boolean circuit is up to 2^s.
  - The 1_{[k]} component is 0 unless κ = 0, so E.4 then speaks about the zero element.
  - Applying E.4 to the component D = κ + 1 instead violates E4b. With D_b ≥ 2, the product splits are e + e' = D with e_b, e'_b > 0 both possible, so block b lies on both sides of every cut. The separation g_{S,j}(S) · h_{S,j}(S^c) fails.
  - Tracking all degree vectors costs a factor Π_b (D_b + 1), which is 2^{Θ(s k)} for Boolean circuits.
- K.2 and hpoly break in the same way:
  - low X-degree = high t-power, which is saturation information;
  - equality with f^h holds only for κ = 0.

**First failing implication (tasks 4 and 5):** "the R-values of the gates of a small Boolean circuit are t-saturated (block degree ≤ 1, resp. degree ≤ n)". This is equivalent to exact division by t^κ with κ up to 2^s.

**Theorem 4.2 (cost of saturation).**
- (a) Every Boolean circuit of size s has a homogeneous F2[t,X] circuit of size O(s²) for ĝ^h. Padding with t^δ, δ < 2^s, takes O(s) squarings. So size does not grow, but the degree is up to 2^s, and so is κ.
- (b) Suppose there is an arbitrary R-circuit of size σ computing the saturated element f^h, where deg f ≤ n. Then f has an F2-arithmetic circuit of **formal degree ≤ n** and size O(σn²) that is correct on {0,1}^n.
  - *Proof.* J is homogeneous, so the degree-(deg f) component of any lift is a lift of f^h. Strassen homogenization gives it with gate degrees ≤ n. Then set t = 1. ∎
- (c) Hence "every f ∈ P/poly has poly-size saturated R-circuits" implies that P/poly has poly-size circuits of polynomial formal degree. By VSBR depth reduction (KNOWN, cited from memory) this gives **P/poly ⊆ NC/poly**: unproved, and not a small step. It is the same gap as T51 T-D/E2.
  - In addition: f^h|_{t=0} contains the top coefficient. For deg f = n that coefficient is ⊕_x f(x), so it is ⊕P-hard (T48 Thm 3).
  - The converse (poly formal degree ⇒ saturated R-circuit) is not proved. It would require reducing the degree from poly down to deg f̄ mod I.
- (d) Function side (KNOWN, elementary): in every flattening, rank(top form of f̄) ≤ rank(f̄). The t = 0 fiber is a degeneration of the t = 1 fiber (via R[t⁻¹] ≅ B[t^{±1}] and the scaling x = t y). This is the actual tensor connection.
  - It runs on the **function** side: rank bounds at t = 0 carry over to the Boolean fiber.
  - The circuit side (E.4: small circuit ⇒ small rank) is exactly what Theorem 4.1 blocks.

## 5. Contradiction test under P = NP (task 6)
- §1–§4 are unconditional statements about representations; P = NP is used nowhere.
- With P = NP: by Lemma 1.2, correctness (*) of T49 becomes **Φ_W^h ∈ J, i.e. Φ_W^h = 0 in R**, an exact graded identity. This contrasts with T49 Lemma 3, which shows that correctness is never formal in F[G,x].
  - But Φ_W ∈ I ⇔ Φ_W^h ∈ J (I^h = J), so this is an equivalent reformulation, not a new consequence.
  - *Correction (2026-11-28).* Homogenizing f = Σ a_i g_i to a common degree D gives only t^{D−deg f} f^h = Σ t^{D−deg(a_i g_i)} a_i^h g_i^h, a certificate for t^k f^h, not for f^h. Membership f^h ∈ J = I^h holds by saturation ((g_i^h) : t^∞), but an explicit certificate without the factor t^k, and its size, are NOT obtained by homogenization. The O(s²) size applies to the t^k-form only (and also depends on D). Existence after saturation and efficient construction of the multipliers are different statements.
  - Black-box use of W algebrizes (T49 Lemma 4).
  - A white-box law would be an E.4-type statement about W, and that breaks at saturation (Theorem 4.1).
- Saturation = coefficients of NF = ⊕P-type quantities. P = NP is not known to imply ⊕P ⊆ P/poly (T50 B2). F1–F3 (T53) are unchanged.
- **No contradiction.** The graded deformation removes the missing grading (B1) formally, but moves the obstruction into the inhomogeneous specialization ideal (t − 1). Its invariant core is t-saturation, which implies P/poly ⊆ NC/poly (Theorem 4.2c).
- New and usable:
  - Theorem 2.2 with Corollary 2.3 (the graded QE; the t = 0 fiber detects tightness of the T52 bound);
  - Lemma 1.2 / Theorem 4.1 (the exact form of the obstruction);
  - Theorem 4.2 (the cost of saturation).
- Known and only referenced: Theorem 1.1 and Proposition 3.1.
