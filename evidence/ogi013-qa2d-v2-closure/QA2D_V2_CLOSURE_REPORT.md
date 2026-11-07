# QA-2D v2 closure report

**Conclusion (verbatim).** QA-2D v2 could not complete its preregistered confirmatory study because the available Nemotron supply exceeded the infrastructure-failure threshold. The collected observations do not establish whether organized cooperation is superior to the controls.

Status: CLOSED_INFRASTRUCTURE_INFEASIBLE. Everything below is exploratory and descriptive, produced from the preserved rows by `analysis/closure_analysis.py` (deterministic; no p-values, no hypothesis tests, no winner). The planned 400-question confirmatory analysis (H1L, H1c) was not performed.

## 1. Preserved evidence and rows
- 357 rows = 198 reused QA-1 Luna rows (SL) + 159 new rows (T, E, SN: 53 each) over 53 questions. 145 of the 198 SL rows are not paired with any other arm and are excluded from every comparison (preserved).
- Preserved read-only with sha256 in `closure_manifest.json`: lock v2, Amendment A1, provenance addendum (`b62e853`), all rows, `invocations.json`, the gateway request extract, the PlumMe receipt-window id hash, the superseded v1 lock and archived rows.

## 2. Infrastructure failures, reconciled row by row
**Erratum.** The earlier report text said "34 failures" in its cause summary. That figure was an addition error. The row-level recount below is the correct total: **36** = T 13 + E 12 + SN 11, equal to the cause total 15 + 11 + 10.

| cause | T | E | SN | total |
|---|---|---|---|---|
| C1 no provider call; HTTP 429 no capacity / rate-limited route | 5 | 5 | 5 | 15 |
| C2 no provider call; refusal during cooldown after an upstream timeout (HTTP 502) | 4 | 4 | 3 | 11 |
| C3 call made; output unusable (REASONING_LEAKED_AS_CONTENT at the length cap) | 4 | 3 | 3 | 10 |
| **total** | 13 | 12 | 11 | 36 |

By process (first process 22:53:39Z-23:10:12Z; resumed process 23:20:56Z-00:31:18Z) and cumulative, infra-failed / new rows:

| arm | first process | resumed process | cumulative |
|---|---|---|---|
| T | 2/14 | 11/39 | 13/53 |
| E | 0/13 | 12/40 | 12/53 |
| SN | 1/13 | 10/40 | 11/53 |

Gateway cross-check (`inputs/gateway_nemotron_requests_v2_windows.csv`): 167 nemotron requests, 13 errors, 11 of them 60 s aborts.

A protocol-defined infrastructure failure is counted as incorrect in the primary view. It is not a model reasoning error.

## 3. Primary outcomes, all 53 questions (infrastructure failures counted as wrong)

| arm | correct / 53 (95% exact CI) | rows OK | model-wrong (OK row, wrong answer) | infra-failed (protocol: counted wrong) |
|---|---|---|---|---|
| SL | 41/53 = 77.4% [63.8, 87.7] | 53 | 12 | 0 |
| SN | 39/53 = 73.6% [59.7, 84.7] | 42 | 3 | 11 |
| T | 36/53 = 67.9% [53.7, 80.1] | 40 | 4 | 13 |
| E | 36/53 = 67.9% [53.7, 80.1] | 41 | 5 | 12 |

Disclosed asymmetry: SL rows were reused (zero infrastructure exposure). T and E need several successful nemotron calls per question and SN needs one; T and E are structurally more exposed to the supply failures than SN, and all three more than SL.

### Paired 2x2 tables, primary view (counts only; no test, no p-value)

| pair (A vs B) | n | both correct | A only | B only | neither |
|---|---|---|---|---|---|
| T vs SL | 53 | 32 | 4 | 9 | 8 |
| T vs E | 53 | 33 | 3 | 3 | 14 |
| T vs SN | 53 | 34 | 2 | 5 | 12 |
| E vs SL | 53 | 31 | 5 | 10 | 7 |
| E vs SN | 53 | 35 | 1 | 4 | 13 |
| SN vs SL | 53 | 34 | 5 | 7 | 7 |

### T arm trace (OK rows)
- 40 OK T rows; first answers agreed 36; reached an exchange 4; stops {'AGREED_FIRST': 36, 'CONSENSUS_EXCHANGE_1': 3, 'NO_CONSENSUS': 1}.

## 4. Resources (new rows; failed rows record no tokens, so tokens/calls are lower bounds)

| arm | rows | tokens | calls | arm seconds |
|---|---|---|---|---|
| T | 53 | 902513 | 129 | 1215 |
| E | 53 | 840367 | 129 | 755 |
| SN | 53 | 47649 | 53 | 718 |
| total | 159 | 1790529 | 311 | 2689 |

Provider attempts (`invocations.json`): 309 of 3,000. Wall time of the two processes: 16 min 33 s + 70 min 22 s = 86 min 55 s. Receipt counts are in `closure_manifest.json`.

## 5. Stop reason
`INFRA_SHARE_ABOVE_10PCT:E` at 00:31:18Z (2026-11-01) after question 6264 (40 questions in the resumed process): the preregistered pause rule. No restart. Closed by decision as infrastructure-infeasible.

## 6. Sensitivity analysis (separate; labelled)

**Selected by an outcome-related exclusion; not unbiased; does not replace the primary outcomes; no superiority interpretation.** Whether a row is infrastructure-failed depends on the supply and on how many nemotron calls a question needs.

### 6a. All four arms OK (n = 37 of 53)

| arm | correct / 37 (95% exact CI) | rows OK | model-wrong (OK row, wrong answer) | infra-failed (protocol: counted wrong) |
|---|---|---|---|---|
| SL | 31/37 = 83.8% [68.0, 93.8] | 37 | 6 | 0 |
| SN | 35/37 = 94.6% [81.8, 99.3] | 37 | 2 | 0 |
| T | 34/37 = 91.9% [78.1, 98.3] | 37 | 3 | 0 |
| E | 33/37 = 89.2% [74.6, 97.0] | 37 | 4 | 0 |

| pair (A vs B) | n | both correct | A only | B only | neither |
|---|---|---|---|---|---|
| T vs SL | 37 | 30 | 4 | 1 | 2 |
| T vs E | 37 | 32 | 2 | 1 | 2 |
| T vs SN | 37 | 34 | 0 | 1 | 2 |
| E vs SL | 37 | 29 | 4 | 2 | 2 |
| E vs SN | 37 | 33 | 0 | 2 | 2 |
| SN vs SL | 37 | 31 | 4 | 0 | 2 |

### 6b. Pairwise complete cases (both rows OK for that pair)

| pair (A vs B) | n | A correct (95% exact CI) | B correct (95% exact CI) | both | A only | B only | neither |
|---|---|---|---|---|---|---|---|
| T vs SL | 40 | 36/40 = 90.0% [76.3, 97.2] | 34/40 = 85.0% [70.2, 94.3] | 32 | 4 | 2 | 2 |
| T vs E | 38 | 35/38 = 92.1% [78.6, 98.3] | 34/38 = 89.5% [75.2, 97.1] | 33 | 2 | 1 | 2 |
| T vs SN | 38 | 34/38 = 89.5% [75.2, 97.1] | 36/38 = 94.7% [82.3, 99.4] | 34 | 0 | 2 | 2 |
| E vs SL | 41 | 36/41 = 87.8% [73.8, 95.9] | 34/41 = 82.9% [67.9, 92.8] | 31 | 5 | 3 | 2 |
| E vs SN | 40 | 35/40 = 87.5% [73.2, 95.8] | 38/40 = 95.0% [83.1, 99.4] | 35 | 0 | 3 | 2 |
| SN vs SL | 42 | 39/42 = 92.9% [80.5, 98.5] | 34/42 = 81.0% [65.9, 91.4] | 34 | 5 | 0 | 3 |

## 7. Disagreement rate (planning estimate, not a result)

| source | n | first answers differ | rate (95% exact CI) | expected exchange cases at 400 questions (same rate and CI) |
|---|---|---|---|---|
| QA-2D v2 T OK rows: Luna vs nemotron first answers (both exist) | 40 | 4 | 4/40 = 10.0% [2.8, 23.7] | 40 [11, 95] |
| QA-2D v2: SL vs SN single-call letters, both rows OK (same prompt) | 42 | 6 | 6/42 = 14.3% [5.4, 28.5] | 57 [22, 114] |
| QA-1 original T OK rows with two first answers (none: all 6 OK T rows had a single first answer; no Luna-vs-nemotron pairs exist in QA-1) | 0 | - | - | - |

Sources: `inputs/results.jsonl` (T `first_by_pos`, SL/SN letters) and `inputs/qa1_T_rows.jsonl` (QA-1 original study rows). QA-1 contains no Luna-vs-nemotron pairs, so its row is a different pair of models and only indicates scale.
Limits: small n; one model with a high failure share; the 53 questions are the first in a hash order; rows that failed infrastructure checks are missing from the T-based rate. This is not a power claim for H1/H1c and not a recommendation for a v3.

## 8. Scientific history

| time (UTC) | event | SHA / reference |
|---|---|---|
| 2026-10-31 21:57:04Z-22:24Z | v1 run under lock v1 (started before the correction order; stopped by PIDs); 246 rows (198 SL + 48 new over 16 questions), archived and not used | lock v1 `6c20e7a` (22:57+01:00 commit), source `84ed28f` |
| 2026-10-31 (v1 rows) | the 16 observed questions: 12 OK T rows, 11 agreed, 1 exchange; they inform no later decision | Amendment A1 |
| 2026-10-31 22:45:36Z | Amendment A1 (post-lock runner changes listed; independence from the 16 questions argued) | `dde6307` |
| 2026-10-31 22:53:37Z | lock v2 | `f88e7d7`, source `dde6307` |
| 2026-10-31 22:53:39Z-23:10:12Z | v2 first process: 40 new rows over 14 questions; stopped by PIDs for truth reconciliation | `invocations.json` used 73 |
| 2026-10-31 ~23:15Z-23:19Z | truth reconciliation: GitHub sync/local-truth fast-forwarded 313a015a -> ab6cabe5; canonical local main and sync/local-truth fast-forwarded (9 uncommitted items byte-identical) | main == sync/local-truth == `ab6cabe5` |
| 2026-10-31 23:20:46Z | provenance addendum, written after 40 rows existed; executed bytes not captured at launch | `b62e853` |
| 2026-10-31 23:20:56Z-2026-11-01 00:31:18Z | v2 resumed process: +119 rows (resumed run total 159 new rows over 53 questions); automatic pause `INFRA_SHARE_ABOVE_10PCT:E` | used 309 |
| 2026-11-01 | closed as infrastructure-infeasible (this report) | head at generation: see `closure_manifest.json` |

**Conclusion (verbatim).** QA-2D v2 could not complete its preregistered confirmatory study because the available Nemotron supply exceeded the infrastructure-failure threshold. The collected observations do not establish whether organized cooperation is superior to the controls.
