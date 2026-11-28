# T52 — Functional quantifier elimination and degree reduction over F3 (owner's theorem; PI check and composition analysis, 2026-11-27)

Status: CLAIMED (Claude family only). Symbolic only. **Corrected 2026-11-28 (PI, owner gap analysis): §1(a), §3, §4 now carry the input-only rows; see §1′.**
Prerequisites:
- T41 §7, Theorem T: 1-in-3 = affine ternary code {Ax = 1} with "no 2s".
- Proofbook 1895: Chevalley–Warning / Ax–Katz, KNOWN_RESULT.
- Rows 2199/2200: Ax–Katz on the affine slice x0 + Bz never applies, because each Boolean axiom has degree 2 in z.
- T48 9.4 (functional gadgets), T51 (T-D, E2).

## 1. Theorem (owner), checked, with one correction
**Setting.** φ is a positive 1-in-3 formula with external inputs x (Boolean) and internal variables. Over F3,
EXACT1(a,b,c) ⇔ a+b+c = 1 with a,b,c ∈ {0,1}; this is T41 Theorem T. Gauss over F3 parametrizes the affine solutions of the internal
variables as y_i = a_i(x) + ℓ_i(z), with z ∈ F3^d.
**Correction (PI).** The domain factor has to range over **all** internal variables, including the free parameters z_j themselves.
Otherwise z_j = 2 allows additional solutions, uniqueness fails, and cancellations are possible.
So let m = number of all internal variables, let Q(x,z) = Π_{i=1}^m (y_i − 2) (each factor affine in (x,z)), and let F(x) = Σ_{z∈F3^d} Q(x,z).
**(a)** If every Boolean x has at most one Boolean extension (functional encoding), then F(x) = Q(x,z*) = (−1)^{#ones of the extension}
or F(x) = 0. Hence F(x) ≠ 0 ⇔ an extension exists. *Proof:* Q(x,z) ≠ 0 ⇔ all y_i ∈ {0,1}. Each nonzero term is 1 or 2 = −1 per factor,
and there is at most one such term. ∎
**(b)** deg_x F ≤ m − 2d. *Proof:* Σ_{t∈F3} t^k equals −1 if k > 0 and k is even, and 0 otherwise. So a monomial x^α z^β survives only
if every β_j is ≥ 2 and even. deg Q ≤ m, therefore |α| ≤ m − 2d. ∎ This is a Chevalley–Warning-type computation (row 1895); its form
(nonzero indicator, functional) is not in the proofbook. Novelty against the literature is not checked.

## 1′. Correction: input-only rows (2026-11-28; verified by full enumeration of the 16-input example)
Gauss elimination of the internal variables can leave r rows that involve only the inputs: r_j(x) = 0 (affine over F3, j=1..r). The parametrization
y_i = a_i(x) + ℓ_i(z) is a solution family only on {x : r(x)=0}; elsewhere the system has no F3 solution at all, but the polynomial F = Σ_z Q is still defined and can be ≠ 0.
- **Counterexample (exact).** x1+x2+y=1, x3+x4+y=1, y Boolean: r(x) = x1+x2−x3−x4, m=1, d=0, F=y−2 with y = 1−x1−x2 (deg 1 = m−2d). F ≠ 0 on 7 of the 16 inputs where the system is unsatisfiable, e.g. x=(0,0,1,1).
- **(a′)** F_corr(x) := Π_{j=1}^r (1 − r_j(x)²)·Σ_{z∈F3^d} Q(x,z). If every Boolean x has at most one Boolean extension, then F_corr(x) ≠ 0 ⇔ an extension exists (r(x)=0 forces the parametrization to be valid). Matches the satisfiability predicate on all 16 inputs of the example. No affine F3 polynomial equals that predicate (all 243 checked).
- **(b′)** deg F_corr ≤ (m−2d) + 2r =: e*(φ). (b) deg F ≤ m−2d stays true for F as defined; only (a) needed the extra factor.
- **Dependent statements, all replaced by e\* = m−2d+2r:** Prop 3.1 (i) e* ≥ wdeg_3(C); (ii) a satisfying input of weight ≤ e* exists; AND_n: e* ≥ n; §4 below; §6 composition: for the composite, the input-only rows are K2 plus those of φ1, so e* is not additive in general; the §6 formula e = e1+e2+2c (c = rank(K2·L1)) is the change of m−2d only and must be combined with the r-count of the composite.
- **Three different things (do not conflate):** (1) *functional uniqueness* of the Boolean extension: F_corr(x) ∈ {0,±1}; (2) *efficient witness computation*: finding the extension; (3) *propagation completeness*: unit propagation finds it. (1) does not imply (3) or (2): a+b+c=1, a+b+d=1, a+c+d=1 has the unique Boolean solution (1,0,0,0), no unit clause, UP performs 0 steps (F3 has 3 solutions). Whether uniqueness gives efficient search is the unique-SAT/Valiant–Vazirani question (UP vs P), not settled by this theorem.

## 2. Composition: the corrected excess e* is subadditive (rewritten 2026-11-28; replaces Prop 2.1 and §6)
Definitions (all variables counted, T52 §1/§1′): m = # internal variables, d = dim of the affine solution space of the internal variables (given generic inputs), r = rank of the input-only rows, e*(φ) := m − 2d + 2r.
**Proposition 2.1\*.** Compose functional encodings: the outputs u of φ1 are the inputs of φ2. Let K2 = input-only rows of φ2 (rank rk2), L1: z1 ↦ ℓ1(z1)|_u, c := rank(K2·L1). Then
- m = m1 + m2; d = d1 + d2 − c (the c rows with K2L1 ≠ 0 are solvable for z1 given x, so they remove c parameters and are NOT input-only after composition);
- input-only rows of the composite: those of φ1 together with the rk2 − c combinations of K2-rows with K2L1-part 0, hence r ≤ r1 + rk2 − c (equality if independent);
- therefore e*(φ) = m − 2d + 2r ≤ e1* + e2*, with equality iff these input-only rows are independent. The terms ±2c cancel.
*Proof.* Substitute u = a1(x) + ℓ1(z1) into φ2's reduced system: the rows K2·u = κ become K2a1(x) + K2L1 z1 = κ; row-reduce in z1. ∎
(Earlier §2/§6 stated e = m − 2d with e = e1 + e2 + 2c ≥ e1 + e2; that quantity is not the degree bound of the satisfiability polynomial and is superseded.)

**Proposition 2.2 (exact rank form and composition law; derived 2026-11-28, recalculated and checked).** Let A be the full coefficient matrix of a consistent affine system φ over F (columns: inputs and internal variables; the internal variables number m, the fibre dimension is d, r = rank of input-only rows). Then rank A = (m − d) + r (rank of the internal part is m − d; the remaining independent rows are input-only), hence **e*(φ) = 2·rank A − m**. For a composition with disjoint internal variables (u counted once, as an internal variable of φ1), let U_i ⊆ F^{coordinates} be the row spaces embedded in the joint coordinate space. Then rank A_12 = dim(U1 + U2) = rank A1 + rank A2 − dim(U1 ∩ U2) and m = m1 + m2, so
 **e*_12 = e*_1 + e*_2 − 2·dim(U1 ∩ U2).**
Since a vector in U1 ∩ U2 involves only the shared coordinates u, U1 ∩ U2 = (rows of φ1 supported on u) ∩ (input-only rows of φ2, supported on u): its dimension counts the conditions on u imposed by φ2 that φ1 already implies. This gives subadditivity (Prop. 2.1*) and the exact defect: equality e*_12 = e*_1 + e*_2 iff no input condition of φ2 is already a relation of φ1. (Consistency: Prop. 2.1* "equality iff input-only rows independent" is the same statement.) It is an identity of ranks; it says nothing about evaluation cost. Not claimed: that the refined excess e** of Prop. 3.1† below is subadditive (the multilinear reduction of a product of indicators is not controlled by the factors' degrees).

## 3. Lower bound by weak degree (rewritten with e*)
**Proposition 3.1\*.** Let φ_C be a functional encoding with output forced to 1 and F_corr as in §1′. Then F_corr ≠ 0 exactly on C^{-1}(1) and deg F_corr ≤ e*(φ). Hence
- (i) e*(φ) ≥ wdeg_3(C), wdeg_3 = minimal degree of an F3 polynomial whose nonzero set on {0,1}^n is C^{-1}(1);
- (ii) if C is satisfiable it has a satisfying input of Hamming weight ≤ e*(φ).
*Proof (ii).* The multilinear representative of F_corr is ≠ 0; take a minimal monomial S, Möbius inversion gives F̃(1_S) = c_S ≠ 0. ∎
**Proposition 3.1† (refined input contribution; valid, 2026-11-28).** Let P(x) = ∏_j (1 − r_j(x)²) (r_j the independent input-only rows) and ML(P) its multilinear representative on {0,1}^N. Then F_corr = P·Σ_z Q on the cube, and since the multilinear reduction of a product has degree ≤ the sum of the degrees, **wdeg_3(C) ≤ m − 2d + deg ML(P) =: e**(φ) ≤ e*(φ).** deg ML(P) can be far below 2r: for a row x_i − 1 = 0, 1 − (x_i−1)² = x_i on the cube (degree 1, not 2); in general deg ML(P) ≤ number of input variables occurring in the rows. Open: the structure of reduced input rows (e.g. rows of Hamming support ≤ 2 give factors of degree ≤ 2 per row, but rows with large support and coefficients ±1 are the costly case).
**Reference calculation (CORRECTED 2026-11-28 — my first version ignored that the internal variable y must be Boolean; the owner's recalculation is right).** φ: x1+x2+y = 1, x3+x4+y = 1 over F3, **all five variables Boolean**. A = [[1,1,0,0,1],[0,0,1,1,1]], rank 2, m = 1 ⇒ d = 0, r = 1 (input-only row x1+x2−x3−x4 = 0), e* = 2·2 − 1 = 3 ✓. The input-only condition is necessary but not sufficient: x = (1,1,1,1) satisfies it but forces y = 2 ∈ F3∖{0,1}, no Boolean extension. Exact enumeration: **5 satisfying inputs** {0000, 0101, 0110, 1001, 1010} and **11 unsatisfying** (not 6/10). Exact F3 linear algebra on the 11 unsatisfying points:
| degree ≤ | dim of polynomials vanishing on all unsatisfying inputs | polynomials with exactly the satisfying support |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 0 | 0 |
| 2 | 1 (spanned by (x1−x2)(x3−x4), which vanishes at the satisfying input 0000) | 0 |
| 3 | 4 | 10 (of 81) |
| 4 | 5 | 32 |
**Analytic proof (replaces the enumeration; owner derivation, re-derived 2026-11-28).** Name the values of f on the five satisfying inputs a = f(0000), b = f(1010), c = f(1001), d = f(0110), e = f(0101); f vanishes on the other 11 points. By Möbius inversion the coefficient of the monomial x_T is Σ_{U⊆T}(−1)^{|T|−|U|} f(1_U), and f(1_U) ≠ 0 only for U = ∅ or the four 2-sets {1,3},{1,4},{2,3},{2,4}. Degree-3 monomials: T = {1,2,3}: −a−b−d; {1,2,4}: −a−c−e; {1,3,4}: −a−b−c; {2,3,4}: −a−d−e. Degree 4: a+b+c+d+e. So multilinear degree ≤ 2 ⇔ a+b+d = a+c+e = a+b+c = a+d+e = a+b+c+d+e = 0. (1st + 2nd) − 5th gives **a = 0** (any characteristic): every polynomial of degree ≤ 2 vanishing on the 11 unsatisfying inputs also vanishes at 0000, so none has the exact satisfying support. The solution space is then b = −d, c = −e, c = −b ⇒ (b,c,d,e) = s·(1,−1,−1,1): dimension 1 (generated by (x1−x2)(x3−x4)). Degree ≤ 3 only requires a+b+c+d+e = 0: dimension 4. Exact support needs all five values in F3* = {±1}: sum of five ±1 ≡ 0 mod 3 ⇔ sum = ±3 ⇔ exactly 4 or exactly 1 of them equal +1: C(5,4)+C(5,1) = **10** (for a = +1: 5, for a = −1: 5), e.g. (1,−1,−1,−1,−1). Degree 4: no condition, 2⁵ = 32 exact-support polynomials. Hence **wdeg_3 = 3** with dimensions 0,0,1,4,5 and counts 0,0,0,10,32 — identical to the enumeration, now derived. No further enumeration is needed for this example.
**Exact weak degree wdeg_3 = 3 = e* = e** (m−2d+deg ML(P) = 1 + 2): the bound is SHARP in this example.** The retracted claims (wdeg = 2; "P = 1−(x1+x2−x3−x4)² has exactly the required support"; "F_corr can be replaced by P") are false: P is nonzero on (1,1,1,1), and it is the factor Σ_z Q (degree 1) that removes that point, which is why the degree is 1 + 2. Lesson recorded: any weak-degree computation for a functional encoding must enumerate extensions over the actual domain of the internal variables, not only the residual input rows.

Example: C = AND_n: e*(φ) ≥ n for every functional encoding. Since m − 2d + 2r = e* and 0 ≤ r ≤ N (N = #inputs): **m ≥ wdeg_3(C) − 2r + 2d ≥ wdeg_3(C) − 2N**; the size consequence "m ≥ wdeg_3" holds only for r = 0 (inputs affinely free). In particular the encoding-size information carried by e* is at most O(N).

## 4. Efficiency (rewritten)
If e* ≤ D, the coefficients of F̃_corr follow by Möbius inversion from the values F_corr(1_T), |T| ≤ D. Each value needs the unique extension of x = 1_T (or its absence): computable in poly time if unit propagation is complete for the encoding (propagation completeness; uniqueness of the extension alone is not enough, §1′). Cost n^{O(D)}·poly. In general e* ≥ wdeg_3(C) can be Θ(n) (AND_n).

## 5. Relation to the external mechanism (T51 T-D) and the contradiction test (unchanged in substance)
- e* is subadditive and poly-bounded (e* ≤ m + 2N). It is the kind of progress measure T51 asks for but fails the decisive property: composition is substitution, F(x) = F1(x)·F2(u(x)) is not a product of the children's polynomials, and the degree arises from summation over z, not from multiplication along gate paths; the VSBR-type balanced decomposition (E2) does not follow.
- Theorem 1 (with §1′), Proposition 2.1\* and Proposition 3.1\* are unconditional; P = NP is not used. **No contradiction.**
- First failing implication: "a low-e* description exists for general poly-size circuits" (false in general: AND_n).
