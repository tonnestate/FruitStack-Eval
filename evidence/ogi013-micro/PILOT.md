# Functional check of the team procedure: results (3 tasks x 3 arms, one start each; evaluator v2.2)

Not an OGI test, not a benchmark result. n = 3, no token matching, no N arm. The only possible outcomes are STOP or PROCEED_TO_C3_PLANNING (amended section 4). Nothing below claims that the organisation helps, improves or adds value.
All 9 episodes ran once with a final status; no INFRA_FAILED, no OPERATOR_INTERRUPTED (the detached pilot process survived the operator session end).

| task | arm | final status / release class | resolved | F2P | P2P | tokens (prompt+completion) | wall s |
|---|---|---|---|---|---|---|---|
| intervals-1 | T | RELEASED_NO_CONSENSUS | yes | 2/2 | 4/4 | 234,956 | 1,306 |
| intervals-1 | S | RELEASED_UNVALIDATED | yes | 2/2 | 4/4 | 29,554 | 193 |
| intervals-1 | L | DONE | yes | 2/2 | 4/4 | 88,490 (raw Codex: 75,392 cached input + 12,599 uncached input + 499 output) | 14 |
| duration-1 | T | RELEASED_NO_CONSENSUS | **no** | 1/2 | 2/2 | 245,392 | 1,818 |
| duration-1 | S | NO_PATCH | no | - | - | 26,679 | 269 |
| duration-1 | L | DONE | yes | 2/2 | 2/2 | 106,079 (97,920 cached + 7,481 uncached input + 678 output) | 17 |
| lru-1 | T | RELEASED_NO_CONSENSUS | yes | 3/3 | 3/3 | 186,362 | 1,258 |
| lru-1 | S | NO_PATCH | no | - | - | 83,022 | 476 |
| lru-1 | L | DONE | yes | 3/3 | 3/3 | 88,741 (80,768 cached + 7,356 uncached input + 617 output) | 12 |

Resolved with tokens per arm: **T 2/3 resolved, 666,710 tokens; S 1/3 resolved, 139,255 tokens; L 3/3 resolved, 283,310 raw tokens (254,080 of them cached input).**
Tokens per resolved task: T 333,355; S 139,255; L 94,437 (raw).

Stack MangoMe use (checkpoint writes by the evaluated stack, per episode; the stack made no MangoMe reads of its own): intervals T 65, S 6; duration T 48, S 5; lru T 32, S 5; L none (Codex runs outside the stack). Every T/S episode had its own WorkIdentity and EXECUTE turn (`run.json`).
Operator MangoMe use: none in this step.

## Facts about the T episodes (all three ended RELEASED_NO_CONSENSUS; no unanimous release, no complete C1-C4 chain: 0 complete, 24 partial, 2 harmful; `CHAIN.md`)
- intervals-1: both solvers' first positions and all later snapshots grade 2/2 (similarity 0.286, lineages poolside and dots3). Nothing could improve on hidden tests, so no chain could reach C4.
- lru-1: the first snapshot already graded 3/3 and was released; the later challenge/vote cycles produced no revision.
- duration-1: the first position (S3_first) and the first revision grade 2/2; revision 2 grades 1/2 and the release rule (most visible relevant tests passing) released that worse patch (`RELEASED.diff` 1/2). The two harmful chains are the objections O4/O5 whose revisions lowered the hidden F2P (2/2 -> 1/2). Solver lineage diversity was not met in that episode (one solver position).
- Wall: duration T ended at 1,818 s against the 1,800 s cap (the guard acts at turn granularity); token caps were respected.
## Facts about S and L
- S duration and lru ended NO_PATCH (guard `STOP:NO_PROGRESS` after 17 and 25 turns); S intervals released a 2/2 patch.
- L resolved all three tasks in 12-17 s with 3-4 commands each.

## Deviations and defects (reported, not fixed during the pilot)
- Arm L diff export: the runner's diff included binary `__pycache__/*.pyc` files, which `git apply` cannot apply, so the standard snapshot grader failed on the L diffs. L was graded by running evaluator v2.2 directly on the retained agent workspace (`runs/<task>/L/grade_ws_v22.json`; the evaluator copies only `django/` changes and ignores bytecode); `.py`-only diffs are retained as `L_final_py_only.diff`. No episode was rerun.
- The T release rule for duration-1 picked a worse patch than two earlier gate-accepted snapshots.

## Outcome under the amended rule
Facts: 0 complete C1-C4 chains in three T episodes, 2 harmful chains, 0 unanimous releases, T did not exceed L. This amended rule yields only STOP or PROCEED_TO_C3_PLANNING; the operator's reading of the facts is STOP. The decision is the owner's/lead's. Arm N has not been started and needs the owner's approval.
