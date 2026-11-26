# Synthesis SYN-f8bd0657b6c6

## synthesis_id

SYN-f8bd0657b6c6

## original_ids

["Q-156fa9c912:S0530"]

## mathematical_domain

formal languages / streaming complexity

## title

Residual-quotient width bound for finite families

## mathematical_statement

Let F be a finite family of K Boolean strings of common length N. At depth t, 0<=t<=N, partition all length-t prefixes by equality of their residual sets R(p)={z: pz in F}. The number of equivalence classes is at most min(2^t,K)+1. Nonempty residual classes are witnessed by length-t prefixes of members of F, giving at most min(2^t,K) nonempty classes, plus at most one class for empty residuals. The bound is a width bound in terms of |F| and does not bound transition circuit cost from a compact representation of F.

## formula_latex

\#classes_t \le \min(2^t, K) + 1

## assumptions

["F is finite with K strings of common length N"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: LEMMA (residual quotient width). Let F be a finite family of K Boolean strings of common length N. At depth t, 0<=t<=N, partition all length-t prefixes by equality of their residual sets R(p)={z: pz in F}. The number of equivalence classes is at most min(2^t,K)+1. Proof: Every nonempty residual class contains a prefix p occurring as the length-t prefix of at least one word in F. Distinct such prefixes number at most 2^t and at most K, so there are at most min(2^t,K) distinct nonempty residual sets. All prefixes with empty residual, if any, belong to a single additional class. Thus the total is at most min(2^t,K)+1. At t=0 the bound remains valid (there is only one prefix, and hence at most one class). Scope: finite equal-length string families; this is a width bound in terms of |F| and does not bound the transition circuit cost from a compact representation of F.

## reconstructed_proof

[{"statement": "each nonempty class contains a length-t prefix of some member of F", "justification": "definition of residual", "passage": "Every nonempty residual class contains a prefix p occurring as the length-t prefix of at least one word in F."}, {"statement": "distinct such prefixes give at most min(2^t,K) nonempty classes, plus one empty class", "justification": "counting", "passage": "Distinct such prefixes number at most 2^t and at most K, so there are at most min(2^t,K) distinct nonempty residual sets."}]

## required_theorems

[]

## established_dependencies

[]

## missing_dependencies

[{"needs_validation": "a width bound in |F|; no bound on the transition cost from a compact representation"}]

## required_transfers

[]

## established_transfers

[]

## alternative_derivations

[]

## existing_validations

[{"validation_id": "PS:Q-156fa9c912#658", "node_id": "Q-156fa9c912:S0530", "reviewer": "pnp-desk/research/R2844", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-156fa9c912#658", "node_id": "Q-156fa9c912:S0530", "reviewer": "pnp-desk/research/R2844", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[{"needs_validation": "a width bound in |F|; no bound on the transition cost from a compact representation"}]

## required_recomputations

[]

## counterexamples

[]

## first_invalid_inference



## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The record states a width bound with explicit scope limits and no route role.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2532", "origin_event_ids": ["fdfae2dfd02c19c7f6385a8b6cc7bd9c585278e7d9a1e37254a09a2bb569ec8f"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

supply the missing arguments/dependencies, then re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
