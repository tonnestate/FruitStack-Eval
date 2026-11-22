# Kaggle Gemma 4 Developer Agent — Public Leaderboard Snapshot

**Export filename timestamp:** 2026-11-09 06:27:23 (timezone not specified in filename; Kaggle CSV export supplied by operator)  
**Purpose:** competitive landscape context for the independent Gemma 4 coding-agent entry. **Not** research evidence for SER's H1/H2/H3 and **not** a dataset of code/graph/repair tasks.

## Source and integrity

Original uploaded ZIP: `gemma-4-developer-agent-publicleaderboard-2026-11-09T06_27_23.zip`  
ZIP SHA-256: `7649eac070f0739c1cd26e959fa906f7326d54f00e21f188dc64bbfa7032f627`  
CSV SHA-256: `14c6dcd51023703b26d299a38c40621701bfe9a799cae1d0db0765759e8d6cb7`  
CSV columns: `Rank, TeamId, TeamName, LastSubmissionDate, Score, SubmissionCount, TeamMemberUserNames`  
Observed rows: **5,174** teams (5,175 CSV lines including header), seven columns, no malformed rows.  
Latest `LastSubmissionDate` in export: `2026-11-09 05:39:16` (as recorded by CSV; timezone not specified in CSV).

This report is an aggregate summary. It does not redistribute participant account identifiers or claim access to submitted agent code.

## Score distribution

| Public score | Teams |
|---|---:|
| 0.29 | 1 |
| 0.24 | 11 |
| 0.22 | 72 |
| 0.20 | 395 |
| 0.18 | 866 |
| 0.17 | 952 |
| 0.15 | 754 |
| 0.13 | 463 |
| 0.12 | 324 |
| 0.10 | 270 |
| 0.08 | 222 |
| 0.06 | 192 |
| 0.05 | 194 |
| 0.03 | 185 |
| 0.01 | 100 |
| 0.00 | 173 |

Checks: total **5,174**; mean score **0.13533**; median **0.15**. **479** teams scored at least 0.20; **84** scored at least 0.22; **12** scored at least 0.24. Median submissions per team: **5** (max **47**).

## What these numbers do and do not establish

The official scoring description says a submitted patch receives a PASS/FAIL on each issue, and overall score is the proportion of passing patches. The **public** board uses approximately **50%** of evaluation cases; the **private** cases determine final standings. Displayed two-decimal scores have limited resolution. The snapshot is observational ranking data—not paired experiments, hidden task-level ground truth, reproducible code, or a model-quality estimate.

The distribution does **not** identify which architecture, prompts, fine-tuning, skills, graph policy, or underlying mechanisms produced a score. Do not infer causal efficacy, use teams' names as evidence, reverse engineer private tasks, or put these standings in the manuscript's H1/H2/H3 Results tables. They may be briefly cited as dated competitive context with the appropriate caveat.

## Verified official competition constraints relevant to the working manuscript v0.2

Official reference: https://www.kaggle.com/competitions/gemma-4-developer-agent/overview  
Public board: https://www.kaggle.com/competitions/gemma-4-developer-agent/leaderboard

1. **Coding-agent entry format:** root `agent.yaml` inside `submission.zip`, with permitted ADK agent configuration, prompts, subagents, adapters, and skills. A private external FruitStack service is **not** the submission artifact.
2. **Supported model at the time verified:** `gemma-4-31b-it-qat-w4a16-ct` for all agents and subagents. Manuscript v0.2's alternative `gemma-4-e4b-it-qat-w4a16-ct` must not be assumed allowed without an updated official rule.
3. **Official tools:** `run_command`, `submit_patch`, `get_status`, `read_file`, `edit_file`, `write_file`, `get_code_neighbors`, `search_similar_code`, `get_code_subgraph`. `search_similar_code(query, k)` provides a query-search interface over the harness's precomputed embeddings; investigate whether that suffices before implementing a separate query encoder. Do not imply access to raw embeddings/graph files that has not been confirmed in the installed dataset.
4. **Evaluation:** issue-level patches are applied and independently tested; scoring budget is **12 hours for all tasks**, including sandbox setup, excluding validation time. Verify per-task restrictions in the installed `HARNESS_README.md`.
5. **Notebook accelerator:** Kaggle L4x4 pool allows 96 GB total GPU memory; sessions must have internet disabled. Availability of notebook GPUs does **not** prove identical hardware for official scoring.
6. **Deadlines shown in competition overview:** optional paper November 12, 2026; coding competition rules/entry November 25; coding final submission December 2, 2026, each at 23:59 UTC unless updated.

## Immediate research use

- Preserve the scientific manuscript v0.2 (SER), its preregistration, and H3 (A/B/C), H1 (E versus E-minus), H2 (E versus D-star).
- Treat this leaderboard strictly as a **competitive baseline**, not as an experimental treatment or research dataset.
- Run H3 and repair ablations on legitimate competition development tasks or eligible reproducible instances, under frozen snapshots and independent graders.
- Construct the competition submission using the permitted `agent.yaml`/ADK format and allowed Gemma base model; reuse research findings where they demonstrably help.
- Report official public and private evaluation separately. Do not assume public leaderboard rank is the final rank.
