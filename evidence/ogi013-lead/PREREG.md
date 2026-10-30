# OGI-013 PREREG (team driver) — written 2026-10-30, completed with the driver commit and sha256 at the G-dev freeze

## Claim boundary (Addendum 5 section D, verbatim in substance)
- The study measures task performance, as resolved instances under official hidden tests, and attributes changes to specific organisational interventions.
- It does not measure intelligence of any model or of the organisation; no result may be described that way.
- A positive result supports only: on these task families, under these conditions, the organised team resolved more tasks than the same models without organisation (N), than its member alone (S), and/or than Luna (L), and these named interventions caused these measured corrections.
- A claim beyond one task family needs a consistent effect on two independent families: SWE-bench Verified and Terminal-Bench 2.1.

## Recorded interpretations and tooling decisions
1. Progress guard (Addenda 3 F, 5 B, FIX below): per-role quality definitions; read-only roles: 12 distinct read/search calls; verdict delivered ends the session.
2. `run_python` tool added to the coding driver because Addendum 5 refers to it: bwrap (read-only host, no network, workspace-only write), plus an audit hook limiting `open()` to the workspace, interpreter and system libraries and blocking process creation (except `git`). Identical for every arm. Not a hard jail.
3. A candidate's author lineage does not vote on its own candidate (Addendum 6 section 4 versus B.4); unanimity = every other role-holder; the author's endorsement is its submission.
4. Tolerant action parser (`parse_code_action`): format tolerance only (execution defect: valid intent rejected as BAD_ACTION). Identical for every arm.
5. `NO_ELIGIBLE_NEURON` is waited out (10 x 60 s per step, logged `SUPPLY_WAIT`, not a turn); infrastructure failures are not evidence about the work.
6. Withdrawal evidence: a reason of >= 20 characters sharing an identifier (>= 6 chars) with the output of a check the voter executed after the objection was raised.
7. Development task: smallest `sha256("OGI013-DEV-1|"+instance_id)` among SWE-bench Lite django/django excluding `django__django-11019` and the 50-instance Verified sample (`django__django-14855`; the exclusion against the not-yet-drawn Verified sample is checked when it is drawn). Its outcome is never reported as a result; hidden grades of it are used only for the guard audit and tool checks.

## A-11019 label (Addendum 4 section B.2, exact)
"A-11019: P0 is issue-correct; hidden-test defect not derivable from materials". Kept together with: case series, descriptive only.

## Experiment A on Verified: critique validity (lead decision 2026-10-30)
`ISSUES: FOUND` is a valid critique only if it cites an executed check (run_tests / run_python output) or a `file:line` it read, and is not caused by the critic's own tool errors. Otherwise `INVALID_CRITIQUE`, kept in the table; the branch then counts as "no valid critique". A missing verdict line is `INVALID_CRITIQUE`. Valid and invalid critiques are reported per branch (LSR vs LBR): critique quality per lineage is part of the H1 result.

## FIX: commits after the freeze rule
| commit | defect | rerun scope |
|---|---|---|
| (see RESULTS.md) | dev06: all authors stopped after 9 exploration turns; author-type roles now get the 12-read exploration allowance until their first run_tests | G-dev restarted at episode 1 of 3 |
