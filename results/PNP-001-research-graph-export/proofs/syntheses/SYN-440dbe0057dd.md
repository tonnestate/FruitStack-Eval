# Synthesis SYN-440dbe0057dd

## synthesis_id

SYN-440dbe0057dd

## original_ids

["Q-0332cb0a65:S0100"]

## mathematical_domain

finite CSP families; MUS clutters

## title

Unit pinning selects MUSs containing the pinned constraint

## mathematical_statement

Let F be a finite constraint family, u the unit constraint x_j = c, and F' obtained from F minus {u} by substituting x_j = c. Then MUS(F') = {M minus {u} : M in MUS(F), u in M}.

## formula_latex

\mathrm{MUS}(F') = \{M \setminus \{u\} : M \in \mathrm{MUS}(F),\ u \in M\}

## assumptions

["u is the unit constraint x_j=c"]

## proof_status

CLAIMED

## validation_status

REFUTED_BY_DEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: LEMMA (unit pinning selects MUSs containing the pinned constraint). Let F be a finite constraint family, let u be the unit constraint x_j=c, and let F' be obtained from F\{u} by substituting x_j=c. Then MUS(F') = {M\{u}: M in MUS(F), u in M}. Proof: for every S subset F\{u}, S is inconsistent in F' iff S union {u} is inconsistent in F. If S is minimally inconsistent in F', every proper T subset S is consistent in F'; moreover S is consistent in F, since otherwise S union {u} would not be minimal. Thus S union {u} is an MUS of F containing u. Conversely, if M is an MUS of F containing u, then S=M\{u} is inconsistent in F'; every proper T subset S is consistent in F because T union {u} is a proper subset of M, hence consistent; therefore T is consistent after substitution, so S is an MUS of F'. This identity does not assert that substituted MUSs correspond to all MUSs of F or that the selected family is a matroid minor port.

## reconstructed_proof

[{"statement": "Forward inclusion: S in MUS(F') gives S union {u} in MUS(F).", "justification": "S consistent in F is asserted, justified by minimality of S union {u}", "passage": "moreover S is consistent in F, since otherwise S union {u} would not be minimal"}, {"statement": "Converse inclusion.", "justification": "minimality of S in F' from consistency of T union {u}", "passage": "every proper T subset S is consistent in F because T union {u} is a proper subset of M, hence consistent"}]

## required_theorems

[]

## established_dependencies

[]

## missing_dependencies

[{"needs_validation": "The forward step presupposes that S union {u} is an MUS of F, which is not established; the case where S is already inconsistent in F is not handled. Companion record S0101 corrects this identity."}, {"needs_validation": "Record carries 'closes: G0001'; scope is limited to unit pins."}, {"unsupported_assertion": "S is consistent in F, since otherwise S union {u} would not be minimal"}]

## required_transfers

[]

## established_transfers

[]

## alternative_derivations

[]

## existing_validations

[{"validation_id": "PS:Q-0332cb0a65#101", "node_id": "Q-0332cb0a65:S0100", "reviewer": "pnp-desk/research/R2963", "model": "gpt-6-luna", "model_family": "gpt", "method": "AGENT_REVIEW", "result": "REFUTED", "independent": false, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[{"needs_validation": "The forward step presupposes that S union {u} is an MUS of F, which is not established; the case where S is already inconsistent in F is not handled. Companion record S0101 corrects this identity."}, {"needs_validation": "Record carries 'closes: G0001'; scope is limited to unit pins."}]

## required_recomputations

[]

## counterexamples

[{"validation_id": "PS:Q-0332cb0a65#101", "node_id": "Q-0332cb0a65:S0100", "reviewer": "pnp-desk/research/R2963", "model": "gpt-6-luna", "model_family": "gpt", "method": "AGENT_REVIEW", "result": "REFUTED", "independent": false, "scope_status": "FULL_TEXT_RECEIVED"}]

## first_invalid_inference

PS:Q-0332cb0a65#101 REFUTED: Counterexample: take F={u:x=0, a:y=0, b:y=1}. After substituting x=0, {a,b} is an MUS, but it does not contain u and is not the result of deleting u from any MUS of F containing u. The claimed identity omits MUSs already present before pinning.

## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The text states the identity does not assert correspondence to all MUSs of F or that the family is a matroid minor port, and names no route obligation.

## source_references

{"question_id": "Q-0332cb0a65", "session": "pnp-desk/research/R2959", "origin_event_ids": ["f8bf00e3e6beccd933e78ed79a6458a94db04c0eb4848d9b9cd5a56565f81a30"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

supply the missing arguments/dependencies, then independent re-review with the full statement

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
