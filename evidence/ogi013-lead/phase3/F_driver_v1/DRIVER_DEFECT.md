# Driver v1 defect (retained run, outcome as recorded)

- Defect: the coding driver (runners/ogi013_code_task.py, commit c995611) let the episode `submit` (a plain message) without any source diff, and the
  organisation (Brother Mode) was never asked to review code: no edit was ever made. Outcome of this run: status SUBMITTED, patch_bytes 0.
- Graded with evaluate_v2.1 (empty change): see eval_v21.json (0/16 F2P, 58/58 P2P, not resolved).
- Fixed by AMENDMENT-DRIVER-1 (ogi013_coding_gate.py wired into the driver). This run is retained and appears in every table as "F (driver v1, defective)".
- Outcome retained as recorded. Not deleted, not excluded.
