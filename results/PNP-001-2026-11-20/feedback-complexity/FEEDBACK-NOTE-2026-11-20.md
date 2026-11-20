# PNP-001 research note — feedback / fly-by-wire principles vs. the MCSP reuse barrier (2026-11-20)

Status: two elementary lemmas with proofs (independent review: see section 6), one literature pointer. Strongest finding is NEGATIVE:
stability and bounded control impose no restriction on circuits, and observability-type bounds are capped at O(s log(n+s)) bits of
memory, so none of them can deliver either open target of PNP-001 (R-MCSP, or the MMW19 Thm 1.3 streaming bound).

## 1 Formalization
A (synchronous, time-varying) feedback system over {0,1}: state x_t in {0,1}^w, input u (the truth table or a stream of its bits),
update x_{t+1} = F_t(x_t, u), output y = G(x_T). Its unrolling is the circuit Unroll = F_0, F_1, ..., F_{T-1}, G composed; size
= sum_t size(F_t) + size(G). State reuse = a state bit read by several later gates; in the unrolling these are exactly gates with
fan-out > 1 (the parameter r of the reuse route, report sec. 20).
Conversely every circuit C of size S is such a system: order the gates topologically g_1..g_S, let x_t hold the values of g_1..g_t
(w = S bits, or registers reused after their last read), F_t computes g_t from x_t and u and copies the rest. Unroll(F) = C.
Streaming (one-pass) = time-invariant F reading one input bit per step; state count = 2^w.

## 2 Lemma FB1 (stability is free)
Every Boolean circuit C of size S is the unrolling of a time-varying feedback system that reaches a fixed point after S steps and has the
strict Lyapunov function V(x_t, t) = S - t (strictly decreasing until the fixed point, constant afterwards), with Unroll = C, i.e.
zero size overhead and no change of r. (V depends on the step, not on the state: a Lyapunov function in a vacuous sense - which is the
point.) A time-invariant realization needs a ceil(log2(S+1))-bit counter and V = S - counter, but its single update map must decode the
counter, contain all S gate evaluations (or a multiplexer over them) and a conditional write on every state bit: size(F) = Theta(S),
unrolled Theta(S^2), and r changes (every step re-reads every state bit). Only the time-varying statement is overhead-free; it reads all
of u at every step, so it is not a one-pass streaming system.
Proof. The realization of section 1: step t evaluates g_t and leaves every other bit unchanged; after step S nothing changes (F_t =
identity for t >= S), so x_S is a fixed point reached in S steps; V decreases by exactly 1 per step before it. The unrolled circuit
consists of the S gate evaluations; the "unchanged" bits are wires, not gates. QED.
Also "bounded control effort": this realization changes at most one state bit per step, the smallest possible nonzero effort.
Consequence. "C admits a stable / Lyapunov / bounded-effort realization" holds for EVERY circuit. Any lower bound of the form
"stable realizations of f need size X" is a lower bound for all circuits for f - nothing is gained, and the control vocabulary cannot
separate MCSP from parity or inner product (it is satisfied by their linear-size circuits too, R1/R1').

## 3 Lemma FB2 (observability ceiling)
For the language L = MCSP[s] on truth tables of length N = 2^n, read one bit per step (one pass), let I_t = number of Myhill-Nerode
classes of length-t prefixes (prefixes p ~ q iff p·z in L <=> q·z in L for every completion z of length N - t); I_t is the minimum number of
distinguishable ("observable") states any one-pass decider needs after t bits. Then
  I_t <= 1 + |{ tt(C)_{1..t} : C circuit of size <= s on n inputs }| <= 1 + 2^{O(s log(n+s))},
so state-distinguishability (observability / Nerode) arguments give at most a memory lower bound of log2 I_t = O(s log(n+s)) bits.
Proof. Two prefixes that are not a prefix of any positive truth table both have the empty completion set: one class. Two equal
prefixes are the same prefix. Hence every class is either the dead class or contains a prefix of some tt(C) with size(C) <= s, so I_t is
at most 1 + the number of distinct such prefixes, which is at most |Im(Eval_{n,s})| <= number of circuits of size <= s =
2^{O(s log(n+s))}. QED.
Consequence for the streaming route. MMW19 Thm 1.3 needs: no one-pass algorithm with poly(s) space AND poly(s) update time. Space
O(s log(n+s)) is poly(s) and is achievable WITHOUT any oracle: keep as state one size-<=s circuit consistent with the prefix; when a new bit
disagrees, search (brute force) for the next circuit consistent with the old circuit's first t bits and the new bit - O(s log(n+s))
space, exponential update time (MMW19 Thm 1.2 brings the update to O~(s^2) with a Sigma3SAT^A oracle). So no argument based on how many states
must be distinguished can establish the hypothesis; any successful argument must bound the update time (the transition computation),
which is exactly where the oracle locality barrier sits (filter F2; report sec. 20, connection test EXT vs H_C).

## 4 Comparison with known theory
- Branching programs: a width-W, length-T BP is a time-varying feedback system with log W state bits; the best explicit SIZE bounds for
  general BPs are about n^2/log^2 n (Neciporuk 1966) - known to be the ceiling of counting-subfunction methods; feedback vocabulary adds nothing.
- Straight-line programs / pebbling: state reuse = register reuse; every bounded fan-in circuit of size S can be pebbled with
  O(S/log S) pebbles (Hopcroft-Paul-Valiant 1977), tight (Paul-Tarjan-Celoni 1977) - but only with recomputation (exponential time), so the
  program is no longer the same circuit. Small state is available at a time cost; bounded state does not bound reuse at fixed size.
- Noise and redundancy (the genuine fly-by-wire principle: triple modular redundancy, voting): for circuits with independently noisy
  gates, reliable computation of sensitivity-n functions at constant noise needs size Omega(n log n) (Dobrushin-Ortyukov 1977; gap found
  by Pippenger-Stamoulis-Tsitsiklis 1991; corrected proofs Reischuk-Schmeltz 1991, Gal 1991); O(S log S) suffices for any circuit (von
  Neumann 1956; Pippenger 1985). These are superlinear lower bounds - but in the NOISY model; a
  noiseless circuit lower bound does not follow (Pippenger simulation runs the other way), so they do not feed MMW or R-MCSP.
- Barriers: FB1 holds for every circuit (relativizes and localizes trivially); FB2 is a counting statement that also holds with oracle
  gates (MMW19 Thm 1.2 is for every oracle A) - consistent with the locality barrier.

## 5 Implications for PNP-001 (exact)
- R-MCSP (L(MCSP[N^beta]) <= K CC^{2-delta}): FB1 shows stability-based restrictions are vacuous, so they cannot supply the
  MCSP-specific property P. No contribution.
- Streaming route (MMW19 Thm 1.3): FB2 shows observability/state-count arguments cap at O(s log(n+s)) bits, inside the allowed poly(s)
  budget, so they cannot establish the hypothesis. The open obligation remains a lower bound on update (transition) time that does not
  survive small oracle gates.
- Noise/redundancy gives true superlinear bounds only in the noisy model - recorded as a known, non-transferring result.
Verdict: the fly-by-wire / feedback approach cannot help as formulated; the two lemmas say precisely why. Nothing in this note is a step
towards P != NP.

## 6 Independent review (2026-11-20, adversarial reviewer, read-only)
FB1 time-varying: CORRECT; time-invariant cost understated -> fixed above (Theta(S) per step, Theta(S^2) unrolled). FB2 bound and proof:
CORRECT; consequence for MMW19 Thm 1.3: CORRECT (search vs decision fine, s >= n so O(s log(n+s)) is poly(s)); achievability argument
replaced by the oracle-free brute-force algorithm. Literature: pebbling attribution and recomputation caveat fixed; Dobrushin-Ortyukov
correction history completed. Exhaustive illustration n = 2, basis {AND, OR, NOT}, s = 0..5, t = 0..4: I_t never exceeds 1 + #prefixes
(bound loose: s = 2, t = 4 gives I_t = 2 vs bound 15) - finite illustration, not proof. Verdict: negative result stands.
