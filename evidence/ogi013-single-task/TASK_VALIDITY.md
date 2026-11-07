# TASK_VALIDITY — django__django-11019 (Addendum 4 section B.1)

Task is not in SWE-bench Verified (it is a SWE-bench Lite instance used as the frozen single task).

Issue behaviour is checked separately from the hidden tests with `repro_issue_example.py` (the issue's own three-widget example: merging `Media` of three widgets must emit no `MediaOrderConflictWarning` and keep `text-editor.js` < `text-editor-extras.js` < `color-picker.js`). Exit 0 = issue behaviour fixed.

| tree | result (run 2026-10-30, venv38, Django 3.0-dev base `base_commit`) |
|---|---|
| base (unmodified) | ISSUE_BEHAVIOUR_PRESENT: merged order `['text-editor-extras.js', 'color-picker.js', 'text-editor.js']`, one "Detected duplicate Media files in an opposite order" warning |
| base + Luna's P0 (`evidence/ogi013-lead/phase3/L_luna/patch.diff`) | ISSUE_BEHAVIOUR_FIXED: merged order `['text-editor.js', 'text-editor-extras.js', 'color-picker.js']`, no warning |

Label: "A-11019: P0 is issue-correct; hidden-test defect not derivable from materials". P0 passes 3/16 F2P and 58/58 P2P under evaluator v2.1; the issue example is fixed, so the remaining 13 hidden failures are not explained by the issue text or the visible tests.
