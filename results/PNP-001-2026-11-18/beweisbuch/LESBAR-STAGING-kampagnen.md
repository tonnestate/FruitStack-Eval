# Beweisbuch p_vs_np (STAGING-kampagnen)

Eintraege: 9657, Hashkette intakt: True

PROOF LEDGER of this problem (kept across missions; 9657 entries from 2392 missions). It records what is PROVED, what is only observed and what is open. RULE: a statement that is not PROVED or CITED here must never be used as an established premise. You may use it as an explicitly named OPEN ASSUMPTION - your result is then conditional on it.
PROVED (the proof tool supported them over their whole domain):
  - Let X and Z be finite sets, and let E = {E_1,...,E_k} (k >= 1) be relations E_i subset of X x Z with projection pi: X x Z -> X. Let H = pi(intersection of all E_i) be nonempty. Assume COND: if k >= 2 then for every j in {1,...,k}, pi(intersection of E_i over i
  - For every n >= 1, every integer weight vector w in Z^n with max_i |w_i| <= B, every integer threshold t, and every l in {0,...,n}: the set of functions y in {0,1}^(n-l) -> [w_rest.y >= t - w_pre.rho], indexed by rho in {0,1}^l, has at most min(2^l, 2lB+1) dist
  - For all rationals beta, eta, c with 0 <= eta <= beta and 0 <= c < 1: (2+beta-eta)/(1+c) > 1. More generally, for rationals beta, eta and c >= 0: (2+beta-eta)/(1+c) > 1 if and only if c < 1+beta-eta.
  - For every positive 1-in-3 formula F (each clause is a 3-set of variables; sat(F)=1 iff exactly one variable of each clause is 1) that is satisfiable, the affine system over GF(3) with x_a+x_b+x_c=1 for each clause is consistent. Equivalently sat=1 implies cons
  - For every n >= 5 and every choice of distinct vertices u, v, a, b, c in [n], the positive 1-in-3 clause set {uva, uvb, uvc, abc} has no 1-in-3 satisfying assignment.
  - For every n >= 1 and every positive 1-in-3 formula with exactly two clauses T1, T2 (each a 3-subset of {0..n-1}, not necessarily distinct), there is S subset of {0..n-1} with |S ∩ T1| = 1 and |S ∩ T2| = 1. Equivalently, every 2-clause positive 1-in-3 formula i
CITED from the literature (not machine-checked here):
  - Liu-Pass Thm 1.2: one-way functions exist if and only if boundary-MINrK^poly is not in ioBPP (randomized time-bounded Kolmogorov complexity, boundary promise version). Thm 1.1: assuming E not in ioSIZE[2^{eps n}] for some eps > 0, the same holds for plain boun
  - Transfer theorem (Chen-Tal-Wang Lemma 3.8, from Bathie-Williams ITCS 2024 Thm 3.7 + Section 3.3 and the 2-query PCPP of Chen-Williams 2019 Lemma 25): for every alpha > 1, if CAPP with error o(1) for O(n^alpha)-size XOR_2 o THR o THR circuits is solvable in 2^n
  - Chen-Tal-Wang (2026-03-14): there is f in E^NP that requires n^{2.5-eps}-size THR o THR circuits for every eps > 0, via a 2^{n-n^{Omega(eps)}}-time algorithm estimating the acceptance probability of an XOR of two n^{2.5-eps}-size THR o THR circuits and William
  - Cheraghchi-Hirahara-Myrisiotis-Yoshida: Thm 1 (corollary of MMW19): there is mu > 0 such that MCSP[2^{mu n}] not in DTIME1[N^1.01] implies P != NP. Thm 2: there is a constant mu < 1 (close to 1) with MCSP[2^{mu n}] not in BPTIME1[N^1.99]. Thm 3: for every orac
  - Hirahara-Ilango-Williams, Beating Brute Force for Compression Problems, ECCC TR23-171, Thm 1.3: Search-MCSP[s] on truth tables of size 2^n has circuits of size 2^{(4/5)w+o(w)} poly(2^n), w = s log2(s+n) (Fiat-Naor inversion in Boolean circuits). (ECCC TR23-171
  - Tal, The Bipartite Formula Complexity of Inner-Product is Quadratic, ECCC TR16-181, Thm 3.2: bipartite formula complexity of IP_n is Omega(n^2/log^2 n). (ECCC TR16-181)
  - Kabanets-Koroth-Lu-Myrisiotis-Oliveira CCC 2020 (arXiv 2002.08533, ECCC TR20-018) Thm 34: if MCSP (threshold l as input) is in FORMULA[s] o XOR then s = Omega~(N^2); proof needs l = n^{Omega(1)}; fixed-threshold MCSP[N^beta] version not stated. (arXiv 2002.085
  - Chen-Jin-Williams, Sharp Threshold Results for Computational Complexity, ECCC TR20-065 / STOC 2020 (local copy literature/sources/eccc-TR20-065), Thm 1.6: for every alpha in (0,1) and eps > 0, MCSP[n^alpha] has no probabilistic n^{2+alpha-eps}-size formulas (f
  - Atserias-Mueller, Simple general magnification of circuit lower bounds, arXiv 2503.24061v2 (local copy literature/sources/arXiv-2503.24061): general magnification for 2^{n^{o(1)}}-sparse NP problems gives only fixed-polynomial lower bounds (Thm 4, 9; threshold
  - Chen-Jin-Williams, Hardness Magnification for all Sparse NP Languages, ECCC TR19-118 / FOCS 2019 (local copy literature/sources/eccc-TR19-118): if a 2^{n^{o(1)}}-sparse L in NP is not in Circuit[n^{1+eps}], then NP does not have n^k-size circuits for all k (fi
HYPOTHESES on file, not proved:
  - Row A of the K8 bridge map (Oliveira-Pich-Santhanam ToC 2021 Theorem (1)) is correctly stated: exists eps>0 such that for every small enough beta>0, Gap-MCSP[2^{beta n}/(c n), 2^{beta n}] not in Circuit[N^{1+eps}] implies NP not in Circuit[poly]; universal con
  - For the natural adder-plus-comparator encoding (L-b1), the first parameter of a THR o THR instance to violate the hypothesis of the OpenAI counting theorem (<= c n equations, constant degree, <= polylog monomials) is the EQUATION COUNT, not the variable count,
  - Valiant's depth-reduction lemma (primary form: remove r*m/log2(d) edges to reach depth d/2^r) implies that reducing a circuit of size m = Θ(n) and depth d = N^γ to depth N^γ' requires removing a fraction (γ-γ')/γ of all wires. This is feasible (fraction < 1) i
  - For random k-class MAJ o MAJ with k <= 4 and W = 2, the maximum DP state count S(n) grows like 2^{c n} with c < 1 (fitted exponents about 0.93 from n=10 to 12 and 0.83 from n=12 to 14). If so, the DP beats brute force on this random family asymptotically, even
  - For random +-1 weights with thresholds spread over a*sqrt(n), the expected flip count between the full function and the restriction with k fixed variables is about c * m * sqrt(k/n) / a, with c approximately 0.37. Heuristic: fixing F shifts each threshold by W
  - L2's arrangement argument can be fixed for half-open cells matching the >= convention by using a simplex range counting data structure (Matousek 1992) on half-open simplices defined by shifted hyperplanes s_j = t_j - delta/2, with delta the minimal non-zero |U
REFUTED:
  - Conjecture: every minimally GF(3)-blind family of positive 1-in-3 clauses has cov = rank3 + 1. REFUTED: F = {012, 013, 045, 145, 236} on 7 variables is GF(3)-blind (no 0/1 assignment with exactly one 1 per clause; A x = 1 solvable over GF(3)), minimal (no 4-cl
  - False at n=6: the 180 minimal GF(3) gap cores with degree sequence (2,2,2,3,3,3) are Z-blind (all 900 cores are integer-solvable, D-023) and have no variable of degree 1. Representative {012, 013, 045, 145, 234}: degrees v0..v5 = 3,3,2,2,3,2.
  - False from n=7: S = {036, 045, 026, 124, 456, 235, 016} is Boolean-UNSAT, solvable mod 3 (3 solutions), not solvable mod 9; Smith invariants A: (...,9), [A|1]: (...,3). Random UNSAT GF(3)-consistent sets: 6/300 (n=7), 9/300 (n=8), 11/300 (n=9) have a mod-9 obs
  - Non-port (P4 minor) does not indicate hardness: 2-SAT (in P) has a P4 minor at n=3, hence is not a matroid port for all n>=3; so no implication non-port => super-linear circuit size exists. D-013 remains a theorem about ideal secret sharing / ideal mSP only.
APPROACHES already examined (do not repeat one without a new idea):
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> None
NUMERICAL EVIDENCE on file: 2524 entries (finite cases; they prove nothing about all cases). Latest: None
OPEN RESEARCH QUESTIONS (derived from this ledger; questions, not facts):
  - Q-1aeca125c7 [COUNTEREXAMPLE, OPEN] The recorded law 'For formulas with rank2=3: sat = 1' (discovery status EXACTLY_TESTED) FAILS on other exact datasets: agent_onein3_ce_structure_v1_6b2ae1ea: 1449/1449 rows fail, e.g. [{"n": 5, "m": 3, "rank2": 3, "rank3
  - Q-111a0e44c4 [COUNTEREXAMPLE, OPEN] The recorded law 'For formulas with m=3: sat = 1' (discovery status EXACT_FINITE_VERIFICATION) FAILS on other exact datasets: agent_onein3_ce_structure_v1_6b2ae1ea: 1260/1260 rows fail, e.g. [{"n": 5, "m": 3, "rank2": 3,
  - Q-c4a60b0f14 [COUNTEREXAMPLE, OPEN] The recorded law 'For formulas with m=4: sat = cons3' (discovery status EXACT_FINITE_VERIFICATION) FAILS on other exact datasets: agent_onein3_ce_structure_v1_6b2ae1ea: 5198/5891 rows fail, e.g. [{"n": 5, "m": 4, "rank2"
  - Q-30fb0863f2 [COUNTEREXAMPLE, OPEN] The recorded law 'For formulas with rank2=4: sat = cons3' (discovery status EXACTLY_TESTED) FAILS on other exact datasets: agent_onein3_ce_structure_v1_6b2ae1ea: 7967/9215 rows fail, e.g. [{"n": 6, "m": 4, "rank2": 4, "r
  - Q-0348db2ce7 [COUNTEREXAMPLE, OPEN] The recorded law 'For formulas with rank5=4: sat = cons3' (discovery status EXACTLY_TESTED) FAILS on other exact datasets: agent_onein3_ce_structure_v1_6b2ae1ea: 7988/8786 rows fail, e.g. [{"n": 6, "m": 4, "rank2": 4, "r
STOPPED BRANCHES (no new information after a bounded escalation; reopen only under the stated condition):
  - PRIORITY (owner 2026-11-21, DIVERGENT LANE - lane N: THREE-FACTOR / ELIGIBILITY-TRACE ALGORITHMS): abstract the brain's coupling of fast activity a(t), connecti -> reopen if: None
  - PRIORITY (owner 2026-11-21, DIRECTION 1 - lane P: PSEUDORANDOM GENERATORS FOR XOR_2 o THR o THR): an explicit generator G: {0,1}^r -> {0,1}^n that fools XOR_2 o -> reopen if: A threshold-level (single THR gate or THR o THR) bias bound for G_c, or an explicit family whose parity bound transfers through an L1 bound 
  - PRIORITY (owner 2026-11-21, DIRECTION 1 - lane S: STATE COMPLEXITY OF THR o THR): K_l(C) = number of DISTINCT residual functions C|rho over the 2^l assignments  -> reopen if: A proof of a joint count of distinct clamped shift vectors over prefixes that is at most 2^(l - eps(n)) with eps superlogarithmic, or a lemm
  - PRIORITY (owner 2026-11-21, DIRECTION 1 - lane R: CERTIFIED LOW-RANK COMPRESSION OF RESIDUAL FUNCTIONS FOR CAPP; extends lane S Q-cc869fd7f8). Three state measu -> reopen if: A proved theorem bounds D or rank for a variable tree or restriction-then-ran
