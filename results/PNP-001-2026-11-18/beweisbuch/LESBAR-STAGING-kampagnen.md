PROOF LEDGER of this problem (kept across missions; 10155 entries from 2516 missions). It records what is PROVED, what is only observed and what is open. RULE: a statement that is not PROVED or CITED here must never be used as an established premise. You may use it as an explicitly named OPEN ASSUMPTION - your result is then conditional on it.
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
  - For formulas with rank3=6: sat = cons3
  - For formulas with m=6: sat = [rank3 == rank5]
  - For the hidden weight bit family HWB_n, min over variable orders of the OBDD width W_OBDD(HWB_n) is NOT bounded by a polynomial in n (exponential growth, 2^{eps n}), so G0001 for this family is an exponential question; the apparent small-n polynomial fit is an
  - For formulas with rank5=4: sat = 1
  - For formulas with rank2=4: sat = 1
  - For B2 circuits of size s on n variables, fixing one variable to a constant and then a second variable can yield a size drop of at least 2 for essential functions when the circuit contains gates with fan‑out > 1 or specific gate types (AND, OR, XOR). This doub
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
NUMERICAL EVIDENCE on file: 2645 entries (finite cases; they prove nothing about all cases). Latest: None
OPEN RESEARCH QUESTIONS (derived from this ledger; questions, not facts):
  - Q-80630e3b33 [MISSING_PROOF, OPEN] Does a deterministic poly(N)-time, uniform construction exist for a string y in {0,1}^N outside Im_{n,s} (fan-in-2 circuits, size s = f(N) with f superpolylog), with a certificate of non-membership that is not itself an 
  - Q-598da227c2 [MISSING_PROOF, OPEN] Q-08a1c5b68f: is the n=3 literal-wiring UNSAT at affine S=5 (G=0) a true model floor or an encoding artefact? Next step: run the same own encoding at n=3 with the affine family at S=5 and S=6 under symmetry breaking (can
  - Q-73fbc92fa6 [LIMITATION, OPEN] CORRECTION to the affine S=4 control claim: the binding counting step is t=5 (L_5=16 live codes; a dead code needs a 17th code > 2^4), not t=4 (L_4=8 needs 9 <= 16, which is fine). Also desk job A0891 (ds-637881da432344f
  - Q-2f1bc7588b [MISSING_PROOF, OPEN] VALIDATOR RESULT for the claim claim:d694ad611eff by pnp-desk/research/R1498:claude-haiku-5-5@default: OPEN_UNPROVEN - no counterexample found; formal proof attempt TIME_CAP: no FINAL CLAIM: For every n >= 1 and every p 
  - Q-de8f2d456a [COUNTEREXAMPLE, OPEN] The recorded law 'For formulas with rank2=4: sat = cons3' (discovery status EXACTLY_TESTED) FAILS on other exact datasets: agent_onein3_ce_structure_v1_6b2ae1ea: 7967/9215 rows fail, e.g. [{"n": 6, "m": 4, "rank2": 4, "r
STOPPED BRANCHES (no new information after a bounded escalation; reopen only under the stated condition):
  - PRIORITY (owner 2026-11-21, DIVERGENT LANE - lane N: THREE-FACTOR / ELIGIBILITY-TRACE ALGORITHMS): abstract the brain's coupling of fast activity a(t), connecti -> reopen if: None
  - PRIORITY (owner 2026-11-21, DIRECTION 1 - lane P: PSEUDORANDOM GENERATORS FOR XOR_2 o THR o THR): an explicit generator G: {0,1}^r -> {0,1}^n that fools XOR_2 o -> reopen if: A threshold-level (single THR gate or THR o THR) bias bound for G_c, or an explicit family whose parity bound transfers through an L1 bound 
  - PRIORITY (owner 2026-11-21, DIRECTION 1 - lane R: CERTIFIED LOW-RANK COMPRESSION OF RESIDUAL FUNCTIONS FOR CAPP; extends lane S Q-cc869fd7f8). Three state measu -> reopen if: A proved theorem bounds D or rank for a variable tree or restriction-then-rank scheme, or an adversarial family with D = o(2^min(l,n-l)) und
  - Q-2d7c6a77bf follow-up: can a non-prefix partition family, or weighted cut costs, beat the (N-1)+Lambda_pi bound of L-K1-PREFIX? Note: gates with P(u)=0 (consta -> reopen if: A non-prefix partition family or weighted cut cost is shown to be O(polylog(N)*s) on bounded-fan-out expander circuits, or a cross-family re
NEXT PROOF GAP: State this step formally and have it checked: #F equals the sum over clause sets S of (-1)^|S| N(S), where N(S) = 2^(n - |V(S)|) if S is consistent and 0 otherwise (inclusion-exclusion over falsified clauses)  (derived in words only: state it formally and have the proof tool check that it follows from its premises)