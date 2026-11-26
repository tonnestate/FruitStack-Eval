# T30 — Interface relations R_A of 3-SAT building blocks: the transition and what refuting it means (PI, 2026-11-17)

STATUS: elementary, proved here (standard theorems: Cook–Levin, TM-to-circuit simulation). No computation, no ledger entry.
Owner's plan: stay with 3-SAT; for a formula part A with interface variables B define R_A(b) = 1 ⇔ b extends to a satisfying
assignment of A; first PROVE a transition "fast SAT algorithm ⇒ compact representation / efficient operation on R_A", then refute
that consequence.

## Lemma T1 (transition holds)
Hypothesis: a deterministic TM M decides 3-SAT in time p(N) (N = encoding length).
For a 3-CNF A on variables B ∪ Y: R_A(b) = M(A|_{B=b}) (substitute b, simplify; length <= |A|). By the standard simulation of a
time-T machine by circuits of size O(T log T), R_A has a circuit of size O(p(|A|) log p(|A|)) + O(|A|), constructible from A in time
poly(|A|). Operations on building blocks — conjunction A_1 ∧ A_2 along shared interface variables, projection (∃ over internal
variables) — stay inside the same class (the result is again R of a 3-CNF of size |A_1| + |A_2|).

## Lemma T2 (every NP language is an interface relation)
For every L ∈ NP, Cook–Levin gives 3-CNFs A_n(x, y), constructible in time poly(n), with x ∈ L ⇔ ∃y A_n(x, y). So L ∩ {0,1}^n = R_{A_n}
with interface B = x.

## Corollary (equivalence)
  "every R_A has circuits of size poly(|A|)"  ⇔  NP ⊆ P/poly.
⇒ by T2. ⇐: the language {(A, b) : R_A(b) = 1} is in NP; if NP ⊆ P/poly it has poly-size circuits; hard-wiring A gives a circuit for
R_A of size poly(|A|).
Consequence: refuting the consequence of T1 means exhibiting explicit 3-CNFs A_n whose interface relations need superpolynomial
circuits — i.e. proving NP ⊄ P/poly. That implies P ≠ NP and is, as far as known, strictly stronger. So the approach, as formulated,
RESTATES the target (in strengthened, non-uniform form); the transition is not the bottleneck.

## Where the building-block structure could still carry weight
- Table size 2^{|B|} and communication/rank of R_A across a cut prove nothing about circuit size (owner's equality example: full
  rank, O(m) circuit).
- A non-restating use would need a COMPOSITION LEMMA: a lower bound on the circuit complexity of R_{A_1 ∧ A_2} in terms of the parts,
  valid for general circuits. No such lemma is known for circuits. The closest existing programme is the Karchmer–Raz–Wigderson
  conjecture on formula DEPTH of compositions (would give P ⊄ NC^1, not P ≠ NP).
- Restricted representations (formulas, decision diagrams, low rank) CAN be refuted for explicit A, but T1 does not produce them
  (a fast SAT algorithm yields circuits, not those representations), so such refutations do not touch P vs NP.

## Decision (gate)
Transition: PROVED (T1). Consequence to refute: equivalent to NP ⊆ P/poly (T2 + corollary) — a restatement of the target.
No asymptotic lever unless a circuit-level composition lemma is found; that lemma is the single precise open object here.
