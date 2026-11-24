# PNP-001 — CRITICAL_PATH (owner decision, 2026-11-24)

Baseline d7635f9ea437c494f1c032e4faadfb673a4e90b1. E only active mathematical route. A only formalization of existing statements. B/C/D/F/G frozen 4–6 weeks; day-30 owner decision, no automatic restart. Each route sheet below is an audit worklist, not a declaration of proof. Dependencies not reconstructed are blockers under QUARANTINE.md. Source files are relative to results/ unless otherwise indicated.

## E — PRIMARY — algebraic proof complexity

Goal: obtain an unconditional new algebraic lower bound, then determine whether a valid Boolean separation transfer exists. Existing result: THEOREM-12.md (PNP-001-2026-11-20/acc0-level3/) asserts an explicit polynomial-size UNSAT CNF family Psi_n with width >= 2^(delta n), for every variable order and field, for roABP-IPS_LIN. Theorem 14/Lemma 15/Theorem 16 are partial adjacent results; exact scope needs audit. K2 bounded-arithmetic contract is a candidate additional bridge. Ledger seq 14287 is the owner-reported locator for a missing IPS conversion; original row not recovered in this audit, so its exact content is not certified.

Missing lemma E1 (proposed precise sufficient target, not a known result): Fix the field and exact IPS encoding of Psi_n (including Boolean axioms) and the size convention. For every k>=1 there exist d>=1, C>0 and n0 such that for every n>=n0, if Psi_n has a general IPS refutation of size <= n^k, then Psi_n has a valid roABP-IPS_LIN refutation of width <= C n^d in some variable order, with all certificate identities preserved. The order may depend on the instance and certificate; no fixed order is needed for Theorem 12. This family-specific existential conversion is weaker than converting all IPS refutations. Do not equate width, circuit size, syntactic degree and placeholder degree.

Required logical separation: Theorem 12 + E1 would rule out polynomial-size general IPS for this family, assuming the theorem and model match. **It would not alone prove P != NP.** E2 is a separate missing bridge: show P=NP implies polynomial-size general IPS refutations for this family, or find another sufficient established Boolean transfer with exact premises. Existence of some polynomially bounded Cook–Reckhow proof system under P=NP is not polynomial boundedness of IPS. Full IPS lower bounds may imply VP != VNP under the applicable Grochow–Pitassi theorem; that is a different separation.

Next concrete steps (sequential, no new broad campaign):
1. Recover seq 14287 and exact Thm 12/14/15/16 definitions; freeze field, family, placeholders, size/width and certificate equations C(x,0)=0 and C(x,F(x))=1 (check encoding).
2. Separate certificate validity from representation. Test whether linearization in axiom placeholders preserves small size; division-free ring identities only, no unjustified substitution or cancellation.
3. For a family-specific linear certificate, bound coefficient-matrix ranks across a chosen variable order and prove conversion with explicit polynomial overhead, including degree constraints. Identify where arbitrary DAG sharing is lost.
4. Falsify generic variants first (known small circuits with high ROABP rank under selected orders; distinguish fixed-order counterexamples from all-order ones). Use small Psi_n instances only as regression/falsification tests, never asymptotic proof.
5. Audit E2 separately before labeling any result a Boolean separation.

Quarantine: global rules apply; E's concrete dependencies have not yet been enumerated. No claim of clearance. Do not import A's residual bounds or B's cofactor lemma without audited dependency paths.
Stop: day 30, if no new independently auditable sublemma or concrete reduction, recommend switching focus to A subject to owner decision. Stop any formulation immediately upon a valid counterexample; retain it as disputed/failed. E1 established without E2 is algebraic progress, not P != NP.

## A — SECONDARY — streaming / Lean only

Goal: MMW19 Thm 1.3 transfer to P != NP. Exact target (sufficient version of 40a): exists time-constructible s(m)>=m and fixed A in PH such that for every uniform deterministic oracle-free one-pass machine M computing total Search-MCSP^A[s(m)] correctly, and every constants k,l,C,D>0, infinitely many m violate either space <= C s(m)^k or worst-case per-bit update time <= D s(m)^l. Equivalently no such machine has both polynomial bounds for all sufficiently large m; fix finalization/output conventions to MMW. The target problem may use oracle circuits in its definition; the solving machine does not receive an oracle for free. A state-count lower bound in an affine representation is not a general update-time lower bound.

Evidence: reconstruction slice 1 §§4,6; Q-156fa9c912 G0001/G0012/G0015, S0037; Q-85e487150a affine case; manuscript v0.25 and QE* contract. Lean declarations no_tail_bounds and restriction_independent_gates_survive are reported, not yet statement/axiom-audited (LEAN_AUDIT.md).
Quarantine: S0028/S0029 residual-upper-bound identity pending resolution; Q-08a1c5b68f:S0028/S0029/S0152 audit hold; Q-156fa9c912:S0037 misattribution hold. All unknown dependencies blocked.
Next: formalize existing valid statements only, verify state-vs-time/model distinctions, recover exact Lean artifacts. No new update-bound offensive.
Stop: any theorem mismatch, custom axiom, unknown dependency or proof placeholder blocks promotion; no offensive work until owner switches route.

## B — FROZEN — unrestricted MCSP circuits

Goal: MMW19 Thm 1.4 bullet 3 -> NP not in P/poly -> P != NP.
Missing T_B: for a fixed c>=1, every k>=0 and C>0, infinitely many m satisfy CC_B2(MCSP[m^c] on N=2^m inputs) > C N m^k, unrestricted depth. This is a sufficient decision premise for the search version after an audited search-to-decision conversion.
Evidence: RECONSTRUCTION-SLICE-2.md; Q-10bbdfaf2a, Q-9154b244de, Q-f269573fe5, Q-d56ff318ed. A fixed-exponent lower bound does not give this premise.
Quarantine: Q-10bbdfaf2a:S0148/S0508/S0509; S0217 candidate repair audit; transitive dependents unknown.
Next if reopened: audit S0217, constants and totality, against primary MMW source. Stop if model, exponent or output encoding changes without proved reduction.

## C — FROZEN — formula / reuse simulation

Goal: transfer CJW20 formula lower bounds to the MMW target.
Missing K1 sufficient candidate: choose beta in (0,1) and eta>0 such that for every fixed k>=1 and all sufficiently large m, every qualifying streaming decision algorithm for MCSP[s], s=N^beta, N=2^m, with state, update and decoder bound <=s^k yields a De Morgan formula strictly below the applicable CJW20 lower bound, with a fixed exponent margin (choose eta consistent with the primary theorem). Verify the threshold is time-constructible and the exact formula measure. R-MCSP alternate target in REUSE-MCSP-NOTE.md requires its own parameter audit.
Evidence: K1 contract (2026-11-21 specifications), Q-9540547936, Q-2dc43864bc, grand strategy P2. Quarantine: no verified complete dependency list; global holds apply, especially reuse/cofactor premises if used.
Next if reopened: prove precise simulation with sharing and exponent accounted for, locality/oracle controls. Stop if unfolding blow-up exceeds bound or only restricted circuits are simulated.

## D — FROZEN — constructive refuters / range avoidance

Goal: CJSW constructive-separation transfer to Boolean separation.
Candidate missing obligation: for the exact threshold and length regime of CJSW Prop 4.3, construct a refuter family R satisfying every prescribed uniformity, circuit-class and resource quantifier, with for each required m, R(m) a truth table outside Image(Eval_{m,s(m)}). This is a schematic target: numerical threshold, circuit class and uniformity quantifiers not re-extracted from primary source here; no exact theorem assertion or clearance until then.
Evidence: K8 range-avoidance contract (2026-11-21), finite generator experiments, CJSW Thm 1.7/Prop 4.3 cited there. Quarantine: no dependency audit; finite SAT witnesses do not establish asymptotic refuters.
Next if reopened: extract primary proposition verbatim with quantitative parameters, then check generator resources. Stop if generation requires enumeration or an oracle outside the target class.

## F — FROZEN — matching / structured circuits

Goal: explicit structured representation/refutation lower bound, not automatically general computation.
Missing K6: exists an explicit infinite cubic bipartite expander family G_n and delta>0 such that for every vtree T over E(G_n), some eligible T-induced cut A|B has rank_F(M_{A,B})>=2^(delta |V(G_n)|) for the specified field(s). Rank-to-d-SDNNF and lifting hypotheses are additional obligations. A Boolean separation bridge remains separate.
Evidence: K6 contract, Q-12f2991045, pm_cutrank.py, boundary-signature and switching criteria. Quarantine: global holds; no complete dependency audit. Prism graphs show exponentially many matchings do not imply large width/rank.
Next if reopened: prove independent alternating-cycle switches across all vtrees or find a vtree counterexample. Stop on failed all-vtree condition or incompatible lifting model.

## G — FROZEN — PIT / GCT / algebraic and algorithmic transfers

Goal: a valid transfer to general Boolean complexity rather than only an algebraic or restricted-class separation. No single exact Boolean target is established in the reconstruction contract; do not invent one. Concrete intermediate target from grand strategy P1: for every fixed alpha>1, a deterministic 2^n/n^{omega(1)} acceptance-probability algorithm (error o(1)) for O(n^alpha)-size XOR_2 o THR o THR, with weights/encoding as required by cited transfer. Claimed consequence is E^NP size separation against THR o THR, not P != NP. PIT/GCT/VP vs VNP remain distinct obligations.
Evidence: grand strategy, LIT-7, reconstruction CONTRACT.md route G. Quarantine: global holds; no complete dependency audit.
Next if reopened: pick one primary transfer theorem and extract exact premises/quantifiers; identify the Boolean bridge separately. Stop if only an algebraic/threshold separation results and no further sufficient implication is established.

## 30-day milestones
Day 1–7: quarantine and critical-path reconciliation; recover missing transcripts and exact Lean source/log/axioms; resolve seed namespaces; validate route E dependencies.
Day 8–14: E1 formal statement and 3–5 sublemmas; negative controls first.
Day 15–28: E sublemmas only; A formalization only.
Day 30: owner decision from audited evidence, not review counts; no automatic switch or unfreeze.

## Owner follow-up — supersedes sequence above
Operational activation is not complete; see VPS_ACTIVATION.md. E2_GATE.md is now the only active mathematical audit in E; E1 is parked pending E2 go/no-go. A remains existing-statement formalization only; both reported new Lean declarations are UNSOURCED and excluded until audit passes. SCOPED_GRAPH_E_A.json contains the first source-grounded E/A critical slice and computed dependency-only closures, not a complete corpus graph. No new agent promotion; no VPS activation evidence yet. B/C/D/F/G remain frozen by policy. Reassess E/A when E2 audit is decided, without automatically starting a second offensive.
