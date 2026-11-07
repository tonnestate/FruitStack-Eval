# OGI study package: task domains (DRAFT, not locked)

Selection criterion, taken from the research status (section D, "structural limit"): with multiple choice no objection can be executed, so cooperation there is only a persuasion channel. Every domain below has a grader that is **independent of every model**. It is a hidden test run, a machine-checked answer, an official environment grader or a deterministic recomputation, and it maps to a verifier kind of `runners/ogi013_org_discoveries.py` (`executed`, `official_grader`, `dataset_key`). The grader runs only after the episode, outside any live context. Its output never enters a prompt, a brief or the learning ledger's `capture`.

Licenses are as published by the dataset owners at the time of writing. The lock must record for each dataset the source URL, the revision or commit, the file sha256 and the license text actually fetched. A dataset whose fetched license differs from this table is dropped, not substituted. Question and task texts are never committed, only ids and hashes (as enforced by `tests/test_ogi013_qa1.py::test_no_question_text_in_any_committed_file`).

| id | domain | dataset (source) | license | grading method (verifier kind) | role in the study |
|---|---|---|---|---|---|
| D1 | agentic policy tasks | tau2-bench, airline and retail domains (`github.com/sierra-research/tau2-bench`) | MIT | official tau2 evaluator: final environment DB state plus required communication checks, reward in [0, 1], success = reward 1 (`official_grader`) | EVAL-001 primary family 1; EVAL-002 secondary: rules recur across tasks of a domain, but it needs a tau2 adapter in `runners/fs_runtime.py` (`fs_org_driver.Task` is prompt-to-answer, not interactive) |
| D2 | function-level code | BigCodeBench, complete split (`huggingface.co/datasets/bigcode/bigcodebench`); the "hard" subset (`bigcode/bigcodebench-hard`) is held out as D2-hard | Apache-2.0 | hidden unit tests run by the host in the existing bwrap sandbox (no network, workspace-only write); pass = all tests pass (`executed`) | EVAL-001 primary family 2 (positions 1-200, D2-hard excluded); EVAL-002 primary (transfer tasks = positions 201-400; tasks share library APIs, so knowledge can recur); EVAL-003 primary on D2-hard (all tasks) |
| D3 | repository-level code | SWE-bench Verified (`huggingface.co/datasets/princeton-nlp/SWE-bench_Verified`) | MIT (SWE-bench) | official SWE-bench harness: FAIL_TO_PASS and PASS_TO_PASS hidden tests (`executed`); gold-patch-invalid instances excluded before drawing (HARNESS_INVALID, as in `evidence/ogi013-lead/PREREG.md`) | EVAL-003 secondary, and EVAL-001 only if the budget allows (about 10 times the cost per task of D2) |
| D4 | mathematics | MATH-500, level 5 items (`huggingface.co/datasets/HuggingFaceH4/MATH-500`, derived from Hendrycks MATH) | MIT | final `\boxed{}` answer, symbolic equivalence via `math-verify` (Apache-2.0) with sympy; unparsable = wrong (`dataset_key`) | EVAL-001 secondary family, EVAL-003 secondary |
| D5 | research and analysis claims | UCI Wine Quality and UCI Adult (`archive.ics.uci.edu`), plus PhysalisMe `examples/generate_synthetic.py` with recorded seeds | CC BY 4.0 (UCI); PhysalisMe repo license for the generator | each task asks for a quantitative claim (direction and size of an association, out-of-sample score); graded by deterministic recomputation with PhysalisMe (`physalis_analyze` with a fixed seed, `physalis_claim_gate`) against a tolerance fixed at lock. On synthetic data, also graded against the known generating parameters (`executed`) | exploratory only: the grader adapter does not exist yet (see limitations) |

## Why these and not others
- tau2 is already integrated: `runners/ogi013_tau2_run.py`, the official grader as `tau2-official-grader` in `evidence/ogi013-learning/SPEC.md`, and the COLLAB-1 cost archive. Its domain policies make reusable knowledge possible (the research status, section C, says multiple-choice items "cannot test transfer"). Its interactive episodes do not fit `fs_org_driver.Task`, though, so EVAL-002 runs primarily on D2, which fits the existing driver unchanged.
- BigCodeBench-Hard is chosen over HumanEval or MBPP. Those are saturated and widely contaminated, so near-ceiling single-model accuracy would leave almost no discordant pairs. It is also chosen over SWE-bench as the main code family because the micro pilot cost about 222k tokens per T task on SWE-bench (`evidence/ogi013-micro/PILOT.md`).
- MATH-500 level 5 replaces AIME. AIME problems are not openly licensed.
- Two independent families, D1 and D2, are primary, because `evidence/ogi013-lead/PREREG.md` requires a consistent effect on two independent families for any claim beyond one family.

## Draw rule (all domains)
Order by ascending `sha256("OGI-STUDY-1|<domain>|" + task_id)`. Exclusions are applied before positions are taken: development tasks, tasks seen in any OGI-013 run, and harness-invalid tasks. Take the first n of the required sample size (PREREG_DRAFT.md section 5). The list and its sha256 are committed before any study call.

EVAL-002 seeds from the EVAL-001 D2 T episodes (positions 1-200) and transfers to D2 positions 201-400. The two sets are disjoint and fixed before any run. A discovery is never shown for the task it came from, as guaranteed by `LearningHook`.

## Leak guards (all domains)
- Hidden tests, gold patches, keys and expected DB states are stored outside every worker workspace and every prompt. The grader reads them only after the episode ends.
- Visible tests or examples given in the task statement are the same for every arm.
- The learning brief (EVAL-002) shows only discoveries that were VERIFIED by `executed` or `official_grader` on another task. Post-hoc `dataset_key` verifications are never shown, and neither is anything with "same question only" scope. This guard is enforced by `LearningHook` and tested in `tests/test_ogi013_learning_hook.py`.
- Grader outputs are stored only in result rows, never in the ledger `capture` input.

## Limitations
- D5 needs a grader adapter (claim parser plus PhysalisMe recomputation) that does not exist yet, so it is exploratory and is not part of any confirmatory family.
- BigCodeBench execution needs its pinned Python dependency set inside the sandbox. Tasks whose environment cannot be built are excluded before drawing, not after.
- Dataset revisions and licenses must be re-verified at lock (see above). Nothing was downloaded for this draft.
