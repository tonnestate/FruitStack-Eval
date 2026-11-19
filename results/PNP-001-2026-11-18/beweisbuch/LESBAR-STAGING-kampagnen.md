# Beweisbuch p_vs_np (STAGING-kampagnen)

Eintraege: 3889, Hashkette intakt: True

PROOF LEDGER of this problem (kept across missions; 3889 entries from 740 missions). It records what is PROVED, what is only observed and what is open. RULE: a statement that is not PROVED or CITED here must never be used as an established premise. You may use it as an explicitly named OPEN ASSUMPTION - your result is then conditional on it.
PROVED (the proof tool supported them over their whole domain):
  - For every finite list of clauses over variables 0..n-1 in which each clause is a 3-element set of distinct variables, the rank over GF(3) of the clause-variable incidence matrix is at most n-1.
  - For every positive 1-in-3 formula F (each clause a 3-element set of variables; F is satisfiable if some 0/1 assignment has exactly one 1 in every clause): if F is satisfiable, then the GF(3) linear system with equation x_a + x_b + x_c = 1 for each clause {a,b,
  - For every positive 1-in-3 formula F with n variables and at least one clause (each clause a 3-subset of {0..n-1}), with A the clause incidence matrix over GF(3) and b = all-ones: F is 1-in-3 satisfiable iff the affine system A x = b over GF(3) has a solution x
  - For every positive 1-in-3 formula F with incidence matrix A (rows = clauses, columns = variables, entries 0/1): if F is satisfiable then the system A x = 1 is solvable over GF(3). Equivalently cons3=0 implies sat=0.
  - For every positive 1-in-3-SAT formula F (every clause is a 3-set of variables, exactly one of which must be true), if F is satisfiable then the all-ones vector lies in the column space of the clause-variable incidence matrix A over GF(3) (i.e. cons3(F)=1). Equ
  - For every n >= 3 and every nonempty set F of distinct weight-3 clauses over variables 0..n-1: there is a GF(3) vector x with x_a+x_b+x_c = 1 (mod 3) for every clause {a,b,c} in F, taking exactly two distinct values, if and only if F has a 0/1 solution (exactly
CITED from the literature (not machine-checked here):
  - Marti-Farre & Padro, 'On secret sharing schemes, matroids and polymatroids' (TCC 2007; IACR eprint 2006/077): if every share of a perfect secret sharing scheme is shorter than 3/2 times the secret, its access structure is a matroid port (proof via Seymour 1976
  - Kullmann, 'An Application of Matroid Theory to the SAT Problem' (ECCC TR00-018, 2000): minimally unsatisfiable clause sets of bounded deficiency, transversal matroids, matching, resolution; polynomial-time decision for such classes. Background for D-013, NOT a
  - Physical NP solvers and their hidden costs: linear optics driven by classical (coherent) light is classically simulable in time polynomial in the number of modes; optical 'solvers' for subset sum / Hamiltonian path move the exponential into the number of paths
  - Temporal cloaking is experimentally established (time lenses + dispersion open and close a temporal gap and restore the probe): McCall et al. 2011, Fridman et al. 2012, Lukens-Leaird-Weiner 2013/2014, field-programmable silicon temporal cloak 2019. It rearrang
  - Del Pia (2026-10-07): integer programming on polytopes of Chvatal rank at most 1 is as hard as lattice problems (conditional on LWE-type assumptions): short rank-1 cutting-plane refutations can exist while FINDING them is hard - necessary rank != discovery cos
  - Number of non-isomorphic 3-uniform hypergraphs on 7 vertices: 7,013,320 (2^35 labelled clause sets on 7 variables). (OEIS A000665; owner's Burnside computation 2026-11-19)
  - Cutting planes with polynomially bounded coefficients is separated from unbounded CP under SIMULTANEOUS length and line-space bounds (lifting with simple gadgets); the pure length separation is open (Nordstrom survey). Weakening strategies in PB conflict analy
  - Integer programming in fixed dimension is polynomial (Lenstra 1983; Kannan 1987: 2^O(d log d) poly). Applied to A x = 1, x >= 0 integer: the integer solutions form x0 + (integer kernel lattice of dimension d = n - rank_Q(A)), so positive 1-in-3-SAT is decidabl
  - Algebraic CDCL: CryptoMiniSat with Gauss-Jordan elimination refutes an Urquhart parity instance in ~1 s where Kissat did not finish in 16 h, with BDD-based certificates (some ~100 GB) (Soos-Bryant 2023); CDCL(xor) learning disjunctions of parity equations corr
  - CDCL and resolution: CDCL conflict analysis yields resolution proofs, and CDCL with restarts p-simulates resolution, so resolution lower bounds bind classical CDCL. (Pipatsrisawat-Darwiche 2011; Atserias-Fichte-Thurley 2011 (director's recollection; verify bef
HYPOTHESES on file, not proved:
  - On occ2=0 rows, the rank2=6 cell admits one shared law in both datasets: sat = (cons2 + null3) mod 2 = [rank3 == rank5]. The exact-law search found (cons2+null3) mod 2 on lane_1795034161_1 and [rank3==rank5] on lane_1795034271_0 for this cell, which would make
  - Every GF(3)-consistent system with no 0/1 solution (positive 1-in-3, clause sets from n=6 triples) has GF(3) rank n-1 = 5. Over GF(3) its solution set is then a single affine line of 3 points, and none of the 3 is 0/1. Over the rationals the rank may be 6, so 
  - For GF(3)-blind positive 1-in-3 formulas, GF(2) rank 5 and GF(5) rank 5 hold on exactly the same formulas (the rank2=5 blind set equals the rank5=5 blind set) at every n, not just n in {6,7}.
  - On minimal GF(3)-consistent (blind) UNSAT positive 1-in-3 cores, the core size equals the GF(3) rank of the clause system: size = rank3 on every blind core (exact on all 62,370 blind rows of the n=7 table, with 0 holdout counterexamples; no such law for blind=
  - Degree transfer from 3-colouring: for a graph G let T(G) be the positive 1-in-3 formula with clauses (x_v1,x_v2,x_v3) for every vertex v and (x_uc,x_wc,y_uwc) with a fresh variable for every edge uw and colour c. (a) T(G) is GF(3)-consistent for every G. (b) T
  - Every positive 1-in-3 formula that is GF(3)-consistent and unsatisfiable (gf3_blind=1) has GF(2) incidence rank rank2 >= 5. Equivalently, GF(2) rank <= 4 forces sat whenever cons3 holds.
REFUTED:
  - False at n=6: the 180 minimal GF(3) gap cores with degree sequence (2,2,2,3,3,3) are Z-blind (all 900 cores are integer-solvable, D-023) and have no variable of degree 1. Representative {012, 013, 045, 145, 234}: degrees v0..v5 = 3,3,2,2,3,2.
  - False from n=7: S = {036, 045, 026, 124, 456, 235, 016} is Boolean-UNSAT, solvable mod 3 (3 solutions), not solvable mod 9; Smith invariants A: (...,9), [A|1]: (...,3). Random UNSAT GF(3)-consistent sets: 6/300 (n=7), 9/300 (n=8), 11/300 (n=9) have a mod-9 obs
  - Non-port (P4 minor) does not indicate hardness: 2-SAT (in P) has a P4 minor at n=3, hence is not a matroid port for all n>=3; so no implication non-port => super-linear circuit size exists. D-013 remains a theorem about ideal secret sharing / ideal mSP only.
  - procedure alg-f496d8017c75 (cons2 and cons3 and rank_GF3(matrix_B) = m => SAT; author nemotron-3.5-bolt) is sound
APPROACHES already examined (do not repeat one without a new idea):
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> None
NUMERICAL EVIDENCE on file: 1057 entries (finite cases; they prove nothing about all cases). Latest: None
OPEN RESEARCH QUESTIONS (derived from this ledger; questions, not facts):
  - Q-47921f408f [UNEXPLAINED, OPEN] Why do the cell-level exact laws for sat on occ2=0 differ across datasets? On rank2=6 the two datasets yield different expressions, (cons2+null3) mod 2 vs [rank3==rank5]; on n=8 the expression is [rank3==rank5] in one da
  - Q-3085183852 [IMPLICATION, OPEN] PRIORITY (owner 2026-11-19): ACC0 / MOD6 DIRECTION - binding spec /root/contracts/PNP-001-ACC0-MOD6-2026-11-19.md (read it). Object: SAT_N^{1in3} on the triple-indicator input. LEVEL 1a TRANSFER AUDIT first: which known 
  - Q-1f5bfb5344 [UNEXPLAINED, OPEN] ML screen of the exact dataset agent_topic_onein3_n6_subsets_v1_acb44609 (137979 rows): target sat01 is predicted (holdout {"accuracy": 0.9895637048847659, "balanced_accuracy": 0.9920578891634311, "brier": 0.009728580309
  - Q-8506608173 [UNEXPLAINED, OPEN] ML screen of the exact dataset agent_topic_onein3_n6_subsets_v1_acb44609 (137979 rows): target int_z is predicted (holdout {"accuracy": 0.8922742426438615, "balanced_accuracy": 0.922700431761321, "brier": 0.0733345077941
  - Q-dc612cfa42 [UNEXPLAINED, OPEN] ML screen of the exact dataset agent_topic_onein3_n6_subsets_v1_acb44609 (137979 rows): target gf3_cons is predicted (holdout {"accuracy": 0.9942600376866213, "balanced_accuracy": 0.9918639053254438, "brier": 0.005104953
STOPPED BRANCHES (no new information after a bounded escalation; reopen only under the stated condition):
  - Does a non-cheap invariant of the affine GF(3) solution space separate the 1-in-3 gap (consistent but unsatisfiable) from the satisfiable consistent formulas, a -> reopen if: An invariant at n>=11, or a non-cheap one that is not the two-value indicator, gives an exact law or a >=99% near-law on the consistent clas
  - VALIDATOR RESULT for the claim claim:353c2fc1b3c9 by pnp-desk/research/R0183:claude-haiku-5-5@default: FORMALLY_VERIFIED - FORMALLY VERIFIED: Lean theorem one_i -> reopen if: None
  - The n=6 counterexamples to cons3 => sat all have GF(3)-rank 5 (rank3 = n-1) with consistent augmented system. The stated mechanism (a 1-dimensional GF(3) soluti -> reopen if: A0488 completes with mism=0, or an orbit-reduced n=7 census is planned for rank <= n-2 / rank n-1 necessity
  - ML screen pre-check on agent_agent_cg_nullity2_plane_v1_e4863028: the single column(s) ['n_full', 'pt1', 'pt2', 'pt4', 'pt5', 'pt7', 'pt8'] determine target ran -> reopen if: The census is shown to produce nullity-2 instances whose null3 is not n_full - rank3 (i.e. the column definitions differ), or a nullity-2 in
NEXT PROOF GAP: State this step formally and have it checked: #F equals the sum over clause sets S of (-1)^|S| N(S), where N(S) = 2^(n - |V(S)|) if S is consistent and 0 otherwise (inclusion-exclusion over falsified clauses)  (derived in words only: state it formally and have the proof tool check that it follows from its premises)
