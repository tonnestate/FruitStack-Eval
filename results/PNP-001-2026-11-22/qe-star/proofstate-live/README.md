# Live proof states (desk `proofstate/`), copy 2026-11-22

- One file per ledger question that HAS a proof state, i.e. one that at least one research session worked on with `proof_state_update`. Each file is append-only and holds events: steps, reviews, gaps, refuted approaches.
- Count: 98 files as of 17:05 (94 at 15:55; the 4fabee1 push held 92).
- **Correction:** the commit message of 4fabee1 says "182 questions". That number is wrong. It counted the 92 JSON files together with their 90 `.lock` files.
- The ledger contains 2,248 research questions in total:
  - OPEN: 1,424
  - PURSUED: 552
  - ANSWERED: 181
  - STOPPED: 56
  - ESCALATED: 18
  - RETRACTED: 17
- Most questions have no proof state yet. Their history is in the proof book (`results/PNP-001-2026-11-18/beweisbuch/`).

## Review status at 17:05 (other model family, K11 R3)
- `Q-0b7da33369:S0011` (E2, unrolling: online cut-width <= S): SURVIVED_REVIEW, nemotron-3-ultra-550b, session R1551. The review covers the cut-width count only.
- `Q-156fa9c912:S0037` (resource transfer O(U*S)): SURVIVED_REVIEW, nemotron-3-ultra-550b, session R1551. The review covers the standard TM tableau, not the RAM case or uniformity.
- `Q-f0a0962f12:S0002` (claimed Candidate A clauses 1-4 jointly unsatisfiable): REFUTED, nemotron-3-ultra-550b, session R1567. The objection is that the applicability of Cor 6.2 was not shown. Open: whether that contradiction is the intended proof-by-contradiction (Q-0a1653e365).
- Still OPEN: the arrow embedding => L* (Thm 4.1 is linear; the unrolled circuit is not). Nothing here proves QE* or P != NP.
