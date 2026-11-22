# Algebraic Structure of Positive Exact-One Satisfiability and a Conditional Separation Theorem

**Björn Tonn**

*Mathematical manuscript · Revised version 0.25 · 22 November 2026*

## Abstract

We investigate positive exact-one satisfiability through affine linear algebra, graph-colouring kernels, and the cost of exact online computation. An exact criterion expresses Boolean satisfiability as the existence of a two-valued vector in an affine space over \(\mathbb F_3\). For the homogeneous kernel of a three-colouring encoding, we prove a universal support-overlap theorem: the overlap graph of **every finite spanning family**, over **every field**, contains the clique blow-up \(G[K_2]\). A canonical basis achieves equality, yielding
\[
\min_{B\text{ basis of }K_G(\mathbb F)}
\operatorname{tw}(H_B)=2\operatorname{tw}(G)+1
\]
and the analogous exact formula for pathwidth. The \(\mathbb F_3\) treewidth equivalence is separately represented by Lean 4 proof terms. We also give an algebraic refutation transfer and two exact simulations of a one-pass computation by Boolean circuits. In combination with a theorem of McKay, Murray and Williams, the latter yield a fully derived *conditional* implication to \(P\ne NP\). The antecedent is a universal quantitative lower bound on general online computation; it is not implied by the structural width identity without an additional representation-preserving theorem. The respective domains and quantifiers are made explicit, so that the established results can be assessed independently of this remaining implication.

## 1. The main results

Let \(n\ge3\), and put
\[
\mathcal T_n=\{\{i,j,k\}:1\le i<j<k\le n\}.
\]
Positive exact-one satisfiability is NP-complete [1]. For \(E\subseteq\mathcal T_n\), let
\[
F_E(x)=\bigwedge_{\{i,j,k\}\in E}
\bigl(x_i+x_j+x_k=1\bigr),
\qquad x\in\{0,1\}^{n}.
\tag{1}
\]
We write \(A_E\) for the clause-incidence matrix over \(\mathbb F_3\) and
\[
\mathcal A_E=\{z\in\mathbb F_3^n:A_Ez=\mathbf1\}.
\tag{2}
\]

**Theorem 1 (exact affine criterion).** For every \(E\subseteq\mathcal T_n\),
\[
\boxed{
F_E\text{ satisfiable}
\iff
\exists z\in\mathcal A_E:
\left|\{z_i:1\le i\le n\}\right|\le2.
}
\tag{3}
\]

For a finite nonempty simple graph \(G=(V,E_G)\) and a field \(\mathbb F\), the homogeneous kernel \(K_G(\mathbb F)\) of the standard exact-one encoding of graph three-colouring is defined in Section 3. For a finite indexed spanning family \(B=(b_j)_{j\in J}\) of a linear space, its support-overlap graph \(H_B\) joins \(j\ne k\) precisely when
\[
\operatorname{supp}(b_j)\cap\operatorname{supp}(b_k)\ne\varnothing.
\tag{4}
\]

**Theorem 2 (universal embedding and exact width).** For every field \(\mathbb F\), every finite nonempty simple graph \(G\), and every finite spanning family \(B\) of \(K_G(\mathbb F)\),
\[
\boxed{G[K_2]\hookrightarrow H_B.}
\tag{5}
\]
Here \(G[K_2]\) is the lexicographic product replacing each vertex of \(G\) by a two-vertex clique. Moreover,
\[
\boxed{
\begin{aligned}
\min_{B\text{ basis of }K_G(\mathbb F)}
\operatorname{tw}(H_B)&=2\operatorname{tw}(G)+1,\\
\min_{B\text{ basis of }K_G(\mathbb F)}
\operatorname{pw}(H_B)&=2\operatorname{pw}(G)+1.
\end{aligned}}
\tag{6}
\]
Theorem 2 has a direct mathematical proof in Sections 4–5. A Lean 4 development gives the corresponding two-sided treewidth equivalence over \(\mathbb F_3\), with its exact scope stated in Section 6.

A second result concerns a different mathematical object. Let \(N=2^m\), let \(s(m)\ge m\) be a time-constructible circuit-size bound in the parameter regime of [4], and let \(A\in PH\). An admissible staged Boolean realization \(\mathcal C_m\) of the *total* exact search relation \(\mathrm{SearchMCSP}^{A}[s]\) has \(S(\mathcal C_m)\) persistent state bits, Boolean update circuits \(U_t\), and a final exact decoder \(D\). Its charged gate cost is
\[
\Gamma(\mathcal C_m)=
\sum_{t=0}^{N-1}\operatorname{CC}(U_t)
+\operatorname{CC}(D).
\tag{7}
\]
The circuit-size measure allows arbitrary acyclic sharing and nonlinear gates of fan-in two.

**Theorem 3 (conditional separation).** Suppose there are an admissible \(s\) and \(A\in PH\) for which
\[
\boxed{
\begin{gathered}
\forall c,d\in\mathbb N\
\exists m_0\ \forall m\ge m_0:\\
\nexists\mathcal C_m\text{ admissible with}\\
S(\mathcal C_m)\le s(m)^c
\quad\land\quad
\Gamma(\mathcal C_m)\le 2^m s(m)^d .
\end{gathered}}
\tag{8}
\]
Then
\[
\boxed{P\ne NP.}
\tag{9}
\]
The implication from (8) to (9) is proved in Section 8. **The universal lower-bound assertion (8) is a hypothesis of that theorem**, not a consequence claimed here of (6). Moreover, (8) is *stronger than necessary*: the published streaming transfer requires a suitable lower bound only against uniform deterministic streaming algorithms, rather than an exclusion of all possibly nonuniform staged circuits. Section 8 gives the weaker quantified alternative and its exact relation to (8).

## 2. Proof of the affine criterion

Every clause contains exactly three positive variables. Consequently,
\[
A_E\mathbf1=\mathbf0
\quad\text{over }\mathbb F_3,
\qquad
z\in\mathcal A_E
\ \Rightarrow\ 
z+t\mathbf1\in\mathcal A_E
\quad(t\in\mathbb F_3).
\tag{10}
\]

*Proof of Theorem 1.* If \(x\in\{0,1\}^n\) satisfies \(F_E\), then \(A_Ex=\mathbf1\) in \(\mathbb F_3\); thus \(x\in\mathcal A_E\) has at most two coordinate values.

Conversely, suppose \(z\in\mathcal A_E\) has at most two coordinate values. If \(E=\varnothing\), there is nothing to prove. Otherwise \(z\) cannot be constant, since each clause would sum to \(3a=0\), not \(1\), in \(\mathbb F_3\). Hence the coordinates of \(z\) take exactly two distinct values. Each two-element subset of \(\mathbb F_3\) is a translate of \(\{0,1\}\). By (10), there exists \(t\in\mathbb F_3\) such that
\[
x=z+t\mathbf1\in\{0,1\}^{n},
\qquad
A_Ex=\mathbf1.
\]
For any clause the integer sum of three Boolean entries lies in \(\{0,1,2,3\}\); the only such integer congruent to \(1\pmod3\) is \(1\). Therefore \(x\) satisfies every exact-one clause. \(\square\)

If \(\mathcal A_E\) is nonempty, Gaussian elimination gives an affine point \(z_0\) and a basis matrix \(B\) of \(\ker_{\mathbb F_3}A_E\) with
\[
\mathcal A_E=\{z_0+B\lambda:
\lambda\in\mathbb F_3^{r}\},
\qquad
r=n-\operatorname{rank}_{\mathbb F_3}A_E.
\tag{11}
\]

**Corollary 4 (coefficient form).** For a nonempty affine solution space,
\[
\boxed{
F_E\text{ satisfiable}
\iff
\exists \lambda\in\mathbb F_3^r,\
\exists t\in\mathbb F_3:
z_0+B\lambda\in\{t,t+1\}^n.
}
\tag{12}
\]
The two-value criterion is thus *exact* but nonlinear in the coefficient vector \(\lambda\); computing \(z_0,B\) does not solve this final membership problem.

**Proposition 5 (minimal affine-blind obstruction).** Suppose \(F_E\) is unsatisfiable, \(A_Ez=\mathbf1\) is consistent, and deleting any single clause makes \(F_E\) satisfiable. If \(n'\) variables occur in the clauses, then
\[
\operatorname{rank}_{\mathbb F_3}(A_E)=|E|,
\qquad
|E|\le n'-1,
\qquad
\dim\ker A_E=n'-|E|\ge1,
\tag{13}
\]
where the matrix is restricted to the occurring variables.

*Proof.* A linear dependence among the clause rows, in a consistent affine system, makes a row with nonzero coefficient an affine consequence of the remaining equations. Deleting that clause would leave the affine solution set unchanged. By minimality the remaining formula admits a Boolean solution; this solution would also satisfy the deleted clause, a contradiction. Thus the clause rows are independent. The all-ones vector on the occurring variables lies in the kernel by (10), giving the final inequalities. \(\square\)

Equation (13) is a structural restriction on minimal obstructions, not a lower bound on the cost of detecting them.

## 3. From graph colouring to a linear kernel

Let \(G=(V,E_G)\), and let \(C=\{0,1,2\}\) be the colour set. Introduce one variable \(x_{v,c}\) for each vertex and colour, and a variable \(y_{\{u,v\},c}\) for each edge and colour. Consider the positive exact-one constraints
\[
\sum_{c\in C}x_{v,c}=1
\qquad(v\in V),
\tag{14}
\]
\[
x_{u,c}+x_{v,c}+y_{\{u,v\},c}=1
\qquad(\{u,v\}\in E_G,\ c\in C).
\tag{15}
\]

**Lemma 6 (colouring correspondence).** The Boolean system (14)–(15) is satisfiable if and only if \(G\) admits a proper three-colouring. Its affine relaxation over \(\mathbb F_3\) is consistent for every \(G\).

*Proof.* Equation (14) selects precisely one colour for each vertex. For an edge and colour, equation (15) can be completed by a Boolean slack variable exactly if both endpoints do not select that same colour. These are precisely the proper-colouring constraints. For affine feasibility over \(\mathbb F_3\), choose colour 0 at every vertex: \(x_{v,0}=1\) and \(x_{v,1}=x_{v,2}=0\) for every \(v\). For each edge \(e=\{u,v\}\), set \(y_{e,0}=-1\) and \(y_{e,1}=y_{e,2}=1\). Then every vertex equation sums to \(1\); the edge equation for colour 0 sums to \(1+1-1=1\), and each of the other two sums to \(0+0+1=1\). This is an affine \(\mathbb F_3\)-solution, without requiring the slack value \(-1\) to be Boolean. \(\square\)

For **any field** \(\mathbb F\), let \(K_G(\mathbb F)\) be the homogeneous kernel of the coefficient matrix in (14)–(15). Its elements satisfy
\[
\sum_{c\in C}x_{v,c}=0,
\qquad
y_{\{u,v\},c}=-x_{u,c}-x_{v,c}.
\tag{16}
\]
Write
\[
T_{\mathbb F}
=\{(a_0,a_1,a_2)\in\mathbb F^3:
a_0+a_1+a_2=0\}.
\tag{17}
\]

**Lemma 7 (kernel decomposition).**
\[
\boxed{
K_G(\mathbb F)\cong T_{\mathbb F}^{V},
\qquad
\dim_{\mathbb F}K_G(\mathbb F)=2|V|.
}
\tag{18}
\]

*Proof.* Vertex triples are independent choices of elements of \(T_{\mathbb F}\). All edge coordinates are then uniquely forced by (16), and every such choice extends to a kernel vector. Since \(\dim T_{\mathbb F}=2\), the result follows. \(\square\)

The correspondence (14)–(15) and the decomposition (18) are related but different statements. One concerns *Boolean solutions of an inhomogeneous system*; the other concerns *all vectors in a homogeneous linear kernel*.

## 4. The universal support-overlap theorem

Let \(I\) be the full finite coordinate set and \((I_v)_{v\in V}\) be pairwise disjoint subsets of \(I\), not necessarily covering \(I\). Let \(K\le\mathbb F^I\) be a linear subspace. In the colouring kernel, \(I_v\) consists of the three vertex coordinates \((v,c)\), whereas the edge-slack coordinates remain in \(I\setminus\bigcup_{v\in V}I_v\). Let \(B=(b_j)_{j\in J}\) be a finite indexed spanning family of \(K\); independence is **not** required. For every \(X\subseteq V\), \(\pi_X\) denotes restriction to the coordinates in \(\bigcup_{v\in X}I_v\).

Suppose an integer \(d\ge1\) and a graph \(G=(V,E_G)\) satisfy three properties:

\[
\dim_{\mathbb F}\pi_X(K)\ge d|X|
\qquad\text{for every }X\subseteq V;
\tag{19}
\]

\[
z|_{I_v}\ne0,\ z'|_{I_v}\ne0
\Longrightarrow
\operatorname{supp}(z)\cap\operatorname{supp}(z')\ne\varnothing;
\tag{20}
\]

\[
\{v,w\}\in E_G,\ z|_{I_v}\ne0,\ z'|_{I_w}\ne0
\Longrightarrow
\operatorname{supp}(z)\cap\operatorname{supp}(z')\ne\varnothing.
\tag{21}
\]
The quantifiers in (20)–(21) range over all \(z,z'\in K\).

The Hall-selection argument follows the classical marriage theorem [6]; the graph-kernel realization and its universal quantifier were developed in [2].

**Theorem 8 (Hall embedding).** Under (19)–(21), for every finite indexed spanning family \(B\) of \(K\),
\[
\boxed{G[K_d]\hookrightarrow H_B.}
\tag{22}
\]

*Proof.* Define
\[
S_v=\{j\in J:b_j|_{I_v}\ne0\}.
\tag{23}
\]
Condition (20) makes \(S_v\) a clique of \(H_B\). If \(\{v,w\}\in E_G\), condition (21) makes every *distinct* pair from \(S_v,S_w\) adjacent.

For every \(X\subseteq V\), the projections of the \(b_j\) with \(j\in\bigcup_{v\in X}S_v\) span \(\pi_X(K)\). Thus
\[
\left|\bigcup_{v\in X}S_v\right|
\ge\dim_{\mathbb F}\pi_X(K)
\ge d|X|.
\tag{24}
\]
Make \(d\) formal copies of every vertex \(v\), and connect each copy to every \(j\in S_v\). For any subset \(Y\) of copies, let \(X\subseteq V\) be its projection; then \(|Y|\le d|X|\) and its neighbourhood has at least \(d|X|\) members. Hall's marriage theorem [6] supplies an injection
\[
\iota:V\times[d]\hookrightarrow J,
\qquad \iota(v,a)\in S_v.
\tag{25}
\]
The images of the copies of the same \(v\) lie in a clique, and images of copies of adjacent \(v,w\) are adjacent. Hence \(\iota\) embeds the edges of \(G[K_d]\) into \(H_B\). \(\square\)

**Lemma 9 (the colouring kernel meets all three hypotheses).** For \(K=K_G(\mathbb F)\), with vertex triples as blocks, (19)–(21) hold with \(d=2\) over every field \(\mathbb F\).

*Proof.* By Lemma 7 the restriction of \(K_G(\mathbb F)\) to any \(X\subseteq V\) is the whole space \(T_{\mathbb F}^{X}\); hence its dimension is \(2|X|\), proving (19).

Every nonzero element of \(T_{\mathbb F}\) has at least two nonzero coordinates. Any two such supports intersect within a three-element set, giving (20).

For an edge \(\{v,w\}\), suppose kernel vectors \(z,z'\) are nonzero on the respective vertex blocks \(v,w\). If either is also nonzero on the other's vertex block, (20) applies. Otherwise the corresponding edge-coordinate triples are negatives of their respective nonzero vertex triples, by (16). Their supports therefore intersect, proving (21). \(\square\)

Theorem 8 and Lemma 9 prove the *first* assertion of Theorem 2, over **every field and every finite spanning family**.

## 5. Exact optimized width

Treewidth and pathwidth are understood in their graph-decomposition sense [7]. The graph-operation context and related bounds are reviewed in [8]; the exact formula below is proved directly, without importing an unverified product identity.

**Lemma 10 (clique blow-up).** If \(G\) is nonempty and \(d\ge1\), then
\[
\operatorname{tw}(G[K_d])
=d(\operatorname{tw}(G)+1)-1,
\tag{26}
\]
and
\[
\operatorname{pw}(G[K_d])
=d(\operatorname{pw}(G)+1)-1.
\tag{27}
\]

*Proof.* The upper bounds are obtained from any decomposition of \(G\) by replacing each occurrence of \(v\) in a bag by all of its \(d\) copies.

For the lower bound let \((T,\beta)\) be a tree decomposition of \(G[K_d]\) and let \(Q_v=\{v\}\times[d]\). Each \(Q_v\) is a clique and therefore occurs together in at least one bag; the set of bags containing all of \(Q_v\) is connected. Set
\[
\gamma(t)=\{v:Q_v\subseteq\beta(t)\}.
\tag{28}
\]
The bags \(\gamma(t)\) form a tree decomposition of \(G\): the bags containing a given \(v\) are connected, and if \(\{v,w\}\in E_G\), then \(Q_v\cup Q_w\) is a clique contained in a common bag. Since the sets \(Q_v\) are disjoint, for all \(t\),
\[
d|\gamma(t)|\le|\beta(t)|.
\tag{29}
\]
Taking maximal bag sizes yields the required reverse inequality in (26). The same construction preserves a decomposition whose underlying tree is a path, proving (27). \(\square\)

*Proof of the width equalities in Theorem 2.* By Theorem 8 and Lemma 9, \(G[K_2]\) embeds in \(H_B\) for every basis \(B\). Treewidth and pathwidth are monotone under taking subgraphs, so Lemma 10 gives
\[
\operatorname{tw}(H_B)\ge2\operatorname{tw}(G)+1,
\quad
\operatorname{pw}(H_B)\ge2\operatorname{pw}(G)+1.
\tag{30}
\]

For equality choose at each vertex the two independent triples
\[
(1,0,-1),\qquad(0,1,-1),
\tag{31}
\]
with zero triples at other vertices, and extend them uniquely to the edge coordinates using (16). These \(2|V|\) vectors form a basis by Lemma 7. Their supports intersect within each vertex pair, and between vertex pairs precisely when the corresponding vertices of \(G\) are adjacent. Thus for this particular basis \(B_{\mathrm{nat}}\),
\[
H_{B_{\mathrm{nat}}}\cong G[K_2].
\tag{32}
\]
Lemma 10 now supplies matching upper bounds, proving (6). \(\square\)

This establishes not merely that overlap width is *large* but the **exact minimum** across all bases. In particular,
\[
\min_B\operatorname{tw}(H_B(K_n))=2n-1,
\quad
\min_B\operatorname{tw}(H_B(K_{n,n}))=2n+1,
\quad
\min_B\operatorname{tw}(H_B(K_{3,3}))=7.
\tag{33}
\]

### 5.1. The measured quantity

The width in (6) belongs to the *support-overlap graph of a basis* of a fixed linear kernel. Its minimization is over all bases of that kernel. It is not, by definition, the matroid tree-width studied by Hliněný and Whittle [9, 10], nor the minimal state-space dimension of a tree realization of a linear code as in Kashyap [11]. The addendum [10] is material when invoking the former theory; neither comparison changes the invariant defined here.

There is a distinct quantity for an online Boolean computation: the number of state wires crossing an input-time boundary. This equals at most the number of persistent state bits \(S\), but is **not** the treewidth in (6). The two quantities can be compared only after a mathematically defined map puts them on the same representation and proves the required inequalities.

### 5.2. Limits of a width-only argument

The family \(G=K_n\), \(n\ge4\), has optimized overlap width \(2n-1\). Yet its non-three-colourability formula contains the fixed contradictory \(K_4\) subformula and admits a Resolution refutation of constant size. Similarly \(K_{n,n}\) has increasing optimized overlap width but is three-colourable. Therefore
\[
\text{large optimized overlap width}
\not\Longrightarrow
\text{large general proof or decision cost}.
\tag{34}
\]
This is compatible with Theorem 2, whose conclusion concerns a linear-representation invariant.

## 6. The formalized three-element-field instance

The exact \(\mathbb F_3\) treewidth identity of Theorem 2 has a separate Lean 4 formulation, using Lean 4 [12] and the Mathlib library [13]. Writing \(\operatorname{TwLe}(H,k)\) for “\(H\) has treewidth at most \(k\),” the formal statement, for every finite nonempty vertex type and every \(k\in\mathbb N\), has the mathematical content
\[
\boxed{
\left(
\exists B\text{ basis of }K_G(\mathbb F_3):
\operatorname{TwLe}(H_B,2k+1)
\right)
\iff
\operatorname{TwLe}(G,k).
}
\tag{35}
\]
The source contains explicit proof terms for the canonical-basis upper bound, the converse inequality, and their equivalence, rather than placeholders or locally declared axioms. These are **formal proof artifacts** for the stated \(\mathbb F_3\) theorem. This manuscript does not claim an independent reproduction of their complete kernel build.

The universal spanning-family subgraph embedding over arbitrary fields is proved in Sections 4–5. It is **not** identified with (35): the broader field quantifier and the subgraph embedding are not both represented by the same Lean declaration.

## 7. Exact simulation of one-pass computations

A deterministic one-pass algorithm over an \(N\)-bit input has, in a state-based representation, a sequence
\[
q_{t+1}=U_t(q_t,z_t),
\qquad
U_t:\{0,1\}^{S}\times\{0,1\}\to\{0,1\}^{S},
\quad 0\le t<N,
\tag{36}
\]
and a final exact decoder \(D\).

**Lemma 11 (bounded-time transition circuits).** Suppose an update is implemented by a fixed deterministic Turing machine using at most \(\tau\) steps with at most \(S\) bits of work configuration. The update transition can be implemented by a fan-in-two Boolean circuit with gate count polynomial in \(\tau,S\), and the encoded input parameters. Under the usual local tableau convention this is \(O(\tau S)\), up to the fixed machine's representation overhead.

*Proof.* Represent the bounded work configuration on Boolean wires. A single machine move is a fixed Boolean transformation of the bounded tableau, requiring \(O(S)\) local gate operations under that convention. Concatenating at most \(\tau\) such transformations gives a circuit of size \(O(\tau S)\). It computes the deterministic update for every admissible configuration and incoming input symbol. \(\square\)

This proof is scoped to the stated deterministic Turing-machine tableau. The streaming algorithm of [4] instead uses a RAM model that operates on \(O(1)\) bits of bounded workspace at a time. In that model, one RAM operation can be compiled by decoding the addressed position among at most \(S\) stored bits, multiplexing the selected bits, performing the fixed Boolean operation and updating the selected storage bits. This requires at most \(\operatorname{poly}(S,m)\) fan-in-two gates per operation, including address tests and control. Unrolling at most \(\tau\) such operations therefore gives \(\operatorname{poly}(\tau,S,m)\) gates per inter-input update, sufficient for Theorem 3. An arbitrary different random-access model does not automatically inherit the sharper Turing-machine tableau bound \(O(\tau S)\).

**Lemma 12 (exact stage unrolling).** Given exact stage circuits \(U_0,\ldots,U_{N-1}\) and decoder \(D\), there is an acyclic Boolean circuit for the complete input-output relation with
\[
\operatorname{CC}(\text{unrolled circuit})
\le
\sum_{t=0}^{N-1}\operatorname{CC}(U_t)
+\operatorname{CC}(D)=\Gamma,
\tag{37}
\]
and at most \(S\) persistent state wires across every *input-time boundary*.

*Proof.* Connect the state outputs of stage \(t\) to the state inputs of stage \(t+1\) and attach \(D\) after the last update. Induction on the prefix length proves that the connected circuit computes the exact state after every input prefix and the correct final result. The gate counts add, while only the \(S\) state wires are carried from stage to stage. \(\square\)

This lemma permits nonlinearity, time-dependent state updates and gate sharing within the circuit for a stage. Deferred work is counted in \(D\). It **does not** assert that the internal layers of \(U_t\) have width \(S\), or that the resulting Boolean DAG is a basis of a vector space.

The bounded-time simulation and the stage-cut argument have also undergone separate cross-model review in these precise scopes. The review establishes neither a bound from below on \(\Gamma\) nor the existence of a linear overlap representation for every circuit.

## 8. A conditional complexity-class consequence

Let \(m\in\mathbb N\), \(N=2^m\), and let \(s(m)\ge m\) satisfy the parameter and constructibility requirements of [4]. Fix a language \(A\in PH\). The **total** search problem \(\mathrm{SearchMCSP}^{A}[s]\) receives the full length-\(N\) truth table of an \(m\)-input Boolean function. It must return a circuit of at most \(s(m)\) gates, allowed to have \(A\)-oracle gates, that represents the table, or correctly report that no such circuit exists.

Oracle gates in the *circuit being synthesized* are distinct from oracle access by the *ordinary streaming algorithm*. A theorem about one model may not be applied to the other without accounting for the distinction.

**Update-time convention in the cited source.** In [4, Section 2, “Streaming Algorithms”], update time \(u(N)\) is defined as a bound on the total running time **between any two successive input-bit reads**, and the final report must be produced within \(O(u(N))\) time. It is thus a worst-case *per-inter-read interval* bound, not merely an amortized average. In particular, Theorem 1.2 of [4] supplies a uniformly bounded interval cost, so each update circuit in (7) can be charged at the same polynomial scale after replacement of its polynomial-hierarchy oracle calls under \(P=NP\).

Call \(\mathcal C_m\) an admissible staged Boolean realization if it solves **all instances** of this exact total relation and charges every update circuit and its final decoder as in (7). The quantifier in (8) is over all such realizations, not only those with canonical or linear states.

*Proof of Theorem 3.* Assume for contradiction that \(P=NP\). Then \(PH=P\). The algorithm and conditional transfer of McKay, Murray and Williams [4, Theorems 1.2 and 1.3], with their prescribed \(s,A\), yield a uniform deterministic one-pass solver of the exact total search relation with polynomial-in-\(s\) space and polynomial-in-\(s\) worst-case update time. In the construction, the relevant oracle questions have lengths polynomial in \(s\). Under \(P=NP\), these questions can be answered by ordinary polynomial-time computation, so the solver need not be granted free oracle operations.

Write its state size and worst-case update time as
\[
S_{\rm alg}(m)\le s(m)^{c_0},\qquad
\tau_{\rm alg}(m)\le s(m)^{d_0}
\tag{38}
\]
for fixed exponents \(c_0,d_0\) and all sufficiently large \(m\). By the RAM-to-circuit simulation explained after Lemma 11, each such update is implemented by a Boolean circuit with fixed polynomial overhead in \(S_{\rm alg},\tau_{\rm alg},m\), valid for every intermediate configuration and incoming bit. The MMW definition quoted above ensures that \(\tau_{\rm alg}\) bounds each successive-read interval in the worst case rather than only the mean cost. The final output is obtained by a similarly charged computation: outputting a circuit of size \(s\) takes at most polynomial time and space under the specified encoding. Because \(m\le s(m)\), there are fixed \(c,d\) with
\[
S(\mathcal C_m)\le s(m)^c,\qquad
\Gamma(\mathcal C_m)\le 2^m s(m)^d
\tag{39}
\]
for every sufficiently large \(m\). By Lemma 12, the stages and decoder compute the same exact total search relation, so \(\mathcal C_m\) is admissible.

This contradicts the universal exclusion in (8). Hence \(P\ne NP\). \(\square\)

Thus the implication
\[
\boxed{
\begin{gathered}
\text{No exact staged realization with}\\
S=s^{O(1)},\quad\Gamma\le 2^m s^{O(1)}
\\[3pt]\Longrightarrow\
\text{no ordinary one-pass solver with}\\
S_{\rm alg}=s^{O(1)},\quad \tau_{\rm alg}=s^{O(1)}
\\[3pt]\Longrightarrow P\ne NP
\end{gathered}}
\tag{40}
\]
is mathematically established, with the full uniformity and oracle qualifications of [4]. The first arrow is the contrapositive of the proved simulation; the second is the published complexity-theoretic transfer.

**Crucially, (8) itself is not established by Lemmas 11–12.** Those lemmas give upper bounds on the cost of simulating a proposed *fast* computation. They do not show that no such computation exists.

### 8.1. A weaker sufficient lower-bound premise

Theorem 3 is formulated using (8) because the staged-circuit representation makes the simulation explicit. **Equation (8) is sufficient, not necessary, for applying the published streaming separation theorem.** Indeed, it excludes a different, larger class: independently selected staged Boolean circuits at every sufficiently large input length.

To express the weaker requirement, let \(\mathfrak M_{s,A}^{\mathrm{unif}}\) be the class of ordinary **uniform deterministic one-pass algorithms** that solve the exact total \(\mathrm{SearchMCSP}^{A}[s]\) relation at every input length, with the same output and oracle conventions as in [4]. For \(\mathcal M\in\mathfrak M_{s,A}^{\mathrm{unif}}\), write \(S_{\mathcal M}(m)\) for its space usage and \(\tau_{\mathcal M}(m)\) for its worst-case update time. For some admissible \(s,A\), it is enough to prove

\[
\boxed{
\begin{aligned}
&\forall \mathcal M\in\mathfrak M_{s,A}^{\mathrm{unif}}\;
\forall c,d\in\mathbb N\;
\forall m_0\;
\exists m\ge m_0:\\
&S_{\mathcal M}(m)>s(m)^c
\quad\lor\quad
\tau_{\mathcal M}(m)>s(m)^d .
\end{aligned}}
\tag{40a}
\]

This says that **no single uniform exact streaming algorithm** achieves both polynomial-in-\(s\) resource bounds at every sufficiently large input length. It does *not* forbid a separate efficient nonuniform staged realization at each length.

**Proposition 13 (weaker sufficient streaming premise).** For parameters \(s,A\) satisfying the conditions of the streaming theorem in [4], (40a) implies \(P\ne NP\). Further, the stronger circuit exclusion (8) implies (40a).

*Proof.* Under \(P=NP\), the ordinary uniform algorithm provided by the construction underlying [4, Theorems 1.2–1.3] has \(S_{\mathcal M}(m),\tau_{\mathcal M}(m)=s(m)^{O(1)}\) eventually, contradicting (40a). Conversely, if (40a) were false, some uniform algorithm would achieve both resource bounds with fixed exponents for every sufficiently large \(m\). Lemmas 11–12 would turn its updates and complete decoder into an admissible staged circuit with \(S=s^{O(1)}\) and \(\Gamma\le2^m s^{O(1)}\) for all those \(m\), contradicting (8), after increasing the exponents to absorb fixed polynomial overhead. \(\square\)

The logical structure is therefore

\[
\boxed{
\text{universal nonuniform circuit exclusion (8)}
\Longrightarrow
\text{uniform streaming lower bound (40a)}
\Longrightarrow P\ne NP .
}
\tag{40b}
\]

**Neither converse is claimed.** In particular, a proof of (40a) by another mathematical method would make a proof of (8) unnecessary. If the graph-kernel width theorem is used to prove (40a), the required quantitative representation-to-computation argument need cover the uniform machines in (40a) rather than all nonuniform circuits of (8). It must still apply to *every* such uniform machine, preserve exact search semantics, and yield an asymptotic contradiction to polynomial space and update time. The completed exact treewidth identity and the upper-bound simulation alone do not provide that lower-bound argument.

## 9. On combining the two kinds of bounds

The structural result is an exact optimum:
\[
\underbrace{2\operatorname{tw}(G)+1}_{\text{lower bound for every basis}}
\le\operatorname{tw}(H_B),
\tag{41}
\]
with equality for an explicit \(B=B_{\rm nat}\).

The computational lemmas, for an ordinary \(S\)-space, \(\tau\)-step update machine, give
\[
\operatorname{CC}(U_t)=O(\tau S),\qquad
\Gamma=O(2^m\tau S)+\operatorname{CC}(D),
\tag{42}
\]
in the specified tableau convention, and an inter-stage cut of at most \(S\) wires.

The two statements are **both quantitative**. They do not yet bound the same quantity. In particular:
\[
\operatorname{tw}(H_B)\ne
\operatorname{cutwidth}_{\rm input\ stage}(\mathcal C)
\quad\text{by definition or by the preceding lemmas}.
\tag{43}
\]

A sufficient structural-to-computational transfer would require, for each relevant \(m,s\), a suitable graph-indexed linear space \(K_{m,s}\), and for **every** admissible nonlinear staged realization \(\mathcal C_m\) an associated spanning family \(B_{\mathcal C_m}\) with the following *proved* properties:

1. Its coordinates and blocks encode dependencies of the **same exact total search relation**, not those of a different decision task or of an arbitrarily chosen linear relaxation.

2. The resulting space obeys the projection-rank and both support-intersection conditions (19)–(21), with an explicit rank parameter \(d_{m,s}\).

3. There is an explicit resource upper bound
\[
\operatorname{tw}(H_{B_{\mathcal C_m}})
\le
\Psi\bigl(m,s,S(\mathcal C_m),\Gamma(\mathcal C_m)\bigr)
\tag{44}
\]
valid **for all** admissible state encodings, including nonlinear and time-dependent recodings, arbitrary gate sharing, redundancy and deferred final computation.

4. For every fixed resource exponent \(c,d\), the graph-side lower bound exceeds that upper bound throughout an asymptotically sufficient family:
\[
\begin{aligned}
d_{m,s}\bigl(\operatorname{tw}(G_{m,s})+1\bigr)-1
&>\Psi\bigl(m,s,s(m)^c,2^m s(m)^d\bigr).
\end{aligned}
\tag{45}
\]

Under these additional hypotheses the universal embedding gives
\[
\begin{aligned}
d_{m,s}(\operatorname{tw}(G_{m,s})+1)-1
&\le \operatorname{tw}(H_{B_{\mathcal C_m}})\\
&\le \Psi(m,s,S,\Gamma)\\
&<d_{m,s}(\operatorname{tw}(G_{m,s})+1)-1,
\end{aligned}
\tag{46}
\]
a contradiction. Theorem 3 would then imply \(P\ne NP\).

**Proposition 14 (conditional combination under the stronger circuit exclusion).** If a construction satisfying conditions 1–4 is proved for the full admissible computation class and the parameters of Theorem 3, then \(P\ne NP\).

*Proof.* A polynomial-resource staged realization would satisfy (46), which is impossible. Thus (8) holds and Theorem 3 applies. \(\square\)

The proof of this conditional proposition is elementary once conditions 1–4 are assumed. Their satisfaction for **arbitrary nonlinear online circuits** is not established by the universal kernel theorem: the latter quantifies over spanning families *already belonging to an appropriate linear space*. This is one sufficient route, not an obligatory route. By Proposition 13, a direct proof of the weaker uniform streaming lower bound (40a) would also imply \(P\ne NP\), without proving the nonuniform exclusion (8) or the stronger universal representation map demanded in conditions 1–4.

This is not a gap in the proof of the width identity (6), which is complete. It is a new cross-model implication with different quantified objects.

The easy high-width examples (33) also rule out any unconditional assertion that a large basis-overlap width, by itself, makes a corresponding formula computationally difficult. A valid additional hypothesis must distinguish the exact search problem from those controls. Standard proof barriers include relativization [14] and, under the requisite cryptographic assumptions, natural proofs [15]. Their applicability to a proposed transfer must be established, rather than inferred solely from its algebraic notation.

## 10. Algebraic proof-complexity consequences

There is a separate exact translation between characteristic-two polynomial proof systems. For Boolean variables \(a,b,c\) over \(\mathbb F_2\), the exact-one relation is equivalent to
\[
a+b+c+1=0,\qquad
ab+ac+bc=0
\tag{47}
\]
together with Boolean axioms \(x^2-x=0\).

For the colouring encoding (14)–(15), substitute
\[
y_{\{u,v\},c}\longmapsto1+x_{u,c}+x_{v,c}.
\tag{48}
\]
The edge parity polynomial becomes zero, and modulo the Boolean axioms the quadratic polynomial becomes \(x_{u,c}x_{v,c}\). The vertex exact-one equations remain the standard colouring equations.

**Proposition 15 (degree-bounded substitution).** A degree-\(D\) Polynomial Calculus refutation of the positive exact-one XOR/carry system over \(\mathbb F_2\) induces a Polynomial Calculus refutation of its standard graph-colouring encoding of degree at most \(2D\).

*Proof.* Substitution (48) has degree one and sends each source axiom to zero or to a degree-at-most-two combination of target axioms and Boolean relations. A Polynomial Calculus addition step maps to addition. Multiplication by a vertex variable is preserved, while multiplication by an eliminated slack variable becomes multiplication by an affine linear expression and is simulated by a bounded number of variable-multiplication and addition steps. The degrees of intermediate lines increase by at most a factor of two. The last line \(1\) remains \(1\). \(\square\)

Hence the graph-colouring family of Lauria and Nordström [3], which requires Polynomial Calculus degree \(\Omega(|V|)\) in the corresponding algebraic encoding, yields the same asymptotic degree lower bound for its exact-one encoding, up to the factor two. Degree–size relations for Polynomial Calculus are developed by Impagliazzo, Pudlák and Sgall [5]; applications of those relations must retain their quantitative assumptions. This is a *restricted algebraic proof-system* lower bound, not a lower bound on arbitrary Boolean circuits. Stronger proof systems may admit short refutations of the same instances.

## 11. Precise final statement

For positive exact-one satisfiability, the following are proved:

\[
\boxed{
F_E\text{ satisfiable}
\iff
\exists z\in\mathcal A_E:
|\{z_i\}|\le2;
}
\tag{49}
\]

\[
\boxed{
K_G(\mathbb F)\cong T_{\mathbb F}^{V}
\Longrightarrow
\forall B\text{ spanning}:\ G[K_2]\hookrightarrow H_B
\Longrightarrow
\min_B\operatorname{tw}(H_B)=2\operatorname{tw}(G)+1;
}
\tag{50}
\]

\[
\boxed{
\begin{aligned}
(S_{\rm alg},\tau_{\rm alg})=(s^{O(1)},s^{O(1)})
&\Longrightarrow
(S(\mathcal C_m),\Gamma(\mathcal C_m))
=(s^{O(1)},\,\le 2^m s^{O(1)}),\\
\text{universal exclusion of the latter}
&\Longrightarrow P\ne NP.
\end{aligned}}
\tag{51}
\]

The first equivalence and the structural chain are unconditional. The simulation and the **implication** to \(P\ne NP\) are proved in their stated models. The hypothesis excluding every polynomial-resource exact staged realization in Theorem 3 is not established by the preceding structural statements. It is stronger than necessary: the quantified exclusion of uniformly implemented polynomial-resource streaming algorithms in (40a) would already suffice by the published theorem. Neither exclusion is obtained automatically by combining the exact overlap-width equality with the upper-bound circuit simulations.

This article therefore offers a mathematical theorem of exact, representation-independent *linear* overlap width, a formalized special-field equivalence, and a precise conditional complexity consequence. It does not assert an unconditional proof of \(P\ne NP\) from these results alone.

## Acknowledgments

This research was carried out using FruitStack, a multi-agent research environment developed by the author to coordinate mathematical exploration, counterexample analysis, independent checking and formalisation.

## References

[1] T. J. Schaefer, “The Complexity of Satisfiability Problems,” *Proceedings of STOC* (1978), 216–226.

[2] B. Tonn, “Every Basis Sees the Blow-Up: A Universal Subgraph Theorem for Support-Overlap Graphs of a Colouring Kernel” (2026), DOI: 10.5281/zenodo.24438918.

[3] M. Lauria and J. Nordström, “Graph Colouring Is Hard for Algorithms Based on Hilbert's Nullstellensatz and Gröbner Bases,” *Proceedings of CCC* (2017), Article 2.

[4] D. M. McKay, C. D. Murray and R. R. Williams, “Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes,” *Proceedings of STOC* (2019), 1215–1225, DOI: 10.1145/3313276.3316396.

[5] R. Impagliazzo, P. Pudlák and J. Sgall, “Lower Bounds for the Polynomial Calculus and the Gröbner Basis Algorithm,” *Computational Complexity* 8 (1999), 127–144, DOI: 10.1007/s000370050024.

[6] P. Hall, “On Representatives of Subsets,” *Journal of the London Mathematical Society* s1-10 (1935), 26–30, DOI: 10.1112/jlms/s1-10.37.26.

[7] N. Robertson and P. D. Seymour, “Graph Minors. II. Algorithmic Aspects of Tree-Width,” *Journal of Algorithms* 7 (1986), 309–322, DOI: 10.1016/0196-6774(86)90023-4.

[8] F. Gurski and R. Weishaupt, “The Behavior of Tree-Width and Path-Width Under Graph Operations and Graph Transformations,” *Algorithms* 18(7) (2025), article 386, DOI: 10.3390/a18070386.

[9] P. Hliněný and G. Whittle, “Matroid Tree-Width,” *European Journal of Combinatorics* 27 (2006), 1117–1128, DOI: 10.1016/j.ejc.2006.06.005.

[10] P. Hliněný and G. Whittle, “Addendum to Matroid Tree-Width,” *European Journal of Combinatorics* 30 (2009), 1036–1044, DOI: 10.1016/j.ejc.2008.09.028.

[11] N. Kashyap, “On Minimal Tree Realizations of Linear Codes,” *IEEE Transactions on Information Theory* 55(8) (2009), 3501–3519, DOI: 10.1109/TIT.2009.2023718.

[12] L. de Moura and S. Ullrich, “The Lean 4 Theorem Prover and Programming Language,” in *Automated Deduction – CADE 28*, LNCS 12699 (2021), 625–635, DOI: 10.1007/978-3-030-79876-5_37.

[13] The mathlib Community, “The Lean Mathematical Library,” *Proceedings of the 9th ACM SIGPLAN International Conference on Certified Programs and Proofs* (CPP 2020), 367–381, DOI: 10.1145/3372885.3373824.

[14] T. Baker, J. Gill and R. Solovay, “Relativizations of the P =? NP Question,” *SIAM Journal on Computing* 4(4) (1975), 431–442, DOI: 10.1137/0204037.

[15] A. A. Razborov and S. Rudich, “Natural Proofs,” *Journal of Computer and System Sciences* 55(1) (1997), 24–35, DOI: 10.1006/jcss.1997.1494.

---

*This manuscript distinguishes completed formal and mathematical derivations from additional hypotheses of conditional theorems. In particular, none of its external complexity-class consequences is presented without the quantifiers and assumptions under which it follows.*
