# T23 — Main obligation: does the claimed ETH refutation transfer to circuit lower bounds? (PI, 2026-11-17)

STATUS: answered at linear and slightly superlinear size by an EXISTING theorem, conditional on the external ETH claims. The
quantitative refinement (§3) is the PI's own derivation, NOT independently reviewed (subagents unavailable: usage limit until
2026-11-19). Not in the ledger yet.

## §1 The external input (read in source)
- OpenAI, lean/docs/378.md: deterministic machine that COUNTS satisfying assignments of a k-CNF (fixed k >= 2) on n variables in time
  (L+1)^{O_k(1)} · 2^{O_k(n (log log n)^2/sqrt(log n))} (formalized). Manuscript (Oct 25, 2026): 2^{O_k(n log log n/sqrt(log n))},
  and 2^{O_{k,D}(n/sqrt(log n))} when #clauses <= D·n (not stated as formalized).
- Anthropic, formal-math/eth/README.md: deterministic #3-SAT in 2^{O(n log log n/sqrt(log n))}; Lean theorems `ETHIsFalse`,
  `MainTheorem` use only propext, Classical.choice, Quot.sound; independent kernel re-check; Lean-vs-paper correspondence NOT
  machine-checked (README).
- Status: external, unreviewed; outside verification reportedly led by ETH's proposers and R. Williams (news sources). FruitStack
  has not reproduced either proof (Lean compile needs owner approval).

## §2 The transfer theorem already exists (read in source)
Jahanjou–Miles–Viola, "Local reductions", ICALP 2015 (ECCC TR13-099 rev. 2, p. 2–3, proofs p. 18–19):
- Corollary 2: if satisfiability of (1) linear-size circuits, (2) linear-size series-parallel circuits, (3) linear-size log-depth
  circuits, (4) quasi-poly-size SYM-AND circuits is solvable in time 2^n/n^{ω(1)}, then some f ∈ E^NP is not computed by circuits
  of that class.
- Corollary 3 (1'): "ETH is false; i.e., for every ε > 0, 3SAT is in time 2^{εn}" suffices for (1). Known before as Williams,
  SICOMP 2013, Thm 6.1. Proof: Cook–Levin/Tseitin. (2'): SETH false suffices for (2). (3'): n^α-SAT in 2^{n-ω(n/lglg n)} for (3).
- Remark (p. 3): "if 3SAT is in time 2^{εn} then f ∈ E^NP does not have circuits of size cn for a constant c = O(1/ε)";
  "a 5n lower bound is not known for E^NP".
- Open problem stated there: NE (instead of E^NP) for classes (1)–(3) needs a linear-size strengthening of Impagliazzo–Kabanets–
  Wigderson.
CONSEQUENCE (conditional on §1): the claimed algorithms give, for every ε > 0, 3SAT in time 2^{εn} (deterministically), hence
  ∃ f ∈ E^NP with no linear-size circuits (for every constant c, no circuits of size c·n).
  For every fixed k the claims give k-SAT in 2^{o(n)}, so SETH is false as well and (2) follows; (2) is contained in (1).
  Best unconditional explicit lower bounds for general circuits are of the form c·n with c slightly above 3 (JMV: "between 3n and
  5n"; most recent value not re-checked here). So this would be a new superlinear lower bound for E^NP.
  CORRECTION (owner, verified in source): the OpenAI manuscript itself states it — Corollary 1.4 (paper.txt l.122–128): there are
  L ∈ E^NP and c > 0 with C_L(n) > c·n·sqrt(log n) for infinitely many n. The consequence is NOT new.

## §3 Quantitative refinement (PI derivation, unreviewed) — SUPERSEDED: identical to OpenAI Cor. 1.4 (i.o.); kept as a re-derivation
In the proof (JMV Thm 12 / Cor. 2): if the E^NP function has circuits of size s on inputs of length ~2n, then C''_x consists of three
copies of C_x plus O(1)-depth local decision trees and a clause check, so size(C''_x) = 3s + O(n) on n' = n + O(log n) inputs; Tseitin
gives a 3-CNF with N = O(n + s) variables and O(N) clauses; the step needs this 3-CNF decided in 2^{n'}/n'^{ω(1)}.
With the formal bound 2^{C·N (log log N)^2/sqrt(log N)} this holds whenever s <= δ·n·sqrt(log n)/(log log n)^2 for a small constant
δ = δ(C) > 0. Conditional conclusion:
    E^NP ⊄ SIZE( δ · n · sqrt(log n) / (log log n)^2 ),
and with the manuscript's clause-linear bound 2^{O_D(N/sqrt(log N))}: E^NP ⊄ SIZE(δ · n · sqrt(log n)). To be checked: hardwiring
x keeps size <= s(2n + O(log n)); the guessing step costs O(s log s) bits; NTIME(2^n) \ NTIME(o(2^n)) hierarchy as in JMV.

## §4 Where the transfer breaks (the precise remaining gaps)
- Polynomial size: Tseitin maps n inputs, s gates to n + s variables; for s = n^{1+ε} a 2^{o(n+s)} bound gives no savings over 2^n.
  Circuit-SAT for poly-size circuits in 2^n/n^{ω(1)} (needed for NEXP ⊄ P/poly via Williams) does NOT follow. Owner's gap confirmed.
- Log-depth linear size (class 3): needs n^α-SAT (unbounded width); the claims are for fixed k. Not obtained.
- NE/NEXP instead of E^NP: needs a linear-size IKW theorem (open, JMV).
- P vs NP: no implication. E^NP superlinear lower bounds are far from NP ⊄ P/poly.

## §5 Gate decision
Main obligation: ANSWERED at linear/slightly superlinear size (existing theorem + external claim); BLOCKED beyond n·sqrt(log n) by the
Tseitin variable blow-up, with no known way around it for fixed-width SAT algorithms. Next steps, all cheap and analytic:
(a) independent review of §3 when subagents are available again (after 2026-11-19 07:00); (b) check whether the new algorithms'
technique applies to CNF of growing width or to circuits directly (would be needed for classes (3) and beyond) — read the
manuscripts' method sections; (c) ledger entry only after (a).
