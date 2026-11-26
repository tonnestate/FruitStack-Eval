# QE* candidate proof driven to its first false line (director, 2026-11-21, owner request)
Model: Gamma_S (proof state Q-156fa9c912): exact deterministic one-pass algorithm for TOTAL search-MCSP^A[s], arbitrary state maps
sigma_t: {0,1}^t -> {0,1}^S, sigma_{t+1}(pb) = F_t(sigma_t(p), b), decoder D_N; target: max_t CC(F_t) and CC(D_N) not both <= poly(s)
when S = poly(s). P_t = live prefixes (extendable to the truth table of some admissible size-s circuit), |P_t| <= 2^{O(s log s)}.

## The candidate (the QE* intuition "the quantifier over the forgotten past must be eliminated at every step")
C1  Gamma_S covers every correct algorithm (S0036).                                                        TRUE (registered, CLAIMED)
C2  Satz B: sigma_t is injective on P_t and sigma_t(dead) is disjoint from sigma_t(P_t).                    TRUE (S0010, SURVIVED_REVIEW)
C3  Put L_t := sigma_t(P_t) subset {0,1}^S. Then p is live iff sigma_t(p) in L_t, and T in SC_s iff sigma_N(T) in L_N.  TRUE (definitional + C2)
C4  D_N outputs bottom exactly on codes outside L_N, so D_N decides membership in L_N.                       TRUE
C5  "Hence at every t the algorithm decides membership in L_t, i.e. the update F_t decides whether pb is live (prefix-extension
     MCSP, a Sigma_2-type search over consistent circuits)."                                                 *** FIRST FALSE LINE ***
C6  "Prefix-extension liveness needs super-polynomial circuits, so CC(F_t) is super-polynomial."             (rests on C5; and is itself
     an NP-hardness-type lower bound, i.e. as hard as the target)

## Why C5 is false
(a) The model requires a decision only at the end (C4). F_t must PRESERVE the partition {L_t, complement} (map live codes with a
    live extension into L_{t+1}, all others outside it), not COMPUTE it. Membership in L_t at an intermediate t is
    "exists continuation z with D_N(F(..F(code, z_1)..)) != bottom" - a search over 2^{N-t} continuations that no step is obliged to run.
(b) Explicit counter-witness to the underlying implication "a state that separates prefixes must decide/decode them":
    Satz A (S0009, SURVIVED_REVIEW). In the promise version the linear sketch z = A*T is injective on SC_s, each update costs <= S
    gates, and all hardness sits in the final decoder. Separation of prefixes by the state is achieved without any step deciding
    or decoding anything. (In the total version the sketch fails only because it cannot keep dead prefixes off L_t - Satz B corollary,
    S0011 - which kills AFFINE sketches, not cheap non-linear ones.)
(c) Neither does C4 give hardness: D_N acts on S = poly(s) bits, and the encoding may carry a liveness flag, so D_N can be trivial;
    the decision cost can be moved into the updates or the reverse. Only the COMPOSITION is constrained.

## What remains after removing C5 (the exact place where it hangs)
Unrolling (S0011 of Q-0b7da33369 / STATE-RECODING): the composition is a circuit for MCSP^A[s] on N bits of size
<= N * max_t CC(F_t) + CC(D_N) with online cut-width <= S. So the candidate reduces to:
  MISSING LEMMA M (total-version separating compression): for some s, A in PH and all c, d, there is no family of maps sigma_t with
  S <= s^c bits, updates of size <= s^d, that keeps live and dead prefixes of SC_s apart at every t (equivalently: MCSP^A[s] has no
  circuit of size N * s^d and online cut-width s^c, for infinitely many n).
M is exactly the MMW magnification premise in circuit form - the candidate is circular after C5, not merely incomplete.
Status of M: OPEN. Known constraints on any proof of M: affine sigma_t are excluded (S0011) - so M is about NON-LINEAR cheap
separating compressions; the oracle-gate analogue of M is false (MMW Thm 1.2 / 4.1), so a proof must break at fan-in-O~(s) Sigma_3^A
gates (non-localising); pure counting / information / one-way communication cannot prove M (S0038, Lemma 1/2: poly space suffices).
Next concrete question (smallest test of M): is there a cheap NON-linear separating compression for a toy class in place of SC_s
(e.g. truth tables of small read-once formulas or small decision trees)? A cheap one there refutes the naive generalisation of
"separation forces work"; a proof there would be the first instance of the needed mechanism.

## Barrier audit of Missing Lemma M (owner-supplied grid, 2026-11-21; diagnostic, per the PNP-001 barrier rule)
- Relativisation: M's oracle-gate analogue is FALSE (MMW Thm 1.2/4.1) -> a proof of M must use circuit semantics; any argument that
  treats the per-step maps as black boxes fails. Status: requirement known, no mechanism.
- Locality: M is itself phrased with an ordered cut (online cut-width). The MMW oracle algorithm ALSO has cut-width O~(s) and poly(s)
  per-step size once Sigma_3^A gates of fan-in O~(s) are allowed. Precise test: the proof must contain a step that is false for
  per-step circuits with such gates. Correction to the grid: the distinguishing feature is NOT unbounded fan-out (oracle circuits have
  fan-out too) but the small-fan-in oracle gate; and a localising proof would contradict the known MMW upper bound (not "prove
  EXP not in NC^1"). Status: no candidate step known that fails exactly at oracle gates.
- Natural proofs: the property "f has no size N*s^d, cut-width s^c circuit" holds for random f (large) but is not known to be
  constructive (deciding it is itself a circuit-minimisation question for that model), so Razborov-Rudich does not directly apply;
  the grid's demand "do not apply to random functions" is a heuristic, not a theorem. Status: diagnostic only.
- C5 (first false line) fails before any barrier is reached: it is a logical error (preserve vs compute), not a barrier issue.
