# rg2 trace report: /root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/runs/org-demo/d1

- task 2: official reward=1.0; verifier.log=not present

## Decisions
- C-01M60RVA8A6QEBGPE0ZZBTMRT0: draft=message final=None (no ORG_REVISION observed); status=UNKNOWN triage=SKIPPED_SIMPLE_TASK workers=['gpt-oss-120b@default', 'xing4.0-29b-a4b@default']
  rows={'ATTEMPT_FAILED': 2} epistemic={'UNVERIFIED': 2}
  responsibilities planned=1 activated=1 dispatches={'PRIMARY': 1} attempt_errors={'PLUMME_ACQUIRE_FAILED': 1, 'RATE_LIMITED': 1}
- C-01M60RVMY3GN5XH2VD5YJKSWEH: draft=message final=None (no ORG_REVISION observed); status=UNKNOWN triage=SKIPPED_SIMPLE_TASK workers=['beam@default', 'openai-fast@default', 'xing4.0-29b-a4b@default']
  rows={'ATTEMPT_FAILED': 3} epistemic={'UNVERIFIED': 3}
  responsibilities planned=1 activated=2 dispatches={'PRIMARY': 1} attempt_errors={'RATE_LIMITED': 1, 'PINNED_WORKER_UNAVAILABLE': 1, 'PLUMME_ACQUIRE_FAILED': 1}
- C-01M60SDXT1NQK5ZG5PZF5GN29C: draft=message final=None (no ORG_REVISION observed); status=UNKNOWN triage=SKIPPED_SIMPLE_TASK workers=['north-mini-code@default', 'openai-fast@default']
  rows={'PROPOSAL': 1, 'ATTEMPT_FAILED': 2} epistemic={'UNVERIFIED': 3}
  responsibilities planned=1 activated=1 dispatches={'PRIMARY': 1} attempt_errors={'NONE': 1, 'RATE_LIMITED': 1, 'PLUMME_ACQUIRE_FAILED': 1}

Attempt error codes (run): {'PLUMME_ACQUIRE_FAILED': 7, 'RATE_LIMITED': 3, 'PINNED_WORKER_UNAVAILABLE': 1, 'NONE': 1}
Interventions: [('SWITCH_WORKER', 'gpt-oss-120b@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'xing4.0-29b-a4b@default', 'RATE_LIMITED'), ('SWITCH_WORKER', 'openai-fast@default', 'RATE_LIMITED'), ('SWITCH_WORKER', 'xing4.0-29b-a4b@default', 'PINNED_WORKER_UNAVAILABLE'), ('SWITCH_WORKER', 'beam@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'unknown:llm7>llm7>codestral-latest', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'unknown:llm7>llm7>codestral-latest', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'openai-fast@default', 'RATE_LIMITED'), ('SWITCH_WORKER', 'north-mini-code@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'north-mini-code@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'nemotron-3.5-super-vl@default', 'PLUMME_ACQUIRE_FAILED')]
Knowledge-marker events: 0

## Verdict
- worker_contribution: True -- 1 delivered of 12 rows; kinds={'ATTEMPT_FAILED': 11, 'PROPOSAL': 1}
- independent_verification: None -- no quorum-promoted PASS/CONTRADICT; 0 verifier judgments (relations={}); verifier.log not present
- causal_effect_on_decision: False -- no ORG_REVISION events; EPISODE_CLOSED stats.revisions=0
- productive_recovery: False -- 11 SWITCH_WORKER; progress follow-ups on other worker=0
- knowledge_reuse: False -- no markers; ensemble accounting reused_without_inference=0
- organisational_success: None -- worker_contribution AND (causal_effect OR independent_verification) AND reward 1.0 -> wc=True, causal=False, verification=None, reward_1=True
