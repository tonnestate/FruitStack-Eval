# Proofbook seq 18750 — CONNECTION

- key: `5a19c8ecbb6ae1fd`
- at: 1795864828.7575574
- mission: director/mechanism-extraction
- hash: `e6a08de07a6cd57ed5cb5f4bdd45b300622f4475a534956adf9ffe98f9385ce5` (prev `f6de2ab2e2c33565361336629ab7a4b385db41dd129060b845a5a3aff64d64f1`)
- graph nodes: PB:e6a08de07a6cd57ed5cb5f4bdd45b300622f4475a534956adf9ffe98f9385ce5
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)



## Full row (verbatim JSON)

```json
{
 "seq": 18750,
 "at": 1795864828.7575574,
 "problem": "p_vs_np",
 "mission": "director/mechanism-extraction",
 "key": "5a19c8ecbb6ae1fd",
 "kind": "CONNECTION",
 "about": [
  "mech:x18367-row-18299-refutation-withdrawn-sel-c-x-g-1-g-s-in-fl-"
 ],
 "bingo": {
  "record": "MECHANISM",
  "id": "mech:x18367-row-18299-refutation-withdrawn-sel-c-x-g-1-g-s-in-fl-",
  "name": "x18367 Row 18299 refutation withdrawn: SEL:(C,x)->(g_1..g_s) in FL (write-onl",
  "preconditions": "(",
  "effect": ") g_s is CVP, P-complete under logspace reductions; (<=) P=L gives CVP in L, loop over j writing each bit, only the counter stored.",
  "limitations": "Row 18299 refutation withdrawn: SEL:(C,x)->(g_1..g_s) in FL (write-only output) iff P=L.; (<=) P=L gives CVP in L, loop over j writing each bit, only the counter stored.; Universal evaluator only; fixed families not claimed; identity of the T60 selector with SEL unverified.",
  "correctness": "source status UNVERIFIED_STEP; PROOF_STEP seq 18367 (extraction preserves, never upgrades the status)",
  "representations": "reduction",
  "interfaces": "reduction",
  "provenance": "PROOF_STEP seq 18367 key a829a9d1749d322c mission PNP-001-audit-repair-round4-2026-11-28",
  "basis": "EXTRACTED",
  "verification": "UNVERIFIED_STEP",
  "operations": [
   "reduction"
  ],
  "invariants": [
   "Universal evaluator only; fixed families not claimed; identity of the T60 selector with SEL unverified."
  ],
  "guarantees": [
   ") g_s is CVP, P-complete under logspace reductions",
   "(<=) P=L gives CVP in L, loop over j writing each bit, only the counter stored."
  ],
  "assumptions": [
   "("
  ]
 },
 "connection": "MECHANISM mech:x18367-row-18299-refutation-withdrawn-sel-c-x-g-1-g-s-in-fl-: ) g_s is CVP, P-complete under logspace reductions; (<=) P=L gives CVP in L, loop over j writing each bit, only the counter stored.",
 "origin": "director",
 "prev": "f6de2ab2e2c33565361336629ab7a4b385db41dd129060b845a5a3aff64d64f1",
 "hash": "e6a08de07a6cd57ed5cb5f4bdd45b300622f4475a534956adf9ffe98f9385ce5"
}
```
