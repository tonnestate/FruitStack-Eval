# Synthesis SYN-0cd3c828aaac

## synthesis_id

SYN-0cd3c828aaac

## original_ids

["Q-156fa9c912:S0505"]

## mathematical_domain

streaming complexity

## title

Explicit-family streaming update with live-candidate vector

## mathematical_statement

Let F=(C_1,...,C_d) be an explicitly listed family of Boolean circuits on n input bits, each with at most s fan-in-two gates. At stream position i, the live candidates are a vector a in {0,1}^d with a_j=1 iff C_j agrees with all previously read truth-table bits. On reading b, set a'_j=a_j AND (b iff C_j(i)=1) and increment i. This is exact by induction on the number of read bits. Each transition costs O(d(s+n)) fan-in-two gates including the index increment, so it is polynomial only when d, s, n are polynomially bounded; no polynomial bound is given when d is the full circuit-description count. A finite discovery check (cm-69dd62ee713f4a79) corroborates the identity but is not the proof.

## formula_latex

a'_j = a_j \wedge (b \leftrightarrow C_j(i))

## assumptions

["the family is explicitly listed", "each C_j has at most s fan-in-two gates"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: LEMMA (explicit-family streaming update). Let F=(C_1,...,C_d) be an explicitly listed family of Boolean circuits on n input bits, each with at most s fan-in-two gates. At stream position i, represent the live candidates by a vector a in {0,1}^d, where a_j=1 iff C_j agrees with all previously read truth-table bits. On reading b, set a'_j=a_j AND (b iff C_j(i)=1), and increment i. This is exact: by induction on the number of read bits, a'_j=1 exactly when C_j agrees with the entire extended prefix. A transition can be implemented by evaluating each C_j on the binary encoding of i and ANDing its equality-to-b test with a_j; with straightforward fan-in-two circuitry this costs O(d(s+n)) gates, including the index increment. Thus explicit candidate tracking is polynomial when d,s,n are polynomially bounded, but the lemma gives no polynomial bound when d is the full circuit-description count.
evidence: Independent proof by induction over stream positions. Finite DISCOVERY check cm-69dd62ee713f4a79 tested all 256 families of three-input Boolean functions and all prefixes (130,816 cases); it matched the predicted identity. This computation is corroboration only, not the general proof.

## reconstructed_proof

[{"statement": "the update a'_j = a_j AND (b iff C_j(i)=1) is exact", "justification": "induction on read bits", "passage": "by induction on the number of read bits, a'_j=1 exactly when C_j agrees with the entire extended prefix"}, {"statement": "cost O(d(s+n)) including the index increment", "justification": "fan-in-two circuitry", "passage": "with straightforward fan-in-two circuitry this costs O(d(s+n)) gates, including the index increment"}]

## required_theorems

[]

## established_dependencies

[]

## missing_dependencies

[{"needs_validation": "the polynomial-time statement requires d, s, n polynomially bounded, as the text notes"}]

## required_transfers

[]

## established_transfers

[]

## alternative_derivations

[]

## existing_validations

[{"validation_id": "PS:Q-156fa9c912#616", "node_id": "Q-156fa9c912:S0505", "reviewer": "pnp-desk/research/R2684", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-156fa9c912#616", "node_id": "Q-156fa9c912:S0505", "reviewer": "pnp-desk/research/R2684", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[{"needs_validation": "the polynomial-time statement requires d, s, n polynomially bounded, as the text notes"}]

## required_recomputations

[]

## counterexamples

[]

## first_invalid_inference



## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The text states polynomiality only for polynomially bounded d and no route role for the target.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2484", "origin_event_ids": ["18eb61866428a83e42c3748b777c5917bf812f4739e9406b6a8e27a35ee90fbd"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

supply the missing arguments/dependencies, then re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
