# Synthesis SYN-d5e6fc9a2f15

## synthesis_id

SYN-d5e6fc9a2f15

## original_ids

["Q-156fa9c912:S0518"]

## mathematical_domain

formal languages / streaming complexity

## title

Prefix-residual state-count bound

## mathematical_statement

Let A be a finite nonempty subset of {0,1}^N with |A|=M and L=Pref(A). For each depth k in 0..N, a nonempty right residual arises only from a length-k prefix of a word in A, so there are at most min(2^k, M) such residuals at depth k. Summing over depths (an overcount) and adding one empty residual, the minimal deterministic automaton for L has at most 1+sum_{k=0}^N min(2^k,M) states.

## formula_latex

|Q| \le 1 + \sum_{k=0}^{N} \min(2^k, M)

## assumptions

["A is finite and nonempty"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: LEMMA (prefix residual state-count bound). Let A be a finite nonempty subset of {0,1}^N with |A|=M, and let L=Pref(A). The minimal deterministic automaton for L has at most 1+sum_{k=0}^N min(2^k,M) states.
derivation: For each k in 0..N, a nonempty right residual L_p arises only from a length-k prefix p of some word in A. There are at most 2^k such prefixes. There are also at most M such prefixes because distinct length-k prefixes have disjoint sets of descendant words in A, each nonempty. Hence there are at most min(2^k,M) nonempty residuals arising at depth k. Summing these upper bounds over depths may overcount residuals shared across depths, which is harmless. There is at most one additional empty residual. By the right-residual characterization, the number of distinct residuals bounds the minimal automaton state count.

## reconstructed_proof

[{"statement": "nonempty residuals at depth k come from length-k prefixes, so at most 2^k", "justification": "prefix count", "passage": "a nonempty right residual L_p arises only from a length-k prefix p of some word in A"}, {"statement": "at most M distinct depth-k prefixes with nonempty disjoint descendant sets", "justification": "disjointness", "passage": "distinct length-k prefixes have disjoint sets of descendant words in A, each nonempty"}]

## required_theorems

[{"class": "EXPLICIT_INTERNAL_REFERENCE", "premise": "minimal automaton state count equals the number of distinct right residuals", "cited_id": "Q-156fa9c912:S0517", "external_ref": null, "target": "Q-156fa9c912:S0517", "target_validation": "SURVIVED_INDEPENDENT_REVIEW", "target_math_status": "CLAIMED"}]

## established_dependencies

[]

## missing_dependencies

[{"needs_validation": "the step relies on the right-residual characterization stated in the companion record; this makes the record not self-contained"}]

## required_transfers

[]

## established_transfers

[]

## alternative_derivations

[]

## existing_validations

[{"validation_id": "PS:Q-156fa9c912#628", "node_id": "Q-156fa9c912:S0518", "reviewer": "pnp-desk/research/R2788", "model": "minimax-m3.1-flash", "model_family": "minimax", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-156fa9c912#628", "node_id": "Q-156fa9c912:S0518", "reviewer": "pnp-desk/research/R2788", "model": "minimax-m3.1-flash", "model_family": "minimax", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[{"needs_validation": "the step relies on the right-residual characterization stated in the companion record; this makes the record not self-contained"}]

## required_recomputations

[]

## counterexamples

[]

## first_invalid_inference



## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The record applies the characterization of S0517 to bound state counts and states no route role.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2500", "origin_event_ids": ["12814a5c5b5c82a0caaf6ce9a7dc1d3abdf48b6c58f91bf8ce1304d95f374cf5"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

supply the missing arguments/dependencies, then re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
