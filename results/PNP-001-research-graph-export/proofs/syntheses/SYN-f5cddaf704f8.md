# Synthesis SYN-f5cddaf704f8

## synthesis_id

SYN-f5cddaf704f8

## original_ids

["Q-156fa9c912:S0510"]

## mathematical_domain

Boolean circuit complexity

## title

Position-specific candidate-mask update with hardwired columns

## mathematical_statement

Let C_1,...,C_K be an explicitly listed family of Boolean circuits with truth tables E_j in a fixed order. For each position t define the hardwired mask m_t in {0,1}^K by (m_t)_j=E_j[t]. Given candidate bitset x in {0,1}^K and next streamed bit b, define x'_j=x_j AND (b iff (m_t)_j). This is correct for filtering the candidates consistent with the extended prefix and has a fan-in-two AND/NOT circuit of at most K+1 gates for each fixed t. The masks across all t encode the candidate truth tables, so no polynomial-in-(s,n) update bound follows when K is large. The record states that Q-156fa9c912 remains open.

## formula_latex

x'_j = x_j \wedge (b \leftrightarrow (m_t)_j)

## assumptions

["the mask m_t is hardwired for each fixed t"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: LEMMA (position-specific candidate-mask update). Let C_1,...,C_K be an explicitly listed family of Boolean circuits with truth tables E_j in a fixed order. For each position t, define the hardwired mask m_t in {0,1}^K by (m_t)_j=E_j[t]. Given the candidate bitset x in {0,1}^K and next streamed bit b, define x'_j=x_j AND (b iff (m_t)_j). This transition is correct for filtering the candidates consistent with the prefix extended by b, and has a fan-in-two AND/NOT circuit of at most K+1 gates for each fixed t. Proof: If (m_t)_j=1, set x'_j=x_j AND b; otherwise set x'_j=x_j AND NOT b. Share NOT b across coordinates, so the gate count is at most K+1. Coordinate j survives exactly when it was previously present and its truth-table bit at t equals b. Hence the output bitset is precisely the previous candidate set intersected with the candidates agreeing at t; induction on prefix length proves exactness. This is a position-specific circuit family; the masks across all t encode the candidate truth tables, so the result gives no polynomial-in-(s,n) update bound when K is large.
gap: Q-156fa9c912 remains open: this explicit candidate-mask construction costs O(K) gates per position and stores position-specific masks. It does not bound update cost for EXT_{n,s} or arbitrary MCSP decision circuits in terms polynomial in s,n, nor resolve the H_C connection.

## reconstructed_proof

[{"statement": "if (m_t)_j=1 keep x_j AND b, else x_j AND NOT b", "justification": "case analysis on the mask bit", "passage": "If (m_t)_j=1, set x'_j=x_j AND b; otherwise set x'_j=x_j AND NOT b."}, {"statement": "sharing NOT b gives at most K+1 gates", "justification": "gate count", "passage": "Share NOT b across coordinates, so the gate count is at most K+1."}]

## required_theorems

[]

## established_dependencies

[]

## missing_dependencies

[{"needs_validation": "stores position-specific masks costing O(K) per position; no polynomial update bound (the text's open gap)"}]

## required_transfers

[]

## established_transfers

[]

## alternative_derivations

[]

## existing_validations

[{"validation_id": "PS:Q-156fa9c912#621", "node_id": "Q-156fa9c912:S0510", "reviewer": "pnp-desk/research/R2684", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-156fa9c912#621", "node_id": "Q-156fa9c912:S0510", "reviewer": "pnp-desk/research/R2684", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[{"needs_validation": "stores position-specific masks costing O(K) per position; no polynomial update bound (the text's open gap)"}]

## required_recomputations

[]

## counterexamples

[]

## first_invalid_inference



## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The text states a gap and that the update does not bound cost or resolve the H_C connection; it closes no obligation.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2492", "origin_event_ids": ["d42374fe5966581227b7aa390b91ecc2207d1b52bf6edb31e9d9e53f4cf5510f"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

supply the missing arguments/dependencies, then re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
