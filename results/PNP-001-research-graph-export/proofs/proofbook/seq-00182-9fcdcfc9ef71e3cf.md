# Proofbook seq 182 — REFUTATION

- key: `9fcdcfc9ef71e3cf`
- at: 1794902632.5240698
- mission: pi-research-2026-11-17-T11F-d2-resolved
- hash: `18f489093ac93c9509fb8fdd3973e9546006499fa948e0bb4a1b2e35a04004d1` (prev `800711d090c326f26d586c2e1ebdd953e75bb4c46eac9add2a9d6fa01c2b58bf`)
- graph nodes: PB:18f489093ac93c9509fb8fdd3973e9546006499fa948e0bb4a1b2e35a04004d1
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

T11-F: CORRECTS T11-E and RESOLVES d=2. T11-E's candidate filter {g=0 & lambda_1>=(n-m)d} missed the necessary AMBIENT condition a_lambda <= p_lambda = mult of S_lambda in Sym^d(Sym^n W) (the coordinate ring sits in Sym^d(Sym^n W*)). For d=2, Sym^2(Sym^n W) = direct sum over i of S_{(2n-2i,2i)} (classical; verified via power-sum plethysm): ONLY two-row partitions with even second part occur, each with p_lambda=1. Verified occurring lambda: n=4:{(8),(6,2),(4,4)}; n=5:{(10),(8,2),(6,4)}; n=6:{(12),(10,2),(8,4),(6,6)}. For EVERY one, the rectangular Kronecker g(lambda,(2^n),(2^n))>0 (none vanish). Hence NO occurrence obstruction (needs g=0) AND no multiplicity obstruction (a_lambda<=p_lambda=1, would need delta_lambda=0 i.e. g=0) for perm_3 vs det_n at d=2, n in {4,5,6}. VERIFIED NEGATIVE result; almost all 14/20/21 T11-E candidates are excluded simply by a_lambda<=p_lambda=0 (>=3 rows). Obstructions can only appear at d>=3 where the plethysm admits multi-row lambda.

## Full row (verbatim JSON)

```json
{
 "seq": 182,
 "at": 1794902632.5240698,
 "problem": "p_vs_np",
 "mission": "pi-research-2026-11-17-T11F-d2-resolved",
 "key": "9fcdcfc9ef71e3cf",
 "kind": "REFUTATION",
 "evidence": "own verified engine: power-sum plethysm h_2[h_n] Schur-expanded = classical 2-row result; rectangular Kronecker g>0 on all occurring lambda; sum-rule-verified character engine (T11-C)",
 "parent": "T11-E",
 "statement": "T11-F: CORRECTS T11-E and RESOLVES d=2. T11-E's candidate filter {g=0 & lambda_1>=(n-m)d} missed the necessary AMBIENT condition a_lambda <= p_lambda = mult of S_lambda in Sym^d(Sym^n W) (the coordinate ring sits in Sym^d(Sym^n W*)). For d=2, Sym^2(Sym^n W) = direct sum over i of S_{(2n-2i,2i)} (classical; verified via power-sum plethysm): ONLY two-row partitions with even second part occur, each with p_lambda=1. Verified occurring lambda: n=4:{(8),(6,2),(4,4)}; n=5:{(10),(8,2),(6,4)}; n=6:{(12),(10,2),(8,4),(6,6)}. For EVERY one, the rectangular Kronecker g(lambda,(2^n),(2^n))>0 (none vanish). Hence NO occurrence obstruction (needs g=0) AND no multiplicity obstruction (a_lambda<=p_lambda=1, would need delta_lambda=0 i.e. g=0) for perm_3 vs det_n at d=2, n in {4,5,6}. VERIFIED NEGATIVE result; almost all 14/20/21 T11-E candidates are excluded simply by a_lambda<=p_lambda=0 (>=3 rows). Obstructions can only appear at d>=3 where the plethysm admits multi-row lambda.",
 "prev": "800711d090c326f26d586c2e1ebdd953e75bb4c46eac9add2a9d6fa01c2b58bf",
 "hash": "18f489093ac93c9509fb8fdd3973e9546006499fa948e0bb4a1b2e35a04004d1"
}
```
