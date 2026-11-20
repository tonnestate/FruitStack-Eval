# FruitStack RH Research 1.2 — isolated first runtime

This directory is an experimental research workspace. It does not change CherryMe,
PlumMe, MangoMe, DuckDB production state, or any live service.

## Current runnable slice

`fruitstack_rh.py` creates a DuckDB research graph with versioned statement records,
multi-premise inference records, and a hash-linked event journal. The initial seed
records the RH target and open obligations for function-field transfer, the two
Connes–Consani–Moscovici steps, de Bruijn–Newman, RH formalization, and certified
off-line zero search. It stores `WORKS_TOWARD` research leads separately from logical
inferences; these leads do not establish implication. It does not implement Lean
verification or a proof engine.

`real_interval_is_off_critical_line(left, right)` checks exact rational real-part
bounds for a proposed rectangle. It only checks that the box lies in the open
critical strip and excludes `Re(s)=1/2`; it does not evaluate ζ, isolate a zero,
or certify a counterexample.

`exact_polynomial_zero_certificate(coefficients, real, imag)` uses rational
Gaussian arithmetic to verify an exact root of a supplied polynomial at a
point off the critical line. This is a test-function calibration only; it does
not verify zeros of ζ or RH.

`certify_test_function_zero(...)` additionally checks that the exact rational
root lies strictly inside a supplied off-line rectangle and returns a typed
`TEST_FUNCTION_ONLY` record. It is an in-memory calibration result, not a
persisted verifier receipt and not evidence about ζ.

`certify_rouche_polynomial_disk(...)` checks an exact rational Rouché bound for
a polynomial expressed in powers of `z-center`. It certifies the polynomial's
zero count with multiplicity inside a disk wholly off the critical line; it
does not identify distinct roots or say anything about ζ. The experiment
artifact includes a known test-function calibration. `verify_rouche_polynomial_certificate(...)`
independently parses its exact rational data and checks the disk, strict Rouché
bound, and claimed count without calling the certificate producer; experiment
replay uses this check before comparing the frozen artifact.
`record_test_function_rouche_receipt(...)` stores a DuckDB-bound calibration;
`report` checks it with the independent verifier and matches its inputs to the
materialized row and event journal. Creation/link events whose exact backing
row is absent are listed in `orphan_events`; a receipt event also remains
visible in the receipt projection as `ORPHAN_EVENT`. These are replayable
consistency checks for that supplied polynomial only, not authenticated
provenance or ζ/RH evidence.

`run-experiment` executes three frozen, equal-budget permutations of the same tiny
exact-polynomial corpus and can write a deterministic JSON artifact without
overwriting an existing file. The perturbed and shuffled arms are synthetic
priority-order calibration (two candidates are checked per arm), not learned or neural model weights. The harness does
not implement SHAP, evaluate ζ, isolate polynomial roots, or provide RH evidence;
its purpose is to check experiment replay, budget accounting, and the
test-function certificate boundary. `verify-experiment --input FILE` replays the
frozen protocol and checks every field against the recomputed result; it reports
`REPLAY_MISMATCH` for modified artifacts and rejects duplicate JSON keys.

`ml_discovery.py` provides a synthetic pairwise-ranking calibration with
reproducible feature/score perturbations. Its local linear contributions are not
SHAP and it does not use mathematical or RH data. `lean_adapter.py` can invoke a
version-pinned Lean executable on a digest-bound source snapshot. Its strongest
success status is `COMPILED_ONLY`: it does not check a named theorem, transitive
axioms, Mathlib semantics, or RH, so it cannot produce a proof receipt.

```sh
python3 fruitstack_rh.py self-check
python3 -m pytest -q tests
python3 fruitstack_rh.py seed --db state/research.duckdb
python3 fruitstack_rh.py report --db state/research.duckdb
python3 fruitstack_rh.py run-experiment --output /tmp/toy-calibration.json
python3 fruitstack_rh.py verify-experiment --input /tmp/toy-calibration.json
python3 fruitstack_rh.py add-zero-candidate --db state/research.duckdb \
  --candidate-id CANDIDATE-1 --real-left 2/3 --real-right 3/4 \
  --imag-lower 10 --imag-upper 11 --artifact candidate.txt
```

`report` returns verified RH claims, formal inference edges, separate research leads,
sources, per-statement materialized-row integrity (`MATCH`, `LEGACY_PARTIAL`,
`MISMATCH`, or `UNJOURNALED`), orphaned creation/link events, and whether the
event hash chain is internally consistent. The chain has no external head
anchor, so deleting a trailing event suffix cannot be detected.
Kernel-accepted and semantically-reviewed statuses are suppressed to `OPEN` because
no independent receipt workflow exists. Statement/event mismatches also suppress the
displayed status. Inference conclusion, premises, rule, status, and proof reference
are checked against creation events, and
`LINK_PROVED` is never reported without a receipt. Historical events that omit fields are reported as `LEGACY_PARTIAL`; they
are never rewritten or treated as full receipts. `journal_valid` checks hash-chain
consistency only; it is not a signature or tamper-proof authority.
Source and research-lead statuses are checked against their registration/creation
events; mismatches are downgraded to `SOURCE_UNVERIFIED` or `RESEARCH_LEAD` and marked
with an integrity field. Semantic-review references are emitted only when bound to an
intact, matching statement event. It also reports kernel-acceptance and semantic-review references separately;
`verified_rh_claims` stays empty until an independent receipt workflow exists.
Zero-candidate records are checked against their creation event and report
`record_integrity`; artifacts are SHA-256 checked on each report. Their displayed
status is always `CANDIDATE_ONLY` until a separate certification workflow exists. They remain
`CANDIDATE_ONLY`: an event and artifact digest do not certify a zero or a ζ computation.

DuckDB is an existing Python installation dependency in the current workspace.
The research database is generated locally and is not committed as source data.

## Evidence boundary

`LINK_HYPOTHESIS` and open claims remain unverified. This CLI explicitly rejects
direct `LINK_PROVED` and kernel-accepted status promotion. A successful database
self-check establishes only these local data invariants, not any mathematical claim.
The pytest suite exercises seed idempotence, explicit multi-premise storage, refusal
to promote unverified inferences/statements, detection of event-payload tampering,
and exact rational real-interval geometry. It does not exercise a Lean kernel or any
RH proof/refutation workflow.

`contract_test_status.json` maps T-001 through T-080 to the current
`NOT_RUN` or `NOT_IMPLEMENTED` state. Related pytest coverage is context only
and does not count as execution of a contract test.

See `/root/contracts/FRUITSTACK-RH-RESEARCH-1.2-FIRST-PASS-2026-11-07.md` for the
initial literature map and the exact unverified scope.
