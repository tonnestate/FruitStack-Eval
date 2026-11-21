# PNP-001 — Contract K8: Bridge Map and the Direct Bridges to P != NP (owner, 2026-11-21)
Working copy for agents (authoritative text: the owner's message). Status OPEN. Labels [Q]/[G]/[E]/[C]. Never claim P != NP.
Relation: supersedes as umbrella the earlier F-J working copy PNP-001-K8-RANGE-AVOIDANCE-CONSTRUCTIVE-REFUTER-CONTRACT-2026-11-21.md
(its questions Q-31ac362875, Q-d7e7fa69af, Q-eed0582acc stay valid as Stage C) and the K9 bridge file (Q-19b8d82674 = Stage E,
Q-fd7ff4c775 = Stage F, Q-567f504552 = Stage E.4). Do not duplicate those questions.

## 0 Purpose
For each published transfer theorem: (a) exact required lower bound, (b) best known bound in the same model and parameters, (c) gap,
(d) PNP-001 results touching it. Concentrate effort on the shortest gaps that lead directly to P != NP.

## 1 Bridge map (verify in Stage A)
A Oliveira-Pich-Santhanam (ToC 2021) item (1) [Q]: Gap-MCSP[2^{beta n}/cn, 2^{beta n}] not in Circuit[N^{1+eps}], one eps for all small
  beta. Known: same bound stated for near-quadratic U2-formulas [Q, abstract]; nothing superlinear for general circuits. => NP not in
  Circuit[poly] => P != NP.
B Theorem R (REUSE-MCSP-NOTE.md) + CJW20 Thm 1.6 + MMW19 Thm 1.4: MCSP-specific circuit-to-formula simulation with exponent c < 1
  (R-MCSP). Known: formula bound N^{2+beta-eta}; generic simulations need c >= 1 (Prop. R1). => P != NP.
C MMW19 Thm 1.3 [Q]: no one-pass poly(s)-space, poly(s)-update algorithm for search-MCSP^A[s]. Known: space Theta(s log s); nothing for
  update time. => P != NP.  (Director: rows B/C cite MMW19 Thm 1.4 and 1.3 - confirm numbering at the source; K1 uses Thm 1.3.)
D CJSW "Constructive Separations and Their Consequences" (TheoretiCS 2024; FOCS 2021) Sec. 4, Thm 1.7 [Q]: sufficiently efficient refuter
  for MCSP against the Thm 1.7 model. Known: tbd. => P != NP (per paper). Check FIRST.
E Williams method; Wu-Wang template (arXiv:2611.02560) [C]: counting time 2^{n/g(n)} for linear-size 3-CNF; g = sqrt(log n) [C, Oct 2026]
  gives Omega(n sqrt(log n)) for E^NP [C, arXiv:2611.07972]. => E^NP lower bounds, NOT P != NP.
F OPS items (2)-(4), U2-formulas with XOR leaves [Q]: Gap-MKtP lower bounds; magnification threshold below existing bounds in that model
  [Q]; missing only the technique transfer to Gap-MKtP. => EXP not in NC^1.
G Pich-Santhanam (ECCC TR23-199) [Q]: superpolynomial lower bound for EF + wk(f) axioms, given witnessing formulas are tautologies. Known:
  no EF lower bounds. => SAT not in P/poly.

## 2 Stage A - source verification: exact statement, model, parameters, quantifier order for every row. A: is the U2-formula bound for
exactly the same Gap-MCSP parameters and "for every small beta"? If not, A and B are different gaps. D: copy Thm 1.7 in full (MCSP
variant, model, refuter resources, conclusion). E: label per K7 Stage A (Q-cd3478a51e); not a premise before that.
## 3 Stage B - merge [E]: A, B and K1 are the same missing step "formula-to-circuit transfer for MCSP" with sub-forms arbitrary circuits
(R-MCSP), r reused gates (reuse lemma), streaming circuits (K1). Weakest sufficient version per sub-form. Mandatory test: apply every
candidate argument first to model F (U2-formulas with XOR leaves, Gap-MKtP); nothing in F => unlikely for A.
## 4 Stage C - refuters (row D): what a refuter outputs and in what time; can our exact synthesis (SAT-optimal circuits, MUX/SC tables)
refute small candidates in the required model (record sizes); what an asymptotic refuter needs beyond finite synthesis (finite =
evidence only); barrier: CJSW show some separations cannot be constructive (e.g. high time-bounded Kolmogorov complexity) - is the
Thm 1.7 MCSP variant affected?
## 5 Stage D - language gap: does an N^{1+eps} (or N g(N)) circuit lower bound for an E^NP language imply any bound for Gap-MCSP or another
sparse NP language usable in rows A-C? Literature: Korten 2021, Chen-Hirahara-Ren 2024, Li 2024, Ren-Williams ECCC TR26-118. Published
implication with parameters, or "no known implication" with the closest results.
## 6 Stage E - proof complexity (row G): Garlik-Gryaznov-Ren-Tzameret "The Weak Rank Principle" (STOC 2026, ECCC TR26-133) [Q] exact PCR/F2
bounds and hardness of circuit-lower-bound statements; which witnessing formulas G needs, are weak-rank encodings among them or
reducible; Theorem 12 is an ordinary hard CNF - which properties would make it relevant to G; roABP closure caution [C, ITCS 2026]:
quantitative width preservation for every certificate transformation.
## 7 Stage F - amortised gate elimination (control, not a route): Wittcop [C, not located]: check CC(f) >= 2(N-m) - B under the stated
rules; compatibility with R1160; Golovnev-Hirsch-Knop-Kulikov limits [G]: why gate elimination gives at most linear bounds, so it cannot
meet rows A-C.
## 8 Output K8-REPORT.md: P1 verified map A-G; P2 merged obligation + weakest forms; P3 Thm 1.7 + small refuter results; P4 language gap;
P5 proof-complexity comparison; P6 gate-elimination control; P7 chain, premises PUBLISHED THEOREM / CLAIMED / INDEPENDENTLY PROVED / OPEN.
## 9 Restrictions: mathematical research only; no architecture/PlumMe/agent-management/running-session changes; no CI; proof-book
conventions; nothing PROVED without independent review; P != NP not claimed.
