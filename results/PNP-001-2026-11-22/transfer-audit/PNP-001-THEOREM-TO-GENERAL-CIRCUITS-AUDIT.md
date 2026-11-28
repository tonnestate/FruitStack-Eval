# PNP-001 — Theorem-to-general-circuits audit

**Status: IN PROGRESS (22 November 2026, 23:50).** Sections A and G are filled. Sections B–I are filled in from the
research desk as questions are answered and cross-family reviewed. No new theorem is claimed in this version.

Frozen sources:
- results branch `cc/pnp001-results-20261118` at `572fe7e`;
- desk implementation at `d04b048`, which adds the review-quote rule against step-id misattribution;
- live proof states as exported in `qe-star/proofstate-live/`.

## A. Verified evidence inventory

The full table, with every statement and review in full, is in [`EVIDENCE-INVENTORY.md`](EVIDENCE-INVENTORY.md). It was generated
mechanically by [`inventory.py`](inventory.py) from the live proof states. Every dependency is named by its full
`(question_id, step_id)` pair.

Method. For each step the script records:
- the author model and every review: reviewer model, verdict and family;
- a lexical match score between the review text and the statement, used only to *flag* reviews that may concern a
  different statement. It is not used to accept anything.

A step counts as independently reviewed only with a SURVIVED_REVIEW from a different model family whose text matches the
statement.

Result (live state, 23:40):

| Group | Steps | Independent review that matches the statement |
|---|---|---|
| Linear streaming | `Q-85e487150a`: S0014, S0016, S0017 | yes, all three (nemotron) |
| Rank / prefix / witness | `Q-156fa9c912`: S0138, S0125, S0127, S0135, S0144, S0145, S0098, S0102, S0024, S0043, S0053 | yes (nemotron); S0098 has 3 open disputes |
| Rank / prefix | `Q-156fa9c912`: S0021 (affine updates need S ≥ N) | **no**: same-family reviews only, plus one REFUTED review with low match |
| Rank / prefix | `Q-156fa9c912`: S0086 | **flagged**: the cross-family review text barely matches; re-review queued |
| Candidate A | `Q-f0a0962f12`: S0003 (inclusion-exclusion), S0007, S0011 | yes |
| Candidate A | `Q-f0a0962f12`: S0002 (clauses 1–4 jointly unsatisfiable) | REFUTED for nonlinear algorithms; low match, re-check queued |
| Other | `Q-0b7da33369`: S0117; `Q-e72cdd5423`: S0001; `Q-5f55fb62c2`: S0028; `Q-248eb0b818`: S0021 | yes |
| Other | `Q-0a1653e365`: S0002 | **flagged** (low match); re-review queued |
| Other | `Q-7555dd132d`: S0014 (bounded-DP corollary) | REFUTED (nemotron); the low match comes from the refutation arguing a different consequence; kept as refuted |

Rank over different fields. Proof-book entries seq 8987 and 8988 record that for g_s = 1[x ∈ Im_s] the cut rank over Q
exceeds the cut rank over GF(2) at m = 3, s = 2 and 3. Hence rank_F2(M_t) = rank_Q(M_t) does not hold in general. The field
for which `Q-156fa9c912:S0138` is sound is open question T1.

Structural inputs. Taken as established, as the contract instructs:
- Theorem 4.1, under (R), (L) and (E) with rank parameter d: G[K_d] embeds in H_B for every finite spanning family B.
- Theorem 5.4: for the colouring kernel over every field, G[K_2] embeds in H_B.
- Theorem 6.1 and Corollary 6.2: min_B tw(H_B) = 2 tw(G) + 1.

All three are quoted verbatim from `qe-star/PNP-001-PAPER-BASIS-BLOWUP-v4.0.md`, lines 186–312.

## B.–I. Open research questions

The questions are in the proof book and assigned to the desk with priority (CAND-A lane gate).
Construction and review run under the cross-family rule.

| ID | Contract section | Question |
|---|---|---|
| `Q-fb36b9fff1` (T0) | 5–7 | Construct G_{m,s}, K_{m,s} with (R), (L) and (E), and a circuit-derived family B_C, and prove tw(H_{B_C}) ≤ Ψ(m, s, S, Γ) for arbitrary nonlinear circuits. Otherwise give the first failing step with a counterexample. The K_n control and the nonlinear counterexample in `Q-f0a0962f12` are mandatory; afterwards compare with the quantifiers of (40a). |
| `Q-f90dd2d84d` (T1) | 4 | The field for which k ≥ rank_F(M_t) in `Q-156fa9c912:S0138` is sound, and whether it extends beyond linear updates. |
| `Q-00adf4fb0a` (T2) | 4 | Hypotheses of `Q-85e487150a`: S0014, S0016 and S0017, one by one: a counterexample when the hypothesis is dropped, or the strongest correct theorem without it. |

Sections B (dependency graph), C (transfer candidates), D (derivations), E (counterexamples), F (resource analysis),
H (verdict) and I (first missing implication) are written only from answered and independently reviewed steps.
