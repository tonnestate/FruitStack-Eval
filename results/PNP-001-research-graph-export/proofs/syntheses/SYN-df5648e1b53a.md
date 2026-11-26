# Synthesis SYN-df5648e1b53a

## synthesis_id

SYN-df5648e1b53a

## original_ids

["Q-156fa9c912:S0478"]

## mathematical_domain

streaming complexity

## title

Layerwise state lower bound for exact one-pass recognition

## mathematical_statement

Let N>=0, F subseteq {0,1}^N, 0<=t<=N. Define R_t(p)={u in {0,1}^(N-t): pu in F} for each p in {0,1}^t and let r_t be the number of distinct residual sets. Any deterministic streaming machine that decides membership in F exactly must reach at least r_t distinct states after t bits, hence needs at least ceil(log2 r_t) state bits (zero if r_t=1). The bound applies to EXT_{n,s} with F the set of size-at-most-s circuit truth tables in a fixed order. It does not bound transition gate cost or give a simulation from arbitrary H_C.

## formula_latex

2^B >= r_t

## assumptions

["exact recognition of F by a deterministic one-pass machine"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: Layerwise residual lower bound for exact streaming recognition. Let N>=0, F subseteq {0,1}^N, and 0<=t<=N. Define R_t(p)={u in {0,1}^{N-t}: pu in F} for each p in {0,1}^t, and let r_t be the number of distinct residual sets. Any deterministic streaming machine that decides membership in F exactly must reach at least r_t distinct states after t bits, hence needs at least ceil(log2 r_t) state bits (zero if r_t=1). Proof: If p and q have different residuals but lead to the same state, choose u in their symmetric difference. Starting from that shared state, the machine's deterministic run on u gives the same answer for pu and qu. Exactly one lies in F, a contradiction. Thus distinct residuals require distinct states; a B-bit state has at most 2^B possibilities, so 2^B>=r_t. This applies to EXT_{n,s} for F equal to the set of size-at-most-s circuit truth tables in the fixed order, but does not bound transition gate cost or give a simulation from arbitrary H_C.
scope: All finite binary languages F subseteq {0,1}^N and all layers t, for deterministic exact one-pass recognition; applies to EXT prefix membership under its fixed truth-table ordering.
evidence: Direct distinguishability proof: unequal residual sets have a suffix on which membership differs; identical machine states force identical future behavior on that suffix, contradicting exact recognition. This general proof requires no finite enumeration.

## reconstructed_proof

[{"statement": "prefixes with different residuals cannot share a machine state", "justification": "distinguishing suffix u in symmetric difference", "passage": "choose u in their symmetric difference"}, {"statement": "B bits give at most 2^B states, so 2^B>=r_t", "justification": "counting", "passage": "a B-bit state has at most 2^B possibilities, so 2^B>=r_t"}]

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

[{"validation_id": "PS:Q-156fa9c912#605", "node_id": "Q-156fa9c912:S0478", "reviewer": "pnp-desk/research/R2676", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-156fa9c912#605", "node_id": "Q-156fa9c912:S0478", "reviewer": "pnp-desk/research/R2676", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

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

CONNECTION_NOT_IDENTIFIED | The text states the bound does not bound transition gate cost or simulate arbitrary H_C, and cites no route closure.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2420", "origin_event_ids": ["38366f88e5039a1d761c0631685b881465a5c4341021c4997bf988e926ff08a9"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

independent re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
