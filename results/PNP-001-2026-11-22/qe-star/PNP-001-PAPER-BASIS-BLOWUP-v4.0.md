# Owner paper: B. Tonn, Every Basis Sees the Blow-Up, v4.0, 2026-11-22, DOI 10.5281/zenodo.24438918 (text extract; PDF /root/fruits/research/PNP-001/theory/basis-blowup/). SOURCE TEXT, read-only.

                   EVERY BASIS SEES THE BLOW-UP:
               A UNIVERSAL SUBGRAPH THEOREM FOR
          SUPPORT-OVERLAP GRAPHS OF A COLOURING KERNEL

                                               BJÖRN TONN


        Abstract. Let G = (V, E) be a finite nonempty simple graph and F a field. The positive
        one-in-three encoding of the 3-colourability of G has a coefficient matrix whose homogeneous
        kernel KG (F) has dimension 2|V |. For a finite spanning family B of KG (F), the support-overlap
        graph HB has the members of B as vertices, two of them adjacent when their supports intersect.
        We prove that for every field and every spanning family, HB contains the lexicographic product
        G[K2 ] as a subgraph, and as a spanning subgraph when B is a basis. A canonical basis attains
        HB ∼= G[K2 ], so it minimises every subgraph-monotone graph parameter over all bases at once.
        In particular,
                     min tw(HB ) = 2 tw(G) + 1       and     min pw(HB ) = 2 pw(G) + 1.
                       B                                       B

        The proof rests on three properties — full rank of local projections, intersection of supports
        inside a vertex block, and intersection across adjacent blocks — which we isolate in an abstract
        embedding theorem. We show that the direct analogue for q ≥ 4 colours fails already for a single
        vertex, and that unbounded overlap treewidth alone does not force long Resolution refutations.
        The treewidth identity over F3 has been formalised in Lean 4; the subgraph theorem and the
        extension to all fields are proved on paper.




                                            1. Introduction
   A linear space has many bases, and their support patterns can differ widely. One basis may
have supports that overlap only locally, while another basis of the same space mixes distant
coordinates. Whenever the cost of a procedure depends on how the vectors of a chosen basis
overlap, it is natural to ask how much a change of basis can help.
   We answer this question completely for one concrete family of spaces. Starting from a graph
G, we take the standard encoding of 3-colourability by positive one-in-three constraints, pass
to the coefficient matrix of these constraints, and consider its homogeneous kernel KG (F) over
a field F. For a spanning family B of this kernel, the support-overlap graph HB records which
pairs of members share a nonzero coordinate.
   The kernel has an obvious basis with two vectors per vertex of G. Its overlap graph is the
lexicographic product G[K2 ], obtained by replacing every vertex by an edge and every edge by a
complete bipartite join. Our main result says that this graph cannot be avoided.
Main Theorem. For every field F and every finite spanning family B of KG (F), the graph
G[K2 ] is isomorphic to a subgraph of HB . If B is a basis, it is isomorphic to a spanning subgraph
of HB .




     Date: 22 November 2026.
     2020 Mathematics Subject Classification. 05C75, 05C83; 15A03, 94B05.
     Key words and phrases. support-overlap graph, lexicographic product, treewidth, pathwidth, Hall’s theorem,
linear codes, graph colouring, formal verification.
     Preprint, version 4. doi:10.5281/zenodo.24438918.
                                                       1
 2                                         BJÖRN TONN

   Consequently no change of basis improves any graph parameter that is monotone under taking
 subgraphs. Together with a canonical basis that attains HB ∼
                                                            = G[K2 ], this yields for every field
(1.1)             min tw(HB ) = 2 tw(G) + 1,       min pw(HB ) = 2 pw(G) + 1,
                   B                                B
(1.2)                              min|E(HB )| = |V | + 4|E|,
                                     B
where the minima range over all bases of KG (F).
   The proof uses three properties of the kernel and nothing else.
 (1) Rank. The projection of the kernel to the coordinates of any set X of vertices has rank
     2|X|.
 (2) Local intersection. Two kernel vectors that are both nonzero on the block of one vertex
     have intersecting supports.
 (3) Edge intersection. Two kernel vectors that are nonzero on the blocks of two adjacent vertices
     have intersecting supports.
Property (1) yields a doubled Hall condition, properties (2) and (3) yield cliques, and Hall’s
marriage theorem assembles the embedding. Section 4 states this as an abstract theorem for
linear spaces with a block structure indexed by a graph.
 1.1. Contributions.
    • An abstract embedding theorem (Theorem 4.1): under the three properties above with rank
      parameter d, the overlap graph of every spanning family contains G[Kd ].
    • The Main Theorem for the colouring kernel over every field (Theorem 5.4), with a canonical
      basis attaining equality (Proposition 5.3).
    • Simultaneous optimality of the canonical basis for all subgraph-monotone parameters, with
      explicit values for treewidth, pathwidth, number of edges, clique number and chromatic
      number (Section 6).
    • Two sharp limits: the direct analogue for q ≥ 4 colours is false (Proposition 5.5), and no
      unbounded function of the minimum overlap treewidth lower-bounds Resolution refutation
      size on this family (Proposition 6.5).
1.2. What is not claimed. The treewidth and pathwidth of G[Kd ] are known; we include
a short proof for completeness and claim no novelty for it. We have not found the subgraph
theorem, or an abstract statement implying it, in the literature on matroid width, on graphical
realisations of codes, or on transversal theory, but our search was not exhaustive (Section 9).
The paper makes no claim about circuit complexity, about strong proof systems, or about the
complexity of deciding 3-colourability.

                                         2. Preliminaries
   All graphs are finite, undirected and simple. For a graph J we write V (J) and E(J) for its
vertex and edge sets. A clique is a set of pairwise adjacent vertices. A graph J ′ is a subgraph of
J, written J ′ ⊆ J up to isomorphism, if there is an injection V (J ′ ) → V (J) that maps edges
to edges; non-edges need not be preserved. A graph parameter p is subgraph monotone if it is
invariant under isomorphism and p(J ′ ) ≤ p(J) whenever J ′ is a subgraph of J.
 2.1. Tree and path decompositions. A tree decomposition of J is a pair (T, β), where T is a
 tree and β assigns to each node t of T a bag β(t) ⊆ V (J), such that
(T1) every vertex of J lies in some bag;
(T2) for every edge ab of J some bag contains both a and b;
(T3) for every vertex a the nodes t with a ∈ β(t) induce a connected subtree of T .
                                 EVERY BASIS SEES THE BLOW-UP                                       3

Its width is maxt |β(t)| − 1, and the treewidth tw(J) is the least width of a tree decomposition
of J [12]. A path decomposition is a tree decomposition whose tree is a path; the pathwidth
pw(J) is defined accordingly. Both parameters are subgraph monotone. We use the following
standard fact; see [1, Ch. 12].
Lemma 2.1 (Clique containment). Let (T, β) be a tree decomposition of J and let Q be a
nonempty clique of J. Then {t : Q ⊆ β(t)} is nonempty and induces a connected subtree of T .
Proof. For a ∈ Q let Ta be the subtree of nodes whose bag contains a. Any two of these subtrees
intersect, because the corresponding vertices are adjacent and some bag contains both. Pairwise
intersecting subtrees of a tree have a common node (the Helly property), and an intersection of
subtrees of a tree is connected.                                                             □
2.2. The clique blow-up. For an integer d ≥ 1, the lexicographic product G[Kd ] has vertex set
V × {1, . . . , d}; distinct vertices (u, a) and (v, b) are adjacent if u = v or uv ∈ E. Every vertex
of G is thus replaced by a clique of size d and every edge by a complete join.
Lemma 2.2 (Width of the blow-up). For every nonempty graph G and every d ≥ 1,
                                                                               
            tw G[Kd ] = d tw(G) + 1 − 1        and    pw G[Kd ] = d pw(G) + 1 − 1.
   Identities of this kind are known. Gurski and Weishaupt [2] survey the behaviour of treewidth
and pathwidth under substitution and graph products, and Lin [9, Lemma 3.2] states tw(H)+1 =
q(tw(G) + 1) + r for H = G[Kq ] ∨ Kr under the additional hypothesis that the tree-chromatic
number of G equals its clique number. The elementary argument below needs no such hypothesis;
it is also the argument that has been formalised (Section 8).
Proof. Upper bound. Given a decomposition (T, β) of G of width k, replace each bag by
β(t) × {1, . . . , d}. Axioms (T1)–(T3) are inherited, and every bag has at most d(k + 1) elements.
  Lower bound. Let (T, β) be a decomposition of G[Kd ] of width w. Put Qv = {v} × {1, . . . , d}
and
                                     γ(t) = {v ∈ V : Qv ⊆ β(t)}.
Each Qv is a clique, so by Lemma 2.1 the nodes t with v ∈ γ(t) form a nonempty connected
subtree. For uv ∈ E the set Qu ∪ Qv is a clique, so some bag contains it, and that bag’s γ
contains u and v. Hence (T, γ) is a tree decomposition of G on the same tree. The sets Qv
are disjoint, so d |γ(t)| ≤ |β(t)| ≤ w + 1, which gives tw(G) + 1 ≤ (w + 1)/d. Since the tree is
unchanged, the same argument applies to path decompositions.                                    □
2.3. Hall’s theorem. We use Hall’s theorem [3] in the following form. Let (Sv )v∈V be a finite
family of finite sets and d ≥ 1. There are pairwise disjoint sets Av ⊆ Sv with |Av | = d for all v if
and only if
                                 [
(2.1)                                 Sv ≥ d |X|       for all X ⊆ V.
                                v∈X
This follows from the usual statement applied to the bipartite graph in which every v is replaced
by d copies.

                    3. The colouring kernel and its overlap graphs
                                                         ̸ ∅; connectedness is not assumed.
  Throughout, G = (V, E) is a finite simple graph with V =
Let C = {0, 1, 2} be the set of colours and F a field.
4                                                 BJÖRN TONN

3.1. The one-in-three encoding. Introduce a variable xv,c for each v ∈ V and c ∈ C, and a
slack variable ye,c for each e ∈ E and c ∈ C. The formula F (G) consists of the positive exact-one
constraints
                                                                                                      
    EXACT1(xv,0 , xv,1 , xv,2 )    (v ∈ V ),       EXACT1(xu,c , xv,c , ye,c )   e = {u, v} ∈ E, c ∈ C .
A Boolean assignment satisfies F (G) exactly when the variables xv,c describe a proper 3-colouring
of G; the slack variables are then determined. Encodings of this kind are standard in reductions
to positive one-in-three satisfiability [13]. Satisfiability plays no role in what follows; the encoding
only fixes the coefficient matrix.
3.2. The homogeneous kernel. Let IG = (V × C) ⊔ (E × C) be the coordinate set. The
colouring kernel is
                         (                                                                  )
                                                                 (v ∈ V ),
                                          P
                                   IG         c∈C zv,c = 0
(3.1)         KG (F) =       z∈F        :                                               .
                                          zu,c + zv,c + ze,c = 0 e = {u, v} ∈ E, c ∈ C
These are the constraint equations with right-hand side 0 instead of 1. The kernel is a linear
space whether or not G is 3-colourable.
  Let TF = {(a0 , a1 , a2 ) ∈ F3 : a0 + a1 + a2 = 0}, a space of dimension 2. For z ∈ KG (F) and
v ∈ V write z|v = (zv,0 , zv,1 , zv,2 ) ∈ TF . The vertex triples can be prescribed independently, and
the edge coordinates are then forced by (3.1). Hence restriction gives an isomorphism
                             ∼
                             =
(3.2)            KG (F) −−→ TFV ,             z 7−→ (z|v )v∈V ,     so   dim KG (F) = 2|V |.
3.3. Overlap graphs. The support of z ∈ FI is supp(z) = {i ∈ I : zi ̸= 0}.
Definition 3.1. Let K ⊆ FI be a subspace and B = (bj )j∈J a finite indexed family of vectors of K
with span{bj : j ∈ J} = K; dependent and zero members are allowed. The support-overlap graph
HB has vertex set J, and distinct j, k ∈ J are adjacent if and only if supp(bj ) ∩ supp(bk ) ̸= ∅.
  The graph HB depends on the coordinate system of FI ; it is not an invariant of K as an
abstract vector space.

                                  4. An abstract embedding theorem
Setting. Let G = (V, E) be a finite graph, F a field, I a finite set and K ⊆ FI a subspace.
For every v ∈ V let Iv ⊆ I be a set of coordinates, the block of v. For z ∈ K write z|v for the
restriction of z to Iv , and for X ⊆ V let πX : K → v∈X FIv be the joint restriction. Fix an
                                                             Q

integer d ≥ 1 and consider the following conditions.
  (R) Rank. rank πX ≥ d |X| for every X ⊆ V .
  (L) Local intersection. If z, z ′ ∈ K and z|v ̸= 0 ̸= z ′ |v for some v ∈ V , then supp(z)∩supp(z ′ ) ̸=
       ∅.
  (E) Edge intersection. If z, z ′ ∈ K, uv ∈ E, z|u ̸= 0 and z ′ |v ̸= 0, then supp(z) ∩ supp(z ′ ) ̸= ∅.
Theorem 4.1 (Abstract embedding). Assume (R), (L) and (E). Then for every finite spanning
family B = (bj )j∈J of K there is an injection
                                           ι : V × {1, . . . , d} ,→ J
that maps every edge of G[Kd ] to an edge of HB . In particular G[Kd ] is isomorphic to a subgraph
of HB . If dim K = d|V | and B is a basis, then ι is a bijection and the copy of G[Kd ] is spanning.
Proof. For v ∈ V let Sv = {j ∈ J : bj |v ̸= 0}.
   Cliques. By (L), any two distinct indices in Sv are adjacent in HB . By (E), for uv ∈ E every
j ∈ Su is adjacent to every k ∈ Sv with k = ̸ j. Hence Sv is a clique for every v, and Su ∪ Sv is a
clique for every edge uv.
                                     EVERY BASIS SEES THE BLOW-UP                                            5

  Hall condition. Let X ⊆ V . Since B spans K, the vectors πX (bj ) span the image of πX ,
which has dimension at least d|X| by (R). If j ∈
                                                   S
                                                 / v∈X Sv , then πX (bj ) = 0. Hence at least d|X|
              S
indices lie in v∈X Sv , which is condition (2.1).
  Matching. By Section 2.3 there are pairwise disjoint sets Av ⊆ Sv with |Av | = d. Let ι(v, ·)
enumerate Av ; then ι is injective. Two indices in the same Av are adjacent because Sv is a clique.
For uv ∈ E, every index of Au is adjacent to every index of Av , because Su ∪ Sv is a clique and
Au ∩ Av = ∅. These are exactly the edges of G[Kd ].
  If dim K = d|V | and B is a basis, then |J| = d|V | and the injection is a bijection.          □
Remark 4.2. The proof uses that B spans K, not that it is linearly independent. The embedding
is not induced in general: HB may have further edges.
Remark 4.3 (Where a change of basis can help). For a spanning family, condition (2.1) is forced
by (R). If, for some space with a block structure, the sets Sv of a spanning family violate (2.1),
then (R) fails, and nothing prevents a basis whose overlap graph avoids the blow-up. The three
conditions thus also indicate where a change of basis may reduce overlap.

                                      5. The colouring kernel
   We verify the three conditions for K = KG (F) with blocks Iv = {v} × C and d = 2.
Lemma 5.1 (Supports in TF ). Every nonzero vector of TF has at least two nonzero coordinates.
Hence any two nonzero vectors of TF have a common nonzero coordinate.
Proof. A vector with exactly one nonzero coordinate has nonzero coordinate sum. Two subsets
of C of size at least two intersect. No assumption on the characteristic is used.        □
Lemma 5.2. The colouring kernel KG (F) satisfies (R), (L) and (E) with d = 2.
Proof. (R): By (3.2), πX maps KG (F) onto TFX , which has dimension 2|X|.
   (L): If z|v and z ′ |v are nonzero, they are nonzero vectors of TF and share a nonzero coordinate
(v, c) by Lemma 5.1.
   (E): Let e = {u, v} ∈ E, z|u =    ̸ 0 and z ′ |v ̸= 0. If z|v =
                                                                 ̸ 0, apply (L) at v; if z ′ |u ̸= 0, apply (L)
                                   ′
at u. Otherwise z|v = 0 and z |u = 0, and (3.1) gives, for every c ∈ C,
                                                           ′       ′
                                      ze,c = −zu,c ,      ze,c = −zv,c .
The triples z|u and z ′ |v are nonzero vectors of TF , so by Lemma 5.1 there is a colour c with
              ′ . Then z and z ′ are both nonzero at the slack coordinate (e, c).
zu,c ̸= 0 ̸= zv,c                                                                            □

Proposition 5.3 (Canonical basis). Define a linear map Φ : FV ×{0,1} → KG (F) by
                  xv,0 = av,0 ,      xv,1 = av,1 ,     xv,2 = −av,0 − av,1           (v ∈ V ),
                                                                                 
                           ye,c = −xu,c − xv,c         e = {u, v} ∈ E, c ∈ C .
Then Φ is an isomorphism, and the image Bnat = (bv,i )v∈V, i∈{0,1} of the standard basis satisfies
      ∼ G[K2 ].
HBnat =
Proof. Φ is the inverse of the isomorphism (3.2), composed with (a0 , a1 ) 7→ (a0 , a1 , −a0 − a1 ).
The vector bv,i has support
                     supp(bv,i ) = {(v, i), (v, 2)} ∪ {(e, i), (e, 2) : e ∈ E, v ∈ e}.
The entries −1 are nonzero in every field, including characteristic 2. Thus bv,0 and bv,1 share
the coordinate (v, 2). For e = uv ∈ E, each of bu,0 , bu,1 shares the coordinate (e, 2) with each of
                   ̸ v are not adjacent, the supports of bu,i and bv,i′ are disjoint, because no edge
bv,0 , bv,1 . If u =
contains both u and v.                                                                             □
6                                               BJÖRN TONN

Theorem 5.4 (Main Theorem). Let G be a finite nonempty simple graph and F a field. For every
finite spanning family B of KG (F), the graph G[K2 ] is isomorphic to a subgraph of HB ; if B is
a basis, it is isomorphic to a spanning subgraph of HB . For the canonical basis, HBnat ∼
                                                                                        = G[K2 ].
Proof. Combine Lemma 5.2, Theorem 4.1 with d = 2, the dimension formula (3.2) and Proposi-
tion 5.3.                                                                              □
5.1. More colours. For q ≥ 4 colours the zero-sum space in Fq contains nonzero vectors with
disjoint supports, for example (1, −1, 0, 0, . . . ) and (0, 0, 1, −1, . . . ), so condition (L) fails. The
direct analogue of Theorem 5.4 is then not merely out of reach of the proof; it is false.
Proposition 5.5 (Failure of the direct extension). Fix a field F and q ≥ 3. For the single-vertex
graph K1 , the homogeneous kernel of the q-colour exact-one encoding is
                               n           Pq              o
                         Tq = x ∈ Fq :         i=1 xi = 0 ,       dim Tq = q − 1.
It has a basis whose overlap graph is the path Pq−1 , and minB tw(HB ) = 1. For every q ≥ 4 this
overlap graph does not contain K1 [Kq−1 ] = Kq−1 , while the free-coordinate basis has overlap
graph Kq−1 .
Proof. Let e1 , . . . , eq be the standard basis of Fq and B = (e1 −e2 , e2 −e3 , . . . , eq−1 −eq ). These
q − 1 vectors lie in Tq and are linearly independent over every field, so they form a basis. Their
supports are the sets {i, i + 1}, which intersect exactly for consecutive indices; hence HB ∼        = Pq−1
and tw(HB ) ≤ 1. By contrast, all members of the free-coordinate basis (e1 − eq , . . . , eq−1 − eq )
share the coordinate q, so its overlap graph is Kq−1 .
   Every nonzero vector of Tq has at least two nonzero coordinates. If the q − 1 members of a
basis had pairwise disjoint supports, these would cover at least 2(q − 1) > q coordinates, which
is impossible. So every overlap graph has an edge, and minB tw(HB ) = 1. For q ≥ 4 the path
Pq−1 is not complete.                                                                                    □
  The proposition concerns only the direct q-colour version of the same encoding. It does not
exclude weaker embeddings or other encodings for q ≥ 4.

                                           6. Consequences
Theorem 6.1 (Simultaneous optimality). Let p be a subgraph-monotone graph parameter. Then
                                                                        
                                         min           p(HB ) = p G[K2 ] ,
                                   B basis of KG (F)

and the minimum is attained by Bnat . The same value is the minimum over all finite spanning
families.
Proof. By Theorem 5.4, every HB contains G[K2 ], so p(HB ) ≥ p(G[K2 ]), with equality for
Bnat .                                                                                 □
Corollary 6.2 (Explicit values). For every field F, with minima over all bases B of KG (F):
                         Parameter                Minimum over all bases
                         treewidth                minB tw(HB ) = 2 tw(G) + 1
                         pathwidth                minB pw(HB ) = 2 pw(G) + 1
                         number of edges          minB |E(HB )| = |V | + 4|E|
                         clique number            minB ω(HB ) = 2 ω(G)
                         chromatic number         minB χ(HB ) = χ2 (G)
Here χ2 (G) is the 2-fold chromatic number of G: the least number of colours such that every
vertex receives two distinct colours and adjacent vertices receive disjoint pairs.
                                EVERY BASIS SEES THE BLOW-UP                                    7

Proof. All five parameters are subgraph monotone, so Theorem 6.1 applies. The widths of G[K2 ]
are given by Lemma 2.2. The graph G[K2 ] has one edge per vertex of G and four per edge of
G. A clique of G[K2 ] projects onto a clique of G and meets each fibre in at most two vertices,
and Q × {1, 2} is a clique for every clique Q of G. A proper colouring of G[K2 ] is the same as a
2-fold colouring of G.                                                                         □
Corollary 6.3 (Threshold form). For every integer k ≥ 0, the kernel KG (F) has a basis B with
tw(HB ) ≤ 2k + 1 if and only if tw(G) ≤ k.
  Over F3 , Corollary 6.3 is the statement that has been formalised (Section 8).
Remark 6.4 (Basis-dependent procedures). Suppose a procedure chooses a basis B of KG (F)
and its cost is a nondecreasing function of a subgraph-monotone parameter of HB , for instance
dynamic programming along a tree decomposition of HB with cost exponential in tw(HB ).
Theorem 6.1 says that such a procedure gains nothing from a non-canonical basis. This is a
statement about the parameter, not a lower bound on running time: it says nothing about
procedures whose cost is not tied to HB , nor about algorithms that do not use this kernel.
  The next proposition shows that the overlap treewidth alone cannot serve as a proof-size
measure.
Proposition 6.5 (No Resolution lower bound from overlap width alone). There is an infinite
family of unsatisfiable formulas F (Gn ) with minB tw(HB ) = 2n−1 for Gn = Kn , whose standard
CNF translations have Resolution refutations of size bounded by an absolute constant.
Proof. For n ≥ 4, Corollary 6.2 gives minB tw(HB ) = 2 tw(Kn ) + 1 = 2n − 1. Translate each
constraint EXACT1(a, b, c) into the four clauses a ∨ b ∨ c, ¬a ∨ ¬b, ¬a ∨ ¬c and ¬b ∨ ¬c. The
graph K4 is not 3-colourable, so the CNF of F (K4 ) is unsatisfiable and, by completeness of
Resolution, has a refutation of some fixed size. Its clauses occur in the CNF of F (Kn ) for every
n ≥ 4, so the same refutation works for all n.                                                  □
   Hence no unbounded function of the minimum overlap treewidth alone can bound Resolution
refutation size from below on this family. Whether additional hypotheses, such as the absence of
small unsatisfiable subformulas, support a restricted statement is left open.

                         7. Examples and computational checks
                Graph G                         tw(G)    G[K2 ]    minB tw(HB )
                one vertex                       0        K2              1
                two isolated vertices            0      K2 ⊔ K2           1
                one edge                         1        K4              3
                forest with at least one edge    1        —               3
                complete graph Kr               r−1      K2r           2r − 1
   For the graph consisting of a single edge, the kernel has dimension four, and Theorem 5.4
forces HB ∼= K4 for every basis. Over F3 the number of bases up to order and nonzero scaling of
the members is
                                 |GL4 (F3 )|   24 261 120
                                     4
                                             =            = 63 180.
                                   2 · 4!         384
The following checks were run; none is used in a proof.
   • Exhaustive, F3 . For the single edge, all 63 180 bases have overlap treewidth exactly 3. For
     one vertex the minimum is 1; for two isolated vertices the minimum is 1 and the maximum
     3.
   • Random bases, F3 . For P3 , C4 , K4 and C5 plus an isolated vertex, 3000 uniformly random
     bases each, and 600 for the Petersen graph: in every case the sets Sv and Su ∪ Sv were
     cliques, a Hall selection existed, and the selected indices spanned a copy of G[K2 ].
8                                         BJÖRN TONN

  • Other prime fields. The same test over F2 , F5 and F7 , with 1000 random bases for each of
    the four small graphs and 200 for the Petersen graph, with the same outcome.
The scripts are short Python programs without external dependencies; they are provided as
supplementary material.

                                   8. Formal verification
  Part of the development has been formalised in Lean 4 with Mathlib. Its scope is narrower
than the paper. Over F3 (ZMod 3) the formalisation contains the following declarations.
     Statement in this paper                            Lean declaration
     kernel (3.1), overlap graph, tree decompositions   Ker, coeffGraph, TreeDecomp, TwLe
     HBnat ∼
           = G[K2 ] (Proposition 5.3)                   coeffGraph_nat
     upper bound for treewidth in Corollary 6.2         wstar_le_two_tw_add_one
     Sv and Su ∪ Sv are cliques                         suppV_clique, adj_union_clique
     Hall condition (2.1) for d = 2                     two_card_le
     lower bound for treewidth, spanning families       tw_le_of_coeff_tw
     Corollary 6.3                                      wstar_eq_iff
The lower-bound declarations assume only that the family spans the kernel. The formal lower-
bound proof follows the argument of Lemma 2.2, with the sets Sv in place of Qv ; it does not
pass through a subgraph embedding.
  Not formalised are Theorem 4.1, the Hall selection, Theorem 5.4 as a subgraph statement,
the extension to arbitrary fields, the pathwidth identity, Proposition 5.5 and Proposition 6.5.
  The files are WStar.lean and WStarLower.lean, with SHA-256 digests
    WStar.lean      2caafc866c2a7198ea30873054139a3d8b9cacd263a578db31ac3fb4764eb067
    WStarLower.lean dbfc812c176fae4bf36d2408e1e70fc5e1bbff0e2735c92a6de54fc00763b83b
They target Lean 4.35.0 and Mathlib v4.35.0. The accompanying build record reports a successful
compilation and lists exactly propext, Classical.choice and Quot.sound, the standard axioms
of Lean [8], as the axioms of the three main declarations. The sources contain no sorry, admit,
user-declared axioms or native_decide. An independent reproduction of the build is invited;
see the data availability statement.

                                      9. Related work
   Clique blow-ups. The graphs G[Kq ] are standard in work on treewidth, for example in Marx’s
analysis of whether treewidth can be beaten [10]. Width identities for them appear in [2, 9]; see
the discussion after Lemma 2.2.
   Matroid treewidth. Hliněný and Whittle [4, 5] define a treewidth for matroids and show that
it agrees with graph treewidth for the cycle matroid of a graph with at least one edge. Our
parameter is defined differently: it is a minimum, over bases of a fixed coordinatised space, of a
graph parameter of the support-overlap graph. Moreover KG (F) is not the cycle space of G; for
a single vertex the cycle matroid is empty, whereas KG (F) has dimension two.
   Graphical realisations of codes. Kashyap [6, 7] defines the treewidth of a linear code as the
least constraint complexity, that is, the largest local constraint-code dimension, over its tree
realisations. This minimises over realisations on trees, not over bases, and measures dimensions,
not an overlap graph. We are not aware of a translation between the two notions that yields
Theorem 5.4.
   Transversal theory. The Hall step in Theorem 4.1 derives a combinatorial matching condition
from a rank condition. This is close in spirit to Rado’s theorem on independent transversals [11].
The difference is that we need disjoint sets of indices, not an independent transversal, and that
the cliques come from conditions (L) and (E) rather than from the rank function.
                                 EVERY BASIS SEES THE BLOW-UP                                    9

   Sparse null-space bases. Choosing a basis of a null space with favourable support is a
classical theme in numerical linear algebra, usually with the number of nonzero entries as the
objective. Theorem 6.1 shows that for the colouring kernel a single basis is optimal for every
subgraph-monotone measure of the overlap pattern at once.
   Priority. We have not located Theorem 4.1 or Theorem 5.4 in the literature. The argument
is elementary, and a more general statement may exist; we would welcome references.

                            10. Limitations and open questions
  • Homogeneous versus affine. The results concern the kernel with right-hand side 0. The
    affine solution set of the constraint equations is a different object.
  • Coordinates. The overlap graph depends on the coordinate system, including the slack
    coordinates. Invariance under puncturing, shortening or other encodings of 3-colourability
    is not claimed.
  • Number of colours. Condition (L) relies on |C| = 3; by Proposition 5.5 the direct extension
    fails for every q ≥ 4.
  • Linear re-encodings only. The theorem quantifies over spanning families of one linear space
    and says nothing about nonlinear reformulations.
  • No complexity separation. The theorem implies no lower bound for Boolean circuits, for
    proof systems or for algorithms deciding 3-colourability; Proposition 6.5 rules out even a
    naive Resolution bound.
Questions.
(1) Which other constraint encodings satisfy (R), (L) and (E), and with which d?
(2) Is there a natural encoding for which (R) fails and a non-canonical basis has strictly smaller
    overlap treewidth?
(3) For q ≥ 4 colours, what is the strongest valid replacement for the host graph G[Kq−1 ]?
(4) Can Theorem 4.1 be derived from, or does it imply, a known inequality between graph
    treewidth and a width parameter of codes or matroids?
(5) Is there a restricted proof system or algorithmic model, with explicit representation rules,
    for which a width-based lower bound survives the control in Proposition 6.5?

                                        11. Conclusion
   For the homogeneous kernel of the one-in-three encoding of 3-colourability, the overlap graph
of every spanning family contains the two-fold clique blow-up of the underlying graph, over
every field, and the canonical basis realises exactly this graph. It is therefore optimal for every
subgraph-monotone parameter; in particular the minimum overlap treewidth and pathwidth
over all bases are 2 tw(G) + 1 and 2 pw(G) + 1. The proof reduces to a rank condition, two
intersection conditions and Hall’s theorem, and these conditions describe a class of linear spaces
for which the same conclusion holds. The direct analogue fails for four or more colours, and
overlap treewidth alone does not control Resolution proof size.
Data availability. This preprint is registered under doi:10.5281/zenodo.24438918. The
Python scripts of Section 7 are provided as supplementary material. The Lean sources and their
build record are available in the public repository
                 repository https://github.com/tonnestate/FruitStack-Eval
                 commit     ca802b566dfc1e8d0437ab010e464192122d6c31
                 directory results/PNP-001-2026-11-19/lean/
Acknowledgements. Parts of the proofs, the formalisation and the computational checks were
developed with the assistance of AI systems. The author takes responsibility for all statements
in this paper.
10                                          BJÖRN TONN

                                            References
 [1] R. Diestel, Graph Theory, 5th ed., Graduate Texts in Mathematics 173, Springer, 2017.
 [2] F. Gurski and R. Weishaupt, The behavior of tree-width and path-width under graph opera-
     tions and graph transformations, Algorithms 18(7) (2025), 386. doi:10.3390/a18070386. Preprint:
     arXiv:2406.08985.
 [3] P. Hall, On representatives of subsets, J. London Math. Soc. 10 (1935), 26–30.
 [4] P. Hliněný and G. Whittle, Matroid tree-width, European J. Combin. 27 (2006), 1117–1128.
 [5] P. Hliněný and G. Whittle, Addendum to matroid tree-width, European J. Combin. 30 (2009),
     1036–1044. doi:10.1016/j.ejc.2008.09.028.
 [6] N. Kashyap, On minimal tree realizations of linear codes, IEEE Trans. Inform. Theory 55 (2009),
     3501–3519. Preprint: arXiv:0711.1383.
 [7] N. Kashyap, Constraint complexity of realizations of linear codes on arbitrary graphs, IEEE Trans.
     Inform. Theory 55 (2009), 4864–4877. Preprint: arXiv:0805.2199.
 [8] The Lean Language Reference: axioms and validating a Lean proof. https://lean-lang.org/doc/
     reference/latest/.
 [9] Xinheng Lin, Treewidth and the product of tree-independence and tree-chromatic numbers,
     arXiv:2610.20407, 2026.
[10] D. Marx, Can you beat treewidth?, Theory Comput. 6 (2010), 85–112.
[11] R. Rado, A theorem on independence relations, Quart. J. Math. Oxford Ser. 13 (1942), 83–89.
     doi:10.1093/qmath/os-13.1.83.
[12] N. Robertson and P. D. Seymour, Graph minors. II. Algorithmic aspects of tree-width, J. Algorithms
     7 (1986), 309–322.
[13] T. J. Schaefer, The complexity of satisfiability problems, in Proc. 10th ACM Symposium on Theory
     of Computing (STOC), 1978, 216–226.
