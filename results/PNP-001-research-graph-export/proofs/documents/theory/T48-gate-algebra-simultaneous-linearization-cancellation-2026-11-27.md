# T48 — Gate algebra over GF(2): simultaneous linearization, cancellation, and the limit for Q-BD (PI, 2026-11-27)

Status: CLAIMED (Claude family only). Cross-family review is pending; the owner has paused new processes.
Prerequisites: proofbook 17917 (merging, Lemma G), 17919 (hybrid normal form), 17920 (Σ3), 17925 (normal form ⇔ P=NP),
17929 (algorithm-structure direction, Q-BD), 17938 (L1–L3), and T43 §3–§5 (Williams, Lemma B, Q-BD).
Method: symbolic only. This document uses no enumeration and no new computations.

## 0. Conventions
Boolean circuits use the basis {+, ·, 1} over F2. Their gates are formal polynomials in F2[x_1..x_n]. The Boolean function that a gate
computes is its class modulo the ideal I = (x_i² + x_i)_i. Its multilinear normal form NF(g) is unique.
- Formal identity means equality in F2[x].
- Boolean identity means equality modulo I.

These are different. For example, D·(1+D) is not formally zero, but it is Boolean-zero. The universal graph encoding over GF(3)
(U_G, prism, Kempe lattice) is not touched here.
A *piece* is an affine subspace P = p + W ⊆ F2^n, with direction W.

## 1. Theorem 1 (simultaneous linearization of one layer; owner's statement, independently checked)
Let A be an affine space of dimension d. Let g_i = a_i·b_i (i = 1..m) be products of affine functions a_i, b_i on A, with linear parts α_i, β_i.
Define r_* = min over all choices ℓ_i ∈ {α_i, β_i, α_i+β_i} of dim span{ℓ_1..ℓ_m}.
**Claim.** The minimum number of pieces that cover A, such that every g_i is affine on every piece, is exactly 2^{r_*}.
Such a minimal cover can be chosen to be a partition.

**Lemma 1.1.** On a piece P = p+W, the product a·b is affine iff α|W, β|W are linearly dependent. Over F2 this means
α|W = 0, or β|W = 0, or (α+β)|W = 0.
*Proof.* After translating to p, write a = α+s and b = β+t on W. Then ab = αβ + tα + sβ + st.
- If α|W and β|W are independent, extend them to coordinates y_1, y_2 of W. Then αβ = y_1y_2, which has degree 2 as a Boolean function. Adding affine terms does not change this.
- If α|W = 0 or β|W = 0, the product is affine.
- If α|W = β|W, then αβ = α² = α as a Boolean function, which is affine.

The last case uses the Boolean identity, not the formal one. ∎

*Proof of Theorem 1.* Lower bound: let P = p+W be any piece on which all g_i are affine. By Lemma 1.1, each i has some
ℓ_i ∈ {α_i, β_i, α_i+β_i} with ℓ_i|W = 0. The choice may depend on P. Then W ⊆ ∩ ker ℓ_i, so
dim W ≤ d − dim span{ℓ_i} ≤ d − r_*. Every piece therefore has at most 2^{d−r_*} points, and any cover needs at least 2^{r_*} pieces.
Upper bound: take an optimal choice, a basis λ_1..λ_{r_*} of its span, and the 2^{r_*} cosets {λ = c}. On each coset, every
ℓ_i vanishes on the direction, so by Lemma 1.1 every g_i is affine. ∎

**Remarks.**
- (i) "r_* ≤ k" is an NP predicate: guess the choices and compute the rank. Whether r_* can be computed in polynomial time is open here.
- (ii) r_* ≤ min(m, d). Theorem 1 is optimal for one layer.
- (iii) Example: for all pairwise products x_jx_k, r_* = d−1.
- (iv) For every layer of g_i = a_ib_i, the rank-1 choice ℓ_i = α_i+β_i = λ gives r_* ≤ 1, whatever m is.

## 2. Composition across layers
**Proposition 2.1 (local recursion).** Suppose the gates of layers < t are affine on a piece P. Then the inputs of layer t are affine on P.
Their linear parts depend on P, because each branch replaces a gate by a, by 0, or by b. Theorem 1 therefore applies to each P separately.
A layer-wise cover has Σ_P 2^{r_*(t,P)} pieces.
The layer-wise greedy cover is not claimed to be optimal for the whole circuit. Section 4 gives a lower bound that holds for every cover,
whichever way it is constructed.

**Proposition 2.2 (direction characterization ends at degree 2).**
- For Q with deg Q ≤ 2, Q is affine on p+W iff B_Q(u,v) = 0 for all u,v ∈ W, where
  B_Q(u,v) = Q(x+u+v)+Q(x+u)+Q(x+v)+Q(x) = Σ_i α_i(u)β_i(v)+α_i(v)β_i(u) for Q = L + Σ a_ib_i.
  This condition does not depend on p.
- For deg Q ≥ 3 the same condition depends on the coset. Example: Q = x_1x_2x_3 and W = span(e_1,e_2). Q is 0 on {x_3 = 0}, and Q = x_1x_2 on {x_3 = 1}.

*Proof.* For deg ≤ 2, D_uD_vQ is the constant B_Q(u,v). Q|_{p+W} has degree ≤ 1 iff all second derivatives along W vanish.
For degree ≥ 3, D_uD_vQ(x) is a non-constant polynomial in x. ∎
Consequence: the polar-form algebra is exact up to multiplicative depth 1. Beyond that, the object is the family of derivatives
D_{u_0}…D_{u_j}C restricted to cosets, and it is no longer linear algebra in the directions.

**Proposition 2.3 (depth 1 is solved without any cover).** If Q = L + Σ a_ib_i, then SAT and #SAT of Q are computable in poly(n, m).
By Dickson's theorem, Q is affinely equivalent to Σ_{j≤h} y_{2j-1}y_{2j} + affine, and the number of zeros follows from h and the affine part.
This is classical and stated from memory. ∎
Simultaneous linearization therefore pays off only from multiplicative depth 2 onwards.

## 3. Theorem 3 (cancellation dichotomy)
Let C be a circuit of size s.
- (a) *Formal cancellation:* whether C = 0 in F2[x] can be decided in coRP. deg C ≤ 2^s. Evaluate at a random point of F_{2^t}^n with t = s+2.
  Schwartz–Zippel bounds the error by 2^s/2^t = 1/4. ∎
- (b) *Boolean cancellation:* whether C ∈ I, i.e. NF(C) = 0, is coNP-complete. This is exactly Circuit-UNSAT.
- (c) *The exact normal form is ⊕P-hard.* The coefficient of x_1⋯x_n in NF(C) equals Σ_{x∈F2^n} C(x) mod 2 = ⊕SAT(C).
  This follows from Möbius inversion: c_S = Σ_{x ≤ 1_S} C(x). ∎
- (d) *Output degree is coNP-hard.* For fixed k, deciding deg NF(C|P) ≤ k is coNP-hard.
  Let C' = C(x)·y_1⋯y_{k+1} with fresh y. Then NF(C') = NF(C)·y_1⋯y_{k+1}, so deg ≤ k iff NF(C) = 0. ∎

Reading.
- All cancellation that goes beyond formal identity comes from the field equations x² = x. The third option in Theorem 1 (a·a = a)
  is the simplest instance.
- "Direct output analysis without making the internal gates affine" is Boolean ideal membership on pieces. Deciding it is the same problem as Q-BD itself.
- Such an analysis yields a running-time gain only if a saving mechanism for that membership exists. Nothing proved so far supplies one.

## 4. Theorem 4 (limit of gate-wise linearization)
**Definition.** A2 is the class of algorithms that run as follows on a circuit C:
- produce a cover of F2^n by pieces, using any procedure, adaptively, including simultaneous linearization in every layer, any order of choices, and merging;
- keep every gate of C as an explicit polynomial of degree ≤ 2 on every piece;
- decide each piece by Gauss or Dickson.

The running time is at least the number of pieces.
**Theorem.** There are a constant c and explicit circuits C_n of size poly(n) that are unsatisfiable, on which every A2 algorithm needs
at least 2^{n−2c·log n−2} pieces. In particular, no A2 algorithm reaches the bound 2^n/n^{ω(1)}.
*Ingredient (verified at the source):* Li, ECCC TR23-023, Theorem 1.7. For every constant ε > 0 there is a constant c and an explicit
extractor E: {0,1}^n → {0,1} with error ε for affine sources of entropy ≥ c·log n. Take ε = 1/4. Then E is not constant on any affine
subspace of dimension ≥ c·log n, i.e. it is an affine disperser with d = c·log n.
*Proof.*
- (i) If E agreed with an affine function l+γ on some V with dim V ≥ d+1, then E would be constant on V ∩ {l = const}. That set has dimension ≥ d. Contradiction.
- (ii) Suppose E has degree ≤ 2 on V with dim V = k. By Dickson there is a subspace of dimension ≥ ⌈k/2⌉ on which E is affine.
  Fix one variable of each hyperbolic pair. By (i), k ≤ 2d+1.
- (iii) Let C_n = E ∧ ¬E. The gate E belongs to C_n, so on every A2 piece it has degree ≤ 2. Each piece therefore has ≤ 2^{2d+1} points,
  and there are ≥ 2^{n−2d−1} pieces. C_n is unsatisfiable, so no early exit is possible. ∎

**Scope.**
- The pieces are affine. Hybrid pieces of the form A \ ∪B_j (17919) are not covered by this proof; that case is open.
- This is a statement about an algorithm class. It is not a general lower bound, and it is consistent with P = NP: under P = NP,
  Circuit-SAT is solved outside A2.
- Novelty is not claimed. The essence (parity decision trees vs. affine dispersers) is presumably folklore.

## 5. Q-BD: exact position
**Proposition 5.1.** Restrict Q-BD to backdoors that are propagation-complete, as in the images of Lemma B. Then Q-BD ⇔ there is a Circuit-SAT
algorithm for poly-size circuits with n inputs in 2^n/n^{ω(1)}·poly(s). This is Williams' hypothesis.
- ⇒: Lemma B (T43).
- ⇐: unit propagation of positive 1-in-3 from a full assignment of X takes ≤ |vars| rounds. It can be written as a circuit of size poly(|φ|) with
  the n inputs X, and SAT(φ) ⇔ that circuit is satisfiable. ∎

So Q-BD is not an easier intermediate problem. It is the open savings problem for general Circuit-SAT.
**Proposition 5.2.** P = NP ⇒ NEXP ⊄ P/poly.
Proof: P = NP gives Σ2^p = P. If EXP ⊆ P/poly, then EXP = Σ2^p by Meyer, cited in Karp–Lipton 1980 (from memory, classical).
That gives EXP = P, which contradicts the time hierarchy. Since EXP ⊆ NEXP, NEXP ⊄ P/poly. ∎
Consequence: the conclusion of the Williams route holds under both P = NP and its negation candidates. So it can never be the
contradicting consequence K of 17920/17929. This confirms the owner's remark.

## 6. Transfer to P ≠ NP: result
- What P = NP forces in this algebra:
  - The rank r_* becomes computable in polynomial time (binary search on the NP predicate "r_* ≤ k"), and a *compact description* of an optimal cover
    (an optimal choice of ℓ_i, hence a basis λ_1..λ_{r_*}) can be found by self-reduction. (Correction 2026-11-28: the explicit minimal cover is NOT computable in polynomial time:
    for the pairwise products x_jx_k, r_* = d−1 (Remark (iii)), the optimal cover has 2^{d−1} cosets, so merely listing it is exponential. Only the description and per-coset queries are polynomial.)
  - Boolean ideal membership (Thm 3b) becomes polynomial.

  All of these follow from P = NP through NP-predicates only, so they relativize. In the AW world (17590) they all hold, and no contradiction is possible.
- ⊕P-hardness of the normal form (Thm 3c) is not known to follow from P = NP. This document derives no consequence K from it.
- The obvious chain "Theorem 4 + every polynomial-time algorithm can be simulated in A2 ⇒ P ≠ NP" fails.
  Its second premise S ("every poly-time Circuit-SAT algorithm yields poly-size A2 covers") is equivalent to P ≠ NP:
  - if P ≠ NP, S holds vacuously;
  - if P = NP, Theorem 4 contradicts S.

  S is therefore an equivalent formulation, and also a forbidden transfer (representation ⇒ decision). It is not a route.

## 7. Result
- **Strongest established new statements.**
  - Theorem 1 is checked, including Lemma 1.1, which says exactly where Boolean cancellation enters.
  - Theorem 3 is the cancellation dichotomy: formal cancellation is coRP, Boolean cancellation is coNP-complete, and the normal form is ⊕P-hard.
  - Theorem 4 is the limit of gate-wise linearization at 2^n/poly(n). It holds unconditionally, given Li 2023, which was verified at the source.
  - Proposition 5.1 states the equivalence of Q-BD with Williams' hypothesis.
  - Proposition 5.2 shows that the Williams route cannot supply a contradiction with P = NP.
- **First unproved implication (Q-BD).** A saving mechanism for Boolean ideal membership on pieces of general polynomial-size circuits,
  outside A2 and outside formal identity. Equivalently, Williams' hypothesis. Open.
- **First unproved implication (P ≠ NP), unchanged from 17920/17929.** A consequence K of P = NP whose derivation contains a non-relativizing step and
  whose negation is proved unconditionally. The gate algebra yields only relativizing NP-predicate consequences. No K exists so far.
- P ≠ NP has not been proved.

## 8. Addendum (owner, 2026-11-27): defect propagation, an algebraic certificate outside A2
Status: the owner derived it; the PI has checked it. Cross-family review is still pending.

**Corrections to Sections 5 and 7 (owner).** Prop. 5.2 has been checked against the literature. A second proof goes through
IKW (NEXP ⊆ P/poly ⇒ NEXP = MA) and P = NP ⇒ MA ⊆ Σ2 = P, which contradicts the hierarchy. Q-BD is therefore excluded as a direct route to a
contradiction with P = NP. A solution of Q-BD would be an independent result (NEXP ⊄ P/poly), not P ≠ NP.

**Theorem 8.1 (owner: certificate in linear size).** Arithmetize the circuit D (n inputs, s gates) over F2. There are polynomials
Q_1..Q_n, computed jointly by one arithmetic circuit of size O(s), such that
D² − D = Σ_i Q_i·(x_i² − x_i) holds formally in F2[x].
*Proof (checked).* Write e(a) = a² − a. In characteristic 2:
- XOR c = a+b: e(c) = a²+b²+a+b = e(a)+e(b). The cross term 2ab vanishes.
- NOT c = 1+a: e(c) = e(a).
- AND c = ab: e(c) = b²·e(a) + a·e(b). Check: (a²−a)b² + a(b²−b) = a²b² − ab.

Propagate weights backwards, like reverse-mode differentiation:
- start with w(out) = 1;
- for XOR and NOT, add w(c) to the weight of each input;
- for AND, set w(a) += w(c)·b² and w(b) += w(c)·a;
- at a fan-out, the weights add.

Each edge costs O(1) operations, and at the inputs Q_i = w(x_i). ∎
Remark: the existence of such a representation is trivial, because I is the vanishing ideal of F2^n and g² = g holds pointwise. The content of
the theorem is the explicit O(s) bound. The table holds only in characteristic 2. In characteristic 3, the setting of the universal graph,
XOR = a+b−2ab, and the coefficients change.

**Corollary 8.2.** C_n = E ∧ ¬E = E(1+E) = E² − E (char 2). Theorem 8.1 gives an O(s) certificate that C_n ∈ I.
Checking it needs one formal identity test of a circuit, which is in coRP (Thm 3a). No evaluation, no pieces and no normal form are
needed. The A2 counterexample of Theorem 4 is therefore not a barrier for "A2 + formal identity + defect certificates". The A2 barrier remains correct
for A2 itself.

**Classification (from the literature, search 2026-11-27; full texts not yet read).** A certificate of the form
f = Σ g_j f_j + Σ h_i (x_i² − x_i), measured by algebraic circuit size, is exactly the Ideal Proof System (IPS) of Grochow–Pitassi
(FOCS 2014, JACM). It p-simulates Extended Frege. Superpolynomial IPS lower bounds for Boolean tautologies imply VP ≠ VNP.
Theorem 8.1 is therefore an IPS certificate of linear size for the Boolean defect. Its novelty is not claimed.

**Proposition 8.3 (scope of the extended class).** Corollary 8.2 uses only the syntactic form E(1+E). Let C' = E ∧ E~, where E~ is a
structurally different circuit for ¬E. A certificate for C' needs a compact certificate of E + E~ + 1 ∈ I, i.e. of circuit equivalence.
A uniform barrier for "pieces + IPS certificates" would be an IPS lower bound, and by Grochow–Pitassi it would imply VP ≠ VNP.
So for the extended class there is neither a saving proof nor an attainable barrier proof without algebraic circuit lower bounds.
(No lower bound is used as a premise here; this is only a classification.)

**Consequence for Q-BD.** Separate (i) the full normal form (⊕P-hard, Thm 3c) from (ii) a compact certificate (Theorem 8.1). Certificates can be
much cheaper, as 8.2 shows. A saving for Q-BD would need, on ≤ 2^n/n^{ω(1)} pieces, certificates of polynomial size for the zero pieces,
and those certificates would also have to be found. Finding certificates is a search problem. It is not solved here.

## 9. Addendum (owner, 2026-11-27): certificate transfer between a computation and its gate representation
Status: the owner derived it; the PI has checked it and added 9.3–9.5. Cross-family review is still pending. Q-BD and IPS lower bounds are deliberately not reopened.

**Theorem 9.1 (owner: deviation propagation, checked).** Let C be a circuit with n inputs and s gates. Introduce a variable z_v and a gate equation
g_v = z_v − p_v(z_a, z_b) for each gate, with z_{x_i} = x_i. Let f_v(X) be the arithmetized gate polynomial and E_v = z_v − f_v(X). Then:
- AND: E_v = g_v + z_a·E_b + f_b·E_a;
- XOR: E_v = g_v + E_a + E_b;
- NOT: E_v = g_v + E_a;
- inputs: E = 0.

Backward weights (w_o = 1; AND: w_b += w_v·z_a and w_a += w_v·f_b; XOR/NOT: pass the weight on; fan-outs add) give
z_o − f(X) = Σ_v R_v g_v with R_v = w_v. The f_b come from the circuit itself, so the joint size is O(s). ∎
Remark: this holds over every field and for every gate polynomial p of constant arity, because p(z) − p(f) = Σ_j (z_j − f_j)·Δ_j
with divided differences Δ_j of constant size.

**Corollary 9.2 (owner, checked).** Suppose f = Σ Q_i (x_i² − x_i). Then 1 = (1 − z_o) + Σ R_v g_v + Σ Q_i (x_i² − x_i).
This is an IPS refutation of {1 − z_o, g_v, x_i² − x_i}. The extra cost is O(s).

**Proposition 9.3 (reverse direction, made precise by the PI).** Let
1 = A·(1 − z_o) + Σ B_v g_v + Σ C_i (x_i² − x_i) + Σ D_v (z_v² − z_v)
be any refutation of the gate system. Boolean axioms on z are allowed. Substitute z_v := f_v(X). The g_v vanish formally, and
z_v² − z_v becomes f_v² − f_v. Multiply by f and use f(1 − f) = −(f² − f). This gives an expression for f in the ideal of the
x_i² − x_i. To keep the overhead linear, Σ_v D_v·(f_v² − f_v) has to be traced back to the inputs **jointly**: run Theorem 8.1 once with
initial weights w_v := D_v at all gates at the same time. The propagation is linear in the initial weights. Running Theorem 8.1
separately per gate would cost O(s²). With the joint run the overhead is additive O(s). ∎
So the certificate sizes for "f ∈ I" and "the gate system is unsatisfiable" agree up to an additive O(s), for IPS certificates in
Hilbert form with shared circuits.

**Proposition 9.4 (transfer to Lemma-B images and to the GF(3) encoding; PI).** Let R be a reduction from circuits to CSP instances made of
constant-size gadgets. Assume each gadget is functional: its auxiliary variables are uniquely determined by its interface variables.
Let the domain be finite, S ⊆ F, with domain axioms π_S(y) = Π_{σ∈S}(y − σ). Then the minimal IPS certificate sizes for C and for R(C) agree
up to an additive O(#gadgets).
*Proof.*
- Local lemma: the ideal generated by a gadget's constraints together with the domain axioms of its constant number of variables is radical,
  because it is zero-dimensional and contains square-free univariate polynomials. Hence every polynomial that vanishes on all local solutions
  lies in it, with coefficients of constant size (Nullstellensatz for grid points; Alon, Combinatorial Nullstellensatz, Lemma 2.1, cited from memory).
- Forward direction: each gate equation g_v vanishes on the gadget solutions, so it is a local combination of constant size.
  Substitute into the certificate.
- Reverse direction: the auxiliary variables are functional. Interpolation gives polynomials of constant degree in the interface variables.
  After substitution, each gadget constraint vanishes on all Boolean (or domain) points that satisfy the gate equation. By the local lemma it
  therefore lies in (g_v, domain axioms), with coefficients of constant size.
- Copy chains are equations y − y'.

Each gadget adds O(1). ∎
Application:
- Lemma B (positive 1-in-3, domain {0,1}, constraints x+y+z−1, xy, yz, xz) is covered.
- A gadget-based circuit → 3-colouring reduction over GF(3) (domain {0,1,2}, axiom y³ − y) is also covered, provided its gadgets are functional.
  This covers the colour-gadget part of the U_G/prism encoding.

The p-equivalence U_G ↔ U_H (17913) concerns generating functions, not certificates. It is not covered.

**Proposition 9.5 (existence, size and construction; PI, following the owner's §4).**
- (a) Under P = NP, PIT ∈ P, because BPP ⊆ Σ2 ∩ Π2 = P (Sipser–Gács–Lautemann, classical). "There is an IPS certificate of size ≤ k"
  is an NP predicate. So under P = NP, finding a certificate of size ≤ k is possible in poly(k, s) by self-reduction, whenever one exists.
- (b) If all unsatisfiable circuits have IPS certificates of polynomial size, then coNP ⊆ MA: Merlin sends the certificate and Arthur runs
  randomized PIT. Proof immediate. ∎
- (c) Existence of polynomial-size IPS certificates for all unsatisfiable instances does not follow from P = NP by any known argument.
  Cook–Reckhow shows only that some proof system is p-bounded iff NP = coNP, not that IPS is.

Every consequence of P = NP here goes through NP predicates. They relativize and hold in the AW world (17590). So there is no candidate for K.
The first unproved implication is unchanged (17920/17929).

**9.6 Correction (2026-11-28): transfer of an existing certificate ≠ construction of a formal certificate.**
- *Transfer (Props 9.1–9.4, unconditional):* given an IPS/NS certificate for one representation (circuit f ∈ I, or the gate system), produce one for the other in additive O(s) (O(#gadgets)). Input: a certificate. Output: a certificate. Cost: size + O(s), verification by PIT (poly under P = NP).
- *Construction (not provided):* obtain a certificate for an unsatisfiable instance (or f ∈ I) from an algorithm that merely decides unsatisfiability. 9.5(a) gives it only through the NP predicate "certificate of size ≤ k exists" and then only when such a certificate exists; (c) existence of poly-size certificates is not implied by P = NP. A decision procedure A with time n^κ is not a certificate: unrolling its tableau as a formal refutation is the missing algorithm → formal-certificate link, and its size is not controlled.
- So every statement above that says "certificate size agrees" is conditional on a certificate being given; nothing here constructs one. (Dependents: T49 §6, T59 §5–§6, T61 §5/§7 read the transfer in this sense.)
