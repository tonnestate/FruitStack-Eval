# PNP-001 research-graph export

Snapshot of the PNP-001 research graph (DuckDB) and the append-only proofbook, exported verbatim. Proofbook up to seq 18816; graph ingested up to seq 18816.
Nothing here claims P != NP. Status fields are copied as stored: CLAIMED != proved; edges are CANDIDATE unless a review in `reviews/` says otherwise.

Retrieval:
1. `MANIFEST.json`: inventory, checksums, counts. `GRAPH-SCHEMA.json`: field and edge semantics, mapping to the requested relationship types (null = not present).
2. Find a node: `indexes/node-locator/RANGES.json` -> shard -> entry gives node file path, proofbook seqs, in/out adjacency.
3. Find a proofbook row: `proofs/proofbook/seq-NNNNN.md` (result-type rows) or `history/proofbook/proofbook-*.jsonl` (all rows, hash chain fields `hash`/`prev`).
4. Priority subgraphs: `subgraphs/INDEX.json` (P1-P7 keyword selections, P8 complete obligations). Named results (Theorems 12/14/16, Lemma 15, M9, ...): `subgraphs/P2-algebraic-proof-systems/NAMED-RESULTS.json`.
5. The 12 navigation indexes: `indexes/INDEX.json`. Integrity: `integrity/INTEGRITY.json`.
6. Long-form proofs/reports: `proofs/documents/` (lab and theory reports), syntheses in `proofs/syntheses/`, Lean in `reviews/formal/`.
