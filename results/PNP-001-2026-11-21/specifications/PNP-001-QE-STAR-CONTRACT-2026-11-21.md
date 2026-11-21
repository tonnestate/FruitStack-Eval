# PNP-001 - Final-stage proof reconstruction and QE* research contract (owner 2026-11-21, supersedes the oracle-elimination contract's
# priority; that contract's sections A-D are reused as background)
Authoritative text: the owner's message of 2026-11-21 ("FINAL-STAGE PROOF RECONSTRUCTION AND QE* RESEARCH CONTRACT", sections 0-12).

## Recovered state (director search 2026-11-21, BEFORE any new research)
- FruitStack-Eval cc/pnp001-results-20261118 @ 74931ae: "proof book as of 2026-11-21 06:50" - predates QE*; contains no QE* material.
- Local QE* material: ONLY /root/contracts/PNP-001-STREAMING-LAMBDA-S-CHECK-2026-11-21.md (Lambda_S corrected, Satz A/B, corollary,
  Lemma 1/2, QE* and QE(2,3) recorded as CONJECTURES, open property P) and proof state Q-156fa9c912 (S0009-S0013 each SURVIVED one
  independent review by R1094; G0005 = property P; S0021 affine-updates lemma CLAIMED with scope corrections G0006/G0007).
- In the owner's own source text QE* is "Eigenschaft"/conjecture and QE(2,3) is explicitly "Vermutung, unbewiesen"; Lemma 1 and Lemma 2
  prove that counting and information/cell-probe arguments cannot give it. NO complete proof of QE* exists locally.
- The "five final criticisms" (5.1 time-dependent encoding, 5.2 unrolling CC(f) <= G+D, 5.3 N^2/(R log N), 5.4 amortised vs worst case,
  5.5 oracle locality) exist only in the owner's external chat; locally they are known only through the contract text.
- Unrolling (STATE-RECODING-BOUNDS-CHECK, "Frage 1 focus"): a width-S one-pass algorithm unrolls to a circuit of online cut-width <= S.

## Decisive framing facts (director, elementary; to be independently verified)
F-1 QE* (uniform, poly(s) space and update time) implies P != NP by MMW Thm 1.3; it is therefore at least as hard as P != NP.
F-2 QE* relativises FALSELY: relative to an oracle B with P^B = PH^B the MMW algorithm runs with poly(s) space/update time, so any proof
    of QE* must be non-relativising (the owner's oracle counter-check, made exact).
F-3 Non-uniform Lambda_S version: if NP subset of P/poly then PH subset of P/poly, so the O~(s)-bit Sigma_3^A queries (A in PH) have
    poly(s)-size circuits and Lambda_S-updates of size poly(s) exist; hence the non-uniform QE* implies NP not subset of P/poly.

## Required output (owner parts I-V) - REPORT.md
I recovered latest proof (statements proved / proposed / refuted, with sources above; say explicitly that no complete proof exists if so)
II formal corrections (streaming model, future equivalence for SEARCH semantics, representation classes incl. redundant refinements,
   transition cost, universal target over ALL exponent pairs)
III audit of each inference incl. 5.1-5.5 and the oracle-locality test; Lemma B (representation completeness) and Lemma E (resource
   transfer to worst-case uniform update time) treated as separate obligations
IV strongest genuinely established result with complete proof, or decisive counterexample, or the smallest precise missing lemma
V implication chain with labels PUBLISHED THEOREM / INDEPENDENTLY PROVED / REFUTED / OPEN; never PROVED unless every premise is.
Sources: local texts listed in /root/contracts/PNP-001-ORACLE-ELIMINATION-CONTRACT-2026-11-21.md. Sharma-Velusamy (ESA 2026) is NOT
local: mark claims about it "not source-checked".

## Result 2026-11-21: OPEN (report theory/oracle-elimination/QE-STAR-REPORT.md with binding errata; review QE-STAR-REVIEW.md).
Director correction: F-3 as stated in this contract is right, but my reading "nonuniform QE* does not imply P != NP" was wrong - it does.
