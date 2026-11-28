# T55 — Autoencoder geometry of the solution bundle and the fibre-symmetry obstruction (owner's derivation; PI check, 2026-11-27)

Status: CLAIMED (Claude family only). Symbolic only.
Prerequisites: T49 Lemma 2 (Skolem form), T54 Thm 4.1 (E.4 fails for Boolean circuits at t-saturation), T53 E2.

Setting: Y = {(x,z) : R(x,z) = 1} → X = π(Y), with fibres Z_x of size N(x).
- (Af)(x,z) = f(x) is the encoder.
- (L_S g)(x) = g(x, S(x)) is the multiplicative decoder. By Gelfand/Stone duality these are exactly the algebra-homomorphism sections.

## 1. The owner's computations (verified)
- A^T A = diag(N(x)), so rank A = |X| and the singular values are sqrt(N(x)).
- ||L_S|| = 1 and L_S A = id.
- The projector A L_S has norm sqrt(max N).
- The Moore–Penrose decoder (A^T A)^{-1} A^T averages over each fibre, and A A^+ has norm 1.
- L_S = A^+ ⇔ N ≡ 1 on X (functional encodings).

All of this is elementary linear algebra on a finite bundle.

## 2. Fibre-symmetry obstruction (owner's §4, verified, sharpened)
Let G = Π_x Sym(Z_x) act on functions on Y. Every U ∈ G satisfies U A = A. For any two selectors S1, S2 there is a U ∈ G with
L_{S2} = L_{S1} U and A L_{S2} = U^{-1}(A L_{S1}) U.

**Corollary.** No G-invariant functional of (A, L_S) distinguishes selectors. This covers spectra, norms, ranks, and any basis-free invariant of the pair.
- For R ≡ 1 with m = 1, the selectors are all Boolean functions of x, including those of exponential circuit size (Shannon).
- Every geometric measure that can separate easy selectors from hard ones must therefore break G, i.e. it must use the coordinate (bit) structure of z and x.

## 3. Where coordinate-bound geometry lands
The coordinate structure is the tensor factorization F^{Y} ⊂ (F^2)^{⊗(n+m)}. Two kinds of tensor invariant are available.
- **Local-GL invariants** are coordinate-bound and not G-invariant. These are flattening ranks, Strassen spectral points, and the external "prices".
  - On the graph tensor Γ_S = Σ_x e_x ⊗ e_{S(x)}, easy selectors already reach maximal flattening rank. For example S(x) = x, or z = IP(x) across the cut x_1 | x_2.
  - So rank alone does not separate either.
  - The external mechanism therefore needs its circuit-side lemma: small circuit ⇒ small invariant (E.4/K.2).
- **The "missing theorem" of the owner's §5** says that polynomial computations restrict coordinate-bound geometric transformations. Instantiated with the only coordinate-bound geometry for which a circuit-side lemma is known, it is exactly E.4 for Boolean circuits.
  - That is the first failing implication of T54 Thm 4.1: gate values are not t-saturated, and block degree is up to 2^s.
  - Instantiated as "the cost of the fibre permutation U along gates", it is the circuit complexity of S2 relative to S1, i.e. a circuit lower bound for selectors (T49 §6).

**Result:** a precise obstruction. The G-invariant geometry of the exact autoencoder is complexity-blind. The coordinate-bound geometry reduces to E.4 for Boolean circuits, which is the first failing implication already identified in T54. No contradiction; P = NP enters only through the existence of a small S.
