# Synthesis SYN-c0c4fb5d025f

## synthesis_id

SYN-c0c4fb5d025f

## original_ids

["Q-156fa9c912:S0524"]

## mathematical_domain

Boolean circuit complexity

## title

Explicit candidate-list update circuit of size K(s+6)+cn

## mathematical_statement

Let C_1,...,C_K be Boolean circuits, each on n input bits with at most s fan-in-two AND/OR/NOT gates, with truth-table bits read in the order indexed by i in {0,1}^n. A streaming state (i,M), with mask M_j=1 exactly when C_j agrees with all bits read so far, can be updated on the next bit b by a fan-in-two AND/OR/NOT circuit of at most K(s+6)+cn gates for an absolute constant c. The update is M'_j=M_j AND [C_j(i)=b] together with i'=i+1 modulo 2^n. It is an exact finite-candidate implementation, not a polynomial-in-s bound when K is the full set of size-s circuit descriptions.

## formula_latex

size \le K(s+6)+cn

## assumptions

["n counter bits index the truth table", "M_j=1 iff C_j agrees with all bits read so far"]

## proof_status

CLAIMED

## validation_status

REFUTED_BY_DEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: LEMMA (explicit candidate-list update cost). Let C_1,...,C_K be Boolean circuits, each on n input bits and with at most s fan-in-two AND/OR/NOT gates, and let their truth-table bits be read in the same fixed order indexed by i in {0,1}^n. A streaming state (i,M), where M is a K-bit mask and M_j=1 exactly when C_j agrees with all bits read so far, can be updated on the next streamed bit b by a fan-in-two AND/OR/NOT circuit of at most K(s+6)+c n gates for an absolute constant c. The update is M'_j=M_j AND [C_j(i)=b] for every j, together with i'=i+1 modulo 2^n. Proof: For each j, use a copy of C_j with the n counter bits as input to compute c_j=C_j(i), costing at most s gates. Compute the match bit as (c_j AND b) OR (NOT c_j AND NOT b), using at most four gates per j, with NOT b shared across j. Compute M'_j by one further AND gate. Thus all K mask coordinates cost at most K(s+5)+1 gates. A ripple increment of the n-bit counter uses O(n) fan-in-two gates: bit 0 is negated, and bit r>0 is toggled exactly when all lower bits are 1, with each prefix conjunction and each XOR implementable using O(1) gates per bit. Hence the total is at most K(s+6)+c n for some absolute c. Induction on the number of read bits proves the mask invariant: the update retains C_j exactly when it was previously retained and its next truth-table bit equals b. This is an exact finite-candidate streaming implementation, not a polynomial-in-s bound when K is the full set of size-s circuit descriptions.

## reconstructed_proof

[{"statement": "mask coordinates cost at most K(s+5)+1 gates", "justification": "per-candidate count", "passage": "Thus all K mask coordinates cost at most K(s+5)+1 gates."}, {"statement": "ripple increment costs O(n) gates", "justification": "ripple counter", "passage": "A ripple increment of the n-bit counter uses O(n) fan-in-two gates"}]

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

[{"validation_id": "PS:Q-156fa9c912#641", "node_id": "Q-156fa9c912:S0524", "reviewer": "pnp-desk/research/R2820", "model": "gpt-6-luna", "model_family": "gpt", "method": "AGENT_REVIEW", "result": "REFUTED", "independent": false, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[]

## required_recomputations

[]

## counterexamples

[{"validation_id": "PS:Q-156fa9c912#641", "node_id": "Q-156fa9c912:S0524", "reviewer": "pnp-desk/research/R2820", "model": "gpt-6-luna", "model_family": "gpt", "method": "AGENT_REVIEW", "result": "REFUTED", "independent": false, "scope_status": "FULL_TEXT_RECEIVED"}]

## first_invalid_inference

PS:Q-156fa9c912#641 REFUTED: The modulo-2^n index wraps after the final truth-table bit, and the stated state has no done flag or other length information. With a listed constant-zero circuit and an all-zero truth table, a further zero bit preserves the candidate mask, falsely accepting a string longer than the truth-table length.

## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The record scopes the result to finite explicit candidate lists and states no route role.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2516", "origin_event_ids": ["0e51740db81f1a62a75dd085901d581a56fde849a7ab8f11edbc005f3e9b4798"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

independent re-review with the full statement

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
