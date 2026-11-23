# PNP-001 reconstruction, slice 1 (2026-11-23)

This slice implements part of the owner contract `/root/contracts/PNP-001-EXISTING-PROOF-RECONSTRUCTION-2026-11-23.md`.

**Status: IN PROGRESS.** This slice covers the evidence repair and inconsistency cases A to D. The route analysis A to G and
the verdict on H are not done yet. **H is not determined.**

Sources:
- Staging proofbook, seq 0 to 11704, hash chain intact (11,701 entries, 0 breaks).
- 112 live proof states.
- Desk commits `4a64785` (gap status) and `43a550e` (model family).
- MMW19 primary PDF: people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf, fetched 2026-11-23, sha256 prefix `bc6d4178bac7aa09`.
  The agents cite `7077714b...` for the same URL; the two copies have not been reconciled.

## 1. Why G0001 to G0040 are "not complete"
The gap IDs are not obligations. Until 2026-11-23, the desk gave every `gap` text a new ID (`pnp_desk.py`, proof_state_update)
and listed every ID as an open obligation forever. Nothing ever set a gap to closed. Across 112 questions, 1,804 gap IDs exist
and none is CLOSED.

In `Q-156fa9c912`, G0001 to G0040 classify as follows:
- **31 NOTE:** comments, corrections or restatements of earlier gaps, mainly G0003, G0004 and G0006. For example, G0007,
  G0009, G0011, G0013, G0014, G0016 and G0018 all repeat "G0006 stays open for F_p, p >= 5".
- **4 OPEN:** real obligations:
  - G0001: update-time lower bound for the EXT representation;
  - G0005: property P;
  - G0012: universal MMW Thm 1.3 premise (QE*);
  - G0015: missing Lemma M.
- **4 CLOSING_SURVIVED_CLOSURE_UNCONFIRMED:** a closing step survived review, but no reviewer confirmed that it closes the
  gap. These are G0002 (S0103), G0003 (S0128, S0212), G0006 (S0024) and G0009 (S0372).
- **1 CLOSING_REFUTED:** G0004, whose closing step S0021 was refuted.
- **G0006 as stated is false:** G0039 notes the injective counterexample, and G0040 notes that the repaired form is an
  identity. The desk has no "withdrawn" state, so these notes can only reclassify G0006 by hand.

**Repair (`4a64785`):** a gap text naming existing gap IDs is now stored as `gap_note_on` and gets no new ID.
`proof_state_read` returns `open_obligations` with a status, plus `closed_obligations` and `gap_notes`.
CLOSED requires a closing step that has a cross-family review with `confirms_closure`, or a Lean FORMALLY_VERIFIED result.
No original entry was changed; the status is derived on read.

Across all 112 questions: 590 OPEN, 1,142 NOTE, 37 survived but closure unconfirmed, 29 closing step claimed, 6 closing
step refuted, 0 CLOSED.

## 2. Model-family defect (`43a550e`)
`lab_tools.model_family` treated every model key except claude-* as its own family. As a result, nemotron-3-ultra reviewing
nemotron-3.5-super counted as an independent cross-family review (K11 R3).

The family is now the leading name, so nemotron, claude, gpt, gemma, minimax and kimi are each one family. Step statuses
after the fix: 343 CLAIMED, 308 SURVIVED_REVIEW, 86 REFUTED, 5 DISPUTED. Only a few steps changed status.

The mechanical register (`register.py`) also flags 240 of the SURVIVED steps whose independent reviews never quote 40
consecutive characters of the statement. This is a misattribution warning, not a refutation.

## 3. Case A: Q-e575463471 S0010 and S0011
- S0010 and S0011 are the same statement, LEMMA S-P1-WIN, by nemotron-3.5-super-vl.
- S0011 was REFUTED by R1840 (claude-haiku, another family). Counterexample: a = (1,1,1,1) with window {1,2} gives 4 + 6 = 10
  assignments against the bound ceil(2/2)·C(4,2) = 6; independent run `cm-8536dc0f643548a8`.
- S0010 has the identical text, so the counterexample refutes it too. The desk still shows S0010 as CLAIMED: its only review
  was a nemotron SURVIVED by R1798, which no longer counts after the family fix. **S0010 must not be used as a premise.**
- The repair is S0033 (claude-haiku, CLAIMED): for every a_i in Z\{0} and every integer window [t, t+W-1], the count is at
  most W·C(k, floor(k/2)). The proof uses a sign flip and then Sperner on each value. It awaits a non-Claude review.
- Dependents of S0010 and S0011: no step in the register names S0010 or S0011 in its `closes` field or in a "repair of" phrase,
  apart from S0033.

## 4. Case B: Q-156fa9c912 S0037
- S0037 is the RESOURCE TRANSFER statement, recorded by director-owner. It says a uniform one-pass algorithm with space S and
  worst-case update U yields per-step circuits plus a decoder of size O(U·S) by tableau simulation.
- Its three positive reviews refer to three different statements:
  - **R1180** (claude-haiku) reviewed an image bound taken from APPROACH seq 8321, not S0037. R1180 retracted this itself
    (G0024), but only as a gap note, so the SURVIVED event still stands in the record.
  - **R1252** (claude-haiku) reviewed the well-definedness of pi_t, also a different claim.
  - **R1551** (nemotron-3-ultra) reviewed the tableau simulation of space S and update U, which is S0037 itself.
- **Result:** S0037 has exactly one valid review, R1551. The other two must not lend it status.

## 5. Case C: inclusion-exclusion, seq 51
- Seq 51 is a PROOF_STEP for #F = Σ_S (-1)^{|S|} N(S), counting assignments that falsify no clause.
- Seq 76 is the desk's automatic QUESTION "Close the proof gap (UNVERIFIED_STEP) ... derived in words only".
- Classification: the mathematical proof is present (standard inclusion-exclusion), the formal check is absent, and no
  implication is missing.
- The automatic UNVERIFIED_STEP questions mix these categories. They are to be read as "formal check absent", not as missing
  mathematics.

## 6. Case D: McKay, Murray and Williams 2019, Theorems 1.3 and 1.4 (primary text, verbatim)
- **Thm 1.3:** if there are a time-constructible s(n) >= n and A in PH such that search-MCSP^A[s(n)] is not solvable by a
  poly(s(n))-space streaming algorithm with poly(s(n)) update time, then P != NP.
- **Thm 1.4** has three bullets, for s(n) >= n and A in PH:
  1. if there is eps > 0 such that for all c >= 1, search-MCSP^A[2^{eps n/c}] on N = 2^n inputs has no N^{1+eps}-size,
     O(1/eps)-depth TC0 circuits, then NP is not in TC0;
  2. if search-MCSP^A[s(n)] has no circuits of N·poly(s(n)) size and O(log N) depth, then NP is not in NC1;
  3. if search-MCSP^A[s(n)] has no circuits of N·poly(s(n)) size and poly(s(n)) depth, then NP is not in P/poly.
- **Verdict:**
  - Seq 9652 and 9656 (R1421) read bullet 3 correctly.
  - Seq 11387 (R1809) is **wrong**: it calls Thm 1.4 "a TC0 result" from bullet 1 alone and dismisses the P/poly route.
  - Not settled by the theorem statement itself: whether the hypothesis is "infinitely often" or "almost everywhere". Seq
    9656 inferred "infinitely often" from the proof; the proof section still has to be checked.
- **Relevance to (8):** bullet 3 asks for a lower bound against circuits of depth at most poly(s(n)), which is weaker than a
  bound against circuits of any depth. Whether the "for every k" form of (8) meets bullet 3 exactly is part of route B. It
  depends on the search versus decision distinction, the oracle A, the quantifier and the threshold s(n) = n^c.
  **Not yet checked.**

## 7. Next slices
1. Case E: extract proofs from FINAL texts.
2. Routes A to G, each checked for matching objects, quantifiers, bounds and counterexamples.
3. Verdict on H.

Every step builds on `out/register-nodes.json`, `out/register-edges.json` and `out/ledger-proof-events.json`.
No model quota is used; the work is local parsing and reading.
