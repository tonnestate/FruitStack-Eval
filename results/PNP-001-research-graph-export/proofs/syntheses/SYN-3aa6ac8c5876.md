# Synthesis SYN-3aa6ac8c5876

## synthesis_id

SYN-3aa6ac8c5876

## original_ids

["Q-156fa9c912:S0503"]

## mathematical_domain

Boolean circuit complexity

## title

Nondeterministic verification bound for EXT prefixes

## mathematical_statement

Fix n,s and an explicit binary encoding of fan-in-two Boolean circuits with at most s gates, each gate record using O(log(n+s)) bits, output wire specified in the description. Let N=2^n. For each t in {0,...,N}, EXT_{n,s}(p)=1 for p in {0,1}^t iff there exists a valid description d of at most L=O(s log(n+s)) bits whose circuit C_d agrees with p on the first t inputs in the fixed truth-table order. Then EXT_{n,s}(p) is in NP with witness length at most L+O(1) and deterministic verification time O(t(s+n)+L) in a standard gate-list encoding. This is a nondeterministic upper bound and certificate cost only; no deterministic transition algorithm, no compression, no hardness lower bound.

## formula_latex

witness length <= L + O(1),\quad verification time = O(t(s+n)+L)

## assumptions

["an explicit binary encoding of fan-in-two circuits with at most s gates", "each gate record uses O(log(n+s)) bits"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: LEMMA (EXT prefix has a short verifiable circuit witness). Fix n,s and an explicit binary encoding of fan-in-two Boolean circuits with at most s gates, where each gate record uses O(log(n+s)) bits and the output wire is specified in the description. Let N=2^n. For each t in {0,...,N}, define EXT_{n,s}(p)=1 for p in {0,1}^t iff there exists a valid description d of at most L=O(s log(n+s)) bits whose circuit C_d agrees with p on the first t inputs in the fixed truth-table order. Then EXT_{n,s}(p) is in NP with witness length at most L+O(1) and deterministic verification time O(t(s+n)+L), in a standard gate-list encoding. Proof: Guess d, reject if it is not a valid circuit description of the stated size, then for each of the t input strings evaluate the s-gate circuit in topological order and compare its output with the corresponding bit of p. One circuit evaluation costs O(s+n) including input access under the stated encoding, so all comparisons cost O(t(s+n)); description validation and parsing cost O(L). The verifier accepts exactly when a size-at-most-s circuit has the required prefix, which is exactly the defining existential condition. Scope: this proves a nondeterministic upper bound and an explicit certificate/checking cost only; it gives no deterministic transition algorithm, no compression of the candidate set, and no hardness lower bound.

## reconstructed_proof

[{"statement": "the verifier guesses d, rejects invalid descriptions, and checks the prefix", "justification": "existential certificate", "passage": "Guess d, reject if it is not a valid circuit description of the stated size"}, {"statement": "t circuit evaluations cost O(t(s+n))", "justification": "one evaluation is O(s+n)", "passage": "so all comparisons cost O(t(s+n))"}]

## required_theorems

[]

## established_dependencies

[]

## missing_dependencies

[{"needs_validation": "the statement is an NP upper bound with an explicit certificate cost only; no deterministic algorithm or hardness is claimed"}]

## required_transfers

[]

## established_transfers

[]

## alternative_derivations

[]

## existing_validations

[{"validation_id": "PS:Q-156fa9c912#614", "node_id": "Q-156fa9c912:S0503", "reviewer": "pnp-desk/research/R2684", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-156fa9c912#614", "node_id": "Q-156fa9c912:S0503", "reviewer": "pnp-desk/research/R2684", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[{"needs_validation": "the statement is an NP upper bound with an explicit certificate cost only; no deterministic algorithm or hardness is claimed"}]

## required_recomputations

[]

## counterexamples

[]

## first_invalid_inference



## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The text explicitly scopes the result to an upper bound with no hardness lower bound and no route role.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2484", "origin_event_ids": ["2a5ec1b628acdc13c4063a57745c45abee163491bc9ff39b996163676eadab3c"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

supply the missing arguments/dependencies, then re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
