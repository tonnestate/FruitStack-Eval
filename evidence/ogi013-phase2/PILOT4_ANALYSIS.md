# PILOT-4 — root cause, mechanism and decision-level trace

Evidence: `runs/pilot-4/` (preserved, unmodified), commit under test `7782562dd186f395df2bd71a2429cd7a41eb8766`. Task: official tau2 airline task 24. Reference (evaluation_criteria): the ONLY expected write is
`book_reservation` JFK→SEA, HAT069 (2024-05-20) + HAT276 (2024-05-25), basic economy, gift_card_7359776 $39 + gift_card_7773485 $67, 1 free bag; NL assertions: the agent does NOT cancel H9ZU1C (policy-ineligible),
books exactly that trip. Both arms scored 0.0 (db_match False, `book_reservation` not executed). Nothing below changes or re-scores that.

## Layer separation
| layer | SINGLE | COLLAB |
|---|---|---|
| model decision | refused the ineligible cancellation itself (msg 8), moved on, searched flights, proposed exactly HAT069/HAT276 ($51+$55 = $106 = 39+67, i.e. the reference trip), asked for confirmation | drafted `cancel_reservation(H9ZU1C)` after the user gave a reason (policy-ineligible: booked 2024-05-01, economy, no insurance) |
| organisational decision | none (no review) | independent critique (gpt-oss lineage) blocked the cancel; author revised to `transfer_to_human_agents`; third lineage (gemini-flash) ratified it |
| simulator behaviour | the last user message was `Yes, that is correct. Please proceed with the booking … ###STOP###`: the LLM user simulator confirmed AND emitted the stop token in one message | gave its reason and said it was "ready to look into those flight options" |
| benchmark termination | `###STOP###` ends the conversation at once (`user_stop`): the confirmed booking could not be executed | `transfer_to_human_agents` → `###TRANSFER###` ends the episode (`user_stop`) |
| harness | no defect found (receipts, dispatch and token accounting reconcile; no budget stop; nothing refused) | no defect found; two rejected requests (Groq billing/credit exhausted; NVIDIA TRIAL_CREDIT route forbidden), zero tokens, recorded (SINGLE had one billing rejection) |

## SINGLE: why it ended without the booking
The agent did everything the policy requires before a write (asked for the confirmation of flights, payment order and baggage). The user simulator then answered with the confirmation and the stop token **in the same message**, so the episode terminated
before the agent's next turn. This is simulator behaviour plus tau2's termination rule — not an agent error, not a harness defect, and not changeable without altering the benchmark (not done). Whether the agent would then have passed the grader
(exact payment split, baggage, communicate checks) is UNKNOWN: the booking never ran. The score 0.0 therefore says "no write executed", not "wrong write".

## COLLAB: was the transfer necessary? could the booking objective have been pursued?
No, and yes. Policy line 13: "You should deny user requests that are against this policy." Line 15: transfer "if and only if the request cannot be handled within the scope of your actions". An ineligible cancellation is a request to **deny**
(and the user had pre-committed: "if cancellation is not possible, accept it and move on" — the simulator's own task text), after which the user's second objective (the booking) was open. The transfer was itself a policy deviation and it destroyed the
remaining objective. The reviewers' stated grounds quoted the cancellation rules correctly and then asserted that a transfer was "the mandatory next step" — a misreading that the re-reviewer repeated with confident, itemised "checks".

## Decision-level trace (COLLAB, `decision_metrics.py`, mechanical classification against the reference actions)
| # | step | actor (lineage) | content | class |
|---|---|---|---|---|
| 1 | draft | gemini-3.1-flash-lite (gemini-flash-lite) | `cancel_reservation(H9ZU1C)` | UNEXPECTED_WRITE (reference: do not cancel) |
| 2 | critique | gpt-oss-20b (gpt-oss) | policy forbids cancellation; proposes `transfer_to_human_agents` | defect FOUND (real), alternative action wrong |
| 3 | revision | author model (pinned) | `transfer_to_human_agents` | UNEXPECTED_TRANSFER |
| 4 | re-review | gemini-3-flash-preview (gemini-flash) | `ISSUES: NONE`, grounds stated (and misstating the transfer rule) | grounded agreement ≠ correctness |
| 5 | execution | | transfer executed → episode ended | expected action not completed |
| 6 | review 2 | gemini-flash | `message` (transfer notice) validated unchanged | NO_CHANGE_SAFE |
Review outcome (mechanical): **ERROR_REPLACED_BY_DIFFERENT_ERROR**. Unexpected writes executed: 0 (in SINGLE: 0). Unexpected transfers executed: 1 (SINGLE: 0). Expected actions completed: 0 / 0.

## Value and limits of the independent correction
- Value (observed): a policy-ineligible write was **prevented**, by a different model lineage, with a concrete, correct policy citation; the author accepted the criticism; a further lineage re-evaluated the revision. The mechanism ran end to end on real providers.
- Limits (observed): the correction was replaced by another wrong action that cost the episode its second objective; the independent re-review ratified it. Stated grounds are not evidence of correctness (the pilot's own design principle), and one critic's *alternative action*
  was adopted without a check against the "deny vs transfer" rule. The prevented write is not shown to have lowered the score (no counterfactual run; in SINGLE the same author model refused at the same decision point, so the draft cancel was a sampling outcome).
- Cost: 4 review requests, 34,624 tokens (3 challenge calls 29,446 incl. one 11,920-token reasoning answer, 1 revision 5,178). Total COLLAB arm 15 requests / 61,635 tokens vs SINGLE 22 / 92,898 — fewer because the conversations diverged, not because review is cheaper.
- Independence: three lineages, but two are Google Gemini models; independence keys differ, vendor does not.
- Calibration observed: PlumMe's chars/3 input estimate over-counted Gemini input by ~34% (5,633 vs 4,195); the cl100k proxy under-counted by ~5% (4,006 vs 4,195). No step used more than one provider request (continuation guard not exercised live).

## Defects and confounders
Harness defects: none found in PILOT-4. Confounders: simulator STOP-with-pending-action (SINGLE), divergent conversations, fixed arm order, n = 1. Mitigation for the prospective study: arm order by hash parity, a mechanical `premature_stop` flag
(final user message carries the stop token while a confirmed write is pending) recorded as covariate — not excluded, not repaired.
