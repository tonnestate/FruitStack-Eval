# Positive Exact-One Satisfiability: Algebraic Structure, Universal Basis Obstructions, and the Boundary of General Computation

**Björn Tonn**  
**22 November 2026 — Mathematical manuscript, version 0.6**

## Abstract

We study positive exact-one satisfiability through an affine relaxation over \(\mathbb F_3\), the homogeneous kernel of a graph-colouring encoding, and restricted algebraic proof systems. Satisfiability is equivalent to the existence of a two-valued point in the affine solution space. For the homogeneous colouring kernel \(K_G(\mathbb F)\), we prove over every field \(\mathbb F\) that the support-overlap graph of every spanning family contains the lexicographic product \(G[K_2]\). A canonical basis attains this embedding, giving the exact optimized width
\[
\min_{B\text{ basis of }K_G(\mathbb F)}
\operatorname{tw}(H_B)=2\operatorname{tw}(G)+1.
\]
A substitution from the characteristic-two XOR/carry encoding of exact-one clauses to the standard graph-colouring polynomials transfers Polynomial Calculus degree lower bounds. We isolate the precise model boundaries: high optimized overlap width does not imply large unrestricted Boolean circuit size, and large Polynomial Calculus degree does not imply hardness for stronger proof systems. We finally prove conditional implications from explicitly quantified—but unproved—general-circuit and online-circuit hypotheses to \(P\ne NP\). The structural results are unconditional; the computational lower-bound hypotheses are not proved.

**Keywords:** satisfiability; exact-one constraints; affine spaces; finite fields; graph colouring; support overlap; Hall's theorem; treewidth; Polynomial Calculus; circuit complexity.

---

## 1. The complete decision problem

For \(n\ge3\) put
\[
\mathcal T_n=\{\{i,j,k\}:1\le i<j<k\le n\},
\qquad M_n=\binom n3.
\]
An input \(y\in\{0,1\}^{M_n}\) selects a positive exact-one formula
\[
F_y=
\bigwedge_{\substack{e=\{i,j,k\}\in\mathcal T_n\\ y_e=1}}
[\,x_i+x_j+x_k=1\,],
\quad x\in\{0,1\}^n.
\tag{1}
\]
Define the Boolean decision function
\[
f_n(y)=1\iff F_y\text{ is satisfiable}.
\tag{2}
\]

The question is the complexity of the entire family \((f_n)\), not the constant truth value of one fixed unsatisfiable formula. Positive exact-one satisfiability is NP-complete [1].

Let \(\operatorname{CC}(g)\) denote the minimum number of gates in an unrestricted fan-in-two Boolean **DAG** computing \(g\), including arbitrary sharing of intermediate gates.

**Proposition 1.** The following bound would imply \(NP\not\subseteq P/poly\) and therefore \(P\ne NP\):
\[
\forall k\in\mathbb N\ \forall n_0\in\mathbb N\
\exists n\ge n_0:
\operatorname{CC}(f_n)>M_n^k.
\tag{3}
\]

**Proof.** If \(NP\subseteq P/poly\), the NP-complete language represented by (2) has circuits of size at most \(M_n^k\) for some fixed \(k\) and every sufficiently large \(n\), absorbing polynomial encoding overhead by increasing \(k\). This contradicts (3). Since \(P\subseteq P/poly\), the latter separation implies \(P\ne NP\). \(\square\)

Statement (3) has **not** been proved by any of the invariants below. It states one sufficient lower-bound target; a direct uniform lower bound could also separate \(P\) from \(NP\) without establishing it.

## 2. The affine exactness theorem

Let \(A_y\) be the incidence matrix of the selected clauses, viewed over \(\mathbb F_3\), and write
\[
\mathcal A_y=\{z\in\mathbb F_3^n:A_yz=\mathbf1\},
\qquad
K_y=\ker_{\mathbb F_3}A_y.
\tag{4}
\]
Each row has three ones, so
\[
A_y\mathbf1=\mathbf0\pmod3,
\qquad
z\in\mathcal A_y\implies z+t\mathbf1\in\mathcal A_y
\quad(t\in\mathbb F_3).
\tag{5}
\]
If \(\mathcal A_y\ne\varnothing\), Gaussian elimination gives \(z_0\in\mathcal A_y\), a basis matrix \(B\) of \(K_y\), and
\[
\mathcal A_y=\{z_0+B\lambda:\lambda\in\mathbb F_3^r\},
\qquad r=\dim K_y.
\tag{6}
\]

**Theorem 2 (two-value criterion).** For every positive exact-one formula,
\[
\boxed{
f_n(y)=1\iff
\exists z\in\mathcal A_y:
|\{z_1,\ldots,z_n\}|\le2.
}
\tag{7}
\]

**Proof.** A Boolean satisfying assignment belongs to \(\mathcal A_y\): among the possible sums \(0,1,2,3\) of three Boolean values, exactly \(1\) is congruent to \(1\pmod3\). Conversely, if the formula is empty it is satisfiable. Otherwise a constant vector cannot solve \(A_yz=\mathbf1\), since the sum of three equal field elements is zero. Any solution with at most two coordinate values therefore has exactly two. Each two-element subset of \(\mathbb F_3\) is a translate of \(\{0,1\}\). By (5) an appropriate translate of \(z\) is Boolean and still belongs to \(\mathcal A_y\). Each of its clause sums is then \(1\) over the integers. \(\square\)

**Corollary 3.** The following are equivalent:
\[
\begin{aligned}
&F_y\text{ is satisfiable};\\
&\mathcal A_y\cap\{0,1\}^n\ne\varnothing;\\
&\exists\lambda\in\mathbb F_3^r,\ t\in\mathbb F_3:
z_0+B\lambda\in\{t,t+1\}^n.
\end{aligned}
\tag{8}
\]

Thus Gaussian elimination solves the *affine feasibility* problem and returns a complete linear description (6), but the last condition in (8) is a separate nonlinear feasibility predicate. The exactness of (8) does not reduce the difficulty of the complete NP problem.

### 2.1. Independent rows in minimal blind obstructions

Call \(F_y\) **blind** if \(\mathcal A_y\ne\varnothing\) but \(f_n(y)=0\), and **minimal blind** if removing any clause makes it satisfiable.

**Proposition 4.** If a minimal blind formula has \(q\) clauses on its \(n'\) occurring variables, then
\[
\operatorname{rank}_{\mathbb F_3}(A_y)=q,
\qquad
q\le n'-1,
\qquad
\dim K_y=n'-q\ge1.
\tag{9}
\]

**Proof.** The affine system is consistent. If a selected row is linearly dependent on the others, its equation is a consequence of the remaining equations. Deleting the corresponding clause does not change \(\mathcal A_y\). Minimality supplies a Boolean solution to the smaller formula; because that solution lies in the unchanged affine space, it also satisfies the deleted clause, contradiction. Thus the rows are independent. By (5), the all-ones vector is a nonzero kernel element, so their rank is at most \(n'-1\). \(\square\)

The proved chain is
\[
\text{minimal blind obstruction}
\Longrightarrow \operatorname{rank}A_y=q
\Longrightarrow \dim K_y=n'-q\ge1.
\tag{10}
\]
It is a structural statement about an obstruction, not a lower bound on the cost of finding it.

## 3. Exact reduction from graph colouring

Let \(G=(V,E)\) be a nonempty finite simple graph and \(C=\{0,1,2\}\). Introduce Boolean variables \(x_{v,c}\) for \(v\in V,c\in C\), and slack variables \(z_{e,c}\) for \(e\in E,c\in C\). Consider
\[
\sum_{c\in C}x_{v,c}=1
\quad(v\in V),
\tag{11}
\]
\[
x_{u,c}+x_{v,c}+z_{\{u,v\},c}=1
\quad(\{u,v\}\in E,\ c\in C).
\tag{12}
\]

**Proposition 5.** The positive exact-one formula (11)–(12) is Boolean satisfiable exactly when \(G\) is properly 3-colourable. Over \(\mathbb F_3\) its affine relaxation is always nonempty.

**Proof.** The first equation chooses precisely one colour per vertex. A Boolean slack variable in the second equation exists exactly when its endpoints do not both choose the indicated colour. These constraints are equivalent to proper 3-colouring. Over \(\mathbb F_3\), the assignment \(x_{v,c}=0\), \(z_{e,c}=1\) satisfies all equations for every graph. \(\square\)

Over an arbitrary field \(\mathbb F\) let \(K_G(\mathbb F)\) be the homogeneous kernel of the same incidence matrix:
\[
K_G(\mathbb F)=
\left\{(x,z):
\begin{array}{ll}
\sum_c x_{v,c}=0 &(v\in V),\\
x_{u,c}+x_{v,c}+z_{\{u,v\},c}=0
&(\{u,v\}\in E,\ c\in C)
\end{array}
\right\}.
\tag{13}
\]
Put
\[
T_{\mathbb F}=\{(a_0,a_1,a_2)\in\mathbb F^3:
a_0+a_1+a_2=0\}.
\tag{14}
\]

**Lemma 6.**
\[
\boxed{
K_G(\mathbb F)\cong T_{\mathbb F}^{V},
\qquad
\dim K_G(\mathbb F)=2|V|.
}
\tag{15}
\]

**Proof.** Vertex triples are independently selectable elements of \(T_{\mathbb F}\). Every edge coordinate is then uniquely determined by \(z_{\{u,v\},c}=-x_{u,c}-x_{v,c}\). The zero-sum subspace of \(\mathbb F^3\) has dimension two. \(\square\)

This establishes two distinct implications:
\[
G\text{ 3-colourable}\iff
\text{(11)–(12) Boolean satisfiable},
\tag{16}
\]
\[
K_G(\mathbb F)\cong T_{\mathbb F}^V,
\qquad\dim K_G=2|V|.
\tag{17}
\]
Equation (17) concerns a homogeneous *linear representation*. It does not, by itself, decide (16).

## 4. Universal subgraph embedding for all spanning families

Let \(K\subseteq\mathbb F^I\) with \(I=\bigsqcup_{v\in V}I_v\). For a finite indexed spanning family \(B=(b_j)_{j\in J}\) define the support-overlap graph \(H_B\) by
\[
jk\in E(H_B)
\iff
j\ne k\ \land\
\operatorname{supp}(b_j)\cap\operatorname{supp}(b_k)\ne\varnothing.
\tag{18}
\]

Assume, for a graph \(G=(V,E)\) and integer \(d\ge1\),
\[
\dim\pi_X(K)\ge d|X|\quad(X\subseteq V),
\tag{R}
\]
\[
u|_{I_v}\ne0,\ w|_{I_v}\ne0
\implies \operatorname{supp}(u)\cap\operatorname{supp}(w)\ne\varnothing,
\tag{L}
\]
\[
vw\in E(G),\ u|_{I_v}\ne0,\ w|_{I_w}\ne0
\implies\operatorname{supp}(u)\cap\operatorname{supp}(w)\ne\varnothing.
\tag{E}
\]
Here \(\pi_X\) projects onto the coordinate blocks indexed by \(X\).

**Theorem 7 (Hall embedding).** Under (R), (L), (E), every finite spanning family \(B\) of \(K\) satisfies
\[
\boxed{G[K_d]\hookrightarrow H_B.}
\tag{19}
\]
If \(\dim K=d|V|\) and \(B\) is a basis, the embedded copy is spanning.

**Proof.** Put \(S_v=\{j:b_j|_{I_v}\ne0\}\). By (L), \(S_v\) is a clique; by (E), all distinct pairs from \(S_v\) and \(S_w\) are adjacent when \(vw\in E(G)\). The vectors \(\pi_X(b_j)\), \(j\in\bigcup_{v\in X}S_v\), span \(\pi_X(K)\), hence
\[
\left|\bigcup_{v\in X}S_v\right|
\ge\dim\pi_X(K)\ge d|X|.
\tag{20}
\]
Replace each vertex \(v\) of \(G\) by \(d\) copies, each adjacent in a bipartite matching instance to all indices in \(S_v\). Any set of copies projecting to \(X\) has size at most \(d|X|\) and neighbourhood of size at least \(d|X|\). Hall's theorem gives an injection
\[
\iota:V\times[d]\hookrightarrow J,\qquad
\iota(v,i)\in S_v.
\tag{21}
\]
The clique and edge-intersection properties make \(\iota\) an edge-preserving injection of \(G[K_d]\) into \(H_B\). If \(|J|=\dim K=d|V|\), it is bijective. \(\square\)

### 4.1. Exact graph-width identity

**Lemma 8.** For any nonempty finite graph \(G\) and \(d\ge1\),
\[
\operatorname{tw}(G[K_d])
=d(\operatorname{tw}(G)+1)-1,
\tag{22}
\]
and
\[
\operatorname{pw}(G[K_d])
=d(\operatorname{pw}(G)+1)-1.
\tag{23}
\]

**Proof.** Replacing each vertex in each decomposition bag by its \(d\) copies gives the upper bounds. Conversely, given a tree decomposition \((T,\beta)\) of \(G[K_d]\), write \(Q_v=\{v\}\times[d]\) and define \(\gamma(t)=\{v:Q_v\subseteq\beta(t)\}\). The nodes whose bags contain \(Q_v\) form a nonempty connected subtree, by clique containment. If \(vw\in E(G)\), the union \(Q_v\cup Q_w\) is a clique, so a bag contains both. Thus \((T,\gamma)\) is a tree decomposition of \(G\). Since the \(Q_v\) are disjoint, \(d|\gamma(t)|\le|\beta(t)|\), giving the lower bound in (22). The construction keeps the same underlying path for path decompositions. \(\square\)

**Theorem 9 (optimized colouring-kernel width).** For every field \(\mathbb F\) and nonempty finite simple graph \(G\),
\[
\boxed{
\min_{B\text{ basis of }K_G(\mathbb F)}
\operatorname{tw}(H_B)
=2\operatorname{tw}(G)+1,
}
\tag{24}
\]
\[
\boxed{
\min_{B\text{ basis of }K_G(\mathbb F)}
\operatorname{pw}(H_B)
=2\operatorname{pw}(G)+1.
}
\tag{25}
\]

**Proof.** Condition (R) with \(d=2\) follows from (15). Each nonzero zero-sum triple in \(T_{\mathbb F}\) has support of size at least two. Two such supports intersect, proving (L). For (E), consider two kernel vectors nonzero on the vertex blocks at endpoints \(v,w\) of an edge. If either is nonzero on the other's block, (L) gives intersection. Otherwise their edge-coordinate triples are the negatives of those two nonzero zero-sum triples; their supports intersect. Thus Theorem 7 yields \(G[K_2]\hookrightarrow H_B\) for every basis, giving the lower bounds by Lemma 8.

For the upper bounds use the two basis vectors per vertex with vertex triples
\[
(1,0,-1),\qquad(0,1,-1)
\tag{26}
\]
and all other vertex triples zero; the auxiliary coordinates are determined by (13). The two vectors at one vertex overlap. Across each edge all four pairs of corresponding vectors overlap at its slack coordinates. Vectors at nonadjacent vertices have disjoint supports. Consequently the canonical basis has \(H_B\cong G[K_2]\), attaining both lower bounds. \(\square\)

The complete proved structural chain is
\[
\begin{gathered}
K_G(\mathbb F)\cong T_{\mathbb F}^{V}\\
\Downarrow\ \text{projection rank and support intersection}\\
G[K_2]\hookrightarrow H_B
\qquad(\forall B\text{ spanning }K_G)\\
\Downarrow\ \text{subgraph monotonicity}\\
\operatorname{tw}(H_B)\ge2\operatorname{tw}(G)+1\\
\Downarrow\ \text{canonical basis}\\
\min_B\operatorname{tw}(H_B)=2\operatorname{tw}(G)+1 .
\end{gathered}
\tag{27}
\]

For the established test families,
\[
\min_B\operatorname{tw}(H_B(K_n))=2n-1,
\quad
\min_B\operatorname{tw}(H_B(K_{n,n}))=2n+1,
\tag{28}
\]
and
\[
\min_B\operatorname{tw}(H_B(K_{3,3}))=7.
\tag{29}
\]

**Proposition 10 (colour-count boundary).** For \(q\ge4\), the direct analogue \(G[K_{q-1}]\hookrightarrow H_B\) is false for the \(q\)-colour zero-sum kernel, even for \(G=K_1\).

**Proof.** For one vertex the kernel is \(T_q=\{a\in\mathbb F^q:\sum_i a_i=0\}\). The basis \(e_1-e_2,e_2-e_3,\ldots,e_{q-1}-e_q\) has support-overlap graph \(P_{q-1}\), which is not \(K_{q-1}\) when \(q\ge4\). \(\square\)

Theorems 7 and 9 are paper proofs of structural statements. They do not assert a gate lower bound for arbitrary nonlinear computation. The separately reported Lean formalization concerns an \(\mathbb F_3\) width identity, not the general-field theorem in the form stated above.

## 5. Algebraic proof transfer and its exact boundary

Over \(\mathbb F_2\), for Boolean variables \(a,b,c\), the exact-one relation is equivalent to
\[
a+b+c+1=0,
\qquad
ab+ac+bc=0,
\tag{30}
\]
with Boolean axioms \(x_i^2-x_i=0\).

**Lemma 11.** Equations (30) hold simultaneously exactly when one of \(a,b,c\) is \(1\).

**Proof.** The first equation selects odd Hamming weights \(1\) and \(3\); the second excludes weight \(3\). \(\square\)

For the graph-colouring encoding (11)–(12), substitute
\[
z_{\{u,v\},c}\longmapsto
1+x_{u,c}+x_{v,c}.
\tag{31}
\]
Under this ring homomorphism the edge parity axiom vanishes, while the carry axiom becomes
\[
x_{u,c}x_{v,c}=0\pmod{\{x_i^2-x_i\}}.
\tag{32}
\]
The vertex exact-one axioms remain the usual graph-colouring axioms.

**Proposition 12 (degree-preserving refutation transfer).** A degree-\(D\) Polynomial Calculus refutation of the positive exact-one XOR/carry system associated with \(G\) induces a Polynomial Calculus refutation of its standard 3-colouring encoding of degree at most \(2D\).

**Proof.** The substitution (31) has degree one. Each source axiom maps to zero or a bounded-degree combination of target colouring axioms and Boolean axioms; this is checked by (30)–(32). Addition of source derivation lines maps to addition. Multiplication by a vertex variable stays multiplication by that variable; multiplication by an auxiliary variable becomes multiplication by an affine-linear polynomial and is implemented by additions and at most two variable-multiplication steps. Induction over the source derivation bounds the image-line degrees by \(2D\) and maps the final line \(1\) to \(1\). \(\square\)

The bounded-degree non-3-colourable graph family of Lauria and Nordström [2] has graph-colouring Polynomial Calculus degree \(\Omega(|V(G)|)\). By Proposition 12,
\[
\deg_{\mathrm{PC}}(\text{positive exact-one XOR/carry system})
=\Omega(|V(G)|)
\tag{33}
\]
for the corresponding family. Standard degree–size inequalities [3] then yield large refutations in that **specified proof system**.

The same graph family admits polynomial-length cutting-planes refutations [2]. Therefore
\[
\boxed{
\text{large Polynomial Calculus degree}
\not\Longrightarrow
\text{large unrestricted proof complexity}.
}
\tag{34}
\]
A lower bound for unrestricted Boolean circuits does not follow without an additional theorem efficiently translating *every* correct algorithm or circuit into the restricted proof system. No such theorem is established here.

## 6. Why the structural width is not a computation lower bound

Theorems 7 and 9 quantify over bases or spanning families of a **fixed linear kernel**. They do not quantify over arbitrary decision circuits for the full function \(f_n\).

For \(G=K_n\), \(n\ge4\), (28) gives
\[
\min_B\operatorname{tw}(H_B)=2n-1.
\tag{35}
\]
Nevertheless the corresponding non-3-colourability formula contains the fixed unsatisfiable \(K_4\) subformula, so a constant-size Resolution refutation works for every \(n\). For \(G=K_{n,n}\), (28) grows linearly although the graph is obviously 3-colourable.

Thus an unbounded function \(h\) cannot satisfy
\[
\mathrm{ResSize}(\Phi_G)\ge
h\!\left(\min_B\operatorname{tw}(H_B)\right)
\quad\text{for all non-3-colourable }G.
\tag{36}
\]
This does **not** refute the structural theorem. It refutes the unqualified inference from optimized basis overlap to general computation.

A second distinction is the quantifier over inputs. The satisfiability of one fixed graph formula is a constant truth value, computable by a constant circuit when its answer is hard-wired. The function \(f_n\) instead accepts **all** clause selectors and is NP-complete.

### 6.1. The required missing theorem, expressed mathematically

An attempted structural-to-circuit implication would require a graph family \(G_n\) and, for **every** general Boolean DAG \(C\) computing \(f_n\), a *semantically justified* construction of a spanning family \(B_{C,n}\subseteq K_{G_n}(\mathbb F)\) with
\[
\operatorname{tw}(H_{B_{C,n}})\le Q(n,|C|),
\tag{37}
\]
and a quantitative separation
\[
\forall k\ \forall n_0\ \exists n\ge n_0:
Q(n,M_n^k)<2\operatorname{tw}(G_n)+1.
\tag{38}
\]

Here \(Q(n,S)\) may be replaced by a nondecreasing upper envelope in \(S\). The construction must allow every nonlinear state representation, shared intermediate gates, reordering, and computations deferred to an output stage. Merely choosing an arbitrary large-width representation of a cheap computation would not establish (37).

**Conditional Proposition 13.** If (37) and (38) are proved for the full family \((f_n)\), then \(NP\not\subseteq P/poly\), hence \(P\ne NP\).

**Proof.** Suppose a fixed polynomial bound \(|C_n|\le M_n^k\) holds for all sufficiently large \(n\). By Theorem 9 and (37),
\[
2\operatorname{tw}(G_n)+1
\le \operatorname{tw}(H_{B_{C_n,n}})
\le Q(n,|C_n|)
\le Q(n,M_n^k).
\]
Choose arbitrarily large \(n\) from (38). The inequality becomes strict in the opposite direction, contradiction. Apply Proposition 1. \(\square\)

**Status:** The deduction in Proposition 13 is proved. Its hypotheses (37) and (38), especially the *general nonlinear circuit-to-linear spanning-family construction* (37), are not proved by Theorem 7, Theorem 9, or any proof supplied here. This is the exact point at which the structural chain stops.

## 7. A mathematically separate streaming implication

A second sufficient route uses exact circuit synthesis from an \(N=2^m\)-bit truth table. It does **not** follow from the colouring-kernel chain.

Fix \(s=s(m)\ge m\) time constructible and an oracle language \(A\in PH\). The total search problem \(\mathrm{SearchMCSP}^{A}[s]\) asks for an \(A\)-oracle circuit of size at most \(s\) computing the given truth table, or a correct report that no such circuit exists. Allowing oracle gates in the *output circuit* does not grant unit-cost oracle operations to the ordinary streaming algorithm.

An exact deterministic one-pass Boolean realisation has an \(S\)-bit state, update circuits
\[
F_t:\{0,1\}^S\times\{0,1\}\longrightarrow\{0,1\}^S
\quad(0\le t<N),
\tag{39}
\]
and an output circuit \(D\). Its gate cost is
\[
\Gamma=\sum_{t=0}^{N-1}\operatorname{CC}(F_t)
+\operatorname{CC}(D).
\tag{40}
\]

**Lemma 14 (unrolling).** Such a staged realisation yields a Boolean DAG computing the same total search relation with at most \(\Gamma\) gates and at most \(S\) persistent state wires across every **input-time boundary**.

**Proof.** Connect the state outputs of stage \(t\) to the state inputs of stage \(t+1\) and attach \(D\) at the end. An induction on the number of consumed input bits verifies the state at every boundary. The gate count is bounded by the sum of the stage and decoder counts. The only persistent wires between consecutive stages are the \(S\) state wires. \(\square\)

These are **online state-cut** bounds, not bounds on the internal layer width of each stage and not a linear-space embedding.

McKay, Murray and Williams [4, Theorem 1.3] prove the following conditional implication for appropriate parameters:
\[
\begin{gathered}
\exists\,s,\ A\in PH:\ 
\mathrm{SearchMCSP}^{A}[s]
\text{ has no deterministic one-pass algorithm}\\
\text{with both }\operatorname{poly}(s)\text{ space and }
\operatorname{poly}(s)\text{ worst-case update time}\\
\Longrightarrow P\ne NP.
\end{gathered}
\tag{41}
\]

A **stronger sufficient assumption** is that, for some such \(s,A\),
\[
\forall c,d\in\mathbb N\
\exists m_0\ \forall m\ge m_0:
\quad\text{no exact staged realisation satisfies }
\begin{cases}
S\le s(m)^c,\\
\Gamma\le2^m s(m)^d.
\end{cases}
\tag{42}
\]

**Conditional Proposition 15.** Under (42), \(P\ne NP\).

**Proof.** Under \(P=NP\), the algorithm construction behind [4, Theorem 1.3] provides an ordinary deterministic one-pass algorithm with memory and worst-case update time polynomial in \(s\). A bounded-time discrete update on polynomially many state bits can be compiled into a Boolean circuit of size polynomial in the time, space and \(m\), with output computation likewise charged. As \(m\le s(m)\), the total staged circuit has \(S\le s(m)^c\) and \(\Gamma\le2^m s(m)^d\) for suitable fixed \(c,d\) and all sufficiently large \(m\). This contradicts (42). \(\square\)

The asymptotic lower-bound assumption (42) is **not proved**. It is also stronger than merely excluding **uniform** streaming algorithms: its quantifier ranges over nonuniform staged realisations. The reverse implication from the streaming lower bound to (42) is not established.

There is no known deduction here of the form
\[
\min_B\operatorname{tw}(H_B(K_G))\text{ large}
\Longrightarrow
\text{the general online-circuit bound (42)}.
\tag{43}
\]
Any such deduction requires a mathematical map from **arbitrary nonlinear online circuits** to the linear kernels in Section 4, with a quantitative guarantee resistant to gate sharing, recoding and deferred decoding.

## 8. Conclusions: the complete implication diagram

The actual mathematical chains are:

**Exact affine decision equivalence**
\[
F_y\text{ satisfiable}
\iff
\mathcal A_y\cap\{0,1\}^n\ne\varnothing
\iff
\exists\lambda,t:\ z_0+B\lambda\in\{t,t+1\}^n.
\tag{44}
\]

**Unconditional support-overlap theorem**
\[
K_G(\mathbb F)\cong T_{\mathbb F}^V
\Longrightarrow
G[K_2]\hookrightarrow H_B
\Longrightarrow
\min_B\operatorname{tw}(H_B)=2\operatorname{tw}(G)+1.
\tag{45}
\]

**Restricted algebraic hardness**
\[
\deg_{\rm PC}(\text{3-colouring equations})=\Omega(|V|)
\Longrightarrow
\deg_{\rm PC}(\text{positive exact-one XOR/carry})=\Omega(|V|).
\tag{46}
\]

**Unproved structural-to-general-circuit transfer**
\[
\underbrace{(37)\land(38)}_{\text{not established}}
\Longrightarrow
\operatorname{CC}(f_n)\text{ superpolynomial}
\Longrightarrow
P\ne NP.
\tag{47}
\]

**Separate unproved online-circuit premise with a published endpoint**
\[
\underbrace{(42)}_{\text{not established}}
\Longrightarrow
\underbrace{\text{streaming lower bound}}_{\text{published implication (41)}}
\Longrightarrow P\ne NP.
\tag{48}
\]

The proofs of (44)–(46) hold in their **specified mathematical models**. In (47), the deduction from the missing premises is proved but the premises are not. In (48), the final transfer is a published result but the antecedent is not proved. The two conditional routes are not shown to be equivalent.

No claim that \(P\ne NP\) has been proved is made. The contribution is the exact algebraic and structural theorem chain, together with a logically explicit boundary at which a theorem about **all general computations** is still required.

## References

[1] T. J. Schaefer, “The Complexity of Satisfiability Problems,” *STOC*, 1978, 216–226.

[2] M. Lauria and J. Nordström, “Graph Colouring Is Hard for Algorithms Based on Hilbert's Nullstellensatz and Gröbner Bases,” *CCC*, 2017, article 2.

[3] R. Impagliazzo, P. Pudlák and J. Sgall, “Lower Bounds for the Polynomial Calculus and the Gröbner Basis Algorithm,” *Computational Complexity* **8** (1999), 127–144.

[4] D. M. McKay, C. D. Murray and R. R. Williams, “Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes,” *STOC*, 2019, DOI 10.1145/3313276.3316396.

[5] P. Hliněný and G. Whittle, “Matroid Tree-Width,” *European Journal of Combinatorics* **27** (2006), 1117–1128.
