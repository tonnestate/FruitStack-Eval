# Offline SOLVE -> CHALLENGE -> REVISE -> RE-EXAMINE -> CONSOLIDATE trace (mock workers, real cherryme.brother rounds and ContributionLedger; no model call)

Task: POLICY refunds only within 24h; the customer asks to cancel HAT001 booked 2h ago. The draft cancels the WRONG reservation.

| step | stage | worker (lineage) | output (excerpt) | ledger row |
|---|---|---|---|---|
| 1 | SOLVE (seed draft) | draft-model (lineage-draft) | {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "WRONG1"}} | SOLUTION |
| 2 | CHALLENGE | challenge-model-1 (lineage-challenge-1) | ISSUES: FOUND | CRITIQUE/DISSENT |
| 3 | REVISE | revise-model-2 (lineage-revise-2) | {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "HAT001"} | REVISION/UNVERIFIED |
| 4 | CHALLENGE | challenge-model-3 (lineage-challenge-3) | ISSUES: NONE | CRITIQUE/UNVERIFIED |

Second challenge prompt contains the REVISED solution: True | first challenge prompt contains the policy and conversation: True

## CONSOLIDATE (host)

- final action: {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "HAT001"}}; changed=True; improved=True; validated_unchanged=False; unresolved=[]; stop=NO_ISSUES; provider calls=3
- attribution (read from the ledger):
  - {'role': 'revision', 'model': 'revise-model-2', 'lineage': 'lineage-revise-2', 'changed_action': True}
  - {'role': 'critique', 'model': 'challenge-model-1', 'lineage': 'lineage-challenge-1', 'found_issues': True, 'materially_improved': True}
  - {'role': 'critique', 'model': 'challenge-model-3', 'lineage': 'lineage-challenge-3', 'found_issues': False, 'materially_improved': False}
