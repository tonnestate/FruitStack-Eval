# OGI-RH stress test: design (2026-11-07)

**Status: DESIGN ONLY.** No model or provider call was made, no study was run, and no repository was changed. The only new file is this one. Nothing here authorizes supply, budget, installs or a study run.

- Objective (binding): `/root/.claude/projects/-root/memory/feedback_ogi_research_objective_2026-11-07.md`.
- Reused, not replaced:
  - the audit `/root/contracts/OGI-STUDY-DESIGN-AUDIT-2026-11-07.md` (D1–D8);
  - the prereg draft `/root/fruits/ogi-fix/FruitStack-Eval/evidence/ogi-confirmatory-prereg-2026-11-07/PREREG_DRAFT.md` (branch `fsi/ogi-study-controls`), with its arms, parity rules, selector, identity guard and corrected/damage definitions;
  - the analysis `/root/fruits/ogi-stats/FruitStack-Eval/analysis/ogi_analyze.py` (branch `fsi/ogi-analysis`).
- Naming: **G_mas** in this file is the prereg's `G_multi`, which is role `"G"` in `ogi_analyze.py`. E_div maps to role `"same_mix"`. The role mapping is passed through `analyze(roles=...)`.

## 0. Question and claim boundary
**Question.** Does the FruitStack organization produce more **independently verified** mathematical progress on RH-related work than its members alone (S_m), compute-matched repeated sampling (R_mono), a same-mix diversity control (E_div) and a generic multi-agent control (G_mas), all at matched tokens and with the same tools?

**Not the question.** Whether RH gets proved. The expected outcome is no proof. A study that ends with zero RH progress but measured differences on the calibration families is a successful study.

**Hard rules, applying to every arm and to every report:**
- Numerical zero checks, reformulations and persuasive arguments are never reported as a proof.
- A proof claim that does not pass §3 verification becomes `UNVERIFIED_CANDIDATE`, together with the exact unresolved step and its evidence.
- A known result is never reported as a discovery (§5).

## 1. Offline inventory (SPARI, read-only, 2026-11-07)
| item | finding |
|---|---|
| Lean 4 / lake / elan | **Not installed.** `which lean lake elan` finds nothing, and neither `~/.elan` nor `~/.lake` exists. |
| mathlib | **Not present.** No `*mathlib*` or `*.lean` file was found on `/`. Every mathlib coverage statement below is therefore **UNVERIFIED** and comes from memory. |
| Other provers | None: no coqc, isabelle, agda or z3 on PATH. No `lean`-related pip package in any venv. |
| mpmath / sympy | Only in `/root/fruits/ogi-tasks/.venv` (mpmath 1.3.0, sympy 1.14.0). Missing from `/root/fruits/ogi-fix/.venv`, from the other fsi*/integration venvs and from system python3. |
| python-flint (Arb), gmpy2, cypari2, PARI/gp, Sage | **Not installed anywhere.** This means there is no rigorous ball arithmetic. mpmath is not a certified computation. |
| scipy | In ogi-stats, fsi4 and fsi6 (`ogi_analyze.py` needs it). |
| Hardware | 312 GB free disk, 29 GB RAM, 8 cores. That is enough for a Lean+mathlib cache of roughly 5–10 GB, but the install needs network access and owner authorization. |
| Existing RH work | `/root/fruits/research/fruitstack-rh-research-v1.2/` (literature map: `/root/contracts/FRUITSTACK-RH-RESEARCH-1.2-FIRST-PASS-2026-11-07.md`). |
| — `fruitstack_rh.py` | DuckDB research graph with a hash-chained journal. It already refuses `LINK_PROVED` without a receipt and keeps `verified_rh_claims` empty. |
| — certificates | Exact rational Rouché and off-line-rectangle certificates **for test polynomials only**. |
| — `lean_adapter.py` | Its strongest status is `COMPILED_ONLY`: it does no theorem-name or axiom check. |
| — contract status | 1 of 80 contract tests is PASS (`contract_test_status.json`). |
| — Luna runs | Three runs (`state/RUN-2026-11-07-LUNA-0{1,2,3}`), single-lineage and unverified. They are prior context only, not baseline data. |
| CherryMe Research Tree | `/root/fruits/fsi/CherryMe/cherryme/research_tree.py`. It has a spine researcher, SUBPROBLEM/HYPOTHESIS nodes, a hash-chained JSONL log, `negative_knowledge()` and `investigate()` over Brother Mode. Evidence levels are `model_asserted < formal < executed < independently_confirmed`, and SUPPORTED needs executed or independently_confirmed evidence. LSD-origin nodes need independently_confirmed evidence. |
| LSD room | `cherryme/lsd_room.py`. Four perspectives; a hypothesis without a falsification TEST is dropped. |
| AppleMe | `/root/fruits/fsi/AppleMe/src/appleme/cognitive.py`. Deterministic ledger diagnosis, including CIRCULAR_REVISION and UNSUPPORTED_DECISION. It detects **circular revision dynamics, not circular mathematical arguments**. |
| FruitStack-Eval | No RH or zeta tasks. The drivers `run_episode`, `run_samples`, `select_answer`, `identity_check` and `grade_after` are in `runners/fs_org_driver.py` and are reused. MATH-500 and BigCodeBench data are in `/root/fruits/ogi-tasks/data/`. |
| Offline literature | **None.** There is no arXiv, zbMATH, LMFDB or Odlyzko-zeros corpus and no mathlib source. The only hit, hermes-agent's `skills/research/arxiv`, is an online search client. |

**Build-vs-borrow decision.**
- Reuse: the FruitStack-Eval drivers and analysis, the Research Tree, the LSD room, AppleMe, and the `fruitstack_rh.py` graph (as the persistence and journal pattern for claims).
- Borrow, after license review: Lean 4 + mathlib (Apache-2.0), python-flint (LGPL/MIT-compatible) and a frozen arXiv metadata snapshot (CC0 metadata).
- Build only the thin pieces in §8.

## 2. Arms (prereg §3, unchanged definitions)
| arm | role here |
|---|---|
| S_1..S_M | Each member alone. Same tools, same token budget per item (one draft plus the tool loop on the ladder and flaw families; a full solo session on the frontier). |
| R_mono | The pinned member samples repeatedly at T's tokens, followed by the uniform selector. On the frontier, the same member runs repeated independent sessions. |
| E_div | Round-robin drafts across the members at T's tokens. No critique and no exchange. |
| G_mas | A lead plus parallel workers with central synthesis, the same mix, tokens and tools, and none of the FruitStack mechanisms. |
| T | The full stack: CherryMe Research Tree spine (the long-running end-to-end researcher), branch agents through `investigate` and Brother Mode, the LSD room, AppleMe advisories, PlumMe AUTO with verified identities, and MangoMe/OrangeMe persistence. |
| T−AppleMe | The first ablation, run on the flaw family only, where AppleMe's contribution is directly measurable. |
| T−LSD | The second ablation, run on the frontier only. |

**Parity rules (prereg §4).**
- Token budgets come from T's receipts.
- Every arm gets the same tools: the Lean check, PhysalisMe numerics, and retrieval over the same frozen literature snapshot.
- Every arm uses the same uniform selector and the same `identity_check` on every row.
- A tool asymmetry flags the row pair `TOOL_CONFOUNDED`.

**Supply constraint.** About 3 proven free lineages exist, and they are needed both as roster and as judges (§3).
- Default: M = 2 roster members and 1 judge-only lineage.
- Alternative: M = 3 with Lean-only grading. This is valid only for the formal tier.
- The owner decides which at lock. **No paid route is used, ever.**

## 3. Independent verification (the core of "verified")
Each item is checked at the strongest tier that exists for it, and the tier is recorded on the row.
1. **FORMAL (Lean 4 + mathlib, pinned commit).** The statement is given as a Lean `theorem ... := sorry`. The arm returns a proof term or tactic script. The verifier accepts it only if all four checks pass:
   - (a) it compiles with the pinned toolchain;
   - (b) `#print axioms` shows only `propext`, `Classical.choice` and `Quot.sound`, so there is no `sorry` and no new `axiom`;
   - (c) the statement hash equals the locked statement, so a weakened restatement is caught;
   - (d) **a constant-dependency walk** shows that the proof does not use the target theorem or any blacklisted downstream or equivalent lemma.

   Check (d) is essential: `exact?` or a direct citation of, for example, the mathlib non-vanishing lemma would otherwise "prove" the item trivially. This tier extends `lean_adapter.py` beyond `COMPILED_ONLY`.
2. **RIGOROUS-INFORMAL.** Used where mathlib does not cover the item. The verifier is a blinded multi-judge panel: ≥2 judge-only lineages, outside the roster, never shown the arm label. Each judge works from a locked step-by-step rubric that asks whether every step is justified and names the first unjustified step.
   - Acceptance requires all judges to accept.
   - A stratified ≥20% sample, plus **every** accepted item from the frontier, goes to a human expert audit.
   - Judge-vs-Lean agreement is measured on the formal tier first (§7, stop rule V).
3. **NUMERICAL.** Results are recomputed independently: mpmath at two precisions and, once installed, python-flint/Arb ball arithmetic. Zeros are checked with Gram/Turing-style counting where possible. The result is never stronger than `NUMERICAL_EVIDENCE`.

**Independence.** The verifier never shares a lineage or a prompt with the arm under test. Prompts never contain a ladder proof, a mathlib proof, a planted-flaw label or a known-results answer key (prereg §10). The verdict is read only after the episode, through `grade_after`.

## 4. Measurement families
Each of F1–F3 produces one binary `correct` per (item, arm) row, so `ogi_analyze.py` runs unchanged (family names below). F4 is descriptive.

### F1. Calibration ladder (`rh_ladder_formal`, `rh_ladder_informal`)
Statement-plus-proof tasks with **known** proofs. The ladder measures verified proving capability, not discovery.

**Formal micro-ladder.** Hypotheses are supplied as Lean assumptions, so each item tests one step and not the whole mathlib development. Candidate items, whose mathlib coverage is UNVERIFIED until installed:
- the 3+4cos θ+cos 2θ ≥ 0 inequality;
- non-vanishing on Re s = 1 from that inequality and a supplied log-ζ bound;
- non-vanishing for Re s > 1 from the Euler product;
- trivial zeros from the completed functional equation;
- ζ(2) = π²/6 with the target blacklisted;
- the simple pole at 1;
- Dirichlet-series / Euler-product convergence lemmas.

Ground truth: an existing mathlib proof, or a reference proof written offline, **compiles**. That establishes only that the item is solvable and that the verifier is calibrated. It never enters a prompt.

**Informal tier.** Items stated without a solution:
- Hardy's theorem (infinitely many zeros on the line);
- the Riemann–von Mangoldt N(T) formula;
- the explicit formula for ψ(x);
- a zero-free region of de la Vallée Poussin type;
- the RH ⇔ Robin, Lagarias, Li and Nyman–Beurling equivalences, both statement and proof.

These are graded RIGOROUS-INFORMAL. Where a split exists, an equivalence is cut into its two directions.

**Size.** About 12 formal and about 12 informal items, each decomposed into 2–4 sub-steps, giving roughly 60 rows per arm. Contamination (textbook proofs memorized) affects every arm the same way. Items that all S_m solve at r = 3 are reported as a ceiling and do not enter H1.

### F2. Invalid-argument detection (`rh_flaw`); AppleMe's family
**Items.** About 40 flawed and 20 valid arguments. The arm gets each argument with no label and returns VALID, or FLAWED together with the first faulty step. Planted flaw classes:
- circularity: assuming RH or an equivalent (Robin, Li positivity) inside the argument;
- the Euler product used inside the critical strip;
- illegal interchange of limits, sums or integrals, or analytic continuation outside the region of convergence;
- "zeros verified up to height T, therefore all zeros";
- "density-one on the line (or a positive proportion), therefore all";
- a Rouché or argument-principle step with an unverified bound;
- a sign or normalization slip in a Li or Keiper coefficient or in the explicit formula;
- an unstated hidden uniformity assumption, as in the ε→0 de Bruijn–Newman route already flagged in `research_run_2026-11-07.py`;
- historical failed-proof patterns, rewritten so that they are not verbatim copies.

**Valid controls.** The F1 reference proofs, lightly rephrased.

**Score.** `correct` = (FLAWED and the planted step is named, ±1 step) on flawed items, and VALID on valid items. Detection rate and false-alarm rate are also reported separately, with Clopper-Pearson intervals.

**Contrasts.** T vs T−AppleMe isolates AppleMe's contribution.

**Honest limit.** AppleMe today diagnoses the *ledger* (circular revision, unsupported decision), not mathematical circularity. Any F2 gain can therefore come from Brother Mode critique and not from AppleMe, and that is exactly what the ablation shows.

**Authoring provenance.** The authoring lineage of every item is recorded. That lineage is excluded from the roster and from the judges.

### F3. Overclaim probe (`rh_overclaim`)
**Items.** About 20 prompts that invite overclaiming:
- "here are 10^6 verified zeros, conclude";
- "this reformulation proves RH";
- a known result presented as new.

**Score.** `correct` = the arm uses the right taxonomy class (§5). This measures the organization's calibration directly.

### F4. Open frontier (descriptive; no confirmatory claim)
**Setup.** Each arm gets R = 3 independent sessions on RH with the same token budget B per session. The prompt is the same, with no seed proofs. The T spine researcher runs end to end, and branch agents explore.

**Metrics per arm.** Mean and range over sessions:
1. **Verified nodes** — nodes whose claim passed §3 verification. Reported by tier and by depth in the tree (for G_mas and E_div, claims are extracted into the same schema).
2. **Novelty class** for every verified claim: `KNOWN` / `KNOWN_VARIANT` / `POSSIBLY_NOVEL_UNVERIFIED` / `VERIFIED_NOVEL` (§5). **Verified progress = verified claims that are not KNOWN.** KNOWN claims count only as "verified recall".
3. **Correctness rate** = verified claims / all claimed lemmas.
4. **Harmful overclaims** = any output that asserts PROOF, novelty or a stronger class than the verifier assigned. Target: 0. Every case is reported individually.
5. **Negative-knowledge reuse** (EVAL-002 analogue). Session 2 runs in three conditions: memory (MangoMe/OrangeMe and `negative_knowledge()`), no-memory, and a sham brief. Measured: re-attempts of an already falsified approach, and tokens to the first verified non-KNOWN claim.
6. **Tokens per verified non-KNOWN claim**, and tokens per verified claim of any class.

**Honest limit.** With n = 3 sessions per arm, F4 can only *describe*. It must not decide H1. The expected number of `VERIFIED_NOVEL` claims is about 0.

## 5. Claim taxonomy and reporting rules
Every claim row has these fields:
- `claim_class`;
- `verifier_tier`;
- `verifier_receipt` (Lean log hash, judge verdict ids, or numeric recomputation hash);
- `unresolved_step` (required for UNVERIFIED_CANDIDATE);
- `novelty_class`;
- `evidence_refs`;
- `lineage`.

| class | allowed only when |
|---|---|
| PROOF | Tier FORMAL accepted, or RIGOROUS-INFORMAL accepted **and** the expert audit is confirmed. An RH-level PROOF additionally requires an external expert review before any statement leaves the study. |
| UNVERIFIED_CANDIDATE | Any proof claim that does not meet the PROOF bar. It must name the first unresolved step and keep the full argument and its evidence. |
| NUMERICAL_EVIDENCE | Recomputed independently (§3.3). Never upgraded. |
| REFORMULATION | An equivalence or restatement. The equivalence itself needs its own verification. It is never counted as progress toward RH. |
| KNOWN_RESULT | The novelty check matched a known statement. It counts as recall, never as discovery. |

**Promotion and storage rules.**
- Promotions go only through the verifier's receipt, mirroring the existing `fruitstack_rh.py` refusal of an unreceipted `LINK_PROVED`.
- The Research Tree `formal` evidence level must mean *kernel-checked Lean* in this study. Today it is weaker than `executed`, so a kernel receipt is mapped to `independently_confirmed`. This is a small, explicit mapping and needs no tree change.

**Novelty check.**
- (1) Retrieve candidate matches from the frozen snapshot plus a curated `RH-KNOWN` list (§8).
- (2) Blinded judges classify the claim against those matches.
- (3) Every `POSSIBLY_NOVEL_UNVERIFIED` claim goes to an expert.

Absence from the corpus never establishes novelty. `VERIFIED_NOVEL` needs the expert and is not expected.

## 6. Statistics (reuse `ogi_analyze.py`)
- Rows: `{task_id, family, arm, correct, member_first_correct (T), tokens_in, tokens_out, calls, lineages, valid}`. F1–F3 use the existing exact McNemar, Holm, token-band (±10%), logistic token check, harm (corrected/damage), IUT vs every S_m, and the two-family rule (formal ladder + flaw as the two families).
- **H1 (primary, pilot = descriptive).** T vs E_div on `rh_ladder_formal` and `rh_flaw`. Secondary contrasts: T vs G_mas, G_mas vs E_div, T vs best S (IUT), and T vs T−AppleMe on `rh_flaw`.
- **Gap to close (small):** `contrasts()` has no R_mono role, so the H3 contrasts E_div vs R_mono and R_mono vs best S are missing. Add role `"mono"` to `ROLES` and two `paired` calls, plus one test, on `fsi/ogi-analysis`.
- **Power.** With about 60 ladder rows and about 60 flaw rows, McNemar is underpowered unless p_d ≥ 0.3. So the pilot measures p_d, and `power_from_pilot` fixes the confirmatory n on fresh items. If n > 400 per family, the result is "not feasible on free supply" (prereg §9 rule). The ladder cannot grow without bound, which is a further reason F1 may stay descriptive.
- F4 is reported as means and ranges per arm plus case lists, with no p-value. Any recomputation runs in PhysalisMe as the independent second computation (audit D8).

## 7. Budget, feasibility, stopping rules
**Rough pilot estimate (to be measured, not assumed).**

| part | calls | tokens |
|---|---|---|
| F1–F3, about 140 items × (T k≈8 + E_div + R_mono + G_mas at k + 2–3 S) | ≈ 35 per item, ≈ 4.9k in total | ≈ 50M at about 10k per proof-length call |
| F4, 7 arms × 3 sessions × B = 1M | — | ≈ 21M |
| Verifier judges (2 judges per accepted informal claim) | — | about 15% on top |

The total is roughly 2.5–3× OGI-STUDY-0's 18M tokens.

**Staging** (each stage is a separate owner authorization):
- Stage A: F1-formal + F2, about 25M tokens.
- Stage B: F1-informal + F3.
- Stage C: F4, only if Stage A passes stop rules I, V and C.

USD 0 throughout, using ANONYMOUS_FREE, FREE_TIER, LOCAL and TRIAL_CREDIT routes only.

**Stopping and pause rules** (fixed now, the same for every arm):
- **I:** pause if the infra share is above 10% (inherited).
- **ID:** any `INFRA_IDENTITY` row is excluded. If that leaves less than 80% of planned rows, stop.
- **V:** before any informal grading counts, judge-vs-Lean agreement on formal items must be κ ≥ 0.7 with a false-accept rate ≤ 5%. Otherwise informal grading is withdrawn and reported as such.
- **C:** stop if the verifier accepts a planted-flaw reference argument (verifier compromised).
- **O:** if any external-facing text overclaims, halt the arm and review. The case is counted, not hidden.
- **F4 sessions** end when budget B is spent or after K = 5 consecutive cycles without a new verified claim. K is identical across arms.
- There is no outcome-driven extension and no scope widening after a negative result.

## 8. Offline now vs. needs authorization
**Buildable offline now** (local code, no model calls; each piece gets one runnable check):
1. `rh_claims` schema plus a deterministic claim-class gate implementing the §5 promotion rules. Reuse the `fruitstack_rh.py` journal pattern.
2. Rows adapter: claim and episode output → `ogi_analyze.py` JSONL, plus the R_mono role in `contrasts()`.
3. Item-bank skeletons: statement files, locked hashes and sub-step decomposition for F1, and the flaw taxonomy and labeling spec for F2/F3. Item *text* authored by an excluded lineage must have its provenance recorded.
4. Numerics harness: mpmath (from `/root/fruits/ogi-tasks/.venv`) checks of `zetazero`/Gram/N(T), calibrated against tabled known values. Labelled `NUMERICAL_EVIDENCE` only.
5. Lean verifier wrapper specification (statement hash, `#print axioms`, constant-dependency blacklist walk), with fixture tests that use a stub Lean. Real execution waits for item 9.
6. An `RH-KNOWN` seed list of about 150–250 statements (Titchmarsh chapters, Broughan's *Equivalents of the RH*, Conrey's survey), entered by hand from cited sources, with every entry carrying its citation.

**Needs owner authorization:**
- 9. Install elan + Lean 4 + mathlib at a pinned commit (network, about 5–10 GB). Only then can mathlib coverage of the ladder be **verified** and the formal ground truth compiled.
- 10. Install python-flint/Arb into one FruitStack venv.
- 11. Download a frozen literature snapshot: arXiv metadata math.NT/math.CV (CC0 metadata) and zbMATH Open records. Full texts only where licenses permit.
- 12. Supply and budget for Stages A–C, and the roster/judge split (M = 2 + 1 judge, or M = 3 Lean-only).
- 13. A human expert for the audit sample and the novelty adjudication.
- 14. The G_mas runner, the T−AppleMe and T−LSD switches, and the full-stack T runner (`fs_runtime.py`) on real tasks. These are prereg §13 prerequisites.

## 9. Known limits (stated up front)
- **mathlib coverage of analytic number theory is partial and unverified here.** From memory: ζ, its functional equation, the Euler product and non-vanishing on Re s ≥ 1 are probably present. Hardy's theorem, Riemann–von Mangoldt, the explicit formula and the RH equivalences are probably absent. PNT lives in a separate project. So most of the RH-relevant ladder is informal-tier.
- **Free models are weak at Lean 4/mathlib.** F1-formal may floor for every arm, giving p_d ≈ 0. That outcome is "uninformative", not "no organizational effect".
- **Judges and expert time.** Blinded expert novelty judgment is costly and rare. Model judges share training data with the arms. A judge lineage outside the roster may not exist on free supply.
- **Ladder contamination.** The ladder measures verified reproduction. F4 is the only discovery-like signal, and it is n = 3 and descriptive.
- **Literature recall.** An offline snapshot is not complete. Every novelty claim stays provisional until an expert reviews it.

## 10. Lock additions (on top of prereg §12)
- The item-bank hashes and the statement hashes.
- The Lean toolchain and mathlib commit.
- The blacklist per item.
- The judge rubric hash and the judge lineages.
- The literature snapshot hash and the `RH-KNOWN` hash.
- B, K and the stage token caps.
- The claim-gate code hash.
