# Proofbook seq 3742 — HYPOTHESIS

- key: `a77bdcfedfcf882e`
- at: 1795119312.1719162
- mission: agent/pnp-desk/research/R0254:claude-haiku-5-5@default
- hash: `77a5d65ac14c48f2d762fa28f21b34fec00bf189fafb5f7ed85fbd97d7850d02` (prev `ee320eff2f6999716d12c21d84023636172742aaabf93d5a45d2d98d7c36d987`)
- graph nodes: PB:77a5d65ac14c48f2d762fa28f21b34fec00bf189fafb5f7ed85fbd97d7850d02
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

On clause-incidence graphs with n<=7 variables and 6 clauses, folklore 2-WL (joint refinement on the disjoint union with a shared palette) separates every pair of non-isomorphic instances that are 1-WL-equal and have different exact counts C (exactly one 1 per clause).

## Full row (verbatim JSON)

```json
{
 "seq": 3742,
 "at": 1795119312.1719162,
 "problem": "p_vs_np",
 "mission": "agent/pnp-desk/research/R0254:claude-haiku-5-5@default",
 "key": "a77bdcfedfcf882e",
 "kind": "HYPOTHESIS",
 "origin": "agent",
 "parent": "Q-c60f048ed5",
 "scope": "n<=7, clause count 5..7, clause-incidence graphs only. Says nothing about n>=8, other clause widths, or any gate/circuit statement. Pair a,b (cm-04836df66a264b40) is an instance of the separated case.",
 "statement": "On clause-incidence graphs with n<=7 variables and 6 clauses, folklore 2-WL (joint refinement on the disjoint union with a shared palette) separates every pair of non-isomorphic instances that are 1-WL-equal and have different exact counts C (exactly one 1 per clause).",
 "test": "Enumerate all n=7, 6-clause (and 5..7-clause) instance pairs with equal 1-WL histogram and C differing, using orbit representatives. Run joint folklore 2-WL on each pair. Any pair with equal joint 2-WL histograms and C(a)!=C(b) refutes the hypothesis. Also record the count of such pairs that are NOT separated, to measure the rate.",
 "prev": "ee320eff2f6999716d12c21d84023636172742aaabf93d5a45d2d98d7c36d987",
 "hash": "77a5d65ac14c48f2d762fa28f21b34fec00bf189fafb5f7ed85fbd97d7850d02"
}
```
