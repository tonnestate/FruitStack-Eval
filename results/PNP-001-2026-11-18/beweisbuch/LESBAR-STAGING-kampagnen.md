PROOF LEDGER of this problem (kept across missions; 10357 entries from 2565 missions). It records what is PROVED, what is only observed and what is open. RULE: a statement that is not PROVED or CITED here must never be used as an established premise. You may use it as an explicitly named OPEN ASSUMPTION - your result is then conditional on it.
PROVED (the proof tool supported them over their whole domain):
  - Let X and Z be finite sets, and let E = {E_1,...,E_k} (k >= 1) be relations E_i subset of X x Z with projection pi: X x Z -> X. Let H = pi(intersection of all E_i) be nonempty. Assume COND: if k >= 2 then for every j in {1,...,k}, pi(intersection of E_i over i
  - For every n >= 1, every integer weight vector w in Z^n with max_i |w_i| <= B, every integer threshold t, and every l in {0,...,n}: the set of functions y in {0,1}^(n-l) -> [w_rest.y >= t - w_pre.rho], indexed by rho in {0,1}^l, has at most min(2^l, 2lB+1) dist
  - For all rationals beta, eta, c with 0 <= eta <= beta and 0 <= c < 1: (2+beta-eta)/(1+c) > 1. More generally, for rationals beta, eta and c >= 0: (2+beta-eta)/(1+c) > 1 if and only if c < 1+beta-eta.
  - For every positive 1-in-3 formula F (each clause is a 3-set of variables; sat(F)=1 iff exactly one variable of each clause is 1) that is satisfiable, the affine system over GF(3) with x_a+x_b+x_c=1 for each clause is consistent. Equivalently sat=1 implies cons
  - For every n >= 5 and every choice of distinct vertices u, v, a, b, c in [n], the positive 1-in-3 clause set {uva, uvb, uvc, abc} has no 1-in-3 satisfying assignment.
  - For every n >= 1 and every positive 1-in-3 formula with exactly two clauses T1, T2 (each a 3-subset of {0..n-1}, not necessarily distinct), there is S subset of {0..n-1} with |S ∩ T1| = 1 and |S ∩ T2| = 1. Equivalently, every 2-clause positive 1-in-3 formula i
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
  - The affine control at S=5, G=1 is SAT (positive control). The one-flip structure at t=6 requires exactly one non-free gate at that step to break the collision: E' = E or (b xor (q_A + q_B + q_D)) where q_A,q_B,q_D are the three stored basis bits, giving G=1 at
  - For every m and t, the max residual-class count over fan-in-2 circuits of size s is 2^(floor(s/2)+1). This fits s=1,2,3 (values 2,4,4) and the OR-chain family at every odd s (2^((s+1)/2)).
  - For formulas with rank3=6: sat = cons3
  - For formulas with m=6: sat = [rank3 == rank5]
  - For the hidden weight bit family HWB_n, min over variable orders of the OBDD width W_OBDD(HWB_n) is NOT bounded by a polynomial in n (exponential growth, 2^{eps n}), so G0001 for this family is an exponential question; the apparent small-n polynomial fit is an
  - For formulas with rank5=4: sat = 1
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
  - None -> EXHAUSTED: TURN_LIMIT
  - None -> None
  - None -> None
NUMERICAL EVIDENCE on file: 2692 entries (finite cases; they prove nothing about all cases). Latest: None
OPEN RESEARCH QUESTIONS (derived from this ledger; questions, not facts):
  - Q-e50783bd12 [MISSING_PROOF, OPEN] VALIDATOR RESULT for the claim claim:707bfa09c28e by pnp-desk/research/R1546:claude-haiku-5-5@default: INCONCLUSIVE - the validator could not decide it (twice):  CLAIM: For the family SC_{3,1} (38 truth tables on N=8 inp
  - Q-920dcd6731 [MISSING_PROOF, OPEN] Does the affine family of n=3 (N=8) admit a dead-separated streaming system with S=5 and G<=1? A hand analysis suggests an explicit code: slots A=f(0), B=f(1), C=f(2), D=f(4), plus a dead flag E. Wires store the basis va
  - Q-6d0328cd7e [MISSING_PROOF, OPEN] Q-f1e058b72f
  - Q-db3dcab07d [UNEXPLAINED, OPEN] RESULT READY - the background job A1032 (LemmaM SC31 decoder size, background, g=1..8) submitted by R1557 finished after that session ended: code_run finished: ok=True dataset None experiment cm-8872774ad6be40ea . Its pu
  - Q-62aa151845 [UNEXPLAINED, OPEN] Two recorded laws for class m=6 and target sat DISAGREE on 6424 of 10937 rows: (a) 'For formulas with m=6: sat = (components + pairs_overlap2) mod 2' vs (b) 'For formulas with m=6: sat = (cons3 * planar) mod 2' (datasets
STOPPED BRANCHES (no new information after a bounded escalation; reopen only under the stated condition):
  - PRIORITY (owner 2026-11-21, DIVERGENT LANE - lane N: THREE-FACTOR / ELIGIBILITY-TRACE ALGORITHMS): abstract the brain's coupling of fast activity a(t), connecti -> reopen if: None
  - PRIORITY (owner 2026-11-21, DIRECTION 1 - lane P: PSEUDORANDOM GENERATORS FOR XOR_2 o THR o THR): an explicit generator G: {0,1}^r -> {0,1}^n that fools XOR_2 o -> reopen if: A threshold-level (single THR gate or THR o THR) bias bound for G_c, or an explicit family whose parity bound transfers through an L1 bound 
  - PRIORITY (owner 2026-11-21, DIRECTION 1 - lane R: CERTIFIED LOW-RANK COMPRESSION OF RESIDUAL FUNCTIONS FOR CAPP; extends lane S Q-cc869fd7f8). Three state measu -> reopen if: A proved theorem bounds D or rank for a variable tree or restriction-then-rank scheme, or an adversarial family with D = o(2^min(l,n-l)) und
  - Q-2d7c6a77bf follow-up: can a non-prefix partition family, or weighted cut costs, beat the (N-1)+Lambda_pi bound of L-K1-PREFIX? Note: gates with P(u)=0 (consta -> reopen if: A non-prefix partition family or weighted cut cost is shown to be O(polylog(N)*s) on bounded-fan-out expander circuits, or a cross-family re
NEXT PROOF GAP: State this step formally and have it checked: #F equals the sum over clause sets S of (-1)^|S| N(S), where N(S) = 2^(n - |V(S)|) if S is consistent and 0 otherwise (inclusion-exclusion over falsified clauses)  (derived in words only: state it formally and have the proof tool check that it follows from its premises)