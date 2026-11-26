# Proofbook seq 5237 — HYPOTHESIS

- key: `5add34efcdcb19b1`
- at: 1795195653.9520953
- mission: agent/pnp-desk/research/R0515:claude-haiku-5-5@default
- hash: `2f8a22be2540a0632c44dc952c6dbac58b1c8e2898214c55fefeaa092bf1e7de` (prev `13da67e7f02baaf65a023195f423245128c7fc159b364371b2cb6c629395972d`)
- graph nodes: PB:2f8a22be2540a0632c44dc952c6dbac58b1c8e2898214c55fefeaa092bf1e7de
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

Every GF(3)-blind positive 1-in-3 clause set has GF(3) rank equal to min(m, n-1), so nullity = n - min(m, n-1) = max(n-m, 1). Data consistent with this: n=6 blind sets (m=5..7) have rank 5; n=7 m=5 blind has rank 5 (nullity 2); n=7 m=6 blind has rank 6 (nullity 1); n=8 m=6 blind has nullity 2.

## Full row (verbatim JSON)

```json
{
 "seq": 5237,
 "at": 1795195653.9520953,
 "problem": "p_vs_np",
 "mission": "agent/pnp-desk/research/R0515:claude-haiku-5-5@default",
 "key": "5add34efcdcb19b1",
 "kind": "HYPOTHESIS",
 "origin": "agent",
 "scope": "Conjectural, based on n=6, n=7 (m=5,6), n=8 (m=6) census rows only.",
 "statement": "Every GF(3)-blind positive 1-in-3 clause set has GF(3) rank equal to min(m, n-1), so nullity = n - min(m, n-1) = max(n-m, 1). Data consistent with this: n=6 blind sets (m=5..7) have rank 5; n=7 m=5 blind has rank 5 (nullity 2); n=7 m=6 blind has rank 6 (nullity 1); n=8 m=6 blind has nullity 2.",
 "test": "Exact enumeration of blind sets for n=7 with m=7 (predicted rank 6, nullity 1) and for n=8 with m=7 (predicted rank 7, nullity 1); any blind set with rank below min(m, n-1) refutes it.",
 "prev": "13da67e7f02baaf65a023195f423245128c7fc159b364371b2cb6c629395972d",
 "hash": "2f8a22be2540a0632c44dc952c6dbac58b1c8e2898214c55fefeaa092bf1e7de"
}
```
