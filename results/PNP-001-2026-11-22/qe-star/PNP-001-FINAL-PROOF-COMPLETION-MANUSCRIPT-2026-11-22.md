# PNP-001 — FINAL PROOF COMPLETION AND MANUSCRIPT INTEGRATION (owner contract, 2026-11-22 ~14:20)

Recorded by Claude (PI), condensed with all requirements kept.

**Mission.** Complete the existing programme on the route:

Universal Embedding → representation-independent computation lower bound → QE* → MMW19.

- No new general programme.
- No re-proofs of completed results.
- No finite experiments counted as asymptotic progress.

## Sources
- Manuscript `PNP-001_Research_Manuscript_v0.24(2).docx` (v0.24, 2026-11-20). Needed from it:
  - Thm 4 (two-value criterion)
  - Thm 16 (matroid port)
  - Thm 30 (exact kernel-basis width)
  - Thm 44 (PC degree)
  - Prop 45 / Cor 46 (circuit unfolding, formula/protocol transfer)
  - Prop 47 (raw kernel-width ceiling)
  - Sec. 4, 8, 9, 10, 11 and 12

  NOT on the VPS as of 14:20. Owner upload needed. First check whether v0.25 or later already exists; never overwrite a newer version.
- Paper basis_blowup v4: Thm 4.1, Lemma 5.2, Prop 5.3, Thm 5.4, Thm 6.1, Cor 6.2, Rem 6.4, Prop 6.5.
  - Copy: /root/fruits/research/PNP-001/theory/basis-blowup/.
  - Lean files WStar.lean and WStarLower.lean are in FruitStack-Eval results/PNP-001-2026-11-19/lean/. Their SHA-256 values match the paper.
- FruitStack-Eval `cc/pnp001-results-20261118`, last commit ec65e1b; PNP-001-research; live Q-156fa9c912; results/PNP-001-2026-11-22/qe-star/.

## Obligations
1. **Exact MMW19 Thm 1.3 hypotheses**, from the publication. Write QE* in a sufficient form.
2. **Frozen inventory of established theorems.** For each, record:
   1. statement
   2. domain
   3. quantifiers
   4. field restrictions
   5. representation restrictions
   6. proof location
   7. independent verification
   8. Lean status
   9. counterexamples
   10. whether it is used in the final chain
3. **Representation completeness.** For every admissible machine (q_t, U_t, D), construct G_{m,s}, K_{m,s}, B_A and H_{B_A}.
   - Explicit space and coordinates; exact Search-MCSP semantics.
   - No linearity assumption; nonlinear and time-dependent recodings, redundancy, sharing, noncanonical witnesses and decoder work all included.
   - The construction's own cost is counted.
   - Not circular. Otherwise: a counterexample and the missing property.
4. **R, L and E** for K_{m,s}. Then G_{m,s}[K_d] ⊆ H_{B_A} and an explicit infinite-family width lower bound. No complexity conclusion at this stage.
5. **Width-to-computation.** tw(H_{B_A}) ≤ f(S,U,m,s) derived, then d(tw(G)+1)−1 ≤ tw(H) ≤ f contradicts every MMW-prohibited regime.
   - Count real computation.
   - DAG fan-out and sharing.
   - Arbitrary representations.
   - Decoder cost.
   - Search and totality.
   - Asymptotic, with the full quantifier order.
6. **Falsification against our own control examples:**
   - (A) K_n: width 2n−1 with constant Resolution. Name the extra Search-MCSP premise.
   - (B) the same function with a different computation graph or encoding.
   - (C) stronger proof systems (PC, CP, roABP-IPS and above).
   - (D) all retractions: distinguishability, prefix tests, affine fibres, comm-rank, update-gate complexity, circuit-to-formula, deferred computation.
7. **Oracle audit** per lemma: the ordinary model versus the published oracle construction. Name the differing premise and prove that the distinction suffices.
8. **QE* and P≠NP.** Only after 1–7, as one uninterrupted argument:

   Representation theorem ⇒ embedding ⇒ unavoidable update computation ⇒ QE* ⇒ P≠NP.
9. **Lean**, separately:
   - (1) Thm 4.1
   - (2) the Hall selection
   - (3) Thm 5.4 as a subgraph embedding
   - (4) arbitrary fields
   - (5) the exact match with Cor 6.2

   Reproduce the pinned F3 build (Lean 4.35.0, Mathlib v4.35.0). Check faithfulness, `#print axioms`, no sorry, admit or axioms, and an independent kernel compile.
10. **Roles:** constructor, critic, counterexample investigator, Lean verifier, source auditor. Different sessions and model families. The critic attacks the whole separation. Majority votes are not evidence.
11. **Manuscript successor to v0.24.** Find v0.25 or later first. Never claim the separation unless every gate is passed.

## Deliverables
In the PNP-001 structure, pushed to the existing branches:
1. PNP-001-COMPLETE-PROOF-DEPENDENCIES.md
2. PNP-001-REPRESENTATION-TRANSFER.md
3. PNP-001-WIDTH-TO-COMPUTATION.md
4. PNP-001-QESTAR-AND-MMW-AUDIT.md
5. PNP-001-INDEPENDENT-MATHEMATICAL-REVIEW.md
6. PNP-001-FORMAL-VERIFICATION-REPORT.md
7. the revised manuscript
8. the proof book, append-only

No production or orchestration changes. No CI.

## Acceptance gate
A P≠NP claim needs every point of section 15 of the owner text:
- a precise target
- all intermediate theorems proved
- a representation theorem for the full model
- sufficient asymptotic strength
- every MMW hypothesis met
- the oracle check passed
- the counterexamples survived
- no unresolved material gap in review
- complete reproducible reasoning in the manuscript

Otherwise: the strongest valid theorem plus the first missing implication.
