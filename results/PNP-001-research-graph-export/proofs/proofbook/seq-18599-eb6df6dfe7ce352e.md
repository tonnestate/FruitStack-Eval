# Proofbook seq 18599 — CONNECTION

- key: `eb6df6dfe7ce352e`
- at: 1795864362.0557053
- mission: director/mechanism-extraction
- hash: `065c0b40d1240d0f2bed66a174f8d34eea42e613c2c62851951eabd402a3c12e` (prev `06b09b2877d0c6ce9fcb956ab9cda98e23aa834749affb219cd2aa906bf2970f`)
- graph nodes: PB:065c0b40d1240d0f2bed66a174f8d34eea42e613c2c62851951eabd402a3c12e
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)



## Full row (verbatim JSON)

```json
{
 "seq": 18599,
 "at": 1795864362.0557053,
 "problem": "p_vs_np",
 "mission": "director/mechanism-extraction",
 "key": "eb6df6dfe7ce352e",
 "kind": "CONNECTION",
 "about": [
  "mech:x16811-st2-independent-transfer-strengthened-author-claude-f"
 ],
 "bingo": {
  "record": "MECHANISM",
  "id": "mech:x16811-st2-independent-transfer-strengthened-author-claude-f",
  "name": "x16811 ST2 INDEPENDENT TRANSFER, STRENGTHENED (author Claude family; owner's ",
  "preconditions": "ST2 INDEPENDENT TRANSFER, STRENGTHENED (author Claude family; owner's sec. 9 argument with P = NP replaced by NP subset P/poly): let S be polylog-uniform AC0_d[2^{m^k}] with r CX rounds, uniformity time m^u.; Assume NP subset P/poly, so PH subset P/poly and Sigma_{d'} has circuits of size n^{c}.",
  "effect": "Induction: if every earlier answer has size <= m^{K_i}, hardwiring b and D_<j gives a circuit for X_j of size m^{K_j}, K_j = c*O(K_{j-1} + k + u), independent of b.; For b > K* = max_j K_j the answer 'a circuit of size m^{K_j} for X_j' is admissible in every round (Teacher only has to exist, no uniformity needed), so X_r has circuit complexity <= m^{K*} < m^b at every large N: S fails for all b > K*.; Hence: absolute protocol => NP notsubset P/poly (stronger than Thm 1.7's P != NP).",
  "limitations": "For b > K* = max_j K_j the answer 'a circuit of size m^{K_j} for X_j' is admissible in every round (Teacher only has to exist, no uniformity needed), so X_r has circuit complexity <= m^{K*} < m^b at every large N: S fails for all b > K*.",
  "correctness": "source status UNVERIFIED_STEP; PROOF_STEP seq 16811 (extraction preserves, never upgrades the status)",
  "representations": "padding, circuit",
  "interfaces": "padding, circuit, bound:m^k}, bound:m^u., bound:n^{c}",
  "provenance": "PROOF_STEP seq 16811 key 156a2ead9b31e165 mission director/closure-st",
  "basis": "EXTRACTED",
  "verification": "UNVERIFIED_STEP",
  "operations": [
   "padding",
   "circuit"
  ],
  "guarantees": [
   "Induction: if every earlier answer has size <= m^{K_i}, hardwiring b and D_<j gives a circuit for X_j of size m^{K_j}, K_j = c*O(K_{j-1} + k + u), independent of b.",
   "For b > K* = max_j K_j the answer 'a circuit of size m^{K_j} for X_j' is admissible in every round (Teacher only has to exist, no uniformity needed), so X_r has circuit complexity <= m^{K*} < m^b at every large N: S fails for all b > K*.",
   "Hence: absolute protocol => NP notsubset P/poly (stronger than Thm 1.7's P != NP)."
  ],
  "bounds": [
   "m^k}",
   "m^u.",
   "n^{c}",
   "size <= m^{K_i}",
   "m^{K_j}",
   "O(K_{j-1} + k + u)",
   "complexity <= m^{K*}",
   "m^b"
  ],
  "assumptions": [
   "ST2 INDEPENDENT TRANSFER, STRENGTHENED (author Claude family; owner's sec. 9 argument with P = NP replaced by NP subset P/poly): let S be polylog-uniform AC0_d[2^{m^k}] with r CX rounds, uniformity time m^u.",
   "Assume NP subset P/poly, so PH subset P/poly and Sigma_{d'} has circuits of size n^{c}."
  ]
 },
 "connection": "MECHANISM mech:x16811-st2-independent-transfer-strengthened-author-claude-f: Induction: if every earlier answer has size <= m^{K_i}, hardwiring b and D_<j gives a circuit for X_j of size m^{K_j}, K_j = c*O(K_{j-1} + k + u), independent of b.; For b > K* = max_j K_j the answer 'a circuit of size m^{K_j} for X_j' is admissible in every round (Teacher only has to exist, no unif",
 "origin": "director",
 "prev": "06b09b2877d0c6ce9fcb956ab9cda98e23aa834749affb219cd2aa906bf2970f",
 "hash": "065c0b40d1240d0f2bed66a174f8d34eea42e613c2c62851951eabd402a3c12e"
}
```
