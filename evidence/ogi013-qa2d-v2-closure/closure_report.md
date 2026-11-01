# QA-2D v2 closure report (exploratory, descriptive; study closed as infrastructure-infeasible)

**Conclusion.** QA-2D v2 could not complete its preregistered confirmatory study because the available Nemotron supply exceeded the infrastructure-failure threshold. The collected observations do not establish whether organized cooperation is superior to the controls.

## Scope and history
- 357 result rows: 198 reused QA-1 Luna rows (SL) + 159 new T/E/SN rows over 53 of the 400 preregistered questions. The planned 400-question confirmatory analysis (H1L, H1c with Holm) was **not** performed; nothing below is a confirmatory result.
- History: superseded v1 run (246 rows, archived, not used) -> Amendment A1 -> lock v2 (`f88e7d7`, source `dde6307`) -> 40 rows -> stopped for truth reconciliation (sync/local-truth fast-forwarded to `ab6cabe`) -> retrospective provenance addendum (written after the first 40 rows) -> resumed -> automatic pause at question 6264 (`INFRA_SHARE_ABOVE_10PCT:E`) -> closed by decision.
- The 16 questions observed in v1 are inside the first 53 questions of the same hash order and are described in Amendment A1.

## Infrastructure failures (reconciled against the row files and the printed run logs)
Total 36 = T 13 + E 12 + SN 11. By cause:

| cause | T | E | SN | total |
|---|---|---|---|---|
| call made; output unusable (reasoning leaked as content, finish_reason=length) | 4 | 3 | 3 | 10 |
| no provider call; route cooling down after upstream timeout (HTTP 502) | 4 | 4 | 3 | 11 |
| no provider call; route rate-limited / on cooldown (HTTP 429) | 5 | 5 | 5 | 15 |
| **total** | 13 | 12 | 11 | 36 |

Failure shares (new rows, 95% exact CI): T 13/53 = 24.5% [13.8, 38.3]; E 12/53 = 22.6% [12.3, 36.2]; SN 11/53 = 20.8% [10.8, 34.1].
A protocol-defined infrastructure failure is counted as incorrect in the primary table; it is **not** a model reasoning error.

## Arm outcomes, all 53 questions (primary view: infrastructure failures counted as incorrect)

| arm | correct (95% exact CI) | model-wrong (row OK, answer wrong) | infra-failed (counted wrong) | correct among OK rows |
|---|---|---|---|---|
| T | 36/53 = 67.9% [53.7, 80.1] | 4 | 13 | 36/40 = 90.0% [76.3, 97.2] |
| E | 36/53 = 67.9% [53.7, 80.1] | 5 | 12 | 36/41 = 87.8% [73.8, 95.9] |
| SL | 41/53 = 77.4% [63.8, 87.7] | 12 | 0 | 41/53 = 77.4% [63.8, 87.7] |
| SN | 39/53 = 73.6% [59.7, 84.7] | 3 | 11 | 39/42 = 92.9% [80.5, 98.5] |

Asymmetric exposure: T, E and SN depend on the free nemotron route and carry its infrastructure failures; SL (Luna) has none because its 198 rows are reused QA-1 rows. The primary view therefore penalises the nemotron-dependent arms for supply failures, which are not reasoning errors.

## Paired contingency tables, primary view (EXPLORATORY; no multiplicity control; not the preregistered Holm family)

| pair | both correct | first only | second only | neither | paired difference [exact conditional CI] | exact McNemar p |
|---|---|---|---|---|---|---|
| T vs SL | 32 | 4 | 9 | 8 | -9.4 pts [-20.1, +5.6] | 0.2668 |
| T vs E | 33 | 3 | 3 | 14 | +0.0 pts [-8.6, +8.6] | 1.0000 |
| T vs SN | 34 | 2 | 5 | 12 | -5.7 pts [-12.2, +5.5] | 0.4531 |
| E vs SL | 31 | 5 | 10 | 7 | -9.4 pts [-21.6, +6.6] | 0.3018 |
| E vs SN | 35 | 1 | 4 | 13 | -5.7 pts [-9.3, +4.1] | 0.3750 |
| SN vs SL | 34 | 5 | 7 | 7 | -3.8 pts [-15.8, +10.1] | 0.7744 |

## Sensitivity: questions with no infrastructure failure in any arm (n = 37 of 53) — labelled SENSITIVITY ANALYSIS

This subset is selected on infrastructure success, which depends on the supply and on call counts (T and E make more nemotron calls on harder, disagreeing questions). It is **not** unbiased evidence of superiority and does not replace the primary view.

| arm | correct (95% exact CI) |
|---|---|
| T | 34/37 = 91.9% [78.1, 98.3] |
| E | 33/37 = 89.2% [74.6, 97.0] |
| SL | 31/37 = 83.8% [68.0, 93.8] |
| SN | 35/37 = 94.6% [81.8, 99.3] |

| pair | both correct | first only | second only | neither | paired difference [exact conditional CI] | exact McNemar p |
|---|---|---|---|---|---|---|
| T vs SL | 30 | 4 | 1 | 2 | +8.1 pts [-5.8, +13.4] | 0.3750 |
| T vs E | 32 | 2 | 1 | 2 | +2.7 pts [-6.6, +8.0] | 1.0000 |
| T vs SN | 34 | 0 | 1 | 2 | -2.7 pts [-2.7, +2.6] | 1.0000 |
| E vs SL | 29 | 4 | 2 | 2 | +5.4 pts [-9.0, +14.8] | 0.6875 |
| E vs SN | 33 | 0 | 2 | 2 | -5.4 pts [-5.4, +3.7] | 0.5000 |
| SN vs SL | 31 | 4 | 0 | 2 | +10.8 pts [-2.2, +10.8] | 0.1250 |

## T arm descriptive trace (OK rows)
- T OK rows 40; first answers agreed 36; exchanges 4; stops {'AGREED_FIRST': 36, 'CONSENSUS_EXCHANGE_1': 3, 'NO_CONSENSUS': 1}.

## Resource consumption (new rows only; failed rows record no tokens, so these are lower bounds)

| arm | rows | tokens | calls | arm seconds |
|---|---|---|---|---|
| T | 53 | 902513 | 129 | 1215 |
| E | 53 | 840367 | 129 | 755 |
| SN | 53 | 47649 | 53 | 718 |
| total | 159 | 1790529 | 311 | 2689 |

