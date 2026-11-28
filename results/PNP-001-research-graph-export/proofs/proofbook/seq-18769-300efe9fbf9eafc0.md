# Proofbook seq 18769 — CONNECTION

- key: `300efe9fbf9eafc0`
- at: 1795865551.4881878
- mission: director/mechanism-extraction
- hash: `76cdf974f48c2b1a8a8f43c6c44dbb97d95c46c78731544d17ffaf2b29afc683` (prev `336e3c0ae2ccf6f9094bad4f099c9971a29fddd74942e8ff917b6c2ce662ecb3`)
- graph nodes: PB:76cdf974f48c2b1a8a8f43c6c44dbb97d95c46c78731544d17ffaf2b29afc683
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)



## Full row (verbatim JSON)

```json
{
 "seq": 18769,
 "at": 1795865551.4881878,
 "problem": "p_vs_np",
 "mission": "director/mechanism-extraction",
 "key": "300efe9fbf9eafc0",
 "kind": "CONNECTION",
 "about": [
  "mech:x18766-t66-sec-9-thm-9-1-o-rc-m-r-log-r-log-t-for-scalar-obs"
 ],
 "bingo": {
  "record": "MECHANISM",
  "id": "mech:x18766-t66-sec-9-thm-9-1-o-rc-m-r-log-r-log-t-for-scalar-obs",
  "name": "x18766 T66 sec.9 Thm 9.1 (O(rC+M(r)(log r+log T)) for scalar observations wit",
  "preconditions": "T66 sec.9 Thm 9.1 (O(rC+M(r)(log r+log T)) for scalar observations with promised Hankel rank r via BM on 2r terms + Bostan-Mori, promise/field/uniformity audited) and Thm 9.2: if the promise r is computed in time t_rho",
  "effect": "for the diagonal language t_rho + rC + M(r)(log r+log T) = Omega(T/log T) in",
  "limitations": "none stated in the source; validity beyond its stated scope unverified",
  "correctness": "source status UNVERIFIED_STEP; PROOF_STEP seq 18766 (extraction preserves, never upgrades the status)",
  "representations": "rank, hankel, diagonal, hierarchy",
  "interfaces": "rank, hankel, diagonal, hierarchy, bound:O(rC+M(r), bound:Omega(T/log T), bound:T^{1-o",
  "provenance": "PROOF_STEP seq 18766 key cd71f919259a0469 mission director/pi-t66",
  "basis": "EXTRACTED",
  "verification": "UNVERIFIED_STEP",
  "operations": [
   "rank",
   "hankel",
   "diagonal",
   "hierarchy"
  ],
  "guarantees": [
   "for the diagonal language t_rho + rC + M(r)(log r+log T) = Omega(T/log T) in"
  ],
  "bounds": [
   "O(rC+M(r)",
   "Omega(T/log T)",
   "T^{1-o"
  ],
  "assumptions": [
   "T66 sec.9 Thm 9.1 (O(rC+M(r)(log r+log T)) for scalar observations with promised Hankel rank r via BM on 2r terms + Bostan-Mori, promise/field/uniformity audited) and Thm 9.2: if the promise r is computed in time t_rho"
  ]
 },
 "connection": "MECHANISM mech:x18766-t66-sec-9-thm-9-1-o-rc-m-r-log-r-log-t-for-scalar-obs: for the diagonal language t_rho + rC + M(r)(log r+log T) = Omega(T/log T) in",
 "origin": "director",
 "prev": "336e3c0ae2ccf6f9094bad4f099c9971a29fddd74942e8ff917b6c2ce662ecb3",
 "hash": "76cdf974f48c2b1a8a8f43c6c44dbb97d95c46c78731544d17ffaf2b29afc683"
}
```
