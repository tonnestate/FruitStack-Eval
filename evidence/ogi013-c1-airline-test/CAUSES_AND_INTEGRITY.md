# c1 airline-test: causal attribution of the 17 shared failures and integrity audit (2026-10-27)
Added after c1; c1 results (rows.jsonl, compare.json, RESULT.md, sha256 manifest) are unchanged. Scripts: classify_failures.py, replay_assurance.py,
attribute_causes.py, integrity.py. Raw outputs: failure_table.json, replay_assurance.json, cause_attribution.json, integrity.json.

## Causes (34 failing arms = 17 tasks x 2; rule-based, rules in attribute_causes.py)
| primary cause | FIXED | ADAPTIVE |
|---|---|---|
| AppleMe LOOPING/THRASHING/STALLED false positive -> PeachMe HEALTH_WARNING block (sensor fed no information gain) | 13 | 14 |
| Route output unusable (>=2 fallback "could not complete that step" turns) -> same reflex | 2 | 2 |
| Reflex still fires with gain-grounded events (not explained by the sensor fault) | 1 | 1 |
| Task failed without any block (model/policy) | 1 | 0 |
Authorization, budget, tool execution and Pomelo effects were not causes: the only Pomelo refusals are the reflex's own HEALTH_WARNING blocks.
Common termination artifact: after the stop the runner called transfer_to_human_agents, refused by the same reflex -> tau2 "too_many_errors" (8 refused calls).

## Did the adaptive organisation get to act?
Largely no. Failing ADAPTIVE arms mostly ended with 0 escalations/contributions (organisation is triggered on write actions; episodes were stopped during read-only
lookups). FIXED arms ran its fixed pipeline on every step, so it used more steps before the same stop. c1 therefore mostly measured how soon a
mis-fed sensor stops an episode, not organisational ability. Offline replay (no model calls): with environment-observed gain, AppleMe stayed HEALTHY on every
pre-block turn in the 27 sensor-starved arms; this shows the sensor would not have fired there, NOT that those tasks would have been solved.

## Integrity
- Strict evaluator (--require-complete): passes, 20/20 complete pairs, none unmatched or confounded.
- Trial credit: 15 TRIAL_CREDIT receipts exist (11 in kept arms, 4 in discarded attempts), all provider nvidia, ALL failed with FORBIDDEN, no tokens, no cost. Attempts
  continued until the PLUMME_TRIAL_CREDIT=off switch took effect (15:28Z); nothing was consumed. This corrects RESULT.md's statement that only one discarded
  attempt touched a trial-credit route: kept arms also attempted such routes (always rejected).
- Discarded attempts: 20 arms (10 pairs) dropped on simulator-route failure, 463 receipts (298 failed); logged; none re-used in results. Dropping is decided by route
  failure only, before grading, so it cannot depend on reward.
- Simulator model: identical within every pair (0 pairs with >1 sim model).
- Agent model mix differs between arms (AUTO routing; e.g. FIXED used gemini-3.1-flash-lite 97 successful calls vs 41 in ADAPTIVE; ADAPTIVE leaned on openai-fast).
  This is an uncontrolled confound for any quality or resource difference. Provider mix also shifted during the campaign (provider admission/availability is time-varying).
- Cost: 185 (FIXED) / 131 (ADAPTIVE) successful receipts have cost_usd null; labels are FREE_TIER/ANONYMOUS_FREE, no measured zero. Cost per success remains undefined; no zero was assumed.
