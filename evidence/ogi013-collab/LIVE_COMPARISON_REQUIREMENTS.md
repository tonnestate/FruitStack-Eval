# Minimal requirements for ONE live, matched, resource-budgeted comparison of the collaboration step (NOT executed; owner authorisation of the maximum consumption required)

Arms (same task, same pinned simulator model, same AUTO supply, fresh state each): SINGLE (mode single) | COLLAB (mode rg2, OGI013_ORG_COLLAB=1, policy OFF).
Task: one fixed airline task with a write action and known headroom (candidates from the archived c2 outcomes: 24 or 29, both failed by both c2 arms) or task 6 (the single-model counterfactual is still unknown).
Budget (to be fixed by the owner; reuse evidence/ogi013-pilot/pilot_guard.py + a budget file, fail-closed, every dispatch is a receipt row): measured basis = airline:2/d2 agent steps ~15 dispatches / ~81k tokens + simulator
~13 calls / ~20k tokens; one collaboration review = challenge (+ revise + challenge) = 1-3 calls carrying the full task prompt (~5k tokens each) + at most one specialist call. Proposed ceiling for the COLLAB arm: 90 dispatches / 300k tokens,
SINGLE 45 / 160k, whole comparison 135 / 460k, 0 cash, 90 min. Stop conditions already in code: Brother-Mode loop guards (max 2 rounds, 3 consecutive failures), economy gate (purpose, no-new-information, known supply failure).
Read-out (descriptive, n=1 per arm): official reward per arm; per review: improved / validated_unchanged / review_unavailable / unresolved (ORG_COLLAB events); dispatches and tokens per arm; marginal dispatches per improving review.
Success of the *mechanism* is an action-changing ORG_REVISION after found issues; a validated-unchanged review is reported as independent validation only.
Not claimed by this comparison: any effect size, any generalisation, or OGI. The frozen OGI-013 study, its evidence and its preregistration are unchanged.
