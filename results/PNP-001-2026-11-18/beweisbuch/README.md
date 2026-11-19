# Beweisbuch p_vs_np (AppleMe ProofLedger, append-only, hash-chained)

Stand: 2026-11-19, 15:00 (UTC+1).

- `proofbook-p_vs_np-STAGING-kampagnen.jsonl` - 2,780 entries. The book the FruitStack research organisation writes into (staging copy; the live book stays untouched): agent research sessions, fast-validator verdicts, the first kernel-checked Lean result, literature (KNOWN_RESULT), director synthesis, 35 retractions.
- `proofbook-p_vs_np-LIVE-stand-heute.jsonl` - 529 entries. The live book (`/var/lib/cherryme/knowledge/proofs/p_vs_np.jsonl`) as of today, unchanged by this export.
- `LESBAR-*.md` - readable rendering (ledger brief) of each.

Both hash chains verify (`verify_chain` True). Retracted entries stay in the file; the view excludes them.

Reading the verdict states (see the desk's verification chain): FINITE_CONFIRMED = independently recomputed on the stated finite domain (not a proof of any general statement); FORMALLY_VERIFIED = Lean 4 kernel accepted a complete core-Lean file with standard axioms only (artifact stored byte-identically with sha256) AND an independent fidelity review found the Lean statement equal to or stronger than the claim (the review is quality control by a model, not a formal proof of equivalence); OPEN_UNPROVEN = survived the counterexample search, no formal proof. Nothing in this book is a proof of P != NP or P = NP.
