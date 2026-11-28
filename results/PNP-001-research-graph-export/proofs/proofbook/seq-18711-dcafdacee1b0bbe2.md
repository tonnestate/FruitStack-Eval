# Proofbook seq 18711 — CONNECTION

- key: `dcafdacee1b0bbe2`
- at: 1795864713.9124281
- mission: director/mechanism-extraction
- hash: `2666d971369c6a52a267798ffa4b1d576e79b201229210fa5d186c873b220cb5` (prev `b75c47b8757ea1f8b843641832bc0518a85ecadb0f6f92de95f60ebdf681a673`)
- graph nodes: PB:2666d971369c6a52a267798ffa4b1d576e79b201229210fa5d186c873b220cb5
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)



## Full row (verbatim JSON)

```json
{
 "seq": 18711,
 "at": 1795864713.9124281,
 "problem": "p_vs_np",
 "mission": "director/mechanism-extraction",
 "key": "dcafdacee1b0bbe2",
 "kind": "CONNECTION",
 "about": [
  "mech:x18314-correction-to-18312-2-over-f2-a-valid-certificate-sum"
 ],
 "bingo": {
  "record": "MECHANISM",
  "id": "mech:x18314-correction-to-18312-2-over-f2-a-valid-certificate-sum",
  "name": "x18314 CORRECTION to 18312 (2): over F2 a valid certificate sum a_i f_i=1 has",
  "preconditions": "Choice functions embed injectively into certificates (sigma -> c_i=1[sigma=i]); the converse needs a selection (e.g. first active summand), so the two are not in bijection.",
  "effect": "CORRECTION to 18312 (2): over F2 a valid certificate sum a_i f_i=1 has, at every point, an ODD number of active summands (a_i f_i=1); exactly one active summand is the special case of a choice function.",
  "limitations": "Choice functions embed injectively into certificates (sigma -> c_i=1[sigma=i]); the converse needs a selection (e.g. first active summand), so the two are not in bijection.",
  "correctness": "source status UNVERIFIED_STEP; PROOF_STEP seq 18314 (extraction preserves, never upgrades the status)",
  "representations": "certificate",
  "interfaces": "certificate, bound:exactly one active summand is the spec",
  "provenance": "PROOF_STEP seq 18314 key d7af4f671c467d34 mission PNP-001-T60-gate-ideal-saturation-2026-11-28",
  "basis": "EXTRACTED",
  "verification": "UNVERIFIED_STEP",
  "operations": [
   "certificate"
  ],
  "guarantees": [
   "CORRECTION to 18312 (2): over F2 a valid certificate sum a_i f_i=1 has, at every point, an ODD number of active summands (a_i f_i=1); exactly one active summand is the special case of a choice function."
  ],
  "bounds": [
   "exactly one active summand is the spec"
  ],
  "compatibility": [
   "Choice functions embed injectively into certificates (sigma -> c_i=1[sigma=i]); the converse needs a selection (e.g. first active summand), so the two are not in bijection."
  ]
 },
 "connection": "MECHANISM mech:x18314-correction-to-18312-2-over-f2-a-valid-certificate-sum: CORRECTION to 18312 (2): over F2 a valid certificate sum a_i f_i=1 has, at every point, an ODD number of active summands (a_i f_i=1); exactly one active summand is the special case of a choice function.",
 "origin": "director",
 "prev": "b75c47b8757ea1f8b843641832bc0518a85ecadb0f6f92de95f60ebdf681a673",
 "hash": "2666d971369c6a52a267798ffa4b1d576e79b201229210fa5d186c873b220cb5"
}
```
