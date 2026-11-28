# PNP-001 - Deep mathematical research contract: Oracle Elimination, Nonlocality, and Exact Search-MCSP Streaming Lower Bounds
Owner assignment 2026-11-21 (authoritative text: the owner's message of 2026-11-21; this file is its working copy for agents).
Status: research assignment - no claimed separation of complexity classes.

## Mission (one question)
How to obtain a lower-bound argument that is genuinely sensitive to the computational power hidden in Stream-Merge's oracle while remaining
valid against EVERY ordinary deterministic one-pass algorithm admitted by MMW Thm 1.3. Distinguish (1) hardness of the particular
Stream-Merge oracle, (2) hardness of alternative state representations, (3) a universal lower bound against every algorithm of the exact
MMW model - only (3), under the exact hypotheses of the magnification theorem, can support a separation. A valid negative result or a
precisely identified unproved lemma beats an unsupported positive claim. No new representation-specific hardness measure without proven
relevance to general computation.

## Local primary sources (read these, quote exact statements with line numbers)
- MMW STOC 2019: /root/fruits/research/PNP-001/literature/sources/mmw19/paper.txt - Sections 2.1, 4, 5; Thms 1.2, 1.3, 4.1.
- Chen-Hirahara-Oliveira-Pich-Rajgopal-Santhanam, Beyond Natural Proofs (ITCS 2020 / JACM 2022): .../sources/chops-locality/ - Thm 2.
- Atserias-Mueller 2025: .../sources/arXiv-2503.24061/paper.txt - Sections 3, 5, distinguishers, Thm 11 (Thm 27 parameters).
- Cheraghchi-Hirahara-Myrisiotis-Yoshida STACS 2021: .../sources/eccc-TR20-103/ - Thms 1-3, 16, Lemma 17, Cor 18, Remark 19.
- Pich 2024 (Comput. Complexity), Localizability of the approximation method: .../sources/arXiv-2212.09285/paper.txt
- Chen-Jin-Santhanam-Williams 2024 (TheoretiCS), Constructive separations: .../sources/arXiv-2203.14379/paper.txt
Existing PNP-001 context to reuse (do not redo): /root/contracts/PNP-001-P2-DOSSIER-2026-11-21.md sections C, H, I, K, K-REV, L;
/root/contracts/PNP-001-STREAMING-LAMBDA-S-CHECK-2026-11-21.md (Lambda_S, Satz A/B, Lemma 1/2: MMW is the TOTAL version);
/root/contracts/STATE-RECODING-BOUNDS-CHECK-2026-11-21.md (unrolling: one-pass width-S algorithm = circuit of online cut-width S);
proof state of Q-156fa9c912 (streaming lane: FB2 space ceiling O(s log s), G0004 update-time obligation, G0005 property P).
Preserve XOR/Carry, GF(3), Nullstellensatz, roABP-IPS, kernel-width, matroid-port results; do not reopen refuted approaches without a new premise.

## Required content (report sections A-F)
A Exact theorem ledger: MMW Thms 1.2, 1.3, 4.1 with all parameters/quantifiers (s(n) >= n time-constructible, A in PH, poly(s) space AND
  poly(s) update time; meaning of the polynomial quantifiers; published statement vs any interpretation). Formal definitions: admissible
  truth table, Boolean / A-oracle circuit, valid output, valid "no circuit" report, deterministic one-pass streaming algorithm, workspace,
  worst-case update time, total time. Fix and state one admissible A in PH for the central investigation; never silently replace
  search-MCSP^A by ordinary search-MCSP.
B Oracle reconstruction: Stream-Merge (block length 100 s log s vs oracle interface 200 s log s, t(n) = 200 s(n) log s(n)), encoding,
  padding, output conventions, query complexity, how oracle outputs are computed in PH, role of A, last incomplete block, local time vs
  unit-cost oracle time. Compatible continuation space V(C,p,y) with the paper's indexing; canonical minimum circuit with tie-breaking or
  bottom. Answer: constraints implicit in C; prefix-consistency check; work of canonical witness selection; where E/A quantifiers enter;
  what is cheap only because of the oracle; which difficulties vanish under another state representation. A compact state is not a cheap
  transition; hardness of the canonical selector is not hardness of every streaming algorithm.
C Locality analysis (CHOPRS Thm 2 + Cheraghchi et al.): what "localizes" means, admitted oracle-gate classes, fan-in/depth/size/placement
  restrictions, why efficient oracle circuits invalidate transfers, what is NOT covered (not a universal impossibility theorem). Exact
  comparison with Cheraghchi et al. (threshold s(n), det vs randomized, decision vs search, ordinary vs oracle outputs, one-tape vs general
  streaming, query length, resources, parameter ranges) and the exact incompatibility that keeps it from the MMW consequence. Pich:
  whether approximation-polynomial / restriction / algebraic arguments are covered. Chen-Jin-Santhanam-Williams: counterexample to one
  algorithm vs refuter for a class vs constructive separation vs lower bound against all algorithms.
D Atserias-Mueller transfer: isolate the mechanism behind the apparent non-localisation (strongly explicit distinguishers, approximation
  /promise conditions, uniformity, magnification consequence, the non-relativising/non-localising part). Test transfer to EXACT online
  version-space maintenance preserving exactness, deterministic one-pass model, workspace/update bounds, oracle-circuit outputs,
  uniformity, all quantifiers. Either a proved transfer lemma or the first invalid implication.
E Proof-obligation ledger: per step - statement, assumptions, proof or counterexample, relevance to universal algorithms, oracle stress
  test, verification status. Main target (NOT a fact): for fixed admissible A in PH and s(n), no deterministic one-pass algorithm solves
  exact search-MCSP^A[s(n)] with poly(s) workspace and poly(s) worst-case update time. Bridge lemma requirements: arbitrary state,
  adaptive reorganisation, shared computation, reuse, non-canonical representatives, algorithms that never run Stream-Merge. A pure
  counting/information argument cannot suffice (MMW oracle algorithm maintains the information compactly) - a computational ingredient
  is mandatory. Nonlocality: a PROVED property ordinary poly-resource algorithms must satisfy but the oracle construction need not.
F Final outcome, exactly one: PROVED / REFUTED / OPEN (+ smallest missing lemma). Never classify P vs NP from an intermediate lemma.

## Mandatory tests for every candidate lower-bound mechanism L
Oracle stress test: A ordinary model - does L rule out the intended ordinary algorithm? B oracle model - would L also rule out MMW Thm 4.1
(then invalid/inapplicable)? C exact point of nonlocality - the premise/inference/inequality that fails with oracle gates (explicit; else OPEN).
Falsification F1 known oracle upper bound, F2 alternative representation, F3 model weakening (formulas, ROBPs, one-tape, bounded depth),
F4 quantifier mismatch (one exponent, finitely many lengths, restricted inputs, non-uniformity), F5 promise vs exact, F6 unjustified
hardness transfer from a subroutine, F7 finite counterexamples as asymptotic refutation. A failed check closes the claim unless repaired.
Status per claim: PROVED (complete derivation, valid hypotheses, independent verification) / REFUTED / OPEN. Agreement of several language
models is not verification. Finite computation is a sanity check only. No broad enumeration campaign.

## Execution (director)
Construction: Codex writes the report /root/fruits/research/PNP-001/theory/oracle-elimination/REPORT.md (English).
Criticism: an independent critic (separate model/session) receives statement, model, proof, cited theorems and quantifier derivations
and searches for counterexamples and missing reductions; result appended as REPORT-REVIEW.md. New lemmas are registered as CLAIMED steps
in the proof state of Q-156fa9c912 for independent session review and the Lean fidelity lane. No service restarts, no orchestration changes.
