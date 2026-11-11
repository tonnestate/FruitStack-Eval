# HELP/2 — author–helper coordination (supersedes Addendum 3 B.3 help rules)

Status: IMPLEMENTED in `runners/ogi013_code_task.py` + `runners/ogi013_team_code.py` (branch `cc/fruitstack-recovery`), offline-tested, not live-validated, not deployed. Owner review required before any frozen protocol adopts it.

## Evidence (episode 5, django-11119, 2026-11-11)

- S2 author asked for help at turn 8 (`idle`). The helper ran **52 turns / 451,624 tokens (55 % of the episode)** on the author's thread; the author waited 7.5 min.
- The author then edited (04:25), its tests improved (04:27), and the **unconditional `half_budget` rule** (turn == nominal/2) interrupted it at 04:28 with a second helper. The episode budget ran out during the author's final edit: no patch.

## Rules replaced

| Addendum 3 B.3 (old) | Harm | HELP/2 |
|---|---|---|
| `half_budget`: request help at turn = nominal/2, whatever the author is doing | interrupts productive authors | removed; help only on a demonstrated stall: `zero_tests` (2 runs executing 0 tests), `edit_rejected` (2 rejected edits), `idle` (8 actions without edit/check) |
| helper runs synchronously inside the author's session | author blocked for the whole consult | helper runs on its own thread and forked session; the author keeps working; the answer is injected when ready |
| no bound on a consult except HARD_TURNS = 400 | one helper took 55 % of the episode | a consult may spend at most `HELP_TOKEN_SHARE` = 10 % of the episode tokens unspent when it starts; it is told to answer on its last affordable turn and stops at the share (`STOP:TOKEN_SHARE`) |
| every new stall condition triggers another consult | repeated consults without effect | a consult that is followed by no executed test or accepted submit within 5 turns (`HELP_GIVEN recovered=false`) ends help for that session |
| consult answer posted whenever it returns | late answer could change a finished collaboration | a consult still running when the author's session ends is cancelled; its answer is discarded and never posted |

Unchanged: the no-progress guard (NO_PROGRESS_TURNS = 8, GUARD-FIX cycle credit), helper lineage independence (Addendum 8 B.3), the helper's answer remains UNVERIFIED advice.

## Related defect fixed in the same change

`4e06e34` (2026-10-31) dropped the transcript line that records a model's own tool call. Since then every coding session saw tool RESULTS without the calls that produced them (which file, which edit, whether tests ran), and `render()` no longer kept the latest test output in full. Restored; regression test `test_the_model_sees_its_own_previous_calls`.

## Proposed, NOT implemented (owner decision)

Release vote: any `APPROVE: ACCEPTABLE` is filed as an objection and forces revise + challenge cycles until `VOTE_NO_SHRINK_3` (up to 4 cycles), and the voter's next `OWN_OBJECTIONS: NONE` is then ruled ungrounded because the ledger holds its own vote-objection. Observed offline: 8 votes, 4 cycles, release `CANDIDATE_NO_CONSENSUS` for a correct, test-passing patch. Proposal VOTE/2: release on unanimous APPROVE (EXCELLENT or ACCEPTABLE) with no open GROUNDED objection; an ACCEPTABLE vote's remarks are recorded as suggestions, not objections.

## Checks

`tests/test_fruitstack_artifact_delivery.py` (productive author never interrupted; author works while the helper runs and a late answer changes nothing; no repeat after unproductive help; token share; own calls visible; guard unchanged; exploring author delivers) and `tests/test_fruitstack_team_e2e.py` (real launcher + stack + Django tests + grader, scripted transport only: accepted, graded patch, 16 calls, 24,958 tokens).
