# COLLAB-1 — SINGLE-E effort calibration (fixed before any study episode)

## The mismatch that is corrected
The registered C3 SINGLE-E draws `k` independent drafts at **every agent turn** (`OGI013_SINGLE_E_K`), while C3 takes `k` from the median provider dispatches of organisation decisions (`supervisor.sh` stage_freeze over RG2-RANDOMIZED training rows). That is
requests per *organisation decision* turned into drafts per *turn* — in a conversation with ~10–15 turns it spends an order of magnitude more than the organisation does, and it is only known after the COLLAB-like arm has run.
COLLAB reviews only consequential decisions (a write or a transfer; the economy gate skips reads and plain messages: `ORG_SKIPPED simple_task` in PILOT-4). Equal effort therefore has to be matched **per consequential decision**.

## Definition (registered for COLLAB-1; the C3 behaviour is unchanged: `OGI013_SINGLE_E_SCOPE` defaults to `all`)
SINGLE-E (`OGI013_SINGLE_E_SCOPE=writes`, `OGI013_SINGLE_E_K=3`): when the first draft of a turn is a write or a transfer, two more independent drafts of the same prompt are drawn from the same supply and the majority canonical action wins (registered tie rule:
earliest draft); every other turn is a single draft. No critique, revision or organisation.

## Calibration data and why k = 3 (no confirmatory outcome used)
Effort of the COLLAB mechanism per consequential decision, in provider requests (recorded receipts, `provider_attempt_count`):
| case | requests per decision | source |
|---|---|---|
| draft, one critique, no issue found | 2 | structure of the mechanism (draft + critique) |
| draft, critique, revision, re-review (issue found) | 4 | PILOT-4 review 1 (`calls` = 3 review requests + the draft); the only real-provider observation |
| specialist added | ≥ 5 | structure; not observed |
The only recorded real decision costs 4; the structural minimum is 2; the share of decisions with an issue is UNKNOWN (n = 1). Without that share the unbiased registered choice is the midpoint **k = 3 requests per consequential decision**. A larger k would favour the control and make a COLLAB advantage harder to show,
a smaller k the opposite; the midpoint is a declared compromise, not an estimate, and **realised effort is therefore part of the analysis, not an assumption**: the report gives COLLAB − SINGLE-E differences in actual provider requests and tokens per episode (paired, bootstrap CI) and a pre-specified
effort-matched sensitivity (E2 on the pairs where COLLAB requests ≤ 1.25 × SINGLE-E requests). Worker-count equality is never taken to mean equal resources.

## Order
`study_manifest_v2.json` assigns each task one of the six permutations of {SINGLE, COLLAB, SINGLE-E} by cycling over the tasks ranked by the seeded hash: each condition is first and last in 16 of 48 blocks (verified in `tests/test_ogi013_collab1_campaign.py`'s manifest check). SINGLE-E is no longer run last.
Within a block all three conditions share one simulator model (chosen once by PlumMe, route file reused) and start from clones of the same frozen ledger snapshot.
