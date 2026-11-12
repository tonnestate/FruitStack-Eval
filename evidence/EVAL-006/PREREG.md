# EVAL-006 pre-registration: full FruitStack organization vs one model call on BigCodeBench-Hard (EXPLORATORY)

Written and committed 2026-11-12, before any model call of this evaluation. Separately versioned from OGI-013 and EVAL-001..005. Exploratory: n = 20,
no hypothesis is confirmed or rejected by it, and no superiority claim follows from it in either direction. Negative results are reported as they are.

## 1. Tasks and split

- Pool: the 130 ELIGIBLE ids of BigCodeBench-Hard v0.1.4 in `runners/ogi_tasks/eligibility.json` (official semantics, owner decision D2 2026-11-09; dataset
  file sha256 `73a4270b…a6ce79`, pinned in `runners/ogi_tasks/datasets.json`). These tasks were never run by the full organization before.
- Draw: `sorted(random.Random(20261112).sample(sorted(eligible_ids), 20))` (CPython 3.12.14 Mersenne Twister; `runners/eval006.py split`). **Seed 20261112.**
- The 20 ids (`task_ids.txt`, sha256 of the file = `1c76f10937d4b5f228ef2f941090a3a2c9a77c6d3be74080ab70ab6066656793`):
  1008, 1015, 129, 17, 184, 326, 37, 374, 445, 477, 486, 574, 654, 720, 777, 915, 916, 964, 99, 999 (all `BigCodeBench/<n>`).
- The other 110 eligible ids (`reserved_ids.txt`, sha256 `d936b53c1a6edcb4b35c43297316c99aae134c107f759028775f9b94bb056cd4`) are **RESERVED** for later
  confirmatory work. They are not used in EVAL-006, not for tuning, smoke tests or prompt development, and nothing observed here is evaluated on them.
- Before this commit the grader was smoke-tested on two of the 20 ids with the dataset's reference solution and a stub (PASS / FAIL as expected). No model saw
  any task.
- Task texts, tests and raw model answers stay outside the repository in the run directory `/root/fruits/research/EVAL-006` (datasets.json rule). Committed
  evidence carries ids, digests, grades and accounting only.

## 2. Arms (same tasks, same PlumMe supply and policy, zero cash)

Shared: real PlumMe supply (`fs_runtime.operational_service()`: `Settings.load()` + default adapters), environment of the 2026-11-12 operational launcher
(`/root/.plumme/runtime.env`, `PLUMME_ZERO_CHARGE_DISPATCH=1`, `PLUMME_COST_POLICY=FREE_ONLY` — PlumMe reports this variable as deprecated and applies its
budget-aware AUTO policy; zero cash is enforced by zero-charge dispatch). Each arm has its own isolated `PLUMME_STATE_DIR` (`$RUN/state-single`,
`$RUN/state-org`), each seeded with a copy of `/root/fruits/research/FRUITSTACK-FULLSTACK-OPERATIONAL-20261112/competence-live-copy.jsonl`
(sha256 `3e3ee29a60e0a2e04508563bcfb152e498cc150b0b5c8dab617d1880bc373ffd`) as `competence.jsonl`; an arm's state carries over between its own tasks only.

Objective text (both arms) = the task's `instruct_prompt` (stripped) + `"\n\nEnd your answer with exactly one fenced python code block."`
(`fs_runtime.CODE_FORMAT`). No tests are shown to either arm.

- **SINGLE** (`runners/eval006.py single`): one AUTO PlumMe REASONING call through PeachMe's `PlumMeProvider` (acquire: role REASONING, objective hint = first
  512 chars, no required skills, max_cost_usd 0.5; execute: prompt = the objective text exactly, max_output_tokens 2000, max_total_tokens 6000,
  max_cost_usd 0.5 — the same per-step ceilings a research worker gets: `ResearchPlan.max_output_tokens` = 2000, reservation = output + 4000, worker
  budget max_cost_usd 0.5). Retry rule = Brother Mode's SOLVE replay rule (`cherryme.brother`): a failed delivery is replayed once unless its class is
  unconfirmed (`EXECUTION_NOT_CONFIRMED*`, `UNCERTAIN_CHARGEABLE`); the replay excludes the failed lineage when the class is one PeachMe's WorkerPool retires
  (`EXECUTION_NOT_PERFORMED`, `EXECUTION_OUTPUT_UNUSABLE`, `EXECUTION_NOT_CONFIRMED`, `NO_OUTPUT`). So at most 2 calls. Note: ORG's pool can additionally
  replace failed workers (max_workers 3 + max_replacements 2); that is part of the organization, not added to SINGLE.
- **ORG** (`runners/eval006.py org`): `fs_runtime.run()` → `mission()` with the task as objective and the claim "The final fenced python code block of the answer
  is a correct and complete implementation of the task as specified." Config = `config/fs_runtime/operational_20261112.toml` (mission budget 2, call_budget 10,
  session budget 14 calls / 120k tokens / USD 1.0; worker budget 12 calls / 60k tokens / USD 0.5; LSD on; n_solvers 2; max_rounds 1; MangoMe memory backend;
  OrangeMe local ledgers) **minus** the PhysalisMe analysis (its synthetic dataset is unrelated to these tasks; no tool registry). Full path otherwise:
  PEACH-MISSION/1, CherryMe inquiry, Research Tree, LSD Room, Brother Mode with PlumMe workers, AppleMe diagnosis/advice, knowledge, MangoMe/OrangeMe.
  - **Research verifier: `verifier=None`.** BigCodeBench provides no public example tests separate from its grading tests: the row fields are task_id,
    complete_prompt, instruct_prompt, canonical_solution, code_prompt, test, entry_point, doc_struct, libs (+ q_idx, question, score, _id); `test` is the
    grading suite, and the docstring examples are not executable tests. FSE's visible/hidden split (`ogi_tasks/code.py`) is an FSE construct whose visible
    third is part of the official grading suite, so running it as the host check would leak part of the grade. Without a check, nothing executes the code
    inside the mission and the claim cannot be settled by model statements (mission state UNRESOLVED is expected and is not a failure of the arm).
  - **Candidate signature for code**: `fs_runtime.code_signature` = the last fenced block tagged python/python3/py or untagged, stripped (task field
    `answer_format = "python_block"`). The ANSWER-line reader `candidate_signature` is unchanged for the old tasks (default `answer_line`).
  - **ORG's answer** = PeachMe `verify_candidate`'s rule applied without a verifier (`fs_runtime.brother_summary`): the signature of Brother Mode's final
    positions, consensus if all equal, else the primary = the first position. Every final position (incl. a specialist tie-break) is recorded and graded as
    a secondary, descriptive "any final position" column.
  - Knowledge: each ORG task runs in its own process and out directory (needed for per-task interleaving), so no knowledge carries between tasks; without an
    executed check nothing would be INDEPENDENTLY_CHECKED anyway.
- Extraction is the same for both arms: the graded code is `code_signature(final text)`; no fenced block = NO_CANDIDATE (graded as fail, counted as abstention).

## 3. Execution

- Interleaved per task: for each of the 20 ids in sorted order, SINGLE then ORG, one process each (`evidence/EVAL-006/run.sh`), so both arms meet the same
  supply conditions within minutes. Free supply is volatile and another FruitStack run may share providers; failures are recorded, not hidden.
- Re-attempt rule (both arms, decided now): after all 20 tasks, a task-arm that ended with no candidate AND no model output at all (zero success receipts in its
  PlumMe state for that invocation, e.g. SUPPLY_UNAVAILABLE before any dispatch) is re-attempted exactly once; the re-attempt is final and the earlier attempt
  is kept. A task-arm that received any model output is final.
- Component sources are frozen `git archive HEAD` copies in `$RUN/src`: CherryMe 4abffc6, PeachMe 56764bf, PlumMe 34152e2, AppleMe aca5f8b, MangoMe 8a69f30,
  OrangeMe 366b450, PhysalisMe 448a3b1, PomeloMe b62f64b (full hashes in `$RUN/REVISIONS.txt`); FSE = this branch `cc/eval006-fullorg` at this commit;
  interpreter `/root/fruits/ogi-final/.venv/bin/python` (3.12.14). Zero cash; no cloud CI.

## 4. Grading (host, after both arms)

- `runners/eval006.py grade`: every candidate (SINGLE, ORG, and each ORG final position) gets an opaque random key; the list is shuffled and graded by ids and
  code only with `ogi_tasks.grade(..., mode="confirmatory")` = official in-process semantics in bwrap with the static tamper audit, in the pinned grader venv
  `/root/fruits/ogi-tasks/.venv` (Python 3.12.14). The blind grade file is written before the key→arm map is joined.
- **Primary metric: pass@1 per task (0/1) = every test of the task's suite passes AND the tamper audit is clean** (official BCB pass@1; no test was shown to
  any arm, so the full suite is the grade). Secondary: FSE's hidden-only grade (`correct`), raw all-tests-pass ignoring the tamper audit, ORG any-final-position.
- Also recorded per arm: provider calls, input/output tokens (PlumMe receipts of that invocation), cash, wall time (whole process incl. supply discovery),
  abstentions/no-candidate, failure receipts and error classes, models and lineages used.

## 5. Analysis (`runners/eval006.py analyze`)

Paired per-task table; pass rates with exact Clopper-Pearson 95% CIs; paired difference with the exact McNemar p-value (two-sided binomial on discordant
pairs) — descriptive, exploratory; tokens and calls per solved task. Attribution only as far as the data allows: tasks one arm solved and the other did not;
whether Brother Mode changed ORG's answer (CRITIQUE rows with DISSENT, REVISION rows whose candidate digest differs from the author's SOLUTION); whether
the models differed. With n = 20 an observed difference of a few tasks is compatible with no difference.
