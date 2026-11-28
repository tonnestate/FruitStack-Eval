# Proofbook seq 18639 — CONNECTION

- key: `fbaa38af5fee1ea8`
- at: 1795864478.517048
- mission: director/mechanism-extraction
- hash: `39e62db9bbb937f3464485774c9c13108025b440d5bc269a65daf025f2a24c95` (prev `83dbd94e2b366fc42254bf9872001233240e1e5c47b70d563c200525b3527302`)
- graph nodes: PB:39e62db9bbb937f3464485774c9c13108025b440d5bc269a65daf025f2a24c95
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)



## Full row (verbatim JSON)

```json
{
 "seq": 18639,
 "at": 1795864478.517048,
 "problem": "p_vs_np",
 "mission": "director/mechanism-extraction",
 "key": "fbaa38af5fee1ea8",
 "kind": "CONNECTION",
 "about": [
  "mech:x17207-robust-gamma-owner-derivation-2026-11-26-director-che"
 ],
 "bingo": {
  "record": "MECHANISM",
  "id": "mech:x17207-robust-gamma-owner-derivation-2026-11-26-director-che",
  "name": "x17207 ROBUST-GAMMA (owner derivation 2026-11-26, director check;",
  "preconditions": "no explicit assumption found in the source statement",
  "effect": "Restriction with k >= N^{gamma+o(1)} free bits (p = N^{gamma-1+o(1)}): Pr[some a-circuit within tau] <= 2^{O(N^beta)} 2^{tau log(ek/tau)} 2^{-k} = 2^{-Omega(k)}; restricted size p^2 L N^{o(1)}, CKLM PRG outputs have size L_rest^{1/3+o(1)} <= a iff L <= N^{2+3beta-2gamma-xi}.; NO: each a-circuit survives with prob <= e^{-t tau/N}, union over 2^{O(N^beta)} circuits;; So a uniform bound L(H_{J,a}) <= L_H for the partial-consistency predicate H_{J,a} gives probabilistic formulas of size L_H (J hard-wired).",
  "limitations": "Restriction with k >= N^{gamma+o(1)} free bits (p = N^{gamma-1+o(1)}): Pr[some a-circuit within tau] <= 2^{O(N^beta)} 2^{tau log(ek/tau)} 2^{-k} = 2^{-Omega(k)}; restricted size p^2 L N^{o(1)}, CKLM PRG outputs have size L_rest^{1/3+o(1)} <= a iff L <= N^{2+3beta-2gamma-xi}.",
  "correctness": "source status UNVERIFIED_STEP; PROOF_STEP seq 17207 (extraction preserves, never upgrades the status)",
  "representations": "restriction, sampling, circuit, formula",
  "interfaces": "restriction, sampling, circuit, formula, bound:N^beta/, bound:N^gamma, bound:k >= N^{gamma+o(1)}",
  "provenance": "PROOF_STEP seq 17207 key 3423ec37fe7e283c mission director/closure-exclusions",
  "basis": "EXTRACTED",
  "verification": "UNVERIFIED_STEP",
  "operations": [
   "restriction",
   "sampling",
   "circuit",
   "formula"
  ],
  "guarantees": [
   "Restriction with k >= N^{gamma+o(1)} free bits (p = N^{gamma-1+o(1)}): Pr[some a-circuit within tau] <= 2^{O(N^beta)} 2^{tau log(ek/tau)} 2^{-k} = 2^{-Omega(k)}; restricted size p^2 L N^{o(1)}, CKLM PRG outputs have size L_rest^{1/3+o(1)} <= a iff L <= N^{2+3beta-2gamma-xi}.",
   "NO: each a-circuit survives with prob <= e^{-t tau/N}, union over 2^{O(N^beta)} circuits;",
   "So a uniform bound L(H_{J,a}) <= L_H for the partial-consistency predicate H_{J,a} gives probabilistic formulas of size L_H (J hard-wired)."
  ],
  "bounds": [
   "N^beta/",
   "N^gamma",
   "k >= N^{gamma+o(1)}",
   "N^{gamma-1+o",
   "O(N^beta)",
   "Omega(k)",
   "p^2",
   "N^{o"
  ]
 },
 "connection": "MECHANISM mech:x17207-robust-gamma-owner-derivation-2026-11-26-director-che: Restriction with k >= N^{gamma+o(1)} free bits (p = N^{gamma-1+o(1)}): Pr[some a-circuit within tau] <= 2^{O(N^beta)} 2^{tau log(ek/tau)} 2^{-k} = 2^{-Omega(k)}; restricted size p^2 L N^{o(1)}, CKLM PRG outputs have size L_rest^{1/3+o(1)} <= a iff L <= N^{2+3beta-2gamma-xi}.; NO: each a-circuit surv",
 "origin": "director",
 "prev": "83dbd94e2b366fc42254bf9872001233240e1e5c47b70d563c200525b3527302",
 "hash": "39e62db9bbb937f3464485774c9c13108025b440d5bc269a65daf025f2a24c95"
}
```
