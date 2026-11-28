# T52 — Functional quantifier elimination and degree reduction over F3 (owner's theorem; PI check and composition analysis, 2026-11-27)

Status: CLAIMED (Claude family only). Symbolic only: no enumeration, no runs.
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

## 2. Composition (owner §4): the excess is additive
Define the excess e(φ) := m − 2d.
**Proposition 2.1.** Compose two functional encodings by substitution: the outputs u of φ1 become the external inputs of φ2. Then
m = m1 + m2 and d = d1 + d2, so e = e1 + e2.
*Proof.* The internal variables of φ2 are y2 = a2(u) + ℓ2(z2), and u = a1(x) + ℓ1(z1) is affine. Substitution gives forms affine in (x, z1, z2)
without any new equation, so the solution space has dimension d1 + d2. The variables u are counted in m1. ∎
Fan-out (copy chains) consists of gadgets of its own, and their excess adds as well. For a circuit, e = Σ_gadgets e_g.

## 3. Lower bound: no transformation can push the excess below a function invariant
**Proposition 3.1.** Let φ_C be a functional encoding with the output forced to 1. Then F ≠ 0 exactly on C^{-1}(1). On {0,1}^n, F has a
unique multilinear representative F̃ with deg F̃ ≤ deg F ≤ e. Then:
- (i) e ≥ wdeg_3(C), where wdeg_3 is the minimal degree of an F3 polynomial whose nonzero set on {0,1}^n is C^{-1}(1) (weak degree).
- (ii) If C is satisfiable, C has a satisfying input of Hamming weight ≤ e.

*Proof of (ii).* F̃ ≠ 0. Take a minimal monomial S of F̃. Möbius inversion gives F̃(1_S) = c_S ≠ 0. ∎
Example (proved): for C = AND_n the only satisfying input is 1^n, so every functional encoding of AND_n has excess ≥ n.
Consequence: the excess is a property of the function, bounded below by its weak F3-degree. Encodings and transformations cannot remove it.
This is not a new structure measure. It reduces to the classical weak degree (literature on weak/nonzero degree over F3, e.g.
Smolensky-type bounds, cited from memory).

## 4. Efficiency (owner: "does low degree give an efficient coefficient computation?")
If e ≤ D, then the coefficients of F̃ are computable by Möbius inversion from the values F(1_T) with |T| ≤ D. Each value is obtained in
poly time by unit propagation, because the extension is unique. Cost: n^{O(D)}·poly, and SAT(C) is decided by checking all inputs of weight ≤ D.
So low excess ⇔ an explicit low-degree description, and it can be computed without evaluating the sum over z.
For general circuits, however, e ≥ wdeg_3(C), and that can be Θ(n). Example: AND_n, exactly n.

## 5. Relation to the external mechanism (T51 T-D) and the contradiction test
- The excess is additive and poly-bounded (≤ m = O(s)). It is the kind of progress measure that T51 asks for, but it fails the decisive property:
  - composition yields F(x) = F1(x)·F2(u(x)), which is substitution, not a product of the children's polynomials;
  - the degree arises from summation over z, not from multiplication along gate paths.

  So the VSBR-type balanced product decomposition (E2) does **not** follow. Moreover, the degree bound is informative only if e < n, while e ≥ wdeg_3(C).
- Contradiction test: Theorem 1, Proposition 2.1 and Proposition 3.1 are unconditional. P = NP is not used. They are statements about encodings and
  representations of a function (representation ⇒ decision is a forbidden transfer). **No contradiction.**
- Proved and usable: functional QE over F3 as an exact nonzero indicator, additivity of the excess, and the lower bound by weak degree.
- First failing implication on this path: "a low-excess description exists for general poly-size circuits". It is false in general
  (AND_n: e ≥ n), and the excess does not supply the product structure that E2 needs.

## 6. Correction to Proposition 2.1 (owner, 2026-11-27; checked by the PI)
Proposition 2.1 tacitly assumed that φ2's affine system is solvable for **every** input value in F3^k, i.e. that its reduced echelon form
has no row that involves only input variables.
In general, let K2 be the input-only rows of φ2 and L1: z1 ↦ ℓ1(z1)|_u. If the composite fibre is nonempty, then d = d1 + d2 − c with
c = rank(K2·L1), and hence **e = e1 + e2 + 2c ≥ e1 + e2**.
- Exact condition: c = 0 ⇔ K2·L1 = 0.
- Sufficient: K2 = 0, i.e. φ2's inputs are affinely free.
- Functional uniqueness on Boolean inputs does not guarantee c = 0 over F3^k.

Proposition 3.1 and the AND_n bound are unaffected: they concern the whole encoding, and c ≥ 0 only increases e.
