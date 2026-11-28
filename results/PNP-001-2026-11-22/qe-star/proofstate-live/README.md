# Live proof states (desk `proofstate/`), copy 2026-11-22

- One file per ledger question that HAS a proof state, i.e. one that at least one research session worked on with `proof_state_update`. Each file is append-only and holds events: steps, reviews, gaps, refuted approaches.
- Count: 106 files as of 20:10 (98 at 17:05, 94 at 15:55; the 4fabee1 push held 92).
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

## Status at 20:10
- Manuscript v0.25 (commit 9f017c7) is under adversarial review. Agents read the verbatim copy `/root/contracts/PNP-001-MANUSCRIPT-v0.25-EXACT-ONE.md`.
- Questions:
  - `Q-0cce07fc92`: Theorem 3 vs MMW.
  - `Q-46a82ddf07`: Sections 2-6.
  - `Q-c5a09eda9a`: is (8) proved?
  - `Q-78cc7f4de8`: the MMW per-update quote.
  - `Q-6ead6c935d`: the quantifiers of (40a).
- **(40a) quantifier check (`Q-6ead6c935d`):**
  - The class M^unif uses "the same oracle conventions as in [4]". If the machines may query the Sigma3SAT^A oracle, MMW Thm 1.2 refutes (40a). (40a) must range over oracle-free machines.
  - The box lacks "exists s, A in PH".
- External review supplied by the owner (ledger CONNECTION f2e7a56fd8975b97):
  - Theorem 3 is a valid conditional proof.
  - Sections 2-6: no gap found.
  - (8) is not proved.
- Worst case vs amortized update time (G0002):
  - R1600 found that MMW Thm 1.2 does not define update time in the text it read. 9f017c7 now quotes a per-read definition from MMW Section 2.
  - Desk verification of that quote is pending.
- **Targets:**
  - `Q-248eb0b818`: (40a), the CAND-A lane gate.
  - `Q-e72cdd5423`: barrier test (relativization / locality).
  - `Q-85e487150a`: restricted classes.
  - `Q-cb61ed683c`: (8).
- **First restricted result (`Q-85e487150a:S0001`, R1609):**
  - Status: CLAIMED, cross-family review pending.
  - Claim: linear staged realizations over F_p (q_{t+1} = M_t q_t + z_t v_t, arbitrary decoder) of total Search-MCSP need S >= 2^m/(p-1).
  - Proof route: Chevalley-Warning plus totality. It does not cover nonlinear updates.
- **Reviews:**
  - `Q-f0a0962f12:S0007` (repair of S0002) SURVIVED_REVIEW, nemotron-3-ultra.
- `desk-lanes-live.json`: the desk's lane allocation with all owner decisions.
- Nothing here proves (40a), (8), QE* or P != NP.
