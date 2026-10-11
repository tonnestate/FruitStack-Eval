# Pilot procedure (FRUITSTACK-EVAL-001, phase 2 and 3)

Version PILOT-PROC/1, written 11 October 2026, before any pilot data exist. It fixes how the 50-task inquiry pilot of protocol v0.2 (§5.4) is run, graded and analyzed. A change after the first pilot run needs a new version and a note in the gate report.

## Preconditions

1. Gates G1 to G5 pass (protocol §5.5). `fse integrity`, `fse independence`, the G3 probe and `fse logcheck` report no blocker on host evidence.
2. The owner has reviewed and approved the 50 references. The approved task file is registered with `fse tasks commit` and the manifest is committed to this repository before the first pilot call. The salts stay with the owner.
3. Arm A runs only after the owner has approved its actual cost. Without arm A, the result is reported as a pilot of F1 and F3, not as the completed pre-registered pilot.

## Task set

50 inquiry tasks in schema FSE-INQUIRY/1. Five subfamilies of ten: TECH, LAW and SCI (TRAIN split), HIST and ORG (HELDOUT split). Each subfamily has five SUPPORTED and five REFUTED claims. Each task asks for a verdict and one key value; the reference names at least one primary source.

## Arms

| Arm | Run | Fixed settings |
| --- | --- | --- |
| F1 | `runners/pilot_inquiry.py --arm F1 --offer <id>` | One PINNED call per task, `REASONING` role, 1024 output tokens. The offer is `best_single_offer` from `fse independence` on the G2 calibration (rule F1-RULE/1: highest calibration accuracy among qualified groups; ties go to more executed calls, then the group name). Pilot tasks are never used to pick it. |
| F3 | `runners/pilot_inquiry.py --arm F3 --cherryme-skill <ACE skill dir> --composer-offer <F1 offer>` | CherryMe with the ACE skill, its persistent workspace and the AppleMe assurance tier; question budget 8, provider-call cap 24 per task; no salvager (not part of F3 in §5). VERDICT comes from CherryMe's claim status: SUPPORTED and REFUTED map to themselves, UNKNOWN and CONFLICT to NOT_ENOUGH_INFO. KEY is extracted from CherryMe's own evidence by one composer call on the F1 offer. A key that does not occur in that evidence (same date, same number or same text) becomes UNKNOWN. This strict reading is the primary analysis. |
| A | separate approved run | One paid frontier model, same prompt and tools as F1. Its model must not belong to the family that drafted the references (Claude), to keep the grading reference free of a home advantage. |

Every free arm runs under `PLUMME_COST_POLICY=FREE_ONLY`; both runners refuse to start otherwise. Tasks run in file order. Each arm gets its own PlumMe state directory, so each arm's DecisionLog is complete and separate.

## What is recorded per task and arm

`results-<ARM>.jsonl`: the arm's final output, `status` (COMPLETED or FAILED), `quota_units`, `cost_eur`, `wall_seconds` and diagnostics. For F3 the diagnostics include CherryMe's claim status, evidence count, questions asked, provider calls and the composer's key and grounding flag. In the pilot, `quota_units` counts provider-facing PlumMe decisions (ACQUIRE and FALLBACK, successful or not); ENSEMBLE records are not counted. Normalization by each provider's free allowance is fixed for the confirmatory round.

## Grading

`fse inquiry grade` grades every answer deterministically (FSE-INQUIRY/1): 1 if verdict and key are right, 0.5 if exactly one is, 0 otherwise. The grader never sees the arm. The report counts, per arm, successes (grade 1), failures (graded below 1), unverifiable tasks (no admissible label), missing answers, unparseable answers and abstentions separately.

Blind audit: `fse blind export --sample 0.2` gives the owner (or a second person) a shuffled, arm-free, name-redacted sample of whole tasks. Its manifest is committed before grading starts. `fse blind ingest --deterministic` reports the agreement with the deterministic grader. A task whose reference turns out to be wrong is voided in this blind step and removed from every arm.

## Analysis (phase 3, descriptive only)

`fse pilot analyze` on the graded rows reports, per arm, labelled tasks, successes, failures, unverifiable tasks, mean utility, utility per quota unit and utility variance. Per pair (other arm minus F1), on paired tasks: success-rate difference, mean utility difference, discordance psi and the concordance table, with a subfamily-cluster bootstrap (task bootstrap below five subfamilies, seed 20261011, 2000 resamples). No p-values and no verdicts are reported.

H4 compares F4 with arm A. F4 does not exist before a learned policy is promoted, so the pilot uses F3 against A as its stand-in. Without arm A, psi for H4 cannot be estimated, and the F3 against F1 estimates inform only the planning of H1. From the relevant psi the module proposes paired sample sizes for the non-inferiority test at the margins of 10 and 5 percentage points (one-sided alpha 0.025, power 0.80), for the psi estimate and its upper interval bound. The upper bound is the recommended basis. Margins, psi and sample sizes become binding only when the owner freezes and deposits them (G7).

## Sealing

After each arm: `fse seal create` over the arm's DecisionLog, its results file and the intervention log, then `fse logcheck --expect-cost-policy FREE_ONLY`. Commit the seal, the results, the graded rows and the run metadata to this repository.
