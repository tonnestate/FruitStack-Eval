# T21 — What would each line prove? Target map and gate for Williams' algorithmic method (PI, 2026-11-17)

STATUS: literature-based classification; no new theorem. Owner standard (2026-11-17): an idea becomes a PNP-001 task only if it
yields a concrete, checkable statement about GENERAL models of computation; a mathematical connection is not a proof route.
Charter: every structure is tested for its actual contribution to P vs NP.

## Target map (what full success of each line would establish, and whether it implies P ≠ NP)
| Line | Full success would prove | Implies P ≠ NP? |
|---|---|---|
| Current main question (T20/O1: conormal invariants, border dc(per_m)) | border dc(per_m) superpolynomial, i.e. VP_s ≠ VNP in the border (GCT) sense | NO known implication. Known implications run the other way only (Bürgisser: Boolean non-uniform separations + GRH => VP ≠ VNP over C). |
| Cubic preprint and any polynomial improvement | border dc(per_m) >= m^c | No. |
| Williams' algorithmic method (nontrivial C-SAT => NEXP ⊄ C; Murray–Williams STOC 2018: NQP ⊄ ACC^0; Chen–Ren: average-case; Chen–Lyu–Williams FOCS 2020: almost-everywhere) | NEXP or NQP ⊄ C for a circuit class C; at the limit C = P/poly: NEXP ⊄ P/poly | No: lower bounds for nondeterministic EXPONENTIAL / quasi-polynomial time, not for NP. NEXP ⊄ P/poly is itself open and does not imply P ≠ NP. |
| Range avoidance (Chen–Hirahara–Ren STOC 2024; Z. Li STOC 2024: S_2E needs circuit size 2^n/n) | strongest lower bound against GENERAL circuits, for symmetric exponential time | No; and the proofs relativize (stated by the authors), so the technique cannot separate P from NP (Baker–Gill–Solovay). |
| Hardness magnification (T12: Oliveira–Santhanam, McKay–Murray–Williams, Chen–Jin–Williams) | NP ⊄ P/poly from weak-looking lower bounds for specific NP problems | Yes (NP ⊄ P/poly => P ≠ NP) — the only line here whose success implies P ≠ NP; blocked in its known forms by the locality barrier (Chen–Hirahara–Oliveira–Pich–Rajgopal–Santhanam). |

## Gate: Williams' algorithmic method as a PNP-001 flank
| Field | Entry |
|---|---|
| HYPOTHESIS | The "faster C-SAT => lower bound for C" mechanism can be extended to classes C strong enough to matter for P vs NP. |
| ASYMPTOTIC TARGET | The mechanism's conclusion lives at NEXP/NQP; P ≠ NP needs lower bounds for NP. Bridging requires scaling the hard function down from NQP to NP — not provided by the method. |
| NEW INFORMATION | A proven general mechanism (unlike our algebraic invariants) — its value is the extensibility question in C, not the class of the hard function. |
| BORDER VALIDITY | n/a (Boolean). |
| CHEAP FALSIFICATION | Done above: even complete success for C = P/poly gives NEXP ⊄ P/poly, which does not imply P ≠ NP. |
| DECISION | NO DIRECT LEVER for P ≠ NP. Admissible only combined with magnification (the one line that reaches NP), where the locality barrier is the known obstruction — i.e. it returns to T12. Not opened as a flank. |

## Consequence for the active mission
By the owner's own standard, the current main question (scheme-theoretic conormal invariants) is a route to an ALGEBRAIC
separation, with no known implication to P ≠ NP. It stays the active question because it is the owner's explicit decision of
2026-11-17 and the program charter lists VP vs VNP as an admissible algebraic model; but its contribution to P vs NP must be stated
as "algebraic analogue", never as a step towards P ≠ NP. Among all lines mapped so far, only hardness magnification has a success
condition that implies P ≠ NP.
