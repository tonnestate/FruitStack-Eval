# Proofbook seq 17158 — PROOF_STEP

- key: `dccfb0b3dff459c1`
- at: 1795727556.8734896
- mission: director/closure-exclusions
- hash: `f4505cfe9df5657ade0b35e471479cad971cfea7bde4738714404638b3d72d1e` (prev `14ea402c1a8f6406deef2bb06691c64dec9f77ce76cd21264d1532b0028d3c79`)
- graph nodes: PB:f4505cfe9df5657ade0b35e471479cad971cfea7bde4738714404638b3d72d1e
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

MECH-RANGE (parameter check against OPS21/Q2, seq 16795-16796): in AF with a PRG of seed s^{c+o(1)} (CKLM19: c = 1/3, seq 16757), stars >= N^{beta+eta/2} force p >= N^{beta+eta/2-1}; with the unconditional worst case s = p L, L = N^{1+eps} (D4-SIM), seed <= N^{beta-eta} needs c(beta + eta/2 + eps) <= beta - eta, so eps/beta < 1/c - 1 (c = 1/3: eps < 2beta). Hence eps(beta)/beta stays bounded for every fixed c and the mechanism cannot reach Q2 without a structural change. Two levers only: (i) c -> 0, a PRG for size-s De Morgan formulas with seed s^{o(1)}, which implies a function in E without polynomial-size De Morgan formulas (open, far beyond the known n^{3-o(1)}); (ii) a bound on the number m of principal formulas: with a Tal-type forest bound (P2) s <~ p^2 L + p sqrt(m L), Q2 requires m <= N^{1-eps+4beta-7eta} at total size N^{1+eps} with eps/beta -> infinity. The 'fundamental change' asked for by the owner is therefore a reduction of m (count of reused gates), not of W; this is a necessary condition, not a construction.

## Full row (verbatim JSON)

```json
{
 "seq": 17158,
 "at": 1795727556.8734896,
 "problem": "p_vs_np",
 "mission": "director/closure-exclusions",
 "key": "dccfb0b3dff459c1",
 "kind": "PROOF_STEP",
 "conclusion": "MECH-RANGE (parameter check against OPS21/Q2, seq 16795-16796): in AF with a PRG of seed s^{c+o(1)} (CKLM19: c = 1/3, seq 16757), stars >= N^{beta+eta/2} force p >= N^{beta+eta/2-1}; with the unconditional worst case s = p L, L = N^{1+eps} (D4-SIM), seed <= N^{beta-eta} needs c(beta + eta/2 + eps) <= beta - eta, so eps/beta < 1/c - 1 (c = 1/3: eps < 2beta). Hence eps(beta)/beta stays bounded for every fixed c and the mechanism cannot reach Q2 without a structural change. Two levers only: (i) c -> 0, a PRG for size-s De Morgan formulas with seed s^{o(1)}, which implies a function in E without polynomial-size De Morgan formulas (open, far beyond the known n^{3-o(1)}); (ii) a bound on the number m of principal formulas: with a Tal-type forest bound (P2) s <~ p^2 L + p sqrt(m L), Q2 requires m <= N^{1-eps+4beta-7eta} at total size N^{1+eps} with eps/beta -> infinity. The 'fundamental change' asked for by the owner is therefore a reduction of m (count of reused gates), not of W; this is a necessary condition, not a construction.",
 "premises": [
  "seq 16762 (AF)",
  "seq 16757 (D1, CKLM19)",
  "seq 16796 (QO2, Q2)",
  "D4-SIM"
 ],
 "prev": "14ea402c1a8f6406deef2bb06691c64dec9f77ce76cd21264d1532b0028d3c79",
 "hash": "f4505cfe9df5657ade0b35e471479cad971cfea7bde4738714404638b3d72d1e"
}
```
