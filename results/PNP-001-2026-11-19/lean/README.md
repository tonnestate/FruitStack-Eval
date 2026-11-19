# Lean verification: w*(F(G)) = 2·tw(G) + 1

F(G): the positive 1-in-3 translation of graph 3-colouring (vertex clause (x_v1, x_v2, x_v3); per edge e = uw and colour c the clause
(x_uc, x_wc, y_ec) with its own slack variable). w*(F) = minimum over bases of the GF(3) kernel of the treewidth of the coefficient graph.

Toolchain: Lean 4.35.0 + Mathlib v4.35.0. Check: `lake env lean WStarLower.lean` inside a Mathlib v4.35.0 project.

| File | sha256 | Content |
|---|---|---|
| `WStar.lean` (266 lines) | `2caafc866c2a7198ea30873054139a3d8b9cacd263a578db31ac3fb4764eb067` | tree decompositions (defined here, not in Mathlib), 2-blow-up, `twLe_blowup`, `coeffGraph_nat` (natural basis coefficient graph = blow-up), upper bound `wstar_le_two_tw_add_one` |
| `WStarLower.lean` (591 lines) | `dbfc812c176fae4bf36d2408e1e70fc5e1bbff0e2735c92a6de54fc00763b83b` | same definitions plus lower bound `tw_le_of_coeff_tw` (any spanning family of the kernel), `twLe_mono`, equivalence `wstar_eq_iff` |

`#print axioms` for `wstar_le_two_tw_add_one`, `tw_le_of_coeff_tw`, `wstar_eq_iff`: `[propext, Classical.choice, Quot.sound]`; no `sorry`.

The lower bound follows the owner's proof text (`LOWER_BOUND_PROOF.md`): GF(3) linear algebra plus the clique fact for tree decompositions
(Helly for subtrees, formalised via convexity, bridges and medians). It does not use Lemma W. Exhaustive data consistent with it: K2 (all
63,180 kernel bases give K4, w* = 3), K4 (w* = 7).

Scope: an exact structural theorem about this family; it is not a complexity lower bound for SAT.
