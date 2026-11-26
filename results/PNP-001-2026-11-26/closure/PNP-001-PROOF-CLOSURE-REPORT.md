# PNP-001 Proof Closure Report

Started 2026-11-26 16:45 CET under the owner order "PNP-001 – Autonomous Proof Closure Mission".
Validation status of everything below: assessor derivations of one session and one model family unless a
Q-id:S-id with SURVIVED_REVIEW is cited. Nothing here is PROVED in the K11 sense. **P ≠ NP is not proved.**

## 1. Reverse proof graph from the target

Every edge is a mathematical implication; references are the evidence for that edge.

### Route M (MMW streaming magnification) — the only route with a published final implication

| # | Statement | Edge to the next line | Evidence | Status |
|---|---|---|---|---|
| M0 | P ≠ NP | — | — | target |
| M1 | ∃ time-constructible s(n) ≥ n, ∃ A ∈ PH: search-MCSP^A[s] has **no** uniform deterministic streaming algorithm with space poly(s) and worst-case update time poly(s) (fresh bit per step not required) | M1 ⇒ M0 | MMW19 Thm 1.3, `literature/sources/mmw19/paper.txt` l. 115–121 (quantifiers re-read 2026-11-26) | published |
| M2 | Γ^A_S lower bound: for the uniform class, max_t of the update cost is not poly(s) | M2 ⇔ M1 | Q-156fa9c912:S0037 (resource transfer, worst-case, SURVIVED_REVIEW), Q-156fa9c912:S0036 (representation completeness, SURVIVED_REVIEW), Q-0cce07fc92:S0024/S0027 (stage circuits incl. oracle slots, SURVIVED_REVIEW), Q-6ead6c935d:S0004 (class match, SURVIVED_REVIEW); assessor row R2-G0004-R1-STRENGTH (uniform QE* ⇔ (40a)) | reduction done, cross-family review pending for the assessor row |
| M3 | **OPEN CORE OBLIGATION O\***: a property of the update maps of every correct uniform algorithm for search-MCSP^A[s] that forces update time s^{ω(1)} | M3 ⇒ M2 | — | **open** |

Note (S0037): the right target is the worst case Γ_S = min max_t CC(F_t), not the sum Λ_S; Λ_S bounds imply Γ_S bounds (Λ_S ≤ N·Γ_S), not conversely.

### Routes R1, R2', W, ARITH (blocked or supporting)

| Route | Final implication | First failing inference | Repair attempted | Status |
|---|---|---|---|---|
| R1 self-diagonalisation (universal certificate verifier) | CC(W_{m,s}) ≤ C m^d s^{1-δ} ⇒ P ≠ NP | the bound is refuted under P = NP i.o. (Meyer), so proving it is proving P ≠ NP (TWENTYSEVENTH, NINETEENTH) | tensor contraction, QE arithmetisation, partial certificates (THIRTIETH–THIRTYTHIRD) | **blocked**: equivalent restatement |
| W witness-circuit / Williams | E^NP or NE lower bounds | P = NP ⇒ ∃L ∈ E with CC > c2^n/n a.e. (R1-KANNAN-UNDER-PNP): class lower bounds never contradict P = NP | — | **supporting route** (owner 2026-11-26) |
| ARITH (VP ≠ VNP, HC/permanent, tensor spectra) | — | formal → Boolean transfer; GL-invariant functionals see only |f^{-1}(1)| (R1-INVARIANCE-OBSTRUCTION) | — | **blocked** for Boolean conclusions |
| HTT magnification | HTT_{N^δ} ∉ DTIME(O(N)) ∀δ ⇒ P ≠ NP | hypothesis contradicts "E needs exponential circuits" (R1-HTT-MAGNIFICATION) | redirect to tasks whose quasi-linear hardness is the believed truth | **blocked** (wrong direction) |

## 2. Why O\* is the minimum remaining obligation and what any proof of it must avoid

Proved constraints (assessor, cross-family review pending):

1. **Information barrier.** S0006 (state O(s log s) suffices), S0010 (prefix separation), S0012 (counting), S0013 (cell-probe ceiling O(S/w)):
   every bound that depends only on states, ranks, fooling sets or cut measures is met by S0006 and cannot exceed polylog N.
2. **Oracle-locality barrier.** MMW19 Alg. 1 (blocks b = Θ(s log s), Stream-Merge) solves search-MCSP^A[s] with poly(s)
   state when each update may ask a Σ_k-oracle on poly(s)-length queries. A technique that is insensitive to what an update
   computes internally (it bounds only states or information) also "proves" a lower bound against these oracle updates, which is
   false. O\* must use the internal computation of the updates.
3. **Degree / rank controls.** OR accumulator (addendum 2026-11-21 §8 A): degree t at one gate per update; equality: rank 2^k at
   O(k) gates. Degree k d (p-1) ≥ 2^m (Q-f90dd2d84d:S0005, CLAIMED) constrains encodings, not update size.
4. **Re-encoding.** F'_t = π_{t+1} ∘ F_t ∘ π_t^{-1} (R2-COST-SHIFT): invariants must be relabelling-invariant; then they bound
   only a minimum over encodings (an MCSP-type minimisation).
5. **Quantifier order of the oracle freedom.** M1 needs ∃A ∀c. Deriving the update cost from A's own time complexity gives at
   most ∀c ∃A_c (time hierarchy inside P); a single A ∈ PH with superpolynomial time is P ≠ PH, i.e. the target. Hardness
   must come from the MCSP search structure, not from A.
6. **Strength.** The non-uniform version of M3 implies Σ_2 ⊄ P/poly, hence NP ⊄ P/poly (R2-G0004-R1-STRENGTH). Work on the
   uniform version.
7. **Unrolling.** Σ_{t<2^k} CC(F_t) ≥ CC(MCSP[s] on 2^k bits) − O(S) at aligned lengths (S0127 + S0033 unrolling,
   R2-Q-18a621cf3e-EXACT-FORM): non-uniform progress on O\* is an MCSP circuit lower bound at the magnification threshold.

## 3. Consolidated route table (mission §13 format)

| Route | Existing verified results | Remaining obligation | First failing inference | Proposed repair | Verification evidence | Status |
|---|---|---|---|---|---|---|
| M | MMW19 Thm 1.3 (published); S0036, S0037, Q-0cce07fc92:S0024/S0027, Q-6ead6c935d:S0004 (SURVIVED_REVIEW) | O\* (uniform update lower bound for search-MCSP^A[s]) | degree/rank → update cost (fails controls A, equality) | update-sensitive mechanism that survives barriers 1–7 | REVIEW lane (other family) | **active** |
| R1 | Q-filter results, partial certificates (THIRTYTHIRD) | CC(W_{m,s}) upper bound = P ≠ NP restated | Meyer step | none without new handle | assessor | blocked |
| W | OpenAI Cor. 1.4, Exact-One witness bound (THIRTYTHIRD) | — | Kannan under P = NP | supporting only | assessor | supporting |
| ARITH | VP ≠ VNP (formal), hexagon 2611.00149 barriers | formal → Boolean | GL invariance | none | assessor | blocked |

## 4. FruitStack allocation (2026-11-26 16:45)

- Peripheral lanes paused (T-B, T-A, K1, K2-K6, QW, MS-0.25, CAND-A, RECON, BINGO, QE*); backup `desk/lanes.json.bak-closure-1645`.
- Lane REVIEW: cross-family verification of the M-chain edges and the assessor rows used in §2.
- Lane CLOSURE: the core obligation O\* (counterexample-first) and the chain audit, admitted through `pnp_graph.gate`.
- Progress metric: closed critical obligations and verified edges only (`python -m pnp_graph.gate` metrics), not entry counts.

## 5. Evaluation 2026-11-26 17:10 (desk proofbook + proofstates since 2026-11-25 18:00)

- Today: 471 proofbook entries (417 APPROACH, 23 HYPOTHESIS, 24 NUMERICAL_EVIDENCE), **0 VERIFICATION, 0 REFUTATION**: no obligation closed.
- Route M support, review provenance re-checked (K11: other session AND other family):

| Step | Author | Cross-family review | Consequence |
|---|---|---|---|
| Q-156fa9c912:S0037 (resource transfer) | director-owner (Claude) | nemotron SURVIVED_REVIEW | valid support |
| Q-156fa9c912:S0036 (representation completeness, edge M2) | director-owner (Claude) | **none** (only claude-haiku) | **edge M2 not cross-family verified**; queued REVIEW first |
| Q-156fa9c912:S0010 (prefix separation, barrier 1) | director-owner (Claude) | **none** (only claude-haiku) | queued REVIEW first |
| Q-0cce07fc92:S0024 / S0027 (stage circuits) | claude-haiku | 1 each SURVIVED_REVIEW | valid support |
| Q-0cce07fc92:S0017 | claude-haiku | 6 REFUTED | correctly excluded |
| Q-6ead6c935d:S0004 (class match) | nemotron | 1 SURVIVED_REVIEW | valid support |
| Q-b5eddd829d:S0001 (indicator degree) | claude-haiku | none | queued REVIEW first |

- O\* (Q-ade9c9f92c, R4379, gpt-6-luna) S0001 "ring-buffer append cost": correct (circular array, O((r+1) log B) per block). It is
  the block-processing control of §2, not progress on O\*: it shows that buffering removes prefix-length dependence from appends.
- Relevant hypotheses consistent with §2: R4353 (counting output functions alone cannot bound update time = barrier 1),
  R4325 (oracle-free RAM transition maps have poly(S w) circuits per step = M2 support). Neither closes O\*.
- Model routing: desk research and formal lanes on gpt-6-luna (owner 2026-11-26: Luna primary, not Haiku); Anthropic models excluded.
- Graph: live graph `/root/fruits/research/PNP-001/graph` promoted to the full build (49k events) plus gate tables; desk results ingested every 3 min.

## 6. Route R10 x CJW20: unrestricted-circuit obligation (2026-11-26, proofbook seq 16755-16769, director/closure)

| Item | Statement | Status |
|---|---|---|
| T07 | L(C) <= 2^r (2S+1), De Morgan circuits | owner-verified + Q-92b080505e:S0001 SURVIVED_REVIEW |
| CJW20-T5.5-GAP | Gap-MCSP[N^beta/(Km), N^beta] needs probabilistic De Morgan formulas of size N^{2+beta-eps} | owner-verified against original proof |
| D1 | origin of the budget: restricted size s = N^{3beta-3eps/5+o(1)}, CKLM19 local PRG seed s^{1/3+o(1)} | derivation |
| D2 | no De Morgan circuit of size N^{1+eps} with r <= (1+beta-2eps) log2 N reused gates (fixed eps, all beta) | derivation, unconditional |
| D3 | basis: B2 circuit -> De Morgan with size <= 3S, reuse <= r+2t; formula bounds only De Morgan | derivation |
| REFUTED | size budget r_rho + log2(2S_rho+1) <= (3beta-eta) log2 N for all circuits | dual-rail parity (r_rho >= k-1); no circuit shrinkage |
| D4 | gamma-almost-formula = OR of 2^gamma disjoint formulas of size <= S+gamma: reuse costs 2^gamma in correlation | exact lemma |
| AF | correlation budget gamma <= log2(1/delta) instead of size budget; reaches gamma up to N^{beta-eta} | conditional on P1 (local PRG with error 2^{-gamma}), P2 (forest shrinkage) |
| D5 | OPS21 quantifiers (exists eps, all small beta, Circuit[N^{1+eps}] => NP not in P/poly): AF budget N^{beta-eta} vanishes as beta -> 0 | limit identified |
| D6 | restriction collapses reused gates with d_g <= N^{1-beta-eta}; only wide reused gates survive | derivation |

Remaining obligation (unrestricted circuits): Gap-MCSP[N^beta] circuits of size N^{1+eps} with more than N^beta wide reused gates
(each depending on > N^{1-beta-eta} inputs), for a fixed eps and all small beta. FruitStack question seq 16764 (CLOSURE lane) works on P1-P4.

## 7. Deep research routes A-G: dedup and fail-fast (2026-11-26, proofbook seq 16774-16786, director/closure-deep)

| Route | Dedup against the book | Fail-fast result (step) | Remaining obligation (gated question) | Desk lane |
|---|---|---|---|---|
| C gate elimination + reparametrisation | seq 1710, H4 seq 1719 | — (needs Mishra-Santhanam TR26-260 source) | potential Phi = S + lambda R + mu D with super-linear drop, promise preserved (OBL-W-C, seq 16781) | W-C, 2 slots |
| A semantic T07 | = D4 restricted to occurring assignments | A1 valid lemma; contrapositive forces \|B_K^+\| >= N^{2+beta-eps}/(2S+1) for every cut. A2 control: every sparse subcube V_T lies in YES, so the cut tuple must take few values on all of them; A o B meets the D5 information threshold | cut rule with few values on sparse subcubes and PRG outputs (OBL-W-A, seq 16782) | W-A, 1 |
| D constructive separation | K8 F/G seq 8479/8481 | D1c: CJSW Thm 1.4 verified at source; simple counterexamples exist by pigeonhole for deterministic space-S streams; the obligation is uniform AC0 selection without advice (+ randomized case) | OBL-W-D, seq 16783 | W-D, 1 |
| B gap-preserving restriction | = D1; Q-9154b244de S0023/S0067/S0113 | B1: as stated refuted (seq 16761); continues as AF premises P1/P2 + D6 | OBL-W-B, seq 16784 | W-B, 1 |
| E sparse NP language | seq 5204/5206 | E1: CJW19 Thm 1.2 gives only C not in Circuit[n^k]; P/poly needs MCSP-type self-reducibility | sparse NP family with that self-reducibility (OBL-W-E, seq 16785) | W-E, 1 |
| F canonical witnesses | route M | F1: CanMCSP not in Streaming[poly,poly] => P != NP (Sigma_2 canonicaliser); instance of M1, quantifier-order barrier applies | OBL-W-FG, seq 16786 | W-FG, 1 |
| G simple hitting sets | CJW20 Thm 5.2 | G1: with H = all simple tables it is the lower bound itself; content only for explicit structured H, merges with D1c | OBL-W-FG | W-FG |

Desk: 9 research slots (REVIEW 2, CLOSURE 1, W-C 2, W-A/D/B/E/FG 1 each), gpt-6-luna primary; backup `desk/lanes.json.bak-deep-*`.
Shared bottleneck exposed by A2, D1c, G1 and D5: every route needs a *uniform/structural selection* that a seed-length or
information count cannot supply - exactly the locality/information barriers of sec. 2. Nothing in this section is verified cross-family yet.

## 8. Quantifier weakening, coverage, DISJ collisions (2026-11-26, proofbook seq 16795-16804, director/closure-quant)

| Item | Statement | Status |
|---|---|---|
| QO1 | NP in P/poly => exists K, for every s: Gap-MCSP[s/(cn), s] in SIZE[N s^K] (greedy anti-checker, approximate counting); s = N^beta gives N^{1+K beta} | derivation (Claude family), cross-family review queued |
| QO2 | weakest sufficient form Q*: for every K some s_K with Gap-MCSP[s_K/(cn), s_K] notin SIZE[N s_K^K] i.o.; Q1 => Q2 => Q*, Q3 => Q* | derivation, review queued |
| QO3 | Q3 = MMW19 Thm 1.4 bullet 3 (source checked; depth poly(s) already suffices) = book target (8), S0141 | dedup |
| QO4 | 368 cross-family-survived lower-bound steps: none superlinear for general circuits; D2 extends to size N^{1+k beta}; D5 quantifier objection removed under Q2, magnitude gap stays | evaluation |
| COV1 | cover K1 (T07+CJW20, low reuse) + K2 (D6) + K3 (AF, conditional); residual R = > N^{beta-eta} wide reused gates after restriction | open: R |
| CJ1 | CJSW Thm 1.4 proof (source checked): the P = NP algorithm is deterministic, so deterministic separations suffice | source |
| CJ2 | suffix y = u AND NOT v (or swapped): no selection of the failing instance needed | checked |
| CJ3 | enumerator A*: refuters with deterministic polylog-time bits fail; W-D bits need real alternations | checked, CLAIMED |
| CJ4 | W-D obligation contains O* (the P = NP compressor never collides on simple prefixes); A/D/G related, transfers not proved | derivation |

Open obligations after this section: OBL-QSTAR (residual R / O*), OBL-W-D-COLLIDE (question seq 16804, supersedes 16783). No new lanes.

## 9. Student-Teacher (Carmosino-Grosser TR25-045 rev.1, proofbook seq 16809-16813, director/closure-st)

| Item | Statement | Status |
|---|---|---|
| ST0 | Thm 1.7 read at the source; it uses Lemma 5.5 and Lemma 5.6, not the witnessing hypotheses | source |
| ST1 | Lemma 5.6 applies Lemma 5.4 (n-input, size n^k) to an N-input SearchMCSP circuit at size n^b; the b-dependence is not tracked | possible accounting gap, review queued |
| ST2 | independent transfer: absolute protocol => NP notsubset P/poly (Teacher answers hardwired, exponents K_j independent of b) | derivation, review queued |
| ST3 | sandwich: [PH language, a.e. superpolynomial] => 0-round protocol => r-round protocol => NP notsubset P/poly | derivation, review queued |
| ST4 | the absolute protocol lies in the same band as Q* / route M; it is not a weaker obligation | evaluation |

Exclusion: counterexample rounds add no leverage beyond a PH circuit lower bound (under PH in P/poly every round is a bounded-complexity composition).
PhysalisMe finite games were not run: ST2 holds for every finite protocol, so finite games cannot change this decision.
