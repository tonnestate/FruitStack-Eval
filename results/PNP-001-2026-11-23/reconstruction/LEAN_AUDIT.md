# PNP-001 — LEAN_AUDIT (2026-11-24)

> **CURRENT STATUS:** The previous freeze order was withdrawn; operational freeze is NOT active or VPS-verified. This audit branch is a historical evidence snapshot. VPS_ACTIVATION.md is a conditional manual template only, not a standing instruction. No route priority is finalized. The actual VPS state has not been independently observed.


Baseline d7635f9ea437c494f1c032e4faedfb673a4e90b1. Status UNSOURCED / BLOCKED — AUDIT NOT PASSED. Both declarations are excluded from the admissible Route A chain. This is a record of the audit performed, not a successful kernel verification.

## Source inventory at baseline
The recursive repository tree is not truncated. The three tracked .lean files in this research branch were read:
- results/PNP-001-2026-11-19/lean/WStar.lean
- results/PNP-001-2026-11-19/lean/WStarLower.lean
- results/PNP-001-2026-11-20/acc0-level3/lean/ACC0L3.lean

Neither requested declaration (no_tail_bounds, restriction_independent_gates_survive) occurs in these files. WStar and WStarLower import named Mathlib graph, finite-type, ZMod, linear-algebra and tactic modules; ACC0L3 imports Mathlib. A lexical scan of these three files found no standalone sorry/admit/native_decide/axiom/opaque markers or #print axioms commands. This does not audit transitive imports, compiled artifacts or the target declarations. In the available audit environment no lean or lake executable was found. No new kernel run or axiom result can be reported.

| Declaration | Source / exact statement | Kernel | Axioms/imports | Quarantine dependencies | Verdict |
|---|---|---|---|---|---|
| no_tail_bounds | missing | historical report only; not rerun | unknown | unknown | UNSOURCED / NOT PASSED |
| restriction_independent_gates_survive | missing | historical report only; not rerun | unknown | unknown | UNSOURCED / NOT PASSED |

## Required reproducible audit, separately for each declaration
1. Recover the original lab source, transcript, exact commit, lean-toolchain, lake manifest and imported project sources. Record hashes of source and statement. Do not reconstruct a weaker theorem under the same name.
2. On the original pinned environment build from clean sources. Run #print on the actual fully qualified theorem, inspect binder types, explicit quantifiers and definitions with set_option pp.all true where necessary. Run #print axioms on the theorem in the same import environment and save stdout/stderr, exit code and version. Resolve the full transitive axiom list, including sorryAx, project assumptions and any native-decision trust mechanism used by that Lean version. Standard axioms (such as propext, Classical.choice and Quot.sound) must be separately disclosed; no project-specific axioms permitted. Inspect imports and definitions, including opaque constants; opacity alone is not an axiom, but hidden semantics must be checked. Reject proof placeholders and native_decide for this protocol.
3. Statement audit: compare the actual declaration and definitions to the original intended mathematical proposition, including all parameters, domains, resource accounting, representation restrictions, gate basis, edge cases and uniformity. For no_tail_bounds, do not infer an update-time lower bound from a tail/state statement; check exactly what bound and quantifier order it proves. For restriction_independent_gates_survive, check what independence, restriction and survival mean and whether constant generation or representation-specific assumptions enter. These are audit questions, not assertions about the missing statements.
4. Resolve semantic dependencies against QUARANTINE.md using canonical Q:S IDs and source hashes, not names alone. Any unknown or red dependency blocks use. A kernel-checked theorem can be irrelevant to the intended route.
5. Obtain two independent blinded critical-node reviews (at least separate proof and statement evaluation). Record the proof artifact, exact statement, axiom list, transcript hashes, evidence and adjudication. No automatic promotion to verified while freeze is in force.

The runtime operator must supply the missing lab source and reproducible Lean environment; repository documentation alone does not close this gate.

## Follow-up search and disposition
GitHub code search for both exact declaration names returned zero hits in FruitStack-Eval (index coverage is not exhaustive). Inspected research-branch history (30 commits) and recursive trees at 7ca60770, 957992ea, d49a05c1: only the same three tracked Lean files; no tracked .olean, lean-toolchain or lake manifest in the inspected trees. VPS reflog, untracked lab builds and agent transcripts are inaccessible in this audit; no assertion they do not exist. Both declarations are now UNSOURCED, audit FAILED TO PASS due to missing provenance (not a mathematical refutation). Removed from the admissible A chain in SCOPED_GRAPH_E_A.json; restoration requires recovered exact source and the full audit above. Do not report a new Lean success.
