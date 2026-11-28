# PNP-001 — FINAL WIDTH-TO-COMPUTATION TRANSFER (owner contract, 2026-11-22 ~14:10)

Recorded by Claude (PI), condensed with all requirements kept.

This contract sharpens /root/contracts/PNP-001-UNIVERSAL-EMBEDDING-QESTAR-TRANSFER-2026-11-22.md. It runs on the same questions (Q-d8b15fc303, Q-9bdbd025db, Q-0945f0e9cd), plus the addendum question listed in the ledger.

**Central question.** Can every polynomial-resource Search-MCSP streaming algorithm be turned into a sufficiently low-width representation of a linear space to which Thm 4.1 applies?
- If yes: give the transformation with exact bounds and derive the contradiction.
- If no: say precisely why it fails, and check whether a restriction specific to Search-MCSP gives a correct replacement.
- No further generic treewidth lower bounds.

## Tasks
- **A.** Recover s(m), A and the quantifiers from MMW Thm 1.3.
  - s(m) = m² is allowed only if it meets the theorem's requirements. Never fix a parameter that blocks the asymptotic conclusion.
  - Construct, for q_{t+1} = U_t(q_t, b_{t+1}):
    - G_{m,s} from the prefix and continuation structure;
    - K_{m,s}, whose coordinates are the computational dependencies;
    - a map from algorithm to spanning family B;
    - H_B, holding only the dependencies the algorithm must really compute.
  - This correspondence is the first obligation. Either it is representation-complete, or give a counterexample together with the minimal extra assumptions. Linear, affine, canonical or fixed-representation mappings do not establish QE*.
- **B.** Check R, L and E for the exact space. If all three hold, G_{m,s}[K_d] ⊆ H_B and the exact width bound follow. If one fails, give the smallest counterexample and the reason.
- **C.** Derive (not guess) an inequality tw(H_B) ≤ f(S,U,m,s). It must be small enough under polynomial resources to give an asymptotic contradiction.
  - Check whether an unavoidable dependence on N makes it too weak.
  - It must survive:
    - nonlinear and time-dependent recoding;
    - redundancy;
    - fan-out and sharing;
    - noncanonical witnesses;
    - deferred computation and decoder work;
    - different algorithms for the same relation;
    - every MMW exponent choice.
  - MANDATORY: apply the inequality to the K_n counterexample of Prop 6.5. If it predicts hardness from width alone, reject it. Then name and prove the extra property of Search-MCSP that excludes such easy cases.
- **D.** Prove 2tw(G_{m,s})+1 ≤ tw(H_B) ≤ f(S,U,m,s).
  - The lower bound on tw(G_{m,s}) must hold for an explicit asymptotic family.
  - The inequality must become impossible for large m under polynomial S and U, for ALL MMW resource bounds.
  - If the width bound is too weak, say so explicitly.
- **E.** Run three tests:
  - E1: how the bound applies to an ordinary algorithm;
  - E2: the published MMW oracle construction substituted into the same framework;
  - E3: the exact assumption or inequality that fails in E2.

  If E2 yields the same impossible bound, the argument is invalid.
- **F.** Check the MMW Thm 1.3 premises one by one:
  - s(m): range and time-constructibility
  - exact total Search-MCSP
  - A in PH
  - deterministic one-pass
  - uniformity
  - workspace
  - update time
  - quantifiers

  Only then conclude P≠NP.

## Roles
- constructor
- independent critic
- formal verifier (Lean, with independent build reproduction)
- evidence auditor (sources, artifacts, dependencies, ledger)

No changes to the orchestration. No CI. Finite experiments only reject or suggest.

## Stop condition
Stop this path at a decisive counterexample to a necessary implication. Do not weaken the target afterwards.

## Deliverable
PNP-001-UNIVERSAL-EMBEDDING-QESTAR-PROOF.md, with 10 parts:
1. definitions and sources
2. construction
3. R/L/E
4. the width-to-work theorem
5. its proof or a minimal counterexample
6. the asymptotic inequality
7. the oracle audit
8. the MMW implication
9. the verification results
10. the remaining obligation

Update the ledger append-only and push with the commit SHA.

## Verdict
Exactly one of PROVED, REFUTED or OPEN.
