# Synthesis SYN-0fa5be11d1f4

## synthesis_id

SYN-0fa5be11d1f4

## original_ids

["Q-156fa9c912:S0475"]

## mathematical_domain

Boolean circuit complexity

## title

Logarithmic-tail completion circuit for an existential projection

## mathematical_statement

Let H:{0,1}^N->{0,1} be computed by a fan-in-two Boolean circuit of h gates, constants and wiring free. For a cut t=N-k define E_t(p)=1 iff there exists q in {0,1}^k with H(pq)=1. (1) E_t is computed by a fan-in-two circuit of at most 2^k(h+1)-1 gates. (2) If k<=c log_2(h+2) for a fixed constant c, E_t has size O((h+2)^(c+1)). (3) For h=poly(s) and k=O(log s), E_t has size poly(s). Scope: all N>=0, all circuits H on N inputs, all cuts t with k=N-t. No MCSP lower bound is claimed.

## formula_latex

size(E_t) <= 2^k (h+1) - 1; k <= c log_2(h+2) implies size(E_t) = O((h+2)^(c+1))

## assumptions

["H is computed by a fan-in-two Boolean circuit of h gates, constants and wiring free", "k<=c log_2(h+2) for a fixed constant c (for the O-bound)", "h=poly(s) and k=O(log s) (for the polynomial statement)"]

## proof_status

CLAIMED

## validation_status

SURVIVED_INDEPENDENT_REVIEW

## evaluation_status

EXTRACTED_AND_CLASSIFIED; semantic extraction not independently verified

## original_proof

proved_step: statement: LOGARITHMIC-TAIL COMPLETION LEMMA. Let H:{0,1}^N->{0,1} be computed by a fan-in-two Boolean circuit of h gates, where constants and wiring are free. For a cut t=N-k, define E_t(p)=1 iff there exists q in {0,1}^k with H(pq)=1. Then E_t is computed by a fan-in-two circuit of at most 2^k(h+1)-1 gates. Consequently, if k<=c log_2(h+2) for a fixed constant c, E_t has size O((h+2)^(c+1)); in particular, for h=poly(s) it has size poly(s) whenever the unprocessed suffix length is O(log s). Proof: For each of the 2^k strings q, take a disjoint copy H_q of H with its first N-k inputs wired to p and its last k inputs fixed to q. OR the 2^k outputs using a binary OR tree, which uses 2^k-1 gates. H_q(p)=H(pq), so the OR computes E_t. The total gate count is 2^k h+(2^k-1)=2^k(h+1)-1. If k<=c log_2(h+2), then 2^k<=(h+2)^c, yielding size <=(h+2)^c(h+1)=O((h+2)^(c+1)). If h is polynomially bounded in s and k=O(log s), this is polynomial in s. This only constructs the completion predicate at cuts with logarithmic remaining suffix; it gives no poly(s) bound for early cuts, no update implementation for the full EXT automaton, and no implication for arbitrary MCSP circuits beyond their decision-circuit size h.
scope: All N>=0, all Boolean circuits H on N inputs, all cuts t with k=N-t, fan-in-two gate count with constants/wiring free. The polynomial consequence assumes the stated asymptotic bounds; no MCSP lower bound is claimed.

## reconstructed_proof

[{"statement": "2^k disjoint copies H_q of H with first N-k inputs wired to p and last k inputs fixed to q", "justification": "H_q(p)=H(pq)", "passage": "take a disjoint copy H_q of H with its first N-k inputs wired to p"}, {"statement": "OR of 2^k outputs by a binary OR tree costs 2^k-1 gates, total 2^k(h+1)-1", "justification": "copy gates plus OR tree", "passage": "OR the 2^k outputs using a binary OR tree, which uses 2^k-1 gates"}, {"statement": "2^k<=(h+2)^c hence size O((h+2)^(c+1))", "justification": "exponent comparison", "passage": "then 2^k<=(h+2)^c, yielding size <=(h+2)^c(h+1)=O((h+2)^(c+1))"}]

## required_theorems

[]

## established_dependencies

[]

## missing_dependencies

[{"needs_validation": "the poly(s) statement depends on the asymptotic hypotheses h=poly(s) and k=O(log s), which the text states but does not verify for any concrete circuit"}]

## required_transfers

[]

## established_transfers

[]

## alternative_derivations

[]

## existing_validations

[{"validation_id": "PS:Q-156fa9c912#588", "node_id": "Q-156fa9c912:S0475", "reviewer": "pnp-desk/research/R2652", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## independent_validations

[{"validation_id": "PS:Q-156fa9c912#588", "node_id": "Q-156fa9c912:S0475", "reviewer": "pnp-desk/research/R2652", "model": "nemotron-3-ultra-550b-a55b", "model_family": "nemotron", "method": "AGENT_REVIEW", "result": "SURVIVED_REVIEW", "independent": true, "scope_status": "FULL_TEXT_RECEIVED"}]

## formal_verification_status

NOT_FORMALIZED

## remaining_proof_obligations

[{"needs_validation": "the poly(s) statement depends on the asymptotic hypotheses h=poly(s) and k=O(log s), which the text states but does not verify for any concrete circuit"}]

## required_recomputations

[]

## counterexamples

[]

## first_invalid_inference



## agent_failures

[]

## target_relevance

CONNECTION_NOT_IDENTIFIED | The text states it gives no poly(s) bound for early cuts and no implication for arbitrary MCSP circuits beyond decision-circuit size h, so no route role is stated.

## source_references

{"question_id": "Q-156fa9c912", "session": "pnp-desk/research/R2412", "origin_event_ids": ["4ff92fd8c09023f5d9c86b4d94974c656e2567a26fd1a9c6873207e9a677653d"], "classifier": "haiku-syn-v1", "classifier_model": "claude-haiku-5-5"}

## required_next_operation

supply the missing arguments/dependencies, then re-review

## snapshot_id

PNP001-SYN-INTERIM-20261126-1
