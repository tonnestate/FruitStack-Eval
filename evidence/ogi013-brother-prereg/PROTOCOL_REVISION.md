# OGI-013 Brother Mode prospective protocol revision

Status: **DRAFT — NOT LOCKED — NOT RESEARCH_READY — DO NOT RUN**

This revision adds a queue condition for the integrated Brother Mode. It does not
amend or reinterpret historical OGI-012, COLLAB-1, c1, c2, c3, QA-2D, or pilot
results. Existing study locks and task/result records remain unchanged. In
particular, earlier c3 activity is excluded from this prospective comparison.

## Executable arm mapping

| Prospective arm | Queue condition | Runner mode | Collaboration behavior |
|---|---|---|---|
| SINGLE | `SINGLE` | `single` | No organization |
| SINGLE-E | `SINGLE-E` | `single_e` | Independent extra drafts; no critique or revision |
| FIXED | `FIXED` | `fixed` | Always-on peer review |
| ADAPTIVE | `BROTHER` | `rg2` | `OGI013_ORG_COLLAB=1`; Brother controller and EVC path |

`BROTHER` is a new condition name so historical `RG2-OFF` retains its old
meaning. The shared queue clears `OGI013_ORG_COLLAB` before every condition;
only `BROTHER` sets it. The runner's integrated-runtime tests separately verify
that this flag selects `collaborate()` and that its valid controller decision
determines the actual action.

## Locking required before any experiment

Before execution, a new immutable preregistration must specify and hash the
benchmark/package revision, disjoint calibration and held-out task lists, all
four arm configurations and component commits, resource ceilings, official
independent evaluator and its version, primary endpoint, paired statistical
analysis, exclusions, failure handling, and stop conditions. The selected
tasks must exclude previous OGI-013 exposures. No provider or benchmark run is
authorized by this draft.

Primary endpoint remains independently verified task success. Calls, tokens,
cost/quota dimensions, runtime, human intervention, beneficial corrections,
harmful corrections, and verified transfer are secondary measures. The study
must report all arms, incomplete tasks, and uncertainty; no success or
organizational benefit is inferred from this queue wiring or its offline tests.

## Current readiness

The arm routing has deterministic offline coverage through
`tests/test_ogi013_block_queue.py::test_research_arms_share_one_offline_queue_block`
and through the actual `FruitStackTau2Agent` collaboration path. The existing
pair exporter and confirmatory analyzer also pass all six pairwise combinations
of the four named arms in
`tests/test_ogi013_export_pair.py::test_four_arm_design_exports_each_pair_for_confirmatory_analysis`.
These synthetic fixtures verify analysis plumbing, not benchmark outcomes,
resource metering, or grader independence. The queue test uses a synthetic
launcher and placeholder results; it verifies dispatch and completion
plumbing. The study is **not RESEARCH_READY**: no new protocol lock, clean
held-out split, approved resource envelope, or host/provider execution
verification exists.
