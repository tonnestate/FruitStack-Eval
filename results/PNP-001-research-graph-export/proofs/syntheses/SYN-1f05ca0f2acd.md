# Synthesis SYN-1f05ca0f2acd

## synthesis_id

SYN-1f05ca0f2acd

## original_ids

["Q-156fa9c912:S0526"]

## mathematical_domain

streaming complexity

## title

Explicit-family residual-mask update with address counter

## mathematical_statement

Let C_1,...,C_M be explicitly listed Boolean circuits on n input bits with fan-in-two gate counts s_1,...,s_M. A streaming machine can maintain the current address i and one agreement bit a_j per candidate using a fan-in-two AND/OR/NOT transition circuit of size O(n+M+sum_j s_j). On input bit b, set a'_j=a_j AND [C_j(i)=b] and advance i modulo 2^n. After t bits, a_j=1 exactly when C_j's truth table agrees with the streamed prefix. The record states the bound applies only to an explicitly listed family and gives no compact transition bound for the minimized EXT automaton or for arbitrary MCSP decision circuits; the gap is whether EXT transitions admit bounded real-gate cost on H_C.

## formula_latex

O(n+M+\sum_j s_j)

## assumptions

["the family is explicitly listed with known gate counts s_j"]

## proof_status

CLAIMED

## validation_status

REFUTED_BY_DEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: LEMMA (explicit-family residual-mask update). Let C_1,...,C_M be explicitly listed Boolean circuits on n input bits, with fan-in-two gate counts s_1,...,s_M. A streaming machine can maintain the current address i and one agreement bit a_j per candidate using a fan-in-two AND/OR/NOT transition circuit of size O(n+M+sum_j s_j). On input bit b, set a'_j = a_j AND [C_j(i)=b] and advance i modulo 2^n. Initially i=0 and all a_j=1. After t bits, a_j=1 exactly when C_j's truth table agrees with the streamed prefix. Proof: Evaluate each given circuit C_j on i, costing sum_j s_j gates; compare each output with b and conjoin with a_j, costing O(M) gates; increment the address with O(n) gates. The stated invariant holds initially. Each update conjoins prior agreement with agreement at the current address, so induction proves it for every t. This applies only to an explicitly listed family; it gives no compact transition bound for the minimized EXT automaton or arbitrary MCSP decision circuits.
gap: Whether EXT transitions admit bounded real-gate cost on H_C, and whether any representation applies to arbitrary MCSP decision circuits.

## reconstructed_proof

[{"statement": "evaluate each C_j on i costing sum_j s_j gates; compare and conjoin O(M); increment O(n)", "justification": "gate accounting", "passage": "Evaluate each given circuit C_j on i, costing sum_j s_j gates"}, {"statement": "induction proves the agreement invariant for every t", "justification": "induction", "passage": "so induction proves it for every t"}]

## required_theorems

[]

## established_dependencies

[]

## missing_dependencies

[{"needs_validation": "whether EXT transitions admit bounded real-gate cost on H_C is the open gap named in the text"}]

## required_transfers

[]

## established_transfers

[]

## alternative_derivations

[]

## existing_validations

[{"validation_id": "PS:Q-156fa9c912#643", "node_id": "Q-156fa9c912:S0526", "reviewer": "pnp-desk/research/R2820", "model": "gpt-6-luna", "model_family": "gpt", "method": "AGENT_REVIEW", "result": "REFUTED", "independent": false, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[{"needs_validation": "whether EXT transitions admit bounded real-gate cost on H_C is the open gap named in the text"}]

## required_recomputations

[]

## counterexamples

[{"validation_id": "PS:Q-156fa9c912#643", "node_id": "Q-156fa9c912:S0526", "reviewer": "pnp-desk/research/R2820", "model": "gpt-6-luna", "model_family": "gpt", "method": "AGENT_REVIEW", "result": "REFUTED", "independent": false, "scope_status": "FULL_TEXT_RECEIVED"}]

## first_invalid_inference

PS:Q-156fa9c912#643 REFUTED: The address is modulo 2^n. After N=2^n input bits it wraps to zero, while the agreement mask can stay live; a stream longer than N may therefore be accepted. This violates recognition of the finite prefix language. The done-bit repair is recorded separately as S0643.

## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The record states an open gap and scopes the bound to explicit families, with no closing role.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2524", "origin_event_ids": ["522c093cb9127f3edde77cba0172cec1239591374cafced38a74e658e505adb3"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

supply the missing arguments/dependencies, then independent re-review with the full statement

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
