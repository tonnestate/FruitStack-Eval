# Proofbook seq 13428 — HYPOTHESIS

- key: `b7cfd195feeccd19`
- at: 1795515334.5390215
- mission: agent/pnp-desk/research/R2648:gpt-6-luna@default
- hash: `d87c53f07c014bd6af5e46722039594d0e2ebd9178b3028b6822de4054c40d92` (prev `9b778fd7c5a41ad2bc4db06f2d7c4e33c6a4dc373a107d3814b7e219f2124848`)
- graph nodes: PB:d87c53f07c014bd6af5e46722039594d0e2ebd9178b3028b6822de4054c40d92
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

For the Q-10bbdfaf2a circuit model, the ordered-DAG description count combined with the entropy neighborhood bound yields a nontrivial robust typical-function separation for gate thresholds s satisfying log2 D(m,s) < 2^m*(1-H_2(delta)).

## Full row (verbatim JSON)

```json
{
 "seq": 13428,
 "at": 1795515334.5390215,
 "problem": "p_vs_np",
 "mission": "agent/pnp-desk/research/R2648:gpt-6-luna@default",
 "key": "b7cfd195feeccd19",
 "kind": "HYPOTHESIS",
 "origin": "agent",
 "scope": "Finite/infinite parameter inequality conditional on the chosen valid D(m,s); no implication to MCSP decision-circuit lower bounds is asserted.",
 "statement": "For the Q-10bbdfaf2a circuit model, the ordered-DAG description count combined with the entropy neighborhood bound yields a nontrivial robust typical-function separation for gate thresholds s satisfying log2 D(m,s) < 2^m*(1-H_2(delta)).",
 "test": "Substitute an independently valid description-count upper bound D(m,s) and check the inequality for explicit growing parameter choices; the claim fails at any proposed parameters where log2 D(m,s) >= 2^m*(1-H_2(delta)). This predicts separation of random truth tables from low-gate truth tables, not hardness of MCSP itself.",
 "prev": "9b778fd7c5a41ad2bc4db06f2d7c4e33c6a4dc373a107d3814b7e219f2124848",
 "hash": "d87c53f07c014bd6af5e46722039594d0e2ebd9178b3028b6822de4054c40d92"
}
```
