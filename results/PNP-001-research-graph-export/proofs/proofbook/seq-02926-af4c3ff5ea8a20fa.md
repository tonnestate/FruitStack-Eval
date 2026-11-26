# Proofbook seq 2926 — HYPOTHESIS

- key: `af4c3ff5ea8a20fa`
- at: 1795096677.05192
- mission: agent/pnp-desk/research/R0188:nemotron-3-ultra-550b@default
- hash: `1f97dec694bd1beaea7480085d67bdd5c0f0ff269b9cd1ff9904dbeea2fc5eb3` (prev `c405fd4d047d0e54ad14d4da0582ab165ac751d69dbf9e9f54d8937e9cca095e`)
- graph nodes: PB:1f97dec694bd1beaea7480085d67bdd5c0f0ff269b9cd1ff9904dbeea2fc5eb3
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

For positive 1-in-3 SAT: if a formula has GF(2) rank ≤ 4 and is GF(3)-consistent (cons3=1), then it is satisfiable (sat=1). Equivalently, every counterexample to 'cons3=1 ⇒ sat=1' has GF(2) rank ≥ 5.

## Full row (verbatim JSON)

```json
{
 "seq": 2926,
 "at": 1795096677.05192,
 "problem": "p_vs_np",
 "mission": "agent/pnp-desk/research/R0188:nemotron-3-ultra-550b@default",
 "key": "af4c3ff5ea8a20fa",
 "kind": "HYPOTHESIS",
 "origin": "agent",
 "scope": "All positive 1-in-3 formulas. This is a finite-table conjecture based on n≤8 data.",
 "statement": "For positive 1-in-3 SAT: if a formula has GF(2) rank ≤ 4 and is GF(3)-consistent (cons3=1), then it is satisfiable (sat=1). Equivalently, every counterexample to 'cons3=1 ⇒ sat=1' has GF(2) rank ≥ 5.",
 "test": "Generate positive 1-in-3 formulas for n=9..15 with GF(2) rank 4 and cons3=1, check if any has sat=0. Search for a rank-4 counterexample at larger n.",
 "prev": "c405fd4d047d0e54ad14d4da0582ab165ac751d69dbf9e9f54d8937e9cca095e",
 "hash": "1f97dec694bd1beaea7480085d67bdd5c0f0ff269b9cd1ff9904dbeea2fc5eb3"
}
```
