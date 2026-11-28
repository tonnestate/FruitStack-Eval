# Lower bound w*(F(G)) >= 2*tw(G) + 1 over all kernel bases — owner's proof text for formalisation (2026-11-19, binding)

This proof does not use Lemma W, the row matroid, or matroid tree-width. It needs only linear algebra over GF(3) and one standard fact
about tree decompositions (a clique lies in a bag; the bags containing it form a connected set).

## Setting
* G = (V, E) finite simple graph, V nonempty. Colours c in {1,2,3}.
* Coordinates I = (V x {1,2,3}) ⊔ (E x {1,2,3}); k(v,c), k(e,c).
* K_G ⊆ GF(3)^I: (V) k(v,1)+k(v,2)+k(v,3) = 0 for every vertex v; (E) k(e,c) = −(k(u,c)+k(w,c)) for every edge e={u,w}, colour c.
  (kernel of the clause matrix of F(G).)
* T = { t in GF(3)^3 : t1+t2+t3 = 0 } (dim 2). Restriction to vertex coordinates is an isomorphism K_G → T^V; dim K_G = 2|V| =: d.
* B = (b_1..b_d) arbitrary basis of K_G. Coefficient graph H_B on {1..d}: j ~ k (j≠k) iff some coordinate i has b_j(i)≠0 and b_k(i)≠0.
* S_v = { j : b_j(v,c) ≠ 0 for some colour c }.
* Tree decomposition (T, β) of H: T a tree, β(t) ⊆ V(H), every vertex in some bag, every edge inside some bag, for every vertex the set of
  nodes whose bag contains it is connected. Width = max |β(t)| − 1.

## Two local facts
* (L1) t in T, t ≠ 0 ⇒ t has at least two nonzero entries.
* (L2) Two subsets of {1,2,3} with at least two elements each intersect.

## Step (i): every S_v is a clique of H_B
j ≠ k in S_v: b_j(v,·), b_k(v,·) nonzero in T; by (L1) supports of size >= 2, by (L2) a common colour c; coordinate (v,c) witnesses j ~ k.

## Step (ii): for every edge e={u,w}, S_u ∪ S_w is a clique of H_B
Both in S_u or both in S_w: step (i). Otherwise j in S_u\S_w, k in S_w\S_u: b_j(w,·)=0, b_j(u,·)≠0, so b_j(e,c) = −b_j(u,c), nonzero exactly on
supp b_j(u,·) (size >= 2); symmetrically b_k(e,c) = −b_k(w,c); by (L2) a common colour c; coordinate (e,c) witnesses j ~ k.

## Step (iii): for every X ⊆ V, |⋃_{v in X} S_v| >= 2|X|
π_X : K_G → T^X restriction, linear and surjective, dim T^X = 2|X|. The π_X(b_j) span T^X; π_X(b_j) = 0 if j not in ⋃_{v∈X} S_v; so at
least 2|X| of them. In particular |S_v| >= 2.
General lemma: if a finite family (b_j) spans K and π : K → N is linear surjective, then finrank N <= #{ j : π(b_j) ≠ 0 }.

## Step (iv): transfer of a tree decomposition
(T, β) tree decomposition of H_B of width w. β_G(t) = { v in V : S_v ⊆ β(t) }.
Fact (C): C nonempty clique of H, (T,β) tree decomposition of H ⇒ T_C = { t : C ⊆ β(t) } nonempty and connected. (Each T_j connected,
nonempty; pairwise intersect since edge {j,k} lies in a bag; pairwise intersecting connected subsets of a tree have a common node (Helly);
intersection of connected subsets of a tree is connected (unique paths).)
(T, β_G) is a tree decomposition of G: vertex v: {t : v in β_G(t)} = T_{S_v}, nonempty clique by (iii),(i) ⇒ nonempty connected by (C).
Edge {u,w}: S_u ∪ S_w nonempty clique by (ii) ⇒ some bag contains it ⇒ u,w in β_G(t).
Width: X = β_G(t): 2|β_G(t)| <= |⋃_{v∈X} S_v| <= |β(t)| <= w+1. Hence tw(G)+1 <= (w+1)/2, i.e. w >= 2 tw(G)+1.

## Suggested Lean decomposition
1. local_support (L1), two_subsets_inter (L2): decide over ZMod 3 / Fin 3.
2. S_clique (i), S_union_clique (ii).
3. card_support_ge_finrank: the spanning lemma, instantiated with π_X, finrank (T^X) = 2|X|.
4. clique_bags_nonempty_connected (fact C) — the only real work. Hint: convexity of T_j (closed under the unique path) makes intersection
   immediate; Helly for finitely many pairwise intersecting convex subtrees by induction (median of three nodes, or leaf removal).
5. tw_le_of_coeff_tw: assemble (iv); cardinality 2 * (β_G t).card <= (β t).card.
6. Combine with wstar_le_two_tw_add_one to get equality.

Exhaustive data: K2 (all 63,180 bases up to order and scaling give K4, w* = 3); K4 (no two nonzero kernel vectors with disjoint support among
6,560, so every basis gives K8, w* = 7).
