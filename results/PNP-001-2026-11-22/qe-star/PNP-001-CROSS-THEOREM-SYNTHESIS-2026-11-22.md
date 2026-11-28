# PNP-001 — CROSS-THEOREM PROOF SYNTHESIS (owner contract, 2026-11-22 ~14:05)

Recorded by Claude (PI) from the owner's chat message, condensed with all requirements kept.

**Goal.** Combine existing PNP-001 results with published transfer theorems, but only where their hypotheses genuinely compose.
- Primary target: an unconditional proof of P≠NP.
- Secondary target: the strongest new unconditional theorem.
- This is not a literature survey.

**Required for each combination:**
1. what the first theorem proves;
2. what the second theorem needs;
3. whether the objects are identical or joined by a proved reduction;
4. which parameters are preserved;
5. whether the result is stronger than its components;
6. whether it reaches general computation or only a proof system;
7. the first missing lemma.

A chain with one unproved arrow is a conditional programme, not a proof.

## Sources
- FruitStack-Eval `cc/pnp001-results-20261118`:
  - THEOREM-12.md and ACC0-L3-REPORT.md (results/PNP-001-2026-11-20/acc0-level3/)
  - REUSE-MCSP-NOTE.md
  - the K1, K6, K8 bridge map, K8 range avoidance, representation combinations and K9 contracts
  - the QE* reconstruction and the embedding contract
- Live proof state of Q-156fa9c912.
- Owner's paper "Every Basis Sees the Blow-Up" v4.0: Thm 4.1, Thm 5.4, Cor 6.2, Remark 6.4, Prop 6.5. Its partial Lean formalisation does not verify the whole paper.

## Line A — Embedding + Theorem 12 + Lemma 15
- Build the exact correspondence: colouring kernel → gadget-lifted formulas → Ψ_n → their spaces → H_B → roABP coefficient rank → Lemma 15 transformations.
- Do not assume that lifting preserves the kernel.
- Check R, L and E for each transformed object; apply Thm 4.1 only if all three hold.
- Target: a resource-preserving theorem that survives (1) arbitrary basis changes and (2) the roABP-IPS certificate transformations.
- If the result is no stronger than Theorem 12 or Lemma 15, record it as a redundancy.
- Mandatory counterexample: Prop 6.5 and the easy high-treewidth examples.

## Line B — Range avoidance + exact SAT counterexamples + constructive refuters
- CJSW "Constructive Separations": Thm 1.7 and the Sec. 4 propositions from the primary source, stated exactly:
  - MCSP language
  - model
  - refuter definition
  - uniformity
  - bounds
  - quantifiers
- Map the reuse of existing generators, enumerators, finite optimality results, counterexamples, range-avoidance work and verification.
- Keep three tasks apart:
  - (1) a counterexample to one circuit;
  - (2) a point outside the range of a whole family;
  - (3) a uniform, efficient refuter in the required class.
- Main obligation: a uniform refuter theorem with ALL resources counted, or the first asymptotic obstruction. A SAT solver does not count as an efficient refuter. Finite experiments do not replace an asymptotic argument.

## Line C — MCSP formula lower bounds + K1/R-MCSP + MMW
- Sources: CJW20 Thm 1.6; MMW19 Thm 1.3 and 1.4; the R-MCSP and K1 work.
- Find the weakest MCSP-specific simulation of the Stream-Merge / Circuit-Min-Merge structures, covering:
  - reuse
  - fan-out
  - sharing
  - depth
  - basis
  - oracles
- Quantitative: for a formula bound with exponent a(β) and a simulation L(f) ≤ C·CC(f)^q, derive the exact condition on q and its dependence on β, and check it against the MMW parameters.
- A restricted (algebraic) simulation does not count as a general Boolean simulation.
- Barrier audit:
  - arbitrary DAG fan-out
  - shared values
  - nonuniform families
  - the MMW oracle construction
  - the locality barrier
  - published bounds for the same parameters

## Cross-connections
- **A→B:** can a basis-independent invariant constrain the Eval image? Is the result constructive or only existential?
- **A→C:** do the Theorem 12 techniques prove a property of the MMW-derived circuits that survives sharing?
- **B→C:** can a refuter or generator give the quantitative magnification bound?
- **C→QE*:** can the Stream-Merge structure give a representation-independent streaming bound without excluding the oracle construction?

Each needs a complete proof or the first missing implication. Do not combine bounds from incompatible models.

## Review
The critic checks:
- quantifier order
- uniformity
- search versus decision
- promise versus total
- encoding size
- circuit basis
- characteristic
- fan-out
- model restrictions
- oracle dependence
- parameter ranges
- whether the result is already known

Use PhysalisMe, CherryMe and Lean. Experiments are counterexample search only.

## Deliverable
PNP-001-CROSS-THEOREM-SYNTHESIS-REPORT.md, sections A–H:
- A. evidence inventory
- B. dependency graph, each arrow marked PUBLISHED / INDEPENDENTLY PROVED / CONDITIONALLY PROVED / OPEN / REFUTED
- C. theorem candidates
- D. proof attempts
- E. falsification
- F. transfer verification
- G. verdict
- H. smallest remaining lemma

Update existing questions instead of creating duplicates. Push with commit hashes. Do not touch production or CI.

## Acceptance
A combination counts as progress only if it delivers one of:
1. an independently checked unconditional theorem stronger than its components;
2. a complete, correctly parameterised proof of an open transfer lemma;
3. a rigorous counterexample to an invalid transfer;
4. a proved reduction of several obligations to one more precise obligation.

Do not restart Theorem 12, Lemma 15, QE*, K1, K6 or K8. Do not duplicate the embedding questions of 2026-11-22.
