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
