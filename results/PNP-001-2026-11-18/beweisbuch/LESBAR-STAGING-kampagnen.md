PROOF LEDGER of this problem (kept across missions; 12104 entries from 3178 missions). It records what is PROVED, what is only observed and what is open. RULE: a statement that is not PROVED or CITED here must never be used as an established premise. You may use it as an explicitly named OPEN ASSUMPTION - your result is then conditional on it.
PROVED (the proof tool supported them over their whole domain):
  - For the cyclic 1-in-3 CNF C_n with clauses {x_i, x_{i+1}, x_{i+2}} (indices mod n, n>=3), with exactly-one constraint per clause, C_n is satisfiable over {0,1} if and only if 3 divides n.
  - Let X and Z be finite sets, and let E = {E_1,...,E_k} (k >= 1) be relations E_i subset of X x Z with projection pi: X x Z -> X. Let H = pi(intersection of all E_i) be nonempty. Assume COND: if k >= 2 then for every j in {1,...,k}, pi(intersection of E_i over i
  - For every n >= 1, every integer weight vector w in Z^n with max_i |w_i| <= B, every integer threshold t, and every l in {0,...,n}: the set of functions y in {0,1}^(n-l) -> [w_rest.y >= t - w_pre.rho], indexed by rho in {0,1}^l, has at most min(2^l, 2lB+1) dist
  - For all rationals beta, eta, c with 0 <= eta <= beta and 0 <= c < 1: (2+beta-eta)/(1+c) > 1. More generally, for rationals beta, eta and c >= 0: (2+beta-eta)/(1+c) > 1 if and only if c < 1+beta-eta.
  - For every positive 1-in-3 formula F (each clause is a 3-set of variables; sat(F)=1 iff exactly one variable of each clause is 1) that is satisfiable, the affine system over GF(3) with x_a+x_b+x_c=1 for each clause is consistent. Equivalently sat=1 implies cons
  - For every n >= 5 and every choice of distinct vertices u, v, a, b, c in [n], the positive 1-in-3 clause set {uva, uvb, uvc, abc} has no 1-in-3 satisfying assignment.
CITED from the literature (not machine-checked here):
  - Thm 4.1, Thm 5.4, Cor 6.2 of the owner's paper (as stated there). PAPER SETTING: G=(V,E) finite graph, F field, K subspace of F^I, blocks I_v; pi_X: K -> prod_{v in X} F^{I_v}. (R) rank pi_X >= d|X| for all X subset V; (L) z,z' in K with z|v != 0 != z'|v => su
  - Liu-Pass Thm 1.2: one-way functions exist if and only if boundary-MINrK^poly is not in ioBPP (randomized time-bounded Kolmogorov complexity, boundary promise version). Thm 1.1: assuming E not in ioSIZE[2^{eps n}] for some eps > 0, the same holds for plain boun
  - Transfer theorem (Chen-Tal-Wang Lemma 3.8, from Bathie-Williams ITCS 2024 Thm 3.7 + Section 3.3 and the 2-query PCPP of Chen-Williams 2019 Lemma 25): for every alpha > 1, if CAPP with error o(1) for O(n^alpha)-size XOR_2 o THR o THR circuits is solvable in 2^n
  - Chen-Tal-Wang (2026-03-14): there is f in E^NP that requires n^{2.5-eps}-size THR o THR circuits for every eps > 0, via a 2^{n-n^{Omega(eps)}}-time algorithm estimating the acceptance probability of an XOR of two n^{2.5-eps}-size THR o THR circuits and William
  - Cheraghchi-Hirahara-Myrisiotis-Yoshida: Thm 1 (corollary of MMW19): there is mu > 0 such that MCSP[2^{mu n}] not in DTIME1[N^1.01] implies P != NP. Thm 2: there is a constant mu < 1 (close to 1) with MCSP[2^{mu n}] not in BPTIME1[N^1.99]. Thm 3: for every orac
  - Hirahara-Ilango-Williams, Beating Brute Force for Compression Problems, ECCC TR23-171, Thm 1.3: Search-MCSP[s] on truth tables of size 2^n has circuits of size 2^{(4/5)w+o(w)} poly(2^n), w = s log2(s+n) (Fiat-Naor inversion in Boolean circuits). (ECCC TR23-171
  - Tal, The Bipartite Formula Complexity of Inner-Product is Quadratic, ECCC TR16-181, Thm 3.2: bipartite formula complexity of IP_n is Omega(n^2/log^2 n). (ECCC TR16-181)
  - Kabanets-Koroth-Lu-Myrisiotis-Oliveira CCC 2020 (arXiv 2002.08533, ECCC TR20-018) Thm 34: if MCSP (threshold l as input) is in FORMULA[s] o XOR then s = Omega~(N^2); proof needs l = n^{Omega(1)}; fixed-threshold MCSP[N^beta] version not stated. (arXiv 2002.085
  - Chen-Jin-Williams, Sharp Threshold Results for Computational Complexity, ECCC TR20-065 / STOC 2020 (local copy literature/sources/eccc-TR20-065), Thm 1.6: for every alpha in (0,1) and eps > 0, MCSP[n^alpha] has no probabilistic n^{2+alpha-eps}-size formulas (f
  - Atserias-Mueller, Simple general magnification of circuit lower bounds, arXiv 2503.24061v2 (local copy literature/sources/arXiv-2503.24061): general magnification for 2^{n^{o(1)}}-sparse NP problems gives only fixed-polynomial lower bounds (Thm 4, 9; threshold
HYPOTHESES on file, not proved:
  - A transition bound for the explicit EXT candidate-list state will yield information about arbitrary MCSP decision circuits only if one proves a representation map from H_C to the candidate-agreement state and bounds the map’s construction and update costs in r
  - For every finite Boolean family F and cut t, distinct next-level residuals arise among the two derivatives R_0 and R_1 of each level-t residual, so D_{t+1}<=2D_t; equality need not hold.
  - For at least one cut in SC_{3,1} or SC_{3,2}, the conflict graph H_t has a chromatic number that improves on the existing prefix-count bound and may sharpen finite state-width constraints.
  - A useful direct-circuit lower bound for MCSP may follow from a constraint on how a small MCSP circuit labels Hamming neighborhoods, combined with the 2m-per-flip complexity envelope.
  - For any two m-bit truth tables at Hamming distance d, their exact B2 circuit complexities differ by at most md; hence MCSP_s boundary pairs have complexities within md of s.
  - For the SC_{n,s} truth-table families, the common-accepting-suffix graph at a cut has clique number strictly larger than the live/dead counting bound at some cut, and the excess may constrain full-search state width under arbitrary encodings.
REFUTED:
  - Lemma D1 (one-step drop, bookkeeping, not progress): C fan-in-2 B_2 circuit of size s computing f; x_i has fan-out 1 into gate g = op(x_i, y), y != x_i; some b in {0,1} makes op(b, .) in {0, 1, y, not y}. Then f|x_i=b has a B_2 circuit of size <= s-1. Proof: d
  - Conjecture: every minimally GF(3)-blind family of positive 1-in-3 clauses has cov = rank3 + 1. REFUTED: F = {012, 013, 045, 145, 236} on 7 variables is GF(3)-blind (no 0/1 assignment with exactly one 1 per clause; A x = 1 solvable over GF(3)), minimal (no 4-cl
  - False at n=6: the 180 minimal GF(3) gap cores with degree sequence (2,2,2,3,3,3) are Z-blind (all 900 cores are integer-solvable, D-023) and have no variable of degree 1. Representative {012, 013, 045, 145, 234}: degrees v0..v5 = 3,3,2,2,3,2.
  - False from n=7: S = {036, 045, 026, 124, 456, 235, 016} is Boolean-UNSAT, solvable mod 3 (3 solutions), not solvable mod 9; Smith invariants A: (...,9), [A|1]: (...,3). Random UNSAT GF(3)-consistent sets: 6/300 (n=7), 9/300 (n=8), 11/300 (n=9) have a mod-9 obs
APPROACHES already examined (do not repeat one without a new idea):
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> None
NUMERICAL EVIDENCE on file: 3020 entries (finite cases; they prove nothing about all cases). Latest: None
OPEN RESEARCH QUESTIONS (derived from this ledger; questions, not facts):
  - Q-5f37ecf7cb [MISSING_PROOF, OPEN] VALIDATOR RESULT for the claim claim:86ce1d1e60ba by pnp-desk/research/R2192:gpt-6-luna@default: INCONCLUSIVE - the validator could not decide it (twice):  CLAIM: For every finite F⊆{0,1}^N, cut t, and correct determinis
  - Q-4fefea7031 [MISSING_PROOF, OPEN] For EXT_{n,s}, what richer state than one-bit prefix extendibility supports a forward update with real fan-in-two cost, and can it be represented by boundedly many operations on H_C for arbitrary MCSP decision circuits?
  - Q-a7ef063323 [MISSING_PROOF, OPEN] Can the candidate-circuit incidence update for EXT_{n,s} be compressed to polynomially many fan-in-two gates while retaining enough information to decide whether any candidate remains?
  - Q-d8719c804c [ASSUMPTION, OPEN] The claim 'For five distinct 3-bit prefixes p_0,...,p_4 and five distinct 3-bit suffixes u_0,...,u_4, define F={p_i u_i,p_i u_{i+1 mod 5}:0<=i<5}. The overlap graph on the live prefixes at cut 3 is C5, with clique number
  - Q-6f64c3d788 [IMPLICATION, OPEN] For Lemma M's time-dependent encodings with reachable transition domain D_t, can the sparse-domain upper bound k+r_t(k-1)+q max(r_t-1,0) be sharpened by sharing structure among equality indicators, and does any such stru
STOPPED BRANCHES (no new information after a bounded escalation; reopen only under the stated condition):
  - PRIORITY (owner 2026-11-21, DIRECTION 1 - lane P: PSEUDORANDOM GENERATORS FOR XOR_2 o THR o THR): an explicit generator G: {0,1}^r -> {0,1}^n that fools XOR_2 o -> reopen if: A threshold-level (single THR gate or THR o THR) bias bound for G_c, or an explicit family whose parity bound transfers through an L1 bound 
  - PRIORITY (owner 2026-11-21, DIRECTION 1 - lane R: CERTIFIED LOW-RANK COMPRESSION OF RESIDUAL FUNCTIONS FOR CAPP; extends lane S Q-cc869fd7f8). Three state measu -> reopen if: A proved theorem bounds D or rank for a variable tree or restriction-then-rank scheme, or an adversarial family with D = o(2^min(l,n-l)) und
  - Q-2d7c6a77bf follow-up: can a non-prefix partition family, or weighted cut costs, beat the (N-1)+Lambda_pi bound of L-K1-PREFIX? Note: gates with P(u)=0 (consta -> reopen if: A non-prefix partition family or weighted cut cost is shown to be O(polylog(N)*s) on bounded-fan-out expander circuits, or a cross-family re
  - RECON-REMAINDER Route G (owner 2026-11-23, target (8)): PIT, GCT, permanent/determinant, algebraic natural proofs, Williams-type transfers, algebraic vs Boolean -> reopen if: A source-checked polynomial-size conversion preserving the Boolean-cube identity predicate, together with a transfer theorem matching its ex
NEXT PROOF GAP: State this step formally and have it checked: #F equals the sum over clause sets S of (-1)^|S| N(S), where N(S) = 2^(n - |V(S)|) if S is consistent and 0 otherwise (inclusion-exclusion over falsified clauses)  (derived in words only: state it formally and have the proof tool check that it follows from its premises)