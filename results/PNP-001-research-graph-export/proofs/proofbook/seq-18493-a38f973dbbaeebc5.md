# Proofbook seq 18493 — CONNECTION

- key: `a38f973dbbaeebc5`
- at: 1795864017.7532332
- mission: director/mechanism-extraction
- hash: `e2969ad839b925fec7e5559521fa41dea2bc6aabfb9eb96f762b05aa74264957` (prev `8bced384c2cf2ca9d112c7fe69808f6b60abb6dd5c78ea13437fef03e4c97d7a`)
- graph nodes: PB:e2969ad839b925fec7e5559521fa41dea2bc6aabfb9eb96f762b05aa74264957
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)



## Full row (verbatim JSON)

```json
{
 "seq": 18493,
 "at": 1795864017.7532332,
 "problem": "p_vs_np",
 "mission": "director/mechanism-extraction",
 "key": "a38f973dbbaeebc5",
 "kind": "CONNECTION",
 "about": [
  "mech:x196-verified-dim-span-d-k-f-c-n-k-2-exactly-for-f-det-n-and"
 ],
 "bingo": {
  "record": "MECHANISM",
  "id": "mech:x196-verified-dim-span-d-k-f-c-n-k-2-exactly-for-f-det-n-and",
  "name": "x196 VERIFIED: dim span{d^k f} = C(n,k)^2 exactly for f=det_n and f=perm_n ",
  "preconditions": "no explicit assumption found in the source statement",
  "effect": "Hence border Waring rank underline-WR(f) >= max_k C(n,k)^2 = C(n,floor(n/2))^2 = Theta(4^n/n), EXPONENTIAL for BOTH determinant and permanent.; By BDI21 Prop 6.6 the minimal noncommutative-ABP width ncw(f) equals this max derivative-space dimension, so ncw(det_n)=ncw(perm_n)=C(n,floor(n/2))^2, also exponential.",
  "limitations": "CONSEQUENCE: BDI21's 'efficient HWV evaluation at low (border) Waring rank points' does NOT apply to det/perm by that property - a prior T13 claim to the contrary is RETRACTED.",
  "correctness": "source status ESTABLISHED_EXTERNAL; KNOWN_RESULT seq 196 (extraction preserves, never upgrades the status)",
  "representations": "rank",
  "interfaces": "rank, bound:d^k, bound:exactly for f, bound:underline-WR(f) >= max_k",
  "provenance": "KNOWN_RESULT seq 196 key df3a5229b33e05bb mission pi-research-2026-11-17-T13T0-corrections",
  "basis": "EXTRACTED",
  "verification": "ESTABLISHED_EXTERNAL",
  "operations": [
   "rank"
  ],
  "guarantees": [
   "Hence border Waring rank underline-WR(f) >= max_k C(n,k)^2 = C(n,floor(n/2))^2 = Theta(4^n/n), EXPONENTIAL for BOTH determinant and permanent.",
   "By BDI21 Prop 6.6 the minimal noncommutative-ABP width ncw(f) equals this max derivative-space dimension, so ncw(det_n)=ncw(perm_n)=C(n,floor(n/2))^2, also exponential."
  ],
  "bounds": [
   "d^k",
   "exactly for f",
   "underline-WR(f) >= max_k",
   "Theta(4^n/n)"
  ]
 },
 "connection": "MECHANISM mech:x196-verified-dim-span-d-k-f-c-n-k-2-exactly-for-f-det-n-and: Hence border Waring rank underline-WR(f) >= max_k C(n,k)^2 = C(n,floor(n/2))^2 = Theta(4^n/n), EXPONENTIAL for BOTH determinant and permanent.; By BDI21 Prop 6.6 the minimal noncommutative-ABP width ncw(f) equals this max derivative-space dimension, so ncw(det_n)=ncw(perm_n)=C(n,floor(n/2))^2, also ",
 "origin": "director",
 "prev": "8bced384c2cf2ca9d112c7fe69808f6b60abb6dd5c78ea13437fef03e4c97d7a",
 "hash": "e2969ad839b925fec7e5559521fa41dea2bc6aabfb9eb96f762b05aa74264957"
}
```
