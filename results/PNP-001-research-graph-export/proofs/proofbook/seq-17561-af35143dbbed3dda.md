# Proofbook seq 17561 — PROOF_STEP

- key: `af35143dbbed3dda`
- at: 1795742229.3962688
- mission: director/closure-exclusions
- hash: `12880031e61b9c71196a80d24fd4b5db543ed83af96fd11ca5bf21ba76ce187f` (prev `2c902c8acb9a3100b81c4c69c93600761920ef10c6109cd6ef810548985a1b44`)
- graph nodes: PB:12880031e61b9c71196a80d24fd4b5db543ed83af96fd11ca5bf21ba76ce187f
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

EXACT COUNTING TRANSFER to colourings and to F(G) (owner gadgets 2026-11-27; PI verification count_transfer_check.py, fg_cov_check.py; CLAIMED, Claude family). (1) Clause gadget: a or b or c -> NAE(a,b,z), NAE(not z,c,0), NAE(not z,not a,0), NAE(not z,not b,0). NAE(x,y,0) is x or y, so z = 1 forces a = b = 0 and c = 1, and z = 0 forces a or b; the extension is unique (z = not(a or b)) iff the clause holds. Table 8/8. (2) Colouring graph: reference triangle T, F, B; literal triangles (x, not x, B); one NAE triangle v1 v2 v3 with v_i adjacent to its literal (constant 0 = F). A satisfied NAE gadget has exactly 2 internal colourings, an all-equal one has none. P_{G_phi}(3) = 6 * 2^{4m} * #SAT(phi). Checked 12/12 random 3-CNF with exact colouring counts. (3) Weighted removal: Q_G(X) = sum over proper sigma of prod_v X_{v,sigma(v)}. Char != 2: weight 1/2 on one internal vertex per gadget. Char 2: over F_4 with omega^2 + omega + 1 = 0, weights v1 (1,1,1), v2 (omega,omega^2,1), v3 (omega^2,omega,1); the gadget sum is 1 on NAE inputs and 0 otherwise, verified 8/8 for all 6 choices of reference colours. (4) Projection: take the parsimonious tableau 3-CNF Psi_n of the clocked machine (branch choice recorded, idle padding, Tseitin auxiliaries determined; 17548) with free inputs x. Set G_n = colouring graph of Psi_n and let pi be: reference vertices X_{ref,c} = [c = designated colour] (removes the factor 6); positive literal vertex of x_i: X_{T} = X_{i,1}, X_{F} = X_{i,0}, X_{B} = 0; gadget weights as in (3); every other variable 1. Then pi(Q_{G_n}) = sum_x U_n(x) prod_i X_{i,x_i} = P_n over every field K with char K != 2 or omega in K. For char 2 without omega: size_K(Q) >= size_{K(omega)}(Q) >= size_{K(omega)}(P_n). Size |G_n| = O(|Psi_n|) = O(T^2), T = n^{10^9}. (5) F(G): variables x_{v,c}, y_{e,c}; EO(x_{v,1},x_{v,2},x_{v,3}) and EO(x_{u,c},x_{w,c},y_{e,c}). y_{e,c} = 1 - x_{u,c} - x_{w,c} is forced and lies in {0,1} iff not both endpoints have colour c, so the solutions are in bijection with proper colourings (checked on random graphs). Weights X_{v,c} on x_{v,c} and 1 on y give Gen_{F(G)} = Q_G, coefficient by coefficient; hence P_n = pi(Gen_{F(G_n)}). SEPARATION OF LEVELS: (i) counting transfer: established here (CLAIMED until cross-family review); (ii) arithmetic lower bound for P_n, hence for Q_{G_n} and Gen_{F(G_n)}: OpenAI's claim, unreviewed and not built; (iii) Boolean decision lower bound: none, since Q_{G_n} is a generating polynomial and the decision version is a different object (17540).

## Full row (verbatim JSON)

```json
{
 "seq": 17561,
 "at": 1795742229.3962688,
 "problem": "p_vs_np",
 "mission": "director/closure-exclusions",
 "key": "af35143dbbed3dda",
 "kind": "PROOF_STEP",
 "conclusion": "EXACT COUNTING TRANSFER to colourings and to F(G) (owner gadgets 2026-11-27; PI verification count_transfer_check.py, fg_cov_check.py; CLAIMED, Claude family). (1) Clause gadget: a or b or c -> NAE(a,b,z), NAE(not z,c,0), NAE(not z,not a,0), NAE(not z,not b,0). NAE(x,y,0) is x or y, so z = 1 forces a = b = 0 and c = 1, and z = 0 forces a or b; the extension is unique (z = not(a or b)) iff the clause holds. Table 8/8. (2) Colouring graph: reference triangle T, F, B; literal triangles (x, not x, B); one NAE triangle v1 v2 v3 with v_i adjacent to its literal (constant 0 = F). A satisfied NAE gadget has exactly 2 internal colourings, an all-equal one has none. P_{G_phi}(3) = 6 * 2^{4m} * #SAT(phi). Checked 12/12 random 3-CNF with exact colouring counts. (3) Weighted removal: Q_G(X) = sum over proper sigma of prod_v X_{v,sigma(v)}. Char != 2: weight 1/2 on one internal vertex per gadget. Char 2: over F_4 with omega^2 + omega + 1 = 0, weights v1 (1,1,1), v2 (omega,omega^2,1), v3 (omega^2,omega,1); the gadget sum is 1 on NAE inputs and 0 otherwise, verified 8/8 for all 6 choices of reference colours. (4) Projection: take the parsimonious tableau 3-CNF Psi_n of the clocked machine (branch choice recorded, idle padding, Tseitin auxiliaries determined; 17548) with free inputs x. Set G_n = colouring graph of Psi_n and let pi be: reference vertices X_{ref,c} = [c = designated colour] (removes the factor 6); positive literal vertex of x_i: X_{T} = X_{i,1}, X_{F} = X_{i,0}, X_{B} = 0; gadget weights as in (3); every other variable 1. Then pi(Q_{G_n}) = sum_x U_n(x) prod_i X_{i,x_i} = P_n over every field K with char K != 2 or omega in K. For char 2 without omega: size_K(Q) >= size_{K(omega)}(Q) >= size_{K(omega)}(P_n). Size |G_n| = O(|Psi_n|) = O(T^2), T = n^{10^9}. (5) F(G): variables x_{v,c}, y_{e,c}; EO(x_{v,1},x_{v,2},x_{v,3}) and EO(x_{u,c},x_{w,c},y_{e,c}). y_{e,c} = 1 - x_{u,c} - x_{w,c} is forced and lies in {0,1} iff not both endpoints have colour c, so the solutions are in bijection with proper colourings (checked on random graphs). Weights X_{v,c} on x_{v,c} and 1 on y give Gen_{F(G)} = Q_G, coefficient by coefficient; hence P_n = pi(Gen_{F(G_n)}). SEPARATION OF LEVELS: (i) counting transfer: established here (CLAIMED until cross-family review); (ii) arithmetic lower bound for P_n, hence for Q_{G_n} and Gen_{F(G_n)}: OpenAI's claim, unreviewed and not built; (iii) Boolean decision lower bound: none, since Q_{G_n} is a generating polynomial and the decision version is a different object (17540).",
 "premises": [
  17540,
  17548,
  17549
 ],
 "prev": "2c902c8acb9a3100b81c4c69c93600761920ef10c6109cd6ef810548985a1b44",
 "hash": "12880031e61b9c71196a80d24fd4b5db543ed83af96fd11ca5bf21ba76ce187f"
}
```
