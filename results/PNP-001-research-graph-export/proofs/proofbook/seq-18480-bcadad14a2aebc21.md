# Proofbook seq 18480 — CONNECTION

- key: `bcadad14a2aebc21`
- at: 1795863979.1411068
- mission: director/mechanism-extraction
- hash: `d3670cb4deda947dc089a79c1ba9c41bad9b5b3b5be84feef5d07284c9053973` (prev `02926e21cd998bd93206a11fc85c53b0f2ddc7582500c1aadf0b52bee8cd6aee`)
- graph nodes: PB:d3670cb4deda947dc089a79c1ba9c41bad9b5b3b5be84feef5d07284c9053973
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)



## Full row (verbatim JSON)

```json
{
 "seq": 18480,
 "at": 1795863979.1411068,
 "problem": "p_vs_np",
 "mission": "director/mechanism-extraction",
 "key": "bcadad14a2aebc21",
 "kind": "CONNECTION",
 "about": [
  "mech:x149-for-char-2-dim-k-x-i-h-a-b-max-a-b-h-1-for-1-h-min-a-b-"
 ],
 "bingo": {
  "record": "MECHANISM",
  "id": "mech:x149-for-char-2-dim-k-x-i-h-a-b-max-a-b-h-1-for-1-h-min-a-b-",
  "name": "x149 For char != 2, dim K[X]/I_h(a,b) = max(a,b)(h-1) for 1<=h<=min(a,b), h",
  "preconditions": "Xie explicitly states the dimension calc does NOT imply reducedness; the complete-intersection/reduced result (Thm 1.3) is ONLY for maximal permanents I_k(k,k+1), NOT for the square critical locus I_{n-1}(n,n).",
  "effect": "For char != 2, dim K[X]/I_h(a,b) = max(a,b)(h-1) for 1<=h<=min(a,b), h<max(a,b).",
  "limitations": "Xie explicitly states the dimension calc does NOT imply reducedness; the complete-intersection/reduced result (Thm 1.3) is ONLY for maximal permanents I_k(k,k+1), NOT for the square critical locus I_{n-1}(n,n).",
  "correctness": "source status ESTABLISHED_EXTERNAL; KNOWN_RESULT seq 149 (extraction preserves, never upgrades the status)",
  "representations": "rank",
  "interfaces": "rank, bound:1<=h",
  "provenance": "KNOWN_RESULT seq 149 key ad079b262f3620a1 mission pi-research-2026-11-17-O1-xie",
  "basis": "EXTRACTED",
  "verification": "ESTABLISHED_EXTERNAL",
  "operations": [
   "rank"
  ],
  "guarantees": [
   "For char != 2, dim K[X]/I_h(a,b) = max(a,b)(h-1) for 1<=h<=min(a,b), h<max(a,b)."
  ],
  "bounds": [
   "1<=h"
  ],
  "compatibility": [
   "Xie explicitly states the dimension calc does NOT imply reducedness; the complete-intersection/reduced result (Thm 1.3) is ONLY for maximal permanents I_k(k,k+1), NOT for the square critical locus I_{n-1}(n,n)."
  ]
 },
 "connection": "MECHANISM mech:x149-for-char-2-dim-k-x-i-h-a-b-max-a-b-h-1-for-1-h-min-a-b-: For char != 2, dim K[X]/I_h(a,b) = max(a,b)(h-1) for 1<=h<=min(a,b), h<max(a,b).",
 "origin": "director",
 "prev": "02926e21cd998bd93206a11fc85c53b0f2ddc7582500c1aadf0b52bee8cd6aee",
 "hash": "d3670cb4deda947dc089a79c1ba9c41bad9b5b3b5be84feef5d07284c9053973"
}
```
