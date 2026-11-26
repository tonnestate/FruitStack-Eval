# Synthesis SYN-482a8c4e7fa6

## synthesis_id

SYN-482a8c4e7fa6

## original_ids

["Q-156fa9c912:S0517"]

## mathematical_domain

formal languages / streaming complexity

## title

Right-residual characterization of minimal state count

## mathematical_statement

Let A be a finite set of binary strings of common length N, L=Pref(A), and for each prefix p let L_p={u: pu in L}. (1) In any deterministic streaming automaton recognizing L, prefixes p and q reaching the same state satisfy L_p=L_q. (2) The distinct sets L_p form the states of a deterministic automaton recognizing L, with transition from L_p on bit b to L_{pb}; the empty residual is a rejecting sink. (3) Hence the minimum number of states equals the number of distinct right residuals among prefixes, including the empty residual if it occurs.

## formula_latex

\min |Q| = |\{L_p : p \text{ prefix}\}|

## assumptions

["L = Pref(A)"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: LEMMA (right-residual state characterization). Let A be a finite set of binary strings of common length N, let L=Pref(A), and for each prefix p let L_p={u: pu is in L}. In any deterministic streaming automaton recognizing L, prefixes p and q that reach the same state have L_p=L_q. Conversely, the distinct sets L_p form the states of a deterministic automaton recognizing L, with transition from L_p on bit b to L_{pb}; the empty residual is a rejecting sink. Thus the minimum number of states equals the number of distinct right residuals among prefixes, including the empty residual if it occurs.
derivation: If p and q reach the same deterministic state, every continuation u produces the same acceptance result after p and q. Since acceptance after p followed by u is exactly the predicate pu∈L, this implies L_p=L_q. Therefore prefixes with distinct residuals must reach distinct states. Conversely, define states to be the distinct residuals L_p and define δ(L_p,b)={u:bu∈L_p}. By definition this set is L_{pb}, so the transition is well-defined on residuals: if L_p=L_q, then {u:bu∈L_p}={u:bu∈L_q}. Declare a residual accepting iff it contains the empty string. Starting from L_ε, induction on the streamed prefix shows the current state is exactly L_p; hence the automaton recognizes L. The empty residual transitions to itself and is rejecting. The lower and upper bounds on the state count coincide.

## reconstructed_proof

[{"statement": "prefixes reaching the same state have equal right residuals", "justification": "continuation argument", "passage": "every continuation u produces the same acceptance result after p and q"}, {"statement": "residuals form a well-defined deterministic automaton, so the bounds coincide", "justification": "transition on residuals", "passage": "The lower and upper bounds on the state count coincide."}]

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

[{"validation_id": "PS:Q-156fa9c912#627", "node_id": "Q-156fa9c912:S0517", "reviewer": "pnp-desk/research/R2684", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-156fa9c912#627", "node_id": "Q-156fa9c912:S0517", "reviewer": "pnp-desk/research/R2684", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

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

CONNECTION_NOT_IDENTIFIED | The record is a self-standing characterization of prefix-language automata with no stated route role.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2500", "origin_event_ids": ["086dcbdfe3aae1b0af82e240a35488b7abce7ffff34c81888e19091527b0d741"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

independent re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
