# Beweisbuch p_vs_np (STAGING-kampagnen)

Eintraege: 4765, Hashkette intakt: True

PROOF LEDGER of this problem (kept across missions; 4765 entries from 1014 missions). It records what is PROVED, what is only observed and what is open. RULE: a statement that is not PROVED or CITED here must never be used as an established premise. You may use it as an explicitly named OPEN ASSUMPTION - your result is then conditional on it.
PROVED (the proof tool supported them over their whole domain):
  - For every positive 1-in-3 clause set F over variables 0..n-1 whose GF(3) system x_a+x_b+x_c=1 (one equation per clause, variables 0..n-1) is consistent with solution set S, F has a 0/1 solution if and only if the union over coordinates i of {p in S : p_i = 2} 
  - For every positive 1-in-3 CNF formula F (each clause is a set of three variables and requires exactly one true variable), with clause-variable incidence matrix A over the integers (rows = clauses, columns = variables, 0/1 entries): if F is satisfiable by a 0/1
  - For every finite list of clauses over variables 0..n-1 in which each clause is a 3-element set of distinct variables, the rank over GF(3) of the clause-variable incidence matrix is at most n-1.
  - For every positive 1-in-3 formula F (each clause a 3-element set of variables; F is satisfiable if some 0/1 assignment has exactly one 1 in every clause): if F is satisfiable, then the GF(3) linear system with equation x_a + x_b + x_c = 1 for each clause {a,b,
  - For every positive 1-in-3 formula F with n variables and at least one clause (each clause a 3-subset of {0..n-1}), with A the clause incidence matrix over GF(3) and b = all-ones: F is 1-in-3 satisfiable iff the affine system A x = b over GF(3) has a solution x
  - For every positive 1-in-3 formula F with incidence matrix A (rows = clauses, columns = variables, entries 0/1): if F is satisfiable then the system A x = 1 is solvable over GF(3). Equivalently cons3=0 implies sat=0.
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
  - PC degree over GF(2), GF(3) and GF(5) coincides for every positive or general 3-CNF formula, so the PC degree is characteristic-independent on the tested families.
  - Among full-support families of distinct 3-subsets, sat=0 and cons3=1 forces rank3 = m (the m clause rows are GF(3)-linearly independent, so the GF(3) system is always solvable) — the GF(3) gap is a 0/1 obstruction on an independent system. Consequence: the gap
  - For m=5 and n>=9: every family with full vertex support is satisfiable in the exact-one sense (sat=1). Consequence: the full-support sat=0 subclass, counts (0,0) = 2135 at n=7 and 560 at n=8, is empty at n=9, and the gap sat=0 with cons3=1 is empty at n>=9. Th
  - For m=5, sat and cons3 agree on every full-support family once n>=8 (the full-support sat=0,cons3=1 gap is absent for all n>=8 at m=5, and sat=cons3 on full support). The n=7 gap (1890) shows the gap is NOT absent for n<=7, so the threshold is a real feature o
  - For n=6, m<=5 positive 1-in-3 clauses: sat == cons3 for m<=4, and for m=5 the 900 counterexamples (cons3=1, sat=0) form a specific algebraic/structural class. The transition at m=5 from perfect alignment to gap=900 is not arbitrary but corresponds to a specifi
  - For positive 1-in-3 CNF formulas F, if F is GF(3)-consistent (cons3=1) and unsatisfiable (sat=0), then the GF(3) nullity is exactly 2, provided n=7 and m=5.
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
NUMERICAL EVIDENCE on file: 1399 entries (finite cases; they prove nothing about all cases). Latest: None
OPEN RESEARCH QUESTIONS (derived from this ledger; questions, not facts):
  - Q-35d88c3331 [LIMITATION, OPEN] Scope of claim:4d1dbc0f6f00 (FINITE_CONFIRMED, validator session F0375). The validator reports that 40 of the 48 rows of agent_pc_degree_gf235_n7_10_v2_284eb602 are -1 in all three PC-degree columns. The generator return
  - Q-a0b6b6667a [LIMITATION, OPEN] Host limit conflict: submit_claim and desk_submit now reject budget_s above 1800 s (schema maximum 1800), but PNP-001 research session R0383 instructs long jobs (n=8 enumerations, witness generators, certificate searches
  - Q-0a9d1c9365 [UNEXPLAINED, OPEN] Correction to the Q-9f79395da7 closing argument: the four stored datasets give per-dataset disagreement counts 236, 129, 77 and 35, summing to 477. Overlap can only lower the union of disagreement rows, so the union is a
  - Q-d550c99f78 [IMPLICATION, OPEN] Extend the S7-orbit count of blind clause sets beyond m=6 at n=7. The m=6 blind table is S7-closed with 54 orbits. What is the orbit count for m=5 and m=7 (all blind sets at each m, using the same canonical form as cm-fc
  - Q-e69abc4805 [LIMITATION, OPEN] Correction to HYPOTHESIS S-56aefe7943 (PC degree characteristic-independent). Its statement says 'for every positive or general 3-CNF formula'. The evidence covers only the 48 general 3-CNF rows with mixed literal signs 
STOPPED BRANCHES (no new information after a bounded escalation; reopen only under the stated condition):
  - The per-coordinate value-set signature (constant/two-valued/three-valued) of the GF(3) plane is constant on all consistent n=7 m=5 rows (every coordinate three- -> reopen if: None
  - Validator claim:105be175a18f (FAST_REFUTED) reports 1011 GF(3)-inconsistent, 21088 consistent nullity-2 and 28 unsatisfiable nullity-3 formulas for n=7, m=5. Ex -> reopen if: None
  - Among n=7 m=5 nullity-2 formulas covering all variables and GF(3)-consistent, the 1890 Boolean-blind formulas have forcing gadgets (classes B and A). Degree pro -> reopen if: a separator of sat for formulas with solution set larger than nullity 2 is found, or the Boolean-blind forcing gadgets on n=7 m=5 are shown 
  - VALIDATOR RESULT for the claim claim:94033264f146 by pnp-desk/research/R0347:claude-haiku-5-5@default: OPEN_UNPROVEN - no counterexample found; formal proof att -> reopen if: None
NEXT PROOF GAP: State this step formally and have it checked: #F equals the sum over clause sets S of (-1)^|S| N(S), where N(S) = 2^(n - |V(S)|) if S is consistent and 0 otherwise (inclusion-exclusion over falsified clauses)  (derived in words only: state it formally and have the proof tool check that it follows from its premises)
