# Beweisbuch p_vs_np (AppleMe ProofLedger, append-only, hash-chained)

- `proofbook-p_vs_np-STAGING-kampagnen.jsonl` - 834 entries. The book the two research campaigns wrote into today (a staging copy, so the live book stayed untouched). Contains all campaign results, 15 retractions, and the director's verifications, the open questions and the D-014f proof step.
- `proofbook-p_vs_np-LIVE-stand-heute.jsonl` - 410 entries. The live book (`/var/lib/cherryme/knowledge/proofs/p_vs_np.jsonl`) as of today, **unchanged**. It does not yet contain today's campaign work (not even D-013).
- `LESBAR-*.md` - readable rendering (ledger brief) of each.

Both chains verify (`verify_chain` True). The staging book is a superset in spirit but not a strict extension of the live one, so it was not merged. Retracted entries stay in the file; the view excludes them.
