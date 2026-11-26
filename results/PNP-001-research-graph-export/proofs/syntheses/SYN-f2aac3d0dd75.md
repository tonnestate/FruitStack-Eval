# Synthesis SYN-f2aac3d0dd75

## synthesis_id

SYN-f2aac3d0dd75

## original_ids

["Q-156fa9c912:S0507"]

## mathematical_domain

streaming complexity

## title

Explicit candidate-list update circuit with counter

## mathematical_statement

Fix n>=1, a finite list C_1,...,C_M of n-input Boolean circuits each with at most s fan-in-two gates, and inputs x_t=bin_n(t) for 0<=t<2^n. A state is (t,a_1,...,a_M) with a_j=1 iff C_j agrees with the streamed prefix of length t. There is a fan-in-two AND/OR/NOT transition circuit taking (t,a_1,...,a_M,b) to (t+1,a'_1,...,a'_M), with wraparound at t=2^n-1, of size O(n+M(s+1)), satisfying a'_j=a_j AND [C_j(x_t)=b] for every valid state. Upper bound for the explicit-list representation only; no polynomial bound on M and no lower bound for arbitrary encodings or H_C.

## formula_latex

size = O(n + M(s+1))

## assumptions

["the list C_1..C_M is hardwired", "x_t = bin_n(t)"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: LEMMA (explicit candidate-list update circuit). Fix n≥1, a finite list C_1,…,C_M of n-input Boolean circuits, each with at most s fan-in-two gates, and enumerate inputs as x_t=bin_n(t) for 0≤t<2^n. A state is (t,a_1,…,a_M), where a_j=1 iff C_j agrees with the streamed prefix of length t. There is a fan-in-two AND/OR/NOT transition circuit taking (t,a_1,…,a_M,b) to (t+1,a'_1,…,a'_M), with wraparound at t=2^n−1, of size O(n+M(s+1)). It satisfies a'_j=a_j∧[C_j(x_t)=b] for every valid state. Proof: wire the n bits of t as x_t; evaluate each hardwired C_j using at most s gates; compare its output with b using O(1) gates and AND with a_j. Increment t modulo 2^n using O(n) gates. Each a'_j is 1 exactly when C_j agreed on the prior t positions and agrees at position t. Induction from (0,1,…,1) proves the invariant. This upper bound concerns only the explicit-list representation; it does not bound M polynomially in n,s or give a lower bound for arbitrary encodings or H_C.

## reconstructed_proof

[{"statement": "evaluate each C_j with at most s gates, compare with b, AND with a_j", "justification": "gate counting", "passage": "evaluate each hardwired C_j using at most s gates; compare its output with b using O(1) gates and AND with a_j"}, {"statement": "increment t modulo 2^n with O(n) gates", "justification": "ripple counter", "passage": "Increment t modulo 2^n using O(n) gates"}]

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

[{"validation_id": "PS:Q-156fa9c912#618", "node_id": "Q-156fa9c912:S0507", "reviewer": "pnp-desk/research/R2684", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-156fa9c912#618", "node_id": "Q-156fa9c912:S0507", "reviewer": "pnp-desk/research/R2684", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

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

CONNECTION_NOT_IDENTIFIED | The text scopes the bound to an explicit list and states no route role for the target.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2492", "origin_event_ids": ["ca5b8e40cf573e9563a77c12da834723d02ca4f29ca0d293835ede670704b2f9"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

independent re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
