# Synthesis SYN-fbf296a674a2

## synthesis_id

SYN-fbf296a674a2

## original_ids

["Q-156fa9c912:S0513"]

## mathematical_domain

formal languages / streaming complexity

## title

Residual left-quotient update for a finite word set

## mathematical_statement

Let A be any finite set of Boolean strings of common length N. For each prefix p of length t<=N let R_p={z in A: p is a prefix of z}. If t<N and b in {0,1}, then R_{pb}={z in R_p: z[t]=b}. Consequently the empty residual stays empty after every further input bit, and R_p is nonempty iff p is a prefix of at least one member of A.

## formula_latex

R_{pb}=\{z \in R_p : z[t]=b\}

## assumptions

["A is finite with all members of common length N"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: LEMMA (residual left-quotient update). Let A be any finite set of Boolean strings of common length N. For each prefix p of length t≤N define R_p={z∈A:p is a prefix of z}. If t<N and b∈{0,1}, then R_{pb}={z∈R_p:z[t]=b}. Consequently the empty residual remains empty after every further input bit, and R_p≠∅ iff p is a prefix of at least one member of A. Proof: for every z∈A, pb is a prefix of z exactly when p is a prefix of z and its t-th bit is b. This is exactly membership in the right-hand set. The two consequences follow from subset inclusion and the definition of R_p.

## reconstructed_proof

[{"statement": "pb is a prefix of z iff p is a prefix of z and z's t-th bit is b", "justification": "prefix characterisation", "passage": "pb is a prefix of z exactly when p is a prefix of z and its t-th bit is b."}, {"statement": "the two consequences follow from subset inclusion and the definition of R_p", "justification": "subset inclusion", "passage": "The two consequences follow from subset inclusion and the definition of R_p."}]

## required_theorems

[]

## established_dependencies

[]

## missing_dependencies

[]

## required_transfers

[]

## established_transfers

[]

## alternative_derivations

[]

## existing_validations

[{"validation_id": "PS:Q-156fa9c912#623", "node_id": "Q-156fa9c912:S0513", "reviewer": "pnp-desk/research/R2684", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-156fa9c912#623", "node_id": "Q-156fa9c912:S0513", "reviewer": "pnp-desk/research/R2684", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[]

## required_recomputations

[]

## counterexamples

[]

## first_invalid_inference



## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The record states a self-standing identity about finite word sets and no route role for the target.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2500", "origin_event_ids": ["c0a2f75291079857bc77c39d15ec048b7878c82cce0e1a11cbe950ab7a469c28"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

independent re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
