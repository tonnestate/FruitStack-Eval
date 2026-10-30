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
| (see RESULTS.md, FIX 2) | gdev1: parser TypeError on non-string name; ledger event keyword clash | G-dev episode 1 rerun |
| (see RESULTS.md, FIX 1) | dev06: all authors stopped after 9 exploration turns; author-type roles now get the 12-read exploration allowance until their first run_tests | G-dev restarted at episode 1 of 3 |

## Pre-registered design (fixed 2026-10-30, before any scored run; changes only by a dated erratum that does not touch H, endpoints, n, selection or thresholds)

Hypotheses
- H1 (Experiment A): from the same failed Luna P0, revision after a VALID independent-lineage critique (LBR) rescues more often than after Luna's own critique (LSR).
  Unit: (instance, replicate). Endpoint: rescue = hidden-test resolved after revision while P0 not resolved. Test: exact two-sided McNemar on discordant LBR/LSR pairs, alpha 0.05.
  Secondary: partial improvement (F2P up, P2P not worse), harm, valid vs INVALID_CRITIQUE counts per branch.
- H2 (Experiment B): team T resolves more instances than the same supply without organisation N. Unit: instance. Exact McNemar T vs N. Secondary: T vs S (McNemar), T vs L (descriptive, Wilson 95% CI).
- H3 (mechanism): >= 1 COMPLETE C1-C4 chain occurs per gate window (definitions: Addendum 6 section 3, Addendum 7, Addendum 8).
- H4 (cost): additional tokens and calls per additional resolved instance (T-N, T-S); tokens per complete chain. Descriptive.

Samples
- Verified pool: princeton-nlp/SWE-bench_Verified, test split, dataset revision recorded at draw time.
  Order: ascending sha256("OGI013-SWEV-1|" + instance_id). Exclusions applied BEFORE taking positions:
  django__django-14855 (development task), django__django-11019, and any instance whose gold patch fails the official harness (HARNESS_INVALID).
  Sample = first 50 after exclusions. Positions 1-5 = window W5, 1-15 = window W15. Commit the list and its sha256 when drawn, before any run on it.
- Terminal-Bench 2.1: Harbor dataset terminal-bench/terminal-bench-2-1, order ascending sha256("OGI013-TB21-1|" + task_id), first 20.
- Development task: django__django-14855 (SWE-bench Lite), never reported as a result.

Sequence and gates (owner decision "cheapest evidence first", 2026-10-30)
1. G-dev: <= 3 episodes after FIX 1. PASS requires all Addendum 3 C items, Addendum 6 section 4 diversity, Addendum 5 C guard audit (wasted tail <= 40%),
   AND >= 1 COMPLETE C1-C4 chain in at least one episode. FAIL -> stop the study after REPORT 1 (finding: no verified correction by the organisation under current supply).
2. W5: T, N, L on positions 1-5, K = 1. CONTINUE iff >= 1 COMPLETE chain in T AND T resolved >= N resolved on W5. Else stop after REPORT 2.
3. W15: T, N, S, L on positions 6-15, K = 1 (W5 results are reused; S added on 1-15). Experiment A on Luna-failed instances within W15, K = 2.
   CONTINUE to the full program iff the McNemar T vs N on W15 has more T-only than N-only resolutions AND >= 3 COMPLETE chains on W15. Else write FINAL.md from existing data.
4. Full program (only after a positive W15): L on positions 16-50; Terminal-Bench 2.1 (20 tasks, L and T, 1 run each); 11019 closure (T, N, S once each); FINAL.md.

Stop conditions in any step: a circuit breaker hit twice -> stop that step and report it as a defect. A stop is a reported result.

Fixed per-arm resources: loop guards per Addenda 5 and 7 and FIX 1; circuit breaker 3,000,000 tokens / 1,500 requests / 4 h per episode; identical for T, N and S.
N's session count: fixed per instance so that N's tokens are within +-10% of T's tokens on that instance; measured from T first.
