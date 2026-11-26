# PNP-001 — Active mission overview (owner decision 2026-11-17)

The proofbook (/var/lib/cherryme/knowledge/proofs/p_vs_np.jsonl, 219 entries) is kept unchanged as the audit trail.
This page is the only active overview.

| Metric | Value |
|---|---|
| Active main question | 1 |
| Prioritised research flanks | 3 |
| New full enumerations without a passed Hypothesis Gate | 0 |
| Expensive computations running at the same time | at most 1 |

## Main question (owner decision 2026-11-17, replaces the conormal question)
Can the new subexponential #k-SAT algorithms (OpenAI and Anthropic, Oct 2026, formalised in Lean; claimed ETH refutation) be
transferred to Circuit-SAT for circuit classes general enough that Williams' algorithms-to-lower-bounds theorem applies, without the
reduction (Tseitin blow-up n -> n + s) destroying the time savings? First task: state the exact transfer statement and search for
existing positive results or counterexamples; no computation before such a transfer statement is named.
Status of the ETH claims: published manuscripts + Lean artefacts (standard axioms; Anthropic: independent kernel re-check);
EXTERNAL, not reproduced by FruitStack. Lean-vs-paper correspondence is not machine-checked (Anthropic README).
Previous main question (conormal invariants, O1 in T20) is parked as an algebraic flank; nothing deleted.
State 2026-11-17 (T23): answered at linear size by an existing theorem — Jahanjou–Miles–Viola 2015 Cor. 3(1') / Williams 2013
Thm 6.1: ETH false => E^NP ⊄ linear-size circuits. Not new: the OpenAI manuscript states it (Cor. 1.4: E^NP needs c·n·sqrt(log n) gates i.o.);
the PI's refinement only re-derived this. Blocked beyond ~n sqrt(log n) by the Tseitin blow-up
(poly-size Circuit-SAT does not follow); no implication for P vs NP. Meta-complexity check: T22 (reference formulation only).
Compression map (T24): fixed-width transfer to size-n^k circuits needs width w >= k-1 (counting) / w >= k (Dell–van Melkebeek, poly-time
reductions, unless coNP ⊆ NP/poly) and N <= n·polylog variables; no construction known beyond series-parallel linear size. Open.
4-SAT SWAP / rank-2 clause factorisation (T25): no asymptotic lever (<= constant factor k in the contraction exponent; it is
already step 1 of the published algorithm, whose gain is bounded occurrence + low degree + interpolation). Transfer to circuits
reduces to T24's variable count, not to fan-out or local tensor rank.
T28: evaluator needs only fixed width + N <= n·sqrt(log n)/polyloglog variables (bounded occurrence is produced internally, cost
included). Lemma G: every gate-value encoding (Tseitin and all grouped variants, any constant width) needs |S| >= CircuitSize(f)/2^w − 1
auxiliary variables — excluded for all f of superlinear circuit complexity. Open: proof-like (non-gate-value) witnesses of length
n·sqrt(log n) with constant-width perfect verification.
Binding obligation (owner 2026-11-17): ∃ L ∈ NP with L ∉ P — both halves for the SAME language. The algorithms-to-lower-bounds line
(T23–T28) cannot deliver it even if it succeeds (conclusions at NEXP / E^NP).

## Flanks (state)
1. Scheme-theoretic dual geometry — dual side CLOSED at quadratic for every containment-derived invariant (T16 Thm C, T20 Thm C');
   conormal side OPEN, reduced to obligation O1 (T20).
2. Kernel/cokernel geometry — identical object to the conormal side of flank 1 (kernel incidence = conormal of det_n, T20 §3).
3. Beyond polar readings (higher corank, non-conormal invariants) — open; any candidate must pass the gate first.
Side flank (owner, theoretical only, no simulation): boson/fermion interference — gate result BLOCKED (T20 §5).
Not opened: Williams' algorithmic method — NO DIRECT LEVER (conclusions at NEXP/NQP, not NP; T21). Astrophysical/cosmological
computing limits, time dilation — no mission (owner 2026-11-17: finitely many physical measurements alone prove no asymptotic
lower bound; physically inspired mathematics may contribute only by proving a theorem about the defined model of computation;
P counts Turing-machine steps, not an observer's waiting time).

## Target map (T21) — what success would prove
The main question targets an ALGEBRAIC separation (superpolynomial border dc(per_m), VP_s vs VNP); no known implication to P ≠ NP.
Report it as "algebraic analogue", never as a step towards P ≠ NP. Of all mapped lines only hardness magnification has a success
condition implying P ≠ NP (NP ⊄ P/poly); its known forms are blocked by the locality barrier (T12).
Hardness magnification (owner decision 2026-11-17, T26): MMW19 Thm 1.4(3) (search-MCSP^A[s] ∉ Circuit[N·poly(s), depth poly(s)] ⇒
NP ⊄ P/poly) worked to its blocking step. Result: any proof of the hypothesis already proves Circuit-Min-Merge^A[s] ∉ P/poly on
ℓ = Θ(s²) bits (explicit Σ3P^A function) — a superpolynomial lower bound of the same nature as the goal. No lever; documented
obstruction. Certificate classifier: theory/checks/certificate_status.py (FULL_RANK / SAMPLE_KERNEL=UNKNOWN / identity proof only).
Check rule (owner): every lower-bound approach must state whether it restricts access to the input structure (black box vs explicit).
Diagonalisation / reverse architecture (T27): owner's D is EXP-complete, so "D ∈ NP" ⇔ NP = EXP (no lever). "P = NP ⇒ faster
simulation ⇒ hierarchy contradiction" needs exactly a fixed-alternation polynomial speed-up of deterministic time (Lemma S:
∃k ∀ε DTIME(t) ⊆ Σ_k TIME(t^ε)); open, implies P ≠ PSPACE; alternation trading has a proven ceiling 2cos(π/7) (Buss–Williams) in the
space-bounded setting and only log* speed-up (PPST) without space bounds.
Admission rule (owner 2026-11-17): an interdisciplinary idea becomes a task only when it yields a concrete, checkable statement about
general models of computation; distinguish resource limits of specific models from lower bounds for universal models.
Paused, no asymptotic lever: degree-6 HWVs (T11-P closed), Koszul flattenings (T19, partial data kept).

## Rules
- Bound-and-Verify: before opening a search space, check whether a single general theorem settles the whole class; only
  candidates surviving a cheap exact filter are computed; every final claim gets an exact certificate.
- Hypothesis Gate before every expensive computation:
  HYPOTHESIS / ASYMPTOTIC TARGET (route to ω(m³)) / NEW INFORMATION (vs polar, rank, occurrence methods) / BORDER VALIDITY
  (theorem or named open obligation linking it to all affine determinant limits) / CHEAP FALSIFICATION (Fermat forms, known
  determinant degenerations) / COMPUTATION (cost, certificate) / DECISION: PROCEED | REFUTED | BLOCKED | NO ASYMPTOTIC LEVER.
  STOP RULE: no expensive computation while the asymptotic lever and the needed degeneration statement are not named precisely.
- Ledger entries only for new or decisive proved claims after independent review; no entries for routine data.

## PI decision 2026-11-17 (owner: "Du bist der Forschungsleiter")
1. Physical-device line CLOSED (gate: no lever for the binding objective). Any physical SAT device either is classically simulable
   (then it is an algorithm; Lemma A in T29 for robust classical dynamics) or lies outside the Turing model; its failure refutes
   nothing (falsification rule). It can only bear on P = NP, never on ∃ L ∈ NP \ P.
2. Frontier for the binding objective ∃ L ∈ NP \ P — every route examined reduces to one of three named open statements:
   (a) NP ⊄ P/poly via an explicit function — magnification relocates to Circuit-Min-Merge ∉ P/poly (T26); building blocks need a
       circuit-level composition lemma for interface relations R_A (T30);
   (b) Lemma S: ∃k ∀ε DTIME(t) ⊆ Σ_k TIME(t^ε) (T27; also implies P ≠ PSPACE);
   (c) superpolynomial lower bounds for all proof systems (NP ≠ coNP; T29/Lemma R context).
   None has a currently identified lever; this is recorded as the honest state, not as a failure to report.
3. Active work item (one, bounded, falsifiable): T28-open — do all f ∈ SIZE(n^k) admit perfectly sound constant-width existential
   CNF verifiers with witness length n·polylog? A construction or an impossibility proof would be a genuine new result. Scope note:
   serves the algorithms-to-lower-bounds line (NEXP/E^NP conclusions), NOT the binding objective — stated explicitly.
4. Independent review of T23–T30 when Claude subagents are available again (after 2026-11-19 07:00); ledger entries only after review.

## Owner correction + working mode (2026-11-17, evening)
Research work runs INTO FruitStack, not through Claude subagents: PI writes the mission request, the full stack computes, PI analyses the
mission record and sets the next iteration. Iteration 3 (T28-open at finite size: exact W_3(f) = least witness length of width-3 existential
CNF verifiers, n <= 6, hypotheses H1-H3) submitted: /root/contracts/longrun-2026-11-15/req-pnp-iter03.json, output pnp-iter03-01.out.
The pending review of T23-T30 is also to go through a mission, not through subagents.

## Owner mission brief 2026-11-17 late: "Information Geometry, Time and Computational Lower Bounds" — MAIN QUESTION NOW
Question: does an information-transfer quantity (crossing sequences, communication across cuts, tensor contraction width) give a time lower
bound that transfers to unrestricted deterministic computation (∀M deciding L ∀k ∃^∞n T_M(n) > n^k)?
PI work: theory/T31-information-transfer-invariant-2026-11-17.md — Lemma L1 (1-tape transfer), Theorem C1 (cap: every cut-sum of
communication-type measures ≤ n²/4 + n, attained by PAL ∈ P), C1'' (no multitape analogue), Theorem C2 (Tseitin/XOR-SAT on expanders:
contraction width Ω(n), exact count in O(n³)), decision D (transport of input information cannot be superpolynomial; obligation R restates
a time lower bound). Status: PI derivations, NOT yet independently verified, NOT in the ledger.
Verification: FruitStack mission /root/contracts/longrun-2026-11-15/req-pnp-iter04.json (queued; submitted when iteration 3 finishes —
one expensive computation at a time).
Flanks (≤3): F1 = T28-open at finite size (iteration 3, running); F2 = bounded-space re-transfer / Lemma S (T27) as the only regime where
transport forces bounds; F3 = review of T23–T30 through a mission (pending).

## Owner mission brief 2026-11-17 late (2): "Identity, Phase Transitions and Emergent Information" (PNP-HYP-EMERGENT-INFORMATION)
PI work: theory/T32-identity-recoverability-emergent-information-2026-11-17.md — exact finite model (bijective U, coarse π, δ_π(t));
W1 (reversible micro / irreversible macro), W2 (preserved-but-unrecoverable = P ≠ UP via Grollmann–Selman 1988), W3 (no
non-identifiability for decision problems), W4 (unrestricted collective-invariant lower bound = SAT ∉ P), E1 (random k-XORSAT: clustering
+ frozen variables yet O(n³) — clustering ⇒ hardness refuted for general algorithms), H (Hopfield stable state PLS-complete).
Decision (pending verification): route fails for an exactly identified reason — emergent information is a property of a representation;
a lower bound quantifies over all representations, and then the invariant is the decision problem itself.
Queue (one mission at a time, chained in background): iteration 3 (running) → iteration 4 (T31 verification) → iteration 5
(T32 verification + cat-map computation + primary sources). Ledger only after these reviews.

## Iteration 3 evaluation (PI, 2026-11-17)
Mission 7b434855 (wall 3392 s, 103 steps done / 15 abandoned): COMPLETED UNVERIFIED, SYNTHESIS_FAILED; claim checks NOT_CHECKABLE /
INVALID (NO_JSON, NOT_ALLOWED:Call) — stack fault to examine: the checkers could not run the workers' code.
Content: W_3 = 0 for all 256 functions on n = 3 — correct but TRIVIAL (every 3-variable function is a width-3 CNF); my request design
flaw, n = 3 carried no information. H1 W_3(PARITY_n) = n−3 reported for n = 3..6 by one worker (nemotron-bolt).
PI independent spot-check (closure criterion K3, exhaustive, scratchpad w3/w3.py): PARITY_3 m=0 yes; PARITY_4 m=0 no, m=1 yes;
PARITY_5 m=1 no (chain gives m=2) ⇒ W_3(PARITY_n) = n−3 CONFIRMED for n ≤ 5. n = 6 lower bound (m = 2 impossible) NOT verified
(4^32 maps; needs symmetry reduction). H2, H3: no checkable result. Finite evidence only; no ledger entry.
Stack fault found 2026-11-17 18:55: iterations 4/5 never started — AnanasMe rejects messages > 4000 characters ("Nachricht muss
1–4000 Zeichen enthalten"), and accept.sh discarded the POST response and then summarised the PREVIOUS mission as if it were the new one.
Fixed in /root/contracts/longrun-2026-11-15/accept.sh (backup accept.sh.bak-20261117): POST response printed, exit 1 if no new mission.
Requests 04/05 shortened to ~3.2k chars and resubmitted (outputs pnp-iter04-03.out, pnp-iter05-03.out).

## Owner mission brief 2026-11-17 late (3): "OpenAI Cross-Theorem Proof Mining"
Sources acquired: openai/math @4eaee87 (literature/sources/openai-math/repo, 3.7 GB working copy), NS blowup PDF (cdn.openai.com; not in
the repo). PI audit: theory/T33-openai-cross-theorem-proof-audit-2026-11-17.md. Verdict (pending review): no implication to P ≠ NP;
F2 (fluid computation) is computability-only by its own statements and Lean signature (no efficiency, no tolerance, no time–step
bound); I4, I5 refuted as routes, I1/I3 conditional on missing compiler/time lemmas and outside NP anyway, I2 open at PDE level and
inapplicable. Review mission req-pnp-iter06.json chained after iterations 4 → 5.

## Owner correction 2026-11-17 late (4): scope to publication state of 10 Nov 2026 — NEW MAIN QUESTION
"Which invariants are common to the two independent SAT proofs (OpenAI, Anthropic), and what stronger statements follow from them
together with the proved simulation theorems?" Sources verified + local copies (T34 §0); one source not found ("What the ETH
Refutations Do Not Give"). PI synthesis: theory/T34-eth-refutations-joint-invariant-and-transfers-2026-11-17.md — common invariant =
signed factorization rank of grouped equality constraints via low-degree parity representations; T28 restated (Lemma G vacuous at
arity N^{9/10}); candidate C1 (Valiant + Lemma 1.3 + JMV ⇒ E^NP ⊄ SIZE-DEPTH(c n √log n loglog n, O(log n)) i.o.), CONDITIONAL, novelty open;
correction: NE lower bounds do not pad down to NP. Conflict of interest noted (Anthropic paper by Claude): verification by non-Claude
workers only. Iteration 6 request rewritten to this question (T33 Navier–Stokes audit stays as recorded; its review folded into the
backlog). Queue: iteration 4 (running) → 5 → 6.

## Owner mission brief 2026-11-17 late (5): "Turing Machine Foundations & Universal Lower-Bound Research" (PNP-TRANSFER-001)
Integrated artifact: theory/T35-turing-machine-information-transfer-theorem-audit-2026-11-17.md. Block simulation (2611.11832)
reconstructed: gain = oblivious-simulation overhead moved inside constraints + enumeration of head patterns (density-2 interface graph).
New PI lemmas (unverified): U1 (interface count Θ(dT)), B1 (min interface = optimal time: restatement), K1 (narrows T31 C1: time→space
simulations + space hierarchy beat the n² communication cap; via OpenAI #137 offline 1-tape n^{5/2−ε}, via Williams 2025 multitape
n^{2−ε}, for a linear-space language), D1 (SAT ∉ P ⇐ [∀ε DTIME(t) ⊆ DSPACE(t^ε)] ∧ [SAT ∉ DSPACE(n^δ)]). Verdict N: no measure is
both representation-invariant and independently bounded for SAT. Verification: req-pnp-iter07.json chained after iteration 6.

## Owner evaluation of the Grok report 2026-11-17 late (6): narrowed to "Information-Transfer Falsification Test"
theory/T36-information-transfer-falsification-test-2026-11-17.md: owner's facts checked in 2611.11832 (one-tape chain; "by necessity
does not relativize"); candidate measures μ1 (realised patterns = 0), μ2 (variety ≤ n per boundary, Lemma E1; forced only at input
cuts ≤ fooling-set cap), μ3 (= time, B1), μ4 (≤ n²/4+n) excluded — Theorem F. Lemma N: normal forms are free ⇒ the normalised
obligation is "SAT has no P-uniform poly-size circuits". Non-relativizing ingredient located: white-box engine on explicit local
encoding (= Williams' method). PNP-TRANSFER-001 NOT accepted. Iteration 7 request narrowed to this test (+ one-tape palindrome
crossing-sequence computation, two implementations). No new large mission.

## Owner direction 2026-11-17 late (7): "Algebraic interface compression with alias correction"
theory/T37-algebraic-interface-compression-alias-correction-2026-11-17.md: owner counterexample (c_t = 41 ≡ 0 mod 41) and multi-prime
theorem verified (condition p−1 > D; pseudo-polynomial cost); OpenAI subset-sum alias mechanism confirmed in source (needs a complete
alias list). Reduction: by 2611.11832 Thm 2 the TM layer adds nothing — question = beat 2^{O(n/√log n)} for density-O(1) circuit-CSP.
Success would refute Weak ETH/SH, not prove P = NP; lower-bound payoff only via Williams (E^NP/NEXP). Iteration 8 chained after 7.

## Owner research transfer 2026-11-17 late (8): exact state compression / observable spaces
theory/T38-observable-spaces-exact-abstraction-2026-11-17.md — proved (PI): O1 sandwich log_q N ≤ dim V_F ≤ N; O2 nonlinear test system
(binary counter, top bit): dim V_F = 2^{n−1}+1, N = 2^n, decision O(n) — computed n = 2..12; O3 conjugated linear system: dim ≤ n+1 but
exponential circuit complexity (counting); O4 alias tags must carry Nerode information at every step + explicit spurious-path
counterexample; O5 single-run observable spaces have dim ≤ T+1 (no P vs NP lever). Universal compression / universal impossibility
claims rejected. Iteration 9 chained after 8. Ledger: after review only.

## Iteration 4 evaluation (PI, 2026-11-17) + recurring stack faults
Mission 51a47598 (T31 review): COMPLETED UNVERIFIED, 53 steps done / 9 abandoned; computations trivial (cube graph Q3 built — not an
expander); no refutation, no confirmation of L1/C1/C1b/C2/D. Content value: nil. T31 stays PI-only.
Recurring faults (iterations 3 AND 4), diagnosed, NOT changed (missions running back-to-back; deploy only with no worker, owner rule):
F-1 SYNTHESIS_FAILED with EXECUTION_NOT_CONFIRMED_TIMEOUT at attempt 1 → PeachMe-current/src/peachme/mission.py ~l.333: any code not
    starting with EXECUTION_NOT_PERFORMED / EXECUTION_OUTPUT_UNUSABLE returns None at once (deliberate: an unconfirmed step must be
    reconciled by the host, no blind retry). Effect: every mission whose wording call times out ends without a synthesis.
    Fix options need an owner decision (e.g. after host reconciliation of the UNKNOWN step, allow one wording retry on another lineage).
F-2 Claim checks INVALID:NO_JSON: checker workers are very small models (allam-2-7b, nemotron-3.5-bolt-e4b) that do not emit the JSON
    verdict → every check NOT_CHECKABLE/INVALID. Checker role needs a minimum capability (selection rule in Aurora/PlumMe; owner decision).
Consequence for research: until F-1/F-2 are fixed, missions deliver computations but no verified verdicts; PI spot-checks remain the
only verification (iteration 3: parity W_3 confirmed n ≤ 5 by PI).

## Stack repairs 2026-11-17 ~20:50 CET (owner: "reparieren") — deployed with no worker running, rollback lines in ROLLBACK.txt
- F-1 PeachMe 668c192 (cc/answer-claims): a settled EXECUTION_NOT_CONFIRMED wording is repeated on another lineage (research-pool rule);
  an open step still stops. Test test_a_settled_timeout_of_the_wording_is_repeated_by_another_lineage_but_an_open_step_is_not
  (fails before, passes after); PeachMe suite 524 tests, only the Pomelo-environment file fails (pre-existing, needs its own env).
- F-2 CherryMe 439a31f (cc/certified-grader) + Aurora d970a1d (cc/decision-contract): claim-check workers request PlumMe's per-call
  exclude_small_models (≤12B and nano/lightning class); Aurora's research verifier uses the new claim_check_worker().
- F-3 CherryMe 3108f24: program_check gives a verdict only for a claim with ONE distinct figure — live 113f17a8 falsely REFUTED E1
  (qualitative claim with figures k≥3, 2003, 2015, n^3; small-model programs agreed on "1"). CherryMe suite: 984 passed, 13 failed =
  the same 13 as before the changes.
## Iteration 5 evaluation (mission 113f17a8, old stack)
PARTLY_VERIFIED; the only "verified" item is the FALSE refutation of E1 (F-3) — E1 stands as PI result (T32), unaffected. W1 cat-map
computation: δ_π(t) periodic (finite permutation; as T32 W1 states for finite Ω), numbers under open objection. No usable verification.
Queue restarted on the repaired stack: iterations 6 → 9 (outputs pnp-iterNN-02.out).

## 2026-11-17 — Owner re-brief "Exact State Compression" prioritised
- T38 extended with Lemma O6. It gives an exact, constructive and compositional closure of bounded ANF degree: h = evaluation of the basis, transitions are linear maps C_a, there is no tag or checksum, and the cost is polynomial in n for constant degrees.
- Test systems:
  - quadratic accumulator: d = k+1 (positive case);
  - counter: D ≥ n−1 is required, proved for all n via F∘δ ⊕ F = x_0⋯x_{n−2}.
- Computation: scratchpad closure.py checks the closure against an independent truth-table closure; 0 mismatches.
- Queue reordered: iteration 6 (running, a7954e5d) is followed by iteration 9, which verifies T38 O1–O6 (request extended with O6, backup req-pnp-iter09.json.bak-o6), then iterations 7 and 8.
- No ledger entry before iteration 9 plus independent review.
- T38 §3c added: O7 (linear abstractions need ≥ d coordinates; counter separates linear from nonlinear compression) and O8 (explicit φ-conjugate family with d = n, degree n−1, O(n) evaluation; the degree method needs D = n−1). Computation in scratchpad o8.py. Iteration 9 request extended with O7/O8 (3.9k chars).

## 2026-11-18 — Iterations 6 and 9 hit the wall; stack fault F-4 repaired
- a7954e5d (iteration 6) and b4968eda (iteration 9) both ended BLOCKED with MISSION_WALL_BUDGET (3600 s), without an answer and with every claim UNKNOWN.
  - Iteration 9 recorded no computation.
  - Iteration 6 recorded two exploratory runs (Qwen2.5-VL-72B, GF(2)/GF(3) ranks), unchecked and not used.
  - The PI results of T38 are unaffected and remain pending verification.
- F-4: the reserve for decision + synthesis + result was 300 s. Live b4968eda:
  - research ended on time (21:46:50Z);
  - the first wording timed out after 180 s;
  - the F-1 repeat r1 finished in 27 s, but was most likely cut at its token limit and widened;
  - r2 was killed by the wall at 21:51Z.
  - So F-1 works, but the reserve was too small.
- Repair: Aurora 9cc3c3c, `synthesis_reserve(wall)`. Hour-long research now keeps 600 s; the 900/150/60 s lanes are unchanged.
  - Test written first: tests/test_synthesis_reserve.py.
  - Suite: no new failures.
  - Deployed 2026-11-18T02:02Z, rollback line in ROLLBACK.txt.
- Queue restarted in the order 9 → 7 → 8 → 6 (outputs pnp-iter*-03.out).
- Open observation (not changed): the research lineages are mostly gemma/qwen2.5/qwen3.5. Model choice for the research workers is to be checked after the next run.
- 2026-11-18: T39 (approximate 𝔽_2-degree ⇒ SAT ∉ subexponential AC^0[⊕] via an explicit projection MAJ→SAT, checked n ≤ 9; barrier statement for P/poly). PI-only, verification queued after iteration 9.

## 2026-11-18 — Iteration 9 (d6d314b7) COMPLETED on the F-4-repaired stack; T40 started
- First research mission with a synthesized answer after F-1..F-4. The O6 objection was answered (wrong model F; recomputed
  d = k+1 for k = 3..8); the record is in T38. CherryMe checks: NOT_CHECKABLE.
- New owner mission "Algebraic Reachability, Subset-Sum Saturation". T40 written (Theorems A, C, D, E, G, H; certificates), all
  computationally checked in lab/exp5x/. Experiment 5 extension running (sim.py).
- 2026-11-18: T41 written (colour-filter criterion CF = T38 Finding E/O7, direction CLOSED; 1-in-3 Fourier dual D1, mod-3 NAE identity D3, read-twice Pfaffian D4; all exact-checked in lab/onein3). Experiment 5 extension restarted with incremental saves (lab/exp5x/sim.log). Queue unchanged: iter 7 done (4fac7453 COMPLETED), iter 10 (T40) running.
- 2026-11-18: T42 (CRT Subset Sum: SEP = solvability over idempotents, JOINT exact iff no subset sum ≡ t mod M besides t, threshold M > max(t, Σw−t); 7200 rows lab/crt). T41 §5 gadget search: no OR-gadget in positive 1-in-3 with ≤3 aux/≤3 clauses (open whether ⊕-top-coefficient is ⊕P-complete for this class).
- 2026-11-18: T41 §6: parsimonious reduction 3-CNF → positive 1-in-3 (functional AND/OR gadgets found and verified; 300/300 exact counts). Top-ANF-coefficient extraction for 1-in-3 products is ⊕P-complete (Theorem P). Next: occurrence bound k between read-twice (P) and ⊕P-complete.
- 2026-11-18: T41 §7: owner's mod-3 linearisation + mod-7 dual verified (also mod 13, 19); exact structure: C = Boolean-word count of the affine ternary code Ax=1, owner's sum = MacWilliams transform; cost 3^min(r,n−r).
- 2026-11-18: T41 §8: multilinearisation identity C = 2^n ML(F)(1/2) verified (also mod 3,5,7,11); read-twice ML = weighted perfect-matching polynomial (100/100): planar = Pfaffian/VP, general = permanent-type.
- 2026-11-18: T41 §9: owner's 2^(n-r) primal + integer dual C=(W0−W1)/3^r verified 300/300; bound O*(1.530^n); Theorem S (translation symmetry, 200/200): W0−W1 is the MacWilliams image of the primal count.
- 2026-11-18: T41 §10: owner's D5 (≤2 occurrences, det mod 2, no planarity) and D6 (principal-minor sum over disjoint H-selections) independently re-checked 700/700 each; read-≤3 reduction check interrupted, UNVERIFIED.

## 2026-11-18 — Iteration 10 evaluated; T41 §10b/§10c; iteration 11 queued
- Iteration 10 (80b3922a, T40) COMPLETED after 3287 s.
  - Its "refutations" of A and D are based on defective agent code; details in the T40 verification record. Not binding.
  - Stack observation (candidate F-5, NOT changed): in iterations 9 and 10 the research computations came almost only from
    Qwen2.5-VL-72B, and it modelled the objects wrongly (groups as lists, missing mod n, a claim applied outside its stated
    scope).
  - CherryMe correctly marked everything NOT_CHECKABLE / UNVERIFIED, so no false ledger entry was made.
  - The weak point is research-worker quality, not verification. To be examined: model choice for research workers. Owner rule
    respected: no architecture change without an order.
- T41 §6 OR gadget transcription corrected (ū, not l̄₂); both gadgets re-verified exhaustively.
- T41 §10b (owner's read-≤3 hardness proof, 150/150 checks) and §10c (differential filter, 120/120, sympy) added.
- Owner instruction "use FruitStack whenever possible": req-pnp-iter11.json (narrow adversarial check of T41 G1–G3, P, R3, D5,
  D6/F) queued directly after iteration 8 (running), before iteration 6.
- Experiment 5 (lab/exp5x/sim.py): the subgroup closure walked g, 2g, 3g, … (up to 2^18 full-array passes) and stalled at Z/2^18.
  Replaced by doubling (g, 2g, 4g, …); self-check against the single-step closure 100/100. Restarted 2026-11-18. Partial results
  up to Z/2^14 kept in sim.out.partial-0511.json.
- PI process error: the old simulation was stopped with a pattern match, which also hit the PI's own shell (memory rule "no pkill
  -f" violated in substance). No data lost. From now on processes are stopped only by individually checked PIDs.
- 2026-11-18: T41 §11: owner's product identity verified 150/150 (sympy); char-2 obstruction to Waring confirmed; PI remark: R ≅ F_2[(Z/2)^m] local ring (no Fourier in char 2).
- 2026-11-18: T41 §12 Lemma L (form-preserving basis changes over F_2 = clause permutations only). Waiting for iteration 11; no further mission.
- 2026-11-18: Experiment 5 extension COMPLETE (972 rows); T40 §5 filled: bounds 0 violations, (Z/2)^r exact law 77/81 in 95% CI, Poisson fails for (Z/2)^r and for full coverage, small generators collapse in cyclic groups.
- 2026-11-18: T41 §13: Reynolds projection rejected (owner counterexample); fixed-point reduction FP + PI quotient preprocessing verified 151/151, quotient→D5 124/124 (87 originally read≥3). External modules not integrated (not available to PI; owner-reported defects recorded).
- 2026-11-18: T41 §13b: owner's incidence-twin lemma + procedure verified (178/178 finished correct, 106 originally read≥3; 53 stuck); confluence not proved. T40 §5 placement by owner noted.
- 2026-11-18: owner order: technically failed runs are documented and repeated. Register: protocol/FAILED-RUNS-REGISTER.md (12 local + 9 mission entries). Queued reruns: it. 6, 4, 5, 10 after it. 11; anf_top parts 4–5 rerun OK; read3 regression rerunning.
- 2026-11-18: PI decision (owner: 'you are the scientific leader'): it. 12 (T39) and it. 13 (T38 O3/O7/O8) queued after the reruns.
- 2026-11-18: novelty audit started (protocol/NOVELTY-AUDIT-T41.md): D5 = Björklund 2010 Lemma 4.2 (known); D6 close variant; AUT-2→D5 only candidate, composition of known results.
- 2026-11-18: T41 §14: planarity clarification (Pfaffian only for read-twice), owner's literature (Moore–Robson, Cai–Fan) recorded unverified, Hadamard signatures recomputed, mod-2 coefficient-cancellation heuristic rejected, extended quotient→holographic class recorded as research object.
- 2026-11-18: T41 §14b: owner's counterexamples recorded (EQ4 Grassmann–Plücker fails; cube instance 0 solutions vs 9 matchings, PI-verified); external 18-variable prototype rejected; no new mission.
- 2026-11-18: T41 §13c (AUT-2/MOD-P verified on n≤7: 285/285, 81/81, 283/283, 83/83) and §14c (owner's defects in external matchgate verifier) recorded; register L13 RERUN-OK.
- 2026-11-18: T41 §14d: owner's equality rule (exact, 16/16) and GL2 no-go (PI Groebner basis {1} for both signs) recorded; external Cayley miner rejected.
- 2026-11-18: T41 §14e: owner's MG-3 recorded and PI-checked (f′ formulas, parity⇒monomial via Groebner radical); propagation sound-not-complete counterexample verified (count 3, x0=0).
- 2026-11-18: T41 §14e: Cai–Gorenstein ToC 10(7) 2014 checked at source; MG-3 even case now via Thm 7.1 (symmetric matchgate characterisation); sharpness d=2 recorded.
- 2026-11-18: owner's exact GL2 matchgate solver reviewed + run (self-test 10/10; read2 FOUND; mg3/eq4/super4 PROVED_NO_BASIS; PI hidden-basis test FOUND T=[[1,1/2],[2,2]]); T41 §14f.
- 2026-11-18: T41 §14f certified: Singular-lift Nullstellensatz certificates (certs/*.json) + independent pure-Python verifier mg_verify.py (re-derives branch systems; 5/5 OK; 4/4 tamper tests rejected).
- 2026-11-18: T43 written (owner's obligation: what follows for ALL poly-time algorithms). Unconditional: nothing (reason stated). Conditional: C1–C3. Bridge: Lemma B (circuit → read≤3 1-in-3 with functional backdoor) + Williams; open question Q-BD (2^n/n^ω(1) in backdoor size). Mishra–Santhanam 4n claim: owner-reported, not located.
- 2026-11-18: owner course correction: back to T11-B. T11-Q written: Q1 (proved: char-2 structures of T41 cannot separate, perm≡det mod 2), Q2 (FP/MOD-P certificates for nonvanishing of tableau sums = lower bounds on γ_λ; not yet carried out), Q3 (orbit-vs-closure toy for MG-3; parked). T43 paused.

## 2026-11-18 afternoon - state for continuation (PI)
- Staging (scratchpad .../staging): lab socket mcp.sock (worktree PhysalisMe, PHYSALIS_SANDBOX_PYTHON=/opt/fruitstack/venv-physalis/bin/python),
  desk loop (pnp_desk.py, AppleMe assurance), invention rounds (pnp_invent.py), research cycles (pnp_research.py, 3 cycles running/done),
  universe demo (lab/universe/demo.py -> demo_result.json), proofbook COPY staging/proofbook.jsonl (live proofbook untouched).
- Commits (not pushed, not deployed): PhysalisMe cc/physalis-math-verification a350778..9009e56 (+ circuits.py uncommitted),
  Aurora-sync cc/decision-contract 68ad36b..0de1ed7, AppleMe cc/proofbook-atomic-append 7273e9c. accept.sh replaced (ROLLBACK.txt lines).
- Findings today: D-002 read-twice=>SAT refuted (n=24); D-004/D-008 F3 exact for m<=4, blind 24%/37% at m=5/6; D-005 = special case of D6;
  agent GF(3) rule (alg-f496d8017c75) refuted (n=8,m=6,C=0); capability assessment protocol/CAPABILITY-ASSESSMENT-2026-11-18.md;
  literature review literature/reviews/LIT-REASSESSMENT-2026-11-18.md; history catalog lab/reassessment/catalog.jsonl (204 statements).
- Running: exact circuit-size calibration vs Knuth n<=4 (physalisme/circuits.py, pysat/CaDiCaL), next: SAT slices (1in3 vs xor3 vs 2sat).
- Open: CherryMe check of D-004 (mission c291b215) result; iteration 12/13 chain waiting for the Aurora slot; nothing live deployed.

### Brute-force circuit track (2026-11-18, later)
- physalisme/circuits.py committed be3e769 (cc/physalis-math-verification): Knuth n=4 calibration PASSED (222 NPN classes, 195 s).
- D-010 (owner + independent recount): 1in3 n=5 slice, 87 MUS. Controls: xor3 needs both right sides; xor3 n=4 has only trivial MUS (size 2) -> matched-k sub-families from n=5 universes.
- Running: lab/circuits/matched_k.py 6 40 (PID 2631841, timeout 4 h, resumable, matched_k.jsonl). First 6 rows: 1in3 size 7 (3 MUS) vs xor3/2sat size 5 (1-2 MUS) - CONFOUNDED by MUS count; analysis must stratify by MUS structure.
