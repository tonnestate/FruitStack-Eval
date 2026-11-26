# Synthesis SYN-54efe8c595e9

## synthesis_id

SYN-54efe8c595e9

## original_ids

["Q-0332cb0a65:S0067"]

## mathematical_domain

binary matroids; GF(2) linear systems

## title

Occurrence-level port for singletons and same-linear-part bundles

## mathematical_statement

GF(2), occurrences each a single equation or a bundle of equations sharing one linear part. Bundles with equal right-hand sides are replaced by w = (a, b); bundles with differing right-hand sides by w = e. The occurrence-level MUS clutter of the system equals the port at e of the binary matroid on {w_i} plus e. Mixed linear parts are not covered.

## formula_latex



## assumptions

["each occurrence is a singleton or a bundle sharing one linear part"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: Lemma T as stated in the lemma field: GF(2), occurrences = singletons or same-linear-part bundles; occurrence-level MUS clutter = port at e of the binary matroid on {w_i} plus e. Closes nothing; bookkeeping restriction. Does not touch G0001 (shared or mixed linear-part auxiliaries).
evidence: cm-1a2cb3072f61489b (replication, different method); cm-a05bfd5b43a54320 and cm-e9df3daa2c3a4895 (counterexamples in the mixed class).
lemma: Lemma T (GF(2), restricted class, bookkeeping; closes no obligation). Occurrences are single equations a.x=b or bundles of equations sharing one linear part a. A bundle with all right-hand sides equal to b has the solution set of a.x=b and is replaced by w=(a,b); a bundle with differing right-hand sides has empty solution set and is replaced by w=e=(0,...,0,1). Claim: the occurrence-level MUS clutter of the system equals the port at e of the binary matroid on {w_i} plus e. Proof: by Lemma S (GF(2) Fredholm), a family of occurrences is inconsistent iff some T has sum of a-parts 0 and sum of b-parts 1, iff e lies in the span of the chosen w_i. Consistency depends only on the w_i, so minimal inconsistent occurrence sets are the minimal sets S with e in span(w_S), which are the circuits through e minus e. Scope: GF(2), any n, each occurrence a singleton or same-linear-part bundle; mixed linear parts NOT covered. Evidence: cm-1a2cb3072f61489b (singletons n=3 m=3 exhaustive 4096 systems, 0 fails; random n=4 m=2..5, 3200 systems, 0 fails; same-linear-part bundles n=3 m<=4, 3000 samples, 0 fails). This is a replication by a different method, not a proof of the general statement.
gap: Open: occurrences with two or more distinct linear parts (the cm-e9df3daa2c3a4895 and cm-a05bfd5b43a54320 failures, 4068/19994 at m=4). G0001 unchanged.

## reconstructed_proof

[{"statement": "A bundle reduces to one vector w_i.", "justification": "a bundle with equal right-hand sides has the solution set of a·x=b; differing right-hand sides give empty solutions", "passage": "A bundle with all right-hand sides equal to b has the solution set of a.x=b and is replaced by w=(a,b)"}, {"statement": "Inconsistency is equivalent to e in span(w_S).", "justification": "Lemma S (GF(2) Fredholm)", "passage": "by Lemma S (GF(2) Fredholm), a family of occurrences is inconsistent iff some T has sum of a-parts 0 and sum of b-parts 1"}, {"statement": "Minimal inconsistent sets are circuits through e minus e.", "justification": "minimal span sets", "passage": "which are the circuits through e minus e"}]

## required_theorems

[]

## established_dependencies

[]

## missing_dependencies

[{"needs_validation": "Mixed linear parts are open (G0001 unchanged); numerical support is a replication, not a proof of the general statement."}]

## required_transfers

[]

## established_transfers

[]

## alternative_derivations

[]

## existing_validations

[{"validation_id": "PS:Q-0332cb0a65#89", "node_id": "Q-0332cb0a65:S0067", "reviewer": "pnp-desk/research/R1963", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-0332cb0a65#89", "node_id": "Q-0332cb0a65:S0067", "reviewer": "pnp-desk/research/R1963", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[{"needs_validation": "Mixed linear parts are open (G0001 unchanged); numerical support is a replication, not a proof of the general statement."}]

## required_recomputations

[]

## counterexamples

[{"role": "COUNTEREXAMPLE", "necessary_for_inference": false, "what": "counterexamples in the mixed-linear-part class", "inputs": "m=4", "result": "4068/19994 failures at m=4", "verification_conditions": null, "reproducibility": "cm-a05bfd5b43a54320; cm-e9df3daa2c3a4895", "passage": "cm-a05bfd5b43a54320 and cm-e9df3daa2c3a4895 (counterexamples in the mixed class)"}]

## first_invalid_inference



## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The text states it closes nothing, is a bookkeeping restriction, and does not touch G0001.

## source_references

{"question_id": "Q-0332cb0a65", "session": "pnp-desk/research/R1771", "origin_event_ids": ["a6085f964e2cb8443f411ff261696f9429246a657872addcc1e246dd0cf733b5"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

supply the missing arguments/dependencies, then re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
