PROOF LEDGER of this problem (kept across missions; 14074 entries from 4001 missions). It records what is PROVED, what is only observed and what is open. RULE: a statement that is not PROVED or CITED here must never be used as an established premise. You may use it as an explicitly named OPEN ASSUMPTION - your result is then conditional on it.
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
  - The padding-invariance assumption for Sigma3SAT^A is satisfied by the standard decider: a Sigma3SAT^A query encodes a quantified Boolean formula with oracle gates; trailing padding bits (e.g., zeros) do not change the encoded instance because the formula lengt
  - The CYCLE-DECOMPOSITION ENCODING BOUND (S0534) shows that any single permutation can be updated in O(SN / L_min) gates where L_min is the shortest cycle length. For the lower bound Omega(sqrt(m)/log m) to hold generally, hard permutations must have L_min = O(s
  - The MMW19 Thm 1.2 streaming algorithm for Search-MCSP[s] makes oracle queries of length q = ω(log s) (not merely Õ(s)). This would make the truth-table compilation step in transfer T0 superpolynomial, breaking the poly(s) simulation premise.
  - For SC_{3,1}, residual-language counts are strictly below live-prefix counts at each t>=4, and the residual profile may be a useful state-complexity invariant for Lemma M.
  - For any finite list D of at most 2^m Boolean strings of common length N, a binary prefix trie with subtree counts supports greedy construction of an absent length-(m+1) prefix in O(m) time after preprocessing. Building the trie can cost Theta(|D|N) time and sp
  - For every m-state set Q and every injective S-bit encoding, a transition that differs from identity on t states admits an O(t log m)-gate fan-in-two AND/NOT extension; the bound may be sharp up to constants for some encodings and sparse permutations.
REFUTED:
  - Lemma D1 (one-step drop, bookkeeping, not progress): C fan-in-2 B_2 circuit of size s computing f; x_i has fan-out 1 into gate g = op(x_i, y), y != x_i; some b in {0,1} makes op(b, .) in {0, 1, y, not y}. Then f|x_i=b has a B_2 circuit of size <= s-1. Proof: d
  - Conjecture: every minimally GF(3)-blind family of positive 1-in-3 clauses has cov = rank3 + 1. REFUTED: F = {012, 013, 045, 145, 236} on 7 variables is GF(3)-blind (no 0/1 assignment with exactly one 1 per clause; A x = 1 solvable over GF(3)), minimal (no 4-cl
  - False at n=6: the 180 minimal GF(3) gap cores with degree sequence (2,2,2,3,3,3) are Z-blind (all 900 cores are integer-solvable, D-023) and have no variable of degree 1. Representative {012, 013, 045, 145, 234}: degrees v0..v5 = 3,3,2,2,3,2.
  - False from n=7: S = {036, 045, 026, 124, 456, 235, 016} is Boolean-UNSAT, solvable mod 3 (3 solutions), not solvable mod 9; Smith invariants A: (...,9), [A|1]: (...,3). Random UNSAT GF(3)-consistent sets: 6/300 (n=7), 9/300 (n=8), 11/300 (n=9) have a mod-9 obs
APPROACHES already examined (do not repeat one without a new idea):
  - None -> EXHAUSTED: MODEL_SUPPLY_SILENT
  - None -> EXHAUSTED: TURN_LIMIT
  - None -> None
  - None -> None
  - None -> EXHAUSTED: TURN_LIMIT
  - None -> EXHAUSTED: TURN_LIMIT
  - None -> EXHAUSTED: TURN_LIMIT
  - None -> EXHAUSTED: MODEL_SUPPLY_SILENT
NUMERICAL EVIDENCE on file: 3163 entries (finite cases; they prove nothing about all cases). Latest: None
OPEN RESEARCH QUESTIONS (derived from this ledger; questions, not facts):
  - Q-5591ad33bf [MISSING_PROOF, OPEN] VALIDATOR RESULT for the claim claim:0a2ceae2bdfe by pnp-desk/research/R2856:gpt-6-luna@default: OPEN_UNPROVEN - no counterexample found; formal proof attempt INCONCLUSIVE: GIVE_UP: The Lean verifier accepted only the el
  - Q-d1d1ad55a5 [MISSING_PROOF, OPEN] VALIDATOR RESULT for the claim claim:c8f7d6e56cf8 by pnp-desk/research/R2856:gpt-6-luna@default: OPEN_UNPROVEN - no counterexample found; formal proof attempt NOT_FORMALIZED: GIVE_UP: No Lean verification was obtained, a
  - Q-ed98f7bb61 [MISSING_PROOF, OPEN] Can a lower bound on distinct EXT residuals be converted into a lower bound on real-gate update cost for arbitrary MCSP decision circuits, invariant under state recoding and accounting for deferred decoding?
  - Q-eb7a8c4610 [MISSING_PROOF, OPEN] Can the signature set |A{0,1}^h| for an integer matrix A of rational rank q be bounded more sharply using the Smith normal form or covolume of the image lattice A Z^h together with the zonotope A[0,1]^h, in a way that yi
  - Q-d25720b26b [MISSING_PROOF, OPEN] Can the exact-string residual-state lemma be generalized to Lemma M's arbitrary-witness decoder by defining continuation equivalence through sets of valid witness outputs, and can that equivalence yield any nontrivial lo
STOPPED BRANCHES (no new information after a bounded escalation; reopen only under the stated condition):
  - Q-2d7c6a77bf follow-up: can a non-prefix partition family, or weighted cut costs, beat the (N-1)+Lambda_pi bound of L-K1-PREFIX? Note: gates with P(u)=0 (consta -> reopen if: A non-prefix partition family or weighted cut cost is shown to be O(polylog(N)*s) on bounded-fan-out expander circuits, or a cross-family re
  - RECON-REMAINDER Case E (owner 2026-11-23, target (8)): recover proofs left unextracted in FINAL outputs (research R*.json, proofbook FINAL entries); list statem -> reopen if: None
  - RECON-REMAINDER Route E (owner 2026-11-23, target (8)): algebraic proof complexity (Thm 12, Thm 14, Lemma 15, Thm 16, NS/PC degree, overlap theorem, IPS): name  -> reopen if: An independent-model-family reviewer can assess S0058-S0060, and a concrete uniform polynomial-size/time NS/PC-to-roABP-IPS_LIN conversion (
  - RECON-REMAINDER Route G (owner 2026-11-23, target (8)): PIT, GCT, permanent/determinant, algebraic natural proofs, Williams-type transfers, algebraic vs Boolean -> reopen if: A source-checked polynomial-size conversion preserving the Boolean-cube identity predicate, together with a transfer theorem matching its ex
NEXT PROOF GAP: State this step formally and have it checked: #F equals the sum over clause sets S of (-1)^|S| N(S), where N(S) = 2^(n - |V(S)|) if S is consistent and 0 otherwise (inclusion-exclusion over falsified clauses)  (derived in words only: state it formally and have the proof tool check that it follows from its premises)