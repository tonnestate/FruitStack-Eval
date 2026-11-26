PROOF LEDGER of this problem (kept across missions; 16937 entries from 5564 missions). It records what is PROVED, what is only observed and what is open. RULE: a statement that is not PROVED or CITED here must never be used as an established premise. You may use it as an explicitly named OPEN ASSUMPTION - your result is then conditional on it.
PROVED (the proof tool supported them over their whole domain):
  - The rank of a submatrix is at most the rank of the matrix
PREMISES: 
PROOF:
SOURCE: proofbook seq 57; mission pi-theory-T1-T2; author model claude-opus-5-5; claim hash d981059752cbd2cd; registered by pnp_autoreview
  - CJW20-T5.5-GAP: Gap-MCSP[N^beta/(K m), N^beta] has no probabilistic De Morgan formula of size N^{2+beta-eps}
  - T07: every De Morgan circuit C of size S with r gates of fan-out > 1 has formula size L(C) <= 2^r (2S+1)
  - statement: Lemma (restriction-independent gates survive). Let C be a fan-in-2 Boolean circuit on variables X∪Y, and let g be a gate whose computed Boolean function depends only on Y. For every assignment a to X, the gate function after restricting X=a is the s
  - statement: For fixed admissible s,A satisfying the stated infinitely-often disjunction, every M in M_{s,A}^{plain} and every fixed c,d has no m1 such that S_M(m)<=s(m)^c and tau_M(m)<=s(m)^d holds for all m>=m1.
derivation: Assume such an m1 exists. Instantiat
  - For the cyclic 1-in-3 CNF C_n with clauses {x_i, x_{i+1}, x_{i+2}} (indices mod n, n>=3), with exactly-one constraint per clause, C_n is satisfiable over {0,1} if and only if 3 divides n.
CITED from the literature (not machine-checked here):
  - OPS21 (ToC v017a011, abstract-page theorem, numbering as Thm 1.4 unconfirmed): exists c>=1; if exists eps>0 such that for every small enough beta>0 Gap-MCSP[2^{beta n}/(cn), 2^{beta n}] notin Circuit[N^{1+eps}] then NP notsubset Circuit[poly] (hence P != NP) (
  - Thm 4.1, Thm 5.4, Cor 6.2 of the owner's paper (as stated there). PAPER SETTING: G=(V,E) finite graph, F field, K subspace of F^I, blocks I_v; pi_X: K -> prod_{v in X} F^{I_v}. (R) rank pi_X >= d|X| for all X subset V; (L) z,z' in K with z|v != 0 != z'|v => su
  - Liu-Pass Thm 1.2: one-way functions exist if and only if boundary-MINrK^poly is not in ioBPP (randomized time-bounded Kolmogorov complexity, boundary promise version). Thm 1.1: assuming E not in ioSIZE[2^{eps n}] for some eps > 0, the same holds for plain boun
  - Transfer theorem (Chen-Tal-Wang Lemma 3.8, from Bathie-Williams ITCS 2024 Thm 3.7 + Section 3.3 and the 2-query PCPP of Chen-Williams 2019 Lemma 25): for every alpha > 1, if CAPP with error o(1) for O(n^alpha)-size XOR_2 o THR o THR circuits is solvable in 2^n
  - Chen-Tal-Wang (2026-03-14): there is f in E^NP that requires n^{2.5-eps}-size THR o THR circuits for every eps > 0, via a 2^{n-n^{Omega(eps)}}-time algorithm estimating the acceptance probability of an XOR of two n^{2.5-eps}-size THR o THR circuits and William
  - Cheraghchi-Hirahara-Myrisiotis-Yoshida: Thm 1 (corollary of MMW19): there is mu > 0 such that MCSP[2^{mu n}] not in DTIME1[N^1.01] implies P != NP. Thm 2: there is a constant mu < 1 (close to 1) with MCSP[2^{mu n}] not in BPTIME1[N^1.99]. Thm 3: for every orac
  - Hirahara-Ilango-Williams, Beating Brute Force for Compression Problems, ECCC TR23-171, Thm 1.3: Search-MCSP[s] on truth tables of size 2^n has circuits of size 2^{(4/5)w+o(w)} poly(2^n), w = s log2(s+n) (Fiat-Naor inversion in Boolean circuits). (ECCC TR23-171
  - Tal, The Bipartite Formula Complexity of Inner-Product is Quadratic, ECCC TR16-181, Thm 3.2: bipartite formula complexity of IP_n is Omega(n^2/log^2 n). (ECCC TR16-181)
  - Kabanets-Koroth-Lu-Myrisiotis-Oliveira CCC 2020 (arXiv 2002.08533, ECCC TR20-018) Thm 34: if MCSP (threshold l as input) is in FORMULA[s] o XOR then s = Omega~(N^2); proof needs l = n^{Omega(1)}; fixed-threshold MCSP[N^beta] version not stated. (arXiv 2002.085
  - Chen-Jin-Williams, Sharp Threshold Results for Computational Complexity, ECCC TR20-065 / STOC 2020 (local copy literature/sources/eccc-TR20-065), Thm 1.6: for every alpha in (0,1) and eps > 0, MCSP[n^alpha] has no probabilistic n^{2+alpha-eps}-size formulas (f
HYPOTHESES on file, not proved:
  - For truth-table functions f on m-bit inputs, if a coordinate restriction has one constant cofactor and one nonconstant cofactor, its circuit complexity differs from that of the nonconstant cofactor by at most one gate in the unrestricted fan-in-two basis; cons
  - For permutations with large order L relative to the allowed phase-register capacity, periodic decoder schedules cannot be implemented with fewer than ceil(log2 L) phase bits.
  - D6'' (repair attempt for R', conditional): surviving narrow reused gates need not be paid in CORRELATION (AF budget N^{beta-eta}); they can be paid in formula SIZE. After the restriction a reused gate g with k_g live variables computes a function of k_g variab
  - For every m>=1 and threshold s, every m-bit truth table with at most floor((s+1)/m) satisfying inputs belongs to MCSP[s] in the free-input-negation fan-in-two basis.
  - INFORMATION THRESHOLD of AF vs magnification: AF can reach at most gamma < t = N^beta reused gates (seed >= log 1/delta, YES complexity <= t). The CHOPRS20 Thm 29 / Lemma 27 almost-formulas that magnification needs carry gamma = 2^{O(n^lambda)} >= t log t reus
  - AF (conditional, replaces the size budget by a correlation budget): let beta in (0,1), eta>0. Assume (P1) a local PRG fooling De Morgan formulas of size s with error delta <= 2^{-gamma}/10, seed and per-bit circuit size <= N^{beta-eta}; (P2) a pseudorandom res
REFUTED:
  - D6 (seq 16770) counting claim: 'reused gates with d_g <= N^{1-beta-eta} contribute <= N^{-2eta}, so only wide reused gates survive the restriction' - REFUTED. The per-gate bound Pr <= p^2 d_g^2/2 is right; the number of narrow reused gates is not bounded. Coun
  - MECHANISM: for every De Morgan circuit of size N^{1+eps}, the CJW20 pseudorandom restriction satisfies r(C|rho)+log2(2S(C|rho)+1) <= (3beta-eta)log2 N w.h.p.
  - Lemma D1 (one-step drop, bookkeeping, not progress): C fan-in-2 B_2 circuit of size s computing f; x_i has fan-out 1 into gate g = op(x_i, y), y != x_i; some b in {0,1} makes op(b, .) in {0, 1, y, not y}. Then f|x_i=b has a B_2 circuit of size <= s-1. Proof: d
  - Conjecture: every minimally GF(3)-blind family of positive 1-in-3 clauses has cov = rank3 + 1. REFUTED: F = {012, 013, 045, 145, 236} on 7 variables is GF(3)-blind (no 0/1 assignment with exactly one 1 per clause; A x = 1 solvable over GF(3)), minimal (no 4-cl
APPROACHES already examined (do not repeat one without a new idea):
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> EXHAUSTED: TURN_LIMIT
  - None -> None
  - None -> None
  - None -> None
NUMERICAL EVIDENCE on file: 3327 entries (finite cases; they prove nothing about all cases). Latest: None
OPEN RESEARCH QUESTIONS (derived from this ledger; questions, not facts):
  - Q-1c841c90f7 [MISSING_PROOF, OPEN] UNIFORM-QE (owner 2026-11-26) WITNESS-SENSITIVE SEARCH ONLY (supersedes Q-4c4127e83e). EXCLUDED - do not pursue: local many-one DECISION reductions to MCSP^A with s,t=M^{o(1)} for ANY oracle A, any uniformity, any gap ve
  - Q-7828a2a6e1 [MISSING_PROOF, PURSUED] CLOSURE-B (owner 2026-11-26) RESIDUAL R' - supersedes the D6 part of seq 16784. D6 is REFUTED (seq 16839, window-parity counterexample); use D6' (seq 16840) and the hypothesis D6'' (director/closure-intervention). Task 1
  - Q-88090df9cf [MISSING_PROOF, OPEN] VERIFY (owner 2026-11-26, cross-family) DIRECTOR DERIVATIONS: the steps in this question's proof state were written by the Claude family (director). Review each step against its stated premises and the primary sources; r
  - Q-47a55293d1 [MISSING_PROOF, OPEN] CLOSURE-D (owner 2026-11-26) UNIFORM STATE COLLISIONS - supersedes seq 16783; no other D work. Read CJ1-CJ4 (director/closure-quant) first. Reduction (CJ2, done): it suffices to construct, for every admissible DETERMINIS
  - Q-aea782b366 [MISSING_PROOF, OPEN] CLOSURE-FG (owner 2026-11-26) CANONICAL WITNESSES AND SIMPLE HITTING SETS: F1 and G1 are in the proofbook (F = route M with a Sigma_2 canonicaliser; G = restatement unless H is explicit, structured and uniformly selected
STOPPED BRANCHES (no new information after a bounded escalation; reopen only under the stated condition):
  - PRIORITY (owner 2026-11-21, DIRECTION 1 - lane P: PSEUDORANDOM GENERATORS FOR XOR_2 o THR o THR): an explicit generator G: {0,1}^r -> {0,1}^n that fools XOR_2 o -> reopen if: A threshold-level (single THR gate or THR o THR) bias bound for G_c, or an explicit family whose parity bound transfers through an L1 bound 
  - Q-2d7c6a77bf follow-up: can a non-prefix partition family, or weighted cut costs, beat the (N-1)+Lambda_pi bound of L-K1-PREFIX? Note: gates with P(u)=0 (consta -> reopen if: A non-prefix partition family or weighted cut cost is shown to be O(polylog(N)*s) on bounded-fan-out expander circuits, or a cross-family re
  - RECON-REMAINDER Case E (owner 2026-11-23, target (8)): recover proofs left unextracted in FINAL outputs (research R*.json, proofbook FINAL entries); list statem -> reopen if: None
  - RECON-REMAINDER Route G (owner 2026-11-23, target (8)): PIT, GCT, permanent/determinant, algebraic natural proofs, Williams-type transfers, algebraic vs Boolean -> reopen if: A source-checked polynomial-size conversion preserving the Boolean-cube identity predicate, together with a transfer theorem matching its ex
NEXT PROOF GAP: State this step formally and have it checked: #F equals the sum over clause sets S of (-1)^|S| N(S), where N(S) = 2^(n - |V(S)|) if S is consistent and 0 otherwise (inclusion-exclusion over falsified clauses)  (derived in words only: state it formally and have the proof tool check that it follows from its premises)