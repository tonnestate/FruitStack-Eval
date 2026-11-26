# Synthesis SYN-29dbc13d7c00

## synthesis_id

SYN-29dbc13d7c00

## original_ids

["Q-156fa9c912:S0476"]

## mathematical_domain

streaming complexity

## title

Minimal state count of exact streaming recognizers equals distinct residuals per layer

## mathematical_statement

Let L be any language of fixed-length words {0,1}^N recognized exactly by a deterministic left-to-right streaming machine. For each depth t and prefix p in {0,1}^t let R_L(p)={u in {0,1}^(N-t): pu in L}. (1) Any such machine has at least |{R_L(p): p in {0,1}^t}| distinct states after t symbols. (2) The layered machine whose depth-t states are the distinct sets R_L(p), with transition R_L(p) --b--> R_L(pb), recognizes L exactly. (3) Hence the minimum number of states at layer t equals the number of distinct residuals R_L(p) at that depth. Scope: all N>=0, all Boolean languages L in {0,1}^N, one bit per transition, fixed known depth; no uniformity, transition gate complexity or MCSP simulation is claimed.

## formula_latex

\min |states_t| = |{R_L(p): p in {0,1}^t}|

## assumptions

["the machine reads one bit per transition with a fixed known depth", "L is recognized exactly"]

## proof_status

CLAIMED

## validation_status

NO_QUALIFYING_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: Let L be any language of fixed-length words {0,1}^N recognized exactly by a deterministic left-to-right streaming machine. For each depth t and prefix p in {0,1}^t define R_L(p)={u in {0,1}^{N-t}: pu is in L}. Any such machine has at least |{R_L(p):p in {0,1}^t}| distinct states after t symbols. Conversely, the layered machine whose depth-t states are the distinct sets R_L(p), with transition R_L(p) --b--> R_L(pb), recognizes L exactly. Therefore the minimum possible number of states at layer t is exactly the number of distinct accepting-continuation residuals at that depth. Proof: If two prefixes p,q reach the same deterministic state, then every continuation u induces the same accept/reject outcome from that state, so R_L(p)=R_L(q); contrapositively distinct residuals require distinct states. For the converse define the transition by appending b to any representative prefix; this is well-defined because equal residuals at depth t imply that for each b the residuals after pb agree, as membership of every remaining v is equivalent to bv belonging to the original residual. At depth N accept exactly when the empty continuation belongs to the residual. Induction on t proves the invariant that the state after p is R_L(p), hence exact recognition. This characterizes the information an exact fixed-length streaming algorithm must preserve; it provides no transition circuit bound in terms of an arbitrary MCSP decision circuit H_C.
scope: All N>=0 and all Boolean languages L subseteq {0,1}^N; deterministic streaming machines reading one bit per transition, with a fixed known depth. State lower bound is per layer; no uniformity, transition gate complexity, or MCSP simulation claim is included.
closes: Q-156fa9c912

## reconstructed_proof

[{"statement": "prefixes reaching the same state have equal residuals", "justification": "same state, same future outcomes", "passage": "then every continuation u induces the same accept/reject outcome from that state"}, {"statement": "transition R(p) --b--> R(pb) is well defined on residuals", "justification": "residual after b determined by residual and b", "passage": "equal residuals at depth t imply that for each b the residuals after pb agree"}]

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

[{"validation_id": "PS:Q-156fa9c912#589", "node_id": "Q-156fa9c912:S0476", "reviewer": "pnp-desk/research/R2652", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "VALIDATION_SCOPE_INCOMPLETE"}]

## independent_validations

[]

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

CONNECTION_NOT_IDENTIFIED | The record lists closes: Q-156fa9c912 (a question id, not a route obligation) and states it provides no transition bound for an arbitrary MCSP decision circuit H_C.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2420", "origin_event_ids": ["ce32f75808d8d340a6ed9c517634d7948a7c7a66632b17bde51d117db38448db"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

independent re-review with the full statement

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
