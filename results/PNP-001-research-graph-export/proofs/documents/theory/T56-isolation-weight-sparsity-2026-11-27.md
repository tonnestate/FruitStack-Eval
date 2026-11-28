# T56 — Sparsity of isolation weights; factorized measures (owner's theorem; PI check, 2026-11-27)

Status: CLAIMED (Claude family only). Symbolic only.
Prerequisites: T55 (fibre symmetry), T53 E2/F2.

## 1. Owner's theorem (verified)
Setting: R(x,z) = [z ≤ x componentwise] over F2, and Λ(x,z) = Σ_T c_T(x) z^T is the multilinear expansion in z, with arbitrary coefficient functions c_T.
- For x = 1_S, Σ_{z≤1_S} z^T = 2^{|S|−|T|}·[T ⊆ S], which is 1 mod 2 iff T = S.
- Exact reconstruction Σ_{z∈Z_x} Λ = 1 therefore gives c_S(1_S) = 1 for every S, so spar_z(Λ) = 2^m for **every** correct Λ.
- Λ = Π(1 + z_i) = [z = 0] is correct and has O(m) gates.

Affine version: the solution sets of Mz = b contain P·V_S + q for every fixed affine chart z = Pw + q, where V_S is a coordinate subspace. So the bound holds in every fixed affine basis, while search is in P (Gauss).

The argument is elementary Möbius inversion. A full F2-support of NOR-type indicators is classical. The theorem shows that monomial sparsity is complexity-blind, which is what the owner concludes.

## 2. Factorized sparsity with free coefficients is also complexity-blind (PI)
If the coefficients may be arbitrary functions of x (circuits over the ring B_n in the variables z), then for every relation and every selector S,
  Λ_S(x,z) = Π_i (1 + z_i + S_i(x)) = [z = S(x)]
is a correct isolation weight of B_n-circuit size O(m). With depth and sharing allowed, the coefficients absorb the whole selector. This is the same phenomenon as the G-invariance in T55.

## 3. The only non-blind version charges the coefficients
Measure the joint circuit size of Λ in (x, z).
- Upper bound: O(m + size(S)). Under P = NP (or NP ⊆ P/poly) small correct Λ exist for 1-in-3-SAT.
- A superpolynomial lower bound for all correct Λ would therefore prove NP ⊄ P/poly. It is a circuit lower bound, and the first failing implication of T49 §6 / T55 is unchanged.
- From memory, unverified: over an **extended** witness space (k = O(n²) copies of z, Valiant–Vazirani with fixed advice hashes, ⊕P closed under AND) small weights exist unconditionally. Any route through Λ would therefore have to use the fixed original witness space.

**Result:** monomial sparsity (owner) and factorized sparsity with free coefficients (PI) are both complexity-blind. The only measure that sees sharing, depth and the coefficients is the circuit size of Λ itself. No contradiction.

## 4. Addendum (owner's derivation, PI check, 2026-11-27): small weights exist unconditionally
This addendum replaces the from-memory remark in §3 (O(n²) copies) by a proof.
- **(a) Original witness space, over K = F_{2^r}, with r = n + ⌈log₂(m+1)⌉ + 1.**
  - P_x(Y) = Σ_z R(x,z) Y^z is multilinear with distinct monomials, so P_x ≢ 0 ⇔ ∃z.
  - Schwartz–Zippel plus a union bound give 2^n·m/2^r < 1, so there is a fixed a ∈ K^m with P_x(a) ≠ 0 for every satisfiable x.
  - The weight Λ_a(z) = Π(1 + (a_i + 1) z_i) = Π a_i^{z_i} then satisfies Σ_z R Λ_a ≠ 0 ⇔ ∃z. This is verified, holds unconditionally, and is nonuniform (the advice is a).
- **(b) Exact normalization with r copies.**
  - Set M = P_x(a). Then M^{2^r−1} = [M ≠ 0].
  - The Frobenius map is additive in characteristic 2, and R ∈ {0,1}, so M^{2^j} = Σ_z R Λ_a^{2^j}.
  - Hence E(x) = Σ_{z_0..z_{r−1}} Π_j R(x,z_j) Λ_a(z_j)^{2^j}.
  - Choose β with Tr(β) = 1. Then W(z⃗) = Tr(β Π_j Λ_a(z_j)^{2^j}) gives E(x) = Σ_{z⃗} W(z⃗) Π_j R(x,z_j) over F2. Tr is F2-linear and E(x) ∈ F2.
  - W has poly-size Boolean circuits, with coefficients counted: F_{2^r} arithmetic, Frobenius is linear, Tr is linear.
  - This yields NP ⊆ ⊕P/poly (known result; the construction is a Schwartz–Zippel isolation variant, and no novelty is claimed). The number of copies is r = O(n + log m).
- **(c) Consequence for §3.**
  - The joint weight size is complexity-blind on the original space over K and on the extended space over F2.
  - Only exactly normalized F2 weights on the original witness space remain open.
  - With x-dependence, Λ(x,z) = Tr(β·P_x(a)^{-1}·Π a_i^{z_i}) is exact. It needs P_x(a), however, and that is an exponential sum in K. The open part is therefore the elimination cost, not the weight.
  - Under P = NP, E ∈ P, so this particular ⊕P/poly expression collapses. That contradicts nothing known, since ⊕P ⊄ P/poly is unproved (T50 B2).
