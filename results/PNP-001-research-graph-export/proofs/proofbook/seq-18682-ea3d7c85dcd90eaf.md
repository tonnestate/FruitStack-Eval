# Proofbook seq 18682 — CONNECTION

- key: `ea3d7c85dcd90eaf`
- at: 1795864635.926878
- mission: director/mechanism-extraction
- hash: `c5cd446f49f83235d0bd5b31cd7225acde9a1381b6e3c65dd5df470941a36ddd` (prev `c2f97e48df24b2410e191d0f93d5f14af971a9dd887ce61b4f17d31ee82d8f30`)
- graph nodes: PB:c5cd446f49f83235d0bd5b31cd7225acde9a1381b6e3c65dd5df470941a36ddd
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)



## Full row (verbatim JSON)

```json
{
 "seq": 18682,
 "at": 1795864635.926878,
 "problem": "p_vs_np",
 "mission": "director/mechanism-extraction",
 "key": "ea3d7c85dcd90eaf",
 "kind": "CONNECTION",
 "about": [
  "mech:x17813-statement-let-q-be-any-set-and-let-f-g-q-q-be-commuti"
 ],
 "bingo": {
  "record": "MECHANISM",
  "id": "mech:x17813-statement-let-q-be-any-set-and-let-f-g-q-q-be-commuti",
  "name": "x17813 statement: Let Q be any set and let f,g:Q→Q be commuting maps, meaning",
  "preconditions": "statement: Let Q be any set and let f,g:Q→Q be commuting maps, meaning f∘g=g∘f.; For every q∈Q, the words 01 and 10 induce the same terminal state when symbol 0 applies f and symbol 1 applies g. proof: Reading 01 applies f; The assumed identity f∘g=g∘f gives g(f(q))=f(g(q)) for every q.",
  "effect": "g, so its terminal state is g(f(q)).; Reading 10 applies g then f, so its terminal state is f(g(q)).",
  "limitations": "none stated in the source; validity beyond its stated scope unverified",
  "correctness": "source status REVIEW_VERIFIED; VERIFICATION seq 17813 (extraction preserves, never upgrades the status)",
  "representations": "statement-level",
  "interfaces": "statement-level",
  "provenance": "VERIFICATION seq 17813 key 01175b4c79a4f2b4 mission agent/pnp-desk/formal/G1127:desk",
  "basis": "EXTRACTED",
  "verification": "REVIEW_VERIFIED",
  "invariants": [
   "The assumed identity f∘g=g∘f gives g(f(q))=f(g(q)) for every q."
  ],
  "guarantees": [
   "g, so its terminal state is g(f(q)).",
   "Reading 10 applies g then f, so its terminal state is f(g(q))."
  ],
  "assumptions": [
   "statement: Let Q be any set and let f,g:Q→Q be commuting maps, meaning f∘g=g∘f.",
   "For every q∈Q, the words 01 and 10 induce the same terminal state when symbol 0 applies f and symbol 1 applies g. proof: Reading 01 applies f",
   "The assumed identity f∘g=g∘f gives g(f(q))=f(g(q)) for every q."
  ]
 },
 "connection": "MECHANISM mech:x17813-statement-let-q-be-any-set-and-let-f-g-q-q-be-commuti: g, so its terminal state is g(f(q)).; Reading 10 applies g then f, so its terminal state is f(g(q)).",
 "origin": "director",
 "prev": "c2f97e48df24b2410e191d0f93d5f14af971a9dd887ce61b4f17d31ee82d8f30",
 "hash": "c5cd446f49f83235d0bd5b31cd7225acde9a1381b6e3c65dd5df470941a36ddd"
}
```
