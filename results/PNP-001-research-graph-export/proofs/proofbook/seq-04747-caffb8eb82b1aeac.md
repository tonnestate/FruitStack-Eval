# Proofbook seq 4747 — HYPOTHESIS

- key: `caffb8eb82b1aeac`
- at: 1795161848.5496635
- mission: agent/pnp-desk/research/R0383:claude-haiku-5-5@default
- hash: `2002db0827778a0aeac057bd335253b9b6d169918526cbe073559645fe7a57b7` (prev `8543ac346b9da22775cb1ba2476e45afb98a5339a09c9776ee49b13c116dcf67`)
- graph nodes: PB:2002db0827778a0aeac057bd335253b9b6d169918526cbe073559645fe7a57b7
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

PC degree over GF(2), GF(3) and GF(5) coincides for every positive or general 3-CNF formula, so the PC degree is characteristic-independent on the tested families.

## Full row (verbatim JSON)

```json
{
 "seq": 4747,
 "at": 1795161848.5496635,
 "problem": "p_vs_np",
 "mission": "agent/pnp-desk/research/R0383:claude-haiku-5-5@default",
 "key": "caffb8eb82b1aeac",
 "kind": "HYPOTHESIS",
 "origin": "agent",
 "parent": "Q-1a23334620",
 "scope": "Conjectured only for the 48-row n=7..10 table; the 24-row n=11,12 table is too small for exact law search.",
 "statement": "PC degree over GF(2), GF(3) and GF(5) coincides for every positive or general 3-CNF formula, so the PC degree is characteristic-independent on the tested families.",
 "test": "Refuted by any formula with pc_gf3 != pc_gf2 or pc_gf5 != pc_gf2. Search (a) n=11,12 with at least 40 rows from a generator matching v2, and (b) structured families where mod-3 coefficients could matter (e.g. 1-in-3 instances, where the GF(3) affine structure is present), then test with exact law search.",
 "prev": "8543ac346b9da22775cb1ba2476e45afb98a5339a09c9776ee49b13c116dcf67",
 "hash": "2002db0827778a0aeac057bd335253b9b6d169918526cbe073559645fe7a57b7"
}
```
