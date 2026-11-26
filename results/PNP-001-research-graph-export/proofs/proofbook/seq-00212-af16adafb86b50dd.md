# Proofbook seq 212 — REFUTATION

- key: `af16adafb86b50dd`
- at: 1794915383.9450905
- mission: pi-research-2026-11-17-padding-floor-refuted
- hash: `f8cbe48c4ad38268477af93b539a11d8407c7831444a0a838e562609f0fe9ee9` (prev `9431e1b112de384b5e2517bbdada58a7937d3d2eaaa69d9739b77c4af9f37721`)
- graph nodes: PB:f8cbe48c4ad38268477af93b539a11d8407c7831444a0a838e562609f0fe9ee9
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

Padding-floor EQUIVALENCE REFUTED (certified counterexample, independently verified); proven (<=) direction retained; replaced by a TWO-CONDITION necessary filter. COUNTEREXAMPLE (owner): (m,n,d)=(2,3,6), lambda=(8,2,2,2,2,2)|-18 has p_lambda>0 and lambda_1=8 >= d(n-m)=6, but gamma_lambda(Y_{2,3})=0. MECHANISM: the HWV P(F)=det((A_{1ij})_{1<=i,j<=6}) (6x6 contraction of the cubic's symmetric coefficient tensor) has weight (8,2,2,2,2,2); the padded permanent z*perm_2 uses only m^2+1=5 essential variables, so the 6x6 contraction has rank<=5 and determinant 0 => vanishes on all of Y_{2,3}. Not identically zero: F_0=x_1^3+3x_1(x_2^2+..+x_6^2) gives contraction=I_6, P(F_0)=1. VERIFIED by exact sympy: z*perm_2 -> rank 4 det 0; random g.f -> rank 5 det 0; F_0 -> rank 6 det 6^6. Generalizes (r=m^2+2) to an infinite counterexample family; subspace-variety geometry (classical, Landsberg). CORRECTED THEOREM (two NECESSARY, neither sufficient): gamma_lambda(Y_{m,n})>0 => lambda_1 >= d(n-m) (padding floor, proven) AND ell(lambda) <= m^2+1 (essential-variable / subspace-variety bound, Y subset Sub_{m^2+1}). AutoML now filters candidates by BOTH independent geometric criteria. The learning loop worked as intended: hypothesis -> targeted counterexample -> a stronger, certified search filter.

## Full row (verbatim JSON)

```json
{
 "seq": 212,
 "at": 1794915383.9450905,
 "problem": "p_vs_np",
 "mission": "pi-research-2026-11-17-padding-floor-refuted",
 "key": "af16adafb86b50dd",
 "kind": "REFUTATION",
 "document": "/root/fruits/research/PNP-001/theory/T11O-padding-floor.md",
 "evidence": "sympy: 6x6 contraction of z*perm_2 rank 4 det 0, of random g.f rank 5 det 0, of F_0 rank 6 det 6^6; (8,2,2,2,2,2) ell=6 > m^2+1=5",
 "parent": "pi-research-2026-11-17-padding-floor-theorem",
 "statement": "Padding-floor EQUIVALENCE REFUTED (certified counterexample, independently verified); proven (<=) direction retained; replaced by a TWO-CONDITION necessary filter. COUNTEREXAMPLE (owner): (m,n,d)=(2,3,6), lambda=(8,2,2,2,2,2)|-18 has p_lambda>0 and lambda_1=8 >= d(n-m)=6, but gamma_lambda(Y_{2,3})=0. MECHANISM: the HWV P(F)=det((A_{1ij})_{1<=i,j<=6}) (6x6 contraction of the cubic's symmetric coefficient tensor) has weight (8,2,2,2,2,2); the padded permanent z*perm_2 uses only m^2+1=5 essential variables, so the 6x6 contraction has rank<=5 and determinant 0 => vanishes on all of Y_{2,3}. Not identically zero: F_0=x_1^3+3x_1(x_2^2+..+x_6^2) gives contraction=I_6, P(F_0)=1. VERIFIED by exact sympy: z*perm_2 -> rank 4 det 0; random g.f -> rank 5 det 0; F_0 -> rank 6 det 6^6. Generalizes (r=m^2+2) to an infinite counterexample family; subspace-variety geometry (classical, Landsberg). CORRECTED THEOREM (two NECESSARY, neither sufficient): gamma_lambda(Y_{m,n})>0 => lambda_1 >= d(n-m) (padding floor, proven) AND ell(lambda) <= m^2+1 (essential-variable / subspace-variety bound, Y subset Sub_{m^2+1}). AutoML now filters candidates by BOTH independent geometric criteria. The learning loop worked as intended: hypothesis -> targeted counterexample -> a stronger, certified search filter.",
 "prev": "9431e1b112de384b5e2517bbdada58a7937d3d2eaaa69d9739b77c4af9f37721",
 "hash": "f8cbe48c4ad38268477af93b539a11d8407c7831444a0a838e562609f0fe9ee9"
}
```
