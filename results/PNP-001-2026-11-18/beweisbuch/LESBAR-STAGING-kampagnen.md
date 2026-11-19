# Beweisbuch p_vs_np (STAGING-kampagnen)

Eintraege: 2780, Hashkette intakt: True

PROOF LEDGER of this problem (kept across missions; 2780 entries from 438 missions). It records what is PROVED, what is only observed and what is open. RULE: a statement that is not PROVED or CITED here must never be used as an established premise. You may use it as an explicitly named OPEN ASSUMPTION - your result is then conditional on it.
PROVED (the proof tool supported them over their whole domain):
  - Full-support sign matrices with every clause block of rank <= 1 are exactly the globally rank-1 sign matrices on the n=5 and n=6 Gal domains (solution dimension |U|+|V|-1: 101 and 3517), so their Gal ratio is 1; D-014 direction 1 is impossible within full-supp
  - On the Gal domains maxterms x minterms (1in3 n=5, n=6; xor3 n=5) no maxterm is contained in any minterm (maxterms are larger: 6 vs 4-5; 9-12 vs 4-6; 10 vs 2-6), so every containment-incidence matrix is identically zero. RC-fbc21332 (rank 0 everywhere) is corre
  - Independent recheck of RC-6d52805a-R: GF(2)/GF(3) rank profile of A and [A|1] (with n, m) does not determine the positive-1in3 count C mod 2. Method limit, expected (parity of #1in3 presumably parity-P-hard), not novel.
  - Audit of Prop 7.3 of the OpenAI cubic border-dc preprint (2026-09-24): no error found. Scope: Sec. 3 (Prop 3.1, permanent projection of the coefficient polynomial G_D) verified by exact computation; Sec. 4 (Lemmas 4.1, 4.2, Prop 4.3) read by PI and tested on s
  - delta_lambda(D_4) = 1 = p_lambda and gamma_lambda(Y_{3,4}) = 1 for lambda=(6,6,4,4,4), degree 6 (function convention). Together with entry 214: both five-row degree-6 candidates with lambda_1 = 6 are closed; neither gives an equation of D_4 nor a separating eq
  - delta_lambda(D_4) = 1 = p_lambda for lambda=(6,6,6,4,2), degree 6 (multiplicity of S_lambda(V*) in the degree-6 functions on the orbit closure of det_4). The same highest weight function is nonzero on l*perm_3, so gamma_lambda(Y_{3,4}) = 1: this lambda gives n
CITED from the literature (not machine-checked here):
  - Physical NP solvers and their hidden costs: linear optics driven by classical (coherent) light is classically simulable in time polynomial in the number of modes; optical 'solvers' for subset sum / Hamiltonian path move the exponential into the number of paths
  - Temporal cloaking is experimentally established (time lenses + dispersion open and close a temporal gap and restore the probe): McCall et al. 2011, Fridman et al. 2012, Lukens-Leaird-Weiner 2013/2014, field-programmable silicon temporal cloak 2019. It rearrang
  - Del Pia (2026-10-07): integer programming on polytopes of Chvatal rank at most 1 is as hard as lattice problems (conditional on LWE-type assumptions): short rank-1 cutting-plane refutations can exist while FINDING them is hard - necessary rank != discovery cos
  - Number of non-isomorphic 3-uniform hypergraphs on 7 vertices: 7,013,320 (2^35 labelled clause sets on 7 variables). (OEIS A000665; owner's Burnside computation 2026-11-19)
  - Cutting planes with polynomially bounded coefficients is separated from unbounded CP under SIMULTANEOUS length and line-space bounds (lifting with simple gadgets); the pure length separation is open (Nordstrom survey). Weakening strategies in PB conflict analy
  - Integer programming in fixed dimension is polynomial (Lenstra 1983; Kannan 1987: 2^O(d log d) poly). Applied to A x = 1, x >= 0 integer: the integer solutions form x0 + (integer kernel lattice of dimension d = n - rank_Q(A)), so positive 1-in-3-SAT is decidabl
  - Algebraic CDCL: CryptoMiniSat with Gauss-Jordan elimination refutes an Urquhart parity instance in ~1 s where Kissat did not finish in 16 h, with BDD-based certificates (some ~100 GB) (Soos-Bryant 2023); CDCL(xor) learning disjunctions of parity equations corr
  - CDCL and resolution: CDCL conflict analysis yields resolution proofs, and CDCL with restarts p-simulates resolution, so resolution lower bounds bind classical CDCL. (Pipatsrisawat-Darwiche 2011; Atserias-Fichte-Thurley 2011 (director's recollection; verify bef
  - Chevalley-Warning / Ax-Katz: for polynomials f_1..f_r over F_q in n variables with sum of degrees D < n, the number of common zeros in F_q^n is divisible by p (Ax-Katz: by q^ceil((n-D)/max deg)). Modular counting of CSP solutions has its own complexity dichoto
  - Model assumptions that change complexity: (1) a Turing machine running T(n) steps uses at most T(n)+O(1) tape cells, so the unbounded tape gives a polynomial algorithm no extra power; (2) a RAM that multiplies arbitrarily large integers at unit cost decides ex
HYPOTHESES on file, not proved:
  - For positive 1-in-3 formulas with rank2=4 (GF(2) incidence rank 4), cons3=1 implies sat=1. Equivalently, the GF(3) affine solution of A x = 1 always yields a 0/1 solution.
  - RETRACTION of S-e0c040e1ea: gap rows (cons3=1, sat=0) do not exist for n <= 5 (exhaustive). The inference that they exist for n in 6..9 rested only on the absence of an exact law for gap on the cons3=1 class and is not a count. Status: unverified.
  - CORRECTION to S-c8ce9b0160: for 0/1 targets, the predictions of 'sat = cons3' and 'sat = 1' differ exactly on rows with cons3 = 0, independent of gap rows (cons3 = 1, sat = 0). Gap rows make both laws fail on those rows; they do not enlarge the disagreement se
  - For every positive 1-in-3 formula, sat <= cons3 (with cons3 = GF(3)-solvability of the clause system x_a+x_b+x_c = 1). Hence the disagreement between 'sat = cons3' and 'sat = 1' on rank2=4 is exactly #{rank2=4, cons3=0}, and the only open content of law (a) is
  - On any class of positive 1-in-3 formulas, the disagreement between 'sat = cons3' and 'sat = 1' is exactly the set of rows with cons3 = 0, because sat => cons3 forces sat = 0 there. Both laws look exact on their own data for two reasons: (a) sat = cons3 is exac
  - For every unsatisfiable positive 1-in-3 formula with n <= 7, the exact rational depth-1 rank-1 Chvatal-Gomory closure of {x >= 0, Ax = 1} is empty.
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
NUMERICAL EVIDENCE on file: 649 entries (finite cases; they prove nothing about all cases). Latest: None
OPEN RESEARCH QUESTIONS (derived from this ledger; questions, not facts):
  - Q-5a88bf352a [MISSING_PROOF, OPEN] VALIDATOR RESULT for the claim claim:5ffe65c14c43 by owner-research: OPEN_UNPROVEN - no counterexample found; formal proof attempt INCONCLUSIVE: GIVE_UP: The claim cannot be formalised and kernel-checked within this lab'
  - Q-5fc2bfcf29 [COUNTEREXAMPLE, OPEN] The recorded law 'For formulas with rank3=3: sat = 1' (discovery status CONJECTURED) FAILS on other exact datasets: agent_agent_onein3_gap_exhaustive_n6_v2_5a6905d6: 1/3 rows fail, e.g. [{"m": 4, "rank3": 3, "cons3": 0, 
  - Q-dc2723a40f [COUNTEREXAMPLE, OPEN] The recorded law 'For formulas with rank2=4: sat = 1' (discovery status EXACTLY_TESTED) FAILS on other exact datasets: agent_agent_r0138_rank2_4_constructive_v1_fc8691c1: 5/2710 rows fail, e.g. [{"n": 8, "m": 4, "nused":
  - Q-1f3e885867 [COUNTEREXAMPLE, OPEN] The recorded law 'For formulas with m=4: sat = 1' (discovery status EXACTLY_TESTED) FAILS on other exact datasets: agent_agent_cg_rank1_n4to7_v1_2bb87450: 15/210 rows fail, e.g. [{"n": 4, "m": 4, "sat": 0, "p_empty": 0, 
  - Q-aa5dbf2f78 [COUNTEREXAMPLE, OPEN] The recorded law 'For formulas with rank5=5: sat = cons3' (discovery status EXACTLY_TESTED) FAILS on other exact datasets: agent_lane_dedup_1795034161_1_944c175f: 4/77 rows fail, e.g. [{"n": 6, "m": 5, "occ1": 1, "occ2":
STOPPED BRANCHES (no new information after a bounded escalation; reopen only under the stated condition):
  - Lab conjecture (desk, unverified): For formulas with rank2=3: Cmod2 = (detB + occ3) mod 2 | triage GENERAL_PROOF_OBLIGATION: a law about all n for an invariant- -> reopen if: dataset_id filtering API is added
  - The recorded law 'For formulas with n=5: sat = cons3' holds without exception on 21 independent exact datasets (6146 rows). Prove it in general, or find the fam -> reopen if: A theoretical argument shows the numerical mismatch is due to a definition error in cons3.
  - The recorded law 'For formulas with rank3=6: sat = cons3' (discovery status EXACTLY_TESTED) FAILS on other exact datasets: agent_lane_r0089_rank3_check_v1_6e38f -> reopen if: a structural invariant of the GF(3) solution coset (or a 0/1-cube obstruction computed exactly for n <= 8) that predicts sat exactly on the 
  - CDCL x ALGEBRA ON OUR FORMULAS (owner 2026-11-19, hypotheses derived from the CDCL literature): (H1) parity reasoning is useless here - GF(2) consistency holds  -> reopen if: A structured hard family (Tutte-barrier k>=5) or learned-clause/DRAT measures show blind > inconsistent at matched m, or NS degree on blind 
NEXT PROOF GAP: State this step formally and have it checked: #F equals the sum over clause sets S of (-1)^|S| N(S), where N(S) = 2^(n - |V(S)|) if S is consistent and 0 otherwise (inclusion-exclusion over falsified clauses)  (derived in words only: state it formally and have the proof tool check that it follows from its premises)
