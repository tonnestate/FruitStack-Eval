# Synthesis SYN-67085de2dca9

## synthesis_id

SYN-67085de2dca9

## original_ids

["Q-156fa9c912:S0527"]

## mathematical_domain

streaming complexity

## title

Fixed-depth residual distinguishability for finite word families

## mathematical_statement

Let L be a finite set of binary words of common length N, and let p and q be words of the same length t. Define R_p={z in {0,1}^(N-t): pz in L} and R_q analogously. In every deterministic automaton accepting exactly L, if R_p != R_q then the states reached after p and q are distinct. Consequently the number of states reached by length-t prefixes is at least the number of distinct residual sets R_p at that depth. This applies to EXT for any finite family of equal-length truth tables; it is an information-state lower bound only.

## formula_latex

\#states_t \ge |\{R_p : |p|=t\}|

## assumptions

["the automaton accepts exactly L and is deterministic"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: LEMMA (residual distinguishability at a fixed depth). Let L be a finite set of binary words, and let p and q be words of the same length t. Define R_p={z in {0,1}^{*: |z|=N-t and pz in L}, where N is the common word length of L}; define R_q analogously. In every deterministic automaton that accepts exactly L, if R_p != R_q then the states reached after p and q are distinct. Proof: Since the sets differ, choose z in their symmetric difference. Then exactly one of pz and qz belongs to L. If p and q reached the same state, determinism would make the automaton's result after reading the common suffix z identical from both states, contradicting that exactly one word is accepted. Consequently, the number of states reached by length-t prefixes is at least the number of distinct residual sets R_p at that depth. This applies to EXT for any finite family of equal-length truth tables, with L equal to that family. It gives an information-state lower bound only; it does not bound transition gate cost or connect EXT to arbitrary MCSP decision circuits.
evidence: Direct proof by symmetric-difference suffix: unequal residual sets provide a suffix accepted after exactly one of the two equal-length prefixes. Determinism forces identical continuations from a shared state, so those prefixes cannot share a state.
closes: Q-156fa9c912

## reconstructed_proof

[{"statement": "choose z in the symmetric difference; exactly one of pz and qz is in L", "justification": "set difference", "passage": "Then exactly one of pz and qz belongs to L."}, {"statement": "determinism gives identical results from the same state on the common suffix z", "justification": "determinism", "passage": "determinism would make the automaton's result after reading the common suffix z identical from both states"}]

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

[{"validation_id": "PS:Q-156fa9c912#655", "node_id": "Q-156fa9c912:S0527", "reviewer": "pnp-desk/research/R2844", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-156fa9c912#655", "node_id": "Q-156fa9c912:S0527", "reviewer": "pnp-desk/research/R2844", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

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

CONNECTION_NOT_IDENTIFIED | The record lists closes: Q-156fa9c912, a question id rather than a route obligation, and states it does not connect EXT to arbitrary MCSP decision circuits.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2532", "origin_event_ids": ["4a9c7cf2f59c7d3cb13798feb142631660fd7ca63b0bdda9fe6e4a8014c4f618"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

independent re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
