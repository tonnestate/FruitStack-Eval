# T64 — Audit register (rounds 1–3) and the verification gate (2026-11-28)

Rule from now on (binding for every agent, replaces "independent review passed" as evidence): **a finding or a claim is accepted only after (1) the exact sentence is located in the file/graph row, (2) the counterexample or proof step is checked by hand or by one exact tiny computation, (3) it is classified, (4) dependents are grepped and edited in the ACTIVE documents, (5) the Proofbook row is written.** Classes: REFUTED (counterexample), MISSING HYPOTHESIS, UNPROVED (no proof given), WORDING (main result intact), NOT LOCATED/NOT CONFIRMED. An agent review or a "SURVIVED_INDEPENDENT_REVIEW" status is not a proof. Negative results (exclusions of research directions) are audited by the same gate: the claim excluded must be separated into (the mathematical approach) / (the concrete construction) / (an intermediate claim).

## Round 3 (this session): theory documents, checked against the text
| id | location | class | edited in |
|---|---|---|---|
| T28 | Lemma G consequence | upper bound used as lower bound: REFUTED inference; only "guarantee insufficient" proved | T28 |
| T36 | Theorem F | scope: only μ1–μ4; "all other measures length-type" UNPROVED; 2^{V_e} not bounded by K·n | T36 |
| T38 O4 | attainability | REFUTED (4 classes, fibres {1,2,3},{4}: bound 1 bit, need 2); lower bound stays | T38 |
| T38 CLOSE cost | missing factor | CONFIRMED (corrected after recomputation): per substitution O(M_D·D·s·M_{rD} + M_D²), at most 1+|A|M_D substitutions; the stated total drops one factor M_D in the construction term. My earlier 'NOT CONFIRMED' was itself an error (compared texts, did not multiply) | T38 |
| T41 §3 | ∀p∃A_p vs ∃A∀p | MISSING HYPOTHESIS (uniformity) | T41 |
| T43 C3 | cause localization | UNPROVED, withdrawn | T43 |
| T45 §3 | 2-SAT linear circuit size | UNPROVED; "not even super-linear" unsupported | T45 |

## Synthesis findings (graph `synthesis_export`, read-only; statuses cannot be changed by me — graph and `synthesis_acceptance` are not written)
| synthesis | located text | verdict |
|---|---|---|
| SYN-cc1f3a285f6b | reconstructed proof: "dependence of {e}∪r_S ⇔ e∈span(r_S), because e≠0 rules out the empty combination" | CONFIRMED proof defect: counterexample r1=(1,0,0), r2=(0,1,0), r3=(1,1,0), e=(0,0,1): {e}∪R dependent, e∉span. Theorem stays valid with minimality ⇒ independence of the r_S. Passed independent review: review missed it |
| SYN-e12a37d0191a | proof: "Zero vectors … are in no circuit and are excluded"; assumptions: "zero vectors are excluded from circuits" | CONFIRMED wording error ({0} is a circuit/loop); theorem concerns circuits through t, unaffected |
| SYN-d74acb1ca989 | proof parenthetical "p≈q (necessarily equal lengths)" | CONFIRMED wording defect: false for empty residuals (F={000}, p=1, q=11); the lemma is stated per depth t, main claim unaffected |
| SYN-0cd3c828aaac | evidence: "tested all 256 families of three-input Boolean functions and all prefixes (130,816 cases)" | CONFIRMED mislabel: 256·511 = 130,816, i.e. 256 single functions (d=1), not all families; evidence is corroboration only (the synthesis says so) |
| SYN-3aa6ac8c5876 | statement: L = O(s log(n+s)), output wire in the description | CONFIRMED edge case: s=0 still needs ⌈log2 n⌉ bits; use O((s+1)log(n+s+2)) |
| SYN-cbdccbd10d82 | original_proof, last sentences: "…subsets can shrink the z-fibre. G0001 stays open." | CONFIRMED wording error: removing equations can only ENLARGE a fibre at fixed x. The substantive point (hypothesis (b) needs ONE fibre Z(x) common to all owners, and for subsets S_i the enlarged fibres can differ between owners, so (b) is not inherited by subsets) is right; the open obligation G0001 stays open for that reason |
| SYN-0c07344564c0 (and 4 cousins, cyclic address counter) | REFUTED_BY_DEPENDENT_REVIEW | scope question (fixed N vs unbounded stream, extra closing bit): consistent classification not done here; recorded as open for a scope-by-scope table |

## Process failures (cause, not excuse)
1. I took graph statuses and agent reviews at face value and built on them (T49 L3, T52 §1, T53 §2, T62). 2. I wrote statements in the active documents without the scope sentence (what is proved, in which model, under which hypothesis). 3. I corrected the Proofbook before the active documents. Remedy: the gate above; every Proofbook correction row must cite the edited document.
Not done: line-by-line verification of the 1,502 proof files; the remaining 32 earlier refutations are NOT yet re-audited (each must be split into approach / construction / intermediate claim).
