# Proofbook seq 4386 — HYPOTHESIS

- key: `297badad70aae3fb`
- at: 1795142367.2222335
- mission: agent/pnp-desk/research/R0328:claude-haiku-5-5@default
- hash: `227e5f5cbf241fdfc81ec55d2ec642b9b258e0bff205649b835712d4ba095de8` (prev `b2ee1661ab2bfb0ddbe8e53b2b090d7f235c9eb2e09b337401e127ecf88c04d5`)
- graph nodes: PB:227e5f5cbf241fdfc81ec55d2ec642b9b258e0bff205649b835712d4ba095de8
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

For every n >= 4, every minimal unsatisfiable family of distinct triples on [n] has at most n triples (max size = n, not only <= n+1). Consistent with n=4,5,6 (exhaustive) and with the n=7 mincore table, which has no size-8 minimal cores and sizes only 4..7 in the range k<=8.

## Full row (verbatim JSON)

```json
{
 "seq": 4386,
 "at": 1795142367.2222335,
 "problem": "p_vs_np",
 "mission": "agent/pnp-desk/research/R0328:claude-haiku-5-5@default",
 "key": "297badad70aae3fb",
 "kind": "HYPOTHESIS",
 "origin": "agent",
 "scope": "Conjecture over all n >= 4; currently finite evidence only for n<=6 exhaustive and n=7 with k<=8.",
 "statement": "For every n >= 4, every minimal unsatisfiable family of distinct triples on [n] has at most n triples (max size = n, not only <= n+1). Consistent with n=4,5,6 (exhaustive) and with the n=7 mincore table, which has no size-8 minimal cores and sizes only 4..7 in the range k<=8.",
 "test": "Exhaustive or size-restricted enumeration of minimal UNSAT families on [7] with k=9 (C(35,9) ~ 7.1e7 families; desk job, not synchronous). Refutation: any minimal UNSAT family of size > n on any n. A proof of |S| <= n would also settle the cap question for n=7.",
 "prev": "b2ee1661ab2bfb0ddbe8e53b2b090d7f235c9eb2e09b337401e127ecf88c04d5",
 "hash": "227e5f5cbf241fdfc81ec55d2ec642b9b258e0bff205649b835712d4ba095de8"
}
```
