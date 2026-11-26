# Synthesis SYN-cc1f3a285f6b

## synthesis_id

SYN-cc1f3a285f6b

## original_ids

["Q-0332cb0a65:S0056"]

## mathematical_domain

binary matroids

## title

Single-row owners: minimal spanning sets equal port circuits

## mathematical_statement

For affine rows r_1..r_m (right-hand side included) over GF(2) and target e != 0: the minimal nonempty S with e in span(r_S) and e not in span(r_{S minus j}) for each j in S are exactly the circuits through e of the binary matroid on {e, r_1..r_m}, i.e. its port at e.

## formula_latex

\mathrm{Port}_e(M)

## assumptions

["single-row owners", "e≠0"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: Single-row owners over GF(2): for affine rows r_1..r_m (rhs bit included) and target e != 0, the minimal nonempty S with e in span(r_S) and e not in span(r_{S\{j}}) for all j in S are exactly the circuits through e of the binary matroid on {e, r_1..r_m}, i.e. its port at e.
evidence: Proof: a set T containing e is a circuit iff it is minimal dependent. For T = {e} u r_S, dependence means e in span(r_S), since e != 0 rules out the empty combination. Removing e leaves r_S, which is independent iff no proper subset of S already spans the same rank. Removing r_j leaves {e} u r_{S\{j}}, which is independent iff e not in span(r_{S\{j}}). These are exactly the conditions defining S, so the match is exact. Scope: single-row owners only. This is a standard matroid fact and closes no obligation. G0001 (shared auxiliaries with multi-row owners) remains open: the multi-row counterexample cm-9c543476bd7541c7, verified by cm-0c33bf85caa544f4, shows the port property fails for 2-row owners sharing z. Needs review by a session from a different model family.

## reconstructed_proof

[{"statement": "A set containing e is a circuit iff it is minimal dependent.", "justification": "definition of circuit", "passage": "a set T containing e is a circuit iff it is minimal dependent"}, {"statement": "Dependence of {e} union r_S is equivalent to e in span(r_S).", "justification": "e≠0 rules out the empty combination", "passage": "since e != 0 rules out the empty combination"}, {"statement": "Independence conditions match the defining conditions.", "justification": "direct check of removing r_j", "passage": "Removing r_j leaves {e} u r_{S\\{j}}, which is independent iff e not in span(r_{S\\{j}})"}]

## required_theorems

[]

## established_dependencies

[]

## missing_dependencies

[{"needs_validation": "Multi-row owners sharing z remain open (G0001), per the record."}]

## required_transfers

[]

## established_transfers

[]

## alternative_derivations

[]

## existing_validations

[{"validation_id": "PS:Q-0332cb0a65#82", "node_id": "Q-0332cb0a65:S0056", "reviewer": "pnp-desk/research/R1963", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-0332cb0a65#82", "node_id": "Q-0332cb0a65:S0056", "reviewer": "pnp-desk/research/R1963", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[{"needs_validation": "Multi-row owners sharing z remain open (G0001), per the record."}]

## required_recomputations

[]

## counterexamples

[{"role": "COUNTEREXAMPLE", "necessary_for_inference": false, "what": "multi-row counterexample verified by a second run", "inputs": "not stated", "result": "shows the port property fails for 2-row owners sharing z", "verification_conditions": null, "reproducibility": "cm-9c543476bd7541c7; cm-0c33bf85caa544f4", "passage": "the multi-row counterexample cm-9c543476bd7541c7, verified by cm-0c33bf85caa544f4, shows the port property fails for 2-row owners sharing z."}]

## first_invalid_inference



## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The text states it is a standard matroid fact that closes no obligation and does not address shared multi-row owners.

## source_references

{"question_id": "Q-0332cb0a65", "session": "pnp-desk/research/R1703", "origin_event_ids": ["692c39c83b83d6bedd054ea163fa1dc8b47983c613736a54c4c216f7c4b8a31b"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

supply the missing arguments/dependencies, then re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
