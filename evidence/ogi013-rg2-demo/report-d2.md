# rg2 trace report: /root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/runs/org-demo/d2

- task 6: official reward=1.0; verifier.log=['tasks/6/org/verifier.log']

## Decisions
- C-01M60TMTBQHK3VSB3F6FEKSD7C: draft=get_reservation_details final=None (no ORG_REVISION observed); status=UNKNOWN triage=SKIPPED_SIMPLE_TASK workers=['gemini-3.1-flash-lite@vision', 'unknown:llm7>llm7>codestral-latest', 'xing4.0-29b-a4b@default']
  rows={'ATTEMPT_FAILED': 4, 'PROPOSAL': 1} epistemic={'UNVERIFIED': 5}
  responsibilities planned=1 activated=1 dispatches={'PRIMARY': 1} attempt_errors={'PLUMME_ACQUIRE_FAILED': 3, 'NONE': 1, 'RATE_LIMITED': 1}
- C-01M60TNEW5WYGNCAX46JBFQB0H: draft=message final=None (no ORG_REVISION observed); status=UNKNOWN triage=SKIPPED_SIMPLE_TASK workers=['north-mini-code@default', 'openai-fast@default']
  rows={'PROPOSAL': 1, 'ATTEMPT_FAILED': 2} epistemic={'UNVERIFIED': 3}
  responsibilities planned=1 activated=1 dispatches={'PRIMARY': 1} attempt_errors={'NONE': 1, 'RATE_LIMITED': 1, 'PLUMME_ACQUIRE_FAILED': 1}
- C-01M60TPAY868P0P0WV9G1Z87PH: draft=message final=None (no ORG_REVISION observed); status=UNKNOWN triage=SKIPPED_SIMPLE_TASK workers=['nemotron-3.5-lightning@default', 'nemotron-3.5-super-vl@default', 'nemotron-3.5-super-vl@vision']
  rows={'PROPOSAL': 3, 'ATTEMPT_FAILED': 4} epistemic={'UNVERIFIED': 7}
  responsibilities planned=1 activated=1 dispatches={'PRIMARY': 1} attempt_errors={'NONE': 3, 'PLUMME_ACQUIRE_FAILED': 3, 'RATE_LIMITED': 1}
- C-01M60TV4QGPDBY79VCM23X1V9R: draft=transfer_to_human_agents final=None (no ORG_REVISION observed); status=UNKNOWN triage=SKIPPED_SIMPLE_TASK workers=['nemotron-3-ultra-550b-a55b@default', 'nemotron-3.5-lightning@default']
  rows={'ATTEMPT_FAILED': 2} epistemic={'UNVERIFIED': 2}
  responsibilities planned=1 activated=1 dispatches={'PRIMARY': 1} attempt_errors={'FORBIDDEN': 1, 'PLUMME_ACQUIRE_FAILED': 1}
- C-01M60TVC0VE61EZ2FTBBPW1971: draft=message final=None (no ORG_REVISION observed); status=UNKNOWN triage=SKIPPED_SIMPLE_TASK workers=['dots-3-note-preview@default', 'mistral-nemo-instruct-2407@default', 'nemotron-3-nano:30b@default']
  rows={'ATTEMPT_FAILED': 3} epistemic={'UNVERIFIED': 3}
  responsibilities planned=1 activated=2 dispatches={'PRIMARY': 1} attempt_errors={'RATE_LIMITED': 1, 'PINNED_WORKER_UNAVAILABLE': 1, 'PLUMME_ACQUIRE_FAILED': 1}
- C-01M60TVSN6J97A00Y3XWF450B4: draft=message final=None (no ORG_REVISION observed); status=UNKNOWN triage=SKIPPED_SIMPLE_TASK workers=['gemini-3.1-flash-lite@vision', 'laguna-xs-2.1@default', 'lfm-2.5-2.6b@default']
  rows={'ATTEMPT_FAILED': 5, 'PROPOSAL': 2} epistemic={'UNVERIFIED': 7}
  responsibilities planned=1 activated=1 dispatches={'PRIMARY': 1} attempt_errors={'INVALID_PROVIDER_RESULT': 1, 'NONE': 2, 'PLUMME_ACQUIRE_FAILED': 3, 'RATE_LIMITED': 1}
- C-01M60TXXKAWZQ682H0TEAQ6YDD: draft=message final=None (no ORG_REVISION observed); status=UNKNOWN triage=SKIPPED_SIMPLE_TASK workers=['inkling-small@vision', 'laguna-s-2.1@default']
  rows={'PROPOSAL': 2, 'ATTEMPT_FAILED': 3} epistemic={'UNVERIFIED': 5}
  responsibilities planned=1 activated=1 dispatches={'PRIMARY': 1} attempt_errors={'NONE': 2, 'INVALID_PROVIDER_RESULT': 2, 'FORBIDDEN': 1}
- C-01M60V0Y7EKZNQ5J5170NZDTFV: draft=message final=None (no ORG_REVISION observed); status=UNKNOWN triage=SKIPPED_SIMPLE_TASK workers=['gemini-2.5-flash@vision', 'gpt-oss:20b@default', 'inkling@vision']
  rows={'ATTEMPT_FAILED': 3} epistemic={'UNVERIFIED': 3}
  responsibilities planned=1 activated=2 dispatches={'PRIMARY': 1} attempt_errors={'FORBIDDEN': 1, 'PINNED_WORKER_UNAVAILABLE': 1, 'PLUMME_ACQUIRE_FAILED': 1}
- C-01M60V1GH6YFMCN9D2EN7AJH01: draft=message final=None (no ORG_REVISION observed); status=UNKNOWN triage=SKIPPED_SIMPLE_TASK workers=['gemini-3-flash-preview@vision', 'gpt-oss-20b@default', 'gpt-oss:20b@default']
  rows={'ATTEMPT_FAILED': 3} epistemic={'UNVERIFIED': 3}
  responsibilities planned=1 activated=1 dispatches={'PRIMARY': 1} attempt_errors={'PINNED_WORKER_UNAVAILABLE': 1, 'BILLING_OR_CREDIT_EXHAUSTED': 1, 'PLUMME_ACQUIRE_FAILED': 1}
- C-01M60VM77P28XZ1H1Y12KJR31W: draft=message final=None (no ORG_REVISION observed); status=UNKNOWN triage=SKIPPED_SIMPLE_TASK workers=['glyph-cluster@default', 'gpt-oss-120b@default']
  rows={'PROPOSAL': 3, 'ATTEMPT_FAILED': 2} epistemic={'UNVERIFIED': 5}
  responsibilities planned=1 activated=1 dispatches={'PRIMARY': 1} attempt_errors={'NONE': 3, 'BILLING_OR_CREDIT_EXHAUSTED': 1, 'PLUMME_ACQUIRE_FAILED': 1}
- C-01M60VMV53739NVD8D101H2H8H: draft=message final=None (action_changed=True); status=REFUTED triage=SKIPPED_SIMPLE_TASK workers=['glyph-cluster@default', 'laguna-s-2.1@default', 'nemotron-3.5-super-vl@default']
  rows={'PROPOSAL': 4, 'VERIFIER': 10} epistemic={'UNVERIFIED': 3, 'SOURCE_BACKED': 8, 'VERIFIED': 2, 'DISSENT': 1}
  responsibilities planned=1 activated=1 dispatches={'PRIMARY': 11} attempt_errors={'NONE': 4}
- C-01M60VY5NS6YNP9SH7G06XMNK1: draft=message final=None (action_changed=True); status=UNKNOWN triage=SKIPPED_SIMPLE_TASK workers=['gemma-4-26b-a4b-it@vision', 'glyph-cluster@default', 'laguna-s-2.1@default', 'nemotron-3.5-super-vl@default']
  rows={'PROPOSAL': 4, 'VERIFIER': 4, 'ATTEMPT_FAILED': 2} epistemic={'UNVERIFIED': 5, 'SOURCE_BACKED': 3, 'DISSENT': 2}
  responsibilities planned=1 activated=1 dispatches={'PRIMARY': 1} attempt_errors={'NONE': 4, 'PLUMME_ACQUIRE_FAILED': 2}
- C-01M60W444FMJ1JZREEXJ4GNH6Y: draft=message final=None (no ORG_REVISION observed); status=UNKNOWN triage=SKIPPED_SIMPLE_TASK workers=['flint-v1.0@default', 'gemma-4-31b-it@vision']
  rows={'ATTEMPT_FAILED': 2} epistemic={'UNVERIFIED': 2}
  responsibilities planned=1 activated=1 dispatches={'PRIMARY': 1} attempt_errors={'RATE_LIMITED': 1, 'PLUMME_ACQUIRE_FAILED': 1}

Attempt error codes (run): {'PLUMME_ACQUIRE_FAILED': 26, 'NONE': 20, 'RATE_LIMITED': 6, 'FORBIDDEN': 3, 'PINNED_WORKER_UNAVAILABLE': 8, 'INVALID_PROVIDER_RESULT': 3, 'BILLING_OR_CREDIT_EXHAUSTED': 2}
Interventions: [('SWITCH_WORKER', 'gemini-3.1-flash-lite@vision', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'xing4.0-29b-a4b@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'unknown:llm7>llm7>codestral-latest', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'unknown:llm7>llm7>codestral-latest', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'openai-fast@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'openai-fast@default', 'RATE_LIMITED'), ('SWITCH_WORKER', 'north-mini-code@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'north-mini-code@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'nemotron-3.5-super-vl@vision', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'nemotron-3.5-super-vl@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'nemotron-3.5-super-vl@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'nemotron-3.5-super-vl@vision', 'RATE_LIMITED'), ('SWITCH_WORKER', 'nemotron-3.5-lightning@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'nemotron-3.5-lightning@default', 'FORBIDDEN'), ('SWITCH_WORKER', 'nemotron-3-ultra-550b-a55b@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'nemotron-3-ultra-550b-a55b@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'nemotron-3-nano:30b@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'nemotron-3-nano:30b@default', 'RATE_LIMITED'), ('SWITCH_WORKER', 'mistral-nemo-instruct-2407@default', 'PINNED_WORKER_UNAVAILABLE'), ('SWITCH_WORKER', 'dots-3-note-preview@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'mistral-nemo-instruct-2407@default', 'PINNED_WORKER_UNAVAILABLE'), ('SWITCH_WORKER', 'dots-3-note-preview@vision', 'PINNED_WORKER_UNAVAILABLE'), ('SWITCH_WORKER', 'minimax-m2.7@default', 'PINNED_WORKER_UNAVAILABLE'), ('SWITCH_WORKER', 'flint-v1.0@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'minimax-m2.7@default', 'PINNED_WORKER_UNAVAILABLE'), ('SWITCH_WORKER', 'gemini-2.5-flash-lite@vision', 'PINNED_WORKER_UNAVAILABLE'), ('SWITCH_WORKER', 'lfm-2.5-2.6b@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'lfm-2.5-2.6b@default', 'INVALID_PROVIDER_RESULT'), ('SWITCH_WORKER', 'gemini-3.1-flash-lite@vision', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'gemini-3.1-flash-lite@vision', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'laguna-xs-2.1@default', 'RATE_LIMITED'), ('SWITCH_WORKER', 'laguna-xs-2.1@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'laguna-s-2.1@default', 'INVALID_PROVIDER_RESULT'), ('SWITCH_WORKER', 'laguna-s-2.1@default', 'INVALID_PROVIDER_RESULT'), ('SWITCH_WORKER', 'inkling-small@vision', 'FORBIDDEN'), ('SWITCH_WORKER', 'inkling@vision', 'FORBIDDEN'), ('SWITCH_WORKER', 'gpt-oss:20b@default', 'PINNED_WORKER_UNAVAILABLE'), ('SWITCH_WORKER', 'gemini-2.5-flash@vision', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'gpt-oss:20b@default', 'PINNED_WORKER_UNAVAILABLE'), ('SWITCH_WORKER', 'gemini-3-flash-preview@vision', 'BILLING_OR_CREDIT_EXHAUSTED'), ('SWITCH_WORKER', 'gpt-oss-20b@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'gpt-oss-120b@default', 'BILLING_OR_CREDIT_EXHAUSTED'), ('SWITCH_WORKER', 'glyph-cluster@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'glyph-cluster@default', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'gemma-4-26b-a4b-it@vision', 'PLUMME_ACQUIRE_FAILED'), ('SWITCH_WORKER', 'gemma-4-31b-it@vision', 'RATE_LIMITED'), ('SWITCH_WORKER', 'flint-v1.0@default', 'PLUMME_ACQUIRE_FAILED')]
Knowledge-marker events: 0

## Verdict
- worker_contribution: True -- 34 delivered of 82 rows; kinds={'ATTEMPT_FAILED': 48, 'PROPOSAL': 20, 'VERIFIER': 14}
- independent_verification: True -- 2 quorum-promoted rows; distinct independence keys per (claim, source)={'C-01M60VMV53739NVD8D101H2H8H|https://tau2-environment.invalid/6/policy/0': 2}
- causal_effect_on_decision: True -- 2 of 2 ORG_REVISION with action_changed=true
- productive_recovery: True -- 47 SWITCH_WORKER; progress follow-ups on other worker=2
- knowledge_reuse: False -- no markers; ensemble accounting reused_without_inference=0
- organisational_success: True -- worker_contribution AND (causal_effect OR independent_verification) AND reward 1.0 -> wc=True, causal=True, verification=True, reward_1=True
