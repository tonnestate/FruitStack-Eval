# Synthesis SYN-421a3bf220bb

## synthesis_id

SYN-421a3bf220bb

## original_ids

["Q-156fa9c912:S0521"]

## mathematical_domain

streaming complexity

## title

Candidate-bitset streaming implementation with index counter

## mathematical_statement

Let A=(C_1,...,C_M) be an explicitly listed finite family of Boolean circuits on n inputs, each with at most s fan-in-two gates, and N=2^n. Stream the truth-table bits in binary input order. There is a deterministic one-pass implementation using M+ceil(log2 N) state bits and at most O(M(s+1)+log N) fan-in-two gates per update that accepts exactly prefixes extendible to a truth table in {Eval(C_i): 1<=i<=M}. Initially j=0 and all v_i=1; on input b with j<N, set v'_i=v_i AND [C_i(x_j)=b] and increment j. It is an exponential-in-description-count bound when A lists all size-s circuits and implies no polynomial update cost.

## formula_latex

O(M(s+1)+\log N)\ \text{gates per update}

## assumptions

["the family is explicitly listed", "stream order is the fixed binary truth-table order"]

## proof_status

CLAIMED

## validation_status

REFUTED_BY_DEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: LEMMA (candidate-bitset streaming upper bound). Let A=(C_1,...,C_M) be an explicitly listed finite family of Boolean circuits on n inputs, each with at most s fan-in-two gates, and let N=2^n. Stream the truth-table bits in binary input order. There is a deterministic one-pass implementation using M+ceil(log2 N) state bits and at most O(M(s+1)+log N) fan-in-two gates per update that accepts exactly prefixes extendible to a truth table in {Eval(C_i):1<=i<=M}. State: an index j in {0,...,N} and a bit vector v in {0,1}^M. Initially j=0 and v_i=1 for every i. On input b while j<N, set v'_i=v_i AND [C_i(x_j)=b] for each i and increment j, where x_j is the jth input in the fixed truth-table order. Each circuit evaluation costs O(s+1); the equality test and conjunction cost O(1) per candidate, and the counter increment costs O(log N). By induction on the number of streamed bits, v_i=1 exactly when Eval(C_i) agrees with the entire prefix read so far. Thus some completion exists exactly when some v_i=1. This is an explicit exponential-in-description-count upper bound when A lists all size-s circuits; it does not imply polynomial update cost.

## reconstructed_proof

[{"statement": "on input b, v'_i = v_i AND [C_i(x_j)=b] and j is incremented", "justification": "update rule", "passage": "On input b while j<N, set v'_i=v_i AND [C_i(x_j)=b] for each i and increment j"}, {"statement": "cost per update O(M(s+1)+log N)", "justification": "gate accounting", "passage": "Each circuit evaluation costs O(s+1); the equality test and conjunction cost O(1) per candidate, and the counter increment costs O(log N)."}]

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

[{"validation_id": "PS:Q-156fa9c912#633", "node_id": "Q-156fa9c912:S0521", "reviewer": "pnp-desk/research/R2788", "model": "gpt-6-luna", "model_family": "gpt", "method": "AGENT_REVIEW", "result": "REFUTED", "independent": false, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[]

## required_recomputations

[]

## counterexamples

[{"validation_id": "PS:Q-156fa9c912#633", "node_id": "Q-156fa9c912:S0521", "reviewer": "pnp-desk/research/R2788", "model": "gpt-6-luna", "model_family": "gpt", "method": "AGENT_REVIEW", "result": "REFUTED", "independent": false, "scope_status": "FULL_TEXT_RECEIVED"}]

## first_invalid_inference

PS:Q-156fa9c912#633 REFUTED: The claimed counter j ranges over {0,...,N}, which has N+1=2^n+1 values and requires n+1 bits. The stated M+ceil(log2 N)=M+n bits do not provide the claimed index representation. Repair: allocate ceil(log2(N+1))=n+1 index bits; the candidate-mask invariant and update argument then apply.

## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The record states the bound implies no polynomial update cost and gives no route role for the target.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2508", "origin_event_ids": ["edd488c65f63ec27b7bd0cd1fa251f06577f0f1f883ae90111cf9d41fab478b4"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

independent re-review with the full statement

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
