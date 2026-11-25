PROOF LEDGER of this problem (kept across missions; 14498 entries from 4158 missions). It records what is PROVED, what is only observed and what is open. RULE: a statement that is not PROVED or CITED here must never be used as an established premise. You may use it as an explicitly named OPEN ASSUMPTION - your result is then conditional on it.
PROVED (the proof tool supported them over their whole domain):
  - statement: Lemma (restriction-independent gates survive). Let C be a fan-in-2 Boolean circuit on variables X∪Y, and let g be a gate whose computed Boolean function depends only on Y. For every assignment a to X, the gate function after restricting X=a is the s
  - statement: For fixed admissible s,A satisfying the stated infinitely-often disjunction, every M in M_{s,A}^{plain} and every fixed c,d has no m1 such that S_M(m)<=s(m)^c and tau_M(m)<=s(m)^d holds for all m>=m1.
derivation: Assume such an m1 exists. Instantiat
  - For the cyclic 1-in-3 CNF C_n with clauses {x_i, x_{i+1}, x_{i+2}} (indices mod n, n>=3), with exactly-one constraint per clause, C_n is satisfiable over {0,1} if and only if 3 divides n.
  - Let X and Z be finite sets, and let E = {E_1,...,E_k} (k >= 1) be relations E_i subset of X x Z with projection pi: X x Z -> X. Let H = pi(intersection of all E_i) be nonempty. Assume COND: if k >= 2 then for every j in {1,...,k}, pi(intersection of E_i over i
  - For every n >= 1, every integer weight vector w in Z^n with max_i |w_i| <= B, every integer threshold t, and every l in {0,...,n}: the set of functions y in {0,1}^(n-l) -> [w_rest.y >= t - w_pre.rho], indexed by rho in {0,1}^l, has at most min(2^l, 2lB+1) dist
  - For all rationals beta, eta, c with 0 <= eta <= beta and 0 <= c < 1: (2+beta-eta)/(1+c) > 1. More generally, for rationals beta, eta and c >= 0: (2+beta-eta)/(1+c) > 1 if and only if c < 1+beta-eta.
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
  - For the MCSP[s] YES set Y on {0,1}^N, the XOR translation stabilizer H={h: Y+h=Y} has dimension at most O(s log(m+s)) when N=2^m and circuits are fan-in-2 over {AND,OR,NOT,0,1}.
  - The local edit bound C(g) ≤ C(f) + m(t+1) for B2 circuits is tight up to constant factors for some pairs (f,g) differing on t inputs. In particular, for the MCSP[m^c] predicate on N=2^m bits, there exist truth tables at Hamming distance t = Θ(N/m) where the ci
  - For some circuit families with large prefix width, allowing transition-map don’t-cares on unreachable states can reduce minimum per-step gate cost relative to synthesizing the entire Boolean map.
  - For a THR-of-THR circuit whose bottom gates have nonnegative integer weights and each gate has total weight at most B, separately encoding every bottom gate by carry-save compression yields O(m(B+log(B+1))) quadratic equations. Test: construct circuits with ov
  - At a layer with q distinct nonempty residuals and at least one empty residual, any live/dead-separated encoding needs at least q+1 states.
  - Any two-sided reduction from a nonconstant source language to Gap-MCSP[s,s'] whose output truth tables are uniformly evaluable by a fan-in-2 circuit of size at most s is impossible. Test a proposed reduction by deriving its evaluator size and comparing it with
REFUTED:
  - Lemma D1 (one-step drop, bookkeeping, not progress): C fan-in-2 B_2 circuit of size s computing f; x_i has fan-out 1 into gate g = op(x_i, y), y != x_i; some b in {0,1} makes op(b, .) in {0, 1, y, not y}. Then f|x_i=b has a B_2 circuit of size <= s-1. Proof: d
  - Conjecture: every minimally GF(3)-blind family of positive 1-in-3 clauses has cov = rank3 + 1. REFUTED: F = {012, 013, 045, 145, 236} on 7 variables is GF(3)-blind (no 0/1 assignment with exactly one 1 per clause; A x = 1 solvable over GF(3)), minimal (no 4-cl
  - False at n=6: the 180 minimal GF(3) gap cores with degree sequence (2,2,2,3,3,3) are Z-blind (all 900 cores are integer-solvable, D-023) and have no variable of degree 1. Representative {012, 013, 045, 145, 234}: degrees v0..v5 = 3,3,2,2,3,2.
  - False from n=7: S = {036, 045, 026, 124, 456, 235, 016} is Boolean-UNSAT, solvable mod 3 (3 solutions), not solvable mod 9; Smith invariants A: (...,9), [A|1]: (...,3). Random UNSAT GF(3)-consistent sets: 6/300 (n=7), 9/300 (n=8), 11/300 (n=9) have a mod-9 obs
APPROACHES already examined (do not repeat one without a new idea):
  - None -> None
  - None -> EXHAUSTED: TURN_LIMIT
  - None -> EXHAUSTED: TURN_LIMIT
  - None -> EXHAUSTED: TURN_LIMIT
  - None -> EXHAUSTED: TURN_LIMIT
  - None -> None
  - None -> EXHAUSTED: TURN_LIMIT
  - None -> EXHAUSTED: TURN_LIMIT
NUMERICAL EVIDENCE on file: 3196 entries (finite cases; they prove nothing about all cases). Latest: None
OPEN RESEARCH QUESTIONS (derived from this ledger; questions, not facts):
  - Q-e8d7425cff [UNEXPLAINED, OPEN] Does the MCSP[m^c] predicate have a pair of truth tables at Hamming distance t = o(N) where the B2 circuit complexity difference is ω(mt)? If yes, the local edit bound is not tight for MCSP, suggesting the MCSP truth tab
  - Q-441857621f [MISSING_PROOF, OPEN] Can the cofactor decomposition inequality C_m(f)<=C_{m-1}(f_0)+C_{m-1}(f_1)+4 be amplified over a large family of MCSP truth-table slices so that hardness aggregates without the factor-of-two loss from repeated Shannon e
  - Q-2285d93e38 [MISSING_PROOF, OPEN] For EXT_{n,s}, can the canonical one-hot residual transition cost O(d_t+d_{t+1}) be bounded by poly(s,n) uniformly in prefix length, or must some level have superpolynomial residual count? This is the exact remaining bri
  - Q-9b770a3112 [MISSING_PROOF, OPEN] VALIDATOR RESULT for the claim claim:ec4975c1357c by pnp-desk/research/R2994:gpt-6-luna@default: OPEN_UNPROVEN - no counterexample found; formal proof attempt INCONCLUSIVE: GIVE_UP: The only Lean verification executed wa
  - Q-5aeb1665c5 [MISSING_PROOF, OPEN] For a fixed fan-in-two relation circuit H(x,w), can the projected residuals of L(x)=∃w H(x,w) be represented by a canonical state whose next-bit transition uses poly(h,r) real Boolean gates uniformly for all H, or is a s
STOPPED BRANCHES (no new information after a bounded escalation; reopen only under the stated condition):
  - PRIORITY (owner 2026-11-21, DIRECTION 1 - lane P: PSEUDORANDOM GENERATORS FOR XOR_2 o THR o THR): an explicit generator G: {0,1}^r -> {0,1}^n that fools XOR_2 o -> reopen if: A threshold-level (single THR gate or THR o THR) bias bound for G_c, or an explicit family whose parity bound transfers through an L1 bound 
  - Q-2d7c6a77bf follow-up: can a non-prefix partition family, or weighted cut costs, beat the (N-1)+Lambda_pi bound of L-K1-PREFIX? Note: gates with P(u)=0 (consta -> reopen if: A non-prefix partition family or weighted cut cost is shown to be O(polylog(N)*s) on bounded-fan-out expander circuits, or a cross-family re
  - RECON-REMAINDER Case E (owner 2026-11-23, target (8)): recover proofs left unextracted in FINAL outputs (research R*.json, proofbook FINAL entries); list statem -> reopen if: None
  - RECON-REMAINDER Route G (owner 2026-11-23, target (8)): PIT, GCT, permanent/determinant, algebraic natural proofs, Williams-type transfers, algebraic vs Boolean -> reopen if: A source-checked polynomial-size conversion preserving the Boolean-cube identity predicate, together with a transfer theorem matching its ex
NEXT PROOF GAP: State this step formally and have it checked: #F equals the sum over clause sets S of (-1)^|S| N(S), where N(S) = 2^(n - |V(S)|) if S is consistent and 0 otherwise (inclusion-exclusion over falsified clauses)  (derived in words only: state it formally and have the proof tool check that it follows from its premises)