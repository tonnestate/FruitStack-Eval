# Proofbook seq 61 — PROOF_STEP

- key: `b1dce1ddb3c4c64e`
- at: 1794840107.7005744
- mission: pi-theory-T1-T2
- hash: `9963a115318452c86ef1e44891128ee5f6ab05dff37fbe97da53fd7cb28f3223` (prev `8a28ee79e3d793d2e990bc7626b0131d80ee2ad12be3877954fa2590ccb7faf6`)
- graph nodes: PB:9963a115318452c86ef1e44891128ee5f6ab05dff37fbe97da53fd7cb28f3223
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

For bounded-degree expanders G, every variable order and every tree decomposition of F_G has a cut of rank 2^Omega(n) (T1 Satz 4)

## Full row (verbatim JSON)

```json
{
 "seq": 61,
 "at": 1794840107.7005744,
 "problem": "p_vs_np",
 "mission": "pi-theory-T1-T2",
 "key": "b1dce1ddb3c4c64e",
 "kind": "PROOF_STEP",
 "assumptions": [
  "Bounded-degree expanders with edge expansion h > 0 exist (random 3-regular graphs; Ramanujan graphs)"
 ],
 "checks": [
  "cm-79b294b8605b4c9e"
 ],
 "conclusion": "For bounded-degree expanders G, every variable order and every tree decomposition of F_G has a cut of rank 2^Omega(n) (T1 Satz 4)",
 "document": "/root/fruits/research/PNP-001/theory/T1-ie-compression-and-barrier.md#Satz4",
 "justification": "expansion gives >= h n/3 crossing edges at the separator edge; greedy lemma; Satz 3",
 "premises": [
  "For the positive 2-CNF F_G and every bipartition (L,R) of its variables, rank M_{L,R}(F_G) >= 2^mu(L,R), mu = largest induced matching across the cut (T1 Satz 3)",
  "The crossing edges of a cut in a graph of maximum degree D contain an induced matching of size at least e/(2 D^2) (T1 greedy lemma)",
  "Every linear order has a balanced cut, and every cubic tree with n leaves has an edge whose smaller side has between n/3 and n/2 leaves (T1 separator lemma)",
  "Bounded-degree expanders with edge expansion h > 0 exist (random 3-regular graphs; Ramanujan graphs)"
 ],
 "prev": "8a28ee79e3d793d2e990bc7626b0131d80ee2ad12be3877954fa2590ccb7faf6",
 "hash": "9963a115318452c86ef1e44891128ee5f6ab05dff37fbe97da53fd7cb28f3223"
}
```
