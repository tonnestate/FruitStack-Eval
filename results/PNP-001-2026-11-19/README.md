# PNP-001 results, 2026-11-19

Exact finite results and one reduction about positive 1-in-3-SAT and its GF(3)-"blind" cores (Boolean-unsatisfiable but consistent as a
linear system over GF(3)). **Nothing here is a statement about P vs NP.** Every item states its level: finite fact, statement about one
proof system / circuit class, or (none so far) about all algorithms.

## Headline results
| Result | Level | Status | Files |
|---|---|---|---|
| Labelled minimal blind cores on [n]: 900 (n=6), 62,370 (7), 3,766,560 (8), 243,054,504 (9); isomorphism classes 3 / 21 / 136 / 848 | finite | exhaustive; n=8, n=9 independently matched by the owner | `tables/`, `scripts/cores_fast.py`, `scripts/isoclasses.py` |
| Every minimal blind core on <= 9 variables has a degree-2 Nullstellensatz refutation in the XOR/carry encoding over GF(2) (L = 1+a+b+c, q = ab+ac+bc) without Boolean axioms | finite | exhaustive | `scripts/cores_deg.py`, `scripts/xorcarry_degree.py` |
| G10 = {012,034,078,135,145,468,569}: NS degree 3 (mod x^2=x), PC degree 2 - smallest size without an NS2 certificate is exactly 10 variables | finite | two implementations each; validator FINITE_CONFIRMED | `scripts/ns_verify.py`, `scripts/pc2_verify.py` |
| Every minimal blind core on <= 10 variables is refuted by iterated degree-2 polynomial calculus (47,088 NS2 failures at n=10, all PC2) | finite | exhaustive | `n10-degree/` |
| F16 (16 variables, 11 clauses): no degree-2 PC refutation (closure rank 131/137, dual functional), degree-3 NS certificate (82 terms) | finite | owner's search, director's independent check | `F16/` |
| Hence 11 <= smallest blind core with PC degree >= 3 <= 16 | finite | - | - |
| 3-colouring transfer: T(G) (vertex clause per vertex, (x_uc, x_wc, y_uwc) per edge and colour) is GF(3)-consistent; the substitution y -> 1 + x_u + x_w maps XOR/carry PC refutations of T(G) to PC refutations of the standard 3-colouring encoding of the same degree. With Lauria-Nordstrom 2017: explicit GF(3)-blind families with PC degree Omega(n), PC size exp(Omega(n)) | one proof system (PC over GF(2)) | argument complete; formal check pending; novelty vs. Atserias-Ochremiak (CSP theory) to be checked | `scripts/col2onein3.py` |
| CG rank 1 for all 136 classes at n <= 8 (135 single-variable certificates, one class needs covering cuts) | finite | exhaustive, exact certificates | `certificates/cgrank2_n8.json` |
| F8 = {146,012,036,256,234,045,157}: exact GF(2) identity 1 + sum q_i = (1+x1+x2+x5)L1 + (x0+x1+x5+x7)L2 + (x0+x1+x4+x7)L3 + (1+x1+x3+x7)L4 + (1+x3)L7 (degree-2 Nullstellensatz certificate) | finite | owner, director (sympy) and validator | - |

Completeness of the enumeration rests on D-018 (two-value criterion, Lean-verified) and T44 C3/C4 (a minimal blind core has at most n-1
clauses, proved). List sizes in the n=10 files are sums over witness types, NOT core counts.

## Corrections made today (kept visible)
- The n=8 certificate list has 17,657 entries / 16,866 clause sets but only 136 isomorphism classes; "216 type-B cores" are one class.
- An agent dataset column `int_feas` (n=6) was wrong on 1,320 rows (false count 30; correct 1,350); datasets are flagged.
- Several director formulations were corrected by the owner (semantic vs. constructive state, Karchmer-Wigderson exactness, degree
  levels); see the proof book (RETRACTION entries).

## Specifications (binding research assignments)
`specifications/`: H-TIME-001 / H-CONSTRUCT (time models, construction cost), ALG-BIT-001 (algebraic / bit-level computation),
ACC0-MOD6 (current priority: circuits with mod-2 and mod-3 gates).

## Proof book
`../PNP-001-2026-11-18/beweisbuch/` updated: 3,889 entries, hash chain intact, readable rendering `LESBAR-STAGING-kampagnen.md`.
