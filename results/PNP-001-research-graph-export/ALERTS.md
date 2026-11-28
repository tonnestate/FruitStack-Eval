# Research director alerts (newest last; generated, append-only source: desk/alerts.jsonl)

## 2026-11-28T14:24:36+0100  SESSION_FAILURES  `SESSION_FAILURES:REVIEW-2026112813`
- finding: lane REVIEW: 18 sessions in 6 h, 0 with FINAL
- significance: workers cannot close their work inside the turn limit
- affected: REVIEW
- proofbook ids: []
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: countdown nudge + continuation rule active; repeated heads are demoted by the lane sorter

## 2026-11-28T14:24:36+0100  STAGNATION  `STAGNATION:REVIEW-2026112813`
- finding: lane REVIEW: no proof step, verification, refutation or connection in 18 sessions (6 h)
- significance: lane output is approach descriptions / numerical records only
- affected: REVIEW
- proofbook ids: []
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: REVIEW share rebalanced; the lane's repeated heads are demoted

## 2026-11-28T14:24:36+0100  STAGNATION  `STAGNATION:COMPRESS-2026112813`
- finding: lane COMPRESS: no proof step, verification, refutation or connection in 18 sessions (6 h)
- significance: lane output is approach descriptions / numerical records only
- affected: COMPRESS
- proofbook ids: []
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: REVIEW share rebalanced; the lane's repeated heads are demoted

## 2026-11-28T14:24:36+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:46`
- finding: REFUTATION recorded: For any satisfiable CNF formula $F$, the number of satisfying assignments $\#F$ is always divisible by 2 if and only if all satisfying assignments are monochromatic (i.e., all zeros or all ones).
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [46]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:36+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:91`
- finding: REFUTATION recorded: The SOSA 2026 paired reduction exposes a sign-free survivor core (non-rogue models all carry sign +1 and biject with SAT), so an involution-based cancellation operation decides SAT without the signed difference
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [91]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:36+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:103`
- finding: REFUTATION recorded: The SOSA-independent claim 'zero-free interpolation faces an intrinsic padding obstruction: no class closed under fresh-clause padding has a uniform-width zero-free neighbourhood of [0,1] for P=Z_F+c' (T6 Z2 conclusion). 
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [103]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:36+0100  VERIFIED  `VERIFIED:120`
- finding: independent verification recorded: The 1/(4e) factor in Sheshadri's smooth-hypersurface bound comes from bounding the polar-intersection count d(d-1)^{N-2} ABOVE by a Bezout count on an enlarged space recording the matrix's corank-one kernel vectors; that count is a single b
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [120]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:36+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:139`
- finding: REFUTATION recorded: My earlier claim (ledger, same session): 'M_n <= n^2 - ceil(3n/2)' via 'c <= floor(n/2)' (each singular block has size >=2).
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [139]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:36+0100  VERIFIED  `VERIFIED:144`
- finding: independent verification recorded: The block-diagonal Hessian rank formula rank Hess(perm_n)(diag(B,C)) = 2kl+2 (perm(B)=perm(C)=0, full-rank gradients, k+l=n) is PROVEN with structural derivation; and M_4=10 is exhaustively confirmed.
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [144]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:36+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:146`
- finding: REFUTATION recorded: Auxiliary claim (intermediate, NOT in Satz T9-B's recorded proof): 'for a rectangular c=2 structure (1,3)+(3,1) the Hessian of perm_4 vanishes'.
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [146]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:36+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:151`
- finding: REFUTATION recorded: Proposed rank-2 construction u1=(1,-1,1,-1,0),u2=(1,1,1,1,1),v1=(1,i,-1,-i,0),v2=(1,1,1,1,0), X=u1 v1^T+u2 v2^T, claimed to be a singular point of perm_5 lying on an 11-dim component.
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [151]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:152`
- finding: independent verification recorded: PhysalisMe integration limitation diagnosed and fixed by correct API usage (no code change). Heavy symbolic computations failed with ok:False/SANDBOX_ENDED_WITHOUT_RESULT because physalis_code_run defaults to timeout_s=120, threads=1 (syste
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [152]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:157`
- finding: independent verification recorded: Satz T9-B (M_4=10) independently re-verified; its Case B proof (c<=2 for no-zero-row/col singular points) was INCOMPLETE and is now fixed with a clean uncancellable-single-term argument covering non-square c=3 structures.
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [157]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:158`
- finding: independent verification recorded: Non-equidimensionality theorem for Sigma(perm_5) (components of dim 11 and 15) is now verified THREE independent ways.
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [158]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:164`
- finding: independent verification recorded: Non-equidimensionality of Sigma(perm_5) and its component counts are FULLY verified (now four independent exact checks). Final counts: exactly 100 dim-11 block components V_{2,3} (C(5,2)^2, S_5xS_5 transitive => all distinct), 20 two-zero-r
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [164]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:173`
- finding: REFUTATION recorded: CORRECTION to T11-B (supersedes the 'p_{lambda,m,d} > g(lambda,(d^n),(d^n))' framing in entry 172). Comparing plethysm a_lambda vs Kronecker k_n(lambda) compares TWO UPPER BOUNDS and is NOT a certified obstruction. Verified direction (stand
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [173]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:180`
- finding: REFUTATION recorded: T11-D: REFUTATION of an unverified padded-permanent multiplicity table (gpt-oss-120b, NOT_VERIFIED) AND a course-correction on obstruction-hunting. (a) The model claimed a_{(5,1)}=1 for the padded perm_2 at (m,n,d)=(2,3,2). CONTAINMENT ARGU
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [180]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:182`
- finding: REFUTATION recorded: T11-F: CORRECTS T11-E and RESOLVES d=2. T11-E's candidate filter {g=0 & lambda_1>=(n-m)d} missed the necessary AMBIENT condition a_lambda <= p_lambda = mult of S_lambda in Sym^d(Sym^n W) (the coordinate ring sits in Sym^d(Sym^n W*)). For d=
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [182]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:183`
- finding: REFUTATION recorded: T11-G: RIGOR CORRECTION to T11-F's overclaim 'no occurrence obstruction at d=2'. An occurrence obstruction requires delta_lambda=0 (det closure mult) AND a_lambda>0. I only established g(lambda,(d^n),(d^n))>0 on all ambient-occurring lambda
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [183]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:187`
- finding: independent verification recorded: T11-K: CherryMe/owner-driven scope narrowing + negative control for T11-J. (1) SCOPE: the certified claim is narrowed to 'NO multiplicity obstruction among the FIVE p_lambda=2 partitions (12,4),(10,6),(10,4,2),(8,6,2),(8,4,4) at degree d=4;
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [187]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:190`
- finding: REFUTATION recorded: T11-M: BUG CONFIRMED (owner's Veronese diagnosis was correct) and FIXED; results SURVIVE. The negative control reported rank 1 at l^4 for lambda!=(16); the owner correctly proved it MUST be 0 (orbit closure of l^4 is the Veronese cone, C[co
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [190]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:191`
- finding: independent verification recorded: T11-N: reference test passed, bug precisely located (Test 3), ALL results RE-CERTIFIED with the corrected engine. REFERENCE TEST (binary quartic, weight (6,2), owner-specified): RAW convention Q=8AC-3B^2 with R_raw=4A d_B+3B d_C+2C d_D+D d_
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [191]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:192`
- finding: independent verification recorded: T11-O: engine-output diagnostic matched to the owner's reference fingerprint; CERTIFICATION_BLOCKED criteria MET; T11-I/J/L released. (1) ACTUAL engine HWV for weight (6,2) printed = c_31^2 - c_40*c_22 = -(a0a2-a1^2): the NORMALIZED covaria
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [192]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:193`
- finding: independent verification recorded: T11-P: T11-L lifted CONDITIONALLY_VERIFIED -> VERIFIED. Independent minor certificates produced from the CORRECTED (binomial-normalized) engine for all five p=2 partitions (12,4),(10,6),(10,4,2),(8,6,2),(8,4,4) at (3,4,4). Each certificate:
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [193]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:195`
- finding: independent verification recorded: T11-P NOTATION FIX (certificates valid): the engine evaluated the padded permanent as l*perm_3 = DEGREE 4 (verified: deg(l)=1, deg(perm_3)=3, product degree 4, matching det_4 degree 4). The ledger text 'x_11^4 perm_3' / 'z^4 perm_3' (degree
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [195]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:197`
- finding: REFUTATION recorded: T13 CORRECTED (owner). FOUR corrections adopted: (1) A separating HWV equation (P in I(D_n), P not in I(Y_{m,n})) proves non-inclusion but does NOT imply gamma_lambda>delta_lambda; geometric separation is MORE GENERAL than the multiplicity 
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [197]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:200`
- finding: REFUTATION recorded: WR correction (owner): the earlier 'border Waring rank of perm/det = Theta(4^n/n)' is too strong. PROVEN is only the LOWER bound underline-WR(f) >= C(n,floor(n/2))^2 = Theta(4^n/n), i.e. underline-WR = Omega(4^n/n) (exponential). Theta woul
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [200]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:201`
- finding: REFUTATION recorded: Task split + ell=5 scope correction (owner). TWO distinct questions must NOT be conflated: (A) FIRST_NONZERO_IDEAL_DEGREE d_min(4) = first d with I(D_4)_d != 0; (B) FIRST_SEPARATING_EQUATION = first HWV in I(D_4) not in I(Y_{3,4}) (ker E_D 
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [201]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:207`
- finding: REFUTATION recorded: REJECTED: the proposed extension of the null-cone lemma to NON-rectangular partitions, and the claimed d_min^sep(3,4) >= 9. MATH ERROR: for a non-rectangular lambda with ell=k, the HWV transforms as P_lambda(g(t).f) = t^w P_lambda(f) with w
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [207]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:212`
- finding: REFUTATION recorded: Padding-floor EQUIVALENCE REFUTED (certified counterexample, independently verified); proven (<=) direction retained; replaced by a TWO-CONDITION necessary filter. COUNTEREXAMPLE (owner): (m,n,d)=(2,3,6), lambda=(8,2,2,2,2,2)|-18 has p_lamb
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [212]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:213`
- finding: independent verification recorded: Two owner corrections adopted + T11-P tool-boundary. (1) TAUTOLOGY dropped: 'det full multiplicity below d_first(n)' is vacuous (d_first is by definition the first degree with I!=0); not a theorem, does not resolve d=6. We need an INDEPENDE
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [213]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:214`
- finding: independent verification recorded: delta_lambda(D_4) = 1 = p_lambda for lambda=(6,6,6,4,2), degree 6 (multiplicity of S_lambda(V*) in the degree-6 functions on the orbit closure of det_4). The same highest weight function is nonzero on l*perm_3, so gamma_lambda(Y_{3,4}) = 1:
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [214]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:216`
- finding: independent verification recorded: delta_lambda(D_4) = 1 = p_lambda and gamma_lambda(Y_{3,4}) = 1 for lambda=(6,6,4,4,4), degree 6 (function convention). Together with entry 214: both five-row degree-6 candidates with lambda_1 = 6 are closed; neither gives an equation of D_4
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [216]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:217`
- finding: independent verification recorded: Audit of Prop 7.3 of the OpenAI cubic border-dc preprint (2026-09-24): no error found. Scope: Sec. 3 (Prop 3.1, permanent projection of the coefficient polynomial G_D) verified by exact computation; Sec. 4 (Lemmas 4.1, 4.2, Prop 4.3) read b
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [217]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:443`
- finding: REFUTATION recorded: procedure alg-1dacc3e542ee (Utilize the property that if a 1-SAT assignment exists, the structure of the propagation graph, specifically the strongly connected components (SCCs) ) is sound
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [443]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:446`
- finding: REFUTATION recorded: procedure alg-b0e4c5fd9aac (The placeholder logic must be replaced with a concrete, executable check based on the required inputs (n, clauses) and the assumptions of the underlyi) is sound
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [446]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:451`
- finding: REFUTATION recorded: procedure alg-ca4f12006c0e (The exact-1 constraint structure can be related to properties of graph homomorphism or exact cover, but for polynomial time, we leverage the existence) is sound
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [451]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:452`
- finding: REFUTATION recorded: procedure alg-cf4ba2054ce6 (Consider the problem through the lens of graph theory, where each variable represents a vertex and each clause forms a hyperedge connecting three vert) is sound
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [452]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:453`
- finding: REFUTATION recorded: procedure alg-381c8d76daac (The new step involves checking for a specific structural property in the graph formed by the clauses. Specifically, we will analyze the bipartite grap) is sound
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [453]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:456`
- finding: REFUTATION recorded: procedure alg-f496d8017c75 (cons2 and cons3 and rank_GF3(matrix_B) = m => SAT; author nemotron-3.5-bolt) is sound
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [456]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:630`
- finding: RETRACTION recorded: 94da0f52b66c36da
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 94da0f52b66c36da
- proofbook ids: [630]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:631`
- finding: RETRACTION recorded: 818b51f9821dd515
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 818b51f9821dd515
- proofbook ids: [631]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:632`
- finding: RETRACTION recorded: Q-6ff572a072
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: Q-6ff572a072
- proofbook ids: [632]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:639`
- finding: RETRACTION recorded: RC-44a8185b-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-44a8185b-R
- proofbook ids: [639]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:640`
- finding: RETRACTION recorded: RC-ac317744-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-ac317744-R
- proofbook ids: [640]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:641`
- finding: RETRACTION recorded: RC-85edfc60-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-85edfc60-R
- proofbook ids: [641]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:642`
- finding: RETRACTION recorded: RC-501997d0-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-501997d0-R
- proofbook ids: [642]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:643`
- finding: RETRACTION recorded: RC-49cdc738-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-49cdc738-R
- proofbook ids: [643]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:644`
- finding: RETRACTION recorded: RC-86dc4a0a-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-86dc4a0a-R
- proofbook ids: [644]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:668`
- finding: RETRACTION recorded: RC-f3adcda9-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-f3adcda9-R
- proofbook ids: [668]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:689`
- finding: RETRACTION recorded: RC-2c3f6465-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-2c3f6465-R
- proofbook ids: [689]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:706`
- finding: RETRACTION recorded: RC-d9508540-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-d9508540-R
- proofbook ids: [706]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:724`
- finding: RETRACTION recorded: RC-ba15e262-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-ba15e262-R
- proofbook ids: [724]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:753`
- finding: RETRACTION recorded: RC-a88b9258-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-a88b9258-R
- proofbook ids: [753]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:782`
- finding: independent verification recorded: Independent recheck of RC-6d52805a-R: GF(2)/GF(3) rank profile of A and [A|1] (with n, m) does not determine the positive-1in3 count C mod 2. Method limit, expected (parity of #1in3 presumably parity-P-hard), not novel.
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [782]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:803`
- finding: RETRACTION recorded: RC-e7bd282a-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-e7bd282a-R
- proofbook ids: [803]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:838`
- finding: RETRACTION recorded: RC-ed9e6721-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-ed9e6721-R
- proofbook ids: [838]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:873`
- finding: RETRACTION recorded: RC-e9b1ffac-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-e9b1ffac-R
- proofbook ids: [873]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:882`
- finding: RETRACTION recorded: RC-c0f92a0e-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-c0f92a0e-R
- proofbook ids: [882]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:899`
- finding: RETRACTION recorded: RC-00c50b02-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-00c50b02-R
- proofbook ids: [899]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:934`
- finding: independent verification recorded: On the Gal domains maxterms x minterms (1in3 n=5, n=6; xor3 n=5) no maxterm is contained in any minterm (maxterms are larger: 6 vs 4-5; 9-12 vs 4-6; 10 vs 2-6), so every containment-incidence matrix is identically zero. RC-fbc21332 (rank 0 
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [934]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:947`
- finding: REFUTATION recorded: Non-port (P4 minor) does not indicate hardness: 2-SAT (in P) has a P4 minor at n=3, hence is not a matroid port for all n>=3; so no implication non-port => super-linear circuit size exists. D-013 remains a theorem about ideal secret sharing
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: matroid-port route (D-011..D-013 as hardness evidence)
- proofbook ids: [947]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:950`
- finding: RETRACTION recorded: Q-9dc24f771d
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: Q-9dc24f771d
- proofbook ids: [950]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:972`
- finding: RETRACTION recorded: RC-45241185-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-45241185-R
- proofbook ids: [972]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:984`
- finding: independent verification recorded: Full-support sign matrices with every clause block of rank <= 1 are exactly the globally rank-1 sign matrices on the n=5 and n=6 Gal domains (solution dimension |U|+|V|-1: 101 and 3517), so their Gal ratio is 1; D-014 direction 1 is impossi
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [984]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:998`
- finding: RETRACTION recorded: RC-11d478b2-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-11d478b2-R
- proofbook ids: [998]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:1029`
- finding: RETRACTION recorded: RC-cb40af87-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-cb40af87-R
- proofbook ids: [1029]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:1069`
- finding: RETRACTION recorded: RC-86f4c1a0-R
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-86f4c1a0-R
- proofbook ids: [1069]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:1143`
- finding: REFUTATION recorded: False from n=7: S = {036, 045, 026, 124, 456, 235, 016} is Boolean-UNSAT, solvable mod 3 (3 solutions), not solvable mod 9; Smith invariants A: (...,9), [A|1]: (...,3). Random UNSAT GF(3)-consistent sets: 6/300 (n=7), 9/300 (n=8), 11/300 (n
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: D-023 conjecture: A x = 1 integer-solvable iff GF(3)-consistent
- proofbook ids: [1143]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:1153`
- finding: REFUTATION recorded: False at n=6: the 180 minimal GF(3) gap cores with degree sequence (2,2,2,3,3,3) are Z-blind (all 900 cores are integer-solvable, D-023) and have no variable of degree 1. Representative {012, 013, 045, 145, 234}: degrees v0..v5 = 3,3,2,2,3,
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: RC-6d00680b hypothesis: every Z-lattice-blind UNSAT formula contains a pendant variable
- proofbook ids: [1153]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:1432`
- finding: RETRACTION recorded: a35d97b4eb58248b
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: a35d97b4eb58248b
- proofbook ids: [1432]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:1617`
- finding: RETRACTION recorded: cf1f751fb58d8219
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: cf1f751fb58d8219
- proofbook ids: [1617]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:1764`
- finding: RETRACTION recorded: 417f3f1ac4a2cb6a
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 417f3f1ac4a2cb6a
- proofbook ids: [1764]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:1809`
- finding: RETRACTION recorded: a682c61d53b2b5ea
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: a682c61d53b2b5ea
- proofbook ids: [1809]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:2021`
- finding: RETRACTION recorded: 9326e718fda98e6e
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 9326e718fda98e6e
- proofbook ids: [2021]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:2125`
- finding: RETRACTION recorded: 28030d3ea1b44f7d
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 28030d3ea1b44f7d
- proofbook ids: [2125]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:2146`
- finding: RETRACTION recorded: dbcc3d5e71bcd2b4
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: dbcc3d5e71bcd2b4
- proofbook ids: [2146]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:2240`
- finding: RETRACTION recorded: 9ac684d4dc9ebdcd
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 9ac684d4dc9ebdcd
- proofbook ids: [2240]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:2241`
- finding: RETRACTION recorded: 416a330e2f2c2b1a
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 416a330e2f2c2b1a
- proofbook ids: [2241]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:2654`
- finding: RETRACTION recorded: c8ded6523c0e062f
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: c8ded6523c0e062f
- proofbook ids: [2654]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:2655`
- finding: RETRACTION recorded: 2953cb31a0cbe0f8
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 2953cb31a0cbe0f8
- proofbook ids: [2655]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:2819`
- finding: independent verification recorded: Every positive 1-in-3-SAT formula (each clause a set of exactly three distinct variables) has a solution of its linear system A x = 1 over GF(2), where A is the clause-variable incidence matrix.
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [2819]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:2830`
- finding: RETRACTION recorded: 0dbe240df86d1d00
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 0dbe240df86d1d00
- proofbook ids: [2830]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:2857`
- finding: independent verification recorded: For positive 1-in-3 formulas over n variables with cons3=1 (A x = 1 solvable mod 3) and GF(3) nullity null3=1, sat=1 if and only if the normalised solution x0 (free variable set to 0) takes at most two distinct values.
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [2857]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:2902`
- finding: independent verification recorded: For every positive 1-in-3 formula F in the 3324-row table agent_agent_bitcost_onein3_intermediate_v1_2d2d725b (n=5 exhaustive, 1024 formulas; n=6 and n=7 sampled as generated by the code), the closed-form count C(F) = sum over x in {0,1}^n 
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [2902]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:2962`
- finding: independent verification recorded: For every finite loopless cubic multigraph G, let Phi(G) be the positive 1-in-3 formula with one variable per edge of G and one clause per vertex listing its three incident edge variables. Then every variable of Phi(G) occurs in exactly 2 c
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [2962]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:2990`
- finding: independent verification recorded: Positive 1-in-3-SAT: a formula phi is a list of m clauses, each a set of 3 distinct variables out of n; C(phi) = number of x in {0,1}^n with exactly one true variable in every clause; A = m x n clause-variable incidence matrix. (T44 Lemma C
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [2990]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:3068`
- finding: independent verification recorded: (T42 Theorem J) Subset sum: weights w in N^n, target t with 0 <= t <= sum w, M a positive integer. If M > max(t, sum w - t), then (exists s in {0,1}^n with w.s = t mod M) iff (exists s in {0,1}^n with w.s = t).
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [3068]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:3087`
- finding: RETRACTION recorded: b2fc5f9b11cdbc3f
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: b2fc5f9b11cdbc3f
- proofbook ids: [3087]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:3101`
- finding: independent verification recorded: (T45 section 2) For every Boolean function f of N variables and every k: log2 D_k(f) - 1 <= N - 1, where D_k(f) is the number of distinct subfunctions obtained by setting exactly k variables to 1; consequently the bound S(f) >= log2 D_k(f) 
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [3101]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:3169`
- finding: independent verification recorded: For every positive 1-in-3 instance: a family of 3-element clauses C_1..C_m over variables {1..n}. There exists v in GF(3)^n taking at most two distinct values with sum_{j in C_i} v_j = 1 (mod 3) for all i if and only if there exists u in {0
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [3169]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:3182`
- finding: independent verification recorded: For every positive 1-in-3 formula F (clauses = 3-subsets of variables, a 0/1 vector x satisfies F iff each clause has exactly one true variable), and the GF(3) system Ax = 1 (mod 3) with A the clause incidence matrix: x in {0,1}^n satisfies
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [3182]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:3218`
- finding: independent verification recorded: For every finite positive 1-in-3 CNF F over variables 0..n-1 (each clause a 3-subset of the variables): if some x in {0,1}^n makes every clause contain exactly one true variable, then the GF(3) linear system A x = 1 is consistent, where A i
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [3218]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:3259`
- finding: independent verification recorded: For every positive 1-in-3 formula F with clause-variable incidence matrix A over the integers, if F is satisfiable then the linear system A x = 1 has a solution over GF(3).
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [3259]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:3290`
- finding: independent verification recorded: For every positive 1-in-3 CNF formula F with at least one clause over variables x_0..x_{n-1} (each clause a 3-element set of variables), let A be the clause-variable incidence matrix over GF(3). Then F is satisfiable (some 0/1 vector has ex
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [3290]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:3313`
- finding: independent verification recorded: For every n >= 3 and every nonempty set F of distinct weight-3 clauses over variables 0..n-1: there is a GF(3) vector x with x_a+x_b+x_c = 1 (mod 3) for every clause {a,b,c} in F, taking exactly two distinct values, if and only if F has a 0
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [3313]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:3315`
- finding: independent verification recorded: For every positive 1-in-3-SAT formula F (every clause is a 3-set of variables, exactly one of which must be true), if F is satisfiable then the all-ones vector lies in the column space of the clause-variable incidence matrix A over GF(3) (i
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [3315]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:3331`
- finding: independent verification recorded: For every positive 1-in-3 formula F with incidence matrix A (rows = clauses, columns = variables, entries 0/1): if F is satisfiable then the system A x = 1 is solvable over GF(3). Equivalently cons3=0 implies sat=0.
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [3331]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:3355`
- finding: independent verification recorded: For every positive 1-in-3 formula F with n variables and at least one clause (each clause a 3-subset of {0..n-1}), with A the clause incidence matrix over GF(3) and b = all-ones: F is 1-in-3 satisfiable iff the affine system A x = b over GF
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [3355]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:3374`
- finding: independent verification recorded: For every positive 1-in-3 formula F (each clause a 3-element set of variables; F is satisfiable if some 0/1 assignment has exactly one 1 in every clause): if F is satisfiable, then the GF(3) linear system with equation x_a + x_b + x_c = 1 f
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [3374]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:3392`
- finding: independent verification recorded: For every finite list of clauses over variables 0..n-1 in which each clause is a 3-element set of distinct variables, the rank over GF(3) of the clause-variable incidence matrix is at most n-1.
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [3392]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:3420`
- finding: RETRACTION recorded: b3a08b924485ebd1
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: b3a08b924485ebd1
- proofbook ids: [3420]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:3421`
- finding: RETRACTION recorded: abc4e39b6f37b81c
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: abc4e39b6f37b81c
- proofbook ids: [3421]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:3721`
- finding: RETRACTION recorded: 83597917c305c689
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 83597917c305c689
- proofbook ids: [3721]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:3722`
- finding: RETRACTION recorded: 03c5724f15db5f89
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 03c5724f15db5f89
- proofbook ids: [3722]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:3723`
- finding: RETRACTION recorded: 4cd59a0b84db64bc
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 4cd59a0b84db64bc
- proofbook ids: [3723]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:3811`
- finding: RETRACTION recorded: 776aeb8beff1837d
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 776aeb8beff1837d
- proofbook ids: [3811]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:4475`
- finding: independent verification recorded: For every positive 1-in-3 CNF formula F (each clause is a set of three variables and requires exactly one true variable), with clause-variable incidence matrix A over the integers (rows = clauses, columns = variables, 0/1 entries): if F is 
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [4475]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:4580`
- finding: independent verification recorded: For every positive 1-in-3 clause set F over variables 0..n-1 whose GF(3) system x_a+x_b+x_c=1 (one equation per clause, variables 0..n-1) is consistent with solution set S, F has a 0/1 solution if and only if the union over coordinates i of
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [4580]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:4869`
- finding: RETRACTION recorded: HYPOTHESIS seq 4825 (R0400) rests on non-existent evidence: the cited dataset has columns n,m,first,subsets,cons,sat,gap,sat_nocons (no gf3_nullstellensatz_* columns), claim record S-687404df64 does not exist, the cited Q-636d6face2/Q-53a5d
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: dfd43c1af8e9f0fc
- proofbook ids: [4869]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:4872`
- finding: independent verification recorded: Update of the director Lean check: formal/acc0l3/ACC0L3.lean sha256 1f00ba8be8e191af... now also proves or2_in_D, or1_in_C0 (claim:03fced129264 both directions) and affine_bool_classified (claim:1a3685a2808b complete); axioms standard only.
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [4872]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:4873`
- finding: RETRACTION recorded: NUMERICAL_EVIDENCE seq 4857 (R0403): the cited run cm-bcb0d052c0b64df4 returned no result and printed only "Construction search required" - it does not contain the claimed representation. The claimed formula exists y: sum x_i - y = 1 (mod 3
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: b64e5be6d03304a9
- proofbook ids: [4873]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:4874`
- finding: RETRACTION recorded: HYPOTHESIS seq 4858 (R0403) rests on seq 4857 (OR_n in C0-exists with m = 1), which is retracted; the question of the minimal m(n) remains open (R0404 reports m = n-1).
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 4c82e714d7b08dd1
- proofbook ids: [4874]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:4901`
- finding: independent verification recorded: THEOREM MG-3 (owner proof 2026-11-18, T41 §14e; independently reviewed 2026-11-20, §14g): in the bipartite holographic setting Holant(EXACT1_3 | EQ_d) with one basis T in GL2(C) on every clause node and (T^-1)^T on every variable node, no T
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [4901]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:4931`
- finding: independent verification recorded: A Boolean function g on {0,1}^a whose values agree with c + sum a_i u_i (mod 3) for all u in {0,1}^a is constant or a literal (u_i or 1-u_i).
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [4931]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:5043`
- finding: RETRACTION recorded: Rung-4 question sharpened: see the new PRIORITY question 'RUNG 4 SHARPENED'.
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 32a09207922ac158
- proofbook ids: [5043]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:5046`
- finding: RETRACTION recorded: Rung-4 question superseded after reading TR26-070: see 'RUNG 4 - DEGREE LIFTING'.
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 71905511359d9251
- proofbook ids: [5046]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:5053`
- finding: independent verification recorded: INDEPENDENT REVIEW of the rung-4 transfer (2026-11-20, report section 11): Lemma T CORRECT (supports inside Pitassi-Robere canonical rectangles; renaming via representative rows), Theorem 4.1 CORRECT for constant k, Lemma N CORRECT with the
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [5053]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:5122`
- finding: RETRACTION recorded: Superseded by 'RUNG 4 - THREE PROOF OBLIGATIONS' (degree lifting done: report sections 11-12).
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 5a3b056291d64cfc
- proofbook ids: [5122]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:5128`
- finding: independent verification recorded: THEOREM 12 (rung 4 complete, report section 12; independently validated 2026-11-20): for the explicit doubly lifted family Psi_n (Lauria-Nordstrom graphs -> 3-CNF F(G) -> gadget lift with h_{2^p-1}, p constant with 2^p - 1 > 2^{1/eps} -> or
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [5128]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:5155`
- finding: RETRACTION recorded: Rung 4b is now task R4b of the INVARIANCE MATRIX question.
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: dd7fafce3b1a4b10
- proofbook ids: [5155]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:5160`
- finding: RETRACTION recorded: Superseded by the binding six-field invariance matrix (spec section 'INVARIANCE MATRIX - binding research instrument').
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 935fc9e855236049
- proofbook ids: [5160]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:5169`
- finding: independent verification recorded: THEOREM 14 (invariance cell M9, partial; report section 14; independently reviewed 2026-11-20, 'proved as stated'): for the family Psi_n of Theorem 12, every field and every variable order, every FULL roABP-IPS refutation (axiom placeholder
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [5169]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:5174`
- finding: independent verification recorded: LEMMA 15 (M9-S, owner proposal; report section 15; independently reviewed 2026-11-20, proved as stated over every field): a full IPS refutation C(x,z) of an unsatisfiable CNF (axioms = products of univariates, Boolean axioms univariate) com
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [5174]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:5192`
- finding: independent verification recorded: THEOREM 16 (invariance cell M9b; report section 16; independently reviewed 2026-11-20): Lemma M9b' (external repair: rank of P_F = prod(1 - Q_D) across a cut >= 2^K for K variable-disjoint crossing clauses when a substitution with transcend
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [5192]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:5475`
- finding: independent verification recorded: For every n >= 1 and every positive 1-in-3 formula with exactly two clauses T1, T2 (each a 3-subset of {0..n-1}, not necessarily distinct), there is S subset of {0..n-1} with |S ∩ T1| = 1 and |S ∩ T2| = 1. Equivalently, every 2-clause posit
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [5475]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:5578`
- finding: independent verification recorded: For every n >= 5 and every choice of distinct vertices u, v, a, b, c in [n], the positive 1-in-3 clause set {uva, uvb, uvc, abc} has no 1-in-3 satisfying assignment.
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [5578]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:5764`
- finding: RETRACTION recorded: Q-2bdb903445
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: Q-2bdb903445
- proofbook ids: [5764]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:5784`
- finding: independent verification recorded: For every positive 1-in-3 formula F (each clause is a 3-set of variables; sat(F)=1 iff exactly one variable of each clause is 1) that is satisfiable, the affine system over GF(3) with x_a+x_b+x_c=1 for each clause is consistent. Equivalentl
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [5784]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:5825`
- finding: RETRACTION recorded: Q-ffc8267d4c
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: Q-ffc8267d4c
- proofbook ids: [5825]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:5828`
- finding: RETRACTION recorded: Q-9379f7ebef
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: Q-9379f7ebef
- proofbook ids: [5828]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:6193`
- finding: REFUTATION recorded: Conjecture: every minimally GF(3)-blind family of positive 1-in-3 clauses has cov = rank3 + 1. REFUTED: F = {012, 013, 045, 145, 236} on 7 variables is GF(3)-blind (no 0/1 assignment with exactly one 1 per clause; A x = 1 solvable over GF(3
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [6193]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:6656`
- finding: independent verification recorded: For all rationals beta, eta, c with 0 <= eta <= beta and 0 <= c < 1: (2+beta-eta)/(1+c) > 1. More generally, for rationals beta, eta and c >= 0: (2+beta-eta)/(1+c) > 1 if and only if c < 1+beta-eta.
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [6656]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:7022`
- finding: independent verification recorded: For every n >= 1, every integer weight vector w in Z^n with max_i |w_i| <= B, every integer threshold t, and every l in {0,...,n}: the set of functions y in {0,1}^(n-l) -> [w_rest.y >= t - w_pre.rho], indexed by rho in {0,1}^l, has at most 
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [7022]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:9047`
- finding: independent verification recorded: Let X and Z be finite sets, and let E = {E_1,...,E_k} (k >= 1) be relations E_i subset of X x Z with projection pi: X x Z -> X. Let H = pi(intersection of all E_i) be nonempty. Assume COND: if k >= 2 then for every j in {1,...,k}, pi(inters
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [9047]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  DISCOVERY  `DISCOVERY:9541`
- finding: Bingo TRANSFER None: 
- significance: new constructed object / cross-project transfer
- affected: None
- proofbook ids: [9541]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: COMPOSE lane extends it (EXTEND question) and verification follows; cross-project applications are to be checked

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:10735`
- finding: independent verification recorded: For the cyclic 1-in-3 CNF C_n with clauses {x_i, x_{i+1}, x_{i+2}} (indices mod n, n>=3), with exactly-one constraint per clause, C_n is satisfiable over {0,1} if and only if 3 divides n.
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [10735]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:11359`
- finding: REFUTATION recorded: Lemma D1 (one-step drop, bookkeeping, not progress): C fan-in-2 B_2 circuit of size s computing f; x_i has fan-out 1 into gate g = op(x_i, y), y != x_i; some b in {0,1} makes op(b, .) in {0, 1, y, not y}. Then f|x_i=b has a B_2 circuit of s
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [11359]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:13304`
- finding: independent verification recorded: statement: For fixed admissible s,A satisfying the stated infinitely-often disjunction, every M in M_{s,A}^{plain} and every fixed c,d has no m1 such that S_M(m)<=s(m)^c and tau_M(m)<=s(m)^d holds for all m>=m1. derivation: Assume such an m
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [13304]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:13488`
- finding: independent verification recorded: statement: Lemma (restriction-independent gates survive). Let C be a fan-in-2 Boolean circuit on variables X∪Y, and let g be a gate whose computed Boolean function depends only on Y. For every assignment a to X, the gate function after rest
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [13488]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:16755`
- finding: independent verification recorded: T07: every De Morgan circuit C of size S with r gates of fan-out > 1 has formula size L(C) <= 2^r (2S+1)
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [16755]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:16756`
- finding: independent verification recorded: CJW20-T5.5-GAP: Gap-MCSP[N^beta/(K m), N^beta] has no probabilistic De Morgan formula of size N^{2+beta-eps}
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [16756]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:16761`
- finding: REFUTATION recorded: MECHANISM: for every De Morgan circuit of size N^{1+eps}, the CJW20 pseudorandom restriction satisfies r(C|rho)+log2(2S(C|rho)+1) <= (3beta-eta)log2 N w.h.p.
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [16761]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:16839`
- finding: REFUTATION recorded: D6 (seq 16770) counting claim: 'reused gates with d_g <= N^{1-beta-eta} contribute <= N^{-2eta}, so only wide reused gates survive the restriction' - REFUTED. The per-gate bound Pr <= p^2 d_g^2/2 is right; the number of narrow reused gates 
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: seq 16770 D6
- proofbook ids: [16839]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:16877`
- finding: RETRACTION recorded: Q-4c4127e83e
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: Q-4c4127e83e
- proofbook ids: [16877]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:16927`
- finding: independent verification recorded: The rank of a submatrix is at most the rank of the matrix PREMISES:  PROOF: SOURCE: proofbook seq 57; mission pi-theory-T1-T2; author model claude-opus-5-5; claim hash d981059752cbd2cd; registered by pnp_autoreview
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [16927]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:16972`
- finding: independent verification recorded: The threshold function 'at most m of n variables are 0' depends only on the numbers of zeros on the two sides of a cut PREMISES:  PROOF: SOURCE: proofbook seq 67; mission pi-theory-T1-T2; author model claude-opus-5-5; claim hash 7be07cb8720
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [16972]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:17166`
- finding: RETRACTION recorded: seq 17145 superseded by T-NORM-F2: the p^2 L term was attributed to Tal's theorem but is AF's open P2; the test itself survives with the unconditional p L bound.
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 843688727ccea2e9
- proofbook ids: [17166]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:17199`
- finding: RETRACTION recorded: seq 17181 said gap/approximate merge gates escape CJW20; by CJW20-GAP the same lower bound holds for the gap and truncated promise problems. Replaced by MERGE-LB.
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: f92750a0b1d2da12
- proofbook ids: [17199]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:17201`
- finding: RETRACTION recorded: seq 17184's dilemma is wrong in its second horn: tau>1 does not lose the CJW20 contradiction (CJW20-GAP), and MECH-RANGE seq 17158 is not the best known Gap formula bound. Replaced by TRUNC2.
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 7425fe5fa69670ce
- proofbook ids: [17201]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:17203`
- finding: RETRACTION recorded: seq 17185 listed 'gap gates plus a Gap-MCSP formula lower bound (=QO2)' as a remaining form; that lower bound follows from the CJW20 proof (CJW20-GAP). Replaced by the next CONNECTION.
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: d08811bb17468824
- proofbook ids: [17203]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:17214`
- finding: RETRACTION recorded: seq 17208 used t*a^K as a QO1 circuit bound for the exact partial-consistency predicate H; QO1 (seq 16795, OPS mechanism) covers Gap-MCSP only, and its phrase 'which no conversion gives' overstated the e_new <= 1 case. Replaced by DECOUPLE-
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 253ed96083c3c7e0
- proofbook ids: [17214]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:17296`
- finding: RETRACTION recorded: seq 17290 point (4) misquoted the Anthropic runtime from a pdftotext extraction that dropped the square root and the square: the Main Theorem (paper.pdf p.2, eq. (1)) is 2^{O(min{k^2 n loglog n / sqrt(log n), k m / sqrt(log m)})}, so the ex
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: fc3481e9acfc9260
- proofbook ids: [17296]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:17335`
- finding: RETRACTION recorded: seq 17325 claimed m <= s/p distinct orders in general; false for jointly generated algebraic families (owner counterexample y(A_a z)). Replaced by the next row; all other content unchanged.
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 8ece38d81c0386b1
- proofbook ids: [17335]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:17404`
- finding: RETRACTION recorded: Retracts the CORRECTION (constant) paragraph of seq 17397: Dvorak-Norin (arXiv:1408.3869 v2, Sec. 1) use 2/3-balance on |A\B| and |B\A|, not 1/2; the director's '1/2' was from memory and wrong. Replacement row follows; all other parts of 17
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: 3a9069399d0a32c5
- proofbook ids: [17404]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:17813`
- finding: independent verification recorded: statement: Let Q be any set and let f,g:Q→Q be commuting maps, meaning f∘g=g∘f. For every q∈Q, the words 01 and 10 induce the same terminal state when symbol 0 applies f and symbol 1 applies g. proof: Reading 01 applies f then g, so its ter
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [17813]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:18279`
- finding: REFUTATION recorded: ERRATUM to Proofbook 17584 (construction text, not the representation theorem). The AND gadget as written there, EO(t,u,~a), EO(t,v,~b), EO(u,v,w) with fresh Boolean t,u,v,w, has a unique internal extension for every input (4/4) but compute
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [18279]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:18292`
- finding: REFUTATION recorded: T59 s7 R3 'no bound better than s*N'; T59 s10(1) 'affine selector => cost-free projection'; T59 s5 'equivalent forms MT/E.4/kappa~1'; T59 s10(4) 'single term'.
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [18292]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  VERIFIED  `VERIFIED:18297`
- finding: independent verification recorded: Source check (independent subagent read full PDFs): Hrubes TR15-067 Thm 1 (monotone 2-CNF, ML VNP-hard over any field, complete if char!=2), Cor 2 (VP!=VNP => some P-computable family has ML not in VP), Thm 7 (|F|>=3: products of width-2 af
- significance: a claim gained review status
- affected: see statement
- proofbook ids: [18297]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: dependent steps are re-evaluated by the graph sync's revalidation_impact on its next run

## 2026-11-28T14:24:37+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:18299`
- finding: REFUTATION recorded: Proposed coupling 'gate-ideal saturation / canonical selector structure forces small space for the selector' is refuted as a route.
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: see statement
- proofbook ids: [18299]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:37+0100  DISCOVERY  `DISCOVERY:18385`
- finding: Bingo TRANSFER None: 
- significance: new constructed object / cross-project transfer
- affected: None
- proofbook ids: [18385]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: COMPOSE lane extends it (EXTEND question) and verification follows; cross-project applications are to be checked

## 2026-11-28T14:24:37+0100  DISCOVERY  `DISCOVERY:18402`
- finding: Bingo COMPOSITION comp:koopman-lucas-period-duality: 
- significance: new constructed object / cross-project transfer
- affected: comp:koopman-lucas-period-duality
- proofbook ids: [18402]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: COMPOSE lane extends it (EXTEND question) and verification follows; cross-project applications are to be checked

## 2026-11-28T14:24:38+0100  DISCOVERY  `DISCOVERY:18445`
- finding: Bingo COMPOSITION comp:hadamard-rank-x-t52-signed-elimination-x-inclusion-exclusion: 
- significance: new constructed object / cross-project transfer
- affected: comp:hadamard-rank-x-t52-signed-elimination-x-inclusion-exclusion
- proofbook ids: [18445]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: COMPOSE lane extends it (EXTEND question) and verification follows; cross-project applications are to be checked

## 2026-11-28T14:24:38+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:18669`
- finding: RETRACTION recorded: Q-c2979e1c2b
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: Q-c2979e1c2b
- proofbook ids: [18669]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director

## 2026-11-28T14:24:38+0100  DISCOVERY  `DISCOVERY:18764`
- finding: Bingo COMPOSITION comp:koopman-hankel-bm-bostan-mori-cost-calculus: 
- significance: new constructed object / cross-project transfer
- affected: comp:koopman-hankel-bm-bostan-mori-cost-calculus
- proofbook ids: [18764]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: COMPOSE lane extends it (EXTEND question) and verification follows; cross-project applications are to be checked

## 2026-11-28T14:24:38+0100  DISCOVERY  `DISCOVERY:18765`
- finding: Bingo COMPOSITION comp:shear-decoupling-tower-x-hankel-rank-separation-x-t52-elimin: 
- significance: new constructed object / cross-project transfer
- affected: comp:shear-decoupling-tower-x-hankel-rank-separation-x-t52-elimin
- proofbook ids: [18765]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: COMPOSE lane extends it (EXTEND question) and verification follows; cross-project applications are to be checked

## 2026-11-28T14:24:38+0100  CONFIRMED_ERROR  `CONFIRMED_ERROR:18772`
- finding: RETRACTION recorded: Q-c7c02fd18c
- significance: a claim is withdrawn; dependents must be reconsidered
- affected: Q-c7c02fd18c
- proofbook ids: [18772]
- github: https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-research-graph-export-20261127/results/PNP-001-research-graph-export (commit 3838b25f4b, seq 18807)
- autonomous action: graph sync computes revalidation_impact; an AUDIT question for the largest dependent set is filed by this director
