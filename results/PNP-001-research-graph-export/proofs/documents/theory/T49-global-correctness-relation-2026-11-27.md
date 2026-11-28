# T49 — The global correctness relation of a hypothetical solver (PI, 2026-11-27)

Status: CLAIMED (Claude family only); cross-family review pending. This document works backwards from the proof goal, as the owner directed on 2026-11-27.
It introduces no new structure measures and no enumeration, and it does not reopen Q-BD, T27 or streaming.
Prerequisites: T48 §3 (cancellation dichotomy), §9 (certificate transfer), 17590 (AW world), 17920/17929 (Σ3, K criterion).

## 1. Setting
L ∈ {3COL, SAT}. R(G,x) is the verifier. For 3COL it is the colouring check behind U_G: R(G,σ) = 1 iff σ is a proper colouring.
R is arithmetized as a polynomial of size poly(|G|). A is a hypothetical poly-time decider for L.

## 2. Lemma 1 (the one-sided identity is vacuous)
The owner's identity R(G,x)(1 − A(G)) = 0 says only "R = 1 ⇒ A = 1". It is satisfied by A ≡ 1.
Every constraint on A therefore needs the second direction as well: A(G) = 1 ⇒ ∃x R(G,x) = 1. ∎

## 3. Lemma 2 (Skolem normal form of correctness)
Assume P = NP. By self-reducibility there is a poly-time W with A(G) = R(G, W(G)). Correctness of A is then equivalent to the single Boolean identity
  (*)  Φ_W(G,x) := R(G,x)·(1 − R(G, W(G))) = 0   for all Boolean (G,x).
*Proof.*
- ⇒: if R(G,x) = 1, then G ∈ L, so W(G) is a witness and R(G, W(G)) = 1.
- ⇐: set A(G) := R(G, W(G)). If A(G) = 1, a witness exists. If G ∈ L with witness x, (*) gives A(G) = 1. ∎

Remark. "There is a uniform poly-time W with (*)" ⇔ P = NP. "There are poly-size circuits W_n with (*)" ⇔ NP ⊆ P/poly.
So (*) is an equivalent formulation and is not presented as a solution. It is the exact normal form of the "global relation between all
solutions and one computation" that the owner asked about.

## 4. Lemma 3 (correctness is never a formal identity)
Over every field F and for every polynomial map W, Φ_W ≠ 0 in F[G,x].
*Proof.* F[G,x] is an integral domain and R ≠ 0. Take any Boolean G ∉ L. Then R(G, W(G)) = 0 there, so 1 − R(G, W(G)) is not the zero polynomial.
A product of two nonzero polynomials is nonzero. ∎
Consequence (with T48 §3 and §9):
- Every correct W satisfies Φ_W ∈ I \ {0}, where I is the Boolean ideal. Correctness is necessarily Boolean cancellation, never formal cancellation.
- Checking (*) for a given circuit W is coNP-complete (T48 Thm 3b).
- The IPS certificate size of (*) equals, up to an additive O(s), that of the gate system of Φ_W and of its Lemma-B/GF(3) images (T48 9.3/9.4).
- Whether short certificates exist is not forced by P = NP (T48 9.5c).

## 5. Lemma 4 (what P = NP forces about (*), and the barrier test)
Let K be a property derived from P = NP via (*) that uses W only as a black box (inputs and outputs) and R only through its low-degree extension.
Then K holds in the AW world (17590): there NP^Ã = P^A, and W^A satisfies (*) relative to the oracle. Such a K is algebrizing and cannot give a contradiction.
A contradiction therefore needs a white-box property Π of all poly-size circuits W satisfying (*), such that:
- (i) Π is derived using the internal structure of W, not only its input-output behaviour;
- (ii) ¬Π is proved unconditionally.

Because (*) is equivalent to NP ⊆ P/poly (nonuniform version), every such argument proves NP ⊄ P/poly at the same time.
In other words, it is a circuit lower bound for SAT/3COL witness functions, obtained as a consequence and not used as a premise.
The forced polynomial identity NF(R(G, W(G))) = NF(χ_L) yields nothing beyond this: χ_L is the indicator of L, and its multilinear form
is fixed by Möbius inversion. Any property of circuits that compute it is again such a lower bound.

## 6. The first unproved implication (sharpened; not a small step)
There is no known white-box law of the form "W is a poly-size circuit with (*) ⇒ Π(W)" with ¬Π proved.
All tools of PNP-001 give only one of the following:
- black-box or low-degree consequences, which are algebrizing (Lemma 4);
- statements about restricted algorithm or proof classes (T48 Thm 4, IPS);
- statements that remain true under P = NP (Williams, T48 Prop 5.2).

This is the same gap as in 17920/17929. Here it is in its most exact form: a white-box property of all correct witness circuits.

## 7. External Lean proof (OAI, build running; first look only, no verdict)
- The top-level theorem `vp_ne_vnp` reduces to `separation_lower_bound`. That theorem states: for every C and every characteristic q,
  n^C < circuitSize(P n) for large n, over every field of characteristic q.
- Its proof goes through `FixedProgramDiagonal.uniform_of_pair_compilers` (FixedCompressedPairDiagonal.lean). Judging by the names, this is a
  **diagonal argument**: a fixed interpreter program ("CompressorReader", "evaluator tail", "address multiplier") over algebraically closed
  countable fields. It is aimed at all circuits of size n^C, with a length threshold chosen per exponent and characteristic.
- This is only a reading of file and theorem names. The mechanism will be extracted only after the build has finished and `#print axioms` has been
  checked. Note: the build pulls in the package `iut`, and it has local changes; it must be checked that VPVNP does not depend on it.
- Question to settle after verification:
  - The algebraic diagonal claims superpolynomial bounds for ONE explicit family. That goes beyond Kannan-type n^k bounds.
  - Does the same mechanism carry over to the white-box form (*), i.e. to Boolean witness circuits W of fixed size n^C?
  - This is a mechanism question, not a result transfer. The result transfer VP≠VNP → P≠NP remains closed.
