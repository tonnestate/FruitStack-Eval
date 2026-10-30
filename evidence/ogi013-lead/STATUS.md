# OGI-013 STATUS (facts only; frozen by owner stop order, 2026-10-30)

Last driver commit before this record: `f7eeec4`. Verdict commit of the earlier study: `4d75a49` (no measured organisational effect; F did not outperform L).

## Episodes started since 4d75a49
| run | end state | why |
|---|---|---|
| Experiment A smoke (`smoke-discarded-prompt-env-defect`) | discarded | critic/reviser prompts lacked the interpreter note arm L received; LBR crashed on a wrong attribute |
| Experiment A main (K=5, LSR and LBR) | completed | 10/10 replicates ended with P0 unchanged |
| dev01 | killed by me | old driver, one model in all roles, 193 refused/abandoned steps |
| dev02 | killed by me | ran with the pre-Addendum-5 activity guard; 81 role handovers, 193 refused steps |
| dev03 | killed | stopped by an over-broad `pkill` shortly after start (my own shell was killed with it); superseded by Addendum 6 |
| dev04 | ended `RELEASED_NO_CONSENSUS` | `NO_ELIGIBLE_NEURON` in the challenge stage and a `FileExistsError` on a reused directory; second solver saw the first solver's diff (leak); identical patches |
| dev05 | ended `NO_PATCH` | 19 of 27 replies rejected as BAD_ACTION (format intolerance); all 3 author sessions stopped by the guard |
| dev06 | ended `NO_PATCH` | Addendum 5 guard stopped all 3 author sessions after 9 exploration turns, no test run |
| gdev1 (aborted pre-FIX-1) | killed by me | started before FIX 1; not counted |
| gdev1 (crash, FIX 2) | ended `NO_PATCH` | `TypeError: unhashable type: 'dict'` in the action parser and a keyword clash `kind` in the ledger event, both in the solve/helper path |
| gdev1 (run 3) | stopped by owner, not counted | running when the stop order arrived; 1 snapshot, 49 steps, no challenge/revision/vote yet |
No dev episode is reported as a result of the development task.

## Fix commits and the defect each fixed
- `142bfcc`, `438a1d4` AMENDMENT-DRIVER-2: sticky author sessions, syntax-guarded `edit_file`, latest `run_tests` visible; Experiment A prompt gaps.
- `37b897f`, `59ffff4`, `c8d742a` AMENDMENT-TEAM-1 development: team episode driver, loop guards, release vote.
- `63258b1` Addendum 5 quality-based progress guard, `run_python`.
- `004e0c9` SNAPSHOT/SESSION events, snapshot grader, guard audit script.
- `2fd2514` Addendum 6: ledger-checked vote grounding, chain and diversity audit.
- `b1d75c9` Addendum 7: objections closed only by verification (a revision closed every objection; an in-vote withdrawal needed no evidence); supply wait; unique work directories.
- `182b036` tolerant action parser (valid intent rejected as BAD_ACTION).
- `74e4771` Addendum 8: solver 2 saw solver 1's diff; solver stage ignored the lineage exclusion; helper independence; solver similarity.
- `31a590f` FIX 1: dev06 guard stopped all authors after 9 exploration turns (author exploration allowance until the first `run_tests`).
- `f7eeec4` FIX 2: parser TypeError on non-string names; ledger event keyword clash; WORK_ERROR traceback.
- `e046cc1`, `a1f9172` records: Experiment A-11019 table, PREREG, TASK_VALIDITY.

## Verified
- Calibrated evaluator v2.1 and the submit gate (earlier phase; unit tests in `tests/test_ogi013_coding_gate.py`).
- Vote grounding, objection lifecycle, chain linking, independent-solving prompts, progress guard, parser: unit tests pass (38 on the last full run).
- Experiment A-11019: 10/10 P0 unchanged; critique validity LSR 5/5 valid, LBR 0/5 valid (`RESULTS.md`).
- Issue behaviour of P0 (`TASK_VALIDITY.md`, `repro_issue_example.py`): fixed.

## Not verified
- No G-dev pass. No development episode has produced a gate-accepted patch that was challenged, revised, re-examined and voted on.
- No COMPLETE C1-C4 chain has been observed in any run.
- No team result of any kind. No T, N or S run on any scored task. No SWE-bench Verified or Terminal-Bench run (Docker and Harbor are not installed on the host).
- The 50-instance Verified sample has not been drawn.

## Record gaps (OGI013_PREREG_COMPLETION section C)
Closed in `a1f9172`: `TASK_VALIDITY.md` and `repro_issue_example.py`; issue-behaviour and critique-validity columns in the A-11019 table; Verified membership of 11019 and 14855 recorded (to be re-verified against the dataset when the sample is drawn).

## Restart rule (also in PREREG.md)
G-dev allows at most 3 episode STARTS in total, crashed or stopped episodes included. A 4th start requires an explicit owner decision.
Counting since FIX 1: 2 starts used (gdev1 crash, gdev1 run 3); the aborted pre-FIX-1 start is not counted. Under a stricter count that includes it, 3 are used.

## Update after the lead's decisions (2026-10-30)
- G-dev starts: strict reading, 3 of 3 used.
- Provenance: the MangoMe source the evaluations imported was a dirty working tree; the logged commit `98009461...` does not identify the code that ran for any run so far. Repair in `MANGOME_DIAGNOSIS.md` (D4).
