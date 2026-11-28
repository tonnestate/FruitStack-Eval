# T11-A — the asymptotic orbit-closure multiplicity obligation (PI framing, 2026-11-17)

The real T11-B/T11-A obligation: certify a LOWER bound L <= gamma_lambda on the padded-permanent orbit closure Y_{m,n}, and an UPPER bound
delta_lambda <= U on the determinant closure D_n, with L > U, for n beyond EVERY fixed polynomial in m. Single-degree computation (T11-C..K)
cannot reach "all n=poly(m)"; T11-A is the structural question. This note records what the verified small-case data already tells us.

## Verified reframing from T11-J data (own validated engine)
The Kronecker coefficient g(lambda,(d^n),(d^n)) is a LOOSE upper bound on delta_lambda(det), and the gap below it is REAL and (so far)
SYMMETRIC between perm and det:
- At (m,n,d)=(3,4,4), p_lambda=2 for five lambda. The EXACT orbit-closure multiplicities (HWV evaluation rank, negative-control-validated):
  - (10,4,2): gamma(perm)=delta(det)=2, but g=4  -> both drop 2 below the Kronecker bound.
  - (8,6,2):  gamma=delta=2, g=4.
  - (8,4,4):  gamma=delta=2, g=5.
  - (12,4),(10,6): gamma=delta=2=g (bound tight here).
- So delta_lambda(det) < g can be strict (2 < 4, 2 < 5): the Kronecker UPPER bound is not the true determinant multiplicity. This is exactly
  why an obstruction CANNOT be certified by g alone (confirmed) AND why it is not excluded by g>0 (confirmed): one must compute the true
  delta_lambda. Where computed, perm matches det (gamma=delta), so no obstruction; the drop below g is symmetric.

## CORRECTION (2026-11-28): the "drop below the Kronecker bound" is a weak-ceiling artefact
**Recomputed ceiling (exact, 2026-11-28).** Both closures Y_{m,n}, D_n are subvarieties of Sym^n W, so ℂ[Y]_d, ℂ[D_n]_d are quotients of ℂ[Sym^n W]_d, and γ_λ, δ_λ ≤ A_λ := ⟨s_λ, h_d[h_n]⟩ (multiplicity of S_λ in Sym^d(Sym^n W^*), independent of dim W ≥ ℓ(λ)). Computed directly from the character of Sym^4(Sym^4 ℂ³)
by the Weyl alternation (3 variables suffice, ℓ(λ) ≤ 3): **A_λ = 2 for (10,4,2), (8,6,2), (8,4,4), (12,4), (10,6)**. Hence the available ceiling is min(A_λ, g_λ) = 2 in all five cases (g = 4, 4, 5, 2, 2): the three multiplicity-2 cases attain the full ambient multiplicity, there is
**no loss** for either perm or det, and the "symmetric loss of multiplicities" reading above (g−γ = 2, 2, 3) compared the exact value against a ceiling (g) that is not sharp. The exact evaluations γ = δ = 2 are unchanged. Consequence: the earlier remark "the drop below g is symmetric, so no obstruction" is replaced by "no drop below the ambient ceiling occurs in the computed cases, so these cases carry no information about asymmetry".
**[Definition question RESOLVED 2026-11-28]** the ledger's p_λ = 2 is the ambient plethysm A^amb = ⟨s_λ,h_4[h_4]⟩ (T11-J/L certificates record p = 2 and exact ranks 2 = A^amb for all five); my padded count 7,6,4,4,4 is a different, also correct quantity, A^par = ⟨s_λ,h_{d(n−m)}·h_d[h_m]⟩ (parametrization ℓ^{n−m}g). Both are upper bounds for γ_λ: γ_λ ≤ min(A^amb, A^par) = 2 for all five; δ_λ ≤ min(A^amb, g)= 2. All five exact values γ=δ=2 sit at the ceiling. Computed with the same engine (exact Fractions): T11P λ=(6,6,6,4,2) at (3,4,6): A^amb = A^par = 1 = γ = δ (at the ceiling again). T11-O counterexample (2,3,6), λ=(8,2,2,2,2,2): A^amb = 1, A^par = 2, γ = 0: both ceilings positive yet γ vanishes, so neither is sharp in general (essential-variable bound ℓ(λ) ≤ m²+1 is what kills it).
**Normalisation rule (all earlier multiplicity comparisons, T11-B…K, T11P):** express every deficit as (min(A_λ, g_λ, further available upper bound)) − exact value, recomputing A_λ = ⟨s_λ,h_d[h_n]⟩ (cheap via Weyl alternation for ℓ(λ) small); the stored exact values γ_λ, δ_λ stay as they are. Done for every λ and (m,n,d) with stored exact values (T11-J/L: 5 λ at (3,4,4); T11P: (6,6,6,4,2) at (3,4,6); T11-O counterexample): in all stored cases of positive γ the exact value equals the ambient ceiling, so the stored data contain NO deficit and no information on asymmetry; recomputation for further (m,n,d) is cheap with the same character engine (cost grows as the number of monomials of degree nd in ℓ(λ) variables).

## The precise structural question (T11-A)
A multiplicity obstruction needs the drop below the ambient/Kronecker ceiling to become ASYMMETRIC: a lambda-family where
delta_lambda(det) drops strictly BELOW gamma_lambda(perm) (perm retains multiplicity the determinant loses), persisting for n=poly(m).
Equivalent operational target: find an invariant/measure on C[Y_{m,n}] that (i) lower-bounds gamma_lambda without the open-orbit proxy
a_lambda, (ii) is NOT a tensor/Waring rank (excluded by EGOW/T10), (iii) separates the symmetric drop. The field has no such invariant;
occurrence is dead (BIP), and the plethysm-Kronecker route faces #P/NP-hard positivity (T11-A.2).

## Honest PI assessment
- What FruitStack has achieved: a validated exact engine that computes TRUE orbit-closure multiplicities gamma_lambda, delta_lambda
  (not just Kronecker/plethysm upper bounds) via HWV evaluation with negative-control-proven discriminating power. This is a genuine,
  reusable capability; most GCT small-case claims in the literature stop at the Kronecker/occurrence level.
- What remains out of reach: the ASYMPTOTIC statement (asymmetric drop for all n=poly(m)) is a structural proof, not a computation. No single
  computation settles it; and no known invariant delivers the required lower bound on gamma_lambda. This is precisely where GCT is stuck.
- Concrete empirical probe the engine CAN run (bounded value): compute gamma_lambda, delta_lambda exactly for a growing family (e.g. the
  p>=2 lambda at (3,5,.),(3,6,.)) and test whether the drop below g EVER becomes asymmetric. A single asymmetric instance would be a real
  obstruction candidate; continued symmetry is verified negative data. But this remains single-case probing, not the asymptotic proof.

## Recommendation (for the ultimate objective)
The GCT line has produced rigorous negative certificates + a validated multiplicity engine, but no obstruction and no path to the asymptotic
bound. Per the atlas (T0), the structural levers NOT blocked at a single open invariant are T13 (algebraic natural proofs = succinct hitting
sets: concretely, decide whether the HWV covariant equations we construct lie in VP) and the Boolean T12/T5. Continuing GCT single-case
probing yields expected negatives; the higher-value move is a structural lever. Decision deferred to owner per the ultimate-objective mandate.
