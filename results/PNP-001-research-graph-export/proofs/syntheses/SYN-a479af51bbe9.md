# Synthesis SYN-a479af51bbe9

## synthesis_id

SYN-a479af51bbe9

## original_ids

["Q-156fa9c912:S0528"]

## mathematical_domain

Boolean circuit complexity

## title

Explicit EXT candidate-mask transition of size O(M(s+n))

## mathematical_statement

Fix n,s and an explicitly listed family D={C_1,...,C_M} of Boolean circuits on n inputs, each with at most s fan-in-two gates and a specified output bit. Fix an order a_0,...,a_(2^n-1) of inputs. After t truth-table bits p_0,...,p_(t-1), encode consistent candidates by a mask u in {0,1}^M with u_j=1 iff C_j(a_i)=p_i for all i<t. Given the next input a_t and bit b, the updated mask is u'_j = u_j AND [C_j(a_t)=b]. This transition has a fan-in-two AND/OR/NOT circuit of size O(M(s+n)), and the new mask is exactly the candidate set consistent with the extended prefix. The bound is linear in M and need not be polynomial when D is the full size-s class. The record closes Q-156fa9c912, a question id.

## formula_latex

size = O(M(s+n))

## assumptions

["D is explicitly listed and its descriptions are available to the transition circuit"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: LEMMA (explicit EXT candidate-mask transition). Fix n,s and an explicitly listed family D={C_1,...,C_M} of Boolean circuits on n inputs, each with at most s fan-in-two gates and a specified output bit. Fix an order a_0,...,a_{2^n-1} of the inputs. After t truth-table bits p_0,...,p_{t-1}, encode the consistent candidates by a mask u in {0,1}^M, where u_j=1 iff C_j(a_i)=p_i for every i<t. Given the next input a_t and bit b, the updated mask is u'_j = u_j AND [C_j(a_t)=b]. This transition has a fan-in-two AND/OR/NOT circuit of size O(M(s+n)), and the new mask is exactly the candidate set consistent with the extended prefix. Proof: For each j, evaluate C_j at a_t in topological order, using at most s gates plus O(n) input handling. Compare its output to b using O(1) gates, then AND the equality bit with u_j. Doing this for all M candidates costs O(M(s+n)) gates. The formula for u'_j is exactly the conjunction of prior consistency and agreement at position t, so induction on t proves the mask invariant and exactness. Scope: D is explicitly listed and its descriptions are available to the transition circuit. The bound is linear in M, so it need not be polynomial in s when D is the full size-s circuit class. This does not establish a representation through an arbitrary MCSP decision circuit H_C.
evidence: Direct construction and induction: evaluate each candidate on the current input, compare with b, and retain it exactly when its prior mask bit is 1 and the output matches. This yields O(M(s+n)) fan-in-two gates and makes the candidate-count dependence explicit.
closes: Q-156fa9c912

## reconstructed_proof

[{"statement": "evaluate C_j at a_t in at most s gates plus O(n) input handling; compare with b in O(1); AND with u_j", "justification": "gate accounting", "passage": "For each j, evaluate C_j at a_t in topological order, using at most s gates plus O(n) input handling."}, {"statement": "induction on t proves exactness of the mask", "justification": "induction", "passage": "so induction on t proves the mask invariant and exactness"}]

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

[{"validation_id": "PS:Q-156fa9c912#656", "node_id": "Q-156fa9c912:S0528", "reviewer": "pnp-desk/research/R2844", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-156fa9c912#656", "node_id": "Q-156fa9c912:S0528", "reviewer": "pnp-desk/research/R2844", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

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

CONNECTION_NOT_IDENTIFIED | The record states closes: Q-156fa9c912, which names a question rather than a route obligation, and states no H_C representation.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2532", "origin_event_ids": ["0f0202b3987e2c1ef0c54a311f4234ecddec4c446c52527058ba07bde1932212"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

independent re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
