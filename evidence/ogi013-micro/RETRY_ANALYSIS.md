# Retry-cause analysis, micro pilot `micro__duration-1` T (repair order R8; read-only analysis of `fruitstack-events.jsonl`)

101 STEP events, `stats.step_retries` 141, 142 `STEP_REFUSED` events (one more refusal abandoned: `STEP_ABANDONED`), 47 `ROLE_HANDOVER` events, 3 `SUPPLY_WAIT`, 13 `BAD_ACTION`, 85 tool calls, 11 distinct models, 4 `SUBMIT_CHECK`.

| retry class (`STEP_REFUSED.code`) | count | share |
|---|---|---|
| EXECUTION_NOT_PERFORMED_RATE_LIMITED (supply) | 87 | 61.3 % |
| EXECUTION_NOT_PERFORMED_PROVIDER_UNAVAILABLE (supply) | 28 | 19.7 % |
| EXECUTION_NOT_PERFORMED_FORBIDDEN (eligibility/policy) | 13 | 9.2 % |
| EXECUTION_OUTPUT_UNUSABLE_SEMANTIC_OUTPUT_FAILURE (unusable output) | 7 | 4.9 % |
| EXECUTION_NOT_PERFORMED_PROVIDER_REJECTED (supply) | 5 | 3.5 % |
| EXECUTION_NOT_PERFORMED_MODEL_NOT_FOUND (supply) | 1 | 0.7 % |
| EXECUTION_NOT_CONFIRMED_FORBIDDEN | 1 | 0.7 % |

Reading: 81 % of the retries are free-tier supply conditions (rate limits and unavailability); gate rejections are not retries (they are tool results inside a step). Because every call re-asked PlumMe AUTO without a pinned model, each refusal moved the next attempt to another model, which is how one episode touched 11 models (calls per model: llama-3.3-70b 22, mistral-nemo 16, qwen2.5-vl-72b 15, mistral-small-3.2-24b 14, qwen3.6-27b 12, gpt-oss-120b 8, others <= 4). R8 pins each role to one model with every retry of a step staying on it; a pinned model is replaced only after 2 consecutive failed steps (`ROSTER_CHANGE`). Rate limits remain a supply fact and are not removed by the roster.
