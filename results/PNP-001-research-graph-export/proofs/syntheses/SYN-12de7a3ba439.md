# Synthesis SYN-12de7a3ba439

## synthesis_id

SYN-12de7a3ba439

## original_ids

["Q-0332cb0a65:S0059"]

## mathematical_domain

GF(2) linear systems; binary matroids

## title

Affine GF(2) constraints without auxiliaries: minimal inconsistent sets are port circuits

## mathematical_statement

For GF(2) affine constraints a_i.x = b_i (i in [m], x in GF(2)^n, no auxiliaries), let v_i = (a_i, b_i) and e = (0,...,0,1). S is a minimal inconsistent subset iff S is a minimal set with e in span(v_S); these are exactly the sets C minus e with C a circuit of the binary matroid on {v_i} plus {e} containing e, i.e. the port of that matroid at e.

## formula_latex

e \in \operatorname{span}(v_S)

## assumptions

["no auxiliary variables", "GF(2) only"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: For GF(2) affine constraints a_i.x=b_i (i in [m], x in GF(2)^n, no auxiliary variables), let v_i=(a_i,b_i) in GF(2)^(n+1) and e=(0,...,0,1). Then S is a minimal inconsistent subset iff S is a minimal set with e in span(v_S), and these are exactly the sets C-e with C a circuit of the binary matroid on {v_i}+{e} containing e (the port of that matroid at e). Scope: no auxiliaries; GF(2) only; classical binary port description; does not address existential or shared auxiliaries (G0001).
evidence: Exhaustive check cm-ff155bd741f54e0b: MUS by brute-force SAT vs port by GF(2) rank, 0 mismatches over nv<=3, m<=4 (9,360 instances). Hand proof: step 2 (inconsistent iff e in row span) and step 3 (every circuit in S+e contains e, so S+e is a circuit) checked line by line.

## reconstructed_proof

[{"statement": "Inconsistency of S is equivalent to e in span(v_S).", "justification": "GF(2) linear algebra (step 2 of the hand proof)", "passage": "step 2 (inconsistent iff e in row span)"}, {"statement": "Minimal sets correspond to circuits through e.", "justification": "every circuit in S+e contains e, so S+e is a circuit", "passage": "step 3 (every circuit in S+e contains e, so S+e is a circuit)"}]

## required_theorems

[]

## established_dependencies

[]

## missing_dependencies

[{"needs_validation": "Auxiliary and shared-auxiliary cases are not covered (G0001)."}]

## required_transfers

[]

## established_transfers

[]

## alternative_derivations

[]

## existing_validations

[{"validation_id": "PS:Q-0332cb0a65#88", "node_id": "Q-0332cb0a65:S0059", "reviewer": "pnp-desk/research/R1963", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-0332cb0a65#88", "node_id": "Q-0332cb0a65:S0059", "reviewer": "pnp-desk/research/R1963", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[{"needs_validation": "Auxiliary and shared-auxiliary cases are not covered (G0001)."}]

## required_recomputations

[]

## counterexamples

[]

## first_invalid_inference



## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The text states it is restricted to no auxiliaries and does not address existential or shared auxiliaries (G0001).

## source_references

{"question_id": "Q-0332cb0a65", "session": "pnp-desk/research/R1721", "origin_event_ids": ["4ea06d16a139e0f9854b1710c94687d8a6c7df2e325daa32b8be8f84214cf7e1"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

supply the missing arguments/dependencies, then re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
