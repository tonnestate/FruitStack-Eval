# Synthesis SYN-cbdccbd10d82

## synthesis_id

SYN-cbdccbd10d82

## original_ids

["Q-0332cb0a65:S0038"]

## mathematical_domain

GF(2) affine systems; shared auxiliaries

## title

Shared-auxiliary consistency of full owner sets

## mathematical_statement

Targets H_i = pi(sol E_i) nonempty, pi the projection to x, E_i finite affine systems over (x, z) with z possibly shared. (a) If the intersection of H_i over Q is empty, then the union over Q of E_i is inconsistent. (b) If there is Z(x) such that for every i and every x in H_i the fibre {z : (x,z) in sol E_i} equals Z(x), then the union over Q is consistent iff the intersection of H_i over Q is nonempty.

## formula_latex

\bigcap_{i \in Q} H_i = \emptyset \Rightarrow \bigcup_{i \in Q} E_i \text{ inconsistent}

## assumptions

["targets H_i nonempty", "uniform fibre Z(x) in case (b)"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: LEMMA R-sound and LEMMA U (shared auxiliaries allowed). Setting: targets H_i = pi(sol E_i) nonempty, pi = projection to x, E_i finite affine systems over (x,z), z may be shared. (a) If the intersection of H_i over Q is empty, then the union over Q of E_i is inconsistent. (b) If there is Z(x) such that for every i and every x in H_i the fibre {z : (x,z) in sol E_i} equals Z(x), then the union over Q is consistent iff the intersection of H_i over Q is nonempty. Proofs: (a) any solution (x,z) gives x in every H_i, hence in the empty intersection. (b) for x in the intersection pick z in Z(x) (nonempty as x is in H_i); (x,z) satisfies every E_i in Q. Scope: consistency of full owner sets only. Does NOT give the MUS pushforward of S0009(a), which needs consistency of subsets S_i, and subsets can shrink the z-fibre. G0001 stays open.
status_requested: CLAIMED
session: pnp-desk/research/R1509

## reconstructed_proof

[{"statement": "Solutions of the union project into the empty intersection.", "justification": "any solution (x,z) gives x in every H_i", "passage": "any solution (x,z) gives x in every H_i, hence in the empty intersection"}, {"statement": "A common z exists for x in the intersection.", "justification": "fibre Z(x) nonempty since x in H_i", "passage": "for x in the intersection pick z in Z(x) (nonempty as x is in H_i)"}]

## required_theorems

[]

## established_dependencies

[]

## missing_dependencies

[{"needs_validation": "Scope note: this does not give the S0009(a) pushforward, which needs consistency of subsets; G0001 stays open per the record."}]

## required_transfers

[]

## established_transfers

[]

## alternative_derivations

[]

## existing_validations

[{"validation_id": "PS:Q-0332cb0a65#79", "node_id": "Q-0332cb0a65:S0038", "reviewer": "pnp-desk/research/R1963", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-0332cb0a65#79", "node_id": "Q-0332cb0a65:S0038", "reviewer": "pnp-desk/research/R1963", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[{"needs_validation": "Scope note: this does not give the S0009(a) pushforward, which needs consistency of subsets; G0001 stays open per the record."}]

## required_recomputations

[]

## counterexamples

[]

## first_invalid_inference



## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The text states the result does not give the MUS pushforward needed and G0001 stays open, so no concrete route role is stated.

## source_references

{"question_id": "Q-0332cb0a65", "session": "pnp-desk/research/R1509", "origin_event_ids": ["4e4d15b61cdcecda95c21e52cdaf05f3f9c974446261ffa9ade26b6c051d0725"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

supply the missing arguments/dependencies, then re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
