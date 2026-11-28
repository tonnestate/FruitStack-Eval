# Proofbook seq 18604 — CONNECTION

- key: `a5b2bde482ffbbf6`
- at: 1795864363.6223946
- mission: director/mechanism-extraction
- hash: `f76adb4a88fd4ce21f9dc0f5e21f9d4c8281d9464a814bc413bc8a8bd06c8465` (prev `1ef12fcee4c8012a3131faf212fcf8b16cef759ec82f765117b5961930610314`)
- graph nodes: PB:f76adb4a88fd4ce21f9dc0f5e21f9d4c8281d9464a814bc413bc8a8bd06c8465
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)



## Full row (verbatim JSON)

```json
{
 "seq": 18604,
 "at": 1795864363.6223946,
 "problem": "p_vs_np",
 "mission": "director/mechanism-extraction",
 "key": "a5b2bde482ffbbf6",
 "kind": "CONNECTION",
 "about": [
  "mech:x16840-d6-repair-of-d6-with-p-n-beta-eps-5-1-and-pairwise-in"
 ],
 "bingo": {
  "record": "MECHANISM",
  "id": "mech:x16840-d6-repair-of-d6-with-p-n-beta-eps-5-1-and-pairwise-in",
  "name": "x16840 D6' (repair of D6): with p = N^{beta+eps/5-1} and pairwise independent",
  "preconditions": "If |C| <= N^{1+eps} and every reused gate has d_g <= D* := N^{(1-beta)/2-eta-7eps/10}",
  "effect": "D6' (repair of D6): with p = N^{beta+eps/5-1} and pairwise independent star events, E[gamma(C|rho)] <= W(C) := sum_{g reused} min(1, p^2 d_g^2/2) (a reused gate with <= 1 live variable becomes a literal or constant, free in the principal-formula forest).; W(C) <= N^{beta-2eta}/2 and Pr[gamma(C|rho) > N^{beta-eta}] <= N^{-eta} (Markov).; With AF (P1,P2): Gap-MCSP[N^beta] has no De Morgan circuit of size N^{1+eps} with W(C) <= N^{beta-2eta}.",
  "limitations": "none stated in the source; validity beyond its stated scope unverified",
  "correctness": "source status UNVERIFIED_STEP; PROOF_STEP seq 16840 (extraction preserves, never upgrades the status)",
  "representations": "threshold, circuit, formula, gate",
  "interfaces": "threshold, circuit, formula, gate, bound:N^{beta+eps/5-1}, bound:p^2, bound:with <= 1",
  "provenance": "PROOF_STEP seq 16840 key 5adc4835af1c825f mission director/closure-intervention",
  "basis": "EXTRACTED",
  "verification": "UNVERIFIED_STEP",
  "operations": [
   "threshold",
   "circuit",
   "formula",
   "gate"
  ],
  "guarantees": [
   "D6' (repair of D6): with p = N^{beta+eps/5-1} and pairwise independent star events, E[gamma(C|rho)] <= W(C) := sum_{g reused} min(1, p^2 d_g^2/2) (a reused gate with <= 1 live variable becomes a literal or constant, free in the principal-formula forest).",
   "W(C) <= N^{beta-2eta}/2 and Pr[gamma(C|rho) > N^{beta-eta}] <= N^{-eta} (Markov).",
   "With AF (P1,P2): Gap-MCSP[N^beta] has no De Morgan circuit of size N^{1+eps} with W(C) <= N^{beta-2eta}."
  ],
  "bounds": [
   "N^{beta+eps/5-1}",
   "p^2",
   "with <= 1",
   "C| <= N^{1+eps}",
   "d_g <= D*",
   "W(C) <= N^{beta-2eta}/2",
   "N^{beta-eta}",
   "N^{-eta}"
  ],
  "assumptions": [
   "If |C| <= N^{1+eps} and every reused gate has d_g <= D* := N^{(1-beta)/2-eta-7eps/10}"
  ]
 },
 "connection": "MECHANISM mech:x16840-d6-repair-of-d6-with-p-n-beta-eps-5-1-and-pairwise-in: D6' (repair of D6): with p = N^{beta+eps/5-1} and pairwise independent star events, E[gamma(C|rho)] <= W(C) := sum_{g reused} min(1, p^2 d_g^2/2) (a reused gate with <= 1 live variable becomes a literal or constant, free in the principal-formula forest).; W(C) <= N^{beta-2eta}/2 and Pr[gamma(C|rho) ",
 "origin": "director",
 "prev": "1ef12fcee4c8012a3131faf212fcf8b16cef759ec82f765117b5961930610314",
 "hash": "f76adb4a88fd4ce21f9dc0f5e21f9d4c8281d9464a814bc413bc8a8bd06c8465"
}
```
