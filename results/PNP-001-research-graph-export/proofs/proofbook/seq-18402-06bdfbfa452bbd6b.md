# Proofbook seq 18402 — CONNECTION

- key: `06bdfbfa452bbd6b`
- at: 1795856411.6976907
- mission: agent/pnp-desk/research/CLAUDE-LEAD:claude-sonnet-5-5@default
- hash: `c6e0a81b98a39b5c7f60ab5d0252991011af70c1de764db75341b00967221856` (prev `4b87d175e2401f434c6b0082b4c75b5c84aff078ef0370b84f210c25020f9579`)
- graph nodes: PB:c6e0a81b98a39b5c7f60ab5d0252991011af70c1de764db75341b00967221856
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)



## Full row (verbatim JSON)

```json
{
 "seq": 18402,
 "at": 1795856411.6976907,
 "problem": "p_vs_np",
 "mission": "agent/pnp-desk/research/CLAUDE-LEAD:claude-sonnet-5-5@default",
 "key": "06bdfbfa452bbd6b",
 "kind": "CONNECTION",
 "about": [
  "comp:koopman-lucas-period-duality"
 ],
 "bingo": {
  "record": "COMPOSITION",
  "id": "comp:koopman-lucas-period-duality",
  "stage": "DERIVE",
  "name": "Koopman-Lucas period duality",
  "sources": [
   "mech:nilpotent-koopman-binomial-expansion",
   "mech:lucas-binomial-periodicity"
  ],
  "construction": "",
  "domains": [
   "dynamical systems",
   "number theory"
  ],
  "derived_properties": [
   "Thm 7.1 (T66 sec.7): minimal period of T->g(F^T x) is exactly p^ceil(log_p r) for nilpotency index r [proof + 60 random systems + counters]",
   "Thm 7.2: K unipotent iff all cycle lengths are powers of p; index <= longest cycle [300 random permutations]",
   "Nilpotent compression = reduction of T modulo the observation period (no compression beyond period)",
   "Compression beyond periodicity requires non-nilpotent K with high-order minimal polynomial (LFSR: period 65535 at dimension 16, T=5e5 verified)"
  ]
 },
 "connection": "COMPOSITION comp:koopman-lucas-period-duality [DERIVE] from mech:nilpotent-koopman-binomial-expansion, mech:lucas-binomial-periodicity: Thm 7.1 (T66 sec.7): minimal period of T->g(F^T x) is exactly p^ceil(log_p r) for nilpotency index r [proof + 60 random systems + counters]; Thm 7.2: K unipotent iff all cycle lengths are powers of p; index <= longest cycle [300 random permutations]; Nilpotent compression = reduction of T modulo the",
 "origin": "agent",
 "prev": "4b87d175e2401f434c6b0082b4c75b5c84aff078ef0370b84f210c25020f9579",
 "hash": "c6e0a81b98a39b5c7f60ab5d0252991011af70c1de764db75341b00967221856"
}
```
