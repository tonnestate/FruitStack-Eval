"""FruitStack Code Mode + EVC (OGI-013 architecture decision, owner 2026-10-31).

Code Mode is the communication and execution technique, EVC the decision basis for further agent activation, CherryMe keeps domain control.
This package is the narrow, typed host-side layer (level D1): the HOST chains, filters, compares and verifies; models only answer or critique.
No model-written code is used as orchestration here. Model-written computations are only *evidence*, executed by the existing bubblewrap
sandbox (ogi013_argument) through an injected verifier.

Modules
  contract  typed, compact messages (result, evidence, conflict, verification, measured uncertainty, resources, next action, full-text reference)
  sieve     invariant-preserving compaction and keep / compact / drop per message (training-free, MessageSieve-style)
  facade    parallel independent calls, deterministic chaining, structural compare, deterministic verification, conflicts, provenance
  duo       the QA duo (two members, cross-critique) executed through the facade, with a pluggable activation policy
  evc       Expected Value of Computation: estimation from recorded runs, policy, offline replay, Pareto over a fixed lambda grid
  shapley   post-hoc marginal contribution of members and the critique link (never used to decide truth)

Status of everything in this package: IMPLEMENTED + OFFLINE_TESTED. HOST_VERIFIED and BENCHMARK_VERIFIED require the VPS runs."""
