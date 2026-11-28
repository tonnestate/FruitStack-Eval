# Proofbook seq 18536 — CONNECTION

- key: `cd89ba7baf8d7edd`
- at: 1795864169.026483
- mission: director/mechanism-extraction
- hash: `1c0ef88add26cb3f132f916884f16b01f474b1bcbec66445facf364cc4c13e18` (prev `6421888c5abae5e80823adf7477e7a339dd4cfc73df6c667add26c8d0806f5a8`)
- graph nodes: PB:1c0ef88add26cb3f132f916884f16b01f474b1bcbec66445facf364cc4c13e18
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)



## Full row (verbatim JSON)

```json
{
 "seq": 18536,
 "at": 1795864169.026483,
 "problem": "p_vs_np",
 "mission": "director/mechanism-extraction",
 "key": "cd89ba7baf8d7edd",
 "kind": "CONNECTION",
 "about": [
  "mech:x3313-for-every-n-3-and-every-nonempty-set-f-of-distinct-wei"
 ],
 "bingo": {
  "record": "MECHANISM",
  "id": "mech:x3313-for-every-n-3-and-every-nonempty-set-f-of-distinct-wei",
  "name": "x3313 For every n >= 3 and every nonempty set F of distinct weight-3 clauses",
  "preconditions": "If b-a = 1, this is 1-in-3 on w.; If b-a = 2, sum(w) = 2 on every clause, i.e. sum(1-w) = 1, so 1-in-3 on z = 1-w.",
  "effect": "For every n >= 3 and every nonempty set F of distinct weight-3 clauses over variables 0..n-1: there is a GF(3) vector x with x_a+x_b+x_c = 1 (mod 3) for every clause {a,b,c} in F, taking exactly two distinct values, if and only if F has a 0/1 solution (exactly one variable equal to 1 in every clause; Then sum over a clause equals (b-a) * sum(w) mod 3, so the clause condition is sum(w) = (b-a)^{-1} = (b-a) mod 3 (sum(w) in {0,..,3}).; Hence the set of GF(3) solutions using at most two values is nonempty exactly when F is positive 1-in-3 satisfiable.",
  "limitations": "For every n >= 3 and every nonempty set F of distinct weight-3 clauses over variables 0..n-1: there is a GF(3) vector x with x_a+x_b+x_c = 1 (mod 3) for every clause {a,b,c} in F, taking exactly two distinct values, if and only if F has a 0/1 solution (exactly one variable equal to 1 in every clause",
  "correctness": "source status REVIEW_VERIFIED; VERIFICATION seq 3313 (extraction preserves, never upgrades the status)",
  "representations": "statement-level",
  "interfaces": "bound:n >= 3, bound:exactly two distinct values, bound:exactly one variable equal to 1 in eve",
  "provenance": "VERIFICATION seq 3313 key 1bf524b45ad5edea mission agent/pnp-desk/formal/G0084:desk",
  "basis": "EXTRACTED",
  "verification": "REVIEW_VERIFIED",
  "guarantees": [
   "For every n >= 3 and every nonempty set F of distinct weight-3 clauses over variables 0..n-1: there is a GF(3) vector x with x_a+x_b+x_c = 1 (mod 3) for every clause {a,b,c} in F, taking exactly two distinct values, if and only if F has a 0/1 solution (exactly one variable equal to 1 in every clause",
   "Then sum over a clause equals (b-a) * sum(w) mod 3, so the clause condition is sum(w) = (b-a)^{-1} = (b-a) mod 3 (sum(w) in {0,..,3}).",
   "Hence the set of GF(3) solutions using at most two values is nonempty exactly when F is positive 1-in-3 satisfiable."
  ],
  "bounds": [
   "n >= 3",
   "exactly two distinct values",
   "exactly one variable equal to 1 in eve",
   "exactly two values because each clause",
   "exactly when F is positive 1-in-3 sati"
  ],
  "assumptions": [
   "If b-a = 1, this is 1-in-3 on w.",
   "If b-a = 2, sum(w) = 2 on every clause, i.e. sum(1-w) = 1, so 1-in-3 on z = 1-w."
  ]
 },
 "connection": "MECHANISM mech:x3313-for-every-n-3-and-every-nonempty-set-f-of-distinct-wei: For every n >= 3 and every nonempty set F of distinct weight-3 clauses over variables 0..n-1: there is a GF(3) vector x with x_a+x_b+x_c = 1 (mod 3) for every clause {a,b,c} in F, taking exactly two distinct values, if and only if F has a 0/1 solution (exactly one variable equal to 1 in every clause",
 "origin": "director",
 "prev": "6421888c5abae5e80823adf7477e7a339dd4cfc73df6c667add26c8d0806f5a8",
 "hash": "1c0ef88add26cb3f132f916884f16b01f474b1bcbec66445facf364cc4c13e18"
}
```
