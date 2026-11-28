PROOF LEDGER of this problem (kept across missions; 18368 entries from 5977 missions). It records what is PROVED, what is only observed and what is open. RULE: a statement that is not PROVED or CITED here must never be used as an established premise. You may use it as an explicitly named OPEN ASSUMPTION - your result is then conditional on it.
PROVED (the proof tool supported them over their whole domain):
  - T6 sharpening: lambda=(7/t)(log t-log log t+u): Q_t -> 56e^u+c locally uniformly (factor (L+u)/log t ->1), Hurwitz gives lambda_t=(7/t)(log t-loglog t+log(c/56)+i pi+o(1)); |lambda_t|=O(log t/t), dist to [0,1] <= (7pi+o(1))/t. Targeted Newton check at t=1e4,1e
  - Row 18299 refutation withdrawn: SEL:(C,x)->(g_1..g_s) in FL (write-only output) iff P=L. (=>) g_s is CVP, P-complete under logspace reductions; (<=) P=L gives CVP in L, loop over j writing each bit, only the counter stored. Universal evaluator only; fixed fami
  - Row 11359 D1 one-step drop repaired by hand: size(C|x_i=b)<=s-1 for g non-output, or output with internal y (complement tables), or s>=2; sole exception s=1 with f| in {true, not x_j} in the Lean model (free wires: inputs and constant false); no exception with
  - Row 16768 seed claim: 'seed >= gamma' is not a general PRG theorem. SEED-FLOOR (17150) gives log2 M >= log2(1/delta)-1 for required error delta; delta=2^{-r-2} comes from a 2^r-term decomposition. With image A=Im(b_K) the loss is |A| (or the number q of residu
  - CJW20/D6 recalculated: per gate p^2 d^2/2 <= 2N^{2e/5-2eta}; union over S<=N^{1+e} gates gives 2N^{1+7e/5-2eta} (owner value confirmed; row 16839/16840 already hold the counterexample and D6'). Narrow threshold D <= sqrt(2B/S)/p => D* = N^{(1-b)/2-eta-7e/10}. 
  - T44 re-derived by hand (S1,S3,S4,C1-C4); table arithmetic checked (360+360+180=900; 8190+54180=62370); enumeration counts stored not recomputed; nothing stale from e*/T6/T29/T52 corrections.
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
  - For every finite transition system with injective S-bit state encoding, the prefix-trie construction extends the transition to a total Boolean map with fan-in-two AND/NOT size O(S+T+H), where T is the changed-state prefix-trie size and H is the sum of Hamming 
  - For support A of size t under the same product restriction, if t*((1+p)/2)^m is small, Markov's inequality gives a small upper bound on the probability that any satisfying point survives. This may support a YES-side elimination bound only if the restriction al
  - For fixed c>=1, if every cofactor after fixing k coordinates has circuit size below (m-k)^c, this reconstruction method preserves the original threshold only when 2^k((m-k)^c)+3(2^k-1)+k < m^c. Determine whether this inequality admits a growing k in the AF/P1/
  - For admissible streaming machine families in which the two transition maps commute on reachable states, fixed AC0-uniform collision families can be obtained from short words with equal symbol counts; the two-letter pair 01 and 10 is the first case.
  - The actual CLOSURE-B restriction may admit a two-stage representation of each relevant leaf-survival event, with independent within-occurrence stages whose probabilities yield the squared terms in P2'.
  - For EXT_{n,s}, the semantic identity R_{p b}(z')=R_p(bz') holds for the union of truth tables of all size-at-most-s circuits, but a representation containing only the current residual function does not by itself specify a bounded-real-gate method for producing
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
  - None -> EXHAUSTED: TURN_LIMIT
  - None -> None
  - None -> EXHAUSTED: MODEL_SUPPLY_SILENT
  - None -> EXHAUSTED: TURN_LIMIT
NUMERICAL EVIDENCE on file: 3459 entries (finite cases; they prove nothing about all cases). Latest: None
OPEN RESEARCH QUESTIONS (derived from this ledger; questions, not facts):
  - Q-c7545bb864 [LIMITATION, OPEN] COST ACCOUNTING of the Koszul/idempotent masking (rows 18311-18312). Construct eta,D,E,h: O(m) ring operations. Apply h or D to a given omega: O(m) products. Verify: sum b_i f_i=E is a formal identity for every system an
  - Q-14b6e4c248 [MISSING_PROOF, OPEN] NORM: does the existence of a De Morgan circuit of size S for Gap-MCSP[N^beta] imply a circuit of size <= N^{1+eps} with W(C) <= N^{beta-2eta} (W from D6', seq 16840) for the same promise problem? Any candidate must fail
  - Q-1c841c90f7 [MISSING_PROOF, PURSUED] UNIFORM-QE (owner 2026-11-26) WITNESS-SENSITIVE SEARCH ONLY (supersedes Q-4c4127e83e). EXCLUDED - do not pursue: local many-one DECISION reductions to MCSP^A with s,t=M^{o(1)} for ANY oracle A, any uniformity, any gap ve
  - Q-7828a2a6e1 [MISSING_PROOF, PURSUED] CLOSURE-B (owner 2026-11-26) RESIDUAL R' - supersedes the D6 part of seq 16784. D6 is REFUTED (seq 16839, window-parity counterexample); use D6' (seq 16840) and the hypothesis D6'' (director/closure-intervention). Task 1
  - Q-47a55293d1 [MISSING_PROOF, PURSUED] CLOSURE-D (owner 2026-11-26) UNIFORM STATE COLLISIONS - supersedes seq 16783; no other D work. Read CJ1-CJ4 (director/closure-quant) first. Reduction (CJ2, done): it suffices to construct, for every admissible DETERMINIS
STOPPED BRANCHES (no new information after a bounded escalation; reopen only under the stated condition):
  - Q-2d7c6a77bf follow-up: can a non-prefix partition family, or weighted cut costs, beat the (N-1)+Lambda_pi bound of L-K1-PREFIX? Note: gates with P(u)=0 (consta -> reopen if: A non-prefix partition family or weighted cut cost is shown to be O(polylog(N)*s) on bounded-fan-out expander circuits, or a cross-family re
  - RECON-REMAINDER Case E (owner 2026-11-23, target (8)): recover proofs left unextracted in FINAL outputs (research R*.json, proofbook FINAL entries); list statem -> reopen if: None
  - RECON-REMAINDER Route G (owner 2026-11-23, target (8)): PIT, GCT, permanent/determinant, algebraic natural proofs, Williams-type transfers, algebraic vs Boolean -> reopen if: A source-checked polynomial-size conversion preserving the Boolean-cube identity predicate, together with a transfer theorem matching its ex
  - CLOSURE (owner 2026-11-26) O*-CE: Core obligation O* of route M (results/PNP-001-2026-11-26/closure/PNP-001-PROOF-CLOSURE-REPORT.md (FruitStack-Eval branch cc/p -> reopen if: None
NEXT PROOF GAP: Prove or refute this open assumption: 18308  (a verified step rests on it: proving it turns a conditional result into a proved one)