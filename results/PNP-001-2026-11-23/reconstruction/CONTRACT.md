# PNP-001: existing-proof reconstruction and cross-theorem closure (owner assignment, 2026-11-23)

Recorded by Claude (PI) from the owner's chat message. The text is condensed; every requirement is kept.
Owner's words: "Repariere das proofbook und erkläre mir warum die G0001-G0040 nicht vollständig sind - Prio 0 Ziel (8)".
Priority: CRITICAL. Mode: evidence first; reconstruct, then compose, then verify.

## Mission
Hypothesis H: the corpus already contains a complete route to P != NP, possibly spread over several directions,
representations and sessions.
- Do not assume a reported gap is open before every existing proof, correction, transfer and reformulation has been checked.
- Do not infer an implication from apparent compatibility; every implication must be proved.
- Goal: the strongest complete proof chain supported by the existing evidence, not more isolated results.

## Sources
FruitStack-Eval, branch cc/pnp001-results-20261118, refreshed from snapshot 1d4eb92664ba6be0a6a98cceb29b842b47b5a41a.
Record the SHA used for every result.

Raw files, read in full (the LESBAR summaries are not substitutes):
- the STAGING and LIVE proofbook jsonl;
- all 112 proofstates in qe-star/proofstate-live.

Documents:
- manuscript v0.24, synthesis v0.25, syntheses v0.3, v0.4 and v0.5;
- basis-overlap paper v4.0;
- WStar.lean and WStarLower.lean;
- ACC0 level 3 and Theorem 12;
- matchgate and holographic results;
- Reuse-MCSP;
- the streaming and QE* reconstructions;
- the transfer-audit inventory;
- perfect matching and structured proof systems;
- K8/K9/K10 bridges and proof-chain audits;
- range avoidance and constructive refuters;
- algebraic complexity, permanent/determinant and GCT;
- local VPS artifacts referenced by the ledger.

## Canonical index (per result)
1. Statement.
2. Quantifiers and hypotheses.
3. Objects and domains.
4. Field characteristic.
5. Input family.
6. Model.
7. Resource and bound.
8. Proof location.
9. Claim ID and equivalent IDs.
10. Reviews, linked to the exact statement.
11. Formal status.
12. Corrections, refutations and retractions.
13. What it implies.
14. What it depends on.

## Known inconsistencies, resolve first
- A: Q-e575463471 S0010/S0011 are the same false window bound (refuted by weights 1,1,1,1 and sums {1,2}). Trace its
  dependents and keep the Sperner repair S0033 with its domain.
- B: Q-156fa9c912 S0037 (resource transfer) versus a later review of an algebraic fibre-counting claim under the same ID.
- C: the inclusion-exclusion identity is a PROOF_STEP (seq 51), but a later summary still lists it as a gap. Separate
  "proof present", "formal check absent" and "implication missing" throughout.
- D: MMW19 Thm 1.2, 1.3 and 1.4 (all conclusions). See seq 9652-9656, 11387 and 11531. The TC0 consequence versus the
  NP not in P/poly transfer; decide from the primary text.
- E: FINAL outputs may contain unextracted proofs; recover them.

## Dependency graph
Nodes:
- theorem, lemma, formal verification, computational certificate;
- published transfer, representation transformation, lower bound;
- conditional, counterexample, retraction, missing obligation.

Edges: IMPLIES, EQUIVALENT_TO, SPECIAL_CASE_OF, GENERALISES, TRANSFORMS_TO, DEPENDS_ON, CONTRADICTS, REFUTES, REPLACES,
VERIFIED_BY.

Every implication edge needs a derivation or an exact citation; no keyword edges. The 223 CONNECTION events are a discovery
index only.

## Routes, worked backwards from separation theorems
- A: streaming Search-MCSP, MMW Thm 1.3. A state-count bound is not an update-time bound.
- B: general MCSP circuit bounds (MMW, Oliveira-Pich-Santhanam), N polylog N regimes.
- C: formula bounds plus reuse simulations plus the R-MCSP theorem.
- D: constructive refuters and range avoidance (efficiency, class, uniformity, all input lengths).
- E: algebraic proof complexity (Thm 12, Thm 14, Lemma 15, Thm 16, NS/PC degree, overlap theorem, IPS). There is no general
  IPS or circuit hardness without a semantic bridge.
- F: matching, structured circuits, d-SDNNF, lifting, tensors, holographic methods. Prism graphs and easy high-width
  instances are mandatory negative controls.
- G: PIT, GCT, permanent/determinant, algebraic natural proofs, Williams-type transfers. Keep algebraic and Boolean apart.

For each candidate chain, check:
1. output matches input;
2. field, representation and uniformity;
3. quantifier order;
4. exact composed bounds;
5. parameter ranges;
6. conversion costs;
7. known counterexamples;
8. verdict.

## Verdict on H
One of:
- H-CONFIRMED;
- H-CONFIRMED-BY-COMPOSITION;
- H-NOT-ESTABLISHED, naming the first missing implication for each chain;
- H-CONTRADICTED-FOR-A-SPECIFIC-CHAIN.

Absence of a found chain does not disprove H.

## Output
A research-audit directory in FruitStack-Eval with:
- A: theorem register;
- B: machine-readable graph;
- C: closure report;
- D: recovered proofs;
- E: minimal unresolved implications;
- F: final determination.

Every claim cites path, commit, sequence number and question/step ID.

## Restrictions
- No new broad campaign; no hundreds of questions; no repeated experiments.
- No model quota for exploration.
- Do not alter or restart the research organisation or services.
- Do not overwrite original proofbook evidence.
- No CI.
- Local parsing and existing formal tools only.
- Commit only the new audit artifacts to the research branch.
- Internal agreement is not external peer review.

## Acceptance
1. Both proofbooks examined in full.
2. All 112 proofstates indexed.
3. Refuted and retracted claims excluded.
4. Duplicate IDs separated.
5. All routes tested.
6. The strongest chain written out.
7. Each gap checked against all fronts.
8. Reproducible trail.
