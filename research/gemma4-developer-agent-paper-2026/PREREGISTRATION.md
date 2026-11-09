# Preregistration — SER study, H3 localization (own benchmark)

Committed **before** any confirmatory H3 outcome was computed. Date: 2026-11-09 (Europe/Berlin).
Applies to `PAPER.md` v0.2 §3.2, §4, §5.1. H1/H2 are preregistered separately before their first episode.

## Data (deviation from PAPER v0.2 §3.1, stated in the paper)

- **Not the Kaggle competition data.** No Kaggle credentials, mounts or competition graph exist on the execution
  host (see `EXECUTION_REPORT_2026-11-09.md`). Per owner order 2026-11-09 the study uses an own benchmark:
  SWE-bench Verified, test split, 500 instances, local parquet
  (sha256 `a45b1fe4e2f0c839…`, full hash in `h3_eval/TASK_MANIFEST.json`).
- Graph: rebuilt per task with Python `ast` at the task's `base_commit` (`h3_eval/swebench_adapter.py`).
  Node type: function/method/class with file, qualname, signature, source span.
  Edge types: `contains` (lexical nesting) and `calls` (call-name resolution: same file first, otherwise
  global name with ≤ 3 definitions; ambiguous names unlinked). No `imports`/`inherits` edges.
- `dense_ranking` omitted for **all** tasks (no competition encoder). Arm A is therefore BM25 only.
- Gold patch is read only by the scorer.

## Tasks

- Deterministic draw: `swebench_adapter.draw(rows, 500)` (stratified by repo, order by sha256 of salt `GEMMA4-SER|` + id).
- **Pilot (excluded from all results):** first 3 of the draw — `astropy__astropy-14369`, `django__django-14089`,
  `matplotlib__matplotlib-24627`. Disclosure: the pilot summary (recall values on these 3 tasks) was printed
  during the smoke run, so pilot outcomes were seen, not only wall time. They carry no weight in any result.
- Pilot timing (per task, 8-core CPU, no GPU): adapter ≈ 10 s; arm A 2.4–6.4 s; arm B 0.1–0.4 s.
  Hence no compute constraint on n.
- **Confirmatory n = 497**: the remaining draw, in manifest order (`h3_eval/TASK_MANIFEST.json`).
  Exclusion rule: a task whose snapshot cannot be built or whose symbol table is empty is excluded and listed.
  Tasks without gold symbols stay in for file recall only (evaluator rule).

## Evaluator and frozen parameters

- `h3_eval/ser_h3.py` unchanged, config `ser-h3-1.0`,
  digest `f02603adcd3a70e984b420b098826b7039cb8003e0a44756613929c54066b8dd` (covers CONFIG and FILTER_PROMPT).
- α 0.5 · 10 top seeds + ≤ 10 verbatim-name seeds · RRF k 60 · arm-A top-3 protected in top 10 ·
  all edge types are content edges.
- Runtime: Python 3.12.14, numpy 2.5.4, scipy 1.18.1 (venv `/root/fruits/research/GEMMA4-SER/.venv`).

## Arm C (Gemma recognition filter)

- **C (confirmatory, locked model `gemma-4-31b-it-qat-w4a16-ct`, greedy):** not executable on this host
  (no GPU; no available route serves this checkpoint). Reported as *not run* unless that runtime becomes available.
- **C′ (exploratory, labelled deviation):** same prompt, parser and fallback, model `gemma-4-31b-it`
  (same base model, not the QAT W4A16 checkpoint) via an authorized PlumMe route, temperature 0, max 512
  output tokens, one call per task. Provider, route and raw response are logged per task. C′ is never
  reported as C, never pooled with C, and carries no confirmatory claim.

## Analysis (as PAPER §4)

- Primary: symbol Recall@10, B vs A (and C vs B if C runs): Wilcoxon signed-rank + paired bootstrap 95 % CI
  (10,000 resamples, seed 0). Non-inferiority (margin 0.02) on the direct subset (A has a gold symbol in top 10).
- Secondary: file Recall@1/@5, per-repo breakdown (descriptive), wall time per arm.
- Everything reported as observed; no outcome-dependent change of parameters, tasks or metrics.
