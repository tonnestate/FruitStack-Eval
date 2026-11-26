# Synthesis SYN-bf8ede9690e2

## synthesis_id

SYN-bf8ede9690e2

## original_ids

["Q-0332cb0a65:S0101"]

## mathematical_domain

finite CSP families; MUS clutters

## title

Pinning partition of substituted MUSs

## mathematical_statement

Let H be a finite constraint family, u the unit constraint x_j = c not in H, and H' obtained by substituting x_j = c in every constraint of H. For each S subset of H write S' for its substituted family. Then MUS(H') is the disjoint union of (I) those S in MUS(H) for which S' remains minimally inconsistent, and (II) those S for which S is satisfiable before pinning and S union {u} is an MUS of H union {u}. This corrects S0100.

## formula_latex

\mathrm{MUS}(H') = \mathrm{I} \sqcup \mathrm{II}

## assumptions

["u is a unit constraint x_j=c not in H"]

## proof_status

CLAIMED

## validation_status

NOT_REVIEWED

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: LEMMA (pinning partitions substituted MUSs by prior inconsistency). Let H be any finite constraint family, let u be a unit constraint x_j=c not in H, and let H' be obtained by substituting x_j=c in every constraint of H. For each S subseteq H, write S' for its substituted family. Then MUS(H') is the disjoint union of (I) those S in MUS(H) for which S' remains minimally inconsistent, and (II) those S for which S is satisfiable before pinning and S union {u} is an MUS of H union {u}. Proof: Take S in MUS(H'). If S is inconsistent before pinning, it remains inconsistent after pinning. Every proper T subset S is consistent after pinning by minimality, hence consistent before pinning, since an inconsistent family remains inconsistent under restriction. Thus S is in MUS(H), and belongs to class I. If S is consistent before pinning, S union {u} is inconsistent because its solutions are exactly the solutions of S' under the fixed value. Every proper subset of S union {u} is consistent: one omitting u is a subset of S; one containing u has form T union {u} for proper T subset S, and T' is consistent by minimality of S in H'. Thus S union {u} is an MUS, so S belongs to class II. Conversely, class I members are MUS after pinning by definition. For class II, inconsistency of S union {u} implies S' is inconsistent; every proper T subset S is consistent after pinning because T union {u} is a proper subset of the stated MUS. Hence S is an MUS of H'. The classes are disjoint by their pre-pinning consistency conditions. This corrects S0100: its unconditional identity fails when a substituted MUS was already inconsistent before pinning.

## reconstructed_proof

[{"statement": "Class I: inconsistent before pinning stays inconsistent after pinning.", "justification": "restriction preserves inconsistency", "passage": "If S is inconsistent before pinning, it remains inconsistent after pinning"}, {"statement": "Class II: consistent before pinning gives S union {u} as an MUS.", "justification": "solutions of S union {u} are the solutions of S' under the fixed value", "passage": "If S is consistent before pinning, S union {u} is inconsistent because its solutions are exactly the solutions of S' under the fixed value"}, {"statement": "The two classes are disjoint.", "justification": "pre-pinning consistency conditions differ", "passage": "The classes are disjoint by their pre-pinning consistency conditions."}]

## required_theorems

[]

## established_dependencies

[]

## missing_dependencies

[{"needs_validation": "Record corrects S0100; the proof of class II covering all proper subsets is a sketch and should be checked."}]

## required_transfers

[]

## established_transfers

[]

## alternative_derivations

[]

## existing_validations

[]

## independent_validations

[]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[{"needs_validation": "Record corrects S0100; the proof of class II covering all proper subsets is a sketch and should be checked."}]

## required_recomputations

[]

## counterexamples

[]

## first_invalid_inference



## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The text states only that it corrects S0100 and names no route obligation.

## source_references

{"question_id": "Q-0332cb0a65", "session": "pnp-desk/research/R2959", "origin_event_ids": ["df9fede54a5fa61ead525b385e46d7cd3243d1c4e00a3e82d34b1bbd4c2ee97e"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

supply the missing arguments/dependencies, then independent re-review with the full statement

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
