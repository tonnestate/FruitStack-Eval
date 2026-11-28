# Proofbook seq 18568 — CONNECTION

- key: `c1caec68ed69bdc4`
- at: 1795864247.916983
- mission: director/mechanism-extraction
- hash: `024ae9327e0a3323dde61c2f5ea787a1ba24ffad9e67fb3ba8132d3a8f1faa24` (prev `77a964a6a927a0e8daf7fab3b72230803b53dc282e9d7cff597f4339a7e5cc70`)
- graph nodes: PB:024ae9327e0a3323dde61c2f5ea787a1ba24ffad9e67fb3ba8132d3a8f1faa24
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)



## Full row (verbatim JSON)

```json
{
 "seq": 18568,
 "at": 1795864247.916983,
 "problem": "p_vs_np",
 "mission": "director/mechanism-extraction",
 "key": "c1caec68ed69bdc4",
 "kind": "CONNECTION",
 "about": [
  "mech:x7022-for-every-n-1-every-integer-weight-vector-w-in-z-n-wit"
 ],
 "bingo": {
  "record": "MECHANISM",
  "id": "mech:x7022-for-every-n-1-every-integer-weight-vector-w-in-z-n-wit",
  "name": "x7022 For every n >= 1, every integer weight vector w in Z^n with max_i |w_i",
  "preconditions": "no explicit assumption found in the source statement",
  "effect": "For every n >= 1, every integer weight vector w in Z^n with max_i |w_i| <= B, every integer threshold t, and every l in {0,...,n}: the set of functions y in {0,1}^(n-l) -> [w_rest.y >= t - w_pre.rho], indexed by rho in {0,1}^l, has at most min(2^l, 2lB+1) distinct members, where w_pre = (w_1..w_l) a",
  "limitations": "none stated in the source; validity beyond its stated scope unverified",
  "correctness": "source status REVIEW_VERIFIED; VERIFICATION seq 7022 (extraction preserves, never upgrades the status)",
  "representations": "threshold",
  "interfaces": "threshold, bound:n >= 1, bound:Z^n, bound:w_i| <= B",
  "provenance": "VERIFICATION seq 7022 key 1b65e0b0a7ac2886 mission agent/pnp-desk/formal/G0173:desk",
  "basis": "EXTRACTED",
  "verification": "REVIEW_VERIFIED",
  "operations": [
   "threshold"
  ],
  "guarantees": [
   "For every n >= 1, every integer weight vector w in Z^n with max_i |w_i| <= B, every integer threshold t, and every l in {0,...,n}: the set of functions y in {0,1}^(n-l) -> [w_rest.y >= t - w_pre.rho], indexed by rho in {0,1}^l, has at most min(2^l, 2lB+1) distinct members, where w_pre = (w_1..w_l) a"
  ],
  "bounds": [
   "n >= 1",
   "Z^n",
   "w_i| <= B",
   "w_rest.y >= t"
  ]
 },
 "connection": "MECHANISM mech:x7022-for-every-n-1-every-integer-weight-vector-w-in-z-n-wit: For every n >= 1, every integer weight vector w in Z^n with max_i |w_i| <= B, every integer threshold t, and every l in {0,...,n}: the set of functions y in {0,1}^(n-l) -> [w_rest.y >= t - w_pre.rho], indexed by rho in {0,1}^l, has at most min(2^l, 2lB+1) distinct members, where w_pre = (w_1..w_l) a",
 "origin": "director",
 "prev": "77a964a6a927a0e8daf7fab3b72230803b53dc282e9d7cff597f4339a7e5cc70",
 "hash": "024ae9327e0a3323dde61c2f5ea787a1ba24ffad9e67fb3ba8132d3a8f1faa24"
}
```
