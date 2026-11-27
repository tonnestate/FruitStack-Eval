# Proofbook seq 17560 — CONNECTION

- key: `5a7dbdab1fce1c39`
- at: 1795742228.9939015
- mission: director/closure-exclusions
- hash: `2c902c8acb9a3100b81c4c69c93600761920ef10c6109cd6ef810548985a1b44` (prev `9e9eb7b98a4844a04ee5dc81af4c3b3f5dcd9a7a833f26e89e4d4db59274ccba`)
- graph nodes: PB:2c902c8acb9a3100b81c4c69c93600761920ef10c6109cd6ef810548985a1b44
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

RETRACTION of one sentence of 17554 + owner theorem (2026-11-27; PI check fg_cov_check.py; CLAIMED, Claude family). RETRACTED: 'computing C_G is as hard as the hull' (only 'at least as hard' holds). THEOREM (owner): (A) G bipartite implies W_G = Q^n (colour one side 1, the other from {2,3}; each vertex of the second side is its own (2,3)-component, so b_K = +-e_v; swap the roles of the sides), hence dim aff = 2n. (B) For any H on n vertices, B_k(H) (each edge replaced by k = 2n+1 internally disjoint length-2 paths) is bipartite with P_{B_k(H)}(3) = sum_j rho_H(j) 2^{kj}, so P_H(3) = P_{B_k(H)}(3) mod 2^k. (C) Adding the edges of a bipartite graph one at a time: P_{G_i}(3) = P_{G_{i-1}}(3) (2/3 - sum_c C_{G_{i-1}}[(u_i,c),(v_i,c)]), using colour symmetry E X_{u,c} = 1/3. So exact C_G on bipartite graphs is #P-hard under Turing reductions, although the hull is explicit there. Checks: (B) mod 2^k and (C) product exact on random small graphs, 0 violations. Known-type (#3-colouring on bipartite graphs is #P-complete; from memory, verify). Counting hardness, not a decision lower bound.

## Full row (verbatim JSON)

```json
{
 "seq": 17560,
 "at": 1795742228.9939015,
 "problem": "p_vs_np",
 "mission": "director/closure-exclusions",
 "key": "5a7dbdab1fce1c39",
 "kind": "CONNECTION",
 "premises": [
  17554
 ],
 "statement": "RETRACTION of one sentence of 17554 + owner theorem (2026-11-27; PI check fg_cov_check.py; CLAIMED, Claude family). RETRACTED: 'computing C_G is as hard as the hull' (only 'at least as hard' holds). THEOREM (owner): (A) G bipartite implies W_G = Q^n (colour one side 1, the other from {2,3}; each vertex of the second side is its own (2,3)-component, so b_K = +-e_v; swap the roles of the sides), hence dim aff = 2n. (B) For any H on n vertices, B_k(H) (each edge replaced by k = 2n+1 internally disjoint length-2 paths) is bipartite with P_{B_k(H)}(3) = sum_j rho_H(j) 2^{kj}, so P_H(3) = P_{B_k(H)}(3) mod 2^k. (C) Adding the edges of a bipartite graph one at a time: P_{G_i}(3) = P_{G_{i-1}}(3) (2/3 - sum_c C_{G_{i-1}}[(u_i,c),(v_i,c)]), using colour symmetry E X_{u,c} = 1/3. So exact C_G on bipartite graphs is #P-hard under Turing reductions, although the hull is explicit there. Checks: (B) mod 2^k and (C) product exact on random small graphs, 0 violations. Known-type (#3-colouring on bipartite graphs is #P-complete; from memory, verify). Counting hardness, not a decision lower bound.",
 "prev": "9e9eb7b98a4844a04ee5dc81af4c3b3f5dcd9a7a833f26e89e4d4db59274ccba",
 "hash": "2c902c8acb9a3100b81c4c69c93600761920ef10c6109cd6ef810548985a1b44"
}
```
