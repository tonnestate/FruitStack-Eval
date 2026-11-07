# OGI-013 QA-2D Timing Breakdown

**Status:** descriptive reconstruction from retained closure artifacts; not an EVC calibration set.

## Inputs and method

- Read-only input: `evidence/ogi013-qa2d-v2-closure/inputs/results.jsonl` (357 rows) and `closure_manifest.json`.
- Grouped rows by `arm`; included numeric `seconds` values only. Percentiles use nearest-rank (`ceil(.95*n)`).
- The closure report records failed-row times as absent; therefore successful-row latency summaries are selected on observability/outcome and are not unbiased end-to-end latency estimates.
- The manifest pins `results.jsonl` SHA-256 `4199ad94d894c6ed019ad26287857ad2d718cc4254e7cd9285e319e831dbd800` and the report SHA-256 `d03b1d8c56b7ae3e6611b2375903c1ab840f35b3a032741b6064c0d126372834`.

## Observed arm time

| Arm | Rows | Successful | Timed rows | Sum (s) | Mean (s) | P50 (s) | P95 (s) | Range (s) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| T | 53 | 40 | 40 | 1215.0 | 30.38 | 11.4 | 89.5 | 4.2–156.0 |
| E | 53 | 41 | 41 | 755.4 | 18.42 | 9.9 | 54.8 | 3.2–96.5 |
| SN | 53 | 42 | 42 | 718.2 | 17.10 | 10.25 | 56.4 | 2.8–76.7 |
| SL | 198 | 198 | 198 | 978.9 | 4.94 | 4.2 | 10.4 | 2.7–14.9 |

T, E and SN each have 13, 12 and 11 rows respectively without an observed numeric duration; these are infrastructure-failed rows. SL is reused from QA-1 and has no new QA-2D infrastructure exposure. The closure report's aggregate arm seconds are rounded to whole seconds (T 1215, E 755, SN 718; SL is reused).

## What cannot be reconstructed

The retained/public closure bundle does not include the per-exchange model-output files (`exchange/*.json`) or the detailed event stream. Although the locked runner can record `phase_seconds`, per-exchange durations, and per-call `Timing`, those stage-level observations are not present in the published closure inputs. Gateway request latency is not a substitute for arm or phase latency. The two process wall times (16m33s and 70m22s; total 86m55s) are in the closure report, but cannot be fairly apportioned to arms from retained evidence.

## Consequence for EVC

This breakdown supplies observed coarse arm-time totals and shows substantial tail latency and outcome-dependent missingness. It does not provide action-level marginal benefit, action-level cost, comparable phase timing, or sufficient completed outcomes to fit/calibrate an EVC policy. QA-2D was closed `CLOSED_INFRASTRUCTURE_INFEASIBLE`; these data do not support an EVC calibration or an organization-superiority claim. Further EVC calibration remains `NOT CALIBRATED` pending a separately approved, adequately observed dataset.
