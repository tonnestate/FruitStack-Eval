# Proofbook seq 18603 — CONNECTION

- key: `f5cbc3ed493cdcfa`
- at: 1795864363.3351827
- mission: director/mechanism-extraction
- hash: `1ef12fcee4c8012a3131faf212fcf8b16cef759ec82f765117b5961930610314` (prev `b7639bc911af828b6b86cb7557274eddb59096a13989e4843b559a7cfa3353c7`)
- graph nodes: PB:1ef12fcee4c8012a3131faf212fcf8b16cef759ec82f765117b5961930610314
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)



## Full row (verbatim JSON)

```json
{
 "seq": 18603,
 "at": 1795864363.3351827,
 "problem": "p_vs_np",
 "mission": "director/mechanism-extraction",
 "key": "f5cbc3ed493cdcfa",
 "kind": "CONNECTION",
 "about": [
  "mech:x16826-strength-map-owner-directive-2026-11-26-do-not-impose"
 ],
 "bingo": {
  "record": "MECHANISM",
  "id": "mech:x16826-strength-map-owner-directive-2026-11-26-do-not-impose",
  "name": "x16826 STRENGTH-MAP (owner directive 2026-11-26: do not impose the stronger n",
  "preconditions": "A uniform lower bound for search-MCSP^A[s] can hold even if small non-uniform circuits exist, so the uniform band carries no circuit-lower-bound obligation.; Existing uniform handle in the book: time-space route Q-C (seq 8531: MMW Thm 1.3 at s = 2^{(log N)^delta} needs time N^{1+o(1)} at space N^{o(1)}, below SAT notin DTISP(n^c, n^{o(1)}), c < 2cos(pi/7); missing a local reduction to search-MCSP^A[s];",
  "effect": "NON-UNIFORM BAND (each obligation implies NP notsubset P/poly, strictly stronger than needed as far as known): OBL-QSTAR (QO1/QO2), target (8)/Q3 (MMW Thm 1.4 b.3), OBL-R10-CJW-BRIDGE, OBL-AF, COV1 residual R (W-A, W-B, W-C), W-E (sparse NP vs circuits), OBL-ST-ABS (ST2).",
  "limitations": "STRENGTH-MAP (owner directive 2026-11-26: do not impose the stronger non-uniform separation where P != NP suffices).; UNIFORM BAND (conclusion P != NP only): route M M1/O* with UNIFORM streaming algorithms (MMW Thm 1.3, condition (40a); sec.2 item 6: only the non-uniform M3 forces NP notsubset P/poly), OBL-W-D-COLLIDE (CJSW: uniform refuters against uniform algorithms), F/CanMCSP (instance of M1).; Murray-Williams no-go covers A = empty and projections only).",
  "correctness": "source status UNVERIFIED_STEP; PROOF_STEP seq 16826 (extraction preserves, never upgrades the status)",
  "representations": "projection, reduction, circuit",
  "interfaces": "projection, reduction, circuit, bound:N^{1+o, bound:N^{o, bound:n^c",
  "provenance": "PROOF_STEP seq 16826 key 3c56ca7e54666bdd mission director/closure-strength",
  "basis": "EXTRACTED",
  "verification": "UNVERIFIED_STEP",
  "operations": [
   "projection",
   "reduction",
   "circuit"
  ],
  "guarantees": [
   "NON-UNIFORM BAND (each obligation implies NP notsubset P/poly, strictly stronger than needed as far as known): OBL-QSTAR (QO1/QO2), target (8)/Q3 (MMW Thm 1.4 b.3), OBL-R10-CJW-BRIDGE, OBL-AF, COV1 residual R (W-A, W-B, W-C), W-E (sparse NP vs circuits), OBL-ST-ABS (ST2)."
  ],
  "bounds": [
   "N^{1+o",
   "N^{o",
   "n^c",
   "n^{o"
  ],
  "compatibility": [
   "Existing uniform handle in the book: time-space route Q-C (seq 8531: MMW Thm 1.3 at s = 2^{(log N)^delta} needs time N^{1+o(1)} at space N^{o(1)}, below SAT notin DTISP(n^c, n^{o(1)}), c < 2cos(pi/7); missing a local reduction to search-MCSP^A[s];"
  ],
  "assumptions": [
   "A uniform lower bound for search-MCSP^A[s] can hold even if small non-uniform circuits exist, so the uniform band carries no circuit-lower-bound obligation."
  ]
 },
 "connection": "MECHANISM mech:x16826-strength-map-owner-directive-2026-11-26-do-not-impose: NON-UNIFORM BAND (each obligation implies NP notsubset P/poly, strictly stronger than needed as far as known): OBL-QSTAR (QO1/QO2), target (8)/Q3 (MMW Thm 1.4 b.3), OBL-R10-CJW-BRIDGE, OBL-AF, COV1 residual R (W-A, W-B, W-C), W-E (sparse NP vs circuits), OBL-ST-ABS (ST2).",
 "origin": "director",
 "prev": "b7639bc911af828b6b86cb7557274eddb59096a13989e4843b559a7cfa3353c7",
 "hash": "1ef12fcee4c8012a3131faf212fcf8b16cef759ec82f765117b5961930610314"
}
```
