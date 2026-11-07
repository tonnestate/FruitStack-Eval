# Amendment A1 to the QA-1 pre-registration (dated 2026-10-31)

Text received from the lead (process counts only, no correctness data):
1. Every 2-hour progress line adds: T rows with >= 1 challenge round; >= 1 grounded objection; >= 1 REPLY carrying evidence; an evidenced WITHDRAWN.
2. Mechanism stop: at 80 T rows with fewer than 5 containing an evidenced REPLY, stop QA-1, keep all rows, report "mechanism did not engage" with the counts; no correctness analysis before that report.
3. QA-2 gate: QA-2 starts only if the finished QA-1 has evidenced REPLY events in >= 20 of 198 T rows; otherwise do not start QA-2, report the counts, stop.
4. The run is otherwise untouched; A1 is recorded as a dated amendment with its commit hash.

## Timing disclosure (mandatory)
A1 arrived AFTER QA-1 had finished (792/792 rows, 2026-10-31 ~15:04Z) and AFTER the sealed correctness analysis and
the report had been produced. It was therefore NOT in force during the run: items 1 and 2 could not be applied
(no amended progress lines were posted, no mechanism stop was evaluated live). The premise "written before any
outcome look" does not hold for this study. A1 is recorded as a post-hoc amendment; item 3 is applied to the finished study.

## Process counts, finished QA-1 (198 T rows; computed from results.jsonl process fields only)
- T rows with >= 1 challenge round: 0 / 198
- T rows with >= 1 grounded objection: 0 / 198
- T rows with >= 1 REPLY (evidenced or not): 0 / 198
- T rows with an evidenced WITHDRAWN: 0 / 198
- Evidenced REPLY events: 0 of 198 T rows (6 T rows were OK; 192 infrastructure-failed before any exchange).

## Gate result
Item 3: 0 < 20, so QA-2 is NOT started. Item 2 would have triggered ("mechanism did not engage") at 80 T rows; the final
counts are the same (0). The finding reflects the infrastructure outage (192/198 T rows failed before collaboration), so it
shows the mechanism was not exercised, not that it was exercised and failed.
