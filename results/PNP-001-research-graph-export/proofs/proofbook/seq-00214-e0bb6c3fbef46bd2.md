# Proofbook seq 214 — VERIFICATION

- key: `e0bb6c3fbef46bd2`
- at: 1794918135.5744197
- mission: PNP-001/T11-P
- hash: `411eddf2795b5da5eebe8a4ff14325feaa57290ba54aae5307da96415ba62ef3` (prev `97d01661f8a90a00b4489dc43f11b6db25c688b404ec37b924e9fbdc2c8acd7b`)
- graph nodes: PB:411eddf2795b5da5eebe8a4ff14325feaa57290ba54aae5307da96415ba62ef3
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

delta_lambda(D_4) = 1 = p_lambda for lambda=(6,6,6,4,2), degree 6 (multiplicity of S_lambda(V*) in the degree-6 functions on the orbit closure of det_4). The same highest weight function is nonzero on l*perm_3, so gamma_lambda(Y_{3,4}) = 1: this lambda gives no equation of D_4 and no separating equation. (6,6,4,4,4) not evaluated; degree-6 partitions with lambda_1>6 or more than five rows remain open; d_min^sep(3,4) stays in [6,24].

## Full row (verbatim JSON)

```json
{
 "seq": 214,
 "at": 1794918135.5744197,
 "problem": "p_vs_np",
 "mission": "PNP-001/T11-P",
 "key": "e0bb6c3fbef46bd2",
 "kind": "VERIFICATION",
 "evidence": "Tableau HWV P_T per Breiding-Ikenmeyer-Michalek-Hodges arXiv:2110.06608 Sec.4 (dagger), tableau rows 111122/223333/444455/5566/66. Exact: P_T expanded into 73100 monomials, all of weight lambda, R_k P_T = 0 for k=1..4; P_T(l^4)=0; P_T(24F)= -37673274855121317888 on det of an explicit integer 4x4 matrix of linear forms in 5 variables (three further sections also nonzero); = 1526056301511479551 mod 2305843009213693967. Cross-checks: merged-state contraction (3,320,118 transitions, 5 s, 71 MB) equals literal 298,598,400-term sum in C mod 2^31-1; control (4^5),d=5 vanishes on l*perm_3 sections k=0..3 and not on det_4. p_lambda=1 by Weyl sum over h_6[h_4] weight multiplicities (weight space 76288). Independent adversarial review: own C evaluator and own tensor, two 61-bit primes + CRT reproduce the exact value; normalisation, HWV tests, 5-variable reduction and p_lambda confirmed; no flaw. Files: /root/fruits/research/PNP-001/theory/T11P-tableau-witness-2026-11-17.md and theory/checks/t11p/.",
 "statement": "delta_lambda(D_4) = 1 = p_lambda for lambda=(6,6,6,4,2), degree 6 (multiplicity of S_lambda(V*) in the degree-6 functions on the orbit closure of det_4). The same highest weight function is nonzero on l*perm_3, so gamma_lambda(Y_{3,4}) = 1: this lambda gives no equation of D_4 and no separating equation. (6,6,4,4,4) not evaluated; degree-6 partitions with lambda_1>6 or more than five rows remain open; d_min^sep(3,4) stays in [6,24].",
 "prev": "97d01661f8a90a00b4489dc43f11b6db25c688b404ec37b924e9fbdc2c8acd7b",
 "hash": "411eddf2795b5da5eebe8a4ff14325feaa57290ba54aae5307da96415ba62ef3"
}
```
