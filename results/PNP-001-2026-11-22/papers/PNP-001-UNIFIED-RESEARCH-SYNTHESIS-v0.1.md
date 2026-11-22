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


---

## 4. Universal support-overlap embedding

### 4.1 The homogeneous colouring kernel

Let \(\mathbb F\) be any field. Consider the homogeneous kernel

\[
K_G(\mathbb F)=\left\{(x,y):
\sum_{c=0}^{2}x_{v,c}=0,\quad
x_{u,c}+x_{v,c}+y_{\{u,v\},c}=0\right\},
\tag{6}
\]

where the first equations range over vertices and the second over edges and colours. The vertex triples are freely selectable in

\[
T_{\mathbb F}=\{(a,b,c)\in\mathbb F^3:a+b+c=0\},
\]

and the edge variables are then forced. Therefore

\[
\dim K_G(\mathbb F)=2|V|.
\tag{7}
\]

For an indexed finite spanning family \(B=(b_j)_{j\in J}\subseteq K_G\), let \(H_B\) be its *support-overlap graph*: \(j\sim k\) when the supports of \(b_j,b_k\) share a nonzero coordinate. The graph depends on the chosen coordinates, not merely on the abstract isomorphism type of \(K_G\).

### 4.2 Abstract embedding theorem

**Theorem 4.1 (Every Basis Sees the Blow-Up v4.0, Theorem 4.1; PAPER PROOF).** Suppose a linear space \(K\subseteq\mathbb F^I\) has blocks \(I_v\) indexed by the vertices of \(G\), with an integer \(d\ge1\), and satisfies:

- **(R)** Joint projection to the blocks in every \(X\subseteq V\) has rank at least \(d|X|\).
- **(L)** Any two vectors nonzero on the same vertex block intersect in support.
- **(E)** Any two vectors nonzero on blocks indexed by adjacent vertices intersect in support.

Then, for every finite spanning family \(B\) of \(K\),

\[
G[K_d]\subseteq H_B.
\tag{8}
\]

If \(B\) is a basis and \(\dim K=d|V|\), the embedded copy spans \(H_B\).

*Proof.* Let \(S_v=\{j\in J:b_j|_{I_v}\ne0\}\). Conditions (L) and (E) ensure that each \(S_v\), and each \(S_u\cup S_v\) for an edge \(uv\), is a clique of \(H_B\). Because \(B\) spans \(K\), the restrictions of \(\{b_j:j\in\bigcup_{v\in X}S_v\}\) span the projection of \(K\) to \(X\). By (R),

\[
\left|\bigcup_{v\in X}S_v\right|\ge d|X|.
\]

Hall's theorem, applied to \(d\) copies of each vertex, supplies mutually disjoint choices \(A_v\subseteq S_v\) with \(|A_v|=d\). Mapping the \(d\) vertices over \(v\) in the clique blow-up to \(A_v\) gives the edge-preserving injection. The basis case has exactly \(d|V|\) members and the injection is a bijection. \(\square\)

The proof is striking because it quantifies over *every* spanning family, not merely over coordinate bases found by one algorithm. The universality is nevertheless confined to spanning families of one coordinatised linear space.

### 4.3 Why the colouring kernel meets the hypotheses

Every nonzero vector of the two-dimensional zero-sum triple space \(T_{\mathbb F}\) has at least two nonzero coordinates. Hence two nonzero vectors on the same colour block have overlapping support. If two vectors are nonzero on blocks belonging to adjacent vertices, the edge-slack coordinates supply support intersection when the vertex-coordinate intersections do not already do so. Full projection rank follows from the independent selection of vertex triples.

Consequently the \(d=2\) hypotheses hold for \(K_G(\mathbb F)\) over **every field**, and

\[
\boxed{G[K_2]\subseteq H_B}
\qquad\text{for every finite spanning family } B.
\tag{9}
\]

This is Theorem 5.4 of the standalone paper. Its canonical basis has two generators per vertex and produces exactly \(H_{B_{\rm nat}}\cong G[K_2]\).

### 4.4 Exact optimized width

Because treewidth and pathwidth are subgraph-monotone and the canonical basis achieves equality,

\[
\min_B\operatorname{tw}(H_B)=2\operatorname{tw}(G)+1,
\tag{10}
\]
\[
\min_B\operatorname{pw}(H_B)=2\operatorname{pw}(G)+1,
\tag{11}
\]
\[
\min_B|E(H_B)|=|V|+4|E|.
\tag{12}
\]

The same simultaneous-optimality conclusion holds for **every subgraph-monotone parameter** evaluated on the overlap graph of a basis.

In particular, the *decision problem* “given \(G\) and \(k\), is there a basis of \(K_G\) with overlap treewidth at most \(2k+1\)?” is exactly equivalent to the graph treewidth decision problem on \(G\). This gives an immediate restricted-optimization hardness interpretation; it does not say that the original graph-colouring decision problem has high time complexity.

### 4.5 Limits and negative controls

The paper's Remark 6.4 is binding: an identity about a representation parameter is not a running-time lower bound.

Proposition 6.5 gives a sharper counterexample. Let \(G=K_n\), \(n\ge4\). Then \(\operatorname{tw}(G)=n-1\), so

\[
\min_B\operatorname{tw}(H_B)=2n-1.
\tag{13}
\]

Nevertheless \(F(K_n)\) contains a fixed unsatisfiable \(F(K_4)\) subformula, hence its standard CNF translation has a Resolution refutation of **constant size**, independent of \(n\). Thus no unbounded function of optimized overlap treewidth alone lower-bounds Resolution proof size on all these formulas.

A separate control is \(K_{n,n}\): its treewidth grows with \(n\), and consequently the overlap width is \(2n+1\), yet a bipartite graph is trivially 3-colourable. The source problem can be easy on the entire displayed family while the structural width diverges.

These two controls address both sides of a decision problem: fixed unsatisfiable witnesses and easily constructible satisfying witnesses. Any proposed universal “large overlap width implies difficult computation” claim fails.

### 4.6 Formal verification boundary

The 19 November repository contains Lean 4 developments in **WStar.lean** and **WStarLower.lean**. The project reports formal checks of the GF(3) optimized treewidth identity, including relevant clique and width lemmas. The independent formalisation of the general-field, spanning-family **subgraph statement** in Theorems 4.1 and 5.4 is not present in the checked formal scope.

This synthesis therefore distinguishes:

\[
\text{GF(3) width result: FORMAL REPORTED},
\]

from

\[
\text{arbitrary-field subgraph theorem: PAPER PROOF}.
\]

The distinction matters for the design of future reductions; replacing a width inequality with a stronger subgraph assertion cannot be attributed to the existing Lean files.

---

## 5. Graph separators, matching and structured proof systems

### 5.1 Perfect Matching as Exact-One SAT

Let \(G=(V,E)\) be a graph and associate a Boolean variable \(x_e\) with each edge. The formula

\[
\Phi_G=\bigwedge_{v\in V}\operatorname{EXACT1}\bigl((x_e)_{e\ni v}\bigr)
\tag{14}
\]

describes perfect matchings. For cubic graphs the local exact-one constraints have arity three. A satisfying assignment selects exactly one edge incident to each vertex; conversely any perfect matching satisfies every local constraint. This is a bijection.

### 5.2 The boundary-signature rank identity

Partition edges as \(E=A\dot\cup B\), and let \(\partial(A,B)\) denote vertices incident with edges of both sides. A locally valid partial matching on \(A\) covers every vertex with incident edges only on \(A\) and covers each boundary vertex at most once. Its *boundary signature* is the set of boundary vertices it matches. Define analogous signatures for \(B\).

For the Boolean communication matrix \(M_{A,B}\) whose entries indicate whether the union of the two chosen edge subsets is a perfect matching, two internally valid partial matchings can be combined exactly when their boundary signatures are complementary.

**Lemma 5.1 (boundary-signature identity; elementary derivation, not an all-vtree bound).** For any field \(\mathbb F\),

\[
\operatorname{rank}_{\mathbb F}M_{A,B}
=
\#\{\sigma:
\sigma\text{ is realised on }A,\ 
\partial(A,B)\setminus\sigma\text{ is realised on }B\}.
\tag{15}
\]

*Proof.* Delete the zero rows and columns corresponding to internally invalid partial edge selections. Group all remaining rows by their signatures \(\sigma\) and columns by their complementary signatures. Entries are one precisely inside compatible row-column pairs. Under row and column permutations the matrix decomposes into independent nonempty all-ones blocks, one for each compatible signature, and zero off-block entries. Each nonempty all-ones block has rank one over any field, including positive characteristic. Summing the ranks proves (15). \(\square\)

The identity is not new merely because it is proved here; a literature-level priority check is necessary. It also does not imply that the rank is exponential under all possible decompositions.

### 5.3 Alternating-cycle rank mechanism

Suppose a fixed perfect matching admits \(r\) vertex-disjoint alternating cycles such that flipping each cycle changes a boundary signature. Flipping any subset gives \(2^r\) distinct compatible boundary signatures; using Lemma 5.1 yields

\[
\operatorname{rank}_{\mathbb F}M_{A,B}\ge2^r.
\tag{16}
\]

The essential missing quantifier is **every relevant vtree**. Proving (16) for a chosen cut or random cuts does not produce a universal structured-compilation lower bound. One must show that every vtree has a cut with a sufficiently large family of independent, realisable alternating-cycle choices.

This obligation is precisely the unresolved main theorem of K6. The number of perfect matchings alone cannot replace it. Prism graphs have exponentially many perfect matchings but bounded treewidth and small structured representations.

### 5.4 SAT-to-UNSAT lifting

Berkholz–Micun, *Proof Systems Based on Structured Circuits* (SAT 2026), develop a lifting method from satisfiable CNFs hard for certain structured representations to unsatisfiable CNFs hard in associated proof systems. The statement is model-specific, including the exact structural restrictions and weakening rules.

The repository also records a related candidate using an exact-one translation of an independent-set constraint on expander graphs. That construction is **not** the same as the cubic Perfect Matching encoding. Its potential lifting consequence must be assessed independently, and known polynomial Resolution refutations prohibit promoting the result into a claim about all refutation systems.

---

## 6. Streaming Search-MCSP: the QE* line

### 6.1 Search-MCSP and the compression trade-off

Let \(N=2^m\) be the length of a truth table \(x\in\{0,1\}^N\), and let \(s(m)\) be a circuit-size threshold. The decision Minimum Circuit Size Problem asks whether \(x\) describes a Boolean function having a circuit of size at most \(s(m)\); the *total search* problem additionally requires a suitable circuit on positive instances and a correct rejection on negative instances.

In a deterministic one-pass streaming model, the machine reads the bits of \(x\) sequentially, maintaining a state \(q_t\) and performing an update

\[
q_{t+1}=U_t(q_t,x_{t+1}).
\tag{17}
\]

A resource claim must specify the bit space \(S\), the worst-case cost \(U\) of an update, the treatment of output and decoding, the machine model, uniformity, circuit basis and any allowed oracles.

McKay–Murray–Williams (STOC 2019) establish a theorem under which a sufficiently strong streaming lower bound for the exact version of Search-MCSP, with prescribed parameters and possible oracle qualification, would imply \(P\ne NP\). Their theorem is a conditional **published transfer**, not an assertion that the needed lower bound is already known.

### 6.2 Low-state upper bounds without time bounds

Let \(\mathcal I_{m,s}\subseteq\{0,1\}^N\) be the truth tables computed by circuits of size at most \(s\). The count of such circuits is bounded by

\[
|\mathcal I_{m,s}|
\le 2^{O(s\log(m+s))}.
\tag{18}
\]

At each prefix length \(t\), the number of nonempty residual languages \(\{q:pq\in\mathcal I_{m,s}\}\) is at most \(|\mathcal I_{m,s}|\), plus a dead residual. Hence the minimal state encoding has size \(O(s\log(m+s))\) bits **if transition computation is free**.

This is a serious obstruction to pure state-count, Myhill–Nerode and one-way communication arguments. Such methods do not prove the required worst-case update-time lower bound. The project labels this observation S0006 in the QE* proof state.

### 6.3 QE* and the open G0004/G0005 obligations

Write **QE*** for the proposed assertion that the appropriate total Search-MCSP streaming problem cannot be solved with both polynomially bounded workspace and polynomially bounded per-update computation, in the precise MMW model and asymptotic parameter range.

The verified implication to pursue is schematically

\[
\boxed{
QE^*\Longrightarrow P\ne NP
}
\tag{19}
\]

where *QE* must be interpreted as a statement satisfying **all** hypotheses of the selected published theorem.

The inspected live proof reconstruction lists:

- **G0004:** a representation-independent lower bound on worst-case update computation for the entire admissible class;
- **G0005:** a nonrelativising property that distinguishes ordinary computation from known efficient oracle-assisted constructions.

The first false inference in an earlier candidate was that an update must explicitly decide whether the newly read prefix remains extendible. Exact streaming semantics require preservation of distinguishable future outcomes, but allow work to be deferred, recoded, shared or performed by a later decoder. The explicit C5 inference was withdrawn.

Another false route claimed update cost was lower-bounded by the rank of a linear transition matrix. The identity update has arbitrarily large rank and zero nontrivial arithmetic operations, so that inference also fails.

### 6.4 A proposed computation-to-width bridge

The proposed mathematical route through Theorem 4.1 is to associate to every admissible Search-MCSP algorithm \(\mathcal M\), with resources \(S,U\), a graph \(G_{m,s}\), a coordinatised linear space \(K_{m,s}\) and a spanning family \(B_\mathcal M\), such that:

\[
\operatorname{tw}(H_{B_\mathcal M})
\le f(S,U,m,s)
\tag{20}
\]

and the hypotheses (R), (L), (E) apply to \(K_{m,s}\). Then Theorem 4.1 would give a lower bound on the same width.

The required chain would be

\[
d\bigl(\operatorname{tw}(G_{m,s})+1\bigr)-1
\le \operatorname{tw}(H_{B_\mathcal M})
\le f(S,U,m,s).
\tag{21}
\]

If the left side were asymptotically incompatible with the right side for **every** allowed polynomial resource bound, the selected MMW transfer might apply.

Equation (21) is a **research template**, not a theorem about Search-MCSP. Three independent gaps are visible:

1. A general algorithm state need not define a basis or even a linear representation satisfying (R), (L), (E).
2. A large overlap width does not by itself impose an update-time cost, as Proposition 6.5 illustrates in a related proof setting.
3. The supposed width-to-cost inequality must fail appropriately for the published oracle-assisted construction, or it would contradict that construction.

### 6.5 Why a structure absent from easy instances is necessary

No theorem of the form “every algorithm for a high-width colouring kernel pays cost \(g(\operatorname{tw})\)”, with unbounded \(g\), can be valid. The \(K_n\) and \(K_{n,n}\) controls show that hard-coded local contradictions and easy witnesses can coexist with growing optimized width.

A promising repaired statement must therefore incorporate an additional property specific to the **Search-MCSP input family**, not just width. Candidate properties include the computational complexity of exact residual transitions, the necessity of finding a replacement witness under arbitrary bit arrivals, or a quantified inability to eliminate shared gates in the relevant circuit family. These are research candidates, not accepted mathematical invariants.

The project question **Q-9c4d56f01f** is intended to address this bridge. The identifier is supplied by the current research discussion; it has not been independently located in the older GitHub snapshot examined for this manuscript.

---

## 7. MCSP-specific circuit-to-formula transfer

### 7.1 Circuit reuse is the central obstacle

Let \(F_{N,\beta}=\mathrm{MCSP}[N^\beta]\), for fixed \(0<\beta<1\). Let \(L(F)\) be De Morgan formula leaf count and \(CC(F)\) general Boolean circuit size in the specified basis. A circuit is a DAG and permits sharing; a formula is a tree and generally duplicates reused computations.

The PNP-001 REUSE-MCSP note gives an elementary simulation:

\[
L(F)\le O(S\,2^r)
\tag{22}
\]

for a circuit of size \(S\) with \(r\) reused gates (under the defined conventions). This is a general *upper bound*, not the strong subquadratic simulation required for the separation programme.

Parity and inner-product controls expose the danger of an unrestricted subquadratic circuit-to-formula conversion. The improvement must be **specific to the MCSP functions or the circuits appearing in a selected transfer**, and must survive arbitrary fan-out and nested sharing.

### 7.2 Conditional theorem R

The repository formulates the open hypothesis R-MCSP:

> There exist fixed constants \(C>0\), \(0\le c<1\) and \(\beta_0>0\) such that for every sufficiently small fixed \(0<\beta<\beta_0\), and sufficiently large \(N\),
>
> \[
> L(F_{N,\beta})\le C\,CC(F_{N,\beta})^{1+c}.
> \tag{23}
> \]

**Theorem 7.1 (conditional R-MCSP implication; as in the archived note).** Assuming (23), the published fixed-threshold MCSP formula lower bound of Chen–Jin–Williams, and the relevant MMW circuit consequence with their exact matching conventions, then \(NP\not\subseteq P/poly\), hence \(P\ne NP\).

*Derivation.* The published fixed-threshold formula lower bound gives, for any fixed \(0<\beta<1\) and \(\eta>0\), with sufficiently large \(N\),

\[
L(F_{N,\beta})>N^{2+\beta-\eta}.
\tag{24}
\]

By (23),

\[
CC(F_{N,\beta})
>
\left(\frac{N^{2+\beta-\eta}}{C}\right)^{1/(1+c)}.
\]

Choose \(\eta<1-c\). For all sufficiently small \(\beta\), the right-hand side exceeds \(N^{1+\delta}\) for some fixed \(\delta>0\) independent of \(\beta\), absorbing the constant \(C\).

On the other hand, the appropriate MMW implication under \(NP\subseteq P/poly\) yields circuits of size \(N\operatorname{poly}(s)\) for the Search-MCSP task and, with the output-verification and search-to-decision overhead explicitly accounted for, corresponding MCSP decision circuits. For \(s=N^\beta\) this is at most \(N^{1+k\beta}\) for a fixed polynomial exponent \(k\). Choose \(\beta<\delta/k\). This contradicts the previous lower bound, yielding \(NP\not\subseteq P/poly\). \(\square\)

**The condition (23) remains OPEN.** The proof is a valid conditional composition only when the threshold parameter, circuit basis, formula measure, search-to-decision conversion, and polynomial exponent are matched exactly. The source note correctly identifies (23) as the missing mathematical statement; it does not assert a separation.

### 7.3 Can the hypothesis be weakened?

A focused alternative is to restrict the simulation to the **special family of circuits produced in the MMW conditional construction** rather than to every optimal circuit computing MCSP. This could require less than (23), but no such weaker sufficient simulation is yet proved.

This is distinct from QE*: a successful circuit-to-formula simulation would need its own formal quantitative audit and might establish a separation without a streaming state/width embedding at all. The fact that both routes confront reuse and representation changes does not establish their mathematical equivalence.

