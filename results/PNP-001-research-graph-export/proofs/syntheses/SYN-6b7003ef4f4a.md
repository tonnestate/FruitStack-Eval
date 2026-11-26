# Synthesis SYN-6b7003ef4f4a

## synthesis_id

SYN-6b7003ef4f4a

## original_ids

["Q-156fa9c912:S0479"]

## mathematical_domain

streaming complexity

## title

Residual quotient automaton of a finite language is minimal per layer

## mathematical_statement

Let F subset {0,1}^N. For each prefix p of length at most N define R(p)={u in {0,1}^(N-|p|): pu in F}. Make one state per distinct residual set at each layer (layers kept distinct). From state R(p) at layer t on bit b go to R(pb) at layer t+1; this is well defined because R(p)=R(q) implies R(pb)=R(qb). Layer-N states accept iff the residual contains the empty string. The resulting layered automaton recognizes F exactly with r_t states at layer t. Combined with the distinguishability argument in S0478, r_t is the minimum number of states at layer t for any exact deterministic streaming recognizer. No transition-complexity claim is made.

## formula_latex



## assumptions

["F is a finite subset of {0,1}^N"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: Residual quotient automaton for a finite language. Let F be a subset of {0,1}^N. For each prefix p of length at most N, define R(p)={u in {0,1}^{N-|p|}: pu in F}. Make one state for each distinct residual set at each layer, keeping layers distinct even if their sets coincide. From state R(p) at layer t, on bit b transition to R(pb) at layer t+1. This transition is well-defined: if R(p)=R(q) for |p|=|q|=t, then for every suffix u of length N-t-1, u is in R(pb) exactly when bu is in R(p), and likewise for q; hence R(pb)=R(qb). Declare the layer-N state accepting exactly when its residual contains the empty string. The resulting deterministic layered automaton recognizes F exactly and has r_t states at layer t, where r_t is the number of distinct residuals there. Combined with the distinguishability argument in S0478, this proves that r_t is the minimum possible number of states at layer t for any exact deterministic streaming recognizer. The construction does not bound the cost of computing its transitions from H_C or the total description size as a function of n and s.
scope: Every finite binary language F subseteq {0,1}^N; deterministic one-pass recognition with position known to the machine. State counts are per layer; no transition-complexity assertion.
evidence: Direct construction and proof: successor residuals are determined solely by the current residual and next bit, because R(pb)={u: bu in R(p)}. Acceptance at the final layer is membership of the empty suffix. No computation is needed for this general finite-language lemma.

## reconstructed_proof

[{"statement": "transition on residuals is well defined", "justification": "equal residuals give equal successors", "passage": "if R(p)=R(q) for |p|=|q|=t, then for every suffix u of length N-t-1, u is in R(pb) exactly when bu is in R(p)"}, {"statement": "minimality follows from the distinguishability lower bound", "justification": "cited lower bound", "passage": "Combined with the distinguishability argument in S0478, this proves that r_t is the minimum possible number of states at layer t"}]

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

[{"validation_id": "PS:Q-156fa9c912#606", "node_id": "Q-156fa9c912:S0479", "reviewer": "pnp-desk/research/R2676", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-156fa9c912#606", "node_id": "Q-156fa9c912:S0479", "reviewer": "pnp-desk/research/R2676", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

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

CONNECTION_NOT_IDENTIFIED | The record combines S0478 but states no route role; it explicitly does not bound transition cost or H_C.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2420", "origin_event_ids": ["59445a7a9922a27a8c51d6ba91d501f1c50afb36ed5933635618441cc54a0351"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

independent re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
