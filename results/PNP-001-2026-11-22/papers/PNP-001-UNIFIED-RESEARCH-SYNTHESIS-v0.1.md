# PNP-001: From Structural Obstructions to General Computation

## A unified research programme on exact-one satisfiability, algebraic kernels, proof complexity, compression and hardness transfers

**Björn Tonn**  
FruitStack / PNP-001 Research Programme  
**Working research manuscript — version 0.1, 22 November 2026**

> **Status.** This is a research synthesis, not a proof of \(P\ne NP\). Theorems established in specified models, exact finite results, published conditional transfers, new conditional deductions, failed arguments, and open proof obligations are distinguished explicitly. A research contract does not count as a proof; agreement among AI models does not count as an independent mathematical verification.

**Keywords:** P versus NP; positive exact-one satisfiability; \(\mathbb F_3\); two-valued affine solutions; matroid ports; support-overlap graphs; Hall embedding; treewidth; Polynomial Calculus; Nullstellensatz; ideal proof systems; roABP-IPS; perfect matchings; d-SDNNF; MCSP; Search-MCSP; streaming lower bounds; constructive refuters; hardness magnification; proof provenance.

---

## Abstract

We synthesise several lines of research initiated from the positive one-in-three satisfiability problem, with a common long-term objective of proving resource lower bounds for general computation. The starting point is the exact distinction between Boolean exact-one solutions and solutions of the associated affine equations over \(\mathbb F_3\). A two-value criterion describes Boolean satisfiability as an intersection property of an affine space. A classification of minimal GF(3)-blind unsatisfiable cores, a matroid-port obstruction, algebraic degree measurements, and a degree-preserving reduction from graph colouring make this distinction concrete.

A second line studies the homogeneous kernel of the graph-colouring exact-one encoding. A universal Hall-type argument, valid over arbitrary fields, embeds \(G[K_2]\) in the support-overlap graph of every spanning family of the kernel; a canonical basis attains equality. Consequently the minimum basis-overlap treewidth is \(2\operatorname{tw}(G)+1\), and the canonical basis simultaneously minimises every subgraph-monotone overlap parameter. This is a representation-independent theorem **within a precisely defined class of linear bases**, not a computational time lower bound. Indeed, complete graphs yield arbitrarily large minimum overlap treewidth while the corresponding unsatisfiable formulas have constant-size Resolution refutations.

Other work yields or investigates lower bounds in restricted proof and circuit models: Polynomial Calculus, Nullstellensatz, matchgates, algebraic branching programs and structured knowledge compilation. We trace the precise boundaries of these models and compare them with four routes toward complexity-class separations: (i) streaming Search-MCSP via the McKay–Murray–Williams (MMW) transfer, (ii) MCSP-specific circuit-to-formula conversion and hardness magnification, (iii) constructive refuters and range avoidance, and (iv) algorithmic methods and algebraic proof-system transfers.

The key proposed unification is a *computation-to-representation bridge*: under sufficiently strong, semantically justified hypotheses, a fast arbitrary computation might have to induce a restricted representation whose measured structural complexity is small. Such a bridge would let a structural lower bound contradict the existence of a fast computation. No presently inspected PNP-001 theorem establishes this bridge for all relevant algorithms, and the four routes are **not yet proved to factor through one common bottleneck**. We give precise conditional statements, a dependency graph, negative controls, and an audit framework for a candidate unification theorem. The manuscript consolidates the research without claiming \(P\ne NP\).

---

## 1. Introduction

### 1.1 The actual separation problem

Let \(P\) denote the languages decidable in deterministic polynomial time, and \(NP\) those having polynomial-time verifiable certificates. The unresolved question is whether \(P=NP\). A polynomial-time algorithm for an NP-complete language such as positive one-in-three SAT would establish equality. To establish \(P\ne NP\), it suffices to prove that one NP-complete language is not in deterministic polynomial time. Proving \(NP\not\subseteq P/poly\) would be an even stronger separation.

The present research is motivated by a recurring phenomenon: a representation can be mathematically rigid even when the represented decision problem is easy. A graph may have large treewidth but contain a small unsatisfiable subinstance. A polynomial can have large formal coefficient rank but compute the zero Boolean function. A one-pass automaton may require many distinguishable states under a restricted encoding but admit a very different nonlinear encoding with inexpensive updates. Such counterexamples are not marginal qualifications. They locate the precise points where structural results stop and claims about arbitrary computation would begin.

Thus the central logical demand of this manuscript is:

\[
\text{proven lower bound in a specified representation}
\quad\not\Rightarrow\quad
\text{lower bound for every algorithm}.
\tag{1}
\]

An implication replacing the non-implication in (1) must itself be proved, with its representation class, computational model, costs, parameter regime and quantifiers.

### 1.2 Historical scope

This article integrates two earlier manuscript streams:

- **PNP-001: Structural Invariants and General Computation, v0.24 (20 November 2026).** This contains the two-value criterion, matroid ports, core enumerations, finite degree results, Chvátal–Gomory rank, graph-colouring transfers, formula/protocol correspondence and proof-complexity barriers.
- **Every Basis Sees the Blow-Up, v4.0 (22 November 2026).** This establishes the abstract and colouring-specific universal subgraph theorems and exact minimum overlap widths, with explicit limitations on algorithmic interpretation.

It additionally integrates the PNP-001 repository results and contracts of 19–22 November: Theorems 12, 14 and 16 for restricted algebraic proof systems; R-MCSP; QE* and proof state Q-156fa9c912; Perfect Matching K6; the K8/K9 bridge maps; Range Avoidance and constructive refuters; the P1 algorithmic-method work; and the cross-theorem synthesis plan.

The four intended research fronts are not assumed to be equivalent. In the unification programme we call them: **F1, representation and streaming computation; F2, MCSP circuits and sharing; F3, proof systems and algebraic structure; F4, algorithmic lower-bound methods and constructive refuters.**

### 1.3 Evidence taxonomy

| Label | Meaning | What it does not mean |
|---|---|---|
| PUBLISHED | Exact theorem stated in an external paper | All tempting extensions of the theorem |
| PAPER PROOF | Argument written in a local manuscript | External peer review or a Lean kernel check |
| FORMAL REPORTED | Lean source and build reported in project evidence | Independent reproduction of the precise intended statement |
| FINITE VERIFIED | Complete exact computation for specified finite cases | Asymptotic hardness |
| CONDITIONAL | Conclusion proved if explicitly named hypotheses hold | Unconditional conclusion |
| OPEN | Missing premise or uncompleted validation | A false theorem |
| REFUTED | A claimed implication has a verified counterexample | Refutation of every possible replacement strategy |

Hash-chain integrity shows non-tampering relative to the exported chain. It does not show that recorded mathematical assertions are correct or that no entries are missing. The current separately archived GitHub proof-state snapshot and the newer live state must not be conflated.

---

## 2. Positive exact-one SAT and the GF(3) decomposition

### 2.1 Definition

Let \(F\) have variables \(x_1,\ldots,x_n\) and clauses \(C_1,\ldots,C_m\), each containing three distinct positive literals. A Boolean assignment \(x\in\{0,1\}^n\) satisfies \(F\) precisely when

\[
\sum_{i\in C_j}x_i=1
\quad (j=1,\ldots,m)
\tag{2}
\]

over the integers. Let \(A_F\) be the \(m\times n\) clause-incidence matrix and define

\[
\mathcal A_F=\{z\in\mathbb F_3^n:A_Fz=\mathbf1\}.
\tag{3}
\]

A formula is called *blind* if \(\mathcal A_F\ne\varnothing\) although \(F\) is Boolean-unsatisfiable. This can occur because coordinates with value \(2\) are permitted in \(\mathcal A_F\).

Since every row of \(A_F\) has three ones, \(A_F\mathbf1=0\) in \(\mathbb F_3\), hence

\[
z\in\mathcal A_F\implies z+c\mathbf1\in\mathcal A_F
\quad (c\in\mathbb F_3).
\tag{4}
\]

### 2.2 Two-value criterion

**Theorem 2.1 (PNP-001 v0.24, Theorem 4; PAPER PROOF, FORMAL REPORTED).** A positive one-in-three formula is satisfiable if and only if its affine solution space \(\mathcal A_F\) contains a vector whose coordinates assume at most two distinct values in \(\mathbb F_3\).

*Proof.* A satisfying Boolean vector is a two-valued affine solution. Conversely, if a nonempty formula has a solution with at most two values, it cannot be constant: each clause sums three equal values to zero, not one. Every unordered pair of distinct elements of \(\mathbb F_3\) is a translate of \(\{0,1\}\). Use (4) to translate the solution into a Boolean vector. Each sum of three Boolean coordinates lies in \(\{0,1,2,3\}\) and is congruent to \(1\pmod 3\); therefore it is exactly \(1\). For the empty formula satisfiability is trivial. \(\square\)

Thus

\[
F\in\mathrm{SAT}
\quad\Longleftrightarrow\quad
\mathcal A_F\cap
\{z:|\{z_1,\ldots,z_n\}|\le2\}\ne\varnothing.
\tag{5}
\]

Gaussian elimination describes \(\mathcal A_F\) in polynomial time. Equation (5) does not make the nonlinear two-value condition polynomial-time decidable. Rather, the condition encodes an NP-complete problem within a succinct affine description.

### 2.3 Minimal blind cores and finite classification

The archive reports the following counts of labelled minimal blind cores on fixed variable sets:

| \(n\) | Labelled cores | Isomorphism classes |
|---:|---:|---:|
| 6 | 900 | 3 |
| 7 | 62,370 | 21 |
| 8 | 3,766,560 | 136 |
| 9 | 243,054,504 | 848 |

The counts were assembled by exact enumeration, canonicalisation and orbit accounting; additional independent implementation checks are recorded in the project. These are finite claims.

At \(n=10\), the archive records 22,333,134 witness-type entries, **not** 22,333,134 distinct minimal cores. Of those studied, 47,088 fail to admit a static degree-two Nullstellensatz certificate but admit degree-two iterated Polynomial-Calculus refutations in the specified encoding. A 16-variable, 11-clause core \(F_{16}\) has reported Polynomial-Calculus degree three and an explicit degree-three Nullstellensatz certificate. Differences between axiom systems, field characteristic, static and iterated derivations, and the treatment of Boolean axioms must be preserved.

The project also proves an obstruction to interpreting the clutter of minimal unsatisfiable clause sets as a matroid port for \(n\ge6\), while the \(n=5\) case admits a representable port. A 2-SAT control has a related representational obstruction despite polynomial-time decidability. Thus *failure of a particular representation* does not establish general computational hardness.

### 2.4 Chvátal–Gomory rank and easy stronger proofs

The v0.24 manuscript reports rank-one Chvátal–Gomory refutations for every unsatisfiable positive one-in-three formula through eight variables under the stated natural relaxation. One exceptional isomorphism class requires two suitable covering cuts in the first round. This concerns rank of a cutting-plane closure; it does not bound the effort required to discover the cuts.

The same caution applies across proof systems. Large Polynomial-Calculus degree is compatible with short cutting-planes refutations. The relative strength and simulation relations of proof systems are mathematical assumptions that must be cited or proved each time they are used.

---

## 3. The graph-colouring family and algebraic hardness

### 3.1 Positive exact-one encoding of 3-colourability

For \(G=(V,E)\), introduce Boolean variables \(x_{v,c}\) for the three colours \(c\in\{0,1,2\}\) at each vertex \(v\), and slack variables \(y_{e,c}\) for each edge and colour. Add

\[
\operatorname{EXACT1}(x_{v,0},x_{v,1},x_{v,2})
\]

for all vertices and

\[
\operatorname{EXACT1}(x_{u,c},x_{v,c},y_{\{u,v\},c})
\]

for all edges \(\{u,v\}\) and colours \(c\).

Boolean satisfiability is equivalent to 3-colourability. As affine GF(3) equations, however, these systems have solutions for all graphs, including non-3-colourable graphs. This allows families which are Boolean-hard for a specified refutation system but algebraically consistent under the linear relaxation.

### 3.2 Degree-preserving substitution

Theorem 44 of the v0.24 manuscript establishes, for its explicitly defined XOR/carry polynomial encoding over \(\mathbb F_2\), a degree-preserving substitution from the exact-one graph-colouring clauses to the standard graph-colouring axioms. The edge slack variables are replaced by affine expressions in the adjacent colour variables; Boolean relations are accounted for in the given ideal.

When combined with the published Lauria–Nordström graph-colouring degree lower bounds, this yields project-reported infinite families of GF(3)-blind exact-one formulas requiring Polynomial-Calculus degree \(\Omega(n)\) and correspondingly exponential size under the applicable size–degree theorem.

**Scope.** This is a lower bound against the specified Polynomial-Calculus proof system. The project explicitly documents polynomial-length cutting-planes refutations for the relevant graph-colouring families. The latter are controls showing why Polynomial-Calculus hardness cannot be equated with the hardness of all proof systems or all SAT algorithms.

### 3.3 The restricted IPS frontier

The later repository records:

- **Theorem 12:** Exponential width \(2^{\Omega(n)}\) for roABP-IPS-LIN refutations of a doubly lifted colouring-derived CNF family, for every variable order and every field. The project records a complete paper argument and two independent internal reviews; formalisation of one supporting lemma was pending.
- **Theorem 14:** An extension to a fuller roABP-IPS setting subject to a stated bound on placeholder degree.
- **Lemma 15:** A sparse-placeholder linearisation argument, with a quantitative width loss; the exact parameters govern all transfers.
- **Theorem 16:** A structural coefficient-rank lower bound for specified algebraic product certificates.

These statements must not be merged into a single theorem about arbitrary IPS certificates. In particular, Theorem 16 deals with a formal polynomial arising from an unsatisfiable CNF whose restriction to Boolean inputs can be the zero function. A high rank of the **formal** polynomial does not yield a high circuit complexity of that Boolean zero function.

The relevant comparator is Hakoniemi–Limaye–Tzameret (2026), who already obtain exponential lower bounds for a different explicit family in roABP-IPS-LIN. The project's novelty claim is accordingly limited to a different family, particular reductions and quantitative lemmas unless a stronger theorem is independently shown.

### 3.4 Matchgate and transformation barriers

The MG-3 investigation records an obstruction to finding a common two-dimensional holographic basis that simultaneously renders certain nonlinear exact-one constraints and equality tensors as planar matchgates. This is an obstruction to that holographic route, not to all counting or decision algorithms.

Similarly, width bounds for roABPs must be shown to survive every certificate transformation used in a reduction. Polynomial identity, satisfiability equivalence or a semantic substitution alone does not control roABP width; factorisation, substitution and sharing can alter width dramatically.

