# Beweisbuch p_vs_np (STAGING-kampagnen)

Eintraege: 8543, Hashkette intakt: True

PROOF LEDGER of this problem (kept across missions; 8543 entries from 2069 missions). It records what is PROVED, what is only observed and what is open. RULE: a statement that is not PROVED or CITED here must never be used as an established premise. You may use it as an explicitly named OPEN ASSUMPTION - your result is then conditional on it.
PROVED (the proof tool supported them over their whole domain):
  - For every n >= 1, every integer weight vector w in Z^n with max_i |w_i| <= B, every integer threshold t, and every l in {0,...,n}: the set of functions y in {0,1}^(n-l) -> [w_rest.y >= t - w_pre.rho], indexed by rho in {0,1}^l, has at most min(2^l, 2lB+1) dist
  - For all rationals beta, eta, c with 0 <= eta <= beta and 0 <= c < 1: (2+beta-eta)/(1+c) > 1. More generally, for rationals beta, eta and c >= 0: (2+beta-eta)/(1+c) > 1 if and only if c < 1+beta-eta.
  - For every positive 1-in-3 formula F (each clause is a 3-set of variables; sat(F)=1 iff exactly one variable of each clause is 1) that is satisfiable, the affine system over GF(3) with x_a+x_b+x_c=1 for each clause is consistent. Equivalently sat=1 implies cons
  - For every n >= 5 and every choice of distinct vertices u, v, a, b, c in [n], the positive 1-in-3 clause set {uva, uvb, uvc, abc} has no 1-in-3 satisfying assignment.
  - For every n >= 1 and every positive 1-in-3 formula with exactly two clauses T1, T2 (each a 3-subset of {0..n-1}, not necessarily distinct), there is S subset of {0..n-1} with |S ∩ T1| = 1 and |S ∩ T2| = 1. Equivalently, every 2-clause positive 1-in-3 formula i
  - THEOREM 16 (invariance cell M9b; report section 16; independently reviewed 2026-11-20): Lemma M9b' (external repair: rank of P_F = prod(1 - Q_D) across a cut >= 2^K for K variable-disjoint crossing clauses when a substitution with transcendental parameters lea
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
  - For random k-class MAJ o MAJ with k <= 4 and W = 2, the maximum DP state count S(n) grows like 2^{c n} with c < 1 (fitted exponents about 0.93 from n=10 to 12 and 0.83 from n=12 to 14). If so, the DP beats brute force on this random family asymptotically, even
  - For random +-1 weights with thresholds spread over a*sqrt(n), the expected flip count between the full function and the restriction with k fixed variables is about c * m * sqrt(k/n) / a, with c approximately 0.37. Heuristic: fixing F shifts each threshold by W
  - L2's arrangement argument can be fixed for half-open cells matching the >= convention by using a simplex range counting data structure (Matousek 1992) on half-open simplices defined by shifted hyperplanes s_j = t_j - delta/2, with delta the minimal non-zero |U
  - The s-shared subclass algorithm runs in O(2^s · poly(m,n,V)) exactly. For it to give a 2^{n(1-δ)} bound for the owner's regime m = n^α, one needs s ≤ n(1-δ). The subclass is non-empty (e.g., m gates each depending on one private variable plus the s shared ones
  - For integer W of rank r with entries bounded by B = O(1), the number of distinct prefix states y = N_{<=p} x_{<=p} in the rank-r Cramer DP (S0098) is at most C^r * poly(n) for an absolute constant C, so the DP runs in 2^{(1-eps)n} poly for r up to (1-eps)n / l
  - For the alternating family G_c with seed k and c = k, the worst-case max single-gate bias over THR gates on {0,1}^(2k) is at most C * 2^(-k/2) for an absolute constant C.
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
NUMERICAL EVIDENCE on file: 2313 entries (finite cases; they prove nothing about all cases). Latest: None
OPEN RESEARCH QUESTIONS (derived from this ledger; questions, not facts):
  - Q-05bd4a690f [MISSING_PROOF, OPEN] PRIORITY (owner 2026-11-21, K2-K6 lane, GRAPH ROUND Q-H - active-front and pebbling claims vs known simulations): any PNP-001 lemma claiming that a computation graph must hold its active front in memory must survive Shal
  - Q-5f38d74ee3 [MISSING_PROOF, OPEN] PRIORITY (owner 2026-11-21, K1 lane, GRAPH ROUND Q-G - non-stream MMW DAGs exactly): reconstruct the MMW19 merge constructions of Thm 1.1 / Lemma 3.1, Thm 1.4 (search-MCSP^A) and Thm 1.7 (MKTP, KT-Min-Merge) level by lev
  - Q-2d7c6a77bf [MISSING_PROOF, OPEN] PRIORITY (owner 2026-11-21, K1 lane, GRAPH ROUND Q-F - cumulative cut cost): verify the cut lemma (gate split with kappa cross edges => DCC(f) <= kappa+1 => log2 rank M_f <= kappa+1). Then investigate whether cut costs o
  - Q-77912decef [MISSING_PROOF, OPEN] PRIORITY (owner 2026-11-21, K2-K6 lane, GRAPH ROUND Q-E - controls for graph invariants): (i) for cubic bipartite expanders G_v verify that the PNP-001 colouring encoding satisfies w*(F(G_v)) = 2 tw(G_v)+1 = Omega(v) (re
  - Q-a295c260c1 [MISSING_PROOF, OPEN] PRIORITY (owner 2026-11-21, K2-K6 lane, GRAPH ROUND Q-D - computation-graph invariants vs locality): MMW Lemma 3.1 gives search-MCSP^A[s] merge-tree circuits whose only nontrivial nodes are Circuit-Min-Merge^A[s] gates o
STOPPED BRANCHES (no new information after a bounded escalation; reopen only under the stated condition):
  - PRIORITY (owner 2026-11-21, DIRECTION 1 - lane P: PSEUDORANDOM GENERATORS FOR XOR_2 o THR o THR): an explicit generator G: {0,1}^r -> {0,1}^n that fools XOR_2 o -> reopen if: A threshold-level (single THR gate or THR o THR) bias bound for G_c, or an explicit family whose parity bound transfers through an L1 bound 
  - PRIORITY (owner 2026-11-21, DIRECTION 1 - lane S: STATE COMPLEXITY OF THR o THR): K_l(C) = number of DISTINCT residual functions C|rho over the 2^l assignments  -> reopen if: A proof of a joint count of distinct clamped shift vectors over prefixes that is at most 2^(l - eps(n)) with eps superlogarithmic, or a lemm
  - PRIORITY (owner 2026-11-21, DIRECTION 1 - lane R: CERTIFIED LOW-RANK COMPRESSION OF RESIDUAL FUNCTIONS FOR CAPP; extends lane S Q-cc869fd7f8). Three state measu -> reopen if: A proved theorem bounds D or rank for a variable tree or restriction-then-rank scheme, or an adversarial family with D = o(2^min(l,n-l)) und
  - PRIORITY (owner 2026-11-21, P2 - TARGET STATEMENT 4: DIRECT MCSP CIRCUIT LOWER BOUND): prove that for some fixed c >= 1, the exact decision problem MCSP[m^c] (t -> reopen if: A general proof of a per-variable drop-2 statement for non-affine functions, or a superlinear method.
NEXT PROOF GAP: State this step formally and have it checked: #F equals the sum over clause sets S of (-1)^|S| N(S), where N(S) = 2^(n - |V(S)|) if S is consistent and 0 otherwise (inclusion-exclusion over falsified clauses)  (derived in words only: state it formally and have the proof tool check that it follows from its premises)
