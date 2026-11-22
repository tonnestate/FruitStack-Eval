# PNP-001 — QE* FINAL PROOF ATTEMPT (owner contract, 2026-11-22 ~13:35)

Recorded by Claude (PI) from the owner's chat message. The full text is condensed here with all requirements kept.
The owner also said: "Wir brauchen gleich noch einen Slot" (one extra research slot for this contract).

**Objective.** Prove P != NP unconditionally. Route:
1. Prove QE*.
2. Apply McKay–Murray–Williams, STOC 2019, Theorem 1.3.
Continue the existing research. Do not restart it, duplicate it, or turn it into a broad campaign.

## 1. Starting point
- Proof state: live desk proofstate `Q-156fa9c912` and live `proofbook.jsonl`.
  - The GitHub snapshot is `tonnestate/PNP-001-research` main. This is the repo created by mistake on 2026-11-22 and it is older.
  - Compare the two before deciding gaps. Never overwrite live evidence with an older snapshot.
- Contracts: `tonnestate/FruitStack-Eval` branch `cc/pnp001-results-20261118`, `results/PNP-001-2026-11-21/specifications/`:
  - QE-STAR
  - ORACLE-ELIMINATION
  - LEMMA-M-EXPERIMENT
  - STATE-RECODING-BOUNDS-CHECK
  - K1-STREAMING-TO-FORMULA
- VPS reports: `/root/fruits/research/PNP-001/theory/oracle-elimination/`. Expected files:
  - QE-STAR-REPORT.md
  - QE-STAR-REVIEW.md
  - QE-STAR-CANDIDATE-FIRST-FALSE-LINE.md
  - EGC-001-SIMULATION.md
  - other related reports

  Record any file that is missing. Never reconstruct missing evidence from memory.

## 2. Target
- Theorem: MMW19 Thm 1.3, taken from the primary source. Record every requirement exactly:
  - s(n)
  - A in PH
  - input representation
  - search semantics
  - uniformity
  - workspace
  - update time
  - all quantifiers
- QE*: for an admissible time-constructible s(n) >= n and an admissible A in PH, no deterministic one-pass streaming algorithm solves exact total Search-MCSP with poly workspace and poly worst-case update time, in the model of the published theorem.
  - The bound must hold for every fixed polynomial resource bound.
- NO weakening to any of the following:
  - promise versions
  - amortised update time
  - canonical encodings
  - affine or low-degree updates
  - Stream-Merge only
  - finite examples
  - an easier oracle problem

  The only exception: a different published theorem whose full hypotheses are established first.

## 3. Work backwards
The dependency chain:

P!=NP ← MMW Thm 1.3 ← QE* ← universal update lower bound ← invariant ← proved lemmas

For each implication, record:
- the statement
- its quantifiers and model
- the proof or citation
- its dependencies
- its independent verification status
- the first unresolved inference

First goal: the SMALLEST genuinely missing lemma.

## 4. Priority A — G0004
- Find an update-computation lower bound for F_t(q_t,b)=q_{t+1} that holds under EVERY poly-workspace representation.
- The bound must cover:
  - nonlinear and time-dependent encodings
  - redundancy
  - shared computation and fan-out
  - deferred and decoder work
  - alternative witnesses
  - algorithms without explicit candidate sets
  - worst-case versus amortised time
  - recurrent computation
- Keep the cost of maintaining a state apart from the information capacity of that state.
- Fallback: the strongest rigorous restricted theorem, together with exactly what a generalisation needs.

## 5. Priority B — G0005
For an invariant I, prove the following:
- (A) every ordinary algorithm within the bounds is constrained by I;
- (B) Search-MCSP violates that constraint;
- (C) the argument does NOT exclude the MMW oracle construction.

Name the exact operation where an oracle gate breaks the argument: a premise, an inequality, or a simulation failure. The word "nonrelativising" alone is not an answer.

Check the result against the literature on magnification and locality barriers.

## 6. Priority C — repair the failed implications
Items to check:
- C5 live/dead prefixes
- Lemma M and its domain
- Lambda_S cost model
- the affine bounds and their fields
- comm-matrix rank
- Myhill–Nerode
- time-dependent recoding
- the step from state information to gate complexity
- the oracle-locality countercheck
- stale SURVIVED_REVIEW entries

For each failed inference, give either the smallest counterexample or a corrected theorem with a proof. Do not repeat a false lemma under a new name.

## 7. Priority D — transfer
- Sources:
  - CJW20 Thm 1.6
  - MMW19 Thm 1.3 and 1.4
  - R-MCSP and K1
- Question: do the update circuits of the exact MMW construction have a structure that transfers to De Morgan formulas? This is the same as ledger Q-5d167697b4.
- Chain: NP ⊆ P/poly ⟹ small MMW-derived circuits ⟹ small formulas ⟹ contradiction.
- Check all exponents and uniformity conditions.
- Keep this route separate from QE*.

## 8. Adversarial tests for every candidate
- oracle
- representation
- sharing
- decoder
- quantifier
- model
- smallest counterexample

Authors and critics must be in separate sessions and from separate model families. Use the PhysalisMe/CherryMe/Lean conventions.

## 9. Rules
- Mathematics only.
- No service, routing, orchestration or production changes.
- Do not interrupt running research.
- No redundant programmes.
- No CI.
- Keep all failures and evidence.
- Record the exact status of every assertion.
- Never present a conditional result as unconditional.
- Never claim P!=NP before every step is independently verified.

## 10. Deliverables
Write these to `/root/fruits/research/PNP-001/theory/oracle-elimination/`:
- A. QE-STAR-RECONSTRUCTION.md
- B. QE-STAR-PROOF-ATTEMPT.md
- C. QE-STAR-INDEPENDENT-REVIEW.md
- D. QE-STAR-TRANSFER-AUDIT.md
- E. updated Q-156fa9c912 and related questions (append-only)

Then push to the existing repos and branches and report the commit hashes.

## 11. Acceptance
Exactly one of the following outcomes:
- **PROVED**: every lemma and transfer independently checked.
- **REFUTED**: a counterexample, plus the strongest corrected theorem.
- **OPEN**: the smallest remaining lemma, with everything else proved or cited.

No percentages. No consensus scores.
