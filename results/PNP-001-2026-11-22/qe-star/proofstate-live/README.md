# Live proof states (desk `proofstate/`), copy 2026-11-22

- One file per ledger question that HAS a proof state, i.e. one that at least one research session worked on with `proof_state_update`. Each file is append-only and holds events: steps, reviews, gaps, refuted approaches.
- Count: 94 files as of 15:55. The 4fabee1 push held 92.
- **Correction:** the commit message of 4fabee1 says "182 questions". That number is wrong. It counted the 92 JSON files together with their 90 `.lock` files.
- The ledger contains 2,248 research questions in total:
  - OPEN: 1,424
  - PURSUED: 552
  - ANSWERED: 181
  - STOPPED: 56
  - ESCALATED: 18
  - RETRACTED: 17
- Most questions have no proof state yet. Their history is in the proof book (`results/PNP-001-2026-11-18/beweisbuch/`).
