# Streaming lane (Q-156fa9c912): Lambda_S framework, Satz A/B, Lemma 1/2 - check by Claude Code 2026-11-21 (owner request, HIGH PRIO)
Level: verified mathematics (elementary); no P != NP claim; every result below RELATIVISES (owner's oracle counter-check) unless noted.

## Corrected framework Lambda_S (owner corrections adopted)
One-pass algorithm on the truth table T in {0,1}^N, memory S bits, per-step update circuits F_t: {0,1}^S x {0,1} -> {0,1}^S (fan-in 2),
decoder Dec: {0,1}^S -> output. Redundancy: reachable codes R_t subset {0,1}^S with a SURJECTION pi_t: R_t -> Q_t (Nerode classes) and
pi_{t+1}(F_t(z,b)) = delta_t(pi_t(z), b). Lambda_S = min over such algorithms of sum_t CC(F_t) (+ CC(Dec) where stated). NON-UNIFORM
(constants may be hard-wired); MMW's model is uniform.
MMW model (checked in local mmw19/paper.txt lines 26-37, 118-124, 516-528): search-MCSP^A[s] must output a circuit OR REPORT THAT NONE
EXISTS (Algorithm 1 outputs 0^{100 s log s} on failure and reports) -> MMW is the TOTAL version (with bottom). Update time is per bit read;
the algorithm may work several steps before requesting the next bit (amortisation is part of the model). Output only at the end.

## Satz A (promise version, deferral) - CORRECT
Input promised in SC_s; S = 2 ceil(log2 |SC_s|) + 1. Random A in F2^{S x N}: Pr[A(x xor x') = 0] = 2^{-S} for x != x'; union bound over
< |SC_s|^2 pairs gives < 1/2, so some A is injective on SC_s. Update z <- z xor b*a_t (a_t hard-wired): <= S gates. Hence
Lambda_S^promise <= O(N S) + min_A CC(Dec_A). Consequence: in the promise version any lower bound on sum CC(F_t) is capped at O(N S);
hardness can only sit in the decoder. Non-uniform (a_t hard-wired) - does not transfer to MMW's uniform model, and MMW is total anyway.

## Satz B (total version) - CORRECT
At every t a correct algorithm maps distinct live prefixes to distinct classes and no dead prefix to a live prefix's class.
Proof: same state => same output on every continuation q. Live p, dead p' with p q in SC_s: output must be a circuit and bottom. Two live
p1 != p2: take q with p1 q in SC_s; output for p1 q is a circuit for p1 q, but p2 q is either in SC_s (needs a circuit for a different
table) or not (needs bottom) - contradiction either way. (The second case is needed; the owner's text states injectivity without it.)
Corollary - CORRECT, and stronger than stated: no algorithm has an affine (kernel-coset) state partition at any t > S (the condition
t > S + log2|SC_s| is not needed): cosets have >= 2^{t-S} >= 2 elements, but a class containing a live prefix is that prefix alone.
Encoding-invariant (statement about the partition). Not a hardness statement: Berlekamp-Massey-type non-affine updates stay cheap.

## Lemma 1 (counting) - CORRECT as stated, with the decoder counted
Algorithms with memory S, update sizes u_t and decoder size D compute at most 2^{O(D log D) + sum_t O((u_t+S) log(u_t+S))} functions,
independent of encoding/redundancy/buffering. The corollary max(S, mean u) >= Omega(K) for almost all layered structures of width K
needs the count of non-isomorphic minimal layered automata (~ 2^{Theta(N K log K)}) - NOT written out, open. Relativises; M_s is
succinctly described, so Lemma 1 says nothing about MCSP.

## Lemma 2 (cell-probe ceiling) - CORRECT (trivial)
Read all S/w cells, compute for free, write all: O(S/w) = O~(s)/w probes per update (S = O~(s) by MMW). No information-transfer /
cell-probe argument gives more.

## Conjectures and open steps (NOT claimed)
- QE*: no encoding (redundant, free) with poly(s) memory admits poly(s)-size fan-in-2 updates for Search-MCSP[s].
- QE(2,3): s = n^c, c >= 2: no one-pass algorithm with S <= s^2 and sum u_t <= N s^3 (fan-in-2 F_t and decoder) solves Search-MCSP[s].
  Weaker than QE*; does NOT meet the MMW transfer. Refuter: an exact online learner for size-s circuits (would break PRFs via the
  learning / natural-proofs connection - Kabanets-Cai context; check exact reference).
- Open step P: a property of layered structures with (1) M_s has P, (2) no (s^2, N s^3) fan-in-2 structure has P, (3) the proof of (2)
  fails once local Sigma_3 gates of fan-in O~(s) are allowed (non-relativising, non-localising requirement).
- Owner-supplied, not checked here: Patrascu-Demaine information-transfer state of the art Omega(lg^1.5 n) for dynamic Boolean
  problems; synaptic cascade model; MMW Algorithm 1 block size 100 s log s, Sigma_3 complexity of Circuit-Min-Merge, O~(s^2) update time.
