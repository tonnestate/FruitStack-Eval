# Synthesis SYN-184ff5ceddd1

## synthesis_id

SYN-184ff5ceddd1

## original_ids

["Q-156fa9c912:S0515"]

## mathematical_domain

Boolean circuit complexity

## title

Representation-specific update cost for an incidence-vector candidate list

## mathematical_statement

Let E_1,...,E_M be fixed N-bit truth tables and encode the surviving candidate set by its incidence vector x in {0,1}^M. At a fixed position t and streamed bit b, the exact next incidence vector is y_i=x_i AND [E_i[t]=b]. A fan-in-two Boolean circuit computes this map with at most M+1 gates (one shared negation of b and at most one gate per coordinate if the table column is supplied as constants). The update size is O(M); it establishes no bound polynomial in (n,s) unless M is polynomial in (n,s), and the record states it does not close the universal update-computation obligation G0004.

## formula_latex

y_i = x_i \wedge [E_i[t]=b]

## assumptions

["truth tables are fixed"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: LEMMA (candidate-list update cost, representation-specific). Let E_1,...,E_M be fixed N-bit truth tables and encode the surviving candidate set by its incidence vector x in {0,1}^M. At a fixed position t and streamed bit b, the exact next incidence vector is y_i=x_i AND [E_i[t]=b]. A fan-in-two Boolean circuit computes this map using at most M+1 gates (indeed, at most one shared negation of b and at most one gate per coordinate if the table column is supplied as constants). Proof: For each i, if E_i[t]=b then y_i=x_i; otherwise y_i=0. These coordinate functions are exactly the stated intersection filter. Thus the explicit-list representation has update size O(M), but this lemma establishes no bound polynomial in (n,s) unless M itself is polynomial in (n,s); it does not close the universal update-computation obligation G0004.

## reconstructed_proof

[{"statement": "for each i, y_i = x_i if E_i[t]=b, else 0", "justification": "case analysis", "passage": "For each i, if E_i[t]=b then y_i=x_i; otherwise y_i=0."}]

## required_theorems

[]

## established_dependencies

[]

## missing_dependencies

[{"needs_validation": "no bound polynomial in (n,s) unless M is; G0004 not closed (text)"}]

## required_transfers

[]

## established_transfers

[]

## alternative_derivations

[]

## existing_validations

[{"validation_id": "PS:Q-156fa9c912#625", "node_id": "Q-156fa9c912:S0515", "reviewer": "pnp-desk/research/R2684", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-156fa9c912#625", "node_id": "Q-156fa9c912:S0515", "reviewer": "pnp-desk/research/R2684", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[{"needs_validation": "no bound polynomial in (n,s) unless M is; G0004 not closed (text)"}]

## required_recomputations

[]

## counterexamples

[]

## first_invalid_inference



## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The record explicitly states it does not close the obligation G0004, so it states no closing role.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2500", "origin_event_ids": ["055ee49ed00bbf2edd12a07fe0257ad6e88908bec389ea8ece3f28957d8150cc"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

supply the missing arguments/dependencies, then re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
