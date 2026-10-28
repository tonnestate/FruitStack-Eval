# Offline collaboration traces (scripted workers; real cherryme.brother rounds + ContributionLedger; zero model calls)

Task: POLICY refunds only within 24h; the customer asks to cancel HAT001 booked 2h ago. WRONG1 is the wrong reservation. Agreement below is a reviewer's claim, not proof.

## A. Sound answer: one independent assessment with stated grounds

| # | ledger kind | worker (lineage) | status | excerpt |
|---|---|---|---|---|
| 1 | SOLUTION | draft-model (lineage-draft) | UNVERIFIED | {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "HAT001"} |
| 2 | CRITIQUE | challenge-model-1 (lineage-challenge-1) | UNVERIFIED | ISSUES: NONE |

- stages called: ['challenge']; provider calls=1; stop=NO_ISSUES
- final action: reservation HAT001; changed=False; improved=False; validated=True; ungrounded_agreement=False; final_reviewed=True
- AGREED: challenge-model-1 (lineage-challenge-1) with HAT001 - grounds: Policy 24h window: booking made 2h ago is inside it; HAT001 is the reservation named in the CONVERSATION.
- contributor: critique challenge-model-1 (lineage-challenge-1) found_issues=False, materially_improved=False

## B. Flawed answer: challenged, revised, the revision examined again

| # | ledger kind | worker (lineage) | status | excerpt |
|---|---|---|---|---|
| 1 | SOLUTION | draft-model (lineage-draft) | UNVERIFIED | {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "WRONG1"} |
| 2 | CRITIQUE | challenge-model-1 (lineage-challenge-1) | DISSENT | ISSUES: FOUND |
| 3 | REVISION | revise-model-2 (lineage-revise-2) | UNVERIFIED | {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "HAT001"} |
| 4 | CRITIQUE | challenge-model-3 (lineage-challenge-3) | UNVERIFIED | ISSUES: NONE |

- stages called: ['challenge', 'revise', 'challenge']; provider calls=3; stop=NO_ISSUES
- final action: reservation HAT001; changed=True; improved=True; validated=False; ungrounded_agreement=False; final_reviewed=True
- AGREED: challenge-model-3 (lineage-challenge-3) with HAT001 - grounds: Policy 24h window: booking made 2h ago is inside it; HAT001 is the reservation named in the CONVERSATION.
- contributor: revision revise-model-2 (lineage-revise-2) changed_action=True
- contributor: critique challenge-model-1 (lineage-challenge-1) found_issues=True, materially_improved=True
- contributor: critique challenge-model-3 (lineage-challenge-3) found_issues=False, materially_improved=False

## C. Unresolved disagreement: the author rejects, the specialist backs the author, the objection stays

| # | ledger kind | worker (lineage) | status | excerpt |
|---|---|---|---|---|
| 1 | SOLUTION | draft-model (lineage-draft) | UNVERIFIED | {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "WRONG1"} |
| 2 | CRITIQUE | challenge-model-1 (lineage-challenge-1) | DISSENT | ISSUES: FOUND |
| 3 | REVISION | revise-model-2 (lineage-revise-2) | UNVERIFIED | {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "WRONG1"} |
| 4 | SOLUTION | specialist-model-3 (lineage-specialist-3) | UNVERIFIED | {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "WRONG1"} |

- stages called: ['challenge', 'revise', 'specialist']; provider calls=3; stop=NO_CHANGE
- final action: reservation WRONG1; changed=False; improved=False; validated=False; ungrounded_agreement=False; final_reviewed=False
- UNRESOLVED objection by challenge-model-1: ISSUES: FOUND
- contributor: revision revise-model-2 (lineage-revise-2) changed_action=False
- contributor: specialist specialist-model-3 (lineage-specialist-3) changed_action=False
- contributor: critique challenge-model-1 (lineage-challenge-1) found_issues=True, materially_improved=False

## D. Author overruled: the specialist backs the critic, its answer is reviewed once more by a new lineage

| # | ledger kind | worker (lineage) | status | excerpt |
|---|---|---|---|---|
| 1 | SOLUTION | draft-model (lineage-draft) | UNVERIFIED | {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "WRONG1"} |
| 2 | CRITIQUE | challenge-model-1 (lineage-challenge-1) | DISSENT | ISSUES: FOUND |
| 3 | REVISION | revise-model-2 (lineage-revise-2) | UNVERIFIED | {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "WRONG1"} |
| 4 | SOLUTION | specialist-model-3 (lineage-specialist-3) | UNVERIFIED | {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "HAT001"} |
| 5 | CRITIQUE | challenge-model-4 (lineage-challenge-4) | UNVERIFIED | ISSUES: NONE |

- stages called: ['challenge', 'revise', 'specialist', 'challenge']; provider calls=4; stop=NO_CHANGE
- final action: reservation HAT001; changed=True; improved=True; validated=False; ungrounded_agreement=False; final_reviewed=True
- AGREED: challenge-model-4 (lineage-challenge-4) with HAT001 - grounds: Policy 24h window: booking made 2h ago is inside it; HAT001 is the reservation named in the CONVERSATION.
- OVERRULED author: draft-model kept WRONG1; overruled by specialist-model-3
- contributor: revision revise-model-2 (lineage-revise-2) changed_action=False
- contributor: specialist specialist-model-3 (lineage-specialist-3) changed_action=True
- contributor: critique challenge-model-1 (lineage-challenge-1) found_issues=True, materially_improved=True
- contributor: critique challenge-model-4 (lineage-challenge-4) found_issues=False, materially_improved=False
