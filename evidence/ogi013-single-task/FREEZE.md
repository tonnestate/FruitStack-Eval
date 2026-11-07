# OGI-013 SINGLE-TASK — frozen before any model ran on it (2026-10-30)

**Task:** `django__django-11019` (SWE-bench Lite, django/django), version 3.0: "Merging 3 or more media objects can throw unnecessary MediaOrderConflictWarnings"
(`django/forms/widgets.py` Media merge ordering). Problem statement = `task.json: problem_statement` (hints_text NOT given to either arm).
**Why this task (rule, outcome-independent):** `select_task.py` — SWE-bench Lite, pure-Python repos, gold patch >= 3 hunks and >= 40 changed lines, >= 2 FAIL_TO_PASS tests, smallest sha256("OGI013-SINGLE-TASK-1|"+id).
The rule's pool contains exactly ONE instance (SWE-bench Lite has only single-file gold patches, so the cross-component criterion had to be operationalised by patch size). No model has touched it.
**Repository revision (both arms):** django/django @ `93e892bb645b16ebaf287beb5fe7f3ffe8d10408` (environment_setup_commit `419a78300f7cd27611196e1e464d50fd0385ff27`), shallow checkout, identical copy per arm.
**Acceptance criteria:** `evaluate.py` — overwrite the test files with the task's `test_patch`, run Django's own runner (`tests/runtests.py`, Python 3.8.20 venv with pytz, sqlparse, asgiref) on the modules of
the 16 FAIL_TO_PASS and 58 PASS_TO_PASS tests; resolved = all 16 + all 58 pass. No LLM judge, no simulator. The agents never see `test_patch`, `patch` or `hints_text`.
**Resource limits (both arms):** 60 min wall clock; FruitStack additionally under the existing per-episode ceilings (110 provider requests, 200,000 tokens, 24,000 per step, USD 0). The fixed model
(`gpt-6-luna`, ChatGPT headless) runs with its native tools in a workspace-write sandbox; actual Codex usage is recorded separately from any estimate.
**Hashes:** task.json 28f4bd9a13e7ae6a75b69d81a3791e554d3376186aea37235977e63eb6f3ad54  evaluate.py 758f603eede07b0626e8a07e66d890f347b312a3adf5977bc54a91930befb657  select_task.py 5ff099c47e536b01a66ef9fb91b15e54f9e3b0bc56cd9513cf2c8daaffb41ccd
