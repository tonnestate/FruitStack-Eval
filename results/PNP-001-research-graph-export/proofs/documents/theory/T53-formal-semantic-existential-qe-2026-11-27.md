# T53 — Formal vs. existential QE: VNP-completeness of formal functional QE, and what P = NP forces about existential projection (2026-11-27)

Status: CLAIMED (Claude family only).
- §1 is the owner's construction, checked by the PI.
- §2–§4 are by the PI.

Symbolic only. Prerequisites: T41 §6/§7, T48 §3 and 9.4, T49, T50 §4, T51 (C1, T-B), T52 (+§6), 17590.

## 1. Formal functional QE is VNP-complete (owner; checked step by step)
Setting:
- C(u) checks over u ∈ {0,1}^n (edges) whether u is a directed Hamiltonian cycle on h vertices. This check is in P.
- φ_C is its parsimonious 1-in-3 encoding (T41 §6), with the output forced to 1.

Construction:
- **Complement pairs.** Every internal variable y gets ȳ = 1 − y. Over F3, (y−2)(ȳ−2) = (y+1)(2−y) = −(y+1)².
  This is −1 at y = 0 and y = 1, and 0 at y = 2. ✓ All valid internal assignments therefore get the same sign.
- **Coupling.** E(x_i, x̄_i, 0), E(x_i, ū_i, a_i), E(x̄_i, u_i, b_i). Over F3 these give x̄_i = 1 − x_i, a_i = u_i − x_i, b_i = x_i − u_i. ✓
  - a_i and b_i are both Boolean ⇔ a_i ∈ {0,1} and −a_i ∈ {0,1} ⇔ u_i = x_i.
  - Hence the encoding stays functional with external inputs x.
  - (a_i−2)(b_i−2) = (1+u_i−x_i)(1+x_i−u_i) = 1 − (x_i−u_i)². ✓
  - The u_i are **free** in the affine system: only Booleanness forces u = x.
- **QE.** Sum over all free parameters: u ∈ F3^n, plus the parameters z' of φ_C.
  - For fixed u, the inner sum is G(u) = Σ_{z'} Π_y −(y+1)².
  - For Boolean u, parsimony gives G(u) = (−1)^{m'}·C(u).
  - For u_i = 2, the u-pair factor −(u_i+1)² is 0.

  So, formally in F3[X]:
  F_C(X) = ε·Π_i(−1−X_i)·Σ_{u: C(u)=1} Π_i (1 − (X_i−u_i)²), with constant ε = ±1. ✓
  The identity is formal, not merely on the Boolean domain: u is summed numerically, and X appears only in the x̄, a, b factors.
- **Extraction.**
  - 1 − (X−u)² is 1 − X² for u = 0 and −X − X² for u = 1.
  - Every summand therefore has minimal degree |u| = h, and its degree-h part is ±Π_{e∈H} X_e.
  - The factor Π(−1−X_i) contributes the constant (−1)^n at its lowest degree.
  - Hence the degree-h homogeneous component of F_C is ±HC_h. ✓
- **Equivalence (nonuniform, over F3).** "All formal QE polynomials of poly-size functional 1-in-3 encodings are in VP" ⇔ VP = VNP.
  - ⇒: Strassen homogenization, and HC is VNP-complete in every characteristic.
  - ⇐: F = Σ_{z∈F3^d} Π(affine) is in VNP. Each ternary parameter t is encoded by two Boolean variables (b1, b2): t = b1 + 2b2, with the
    factor (1 − b1b2) excluding the fourth state. ✓

Note: on Boolean X, Π(1 − (X_i−u_i)²) = [u = X]. So F_C|_{Boolean} = ±Π(−1−X_i)·C(X) is a poly-time function, while the formal F_C is VNP-hard.
This is the formal/Boolean gap of T48 §3, T49 L3, T50 B1 and T50 §4 (MT, Hrubeš), now located inside our own QE.

## 2. Three QE operations, separated exactly
For a relation R(x,z) given by a functional or general 1-in-3/F3 encoding:
- **Formal QE:** Φ(R) = Σ_{z∈F3^d} Q(X,z) ∈ F3[X]. It is linear in the values Q.
- **Semantic projection:** the set fibre {z : R(x,z)}, or its count #fib(x) ∈ ℕ.
- **Existential QE:** E(x) = ∨_z R(x,z) ∈ {0,1}.

Relations:
- **(i) Functional case.** On the Boolean domain, Φ(R) = ±E, so existential = formal mod the Boolean ideal. The whole VNP-hardness in §1 lies in
  the ideal component.
- **(ii) General case.** Φ(R)|_{Boolean} = ±#fib mod 3, which is counting (T51 T-A).
- **(iii) Proposition E1 (proved).** As a function of the 2^d values v_z = R(x,z), existential projection is OR_{2^d}. Over every field its unique
  multilinear representative is 1 − Π_z(1 − v_z), of degree 2^d. Every polynomial that agrees with it on {0,1}^{2^d} has degree ≥ 2^d.
  *Proof.* Multilinear reduction does not raise degree, and the representative is unique. ∎
  - Summation (counting) has degree 1 in the values; existence has degree 2^d.
  - With C1 (T51): ∨ is linear only in idempotent semirings, and there no polynomial computes NOT.

## 3. Owner's item 7: the external geometry directly on existential projection
- The external mechanisms work with **linear** contraction: sums over shared bits of products of field tables.
- Bit networks over the Boolean semiring with **arbitrary local tables** circumvent C1, because the negation sits inside the tables.
  Their contraction is exactly the existential projection of a CSP. Such networks are themselves the NP objects: every NP relation has a
  poly-size network of this kind, unconditionally.
- **Proposition E2.**
  - Under P = NP, for every NP set E, the graph of E has a poly-size **unambiguous** network: the circuit network of the selector S, with a unique
    internal assignment.
  - For unambiguous networks, the contraction over 𝔹 equals the contraction over ℕ, and hence over ℚ. So P = NP turns existential networks into
    **counting networks over a field**.
  - The external geometry is formulated for exactly that kind of object.
- **First failing step: the external theorems refute VP circuits, not small networks.**
  - Small field networks exist **unconditionally** for VNP-hard tensors. Example: the Cook–Levin tableau network for the coefficients c_x of f_n is
    the VNP upper bound in OpenAI §1.
  - The step from "small unambiguous network for E" to "small VP circuit for the generating polynomial of E" fails. Counterexample (T51 T-B): the
    PERM support is in P, but its generating polynomial is PERM.
  - So even after P = NP's bridge from existence to counting, the external mechanism refutes nothing.

## 4. Owner's item 8: what P = NP genuinely forces about existential projection (all checked)
- **(F1) Deterministic uniquification.** R'(x,z) := R(x,z) ∧ "no lexicographically smaller witness". R' is in P under P = NP, and
  ∨_z R = Σ_z R' over ℤ. Existential projection becomes linear after a poly-time refinement.
  Unconditionally this holds only randomized (Valiant–Vazirani).
- **(F2)** E ∈ P, and NP ⊆ SPP (trivially, since P ⊆ SPP).
- **(F3)** For every NP set E and every p, the generating polynomial G_E = Σ_{x∈E} Π(1−(X_i−x_i)²) is in VNP_p, via §1 applied to R'.
  Unconditionally, by Valiant's criterion (cited from memory, check before ledger use), this is equivalent to NP ⊆ Mod_pP/poly.
  NP ⊆ Mod_pP is unknown.
- **Contradiction test.**
  - F1–F3 are consequences of P = NP that go through NP predicates. They hold in the AW world (17590): relative to a PSPACE-complete oracle,
    all of these classes coincide. They are relativizing.
  - ¬F3 would be a VNP lower bound for a G_E (G_E ∉ VNP). No external or in-house theorem supplies that. The external theorems separate VP from
    VNP; they do not place anything outside VNP.
  - **No contradiction.**
- **First failing implication on this route:** "P = NP ⇒ a formal property outside VNP-type statements". Everything P = NP forces in the algebra
  of existential projection lies within VNP (F3), or is relativizing (F1, F2).
