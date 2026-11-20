# RH-2026-ALPOEGE — Evidence audit (Phase A), 2026-11-20 ~20:45 CET

Programme: RH-2026-ALPOEGE (owner Director Command 2026-11-20). Auditor: Claude (research director). Status of the external claim:
**SOURCE_AVAILABLE** (not statically inspected by us yet, not built, not kernel-accepted, not semantically reviewed, not confirmed).

## 1 External sources

| Item | Value | Our check |
|---|---|---|
| Announcement | https://alpo.ge/remark.pdf | downloaded 20:41, 245,114 bytes, sha256 `3fc97784b71ddd44ff8aa0a177e99622a1c61b13cfa843a0989ee4a7a0cfeb8d` = value in the mirror's NOTES.md |
| Formalization archive | https://alpo.ge/lean.tar.gz.part01..part14 (footnote 1 of the announcement) | NOT yet downloaded by us; mirror reports joined 239,275,554 bytes, sha256 `9631b4f0…49c7fc` |
| Public mirror | https://github.com/Deicyde/riemann-hypothesis (created 2026-11-20T14:47Z, head `712a6aef8fe2` at 19:19Z, no license) | metadata via GitHub API; shallow clone in progress (static inspection only) |
| Mirror claims | first commit `40e56bab` = archive `lean/` byte-exact; later commits add only Challenge.lean, comparator.json, export-targets.txt, lakefile block, README, notes, CI | NOT independently checked (needs the archive) |

Local copies: `sources/remark.pdf`, `sources/remark.txt`, `sources/mirror-NOTES.md` (third-party; local research use only, no redistribution; the
formalization has no license — mirror only, never copied into FruitStack deliverables).

## 2 What is claimed (mirror README + NOTES, read by its authors by hand; not yet by us)
- `riemannHypothesis` : Mathlib's `RiemannHypothesis`; `riemannZeta_eq_zero_re` (same, written out).
- `LFunction_ne_zero_of_half_lt_re`, `LFunction_eq_zero_re`, `LFunction_eq_zero_re_of_isPrimitive`: GRH for Dirichlet L-functions
  (all moduli, all characters; trivial character at s = 1 excluded). Not Dedekind zeta or other L-functions.
- `Main.lean`: `riemannHypothesis := Formalism.VW.rh_of_every allChi`; `allChi` = no Dirichlet L-function vanishes for Re s > 1/2; the step
  to the critical-line statements is the standard functional-equation argument (`Formalism/GammaFactorNonvanishing/CritLine.lean`).

## 3 Size and static facts (mirror NOTES; unverified by us)
175,187 `.lean` files, 17,374,215 lines, no comments, 818,755 theorem/lemma and 242,067 def-like declarations; all in the import closure of
`Main`. Text scan: no `axiom`, `sorry`, `admit`, `native_decide`, `implemented_by`, `extern`, `unsafe`, `opaque`, `skipKernelTC`; one
`addDecl` copy mechanism (kernel-checked copies) and five deny-list edits. Lean `v4.33.1` (kernel fixes of 4.34.1 #15241/#15289 NOT included,
hence a 4.33.1 build alone is limited evidence); judging planned with Lean 4.36.0 via Comparator + independent checkers.

## 4 Verification state of the world (as of mirror head 712a6aef)
- Mirror "Results": **build in progress**; no Comparator verdict published.
- Independent run (A. Sutherland, Lean Zulip, as reported by the mirror): solution export 61,570,595,788 bytes, sha256 `5ea74b91…6be244e`,
  ~1 h 20 min, 163 GB peak memory. Not a kernel verdict.
- Mirror's own limits: Comparator cannot detect a modified Mathlib; trusts checkers, Mathlib definitions/cache, exporter, sandboxes.

## 5 What FruitStack can and cannot do here
- **Cannot build or kernel-check on this host**: 29 GB RAM (needs ~150-163 GB), Lean/elan not installed. BUILD_REPRODUCED and
  KERNEL_ACCEPTED are out of reach locally; we will track the public Comparator result and independent checkers instead.
- **Can**: byte-check the mirror against the alpo.ge archive (239 MB download); static import-level dependency graph of `Main`; read the
  five theorem statements against Mathlib's definitions (semantic review of statements, not of the proof); reconstruct the documented
  discovery timeline.

## 6 Documented discovery record (announcement, pp. 1-3) — author's account, partly "a rough timeline Claude provided after a thorough
search", which the author calls a paraphrase that "might make zero sense" for the parts outside his expertise (footnote 4)
1. 10/6/26 Stepanov determinant. 2. 10/9/26 a derivation D with Dp = 0 on a CM curve for p inert in K; divisibility of D^a(Ω·θ(0)) by
p-powers. 3. 10/19/26+ qN = M k + R with the "path" quadric x1·x2 + … + x_{k-1}·x_k; automorphy via θ on a sixfold cover of GL5.
4. 10/6/26+ W(1_S) >= 0 via a determinant, "Stepanov with multiplicity one again; bootstrap". 5. 10/20/26 switch to the von Mangoldt
sum; Guinand-Weil sign; variance test-function trick. 6. 10/8/26 W(1_(0,1] + X^eta 1_(0,1/X]) >= 0 gives > 1 - eta. 7. 10/14/26
determinants for W(.) containing GGP periods (interlacing weights). 8. 11/15/26 iterated theta lifts U(X0) -> ... -> U(Xm) between
totally definite unitary groups, "wins multiplicity m"; m ~ sqrt(X) (the line credited to Claude on p. 1).
Stated transfer: Stepanov's multiplicity (function fields) -> no multiplicity over Z ("like differentiating whole numbers") ->
Fourier-analytic toy setting -> chained theta lifts each "mimicking multiplicity", chain length sqrt(X).
**Unknown** (no conversation logs, no experiment records published): how each step was found, which proposals came from Claude vs the
author beyond the single sqrt(X) line, what was tried and rejected.

## 7 Existing FruitStack RH work (inspected, preserved, not restarted)
- `/root/fruits/research/fruitstack-rh-research-v1.2/` (2026-11-07): DuckDB research graph, statement/inference records, hash-linked
  journal, exact test-function certificates (Rouché disk), equal-budget experiment harness, `lean_adapter.py` (version-pinned Lean
  invocation, never run: Lean absent). README states explicitly: no proof engine, no ζ evaluation, no RH evidence.
- `/root/fruits/integration/fse-eval006b/runners/ogi_rh/` + design `/root/contracts/OGI-RH-STRESS-TEST-DESIGN-2026-11-07.md`: OGI-RH
  stress-test items, claims, numerics, a fail-closed Lean verifier wrapper (UNVERIFIED: Lean absent -> VERIFIER_UNAVAILABLE).
- The masterplan `FruitStack_RH_Research_Masterplan_v1.2_2026-11-07.md` was NOT found under /root/fruits, /root/contracts or the memory
  directory; the v1.2 code and contract test status are its implementation trace. (Owner: please point to the file if it exists.)
- Capability status: research graph + journal OPERATIONAL (isolated); exact certificates OPERATIONAL (test functions only); Lean
  verification PARTIAL (wrapper written, no Lean); AND/OR proof graphs, novelty search, cross-domain discovery, organised-vs-unorganised
  comparison = PROPOSALS / design only (OGI-RH stress test designed, not run).

## 8 Open questions (unresolved)
Comparator verdict; byte identity mirror vs archive; whether `allChi`'s statement and Mathlib's `RiemannHypothesis` are as described
(our own semantic read pending); the decisive mathematical obligations inside 17 M lines (import graph next); any independent expert
assessment of the mathematics.

## 9 First dependency skeleton (our static reading of the mirror clone, head 712a6aef, 2026-11-20 ~21:00) — STATICALLY_INSPECTED (partial)
- `Statements.lean` (imports Mathlib only) defines the four auxiliary statements; our hand reading agrees with the mirror's: zeta zeros
  outside trivial zeros and s = 1 have Re = 1/2; Dirichlet nonvanishing for Re s > 1/2 except (trivial χ, s = 1); zeros in the strip on
  the line (all characters / primitive). `riemannHypothesis` is typed by Mathlib's `RiemannHypothesis` itself.
- `Supplements/Kernels/MainTheorems.lean`: `allChi : UpperTheory.EveryCharacter := UpperTheory.FinalTheorems.everyCharacter`;
  `rhOfAll := Formalism.VW.rh_of_every allChi`. `UpperTheory.EveryCharacter` (CharacterBoxes/EveryCharacter.lean) is textually the same
  Prop as `DirichletLNonvanishingRightOfHalf`.
- `CharacterBoxes/MainConclusion.lean`: `everyCharacter := everyCharacter_of_row UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter`;
  `everyCharacter_of_row h := LiteratureTheorems.every_character_of_literature_of_vWin ⟨h, Zero.LLC.recTExists, h⟩ (One.vwin_of_row h)`.
- `ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean` (814 lines) packages "literature" inputs
  in `OpenLiteratureStatements` with fields `caraianiLocalGlobalDual`, `localLanglandsExists`, `galoisRepOfPolarizedPairLit`, and derives
  published results (Hecke-Tate functional equation, Deligne-Ribet, Hilbert class field, CM elliptic main theorem, ...) from in-repo proofs.
**Decisive obligation identified for semantic review:** the deep "literature" inputs (local-global compatibility in the style of
Caraiani, existence of local Langlands parameters, Galois representations for polarized pairs) enter as in-repo DEFINITIONS
(`UpperTheory.One.M.Row`, `UpperTheory.Zero.LLC.RecTExists`, ...) discharged by in-repo theorems (e.g.
`Gal.Int.galoisLocalGlobalStrong_recParameter`, `Zero.LLC.recTExists`). With no axioms, these are either genuine formalizations of
major theorems or definitions weaker than the literature statements their names suggest. Comparator checks only the final five
statements, so it cannot tell which; a semantic review of these definitions is the first concrete task of Phase B.
