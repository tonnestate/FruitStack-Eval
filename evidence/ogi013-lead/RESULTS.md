# OGI-013 lead order: results so far (frozen task django__django-11019, evaluator v2.1 for every row)
One replicate each. This is a case observation, not a statistical result. No MangoMe MCP tools were used by the operator; FruitStack's own isolated MangoMe/OrangeMe state is part of the integrated stack.

| Arm | resolved | F2P | P2P | provider requests | tokens (prompt/completion) | wall s | USD | models |
|---|---|---|---|---|---|---|---|---|
| L Luna (recorded, Codex native tools) | no | 3/16 | 58/58 | n/a (7 commands) | raw Codex: 198,744 in (182,656 cached) / 2,819 out | 40 | n/a (subscription) | gpt-6-luna |
| F driver v1 (defective, retained) | no | 0/16 | 58/58 | 11 steps | 17,129 / 1,827 | 179 | 0 | nemotron-3-nano:30b, mistral-nemo, nemotron-3-ultra-550b, mistral-small-3.2-24b |
| F driver v2, attempt 1 (prompt-format defect, retained) | NO_PATCH | - | - | 75 calls | 110,294 / 13,189 | 646 | 0 | 5 models, mostly nemotron-3-nano-omni-reasoning |
| F driver v2, attempt 3 (r03, valid format) | NO_PATCH | - | - | 40 steps + 81 retried steps | 163,898 / 13,097 | 820 | 0 | 9 models incl. qwen3guard-gen-8b (a safety classifier) |
| N non-organised (1 draft, same gate and budget) | NO_PATCH | - | - | 63 steps | 183,170 / 7,463 | 746 | 0 | 9 models incl. qwen3guard-gen-0.6b/8b |

Table B (S0/SR/BR) cannot be produced: no run reached an accepted P0, so Brother Mode was never invoked on code.
Mechanism of the F failure: one edit emptied an `if` body (IndentationError); every later run_tests executed 0 tests, so the gate never accepted a submit. Token ceiling (193,821/200,000) was reached at the same time as the 40-turn cap.
Finding (not changed): PlumMe AUTO assigns safety-classifier models (qwen3guard-*) to author roles. Needs an owner decision on an objective model-eligibility rule.
Limits not enforced in the code driver: the 24,000 per-step ceiling (prompts kept small instead). No specialist step. Pristine base tree is at research dir, not under evidence/.
Verdict: no measured organisational effect; F did not outperform L; N and F both NO_PATCH. K=10, SWE-bench Verified and Terminal-Bench 2.1 are not started.
