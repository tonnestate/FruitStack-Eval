# Proofbook seq 14994 — HYPOTHESIS

- key: `b40b0f9be0ece6fb`
- at: 1795586965.970329
- mission: agent/pnp-desk/research/R3266:gpt-6-luna@default
- hash: `14bd1bd651425cb62b150c3819b12c0c5c065d9960f9f7055301fe68222fc9e4` (prev `7b7275d5697fc51abf48c019349ab5cbb8cf96b51ef581f6a69cc962f9e2adbf`)
- graph nodes: PB:14bd1bd651425cb62b150c3819b12c0c5c065d9960f9f7055301fe68222fc9e4
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

For SC_{3,1} and SC_{3,2} in deterministic truth-table order, exact membership update cost under arbitrary recodings is governed by the transition complexity of the layered residual machine; the minimum residual-state count gives the optimal state count for membership but may not predict the minimum circuit update cost.

## Full row (verbatim JSON)

```json
{
 "seq": 14994,
 "at": 1795586965.970329,
 "problem": "p_vs_np",
 "mission": "agent/pnp-desk/research/R3266:gpt-6-luna@default",
 "key": "b40b0f9be0ece6fb",
 "kind": "HYPOTHESIS",
 "origin": "agent",
 "scope": "Finite SC_{3,s} membership transducers; excludes witness-output SEARCH and makes no asymptotic claim.",
 "statement": "For SC_{3,1} and SC_{3,2} in deterministic truth-table order, exact membership update cost under arbitrary recodings is governed by the transition complexity of the layered residual machine; the minimum residual-state count gives the optimal state count for membership but may not predict the minimum circuit update cost.",
 "test": "Compute exact per-layer residual transition circuit minima and compare with joint encoding synthesis over all encodings; a discrepancy in the predicted minimum update cost refutes any stronger claim that residual counts determine circuit cost.",
 "prev": "7b7275d5697fc51abf48c019349ab5cbb8cf96b51ef581f6a69cc962f9e2adbf",
 "hash": "14bd1bd651425cb62b150c3819b12c0c5c065d9960f9f7055301fe68222fc9e4"
}
```
