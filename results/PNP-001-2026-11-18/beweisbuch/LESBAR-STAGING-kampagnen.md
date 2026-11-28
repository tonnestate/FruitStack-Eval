PROOF LEDGER of this problem (kept across missions; 18807 entries from 6012 missions). It records what is PROVED, what is only observed and what is open. RULE: a statement that is not PROVED or CITED here must never be used as an established premise. You may use it as an explicitly named OPEN ASSUMPTION - your result is then conditional on it.
PROVED (the proof tool supported them over their whole domain):
  - T66 sec.10 Thm 10.1: for u'=Au, v'=Bv+h(Au)-Bh(u) with arbitrary h, w=v-h(u) satisfies w'=Bw, v_T=B^T(v_0-h(u_0))+h(A^T u_0) (also time-dependent A_t,B_t and towers). Thm 10.4: pulse h(u)=[u=e] on a primitive n-bit LFSR has Hankel rank exactly 2^n-1 over every
  - T66 sec.9 Thm 9.3: the absorbing halting observation a_t=[t>=tau] has infinite Hankel rank exactly tau+1 over every field (anti-triangular submatrix, determinant +-1; Kronecker for the eventually-constant generalisation: rank tau+1 iff c != 0 and a_{tau-1} != 
  - T66 sec.9 Thm 9.1 (O(rC+M(r)(log r+log T)) for scalar observations with promised Hankel rank r via BM on 2r terms + Bostan-Mori, promise/field/uniformity audited) and Thm 9.2: if the promise r is computed in time t_rho then for the diagonal language t_rho + rC
  - T66 sec.8 Thm 8.1 (symmetric-square lift): V K-invariant of dim r over F_3 (any field), W=span({1} u {fg:f,g in V}); then dim W<=1+r(r+1)/2, K W<=W (K ring homomorphism), every h in W has h(F^t x) satisfying the order-dim W recurrence of char poly of K|_W (Cay
  - T66 sec.7 CORRECTION (owner order): Thm 7.1 holds for the GLOBAL nilpotency index r_g (period of the function-valued sequence, lcm over x), not per trajectory. Thm 7.1a (trajectory): a_T=g(F^T x) is purely periodic with p-power period iff Newton coefficients D
  - T66 sec.7 (comp:koopman-lucas-period-duality, discovery mode): Thm 7.1 minimal period of T->g(F^T x) is exactly p^ceil(log_p r) for nilpotency index r (proof via Thm 6.2 + Lucas; 60 random unipotent systems + counters m=2..4 exact); Thm 7.2 K unipotent iff all
CONDITIONAL (verified steps resting on open assumptions):
  - NONLINEAR/BOOLEAN FORM OF THE QUOTIENT IDENTITY (owner derivation, checked). (i) S=F[x], R=S[z], ideals I_i of R: the module theorem of 18308 applies with pi:R->R/S (S-linear, kernel S); (sum I_i)∩S / sum(I_i∩S) = A/B, i.e. it compares the elimination ideal of
  - CORRECTION to 18312 (2): over F2 a valid certificate sum a_i f_i=1 has, at every point, an ODD number of active summands (a_i f_i=1); exactly one active summand is the special case of a choice function. Choice functions embed injectively into certificates (sig
  - NEW DERIVATIONS (own, instance-verified; novelty vs literature unchecked). (1) h is a Boolean-pivot algebraic-Morse contraction: on the region b_i f_i the constraint f_i is a unit so the pair cancels; elsewhere f_i=0 and e_i survives; critical cells exist only
  - ELEMENTARY IDENTITIES (verified independently; not cited, not claimed new). R=F2[x]/(x_i^2-x_i) is a Boolean ring (every element idempotent). D=prod(1-f_i) is the indicator of V(f), idempotent; E=1-D idempotent; DE=0; R=DR+ER; b_i=prod_{j<i}(1-f_j) gives b_i-b
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
  - For some explicit non-affine computation model with T-step trajectories, there may exist an exact fingerprint with description size o(T), efficient local verification of its update rule, and a decoding algorithm for the final state.
  - For fixed encodings, transitions changing t states with total codeword Hamming movement H admit extensions controlled by changed-state prefix geometry plus H; the explicit bound in S0888 may be asymptotically tight for some code/support geometries.
  - For every finite transition system with injective S-bit state encoding, the prefix-trie construction extends the transition to a total Boolean map with fan-in-two AND/NOT size O(S+T+H), where T is the changed-state prefix-trie size and H is the sum of Hamming 
  - For support A of size t under the same product restriction, if t*((1+p)/2)^m is small, Markov's inequality gives a small upper bound on the probability that any satisfying point survives. This may support a YES-side elimination bound only if the restriction al
  - For fixed c>=1, if every cofactor after fixing k coordinates has circuit size below (m-k)^c, this reconstruction method preserves the original threshold only when 2^k((m-k)^c)+3(2^k-1)+k < m^c. Determine whether this inequality admits a growing k in the AF/P1/
  - For admissible streaming machine families in which the two transition maps commute on reachable states, fixed AC0-uniform collision families can be obtained from short words with equal symbol counts; the two-letter pair 01 and 10 is the first case.
REFUTED:
  - Proposed coupling 'gate-ideal saturation / canonical selector structure forces small space for the selector' is refuted as a route.
  - T59 s7 R3 'no bound better than s*N'; T59 s10(1) 'affine selector => cost-free projection'; T59 s5 'equivalent forms MT/E.4/kappa~1'; T59 s10(4) 'single term'.
  - ERRATUM to Proofbook 17584 (construction text, not the representation theorem). The AND gadget as written there, EO(t,u,~a), EO(t,v,~b), EO(u,v,w) with fresh Boolean t,u,v,w, has a unique internal extension for every input (4/4) but computes XNOR(a,b), not AND
  - D6 (seq 16770) counting claim: 'reused gates with d_g <= N^{1-beta-eta} contribute <= N^{-2eta}, so only wide reused gates survive the restriction' - REFUTED. The per-gate bound Pr <= p^2 d_g^2/2 is right; the number of narrow reused gates is not bounded. Coun
APPROACHES already examined (do not repeat one without a new idea):
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - None -> EXHAUSTED: MODEL_SUPPLY_SILENT
NUMERICAL EVIDENCE on file: 3469 entries (finite cases; they prove nothing about all cases). Latest: None
OPEN RESEARCH QUESTIONS (derived from this ledger; questions, not facts):
  - Q-76a85ec807 [MISSING_PROOF, OPEN] COMPOSE (owner 2026-11-28, pure composition) CONSTRUCT for Thm 10.6 of T66 (theory/T66-compression-by-composition-algebras-2026-11-28.md section 10): a family of computations that is hierarchy-hard in its direct form but
  - Q-57d9097b9e [MISSING_PROOF, PURSUED] COMPOSE (owner 2026-11-28, pure composition) VERIFY (independent, other model family than the proposer; derive and compute yourself, do not read the proposer's scripts first) theory/T66 sec.7-10. (1) Sec.9 Thm 9.3: the i
  - Q-13aa491b30 [MISSING_PROOF, PURSUED] COMPOSE (owner 2026-11-28, pure composition) Combine these mathematical mechanisms: [mech:rank-product-bound-for-entrywise-hadamard-product-of-matrice] rank-product bound for entrywise (Hadamard) product of matrices: ran
  - Q-65a7d49a7a [MISSING_PROOF, OPEN] BINGO2-C (owner 2026-11-28) AMPLIFICATION OF THM 6.2: unipotent filtration/lower central series of the group generated by F; tensor and recursive composition of (F,g) pairs with index r1*r2; quantify when index stays pol
  - Q-96e2ebbfb6 [MISSING_PROOF, OPEN] BINGO2-B (owner 2026-11-28) CROSS-GRAPH CONSTRUCTION SEARCH: search the research graph (T4/SOSA, T38, T52, T55/T60, S0127/S0096 rank compression + dominance counting + component folding, matroid elimination, ocean/phase-
STOPPED BRANCHES (no new information after a bounded escalation; reopen only under the stated condition):
  - RECON-REMAINDER Case E (owner 2026-11-23, target (8)): recover proofs left unextracted in FINAL outputs (research R*.json, proofbook FINAL entries); list statem -> reopen if: None
  - RECON-REMAINDER Route G (owner 2026-11-23, target (8)): PIT, GCT, permanent/determinant, algebraic natural proofs, Williams-type transfers, algebraic vs Boolean -> reopen if: A source-checked polynomial-size conversion preserving the Boolean-cube identity predicate, together with a transfer theorem matching its ex
  - CLOSURE (owner 2026-11-26) O*-CE: Core obligation O* of route M (results/PNP-001-2026-11-26/closure/PNP-001-PROOF-CLOSURE-REPORT.md (FruitStack-Eval branch cc/p -> reopen if: None
  - COMPRESS-D (owner 2026-11-28) TIME-BOXED EXCESS QUESTION (subordinate): does f(J)=2r(J)-|J|>=0 with unique S(x) force e* >= c*s for circuit-evaluation systems?  -> reopen if: Obtain exact definitions of J, r(J), S(x), e*, s and a circuit-specific derivation of a surplus-to-overlap bound strong enough to apply S000
NEXT PROOF GAP: Prove or refute this open assumption: 18308  (a verified step rests on it: proving it turns a conditional result into a proved one)