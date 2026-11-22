# PNP-001: From Structural Obstructions to General Computation

## Exact-one satisfiability, algebraic kernels, proof complexity, and computational lower-bound implications

**Björn Tonn**  
**Working research manuscript — version 0.25, 22 November 2026**

> **Theorem status.** The structural Hall transfer and optimal overlap-width theorem have mathematical proofs, and the GF(3) width equivalence has an additional Lean formalisation. The conditional implication in Theorem 0.2 is a proved deduction; its universal online-circuit hardness premise is not established.

**Keywords:** P versus NP; positive exact-one satisfiability; \(\mathbb F_3\); two-valued affine solutions; matroid ports; support-overlap graphs; Hall embedding; treewidth; Polynomial Calculus; Nullstellensatz; ideal proof systems; roABP-IPS; perfect matchings; d-SDNNF; MCSP; Search-MCSP; streaming lower bounds; constructive refuters; hardness magnification; proof provenance.

---

## Abstract

We synthesise several lines of research initiated from the positive one-in-three satisfiability problem, with a common long-term objective of proving resource lower bounds for general computation. The starting point is the exact distinction between Boolean exact-one solutions and solutions of the associated affine equations over \(\mathbb F_3\). A two-value criterion describes Boolean satisfiability as an intersection property of an affine space. A classification of minimal GF(3)-blind unsatisfiable cores, a matroid-port obstruction, algebraic degree measurements, and a degree-preserving reduction from graph colouring make this distinction concrete.

A second line studies the homogeneous kernel of the graph-colouring exact-one encoding. A universal Hall-type argument, valid over arbitrary fields, embeds \(G[K_2]\) in the support-overlap graph of every spanning family of the kernel; a canonical basis attains equality. Consequently the minimum basis-overlap treewidth is \(2\operatorname{tw}(G)+1\), and the canonical basis simultaneously minimises every subgraph-monotone overlap parameter. This is a representation-independent theorem **within a precisely defined class of linear bases**, not a computational time lower bound. Indeed, complete graphs yield arbitrarily large minimum overlap treewidth while the corresponding unsatisfiable formulas have constant-size Resolution refutations.

Other work yields or investigates lower bounds in restricted proof and circuit models: Polynomial Calculus, Nullstellensatz, matchgates, algebraic branching programs and structured knowledge compilation. We trace the precise boundaries of these models and compare them with four routes toward complexity-class separations: (i) streaming Search-MCSP via the McKay–Murray–Williams (MMW) transfer, (ii) MCSP-specific circuit-to-formula conversion and hardness magnification, (iii) constructive refuters and range avoidance, and (iv) algorithmic methods and algebraic proof-system transfers.

The research has also isolated **L***, a specific online-circuit hardness hypothesis. A second audit recovered independent one-tape MCSP, direct DAG MCSP, uniform Hamming-promise MCSP (milestone K3), Kolmogorov boundary/one-way-function, strong proof-system and low-degree PIT (TR26-313) programmes, which have **different hypotheses and different conclusions**. Reviewed unrolling (the unrolling construction), the model-scoped resource simulation the machine-to-circuit simulation, and the published MMW transfer provide a complete **conditional** route from L* to \(P\ne NP\). The key proposed unification is a *computation-to-representation bridge*: under sufficiently strong, semantically justified hypotheses, a fast arbitrary computation might have to induce a restricted representation whose measured structural complexity is small. Such a bridge would let a structural lower bound contradict the existence of a fast computation. No presently inspected PNP-001 theorem establishes this bridge for all relevant algorithms, and the four routes are **not yet proved to factor through one common bottleneck**. We give precise conditional statements, a dependency graph, negative controls, and an audit framework for a candidate unification theorem. The manuscript consolidates the research without claiming \(P\ne NP\).

---

## Mathematical theorem chains

The following statements separate a proved theorem, a proved conditional implication, and an unproved antecedent. The detailed proofs and model conditions are preserved in the subsequent sections.

**Affine exactness.** For a positive exact-one formula \(F\), let \(\mathcal A_F=\{z\in\mathbb F_3^n:A_Fz=\mathbf1\}\). Every row of \(A_F\) has exactly three ones, hence \(A_F\mathbf1=0\). Translation by a constant therefore preserves the affine space, and
\[
\boxed{
F\text{ satisfiable}\iff
\mathcal A_F\cap\{0,1\}^n\ne\varnothing
\iff
\exists z\in\mathcal A_F:
|\{z_1,\ldots,z_n\}|\le2.
}
\tag{I}
\]

**Universal embedding.** For the homogeneous graph-colouring kernel \(K_G(\mathbb F)\), the full projection-rank (R), same-block support-intersection (L), and adjacent-block support-intersection (E) conditions are proved for every field. Their Hall consequence and the canonical-basis construction give
\[
\boxed{\forall B\text{ spanning }K_G(\mathbb F):
G[K_2]\hookrightarrow H_B},
\qquad
\boxed{\min_{B\text{ basis}}\operatorname{tw}(H_B)=2\operatorname{tw}(G)+1.}
\tag{II}
\]
These are **completed mathematical proofs**. Over \(\mathbb F_3\), the exact optimized-width equivalence is also expressed by proved Lean declarations for both inequality directions. The stronger all-field subgraph embedding is proved in the mathematical text, not asserted as an identically formalized Lean theorem.

**Algebraic proof transfer.** The Boolean exact-one condition has the characteristic-two XOR/carry encoding
\[
a+b+c+1=0,\qquad ab+ac+bc=0.
\tag{IIIa}
\]
A degree-bounded substitution of edge-slack variables transforms exact-one refutations into graph-colouring refutations, yielding
\[
\deg_{\mathrm{PC}}(\text{positive exact-one XOR/carry})
\ge\tfrac12\deg_{\mathrm{PC}}(\text{3-colouring axioms}).
\tag{IIIb}
\]
This establishes hardness in the stated proof system, not for unrestricted Boolean algorithms.

**Conditional separation theorem.** Fix \(N=2^m\), a time-constructible \(s(m)\ge m\), and \(A\in PH\). For every exact staged Boolean realisation \(\mathcal C_m\) of total \(\mathrm{Search\mbox{-}MCSP}^{A}[s]\), let \(S(\mathcal C_m)\) be its persistent state size and
\[
\Gamma(\mathcal C_m)=
\sum_{t=0}^{N-1}\mathrm{CC}(F_t)+\mathrm{CC}(D)
\tag{IVa}
\]
the *complete* update and final-decoder gate cost. The proved implication is
\[
\boxed{
\begin{gathered}
\exists s,\ A\in PH\quad\forall c,d\in\mathbb N\quad
\exists m_0\quad\forall m\ge m_0:\\
\neg\exists\mathcal C_m:
\bigl(S(\mathcal C_m)\le s(m)^c
\ \land\ \Gamma(\mathcal C_m)\le2^m s(m)^d\bigr)\\
\Longrightarrow\quad P\ne NP.
\end{gathered}}
\tag{IVb}
\]
The **deduction** (IVb) is proved by machine-to-circuit simulation, exact staged unrolling and the published streaming transfer of McKay–Murray–Williams; its derivation is given in Theorem 0.2. The **universal hardness premise on the left** is not proved.

**Additional transfer required for a Hall-based proof of the premise.** To obtain the antecedent of (IVb) by the universal embedding, one would need to construct, for every admissible *nonlinear* computation, a graph-indexed linear space and spanning family \(B_{\mathcal C_m}\) satisfying the Hall hypotheses together with a strong bound
\[
d_m(\operatorname{tw}(G_{m,s})+1)-1
\le\operatorname{tw}(H_{B_{\mathcal C_m}})
\le F(m,s,S,\Gamma)
\tag{V}
\]
that contradicts the polynomial-resource regime for the required quantifiers. The first inequality is a proven Hall consequence **once the new representation and its hypotheses are supplied**. The representation map and adequate second inequality have not been established. High width alone is insufficient, as the established \(K_n\) and \(K_{n,n}\) controls demonstrate.

---
## 0. Proven transfers and the quantified separation theorem

### 0.1 Central claim and source status

PNP-001 does **not** lack transfer theorems. The programme has already developed mathematical reductions and transfers between exact-one satisfiability, algebraic degree, support-overlap representations, restricted proof systems, and computational circuit models. Published conditional transfers from MCSP to complexity-class separations are also available.

The strongest *currently selected* proof route has been sharpened by the research director to

\[
\boxed{
\text{Streaming algorithm}
\xrightarrow{\mathrm{the machine-to-circuit simulation}}
\text{small update circuits}
\xrightarrow{\mathrm{the unrolling construction}}
\text{online state-cut circuit}
\xrightarrow{\mathrm{L^*\ (OPEN)}}
\text{streaming lower bound}
\xrightarrow{\mathrm{MMW,\ Thm.\ 1.3}}
P\ne NP.
}
\tag{A}
\]

The source and status of these implications must be separated. The MMW endpoint is a **published theorem**. the unrolling construction is **recorded as having survived an independent review** in the associated transfer question. the machine-to-circuit simulation is recorded as **CLAIMED** in the available archived proofstate; an additional other-model-family review was reported by the research director but the review transcript is not in the checked snapshot. L* has **not** been proved.

This yields a genuine **conditional proof of the separation from L***, not a proof of L* and not an unconditional proof of \(P\ne NP\).

### 0.2 The exact computational model

Let \(m\ge1\), \(N=2^m\), and let \(s=s(m)\ge m\) be time constructible. Let \(A\in PH\). Work with the precise **total search relation** Search-MCSP with \(A\)-oracle gates permitted in the *output circuit*, as defined in McKay–Murray–Williams, STOC 2019, Theorem 1.3. The streaming solver itself does **not** get free \(A\)-oracle access.

An exact staged Boolean realisation has a state of \(S\) bits, an initial state \(q_0\), time-dependent update circuits

\[
F_t:\{0,1\}^S\times\{0,1\}\longrightarrow\{0,1\}^S,
\qquad t=0,\ldots,N-1,
\]

and a readout \(D\) implementing the required total search relation, satisfying

\[
q_{t+1}=F_t(q_t,x_{t+1}).
\tag{B}
\]

States may be nonlinear, redundant or time dependent. Circuits may share arbitrary intermediate gates internally. Computation cannot be made free by moving it to the final decoder; its gates are also charged. Denote the Boolean gate count for a fixed complete fan-in-two basis by \(\mathrm{CC}\), and write

\[
G(\mathcal C)=\sum_{t=0}^{N-1}\mathrm{CC}(F_t)+\mathrm{CC}(D).
\tag{C}
\]

The **online state-cut width** is the number \(S\) of persistent state wires crossing each *input-time boundary*. It is not the usual maximum width of every internal circuit layer. A lower bound for a single canonical witness-selection rule is insufficient: the class here includes **every valid output** of the total search relation.

### 0.3 the unrolling construction: the reviewed unrolling theorem

**Proposition 0.1 (the unrolling construction; the associated transfer question, step the unrolling lemma; SURVIVED_REVIEW).** Every correct exact staged realisation as in (B) induces a Boolean DAG computing the same total search relation, using at most \(G(\mathcal C)\) gates and at most \(S\) persistent wires between consecutive input stages.

*Proof.* Connect the \(S\) state outputs of stage \(t\) to the corresponding state inputs of stage \(t+1\). Inductively, the wires at each boundary carry the correct state after the given prefix. Connect the final state to the output circuit \(D\). The resulting circuit has at most the sum of the gate counts of its components, and only the persistent \(S\)-bit state crosses the boundary between input stages. No linearity assumption is used. \(\square\)

This theorem already provides **representation completeness for the online Boolean circuit model**, covering nonlinear encodings, redundancy, fan-out and delayed work. The independent review in the independent review records an important directional qualification: a general circuit lower bound transfers to the unrolled model, but a restricted online-width lower bound does not become a general circuit lower bound merely by unrolling.

**the algorithm-inclusion statement (archived status: CLAIMED)** further states that every correct one-pass algorithm is admissible in the generalised state/update minimisation; the older one-code-per-class variant was more restrictive.

**the machine-to-circuit simulation (archived status: CLAIMED)** converts a uniform deterministic \(S\)-space, \(U\)-worst-case-update-time machine to stage circuits of size \(O(US)\) in its specified tableau convention. The argument needed below only requires a fixed polynomial in \(S,U,m\), including the output stage. The precise \(O(US)\) estimate is model dependent and is not separately certified by the cited Lean files.

### 0.4 The sufficient online-circuit hardness premise

**Hypothesis L* (OPEN).** There exist a time-constructible \(s(m)\ge m\) and an oracle \(A\in PH\) such that for **every** fixed pair of nonnegative integers \(c,d\), for all sufficiently large \(m\), no exact online Boolean-circuit realisation of total Search-MCSP with the parameters above can simultaneously have

\[
S\le s(m)^c
\quad\text{and}\quad
G(\mathcal C)\le N\,s(m)^d.
\tag{L*}
\]

Multiplicative constants may be absorbed by increasing exponents for the asymptotic statement. Because the staged circuits can be selected nonuniformly for each input length, this version of L* is **stronger than necessary** for excluding ordinary uniform streaming algorithms. In particular, failing to prove the strong L* does not show that the weaker uniform-only statement is false.

The short phrase “more than \(N\operatorname{poly}(s)\) gates” must always be interpreted with these **explicit polynomial-exponent quantifiers**.

### 0.5 Theorem 0.2: the proved conditional implication to \(P\ne NP\)

For \(N=2^m\), time-constructible \(s(m)\ge m\), and \(A\in PH\), let \(\mathcal C_m\) range over **all** exact deterministic staged Boolean realisations of the total \(\mathrm{Search\mbox{-}MCSP}^{A}[s]\) relation. Each has \(S(\mathcal C_m)\) persistent state bits, exact update circuits \(F_t\), and a charged final decoder \(D\), with
\[
\Gamma(\mathcal C_m)=
\sum_{t=0}^{N-1}\operatorname{CC}(F_t)+\operatorname{CC}(D).
\tag{T0}
\]

**Theorem 0.2 (conditional separation).** If for some \(s,A\)
\[
\forall c,d\in\mathbb N\ \exists m_0\ \forall m\ge m_0:
\neg\exists\mathcal C_m:
\bigl[S(\mathcal C_m)\le s(m)^c\land
\Gamma(\mathcal C_m)\le2^m s(m)^d\bigr],
\tag{T1}
\]
then
\[
\boxed{P\ne NP.}
\tag{T2}
\]

*Proof.* Suppose \(P=NP\). The construction behind McKay–Murray–Williams (2019), Theorem 1.3, supplies an ordinary deterministic uniform one-pass algorithm for the total search problem, with persistent workspace \(S_{\rm alg}\le s(m)^{O(1)}\) and worst-case per-symbol update time \(U_{\rm alg}\le s(m)^{O(1)}\). The oracle \(A\) is allowed in the **witness circuit being sought**; it is not provided as unit-cost oracle access to the ordinary streaming algorithm.

For a fixed deterministic machine, a bounded \(U_{\rm alg}\)-step update of a configuration represented with \(S_{\rm alg}\) bits can be simulated by a fan-in-two Boolean circuit of size \(\operatorname{poly}(S_{\rm alg},U_{\rm alg},m)\). Include the full final output procedure in \(D\). Connecting these stage circuits yields an exact realisation of the same total search relation, with arbitrary nonlinear state representation and sharing inside stages accounted for by the charged circuits. Since \(s(m)\ge m\), for suitable fixed integers \(c,d\) and all sufficiently large \(m\),
\[
S(\mathcal C_m)\le s(m)^c,\qquad
\Gamma(\mathcal C_m)\le2^m s(m)^d.
\tag{T3}
\]
This contradicts (T1). Thus \(P\ne NP\). \(\square\)

The implication **(T1)\(\Rightarrow\)(T2) is proved**. The antecedent (T1) is an unproved lower bound for *all* admissible online realisations, and does not follow merely from the completed linear Hall embedding.

### 0.6 The precise role of the universal Hall theorem

Theorem 4.1 of *Every Basis Sees the Blow-Up* establishes, for a **linear space** satisfying the rank, local-intersection and edge-intersection properties (R), (L), (E), that every spanning family \(B\) has

\[
G[K_d]\subseteq H_B,
\qquad
\operatorname{tw}(H_B)\ge d(\operatorname{tw}(G)+1)-1.
\tag{D}
\]

The online circuit supplied by the unrolling construction is an arbitrary **nonlinear Boolean DAG**, not a spanning family of that linear space. Consequently there is no established inference from the unrolling construction's width \(S\) to a small basis-overlap treewidth.

To derive L* by the embedding route, the project must prove a **new** mathematically quantified construction that maps *every* admissible small online Search-MCSP circuit to an appropriate graph-indexed linear space \(K_{m,s}\) and spanning family \(B_\mathcal C\), with (R), (L), (E), and

\[
d(\operatorname{tw}(G_{m,s})+1)-1
\le \operatorname{tw}(H_{B_\mathcal C})
\le F(m,s,S,G(\mathcal C)).
\tag{E}
\]

The right inequality must be strong enough, for an infinite family and **all** relevant exponents, to contradict the polynomial-resource regime. It must account for actual computation and withstand nonlinear recoding, DAG sharing, output deferral and the MMW oracle construction.

This is the research question **the associated transfer question**. The embedding theorem is **an established structural ingredient**, but **Embedding ⇒ L*** is open. It is the principal missing arrow **in this chosen Hall-embedding strategy**, not a necessary intermediate theorem for all possible methods of proving \(P\ne NP\).

The \(K_n\) example in Proposition 6.5 is decisive against any width-only argument: minimum overlap treewidth is \(2n-1\), but a fixed \(K_4\) subformula gives constant-size Resolution refutations. The easy bipartite family \(K_{n,n}\) is another control. A successful new theorem must use a property of the exact Search-MCSP relation that these easy families do not have.

### 0.7 A transfer-theorem atlas

| Transfer | Input | Proved or recorded conclusion | Status and scope |
|---|---|---|---|
| v0.24, Thm 4 | Positive one-in-three SAT and GF(3) | Satisfiability iff a two-value affine solution exists | PAPER PROOF; Lean reported, no algorithmic LB |
| v0.24, Thm 44 | Colouring reduction with specified PC axioms | Degree-preserving substitution; restricted degree/size LB | PAPER PROOF; not arbitrary algorithms |
| v4, Thm 4.1 and Thm 5.4 | Spanning families of the colouring kernel over any field | Universal support-overlap embedding \(G[K_2]\subseteq H_B\) | PAPER PROOF; general-field subgraph claim not in existing Lean |
| v4, Cor 6.2 | Bases of the same kernel | Exact optimized width \(2\mathrm{tw}(G)+1\) | PAPER PROOF; GF(3) width formalisation reported |
| Theorems 12 and 14 | Specified roABP-IPS variants | Exponential width/size lower bounds in restricted proof systems | Local proof and review record; model dependent |
| K6 boundary signatures | Perfect-matching exact-one encoding | Cut communication rank expressed through realizable complementary signatures | Elementary derivation; all-vtree lower bound OPEN |
| the algorithm-inclusion statement | Correct one-pass algorithms | Admission into general state/update minimisation | CLAIMED in archived state |
| the machine-to-circuit simulation | Uniform streaming computation | Polynomial-size staged update circuits | CLAIMED in archived state; later review reported |
| the unrolling construction | Exact nonlinear staged online circuits | Unrolled Boolean DAG with state-cut width \(\le S\) | SURVIVED_REVIEW in the associated transfer question |
| **L*** | Exact total Search-MCSP online circuits | No simultaneous \(S=\mathrm{poly}(s)\), \(G=N\mathrm{poly}(s)\) | **OPEN; sufficient hardness hypothesis** |
| **MMW Theorem 1.3** | Exact Search-MCSP streaming lower bound, specified \(A,s\) | \(P\ne NP\) | **PUBLISHED 2019** |
| Chen–Jin–Williams + Theorem R | Fixed-threshold MCSP formula LB and MCSP-specific conversion | Conditional \(NP\not\subseteq P/poly\) | External formula LB PUBLISHED; R-MCSP OPEN |
| Chen–Jin–Santhanam–Williams | Suitable uniform constructive refuters | Complexity-class separations | PUBLISHED conditional transfer; refuter premise OPEN |

This atlas prevents a second misconception: **Theorem R and the constructive-refuter route are not proved to factor through L***. The organisation's union question **the associated transfer question** is an attempt to connect the routes; the common mathematical factorisation has not yet been established.

### 0.10 Three decisive constraints on the QE* route

The 22 November cross-review identifies three logically separate obstructions. They do not erase the transfer theorems that PNP-001 already possesses. They identify the precise additional premise needed to connect those theorems to an unconditional separation.

**Constraint I: State counting does not lower-bound update work (the small-space construction / the general update-cost lower bound).** Let \(N=2^m\), let \(\mathrm{Circ}_{m,s}\) be the finite set of permitted size-at-most-\(s\) circuits under a fixed description convention, and let \(\mathrm{Im}_{m,s}\) be their output truth tables. Standard description counting gives

\[
|\mathrm{Im}_{m,s}|\le|\mathrm{Circ}_{m,s}|
   =2^{O(s\log(m+s))}.
\tag{F1}
\]

At each prefix length, there are at most \(|\mathrm{Im}_{m,s}|\) live prefixes, plus one dead state. Thus counting alone cannot force more than \(O(s\log(m+s))\) **abstract** state bits, even if it says nothing about the cost of transitioning between state names.

For the **total search problem**, the small-workspace mechanism can also be described constructively. Maintain a size-\(\le s\) circuit \(C\) that agrees with every previously read input bit, the index \(t\), and a dead-state flag. If the next bit \(b=C(t)\), keep \(C\). On a mismatch, enumerate candidate circuits \(C'\) and require

\[
\bigl(\forall j<t,\ C'(j)=C(j)\bigr)\ \land\ C'(t)=b.
\tag{F2}
\]

If a candidate exists, store one; otherwise enter the dead state permanently. The induction works because the current \(C\) *encodes the observed prefix*: for every earlier position, its output agrees with the actual stream. No separate copy of that prefix is needed. At the end, the stored \(C\) is a correct witness or the dead state correctly reports that no circuit exists. **The enumeration may consume enormous time per input bit.** For ordinary bounded-fan-in circuit descriptions the stored circuits and evaluator have \(O(s\log(m+s))\)-type space bounds. If size-\(s\) circuits contain arbitrary \(A\in PH\) oracle gates, evaluation can require further polynomial workspace; the robust fully general uniform bound is \(\operatorname{poly}(s)\), pending an exact oracle-evaluation space audit.

Therefore a **pure-space** lower bound cannot refute the existence of every polynomial-workspace Search-MCSP streaming algorithm. The unproved general **update computation** lower bound the general update-cost lower bound is essential. The argument does not disprove lower bounds within special restricted affine-update models, nor does it grant a polynomial-time prefix-extension test. A decision-language residual quotient must not silently be assumed to supply a valid total-search witness.

**Constraint II: the unrolling construction is complete for online Boolean circuits, not for linear spanning families (the associated transfer question).** The reviewed the unrolling construction step (the associated transfer question, the unrolling lemma; the independent review review) chains the stage update circuits \(F_t\) and final decoder \(D\) into one Boolean DAG of size at most

\[
\sum_t\mathrm{CC}(F_t)+\mathrm{CC}(D),
\tag{F3}
\]

with at most \(S\) *persistent state wires across input-time boundaries*. This accommodates nonlinear, redundant and time-dependent state codes, ordinary DAG gate sharing, and deferred work charged to \(D\). It is **not** a bound on the conventional internal layer width of every stage.

Theorem 4.1 of *Every Basis Sees the Blow-Up* instead applies to **spanning families of a fixed coordinate-defined linear space** satisfying the precise projection-rank and support-intersection conditions (R), (L), (E). the unrolling construction supplies no map from general nonlinear online circuits to such families. The missing proposed theorem is therefore

\[
\forall \mathcal C\in\mathsf{ExactOnlineSearchMCSP}:
\quad \mathcal C\mapsto(K_{m,s},G_{m,s},B_{\mathcal C}),
\quad
\operatorname{tw}(H_{B_{\mathcal C}})
  \le F(m,s,S,G(\mathcal C)),
\tag{F4}
\]

with verified Search-MCSP semantics, (R), (L), (E), and a bound \(F\) strong enough to contradict the Hall lower bound under all relevant polynomial resource exponents. Neither a generic gate-dependency graph nor a hand-selected inconvenient representation automatically qualifies as \(H_B\). A fast function can be implemented with redundant high-width wiring; the desired conclusion concerns the suitable representation **forced by every admissible fast implementation**.

**Constraint III: Large overlap treewidth alone is not computation hardness (Propositions 6.5 and 10.2).** For \(G=K_n\), \(n\ge4\), the minimum basis-overlap treewidth is \(2n-1\), yet the unsatisfiable colouring formula contains a fixed \(K_4\) contradiction and consequently admits a constant-size Resolution refutation. For \(G=K_{n,n}\), \(\operatorname{tw}(G)=n\) and the minimum basis-overlap width is \(2n+1\), although the graph is plainly 3-colourable. Neither example refutes the Hall embedding. Both defeat the shortcut “unavoidable width implies slow general computation.”

A valid new bridge must exploit a mathematically established **Search-MCSP-specific property** not shared by those easy controls. It must also satisfy the the oracle-sensitive condition oracle test: McKay–Murray–Williams construct a fast streaming solver when allowed an additional \(\Sigma_3\mathrm{SAT}^{A}\) oracle. An argument that also forbids this algorithm when those queries cost one unit is invalid. The precise nonrelativising premise must be identified, not asserted by name.

### 0.11 The mathematical implication chain

The standard deterministic machine-to-circuit simulation and exact unrolling yield
\[
S,U=s^{O(1)}
\Longrightarrow
S(\mathcal C_m)=s^{O(1)},\quad\Gamma(\mathcal C_m)\le2^m s^{O(1)}.
\tag{F5a}
\]
Together with the published MMW theorem:
\[
\boxed{
\text{universal online-circuit lower bound (T1)}
\Longrightarrow
\text{streaming lower-bound premise}
\Longrightarrow P\ne NP.
}
\tag{F5}
\]
The implication is proved; (T1) itself is not. The separate Hall-based route would need the unproved quantitative cross-model representation transfer (V).

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

It additionally integrates the PNP-001 repository results and contracts of 19–22 November: Theorems 12, 14 and 16 for restricted algebraic proof systems; R-MCSP; QE* and proof state the associated transfer question; Perfect Matching K6; the K8/K9 bridge maps; Range Avoidance and constructive refuters; the P1 algorithmic-method work; and the cross-theorem synthesis plan.

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

## 6. Streaming Search-MCSP: precise computational lower bounds

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

At each prefix length \(t\), the number of nonempty residual languages \(\{q:pq\in\mathcal I_{m,s}\}\) is at most \(|\mathcal I_{m,s}|\), plus a dead residual. Hence the abstract live-prefix state encoding has size \(O(s\log(m+s))\) bits **if transition computation is free**. Section 0.10 additionally supplies a constructive small-workspace witness-replacement algorithm for total search, with potentially enormous update computation and explicit qualification for (A\in PH\) oracle evaluation.

This is a serious obstruction to pure state-count, Myhill–Nerode and one-way communication arguments. Such methods do not prove the required worst-case update-time lower bound. The project labels this observation the small-space construction in the QE* proof state.

### 6.3 QE* and the open the general update-cost lower bound/the oracle-sensitive condition obligations

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

- **the general update-cost lower bound:** a representation-independent lower bound on worst-case update computation for the entire admissible class;
- **the oracle-sensitive condition:** a nonrelativising property that distinguishes ordinary computation from known efficient oracle-assisted constructions.

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

The project question **the associated transfer question** is intended to address this bridge. Sections 0.10–0.11 reconcile the genuine the machine-to-circuit simulation/the unrolling construction circuit transfers with the still-unproved online-circuit-to-Hall-space implication and the Search-MCSP-specific negative controls. The identifier comes from the newer director report, not independently checked in the older GitHub snapshot.

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
| Streaming QE* | MMW resource-bounded compression | General worst-case update lower bound with exact oracle and representation hypotheses | \(P\ne NP\) | OPEN the general update-cost lower bound/the oracle-sensitive condition |
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

This is the subject of the proposed organisation-level *union theorem* **the associated transfer question**. The identifier is reported by the ongoing research discussion and was not yet present in the older GitHub snapshots inspected during preparation.

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

This is the exact role of the associated transfer question. A proof that the four fronts truly share one reducible obligation would be a new theorem. Merely drawing arrows between their names is not.

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

Proposed union the associated transfer question: factorisation of the separate open bridges [OPEN].
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

## 12. Further mathematical transfer implications

### 12.1 Why a single-gap account is insufficient

The proofbook and the owner-approved K8/K9 bridge map contain more routes than the initial four-front grouping reveals. In particular, *an unrestricted nonlinear streaming lower bound* is only one of several hypotheses which would imply a complexity separation. Other hypotheses involve a **one-tape deterministic time bound**, a **general Boolean circuit lower bound**, a **constructive Kolmogorov-complexity boundary**, special **Extended Frege** lower bounds, or a formula/circuit simulation. These involve different input distributions, machine models and quantifier orders.

The review of the 21 November P2 dossier, K8/K9 contracts, Grand Strategy, T47 non-stream memo, LIT-10/LIT-11 and the 22 November archived proofstates supports the following expanded classification. This is an evidence-based **research map**, not a claim that the missing hypotheses have been proved.

### 12.2 Route O: a one-tape MCSP time lower bound — direct conditional P versus NP separation

Cheraghchi, Hirahara, Myrisiotis and Yoshida, *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP* (STACS 2021; [official proceedings](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.STACS.2021.23)), identify a direct threshold inherited from McKay–Murray–Williams. For a certain sufficiently small **fixed** \(\mu_1>0\),

\[
\mathrm{MCSP}[2^{\mu_1 m}]\notin
\mathrm{DTIME}_1[N^{1.01}]
\quad\Longrightarrow\quad
P\ne NP,\qquad N=2^m.
\tag{O1}
\]

Here \(\mathrm{DTIME}_1\) is specifically a Turing machine with a **one-way read-only input tape and one two-way read/write work tape**. It is neither an arbitrary multi-tape time class nor the state-limited streaming model of Section 6. The paper proves substantial randomized one-tape lower bounds at a **different** size threshold \(\mu_2>\mu_1\); this mismatch prevents treating the already known \(N^{1.99}\) bound as a solution of (O1).

The owner dossier assigns this line to **the associated transfer question**. Its current proofstate records an unresolved local PRG argument; experimental adversaries against an unsourced cut-guessing cost model do not establish a genuine one-tape lower bound. This route **does not require Candidate A**. It may be attacked through one-tape geometry, branching-program decompositions, pseudorandomness and time lower bounds directly. Its oracle stress test concerns permitted query lengths and the local oracle simulation documented in the published paper.

**Audit status:** (O1) is a published conditional implication; the required deterministic time lower bound at the **small** \(\mu_1\) remains OPEN.

### 12.3 Route K: P-uniform hardness magnification for Hamming-promise MCSP

The **K3** milestone in the owner-approved P2 dossier refers to Atserias–Müller's *Simple General Magnification of Circuit Lower Bounds* (arXiv:2503.24061, 2025). K3 is the proposed lower bound for the **Hamming-distance promise** problem \(N^{-\varepsilon}\)-MCSP with the exact paper's parameters.

The YES instances are truth tables of functions admitting circuits below the prescribed threshold; the NO instances are truth tables at a specified Hamming distance from **every** such YES table; intermediate strings are outside the promise. This is **not** the same problem as exact MCSP, two-threshold Gap-MCSP or total Search-MCSP.

The project's P2 K-REV expressly supersedes its earlier K1/K2 formulation. It records the target as

\[
N^{-\varepsilon}\text{-}\mathrm{MCSP}[\sigma]\notin
P\text{-uniform-}\mathrm{SIZE}
   [N^{1+\varepsilon+o(1)}]
\tag{K3}
\]

for the appropriate circuit-size threshold \(\sigma\) and exact assumptions of the cited uniform magnification theorem. Under those published conditions the resulting conclusion is of the form

\[
P\ne NP^{\oplus P}
\tag{K4}
\]

with the actual source theorem determining the oracle-class notation and uniformity details. **This conclusion does not, by itself, imply \(P\ne NP\).** The proposed second step K4—from that uniform separation to \(P\ne NP\)—is an additional OPEN question.

The repo also records a **claimed** near-linear lower-bound lemma K-L for a restricted representation and an explicit same-family proof correction. Such a linear result is below the required \(N^{1+\varepsilon}\)-type threshold and does not close K3. The P2 dossier explicitly warns that a lower bound against LOGTIME-uniform circuits is weaker than one against the full P-uniform class; the direction of class inclusion may not be reversed.

**Audit status:** K3 OPEN, K4 OPEN. The cited Atserias–Müller transfer is an existing published, **weaker-conclusion** route. K3 must remain distinct from ECCC Report 313.

### 12.4 Route PIT-313: low-degree identity testing and disjunctive lower bounds

**ECCC TR26-313** is Nikolai Chukhin, Karthik Gajulapalli, Alexander Golovnev and Ivan Mihajlin, *A Little Derandomization Goes a Long Way: Unconditional Circuit Lower Bounds using Low-Degree PIT* (5 November 2026; [ECCC](https://eccc.weizmann.ac.il/report/2026/313/); [arXiv:2611.07972](https://arxiv.org/abs/2611.07972)). This **is not** the K3 milestone above. They are related at the broad level of lower-bound research, not by an established theorem identifying their hypotheses.

TR26-313 proves unconditionally a disjunction:

\[
\text{NE has a function with almost-maximal Boolean circuit hardness}
\quad\lor\quad
VP_{\mathbb Z}^{0}\ne VNP_{\mathbb Z}^{0}.
\tag{PIT1}
\]

The Boolean alternative is a lower bound for a language in NE. **No transfer from this particular NE conclusion to a superpolynomial general-circuit lower bound for a language in NP is established in the inspected PNP-001 proofbook.** Such a transfer must not be inferred from padding without checking its quantifiers and resource loss. The arithmetic alternative is a constant-free algebraic separation, not the statement \(P\ne NP\). A proof of (PIT1) is not a proof of either disjunct separately.

The repository's K9 and THR-SAT documents propose the stronger new objective of shaving a fixed positive exponent from deterministic PIT for **general size-\(s\) circuits computing degree-\(d\) polynomials in \(t\) variables**, beyond the existing \(O(s t^{d-1})\) finite-field bound:

\[
T_{\rm PIT}(s,t,d)\le O(s t^{d-1-\varepsilon})
\tag{PIT2}
\]

under the exact source hypotheses. A test that works only on the GF(3) colouring kernel, positive one-in-three clause polynomials, sparse monomials or a small fixed degree is insufficient unless a quantitative simulation into the general model is supplied.

The corresponding proofstate **the associated transfer question** already has an elementary multilinear evaluation lemma using all Boolean inputs of weight at most \(d\), with

\[
\sum_{i=0}^{d}\binom{t}{i}
\]

evaluation points. A dimension argument shows that this many points are necessary if one seeks a universal hitting set for the **entire** vector space of all multilinear degree-at-most-\(d\) polynomials. This does not rule out a smaller hitting set for a restricted **small-circuit** class, because its members need not span the full space. The proofstate explicitly records that the general-subclass exponent gain remains OPEN. The range-avoidance proofstate the associated transfer question gives an algebraic annihilator and a witness outside a generator's range by linear algebra, but its claimed running time is of essentially brute-force order; it is not a uniform efficient refuter.

**Audit status:** the published disjunction (PIT1) is established externally; the exponent-improving hypothesis (PIT2) is OPEN for the required general model. Neither K3 nor PIT-313 should be called an unconditional proof of \(P\ne NP\).

### 12.5 Route KOL: Kolmogorov boundary hardness and one-way functions

Liu–Pass, *One-Way Functions and Boundary Hardness of Randomized Time-Bounded Kolmogorov Complexity* (ITCS 2026; [official proceedings](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2026.97)), give a characterization of one-way functions by the hardness of a **specific boundary promise problem** for randomized time-bounded Kolmogorov complexity.

With the paper's exact notions, a sufficient chain is

\[
\mathrm{boundary\text{-}MINrK}^{poly}
   \notin ioBPP
\ \Longleftrightarrow\
\text{one-way functions exist}
\ \Longrightarrow\
P\ne NP.
\tag{KOL1}
\]

The full boundary definitions, promise, randomized complexity and infinitely-often quantifiers cannot be dropped. PNP-001 assigns this line to **the associated transfer question**. Its proofstate contains a survived-review argument about the promise predicates under \(P=NP\) and a separate **claimed** monotonicity lemma for different boundary widths; neither proves the required hardness premise.

An important directional correction already present in the P2 dossier is retained: **\(P\ne NP\) is not known to imply one-way functions**. Thus the cryptographic hardness premise is a sufficient condition for separation, not a characterization of \(P\ne NP\). This line is independent of Hall overlap-width.

### 12.6 Route EF: bounded arithmetic, witnessing tautologies and proof-system strength

Pich–Santhanam, *Towards P ≠ NP from Extended Frege Lower Bounds* ([ECCC TR23-199](https://eccc.weizmann.ac.il/report/2023/199/)), prove conditional transfers from lower bounds for **specially augmented Extended Frege systems** and their witnessing circuit-lower-bound tautologies to strong Boolean circuit lower bounds. The premise is not “some formula is hard for a weak proof system.”

The PNP-001 K8/K9 files distinguish the specific EF-plus-\(w_n^k(f)\)-axiom setting from the current Theorem 12 roABP-IPS and Polynomial-Calculus results. Transforming a lower bound from these restricted systems into the augmented Extended Frege system would require a new and quantitative proof-system simulation. No such transfer is established in the inspected repository.

The **Weak Rank Principle** / PCR track provides further proof-complexity targets for circuit-lower-bound statements, again with an unproved jump to Extended Frege. The relevant invariant is proof-system-specific; the obstacle is not interchangeable with the streaming state encoding of QE*.

**Audit status:** published conditional EF route; required strong proof-system lower bound and simulation from PNP-001's restricted systems OPEN.

### 12.7 Route DAG: direct general circuit lower bounds for MCSP

The owner-approved P2 dossier states a particularly direct target, **the associated transfer question**, which does not require one-pass streaming or a Hall linear-space embedding. Fix a circuit basis \(B_2\), \(N=2^m\), and some fixed \(c\ge1\). A sufficient lower-bound statement has quantifiers

\[
\exists c\ge1\quad
\forall k\ge1\quad
\forall m_0\quad
\exists m\ge m_0:
\quad
\mathrm{CC}_{B_2}(\mathrm{MCSP}[m^c])
   > N m^k.
\tag{DAG1}
\]

Given the published MMW circuit consequence with the same exact threshold and model conventions, (DAG1) implies \(NP\not\subseteq P/poly\), and therefore \(P\ne NP\). The fixed threshold exponent \(c\) and **unbounded quantification over the lower-bound exponent \(k\)** are essential.

The proofstate the associated transfer question now contains 176 archived events. Its last entries explicitly state that G0001/G0002 remain OPEN. A “drop two gates per restriction” elimination step is verified only in small examples around \(m=3\); for \(m\ge4\) no suitable restriction-stable argument has been established. The owner dossier already supplies two instructive no-go controls:

- MCSP is identically zero on a large subcube, so naïve disperser-based gate elimination does not apply directly.
- A fully symmetric sparse function depending on all \(N\) bits can nevertheless have \(O(N)\)-size circuits. Sparsity, symmetry and dependence on every input bit are not sufficient for (DAG1).

This is **an additional direct-to-separation route**, not just a restatement of L*: it targets arbitrary fan-in-two Boolean DAGs with unrestricted sharing.

### 12.8 Route RAND: avoiding streaming — computation graphs, random access and formulas

The **T47** memo, *Escalating Graph vs Computation Graph: What If It Is Not a Stream?* (21 November), explicitly considers four computation shapes: one-pass streaming; event-driven escalating graphs; random-access time-space machines; and general Boolean DAGs.

A proposed equivalence between a suitably restricted escalating graph and a stream is marked a **director inference**, not a verified general theorem. For random-access computation, a separate Chen–Jin–Williams lower-bound transfer applies under its own time, space and advice parameters. General DAG lower bounds are stronger requirements and do not inherit online state-cut width automatically.

The most important lesson is that the alternatives do not share the same *quantified resource*. A small streaming-state interface does not characterize a random-access RAM, and one-cut communication lower bounds do not automatically sum over a shared DAG. The T47 document identifies a missing cumulative-cut accounting lemma, not a proven bridge.

**Audit status:** alternative model comparisons and specific published transfers exist; the new cross-model reductions remain OPEN.

### 12.9 Route ALG: threshold circuit analysis and exact theorem-matched CAPP

The P1 route has a genuine, source-checked published algorithm-to-lower-bound implication: for every fixed \(\alpha>1\), a suitably accurate nontrivial \(2^n/n^{\omega(1)}\)-time acceptance-probability algorithm for \(O(n^\alpha)\)-size \(\mathrm{XOR}_2\circ\mathrm{THR}\circ\mathrm{THR}\) circuits gives corresponding lower bounds against \(n^\alpha\)-size \(\mathrm{THR}\circ\mathrm{THR}\) circuits in \(E^{NP}\). The project cites Chen–Tal–Wang Lemma 3.8, Bathie–Williams (2024), and Chen–Williams (2019).

Unlike an ordinary runtime experiment, a transfer-qualifying algorithm must handle the *correct combined circuit class, all relevant sizes and the stated approximation error*. The repo explicitly tests THR-SAT, MAJ-of-MAJ CAPP, PRGs for XOR-of-two threshold circuits, and certified low-rank residual compression in separate proofstates.

A lower bound for \(E^{NP}\) against one fixed restricted circuit class is **not** \(P\ne NP\). Nevertheless it is an independent mathematical output worth reporting and may inform the Boolean lower-bound tools used in the direct MCSP lines.

### 12.10 Route VERIFY: exact finite synthesis, polynomial identities and hitting sets

Several project results are most appropriately classified as **verification technology**, not yet complexity-class transfers. These include the PhysalisMe exact SAT/UNSAT encoding of state updates, Hall-lemma finite checks, bit-level Polynomial Calculus certificate verification, low-degree identity testing, generator-image annihilators, and the candidate use of hitting sets for any-order read-once algebraic branching programs.

They are important because a mathematically proposed “unavoidable work” invariant should first be attacked with small counterexamples. A satisfiable finite SAT encoding must be host-replayed to validate the decoded algorithm. An unsatisfiable encoding must range over **all** relevant state recodings before it becomes an invariant for its specified finite domain. A same-family AI rewrite is not independent corroboration. In no case can finite tests substitute for the universal asymptotic lower bound required by L*, (O1), (DAG1), or an independent formula-based transfer.

### 12.11 What the research frontier now looks like

| Research route | Smallest sufficient missing statement documented in PNP-001 | Published endpoint if met | Latest checked status |
|---|---|---|---|
| QE* / L* | General representation-independent, oracle-sensitive online update-work hardness | \(P\ne NP\), MMW19 Thm 1.3 | OPEN |
| O: one-tape | Deterministic one-tape \(\mathrm{MCSP}[2^{\mu_1 m}]\) lower bound beyond \(N^{1.01}\), with correct small \(\mu_1\) | \(P\ne NP\), CHMY21 | OPEN |
| DAG: direct general MCSP | Fixed \(c\), all \(k\), infinitely many \(m\): \(\mathrm{CC}(\mathrm{MCSP}[m^c])>Nm^k\) | \(NP\not\subseteq P/poly\), MMW19 | OPEN |
| R-MCSP | Subquadratic exponent in the MCSP-specific circuit-to-formula simulation | \(NP\not\subseteq P/poly\), CJW20 + MMW19 | OPEN |
| OPS Gap-MCSP | \(N^{1+\varepsilon}\) general-circuit LB, fixed \(\varepsilon\), **all sufficiently small** gap parameters | \(NP\not\subseteq P/poly\), OPS21 | OPEN |
| CJSW refuters | Exact uniformly efficient and correctly certified refuter | \(P\ne NP\), CJSW | OPEN |
| KOL | Boundary-MINrK randomized hardness with exact promise/ioBPP quantifiers | One-way functions, then \(P\ne NP\) | OPEN |
| EF | Specific augmented Extended Frege witnessing lower bound | SAT circuit separation via Pich–Santhanam | OPEN |
| K3 Hamming-promise | Exact P-uniform-size LB with target distance and thresholds | \(P\ne NP^{\oplus P}\), not automatically \(P\ne NP\) | OPEN |
| PIT-313 | General-circuit PIT exponent improvement | Strong **disjunctive** Boolean/arithmetic LB statement | OPEN; published weaker unconditional disjunction |
| ALG/THR | Transfer-qualifying improved CAPP for full target class | \(E^{NP}\) restricted-circuit lower bound | OPEN at stronger target sizes |

These rows are **not eleven equivalent statements**. A lower bound in a smaller class cannot be silently substituted for a lower bound in a larger class; a consequence in \(E^{NP}\) cannot be silently substituted for a lower bound for NP; and a uniform lower bound cannot be treated as a nonuniform lower bound without a simulation.

### 12.12 Existing graph-width controls and source bookkeeping

The complete-graph and complete-bipartite controls \(K_n\) and \(K_{n,n}\) are **pre-existing derived consequences** of the established formula

\[
\min_B\operatorname{tw}(H_B)=2\operatorname{tw}(G)+1.
\]

They are not new observations from this audit. They are retained in the earlier sections because they are essential mandatory falsification tests. For instance, with \(G=K_{3,3}\), \(\operatorname{tw}(G)=3\) and the optimized kernel overlap width is \(7\); this is a substitution into the existing theorem, not a new graph-family lower bound. The graph \(K_{3,3}\), the P2 milestone **K3** (P-uniform Hamming-promise MCSP), and literature report **TR26-313** (low-degree PIT) are separate objects. The earlier conversational shorthand is not evidence for equating them; the graph control is an immediate instance of the already proved structural bound.

### 12.13 Archival correction: number of research questions versus proofstate files

Commit **a1dea0e2c** corrects the earlier exporter message, which had described 182 research questions as though they were 182 separate proofstate files. The corrected README says the 182 count wrongly included **92 JSON proofstate files plus 90 lock files**. The subsequent 15:55 export contains **94 actual JSON proofstate files**, while the ledger has **2,248 research questions in total**, with status counts OPEN 1,424; PURSUED 552; ANSWERED 181; STOPPED 56; ESCALATED 18; RETRACTED 17. The five category totals sum to 2,248. These are administrative state categories, not counts of verified mathematical theorems.

The manuscript's earlier Section 0.12 records the **historical** 15:30 snapshot correctly as 92 JSON files, but its phrase “182 research questions” must be read with this 15:55 correction. Any evaluation of research progress should use the underlying individual proofstates and the complete proofbook, not the number of generated files or the number of assertions alone.

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

## Declarations

**Data availability.** Repositories and relevant branch paths are linked above. Some older drafts were supplied through the research conversations and are not necessarily included in the GitHub branch; the live VPS evidence may be newer than the public snapshot.

**Use of AI systems.** Multiple AI model families and code assistants contributed to discovery, calculations, counterexample search, independent criticism and drafting. Their participation is acknowledged as a research methodology; it does not constitute scientific acceptance.

**Novelty.** The status of some exact-one and embedding results relative to the full matroid, coding and graph-width literature remains subject to a complete priority search and external review. Published source results are not claimed as original PNP-001 theorems.

**Separation claim.** No unconditional proof of \(P=NP\) or \(P\ne NP\) is claimed.

*End of reconciled working synthesis, v0.25 — 22 November 2026.*
