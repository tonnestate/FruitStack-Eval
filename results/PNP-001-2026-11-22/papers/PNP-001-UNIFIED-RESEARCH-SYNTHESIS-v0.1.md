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


---

## 8. Constructive hardness, refuters and range avoidance

### 8.1 From existential failure to an efficiently found counterexample

A traditional lower bound may assert that every circuit in a class fails on at least one input. A *constructive separation* strengthens this: given the attempted algorithm, a uniform, resource-bounded refuter must efficiently output an input on which the algorithm errs.

Chen–Jin–Santhanam–Williams, *Constructive Separations and Their Consequences*, establish several published transfer theorems in which sufficiently efficient refuters for carefully specified weak algorithms would entail strong complexity separations, including \(P\ne NP\).

These theorems require a resource-sensitive definition of a refuter. In particular, it is not enough for a finite exhaustive search to find a counterexample to one small circuit. The quantification includes the target algorithm family, all relevant sizes, the uniformity class, the complexity of the refuter itself, and sometimes randomized success guarantees.

### 8.2 Three distinct tasks

There are three logically separate forms of avoidance:

**Individual falsification.** Given a specific candidate circuit \(C\), output an input \(x\) with \(C(x)\ne f(x)\). A SAT solver may be adequate for small circuits, but its runtime must be counted.

**Range avoidance.** Given a circuit or generator \(G:\{0,1\}^r\to\{0,1\}^N\) with \(r<N\), construct an element \(y\notin\operatorname{im}(G)\). The existence of such a \(y\) follows by counting. Efficient construction is a different claim.

**Uniform refutation.** Given the description of any attempted algorithm in a specified class, a highly restricted uniform generator outputs a correctly certified counterexample within the exact resource bounds of the published transfer.

A range-avoidance witness for the circuit-evaluation map can be viewed as a truth table outside the image of all circuits below a given size. This viewpoint makes the finite circuit-synthesis and exact-checking tools relevant as falsifiers. It does not automatically promote them into a uniform asymptotically efficient refuter.

### 8.3 Direct conditional transfer

The K8 research contract prioritises Theorem 1.7 and the related Section 4 propositions of Chen–Jin–Santhanam–Williams. It also identifies a distinct DISJ-refuter transfer. These published implications must be restated with their **complete original parameters** before they are used as edges of the present proof graph.

For the MCSP route, the desired form is

\[
\text{efficient uniform refuter meeting CJSW hypotheses}
\quad\Longrightarrow\quad
P\ne NP.
\tag{25}
\]

The left-hand assertion is **OPEN** for the constructions in PNP-001. The project's finite counterexample engines, exhaustive circuit enumerators, small exact SAT witnesses and agent-based adversarial reviews do not by themselves satisfy it.

### 8.4 Why this line may evade the width bridge

A refuter can sometimes establish a computational separation by exhibiting failures of all candidate procedures **without** proving that their internal computations have a specific low-width representation. Therefore a single universal computation-to-width theorem cannot be declared a necessary condition for this research route.

This logical independence is material to the proposed “union theorem”: any claim that all four fronts share one unavoidable proof step must either show how refuters factor through that step, or replace “necessary for every route” with the weaker claim that the step is sufficient for a chosen combined strategy.

---

## 9. Algorithmic methods, counting and algebraic complexity

### 9.1 Faster algorithms as sources of lower bounds

Williams' algorithmic method converts sufficiently strong algorithms for analysing a circuit class into lower bounds against that same class, subject to exact closure conditions, running times, circuit sizes and uniformity assumptions. This strategy is logically different from directly proving an invariant of an arbitrary streaming state.

The PNP-001 P1 track uses Chen–Tal–Wang (2026), *Super-quadratic Lower Bounds for Depth-2 Linear Threshold Circuits*. The external result establishes lower bounds of order \(n^{2.5-\varepsilon}\) for suitable functions in \(E^{NP}\) against depth-two threshold circuits \(THR\circ THR\). Extending the circuit-analysis algorithm to every desired fixed polynomial-size threshold family would yield further **class-specific** lower bounds. This is not, without another theorem, \(P\ne NP\).

The exact function class matters: a lower bound for a language in \(E^{NP}\) is not automatically a lower bound for one in NP, and a size bound against \(THR\circ THR\) does not apply to unrestricted Boolean circuits.

### 9.2 Counting, tensor contraction and symbolic computation

The K7 research programme compares tensor-contraction and sparse-algebraic counting algorithms, including subexponential #SAT methods discussed in 2026 preprints. Even a rigorously proved \(2^{o(n)}\) algorithm for 3-SAT is superpolynomial unless its full bound is polynomial. It does not establish \(P=NP\), and it does not establish \(P\ne NP\).

Any proposed circuit lower bound based on improved counting must preserve:

- the exact circuit class analyzed;
- gate types and fan-in;
- size and depth thresholds;
- the number of variables and clauses produced by encodings;
- randomized versus deterministic guarantees;
- uniformity, nonuniform advice and oracle operations.

A finite improvement on the exact-one cores or a low-degree subclass does not imply the algorithm required by a Williams-style transfer for all circuits of the target class.

### 9.3 Low-degree polynomial identity testing

Chukhin–Gajulapalli–Golovnev–Mihajlin (2026) develop a connection between improved low-degree polynomial identity testing and unconditional circuit lower bounds, with a disjunctive conclusion involving strong Boolean lower bounds for a specified class or an arithmetic separation.

A disjunction

\[
A\lor B
\]

is not a proof of \(A\). In particular, a Boolean lower bound for a potentially different NP language for every fixed exponent \(k\),

\[
\forall k\ \exists L_k\in NP:\ L_k\notin\mathrm{SIZE}(n^k),
\tag{26}
\]

has different quantifiers from

\[
\exists L\in NP\ \forall k:\ L\notin\mathrm{SIZE}(n^k),
\tag{27}
\]

which is the type of assertion needed to exclude \(NP\subseteq P/poly\). The project explicitly recorded this distinction as a control in its 21 November owner proof-chain review.

The exact arithmetic model and characteristic also matter. An invariant proved only for polynomials over \(\mathbb F_2\) need not imply a theorem about circuits over \(\mathbb Z\) or \(\mathbb Q\).

### 9.4 Bounded arithmetic and stronger proof systems

The PNP-001 programme also studies transfers involving bounded arithmetic, Extended Frege, proof complexity of circuit lower-bound statements, and the Weak Rank Principle. These are important but model-sensitive.

In general, a short computation trace is not automatically a short certificate of its correctness. A proof system can simulate an algorithm only under precise formalizability and soundness hypotheses. An exponential lower bound for one proof system does not refute the existence of all polynomial-time decision procedures.

A successful stronger algebraic proof-system lower bound could be a major independent theorem without resolving \(P\) versus \(NP\). In such cases the paper should state the genuine proof-complexity contribution rather than promoting it to a general-computation claim.

### 9.5 Four routes compared

| Route | Starting result | Missing premise | Published or conditional endpoint | Current status |
|---|---|---|---|---|
| Streaming QE* | MMW resource-bounded compression | General worst-case update lower bound with exact oracle and representation hypotheses | \(P\ne NP\) | OPEN G0004/G0005 |
| R-MCSP | CJW fixed-threshold MCSP formula bound | MCSP-specific subquadratic circuit-to-formula bound, uniform for small \(\beta\) | \(NP\not\subseteq P/poly\) through MMW | OPEN |
| Gap-MCSP magnification | Oliveira–Pich–Santhanam | Correct general-circuit lower bound in the precise parameter window | \(NP\not\subseteq P/poly\) under stated magnification hypothesis | OPEN |
| Constructive refuters | CJSW separations and known component hardness | Required uniform, efficient refuter for exact target model | \(P\ne NP\) under stated refuter theorem | OPEN |
| Threshold-circuit algorithms | Chen–Tal–Wang, Williams-style transfer | Stronger circuit analysis at each relevant polynomial size | \(E^{NP}\) lower bounds for restricted threshold class | Restricted-model frontier |
| Algebra / proof systems | Theorems 12, 14, 16; K6; published lifting | Stronger system lower bounds and exact simulations | Proof-system/algebraic separations, not automatic \(P\ne NP\) | Restricted-model frontier |

The table has six technical rows because the four fronts consist of multiple distinct transfer mechanisms. “Four fronts” refers to organisational groupings, not an asserted equivalence theorem.

---

## 10. A candidate unification theorem

### 10.1 The motivating question

The new research question is whether the different lower-bound programmes can be organised around one proof obligation: **must a fast exact computation induce a low-complexity representation in a class for which a structural lower bound is known?**

This is the subject of the proposed organisation-level *union theorem* **Q-a1e6376406**. The identifier is reported by the ongoing research discussion and was not yet present in the older GitHub snapshots inspected during preparation.

We formalise the question as a general proof template rather than claiming the requested theorem has been established.

### 10.2 Models and maps

Let \(L=(L_n)\) be a decision or search family, and let \(\mathsf{Alg}_n(L)\) denote all admissible algorithms for \(L_n\) in a specified model. Let

\[
\operatorname{cost}(\mathcal A)
\]

measure the relevant time or circuit resources, and let \(\mathcal R_n(L)\) be a family of structured representations with a nonnegative complexity measure

\[
\mu:\mathcal R_n(L)\to\mathbb R_{\ge0}.
\]

A *sound resource-preserving representation transfer* comprises a map \(\Phi_n\) defined for **every** admissible algorithm \(\mathcal A\), plus a proved quantitative bound

\[
\Phi_n(\mathcal A)\in\mathcal R_n(L),
\qquad
\mu(\Phi_n(\mathcal A))
\le F(n,\operatorname{cost}(\mathcal A)).
\tag{28}
\]

It must also preserve the semantics needed for the lower bound: a representation constructed from an algorithm must represent the same total search or decision relation, not a promise restriction or an unrelated encoding.

A *representation lower bound* is a theorem

\[
\forall R\in\mathcal R_n(L),\quad \mu(R)\ge H(n).
\tag{29}
\]

### 10.3 The elementary bridge principle

**Proposition 10.1 (conditional bridge principle).** If (28) and (29) hold for the *same* representation class, measure and input family, then every admissible algorithm \(\mathcal A\) satisfies

\[
H(n)\le F(n,\operatorname{cost}(\mathcal A)).
\tag{30}
\]

*Proof.* Substitute \(R=\Phi_n(\mathcal A)\) into (29), then apply (28). \(\square\)

This proposition is tautological as mathematics; its role is to expose rather than hide the difficult premise. All nontrivial work lies in proving a sufficiently strong map (28) and a sufficient bound (29) for the exact model.

For PNP-001 the proposed choices are:

\[
\mathcal R_n(L)=\{\text{spanning-family support-overlap representations of }K_{m,s}\},
\]

\[
\mu(R)=\operatorname{tw}(H_R),
\]

and a construction from every low-resource Search-MCSP streaming algorithm to such a spanning family. **That construction has not been proved.**

### 10.4 Required strength for the Hall route

A successful Hall-based application would need:

1. A uniform family of graph-indexed spaces \(K_{m,s}\) derived from Search-MCSP semantics.
2. A proof of conditions (R), (L), (E) in those spaces, with a positive rank parameter \(d\).
3. A mapping from *every* relevant deterministic streaming algorithm, including arbitrary nonlinear state encodings, to a spanning family \(B_{\mathcal A}\).
4. A bound \(\operatorname{tw}(H_{B_{\mathcal A}})\le F(m,s,S,U)\) justified by *actual* computation, not merely by state counting.
5. A family of graphs with \(\operatorname{tw}(G_{m,s})\) large enough to contradict that upper bound for all required resource exponents.
6. An oracle test showing precisely why the argument does **not** erroneously forbid the known MMW oracle construction.

The resulting inequality would have the form

\[
d\bigl(\operatorname{tw}(G_{m,s})+1\bigr)-1
\le \operatorname{tw}(H_{B_{\mathcal A}})
\le F(m,s,S,U).
\tag{31}
\]

Everything on the right of the first inequality remains a new research obligation when interpreted as a universal theorem about streaming computation. The published Hall result supplies only the left-hand structural ingredient once its hypotheses have been established.

### 10.5 An obstruction to universal width-to-work claims

**Proposition 10.2 (no unconditional width-only proof-cost bound).** No unbounded function \(g\) can satisfy

\[
\operatorname{ResolutionSize}(F(G))
\ge g\!\left(\min_B\operatorname{tw}(H_B)\right)
\]

for all unsatisfiable colouring-encoded formulas \(F(G)\).

*Proof.* Take \(G=K_n\) for \(n\ge4\). By (13) the width is \(2n-1\), while a fixed \(K_4\) contradiction supplies a Resolution refutation of bounded size. \(\square\)

This does **not** refute every possible Search-MCSP-specific bridge. It refutes the shortcut that simply equates structural width and computation without a further hypothesis.

A second, distinct danger is the identity update on a large state vector: a transition matrix may have high rank but be implemented with no nontrivial arithmetic gates. A lower bound on dimension or rank is not automatically a lower bound on update operations.

### 10.6 Four-front factorisation: proposed theorem, not established

The strongest contemplated **union theorem** would prove that each of F1–F4 either yields a representation lower bound of a shared type or can be transferred, through a known quantitative simulation, to one common missing statement \(\mathcal U\). Formally, for each route \(i\), a factorisation

\[
\mathcal H_i\xRightarrow[\text{proved}]{T_i}\mathcal U
\quad\text{or}\quad
\mathcal U\xRightarrow[\text{proved}]{S_i}\mathcal H_i
\tag{32}
\]

would be required, with directions fixed by the intended separation. The arrows may not be chosen opportunistically after the fact.

**Present verdict: OPEN.** The following obstacles to a common factorisation are substantive:

- A constructive refuter need not operate through a support-overlap representation.
- Williams-style algorithm-to-lower-bound methods can avoid the width model entirely.
- IPS and roABP lower bounds apply to certificates, not necessarily to online streaming computations.
- Circuit-to-formula transfers charge sharing and DAG fan-out, which treewidth alone does not capture.
- Even when two models use the same word “rank,” their matrices, fields, variable partitions and resource semantics may differ.

Therefore the defensible present claim is narrower:

> A common **logical audit method** applies to all four fronts: identify the restricted result, the precise target theorem, and the earliest missing quantitative implication. A common **mathematical bottleneck theorem** remains to be proved.

This is the exact role of Q-a1e6376406. A proof that the four fronts truly share one reducible obligation would be a new theorem. Merely drawing arrows between their names is not.

### 10.7 Dependency graph

The following is a *status-labelled* research graph. A solid arrow denotes a proved implication in its specified model; a dashed arrow denotes an open research obligation.

~~~text
GF(3) two-value criterion ──► algebraic description of EXACT1-SAT
            │
            ├──► finite blind-core census / matroid-port obstruction
            │
            └──► graph-colouring exact-one family
                        │
                        ├──► PC degree transfer (specified axioms)
                        │           └──► restricted proof-size lower bounds
                        │
                        └──► homogeneous colouring kernel
                                     └──► universal Hall embedding
                                                └──► sharp overlap width
                                                        - - -► [COMPUTATION BRIDGE]
                                                                  │
Search-MCSP streaming state / updates - - - - - - - - - - - - - - -┘
                                                                  │
                                                                  - - -► QE*
                                                                              │
                                                                              └──► P ≠ NP [MMW, conditional]

CJW formula lower bound ──► [R-MCSP simulation OPEN] ──► circuit LB
                                                              │
                                                              └──► P ≠ NP [MMW magnification]

Exact circuit synthesis ──► [uniform refuter OPEN] ──► P ≠ NP [CJSW]

Restricted IPS / roABP / matching ──► restricted proof-system LB
                                           - - -► [general-model bridge OPEN]

Fast threshold-circuit analysis - - -► stronger E^NP restricted-circuit LB

Proposed union Q-a1e6376406: factorisation of the separate open bridges [OPEN].
~~~

The dependency graph is not a proof that every route must go through the computation bridge. It makes clear where the arrows remain missing.

---

## 11. Proof barriers and mandatory falsification

### 11.1 Relativisation and oracle stress

Baker–Gill–Solovay show that methods preserved under arbitrary oracle relativisation cannot settle the general \(P\) versus \(NP\) question. In the streaming programme, a more concrete stress test is available: the selected MMW construction uses powerful oracle operations. A proposed no-fast-update theorem must state exactly which premise fails once those oracle gates are admitted.

Declaring a technique “nonrelativising” does not supply this missing argument. Conversely, a technique using polynomials is not automatically subject to every algebraisation barrier.

### 11.2 Natural proofs and locality

Razborov–Rudich's Natural Proofs obstruction applies under particular pseudorandom-function hypotheses to certain constructive and sufficiently large combinatorial properties. The *locality barrier* in hardness magnification concerns classes of arguments insensitive to the availability of small oracle gates. A correct audit evaluates these hypotheses against the exact candidate method, model and parameter range rather than rejecting an argument by analogy.

### 11.3 Easy high-width controls

Candidate width-based theorems must survive:

- \(K_n\): linear overlap-width growth with a fixed \(K_4\) contradiction.
- \(K_{n,n}\): growing width with a trivial colouring algorithm.
- Prism graphs: many perfect matchings and bounded treewidth.
- Functions that are algebraically high-rank as formal polynomials but identically zero on Boolean inputs.
- Identity updates, parity sketches, bounded-rank affine encodings and nonlinear recodings.
- An algorithm that postpones costly work to the decoder.
- An algorithm whose DAG shares expensive intermediate calculations.

The “first false line” principle is essential: when a step fails, the exact invalid implication and smallest counterexample must be archived. An edited conjecture is new and unproved until independently checked.

### 11.4 Quantifier and asymptotic controls

A proposed separation must be checked for the order of all quantifiers. In particular:

\[
\forall k\ \exists L_k
\quad\text{is not the same as}\quad
\exists L\ \forall k.
\]

Likewise a fixed \(s=1\) or \(s=2\) experiment at \(m=3,4\) does not imply a statement for \(s(m)=m^c\) at unbounded \(m\). A worst-case update-time bound is not an amortised bound. A decision algorithm is not automatically a total search algorithm without a proved conversion. A rank lower bound on one vtree cut is not a lower bound against every vtree.

---

## 12. Research record and reproducibility

### 12.1 Archived research objects

The principal sources for this synthesis are:

- Repository **tonnestate/FruitStack-Eval**, branch **cc/pnp001-results-20261118**.
- Repository **tonnestate/PNP-001-research**, branch **main**.
- Draft **PNP-001_Research_Manuscript_v0.24.docx** (20 November 2026).
- Draft **Every_Basis_Sees_the_Blow_Up_v4_2026-11-22.md**.
- **results/PNP-001-2026-11-19/lean/WStar.lean** and **WStarLower.lean**.
- **results/PNP-001-2026-11-20/acc0-level3/THEOREM-12.md** and **ACC0-L3-REPORT.md**.
- **results/PNP-001-2026-11-20/REUSE-MCSP-NOTE.md**.
- **results/PNP-001-2026-11-21/specifications/**, including K1, K6, K7, K8, K9, the lemma-M experiments and Grand Strategy.
- **results/PNP-001-2026-11-22/qe-star/QE-STAR-RECONSTRUCTION.md** and **PNP-001-CROSS-THEOREM-SYNTHESIS-2026-11-22.md**.
- **proofstate/Q-156fa9c912.json** in PNP-001-research.

The separate PNP-001-research proof-state snapshot contains 172 entries at its recorded commit f02b93c. The later QE-STAR-RECONSTRUCTION reports 198 live entries, of which 26 were newer than that GitHub snapshot. The full live state was **not directly available as a standalone repository file** in the examined branch. Claims based on the live state are therefore attributed to the reconstruction report rather than to independent inspection of the VPS.

### 12.2 Independent checks still required

The following remain separate release obligations:

1. Reproduce the Lean builds from a pinned toolchain and check the fidelity of the formal statements to the manuscript.
2. Formalise the abstract Hall embedding and arbitrary-field colouring subgraph theorem, or document why the current proof remains paper-only.
3. Reproduce finite enumeration and certificate archives under the same axiom and field conventions.
4. Audit published lower bounds and their exact parameter regimes before a separation transfer is claimed.
5. Verify the identities of source graph families and transformed CNFs at each gadget-lifting step.
6. Identify independent reviewer sessions and distinguish their mathematical findings from author-only checks.
7. Record every failed transfer in an append-only ledger without overwriting the earlier hypothesis.

The presence of hundreds or thousands of ledger entries does not change the acceptance criterion for any theorem.

### 12.3 Four-front research audit

| Front | Strongest available local starting point | First unproved general-computation step |
|---|---|---|
| F1, representation / streaming | GF(3) width theorem; residual-state formalism; linear-update controls | A representation-complete, oracle-sensitive *update-work* lower bound (G0004/G0005; Q-9c4d56f01f) |
| F2, MCSP / sharing | CJW fixed-threshold formula lower bound; conditional Theorem R | R-MCSP or a weaker sufficient simulation for exactly the MMW-derived circuit family |
| F3, algebra / proof systems | PC degree transfer; Theorems 12/14/16; K6 boundary signature analysis | Stronger system lower bounds and a justified quantitative simulation into the exact target class |
| F4, algorithmic methods / refuters | CTW threshold circuit lower bounds; CJSW conditional refuter theorems | Suitable uniform refuter or sufficiently strong circuit-analysis algorithm with complete parameter match |

---

## 13. Conclusions

We have reconstructed a connected but not yet closed programme of mathematical implications.

**First**, the GF(3) representation isolates exact-one satisfiability as a two-value condition in an affine solution space. The finite blind-core census, matroid-port obstruction, degree data and Chvátal–Gomory checks constitute substantive mathematical results in their stated models.

**Second**, the universal embedding theorem gives a sharp structural answer to basis optimisation for one homogeneous graph-colouring kernel. Every spanning family sees a copy of \(G[K_2]\), and the canonical basis achieves the minimum of every subgraph-monotone overlap parameter. This is a general-field paper theorem with a narrower GF(3) formal-verification record.

**Third**, restricted proof-system and structured-compilation results establish hardness for specific algebraic or graph-based representation systems. These results are not weakened by the observation that stronger systems or unrelated algorithms may be efficient; their mathematical content is precisely the restriction.

**Fourth**, published transfers through resource-bounded compression, MCSP hardness magnification, and uniform constructive refutation provide real conditional routes toward \(P\ne NP\). The conditions have not yet been established by the structural results.

**Fifth**, an attempted *unification theorem* remains an open research question. Four fronts can share a rigorous bookkeeping discipline, but it has not been proved that all four necessarily reduce to a single new computation-to-low-width implication. In particular, algorithmic methods and constructive refuters may establish strong results through mechanisms that do not factor through a Hall-type support-overlap theorem.

The present status can be summarised as

\[
\underbrace{\text{exact structural and restricted-model theorems}}_{\text{available in specified scopes}}
\quad+\quad
\underbrace{\text{published conditional transfers}}_{\text{available}}
\quad+\quad
\underbrace{\text{representation-complete computation bridge}}_{\text{OPEN}}.
\]

We do **not** claim that this establishes \(P\ne NP\). What the synthesis achieves is a sharper specification of the missing proof obligations, a hierarchy of independently useful theorem candidates, and explicit checks preventing a restricted-model result from being misreported as an unrestricted separation.

---

## Appendix A. The concrete next theorem to attempt

The computation-to-width programme should first try to state and falsify the following:

**Candidate A (OPEN, not a proven theorem).** Fix the exact MMW Search-MCSP model with \(s=s(m)\) meeting all theorem hypotheses. There exist uniformly constructible graphs \(G_{m,s}\), linear spaces \(K_{m,s}\) with block structure and a computable transformation \(\mathcal A\mapsto B_\mathcal A\), defined for every admissible exact deterministic one-pass algorithm \(\mathcal A\), such that:

1. \(K_{m,s}\) satisfies (R), (L), (E) with fixed \(d\ge1\).
2. \(B_\mathcal A\) spans \(K_{m,s}\).
3. \(\operatorname{tw}(H_{B_\mathcal A})\le F(m,s,S_\mathcal A,U_\mathcal A)\), with all construction work, output processing and decoder cost accounted for.
4. The lower bound \(d(\operatorname{tw}(G_{m,s})+1)-1\) exceeds \(F\) for every resource bound allowed by MMW for sufficiently large parameters.
5. A precisely identified premise fails in the known MMW oracle-assisted construction.

Only if all five clauses are proved does Candidate A provide the desired width-based entry to QE*. Clause 4 must be asymptotic and uniform across the relevant exponent choices. Clause 5 cannot be satisfied by an informal assertion of nonrelativisation.

The immediate falsification task is to test Clause 3 against nonlinear state encodings, arbitrary DAG reuse, time-dependent recoding, deferred decoding, and easy high-width examples.

## Appendix B. The requested union theorem

**Candidate B (Q-a1e6376406; OPEN).** Construct a single explicitly defined mathematical statement \(\mathcal U\) and establish, for each of the four fronts F1–F4, a *sound and quantitative* reduction making that front's sufficient separation premise follow from \(\mathcal U\), or proving a logically necessary factorisation through \(\mathcal U\).

Until the complete family of reductions is established, the phrase “all four fronts hinge on the same step” should be read as a **research hypothesis about possible proof organisation**, not as a mathematical theorem.

A successful Candidate B would unify the proof obligations; it would not alone prove \(P\ne NP\) unless \(\mathcal U\) itself were established and a published separation transfer completed.

## Appendix C. Source and reproducibility index

### Internal manuscripts and data

- [PNP-001 research results](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results)
- [Historical proof book](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-18/beweisbuch)
- [GF(3) formalisation](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-19/lean)
- [Theorem 12 and algebraic report](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-20/acc0-level3)
- [R-MCSP conditional reduction](https://github.com/tonnestate/FruitStack-Eval/blob/cc/pnp001-results-20261118/results/PNP-001-2026-11-20/REUSE-MCSP-NOTE.md)
- [PNP-001 strategy and bridge contracts](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-21/specifications)
- [QE* reconstruction and cross-theorem work](https://github.com/tonnestate/FruitStack-Eval/tree/cc/pnp001-results-20261118/results/PNP-001-2026-11-22/qe-star)
- [Independent proof-state repository](https://github.com/tonnestate/PNP-001-research/blob/main/proofstate/Q-156fa9c912.json)
- PNP-001, *Structural Invariants and General Computation*, manuscript v0.24, 20 November 2026 (conversation/library manuscript).
- Tonn, *Every Basis Sees the Blow-Up: A Universal Subgraph Theorem for Support-Overlap Graphs of a Colouring Kernel*, version 4.0, 22 November 2026 (conversation/library manuscript).

### External mathematical references

1. Baker, T.; Gill, J.; Solovay, R. (1975). *Relativizations of the P=?NP Question*. SIAM Journal on Computing. https://doi.org/10.1137/0204037
2. Razborov, A.; Rudich, S. (1997). *Natural Proofs*. Journal of Computer and System Sciences.
3. Aaronson, S.; Wigderson, A. (2009). *Algebrization: A New Barrier in Complexity Theory*. ACM Transactions on Computation Theory.
4. Lauria, M.; Nordström, J. (2017). *Graph Colouring is Hard for Algorithms Based on Hilbert's Nullstellensatz and Gröbner Bases*. CCC 2017. https://doi.org/10.4230/LIPIcs.CCC.2017.2
5. Pitassi, T.; Robere, R. (2018). *Lifting Nullstellensatz to Monotone Span Programs over Any Field*. STOC 2018.
6. Hakoniemi, T.; Limaye, N.; Tzameret, I. (2026). *Hard CNF Instances for Ideal Proof Systems*. ECCC TR26-070. https://eccc.weizmann.ac.il/report/2026/070/
7. Berkholz, C.; Micun, M. (2026). *Proof Systems Based on Structured Circuits*. SAT 2026. https://doi.org/10.4230/LIPIcs.SAT.2026.6
8. Chen, L.; Jin, C.; Williams, R. (2020). *Sharp Threshold Results for Computational Complexity*. STOC 2020 / ECCC TR20-065. https://eccc.weizmann.ac.il/report/2020/065/
9. McKay, D.; Murray, C.; Williams, R. (2019). *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*. STOC 2019. https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf
10. Oliveira, I. C.; Pich, J.; Santhanam, R. (2021). *Hardness Magnification Near State-of-the-Art Lower Bounds*. Theory of Computing 17. https://toc.cs.uchicago.edu/articles/v017a011/
11. Chen, L.; Jin, C.; Santhanam, R.; Williams, R. (2024). *Constructive Separations and Their Consequences*. TheoretiCS. https://theoretics.episciences.org/12881
12. Chen, L.; Tal, A.; Wang, Y. (2026). *Super-quadratic Lower Bounds for Depth-2 Linear Threshold Circuits*. ECCC TR26-039. https://eccc.weizmann.ac.il/report/2026/039/
13. Chukhin, N.; Gajulapalli, K.; Golovnev, A.; Mihajlin, I. (2026). *A Little Derandomization Goes a Long Way: Unconditional Circuit Lower Bounds using Low-Degree PIT*. ECCC TR26-313. https://eccc.weizmann.ac.il/report/2026/313/
14. Cook, S.; Reckhow, R. (1979). *The Relative Efficiency of Propositional Proof Systems*. Journal of Symbolic Logic.
15. Grochow, J.; Pitassi, T. (2018). *Circuit Complexity, Proof Complexity, and Polynomial Identity Testing: The Ideal Proof System*. Journal of the ACM.
16. Chen, L.; Hirahara, S.; Oliveira, I. C.; Pich, J.; Rajgopal, N.; Santhanam, R. *Beyond Natural Proofs: Hardness Magnification and Locality* (consult the exact published version for theorem and parameter statements).
17. Williams, R. (2014). *Nonuniform ACC Circuit Lower Bounds*. Journal of the ACM.
18. Atserias, A.; Ochremiak, J. (2017). *Proof Complexity Meets Algebra*. ICALP 2017. https://doi.org/10.4230/LIPIcs.ICALP.2017.110

**Bibliographic caution.** This is a working bibliography, not a final DOI-checked reference database. Specific theorem numbers and quantitative parameter regimes must be checked against the authoritative editions before a theorem is promoted from a research dependency to an established premise.

---

## Declarations

**Data availability.** Repositories and relevant branch paths are linked above. Some older drafts were supplied through the research conversations and are not necessarily included in the GitHub branch; the live VPS evidence may be newer than the public snapshot.

**Use of AI systems.** Multiple AI model families and code assistants contributed to discovery, calculations, counterexample search, independent criticism and drafting. Their participation is acknowledged as a research methodology; it does not constitute scientific acceptance.

**Novelty.** The status of some exact-one and embedding results relative to the full matroid, coding and graph-width literature remains subject to a complete priority search and external review. Published source results are not claimed as original PNP-001 theorems.

**Separation claim.** No unconditional proof of \(P=NP\) or \(P\ne NP\) is claimed.

*End of working synthesis, v0.1 — 22 November 2026.*
