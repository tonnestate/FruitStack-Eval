# Synthesis SYN-38f562faa14d

## synthesis_id

SYN-38f562faa14d

## original_ids

["Q-156fa9c912:S0477"]

## mathematical_domain

streaming complexity

## title

Residual-section recursion for finite prefix families

## mathematical_statement

Let N>=1, let F be any set of N-bit strings, and for each prefix p of length t<=N let R_t(p)={u in {0,1}^(N-t): pu in F}. For t<N and b in {0,1}: R_{t+1}(pb)={v in {0,1}^(N-t-1): bv in R_t(p)}. Consequently R_t(p) is the disjoint union of 0 R_{t+1}(p0) and 1 R_{t+1}(p1), where bA={bv: v in A}. Scope: exact residual languages for any fixed-length target F, including EXT with F=Im(Eval); the statement gives no bound on computing the sections in real gates from an arbitrary MCSP decision circuit H_C.

## formula_latex

R_{t+1}(pb)=\{v: bv \in R_t(p)\}

## assumptions

["F is an arbitrary set of N-bit strings"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: Residual-section lemma for EXT. Let N>=1, let F be any set of N-bit strings, and for each prefix p of length t<=N define R_t(p)={u in {0,1}^{N-t}: pu in F}. For t<N and b in {0,1}, R_{t+1}(pb)={v in {0,1}^{N-t-1}: bv in R_t(p)}. Consequently R_t(p) is the disjoint union of 0R_{t+1}(p0) and 1R_{t+1}(p1), where bA={bv:v in A}. Proof: For any v of length N-t-1, v belongs to R_{t+1}(pb) iff pbv belongs to F, iff bv belongs to R_t(p). Every length-(N-t) string has a unique first bit b and remaining suffix v, so it belongs to exactly one of the two displayed sections; membership in that section is equivalent to pv with that first bit lying in F by the defining equivalence. Thus the pair of child residuals is exactly the information needed to reconstruct the parent residual, and each child is obtained by a fixed section operation. Scope: exact residual languages for any fixed-length target F, including EXT with F=Im(Eval); this proves the abstract transition identity only and gives no bound on representing or computing the sections in real gates from an arbitrary MCSP decision circuit H_C.
evidence: Direct proof by unpacking the definition of R_t(p); no finite computation is needed. This supplies the exact residual transition operation but does not claim a gate-cost bound or close the arbitrary-H_C transition-simulation obligation.

## reconstructed_proof

[{"statement": "membership of v in R_{t+1}(pb) is equivalent to bv in R_t(p)", "justification": "unfold definitions", "passage": "v belongs to R_{t+1}(pb) iff pbv belongs to F, iff bv belongs to R_t(p)"}, {"statement": "every string of length N-t has a unique first bit and suffix, so the two sections partition R_t(p)", "justification": "unique decomposition", "passage": "Every length-(N-t) string has a unique first bit b and remaining suffix v"}]

## required_theorems

[]

## established_dependencies

[]

## missing_dependencies

[{"needs_validation": "the gate-cost remark is not argued; the text itself disclaims any gate bound"}, {"unsupported_assertion": "each child is obtained by a fixed section operation at gate cost"}]

## required_transfers

[]

## established_transfers

[]

## alternative_derivations

[]

## existing_validations

[{"validation_id": "PS:Q-156fa9c912#601", "node_id": "Q-156fa9c912:S0477", "reviewer": "pnp-desk/research/R2676", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}, {"validation_id": "PS:Q-156fa9c912#604", "node_id": "Q-156fa9c912:S0477", "reviewer": "pnp-desk/research/R2676", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-156fa9c912#601", "node_id": "Q-156fa9c912:S0477", "reviewer": "pnp-desk/research/R2676", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}, {"validation_id": "PS:Q-156fa9c912#604", "node_id": "Q-156fa9c912:S0477", "reviewer": "pnp-desk/research/R2676", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[{"needs_validation": "the gate-cost remark is not argued; the text itself disclaims any gate bound"}]

## required_recomputations

[]

## counterexamples

[]

## first_invalid_inference



## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The text explicitly says it proves only the abstract transition identity and closes no arbitrary-H_C transition-simulation obligation, with no route role stated.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2420", "origin_event_ids": ["f9091ccc079a549d81749dd4b764f39f57550acc9335aa87354e3e055a2003c8"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

supply the missing arguments/dependencies, then re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
