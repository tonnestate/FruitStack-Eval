# Synthesis SYN-f5adbd51f5a5

## synthesis_id

SYN-f5adbd51f5a5

## original_ids

["Q-156fa9c912:S0502"]

## mathematical_domain

Boolean circuit complexity

## title

EXT as an existential projection of a decision circuit

## mathematical_statement

Let H:{0,1}^N->{0,1} decide membership in a family F of N-bit strings and let EXT_H(p)=1 iff some member of F extends prefix p. For every prefix p of length t, EXT_H(p)=OR_{u in {0,1}^(N-t)} H(pu). For b in {0,1} and t<N, EXT_H(pb)=OR_{u in {0,1}^(N-t-1)} H(pbu). The exact next-state values are existential projections of H, using 2^(N-t) and 2^(N-t-1) evaluations respectively. No bounded-call or gate-cost-preserving reduction for arbitrary H is claimed.

## formula_latex

EXT_H(pb)=\bigvee_{u \in \{0,1\}^{N-t-1}} H(pbu)

## assumptions

["H decides membership in F exactly"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: LEMMA (EXT as existential projection of a decision circuit). Let H:{0,1}^N->{0,1} decide membership in a family F of N-bit strings, and let EXT_H(p)=1 iff some member of F extends prefix p. For every prefix p of length t, EXT_H(p)=OR_{u in {0,1}^{N-t}} H(pu). For b in {0,1} and t<N, EXT_H(pb)=OR_{u in {0,1}^{N-t-1}} H(pbu). Proof: By the definition of concatenation, the strings extending p are exactly the pu with |u|=N-t; membership in F is exactly H(pu)=1. The same argument applies after fixing next bit b. Thus the exact next-state values are existential projections of H, with the explicit disjunction using 2^(N-t) and 2^(N-t-1) evaluations respectively. This gives no bounded-call or gate-cost-preserving reduction for arbitrary H.
closes: Q-156fa9c912

## reconstructed_proof

[{"statement": "strings extending p are exactly the pu with |u|=N-t", "justification": "concatenation", "passage": "the strings extending p are exactly the pu with |u|=N-t"}, {"statement": "membership in F is exactly H(pu)=1", "justification": "H decides F", "passage": "membership in F is exactly H(pu)=1"}]

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

[{"validation_id": "PS:Q-156fa9c912#613", "node_id": "Q-156fa9c912:S0502", "reviewer": "pnp-desk/research/R2684", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-156fa9c912#613", "node_id": "Q-156fa9c912:S0502", "reviewer": "pnp-desk/research/R2684", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

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

CONNECTION_NOT_IDENTIFIED | The record lists closes: Q-156fa9c912 (a question id, not a route obligation) and states that no gate-cost reduction for arbitrary H is given.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2484", "origin_event_ids": ["6c23230e8e67a980f0f48bedfbe3abcc7735f1edbc76e5eeba2368e592519dec"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

independent re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
