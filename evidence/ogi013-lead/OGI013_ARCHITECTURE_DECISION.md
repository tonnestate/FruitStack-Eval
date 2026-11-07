# OGI-013 architecture decision (owner, 2026-10-31) and sequencing (lead, 2026-10-31)

- Code Mode = communication and execution technique (typed, compact calls; deterministic chaining and verification).
- EVC = the mathematical decision basis for any further agent activation.
- CherryMe = domain-level control (independent reasoning, critique, revision, termination).
- Until EVC is calibrated on real outcome data and independently checked, the current validated control stays active.
- Sequencing: QA-2D first, from the commits recorded in `QA2D_LOCK.txt`; no change to any component QA-2D uses until its report exists; no Code Mode / EVC development before that report
  (only a written inventory of sections 3-8, one page, no code, no model calls). Afterwards: section 8 (timing breakdown from the QA-2D runs), then EVC calibrated on the QA-2D outcomes, one step at a
  time, each compared on the same task set against the QA-2D duo as baseline (section 10). No development sessions in parallel with the QA-2D run.
