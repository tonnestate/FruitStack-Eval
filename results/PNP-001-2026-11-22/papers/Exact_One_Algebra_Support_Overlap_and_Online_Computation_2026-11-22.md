# Algebraic Structure and Support-Overlap Width of Exact-One Constraint Systems

**Björn Tonn**  
22 November 2026

## Abstract

We examine positive exact-one satisfiability through its affine relaxation over the three-element field and through graph-indexed homogeneous kernels. The Boolean feasibility condition is characterized exactly by the existence of an affine solution with at most two distinct coordinate values. For the kernel of the standard three-colouring encoding, a universal embedding argument shows that every finite spanning family has a support-overlap graph containing the two-clique blow-up of the input graph. An explicit basis attains the bound, giving
\[
\min_{B\text{ a basis of }K_G(\mathbb F)}
\operatorname{tw}(H_B)=2\operatorname{tw}(G)+1
\]
over every field \(\mathbb F\). The corresponding equivalence over \(\mathbb F_3\) has also been formalized in Lean 4. We give a further algebraic proof-complexity transfer, and then establish a conditional complexity implication using a precisely defined staged computation model and the streaming theorem of McKay, Murray and Williams. The formal derivation of that implication is distinct from establishing its universal lower-bound premise. In particular, the structural embedding theorem alone does not furnish a lower bound for arbitrary nonlinear circuits.

*2020 Mathematics Subject Classification:* 68Q17, 05C83, 05B35, 03F20.  
*Keywords:* exact-one satisfiability, affine solution sets, Hall's theorem, linear codes, support-overlap graphs, treewidth, Polynomial Calculus, streaming computation.

---

## 1. Boolean feasibility in an affine space

Let \(n\ge3\) and let \(\mathcal T_n=\{\{i,j,k\}:1\le i<j<k\le n\}\). A finite selection \(E\subseteq\mathcal T_n\) defines the positive exact-one formula
\[
F_E(x)=\bigwedge_{\{i,j,k\}\in E}(x_i+x_j+x_k=1),
\qquad x\in\{0,1\}^n.
\tag{1}
\]
Write \(A_E\in\mathbb F_3^{E\times[n]}\) for its clause-incidence matrix and
\[
\mathcal A_E=\{z\in\mathbb F_3^n:A_Ez=\mathbf1\},
\qquad K_E=\ker_{\mathbb F_3}A_E.
\tag{2}
\]
Every row has exactly three nonzero entries, all equal to one. Therefore
\[
A_E\mathbf1=\mathbf0,\qquad
z\in\mathcal A_E\Longrightarrow z+t\mathbf1\in\mathcal A_E
\quad(t\in\mathbb F_3).
\tag{3}
\]

**Theorem 1 (two-value characterization).** The following equivalence holds for every \(E\):
\[
\boxed{
F_E\text{ is satisfiable}
\iff
\exists z\in\mathcal A_E:
\bigl|\{z_i:1\le i\le n\}\bigr|\le2.
}
\tag{4}
\]

*Proof.* A satisfying Boolean vector lies in \(\mathcal A_E\), since for a triple of Boolean variables, the congruence \(x_i+x_j+x_k\equiv1\pmod3\) holds exactly when the integer sum is one. Conversely, if \(E=\varnothing\), the formula is satisfiable. If \(E\ne\varnothing\), no constant vector solves \(A_Ez=\mathbf1\), because its clause sums equal zero in \(\mathbb F_3\). Hence a solution using at most two field elements uses exactly two. Any two-element subset of \(\mathbb F_3\) is a translate of \(\{0,1\}\). By (3), an appropriate translate of \(z\) is again in \(\mathcal A_E\) and has Boolean coordinates. Every corresponding integer clause sum must therefore equal one. \(\square\)

If \(\mathcal A_E\ne\varnothing\), linear algebra supplies \(z_0\in\mathcal A_E\) and a basis matrix \(B\) for \(K_E\), so that
\[
\mathcal A_E=z_0+\operatorname{im}B.
\tag{5}
\]
The theorem immediately gives the exact decision representation
\[
\boxed{
F_E\text{ satisfiable}
\iff
\exists\lambda\in\mathbb F_3^{\dim K_E}\;
\exists t\in\mathbb F_3:
z_0+B\lambda\in\{t,t+1\}^n.
}
\tag{6}
\]
Equation (6) is an exact equivalence, but its membership condition is nonlinear in \(\lambda\). Computing a basis by Gaussian elimination does not itself resolve this condition.

A related restriction applies to minimal unsatisfiable formulas whose affine systems are consistent.

**Proposition 2.** Suppose \(F_E\) is unsatisfiable, \(\mathcal A_E\ne\varnothing\), and removing any clause makes it satisfiable. If \(n'\) is the number of occurring variables, then
\[
\operatorname{rank}_{\mathbb F_3}(A_E)=|E|\le n'-1,\qquad
\dim\ker A_E=n'-|E|\ge1.
\tag{7}
\]

*Proof.* If a clause row were linearly dependent on the other rows, consistency of the affine system would make its equation a consequence of the remaining equations. Removing that clause would not change the affine solution space; by minimality, the remaining clauses would have a Boolean solution, which would then also satisfy the deleted clause. This contradicts unsatisfiability. Thus the rows are independent. The nonzero all-ones vector lies in the kernel by (3), so the rank is at most \(n'-1\). \(\square\)

These are exact statements about affine feasibility and minimal obstructions. They make no assertion about general Boolean circuit lower bounds.

## 2. The graph-colouring kernel

Let \(G=(V,E_G)\) be a nonempty finite simple graph, and let \(C=\{0,1,2\}\). For every \(v\in V\) and \(c\in C\), introduce a variable \(x_{v,c}\), and for every \(\{u,v\}\in E_G\), a variable \(y_{\{u,v\},c}\). Form the exact-one equations
\[
\sum_{c\in C}x_{v,c}=1\qquad(v\in V),
\tag{8}
\]
\[
x_{u,c}+x_{v,c}+y_{\{u,v\},c}=1
\qquad(\{u,v\}\in E_G,\ c\in C).
\tag{9}
\]

**Lemma 3.** Equations (8)–(9) have a Boolean solution if and only if \(G\) has a proper three-colouring. Over \(\mathbb F_3\), their affine relaxation always has a solution.

*Proof.* Equation (8) chooses exactly one colour at each vertex. A Boolean value for \(y_{\{u,v\},c}\) exists in (9) precisely if \(u,v\) do not both choose colour \(c\). Thus the Boolean assignments correspond exactly to proper three-colourings. Over \(\mathbb F_3\), taking \(x_{v,c}=0\) and \(y_{\{u,v\},c}=1\) satisfies every equation. \(\square\)

Over an arbitrary field \(\mathbb F\), let \(K_G(\mathbb F)\) be the homogeneous kernel of the coefficient matrix in (8)–(9):
\[
\sum_{c\in C}x_{v,c}=0,\qquad
x_{u,c}+x_{v,c}+y_{\{u,v\},c}=0.
\tag{10}
\]
Define the two-dimensional zero-sum space
\[
T_{\mathbb F}=\{(a_0,a_1,a_2)\in\mathbb F^3:
a_0+a_1+a_2=0\}.
\tag{11}
\]

**Lemma 4.** Restriction to the vertex coordinates induces an isomorphism
\[
\boxed{
K_G(\mathbb F)\cong T_{\mathbb F}^{\,V},
\qquad
\dim_{\mathbb F}K_G(\mathbb F)=2|V|.
}
\tag{12}
\]

*Proof.* Each vertex triple can be chosen independently in \(T_{\mathbb F}\). Once these triples have been fixed, every edge variable is uniquely determined by
\[
y_{\{u,v\},c}=-x_{u,c}-x_{v,c}.
\tag{13}
\]
Conversely, (13) extends any tuple of zero-sum vertex triples to a vector of the kernel. The dimension statement follows from \(\dim T_{\mathbb F}=2\). \(\square\)

Note that the Boolean satisfiability equivalence in Lemma 3 and the field-independent kernel isomorphism in Lemma 4 are statements about distinct mathematical objects.

## 3. A universal embedding theorem

Let \(I=\bigsqcup_{v\in V}I_v\) be a disjoint union of coordinate blocks, \(K\le\mathbb F^I\) a linear space, and \(B=(b_j)_{j\in J}\) a finite indexed spanning family of \(K\); dependencies among the \(b_j\) are allowed. Its **support-overlap graph** \(H_B\) has vertex set \(J\) and edges
\[
\{j,k\}\in E(H_B)
\iff j\ne k\text{ and }
\operatorname{supp}(b_j)\cap\operatorname{supp}(b_k)\ne\varnothing.
\tag{14}
\]
For \(X\subseteq V\), write \(\pi_X\) for projection to the blocks \(\bigcup_{v\in X}I_v\).

Fix a graph \(G=(V,E_G)\) and an integer \(d\ge1\). Assume:

\[
\dim_{\mathbb F}\pi_X(K)\ge d|X|
\qquad\forall X\subseteq V;
\tag{15}
\]

\[
u|_{I_v}\ne0,\ w|_{I_v}\ne0
\Longrightarrow
\operatorname{supp}(u)\cap\operatorname{supp}(w)\ne\varnothing;
\tag{16}
\]

\[
vw\in E_G,\ u|_{I_v}\ne0,\ w|_{I_w}\ne0
\Longrightarrow
\operatorname{supp}(u)\cap\operatorname{supp}(w)\ne\varnothing.
\tag{17}
\]

The conditions in (16)–(17) are required for all indicated pairs \(u,w\in K\). Let \(G[K_d]\) denote the graph obtained by replacing each vertex of \(G\) by a \(d\)-clique and each edge of \(G\) by all \(d^2\) edges between the corresponding cliques.

**Theorem 5 (universal support-overlap embedding).** If (15)–(17) hold, then every finite spanning family \(B\) of \(K\) satisfies
\[
\boxed{G[K_d]\hookrightarrow H_B.}
\tag{18}
\]

*Proof.* For each \(v\in V\) put
\[
S_v=\{j\in J:b_j|_{I_v}\ne0\}.
\tag{19}
\]
By (16), each \(S_v\) is a clique. By (17), for each edge \(vw\in E_G\), every pair of *distinct* vertices in \(S_v,S_w\) is adjacent in \(H_B\). Since \(B\) spans \(K\), the projected members supported on blocks indexed by \(X\) span \(\pi_X(K)\). Hence for every \(X\subseteq V\),
\[
\left|\bigcup_{v\in X}S_v\right|
\ge\dim\pi_X(K)\ge d|X|.
\tag{20}
\]
Make \(d\) labelled copies of each \(v\) and connect each copy to every \(j\in S_v\). A subset of copied vertices projecting to \(X\) has at most \(d|X|\) members, while its neighbourhood contains \(\bigcup_{v\in X}S_v\). By Hall's marriage theorem there is an injection
\[
\iota:V\times[d]\hookrightarrow J,\qquad
\iota(v,a)\in S_v.
\tag{21}
\]
Two copies of the same vertex map to adjacent members of the clique \(S_v\), and copies of adjacent vertices map to adjacent members of \(H_B\). Thus \(\iota\) is a subgraph embedding of \(G[K_d]\). \(\square\)

The universal quantifier in (18) is over **all spanning families**, not merely bases selected by a particular algorithm.

## 4. Exact treewidth and pathwidth

**Lemma 6 (clique blow-up).** For every nonempty finite simple graph \(G\) and integer \(d\ge1\),
\[
\operatorname{tw}(G[K_d])
=d(\operatorname{tw}(G)+1)-1,
\tag{22}
\]
\[
\operatorname{pw}(G[K_d])
=d(\operatorname{pw}(G)+1)-1.
\tag{23}
\]

*Proof.* For the upper bounds, take a tree or path decomposition of \(G\) and replace each occurrence of a vertex in a bag by all \(d\) copies. The new maximum bag size is at most \(d\) times the old maximum bag size.

Conversely, let \((T,\beta)\) be a tree decomposition of \(G[K_d]\), and write \(Q_v=\{v\}\times[d]\). Every \(Q_v\) is a clique, so the set of bags containing all of \(Q_v\) is nonempty and connected; this follows from the Helly property of subtrees of a tree. Define
\[
\gamma(t)=\{v:Q_v\subseteq\beta(t)\}.
\tag{24}
\]
Every vertex of \(G\) occurs in some \(\gamma(t)\), and the bags containing it form a connected subtree. For each edge \(vw\in E_G\), the union \(Q_v\cup Q_w\) is a clique, so some \(\gamma(t)\) contains both \(v,w\). Consequently \((T,\gamma)\) is a decomposition of \(G\). The \(Q_v\) are disjoint, hence
\[
d|\gamma(t)|\le|\beta(t)|
\qquad\text{for every }t.
\tag{25}
\]
This gives the reverse treewidth inequality. The same transformation preserves a decomposition tree that is a path, proving the pathwidth statement. \(\square\)

**Lemma 7 (the colouring kernel satisfies (15)–(17)).** For \(K=K_G(\mathbb F)\) with vertex triples as coordinate blocks, all hypotheses of Theorem 5 hold with \(d=2\), independently of the characteristic of \(\mathbb F\).

*Proof.* The isomorphism (12) makes the projection to any \(X\subseteq V\) onto \(T_{\mathbb F}^X\) surjective, proving (15).

Every nonzero element of \(T_{\mathbb F}\) has support of size at least two. Two subsets of a three-element coordinate set, each of size at least two, have a common coordinate. This proves (16).

Let \(\{v,w\}\in E_G\), and let \(u,z\in K_G(\mathbb F)\) be nonzero on their respective vertex blocks \(v,w\). If \(z\) is also nonzero at \(v\), or \(u\) at \(w\), the preceding argument gives a shared coordinate. Otherwise both vectors have edge-coordinate triples at \(\{v,w\}\) equal, up to sign, to their respective nonzero vertex triples by (13). Those two supports meet, again because both have size at least two. Thus (17) holds. \(\square\)

**Theorem 8 (exact optimized overlap width).** Let \(G\) be any nonempty finite simple graph and \(\mathbb F\) any field. Then
\[
\boxed{
\min_{B\text{ basis of }K_G(\mathbb F)}
\operatorname{tw}(H_B)
=2\operatorname{tw}(G)+1,
}
\tag{26}
\]
and
\[
\boxed{
\min_{B\text{ basis of }K_G(\mathbb F)}
\operatorname{pw}(H_B)
=2\operatorname{pw}(G)+1.
}
\tag{27}
\]

*Proof.* By Lemma 7, Theorem 5 gives \(G[K_2]\hookrightarrow H_B\) for every basis \(B\). Since treewidth and pathwidth are subgraph-monotone, Lemma 6 gives both lower bounds in (26)–(27).

For matching upper bounds, choose at each vertex the two zero-sum vectors
\[
a=(1,0,-1),\qquad b=(0,1,-1)
\tag{28}
\]
and extend them by (13) to full kernel vectors, with zero vertex triples elsewhere. These \(2|V|\) vectors form a basis by (12). The two vectors at one vertex intersect in a vertex coordinate; for an edge \(vw\), any of the four corresponding vector pairs intersect in an auxiliary edge coordinate; for nonadjacent distinct vertices the supports are disjoint. Therefore the resulting overlap graph is **exactly**
\[
H_B\cong G[K_2].
\tag{29}
\]
Equations (22)–(23) give equality in both bounds. \(\square\)

In particular,
\[
\min_B\operatorname{tw}(H_B(K_n))=2n-1,
\qquad
\min_B\operatorname{tw}(H_B(K_{n,n}))=2n+1,
\tag{30}
\]
and the special case \(K_{3,3}\) has optimized width seven.

### 4.1. Machine-checked equivalence over \(\mathbb F_3\)

For a finite graph \(H\), write \(\operatorname{TwLe}(H,k)\) when a tree decomposition of width at most \(k\) exists. The available Lean 4 development represents the \(\mathbb F_3\) case of Theorem 8 by the statement
\[
\boxed{
\left(
\begin{gathered}
\exists B\text{ a basis of }K_G(\mathbb F_3):\\
\operatorname{TwLe}(H_B,2k+1)
\end{gathered}
\right)
\iff
\operatorname{TwLe}(G,k)
}
\qquad(k\in\mathbb N).
\tag{31}
\]
Proof terms for the two directions and the equivalence are present in the available Lean source, with no unfilled proof placeholders or locally declared axioms. This paper does not claim that the compilation was rerun independently for the present manuscript. The more general all-field spanning-family embedding (18) is proved in the written mathematics above, rather than identified with the exact declaration in (31).

## 5. An algebraic refutation transfer

Over \(\mathbb F_2\), the exact-one relation on Boolean \(a,b,c\) is equivalently
\[
a+b+c+1=0,\qquad ab+ac+bc=0,
\tag{32}
\]
in the presence of \(x^2-x=0\) for each Boolean variable. Indeed the first equation forces odd Hamming weight, and the second excludes weight three.

For the graph-colouring encoding (8)–(9), substitute
\[
y_{\{u,v\},c}\longmapsto 1+x_{u,c}+x_{v,c}.
\tag{33}
\]
The parity equation of each edge clause becomes zero. Modulo the Boolean axioms, its quadratic equation becomes
\[
x_{u,c}x_{v,c}=0.
\tag{34}
\]
The vertex equations are unchanged.

**Proposition 9.** A Polynomial Calculus refutation of degree \(D\) of the characteristic-two exact-one system induces a Polynomial Calculus refutation of the standard graph three-colouring system of degree at most \(2D\).

*Proof.* Apply the degree-one substitution (33) to each line of the original derivation. Images of all initial equations are zero or consequences of the target graph-colouring and Boolean axioms of degree at most two. Addition of lines is preserved. Multiplication by a vertex variable remains multiplication by that variable; multiplication by an eliminated auxiliary variable becomes multiplication by an affine linear expression, which is reproduced using linear combinations and variable multiplications. The resulting maximum degree is at most twice the original degree. Since the constant polynomial \(1\) is fixed by substitution, the image derivation remains a refutation. \(\square\)

Consequently the linear Polynomial Calculus degree lower bounds for the graph families of Lauria and Nordström [3] transfer to the corresponding exact-one encodings:
\[
\deg_{\mathrm{PC}}(\text{exact-one encoding of }G)
=\Omega(|V(G)|)
\tag{35}
\]
for their specified family.

The result concerns the Polynomial Calculus proof system. It cannot be substituted for an unrestricted Boolean circuit lower bound. In particular, a family with large refutation degree can admit short proofs in stronger systems.

## 6. Computation models and exact simulation

For a Boolean decision or total search problem on an \(N\)-bit input, a deterministic one-pass algorithm may be represented by a sequence of update maps
\[
q_{t+1}=F_t(q_t,z_t),
\qquad
F_t:\{0,1\}^S\times\{0,1\}\longrightarrow\{0,1\}^S,
\quad 0\le t<N,
\tag{36}
\]
followed by an exact decoder \(D\). Denote the number of fan-in-two Boolean gates in an implementation of \(F_t\) by \(g_t\) and the complete decoder cost by \(g_D\). The total charged computation is
\[
\Gamma=\sum_{t=0}^{N-1}g_t+g_D.
\tag{37}
\]

**Lemma 10 (bounded-time transition simulation).** If each update of a fixed deterministic Turing-machine implementation uses at most \(U\) steps with at most \(S\) bits of work configuration, there is a fan-in-two Boolean circuit for that update of size polynomial in \(U,S\) and the input-length parameter. For the standard local machine tableau, the size may be taken \(O(US)\) up to fixed machine and encoding conventions.

*Proof.* Encode a work configuration on a Boolean array of length polynomial in \(S\). Each machine move is a local Boolean transformation of that array. Unrolling at most \(U\) moves yields \(U\) layers, each of cost \(O(S)\), plus fixed input and control circuitry. The resulting circuit computes the complete deterministic update for every possible encoded state and incoming input bit. \(\square\)

This lemma is about the specified bounded-time **Turing-machine** representation. The same numerical bound for an arbitrary random-access machine requires an independent simulation argument.

**Lemma 11 (exact staged unrolling).** A family of transitions (36), together with \(D\), yields a Boolean DAG computing the same total input-output relation with at most \(\Gamma\) gates. Exactly \(S\) state wires are carried across each boundary between consecutive stages.

*Proof.* Connect each stage's state outputs to the next stage's state inputs and attach \(D\) to the final state. Induction on \(t\) proves that the circuit state after stage \(t\) is the algorithm's state after reading the first \(t\) input bits. The circuit's gates are precisely those charged in (37), and only the \(S\) state bits persist between stages. \(\square\)

The bound in Lemma 11 is an **inter-stage cut** bound. It is not a statement about internal circuit-layer width, linearity of the update maps, or the complexity of replacing the computation with a spanning family of a linear space.

Both lemmas have also passed a separate review in the indicated narrow models: the Turing-machine tableau construction and the stage-boundary wire count. That review does not by itself establish a lower bound on \(\Gamma\).

## 7. A conditional implication for unrestricted staged computation

Fix \(m\in\mathbb N\) and \(N=2^m\). Let \(s=s(m)\ge m\) be time constructible and let \(A\in PH\). The total relation
\[
\mathrm{SearchMCSP}^{A}[s]
\tag{38}
\]
takes the length-\(N\) truth table of a Boolean function on \(m\) variables and outputs an \(A\)-oracle circuit of size at most \(s\) computing that table, if one exists, and otherwise correctly reports nonexistence. Allowing oracle gates in the circuit *to be output* does not provide the ordinary streaming solver with cost-free oracle calls.

Call a staged realisation **admissible** if it solves the entire total relation (38) for every length-\(N\) input, with all updates and the final decoder charged as in (37).

The following theorem is an implication between precisely quantified mathematical statements.

**Theorem 12 (conditional separation).** Assume that there exist \(s\) and \(A\in PH\) such that
\[
\boxed{
\begin{aligned}
&\forall c,d\in\mathbb N\
\exists m_0\ \forall m\ge m_0:\\[-2pt]
&\quad\neg\exists\text{ an admissible staged realisation }\mathcal C_m
\text{ with }
S(\mathcal C_m)\le s(m)^c\\
&\hspace{120pt}\text{and }
\Gamma(\mathcal C_m)\le2^m s(m)^d.
\end{aligned}}
\tag{39}
\]
Then
\[
\boxed{P\ne NP.}
\tag{40}
\]

*Proof.* Assume \(P=NP\). The polynomial hierarchy then collapses to \(P\). By the streaming construction and consequence of McKay, Murray and Williams [4, Theorems 1.2 and 1.3], the total relation (38), for every permitted \(s,A\), has a uniform deterministic one-pass streaming algorithm with polynomial-in-\(s\) workspace and worst-case per-symbol update time. The oracle questions in the published construction have length polynomial in \(s\); under \(P=NP\) they are answered by ordinary polynomial-time computation, with no oracle privilege for the resulting solver.

By Lemma 10, each update of this ordinary deterministic machine can be represented by a Boolean circuit of size polynomial in \(s\), since \(m\le s(m)\). The final circuit-producing computation is charged in the decoder, as is the output-work of the total search algorithm. For some fixed \(c,d\), this gives
\[
S(\mathcal C_m)\le s(m)^c,\qquad
\Gamma(\mathcal C_m)\le2^m s(m)^d
\tag{41}
\]
for every sufficiently large \(m\). Lemma 11 shows that the staged circuit computes exactly the total search relation, not merely its decision variant. This contradicts (39), so \(P\ne NP\). \(\square\)

The deduction from (39) to (40) is established. The assertion (39) is a **universal lower-bound premise** about all admissible staged realisations; it is not established by Lemmas 10–11. In particular, deriving (39) from the linear-algebraic theorem of Section 3 requires an additional theorem about the relation between arbitrary nonlinear circuits and the supports of vectors in a linear space.

## 8. Exact boundary between structure and general computation

The universal embedding theorem supplies a genuine lower bound:
\[
\forall B\text{ spanning }K_G(\mathbb F):
\quad
\operatorname{tw}(H_B)\ge2\operatorname{tw}(G)+1.
\tag{42}
\]
Its quantified object is a **spanning family of the fixed kernel**.

For contrast, the computation lower bound in Theorem 12 quantifies over **every admissible nonlinear staged circuit**, including arbitrary shared gates, time-dependent updates, state recodings, and computation performed in the final decoder. Neither the set of its states nor the complete Boolean DAG is, merely by definition, a spanning family of \(K_G(\mathbb F)\).

A structural derivation of the premise (39) would require a construction which, for every such circuit \(\mathcal C_m\), supplies a graph \(G_m\), a linear space \(K_m\) and a spanning family \(B_{\mathcal C_m}\) for which the conditions (15)–(17) hold and
\[
d_m\bigl(\operatorname{tw}(G_m)+1\bigr)-1
\le
\operatorname{tw}(H_{B_{\mathcal C_m}})
\le
\Psi(m,s,S(\mathcal C_m),\Gamma(\mathcal C_m)).
\tag{43}
\]
To force a contradiction, the upper bound on the right must be strictly smaller than the lower bound on the left throughout the forbidden polynomial-resource regime, with the necessary asymptotic quantifiers. The first inequality follows from Theorem 5 after the required linear representation has been constructed; the **construction and quantitative second inequality** are independent obligations.

Two elementary controls are decisive. For \(G=K_n\), the width in (30) grows, but every \(K_n\) for \(n\ge4\) contains the fixed non-three-colourable \(K_4\) subgraph, yielding a constant-size refutation of its colouring formula. For \(G=K_{n,n}\), the width also grows, although the graph is immediately three-colourable. Thus no bound on *general* computation follows from width alone.

There is a second quantifier distinction. A specific fixed formula has one truth value and therefore a constant-size decision circuit whose answer is hard-coded. Lower bounds relevant to complexity classes must range over the full decision family or over every admissible algorithm for a complete search relation; fixed-instance structure cannot replace this quantifier.

Accordingly, the mathematically valid chains are
\[
\boxed{
\begin{gathered}
\text{affine exact-one system}
\iff
\text{two-valued point of }\mathcal A_E,\\
K_G(\mathbb F)\cong T_{\mathbb F}^{V}
\Longrightarrow
G[K_2]\hookrightarrow H_B
\Longrightarrow
\min_B\operatorname{tw}(H_B)=2\operatorname{tw}(G)+1,\\
\text{bounded-time one-pass computation}
\Longrightarrow
\text{exact staged Boolean DAG},\\
\text{universal lower bound (39)}
\Longrightarrow
\text{no polynomial-resource one-pass solver}
\Longrightarrow
P\ne NP.
\end{gathered}}
\tag{44}
\]

The first three lines are justified in their respective models; the last line is a **proved conditional implication**. A proof that (39) follows from the preceding structural identity for every admissible nonlinear realisation is not supplied here.

## 9. Closing remark

The exact-one system admits an affine characterization, a field-independent universal support-overlap obstruction, and a sharp optimized treewidth formula. Those theorems constitute a self-contained mathematical result, with a machine-formalized three-element-field instance of the width equivalence. The separate streaming theorem permits a strong conclusion from an explicitly quantified general computation lower bound, and the deduction of that conclusion is complete. This article does not claim that the required universal lower bound has been established; nor does it identify the proved linear-representation obstruction with an unrestricted circuit lower bound without an additional theorem.

## References

[1] T. J. Schaefer, *The Complexity of Satisfiability Problems*, Proceedings of STOC, 1978, 216–226.

[2] B. Tonn, *Every Basis Sees the Blow-Up: A Universal Subgraph Theorem for Support-Overlap Graphs of a Colouring Kernel*, 2026, DOI: 10.5281/zenodo.24438918.

[3] M. Lauria and J. Nordström, *Graph Colouring Is Hard for Algorithms Based on Hilbert's Nullstellensatz and Gröbner Bases*, Proceedings of CCC, 2017, article 2, DOI: 10.4230/LIPIcs.CCC.2017.2.

[4] D. M. McKay, C. D. Murray and R. R. Williams, *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*, Proceedings of STOC, 2019, 104–117, DOI: 10.1145/3313276.3316396.

[5] R. Impagliazzo, P. Pudlák and J. Sgall, *Lower Bounds for the Polynomial Calculus and the Gröbner Basis Algorithm*, Computational Complexity 8 (1999), 127–144.
