# PNP-001 — UNIVERSAL EMBEDDING TO QE* TRANSFER (owner contract, 2026-11-22 ~13:45)

Recorded by Claude (PI) from the owner's chat message, condensed with all requirements kept.
Owner: "Wir haben möglicherweise noch einen Weg".

## Source
- Paper: Björn Tonn, "Every Basis Sees the Blow-Up", v4.0, 2026-11-22, DOI 10.5281/zenodo.24438918.
  - The owner's PDF is authoritative.
  - Copy: /root/fruits/research/PNP-001/theory/basis-blowup/basis_blowup-v4.0.pdf (text in .txt).
- Starting instruments:
  - Thm 4.1 (abstract embedding under R/L/E)
  - Thm 5.4 (colouring kernel: G[K2] ⊆ H_B for every field and every spanning family)
  - Cor 6.2 (min_B tw(H_B) = 2tw(G)+1)
- Limits stated in the paper itself:
  - Remark 6.4: the result is a parameter statement, not a running-time lower bound.
  - Prop 6.5: K_n has overlap tw 2n−1 but constant-size Resolution refutations.
  - Lean covers only part of the paper, over F3 (WStar.lean, WStarLower.lean). Thm 4.1 and Thm 5.4 as subgraph statements are not formalised.
- Never extend the results silently to nonlinear encodings or to arbitrary computational models.

## Hypothesis
Universal embedding → unavoidable computational structure → QE* → P≠NP.

Only the first arrow is established, and only in the kernel model. The second arrow is the target. The third uses MMW19 Thm 1.3 with its exact hypotheses.

## Stages
- **A. Construction**, from exact Search-MCSP^A[s] with N = 2^m and a machine (q_t, U_t, D):
  - a graph family G_{m,s}
  - a space K_{m,s} over an explicit field
  - coordinate blocks that correspond to genuine dependencies of the computation
  - a map from admissible streaming representations to spanning families
  - a quantitative link between H_B and the actual update work

  A state representation is NOT automatically a basis. Either prove representation completeness for all algorithms, or state the exact class of algorithms covered. A linear or affine result stays restricted.
- **B. Conditions.** Check (R), (L) and (E) separately, each by proof or explicit counterexample.
  - Compute rank π_X for the exact space, not from counts.
  - Only then apply Thm 4.1 to get G_{m,s}[K_d] ⊆ H_B and the width bound.
  - Modified encodings only with a rigorous justification.
- **C. Width-to-work theorem.** This is the central task.
  - Prove a worst-case update-time bound for exact Search-MCSP streaming machines with workspace S and update time T. It must exclude every polynomial T at polynomial S, in the full MMW regime.
  - Do not presume an exponential dependence on treewidth.
  - The proof must cover: nonlinear and time-dependent encodings, redundancy, fan-out and sharing, noncanonical witnesses, deferred and decoder work, all deterministic one-pass algorithms, and the exact time convention of the published theorem.
  - It must name the property of Search-MCSP that defeats the easy high-width examples of Prop 6.5.
- **D. Oracle-locality test** for every width-to-work lemma, mandatory before any progress claim:
  - ordinary model: does the lemma give the bound?
  - oracle model: does it falsely exclude the efficient MMW oracle construction?
  - which premise fails when the oracle operation is admitted?
- **E. QE* and MMW.** State the strongest established theorem with its quantifiers. Take the polynomial quantification exactly from MMW, then check each premise. A restricted result never gets the general MMW conclusion.

## Verification
Independent proof and criticism roles, from different sessions and different model families. The critic checks:
1. a streaming representation falsely identified with a basis;
2. failure of R, L or E;
3. hidden reuse of the colouring-kernel structure;
4. complexity not preserved by the encoding;
5. width turned into gate count without support;
6. counterexamples: complete graphs, easy satisfiable families, affine images, alternative encodings;
7. oracle-locality failure;
8. quantifiers too weak for MMW.

Finite computation is for counterexamples only. Use Lean where feasible, with a check that the formal statement is faithful.

## Deliverable
UNIVERSAL-EMBEDDING-QESTAR-TRANSFER-REPORT.md, sections A–H:
- A. construction
- B. R/L/E audit
- C. width-to-work theorem
- D. representation audit
- E. oracle audit
- F. MMW transfer
- G. review
- H. proof-state updates

Push to the existing repos with commit hashes. Never overwrite live data with stale snapshots.

## Acceptance
Exactly one of:
- PROVED
- REFUTED, with the smallest invalid implication
- OPEN, with the strongest established theorem and one precise remaining obligation

No inference from agent agreement, finite tests or lemma counts. Do not redesign the strategy, do not substitute a generic treewidth argument, no broad search.
