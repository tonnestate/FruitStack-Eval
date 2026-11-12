# EVAL-006 analysis (exploratory)

Tasks: 20 (evidence/EVAL-006/task_ids.txt). Primary: official BCB pass@1 (all tests pass, official in-process semantics in bwrap, clean tamper audit).

| arm | pass | rate | 95% CI (Clopper-Pearson) | hidden-only pass (FSE grade) | no candidate | provider calls | input tok | output tok | calls/solved | tokens/solved | wall s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SINGLE | 8/20 | 0.40 | [0.191, 0.639] | 8/20 | 0 | 20 | 340,242 | 4,908 | 2 | 43,144 | 233 |
| ORG | 8/20 | 0.40 | [0.191, 0.639] | 10/20 | 0 | 253 | 3,500,852 | 89,062 | 32 | 448,739 | 3,049 |

Paired: SINGLE-only passes b = 1, ORG-only passes c = 1, both = 7, neither = 11. Exact McNemar (two-sided binomial on discordant pairs) p = 1.0000. Difference ORG - SINGLE = +0.00. Descriptive only (n = 20, exploratory): no superiority claim.

## Per task

| task | SINGLE | ORG | ORG any final position | SINGLE model | ORG workers (lineages) | ORG basis | Brother stop | critiques (found) | revisions (answer changed) | specialist | ORG state | ORG calls | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BigCodeBench/1008 | 1 | 1 | 1 | chatgpt-codex/gpt-6-luna | dots, gpt, qwen3.8 | consensus | NO_SECOND_SOLVER | 0 (0) | 0 (0) | 0 | UNRESOLVED | 13 |  |
| BigCodeBench/1015 | 0 | 0 | 0 | chatgpt-codex/gpt-6-luna | gpt | primary | LOOP_GUARD_ROUNDS | 2 (2) | 2 (2) | 0 | UNRESOLVED | 15 |  |
| BigCodeBench/129 | 0 | 0 | 0 | chatgpt-codex/gpt-6-luna | gpt, nemotron, qwen3.5 | consensus | NO_SECOND_SOLVER | 0 (0) | 0 (0) | 0 | UNRESOLVED | 11 |  |
| BigCodeBench/17 | 0 | 0 | 0 | chatgpt-codex/gpt-6-luna | cerebras, gpt, lfm | consensus | NO_SECOND_SOLVER | 0 (0) | 0 (0) | 0 | UNRESOLVED | 11 | S:TAMPER;O:TAMPER |
| BigCodeBench/184 | 1 | 1 | 1 | chatgpt-codex/gpt-6-luna | gpt, hermes, l3 | consensus | NO_SECOND_SOLVER | 0 (0) | 0 (0) | 0 | UNRESOLVED | 11 |  |
| BigCodeBench/326 | 0 | 0 | 0 | chatgpt-codex/gpt-6-luna | gemma, gpt | consensus | NO_SECOND_SOLVER | 0 (0) | 0 (0) | 0 | UNRESOLVED | 10 |  |
| BigCodeBench/37 | 1 | 1 | 1 | chatgpt-codex/gpt-6-luna | ctx65536, gpt, jan | consensus | NO_SECOND_SOLVER | 0 (0) | 0 (0) | 0 | UNRESOLVED | 10 |  |
| BigCodeBench/374 | 0 | 0 | 0 | chatgpt-codex/gpt-6-luna | flint, gpt | primary | LOOP_GUARD_ROUNDS | 2 (2) | 2 (2) | 0 | UNRESOLVED | 16 |  |
| BigCodeBench/445 | 0 | 1 | 1 | chatgpt-codex/gpt-6-luna | gpt, north, thea | consensus | NO_SECOND_SOLVER | 0 (0) | 0 (0) | 0 | UNRESOLVED | 11 |  |
| BigCodeBench/477 | 1 | 1 | 1 | chatgpt-codex/gpt-6-luna | ernie, gpt, inkling | consensus | NO_SECOND_SOLVER | 0 (0) | 0 (0) | 0 | UNRESOLVED | 12 |  |
| BigCodeBench/486 | 0 | 0 | 0 | chatgpt-codex/gpt-6-luna | cydonia, gpt | consensus | NO_SECOND_SOLVER | 0 (0) | 0 (0) | 0 | UNRESOLVED | 10 |  |
| BigCodeBench/574 | 0 | 0 | 0 | chatgpt-codex/gpt-6-luna | gemini, gpt, llama, qwen2.5 | primary | LOOP_GUARD_ROUNDS | 1 (1) | 1 (1) | 0 | UNRESOLVED | 16 |  |
| BigCodeBench/654 | 1 | 0 | 0 | chatgpt-codex/gpt-6-luna | glm, gpt, nemotron | consensus | NO_SECOND_SOLVER | 0 (0) | 0 (0) | 0 | UNRESOLVED | 11 |  |
| BigCodeBench/720 | 0 | 0 | 0 | chatgpt-codex/gpt-6-luna | gpt, qwen2.5 | primary | LOOP_GUARD_ROUNDS | 2 (2) | 2 (2) | 0 | UNRESOLVED | 17 |  |
| BigCodeBench/777 | 1 | 1 | 1 | chatgpt-codex/gpt-6-luna | gpt, qwen2.5 | primary | LOOP_GUARD_ROUNDS | 2 (2) | 2 (2) | 0 | UNRESOLVED | 19 |  |
| BigCodeBench/915 | 0 | 0 | 0 | chatgpt-codex/gpt-6-luna | gpt, nemotron, qwen3.5 | primary | LOOP_GUARD_ROUNDS | 1 (1) | 1 (1) | 0 | UNRESOLVED | 14 |  |
| BigCodeBench/916 | 0 | 0 | 0 | chatgpt-codex/gpt-6-luna | gpt, nemotron, qwen3.5 | primary | NO_CHANGE | 2 (1) | 0 (0) | 1 | UNRESOLVED | 14 |  |
| BigCodeBench/964 | 0 | 0 | 0 | chatgpt-codex/gpt-6-luna | angelic, gpt, qwen3.5 | consensus | NO_SECOND_SOLVER | 0 (0) | 0 (0) | 0 | UNRESOLVED | 11 |  |
| BigCodeBench/99 | 1 | 1 | 1 | chatgpt-codex/gpt-6-luna | gpt, qwen3.5 | consensus | NO_SECOND_SOLVER | 0 (0) | 0 (0) | 0 | UNRESOLVED | 10 |  |
| BigCodeBench/999 | 1 | 1 | 1 | chatgpt-codex/gpt-6-luna | ernie, gpt, thedrummer | consensus | NO_SECOND_SOLVER | 0 (0) | 0 (0) | 0 | UNRESOLVED | 11 |  |
