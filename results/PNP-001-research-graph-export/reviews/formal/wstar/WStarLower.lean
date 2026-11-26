import Mathlib.Combinatorics.SimpleGraph.Acyclic
import Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.ZMod.Basic
import Mathlib.LinearAlgebra.LinearIndependent.Basic
import Mathlib.LinearAlgebra.Span.Basic
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FinCases
import Mathlib.LinearAlgebra.StdBasis
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.Combinatorics.SimpleGraph.Walk.Maps

/-! PNP-001, w*(F(G)) upper bound, step 2 (graph part).
Tree decompositions (not in Mathlib), the 2-blow-up of a graph, and: width k for G gives width 2k+1 for the blow-up. -/

namespace PNP001

section GraphPart

variable {V : Type} [DecidableEq V]

/-- A tree decomposition of `G` of width at most `k`. -/
structure TreeDecomp (G : SimpleGraph V) (k : ℕ) where
  T : Type
  tree : SimpleGraph T
  isTree : tree.IsTree
  bag : T → Finset V
  cover : ∀ v, ∃ t, v ∈ bag t
  edge : ∀ v w, G.Adj v w → ∃ t, v ∈ bag t ∧ w ∈ bag t
  conn : ∀ v, (tree.induce {t | v ∈ bag t}).Connected
  width : ∀ t, (bag t).card ≤ k + 1

/-- `G` has treewidth at most `k`. -/
def TwLe (G : SimpleGraph V) (k : ℕ) : Prop := Nonempty (TreeDecomp G k)

/-- 2-blow-up: every vertex becomes a 2-clique, every edge a complete bipartite join of the two cliques. -/
def blowup (G : SimpleGraph V) : SimpleGraph (V × Fin 2) :=
  SimpleGraph.fromRel fun p q => p.1 = q.1 ∨ G.Adj p.1 q.1

theorem twLe_blowup (G : SimpleGraph V) (k : ℕ) (h : TwLe G k) : TwLe (blowup G) (2 * k + 1) := by
  obtain ⟨D⟩ := h
  refine ⟨{ T := D.T, tree := D.tree, isTree := D.isTree,
            bag := fun t => D.bag t ×ˢ (Finset.univ : Finset (Fin 2)), cover := ?_, edge := ?_, conn := ?_, width := ?_ }⟩
  · rintro ⟨v, i⟩
    obtain ⟨t, ht⟩ := D.cover v
    exact ⟨t, Finset.mem_product.2 ⟨ht, Finset.mem_univ _⟩⟩
  · rintro ⟨v, i⟩ ⟨w, j⟩ ⟨_, hvw⟩
    have key : v = w ∨ G.Adj v w := by
      rcases hvw with (h | h) | (h | h)
      · exact Or.inl h
      · exact Or.inr h
      · exact Or.inl h.symm
      · exact Or.inr h.symm
    rcases key with h | h
    · subst h
      obtain ⟨t, ht⟩ := D.cover v
      exact ⟨t, Finset.mem_product.2 ⟨ht, Finset.mem_univ _⟩, Finset.mem_product.2 ⟨ht, Finset.mem_univ _⟩⟩
    · obtain ⟨t, h1, h2⟩ := D.edge v w h
      exact ⟨t, Finset.mem_product.2 ⟨h1, Finset.mem_univ _⟩, Finset.mem_product.2 ⟨h2, Finset.mem_univ _⟩⟩
  · rintro ⟨v, i⟩
    have hs : {t | (v, i) ∈ D.bag t ×ˢ (Finset.univ : Finset (Fin 2))} = {t | v ∈ D.bag t} := by
      ext t; simp [Finset.mem_product]
    rw [hs]; exact D.conn v
  · intro t
    rw [Finset.card_product, Finset.card_univ, Fintype.card_fin]
    have := D.width t
    omega



end GraphPart

/-! Step 1: the formula F(G), its GF(3) kernel, the natural basis and its coefficient graph. -/

section Formula

variable {V : Type} [LinearOrder V] (G : SimpleGraph V)

/-- each undirected edge once, oriented by the order -/
abbrev Edge := {p : V × V // p.1 < p.2 ∧ G.Adj p.1 p.2}

/-- variables of F(G): x_{v,c} (colour c) and y_{e,c} (slack of edge e, colour c) -/
abbrev Var := (V × Fin 3) ⊕ (Edge G × Fin 3)

/-- the homogeneous GF(3) system of F(G): sum of the three variables of every clause is 0 -/
def Ker : Submodule (ZMod 3) (Var G → ZMod 3) where
  carrier := {z | (∀ v, z (.inl (v, 0)) + z (.inl (v, 1)) + z (.inl (v, 2)) = 0) ∧
                  ∀ (e : Edge G) (c : Fin 3), z (.inl (e.1.1, c)) + z (.inl (e.1.2, c)) + z (.inr (e, c)) = 0}
  add_mem' := by
    rintro a b ⟨ha1, ha2⟩ ⟨hb1, hb2⟩
    refine ⟨fun v => ?_, fun e c => ?_⟩
    · simp only [Pi.add_apply]; linear_combination ha1 v + hb1 v
    · simp only [Pi.add_apply]; linear_combination ha2 e c + hb2 e c
  zero_mem' := ⟨fun v => by simp, fun e c => by simp⟩
  smul_mem' := by
    rintro r a ⟨h1, h2⟩
    refine ⟨fun v => ?_, fun e c => ?_⟩
    · simp only [Pi.smul_apply, smul_eq_mul]; linear_combination r * h1 v
    · simp only [Pi.smul_apply, smul_eq_mul]; linear_combination r * h2 e c

variable {G}

/-- value of x_{u,c} under the parametrisation a : V × Fin 2 → GF(3)  (x_{u,0}=a_u, x_{u,1}=b_u, x_{u,2}=-a_u-b_u) -/
def xval (a : V × Fin 2 → ZMod 3) (u : V) (c : Fin 3) : ZMod 3 :=
  if c = 0 then a (u, 0) else if c = 1 then a (u, 1) else -a (u, 0) - a (u, 1)

/-- the natural parametrisation of the kernel -/
def phi (a : V × Fin 2 → ZMod 3) : Var G → ZMod 3
  | .inl (u, c) => xval a u c
  | .inr (e, c) => -xval a e.1.1 c - xval a e.1.2 c

theorem phi_mem (a : V × Fin 2 → ZMod 3) : phi (G := G) a ∈ Ker G := by
  refine ⟨fun v => ?_, fun e c => ?_⟩
  · simp [phi, xval]
  · simp [phi]

/-- coefficient (primal) graph of a family of kernel vectors: i ~ j iff some variable has nonzero coefficient in both -/
def coeffGraph {ι : Type} (b : ι → Var G → ZMod 3) : SimpleGraph ι :=
  SimpleGraph.fromRel fun i j => ∃ z, b i z ≠ 0 ∧ b j z ≠ 0

/-- natural basis vector for the free coordinate p = (v, i) -/
def nat (p : V × Fin 2) : Var G → ZMod 3 := phi (Pi.single p 1)

end Formula

section Support

variable {V : Type} [LinearOrder V] {G : SimpleGraph V}

theorem xval_single_ne (v u : V) (i : Fin 2) (c : Fin 3) :
    xval (Pi.single (v, i) (1 : ZMod 3)) u c ≠ 0 ↔ u = v ∧ (c.val = i.val ∨ c = 2) := by
  by_cases h : u = v
  · subst h
    fin_cases i <;> fin_cases c <;> simp [xval]
  · have h0 : ∀ k : Fin 2, (Pi.single (v, i) (1 : ZMod 3) : V × Fin 2 → ZMod 3) (u, k) = 0 := fun k => by
      simp [Pi.single_apply, h]
    simp [xval, h]

theorem xval_single_eq_zero (v u : V) (i : Fin 2) (c : Fin 3) (h : u ≠ v) :
    xval (Pi.single (v, i) (1 : ZMod 3)) u c = 0 := by
  by_contra hc
  exact h ((xval_single_ne v u i c).1 hc).1

theorem nat_inl_ne (v u : V) (i : Fin 2) (c : Fin 3) :
    nat (G := G) (v, i) (.inl (u, c)) ≠ 0 ↔ u = v ∧ (c.val = i.val ∨ c = 2) :=
  xval_single_ne v u i c

theorem nat_inr_ne (v : V) (i : Fin 2) (e : Edge G) (c : Fin 3) :
    nat (G := G) (v, i) (.inr (e, c)) ≠ 0 ↔ (e.1.1 = v ∨ e.1.2 = v) ∧ (c.val = i.val ∨ c = 2) := by
  have hlt := e.2.1
  show -xval _ e.1.1 c - xval _ e.1.2 c ≠ 0 ↔ _
  by_cases h1 : e.1.1 = v
  · have h2 : e.1.2 ≠ v := fun h => (ne_of_lt hlt) (h1.trans h.symm)
    rw [xval_single_eq_zero v _ i c h2, sub_zero, neg_ne_zero, xval_single_ne]
    simp [h1]
  · rw [xval_single_eq_zero v _ i c h1, neg_zero, zero_sub, neg_ne_zero, xval_single_ne]
    simp [h1]

/-- the coefficient graph of the natural basis is exactly the 2-blow-up of G -/
theorem coeffGraph_nat : coeffGraph (G := G) nat = blowup G := by
  have core : ∀ p q : V × Fin 2, p ≠ q →
      ((∃ z, nat (G := G) p z ≠ 0 ∧ nat (G := G) q z ≠ 0) ↔ (p.1 = q.1 ∨ G.Adj p.1 q.1)) := by
    rintro ⟨v, i⟩ ⟨w, j⟩ hpq
    constructor
    · rintro ⟨z, hz1, hz2⟩
      rcases z with ⟨u, c⟩ | ⟨e, c⟩
      · rw [nat_inl_ne] at hz1 hz2
        exact Or.inl (hz1.1.symm.trans hz2.1)
      · rw [nat_inr_ne] at hz1 hz2
        by_cases hvw : v = w
        · exact Or.inl hvw
        · right
          have ha := e.2.2
          rcases hz1.1 with h1 | h1 <;> rcases hz2.1 with h2 | h2
          · exact absurd (h1.symm.trans h2) hvw
          · simpa [← h1, ← h2] using ha
          · simpa [← h1, ← h2] using ha.symm
          · exact absurd (h1.symm.trans h2) hvw
    · rintro (h | h)
      · simp only at h
        subst h
        exact ⟨.inl (v, 2), (nat_inl_ne _ _ _ _).2 ⟨rfl, Or.inr rfl⟩, (nat_inl_ne _ _ _ _).2 ⟨rfl, Or.inr rfl⟩⟩
      · simp only at h
        rcases lt_or_gt_of_ne (G.ne_of_adj h) with hl | hl
        · refine ⟨.inr (⟨(v, w), hl, h⟩, 2), (nat_inr_ne _ _ _ _).2 ⟨Or.inl rfl, Or.inr rfl⟩,
                  (nat_inr_ne _ _ _ _).2 ⟨Or.inr rfl, Or.inr rfl⟩⟩
        · refine ⟨.inr (⟨(w, v), hl, h.symm⟩, 2), (nat_inr_ne _ _ _ _).2 ⟨Or.inr rfl, Or.inr rfl⟩,
                  (nat_inr_ne _ _ _ _).2 ⟨Or.inl rfl, Or.inr rfl⟩⟩
  ext p q
  simp only [coeffGraph, blowup, SimpleGraph.fromRel_adj]
  constructor
  · rintro ⟨hpq, h | h⟩
    · exact ⟨hpq, Or.inl ((core p q hpq).1 h)⟩
    · exact ⟨hpq, Or.inr ((core q p (Ne.symm hpq)).1 h)⟩
  · rintro ⟨hpq, h | h⟩
    · exact ⟨hpq, Or.inl ((core p q hpq).2 h)⟩
    · exact ⟨hpq, Or.inr ((core q p (Ne.symm hpq)).2 h)⟩

end Support

section Basis

variable {V : Type} [LinearOrder V] {G : SimpleGraph V}

/-- the parametrisation as a linear map -/
def phiL : (V × Fin 2 → ZMod 3) →ₗ[ZMod 3] (Var G → ZMod 3) where
  toFun := phi
  map_add' a b := by
    funext z; rcases z with ⟨u, c⟩ | ⟨e, c⟩ <;> simp only [phi, xval, Pi.add_apply] <;> split_ifs <;> ring
  map_smul' r a := by
    funext z; rcases z with ⟨u, c⟩ | ⟨e, c⟩ <;> simp only [phi, xval, Pi.smul_apply, smul_eq_mul, RingHom.id_apply] <;>
      split_ifs <;> ring

theorem xval_of_ker {z : Var G → ZMod 3} (hz : z ∈ Ker G) (u : V) (c : Fin 3) :
    xval (fun p => z (.inl (p.1, Fin.castSucc p.2))) u c = z (.inl (u, c)) := by
  obtain ⟨h1, -⟩ := hz
  fin_cases c
  · simp [xval]
  · simp [xval]
  · simp only [xval]; simp; linear_combination (-1 : ZMod 3) * h1 u

theorem ker_le_range : Ker G ≤ LinearMap.range (phiL (G := G)) := by
  intro z hz
  refine ⟨fun p => z (.inl (p.1, Fin.castSucc p.2)), ?_⟩
  funext w
  rcases w with ⟨u, c⟩ | ⟨e, c⟩
  · exact xval_of_ker hz u c
  · show -xval _ e.1.1 c - xval _ e.1.2 c = z (.inr (e, c))
    rw [xval_of_ker hz, xval_of_ker hz]
    linear_combination (-1 : ZMod 3) * hz.2 e c

theorem range_eq_ker : LinearMap.range (phiL (G := G)) = Ker G :=
  le_antisymm (by rintro _ ⟨a, rfl⟩; exact phi_mem a) ker_le_range

theorem phiL_injective : Function.Injective (phiL (G := G)) := by
  intro a b h
  funext p
  obtain ⟨v, i⟩ := p
  have h0 := congrFun h (.inl (v, 0))
  have h1 := congrFun h (.inl (v, 1))
  fin_cases i
  · simpa [phiL, phi, xval] using h0
  · simpa [phiL, phi, xval] using h1

theorem nat_eq [Fintype V] (p : V × Fin 2) :
    nat (G := G) p = phiL (Pi.basisFun (ZMod 3) (V × Fin 2) p) := by
  simp [nat, phiL, Pi.basisFun_apply]

/-- MAIN (upper bound): if G has treewidth <= k, the GF(3) kernel of F(G) has a basis whose coefficient graph has
treewidth <= 2k+1; i.e. w*(F(G)) <= 2 tw(G) + 1. -/
theorem wstar_le_two_tw_add_one [Fintype V] (k : ℕ) (h : TwLe G k) :
    ∃ b : V × Fin 2 → Var G → ZMod 3, LinearIndependent (ZMod 3) b ∧
      Submodule.span (ZMod 3) (Set.range b) = Ker G ∧ TwLe (coeffGraph b) (2 * k + 1) := by
  refine ⟨nat, ?_, ?_, ?_⟩
  · have hli := (Pi.basisFun (ZMod 3) (V × Fin 2)).linearIndependent.map' (phiL (G := G))
      (LinearMap.ker_eq_bot.2 (phiL_injective (G := G)))
    convert hli using 1
    funext p; exact nat_eq p
  · have hfun : (nat (G := G)) = (phiL (G := G)) ∘ (Pi.basisFun (ZMod 3) (V × Fin 2)) := funext nat_eq
    rw [hfun, Set.range_comp, Submodule.span_image, (Pi.basisFun (ZMod 3) (V × Fin 2)).span_eq, Submodule.map_top,
      range_eq_ker]
  · rw [coeffGraph_nat]
    exact twLe_blowup G k h

end Basis


/-! Lower bound: w*(F(G)) >= 2 tw(G) + 1, following LOWER_BOUND_PROOF.md. -/

section TreeFacts

open SimpleGraph

variable {T : Type} {tree : SimpleGraph T}

/-- a vertex set of a tree is convex if it contains every path between two of its points -/
def TreeConvex (tree : SimpleGraph T) (S : Set T) : Prop :=
  ∀ a b, a ∈ S → b ∈ S → ∀ p : tree.Walk a b, p.IsPath → ∀ x ∈ p.support, x ∈ S

theorem treeConvex_of_connected (hT : tree.IsAcyclic) {S : Set T} (h : (tree.induce S).Connected) :
    TreeConvex tree S := by
  classical
  intro a b ha hb p hp x hx
  obtain ⟨w⟩ := h.preconnected ⟨a, ha⟩ ⟨b, hb⟩
  have hw : ∀ y ∈ (w.map (Embedding.induce S).toHom).support, y ∈ S := by
    intro y hy
    rw [Walk.support_map, List.mem_map] at hy
    obtain ⟨z, -, rfl⟩ := hy
    exact z.2
  let w' : tree.Walk a b := w.map (Embedding.induce S).toHom
  have hw' : ∀ y ∈ w'.support, y ∈ S := hw
  have hpq : (⟨p, hp⟩ : tree.Path a b) = w'.toPath := (hT.subsingleton_path a b).elim _ _
  have hx' : x ∈ (w'.toPath : tree.Walk a b).support := by rw [← hpq]; exact hx
  exact hw' x (w'.support_toPath_subset_support hx')

theorem connected_of_treeConvex (hT : tree.Connected) {S : Set T} (hS : TreeConvex tree S)
    (hne : S.Nonempty) : (tree.induce S).Connected := by
  rw [connected_iff]
  refine ⟨?_, hne.to_subtype⟩
  rintro ⟨a, ha⟩ ⟨b, hb⟩
  obtain ⟨p, hp⟩ := hT.exists_isPath a b
  exact ⟨p.induce S (hS a b ha hb p hp)⟩

theorem treeConvex_inter {A B : Set T} (hA : TreeConvex tree A) (hB : TreeConvex tree B) :
    TreeConvex tree (A ∩ B) := fun a b ha hb p hp x hx =>
  ⟨hA a b ha.1 hb.1 p hp x hx, hB a b ha.2 hb.2 p hp x hx⟩

/-- median: the path x-y, any walk x-z and any walk y-z of a tree share a vertex -/
theorem median (hT : tree.IsAcyclic) {x y z : T} (p : tree.Walk x y) (hp : p.IsPath)
    (q : tree.Walk x z) (r : tree.Walk y z) :
    ∃ m ∈ p.support, m ∈ q.support ∧ m ∈ r.support := by
  classical
  induction p with
  | nil => exact ⟨_, Walk.start_mem_support _, q.start_mem_support, r.start_mem_support⟩
  | @cons u u' y h p' ih =>
    by_cases hur : u ∈ r.support
    · exact ⟨u, Walk.start_mem_support _, q.start_mem_support, hur⟩
    have hp' := (Walk.cons_isPath_iff h p').1 hp
    have hu'q : u' ∈ q.support := by
      by_contra hu'q
      have hbr := isAcyclic_iff_forall_adj_isBridge.1 hT h.symm
      have hmem := isBridge_iff_forall_walk_mem_edges.1 hbr ((p'.append r).append q.reverse)
      simp only [Walk.edges_append, Walk.edges_reverse, List.mem_append, List.mem_reverse] at hmem
      rcases hmem with (h1 | h1) | h1
      · exact hp'.2 (p'.snd_mem_support_of_mem_edges h1)
      · exact hur (r.snd_mem_support_of_mem_edges h1)
      · exact hu'q (q.fst_mem_support_of_mem_edges h1)
    obtain ⟨m, hm1, hm2, hm3⟩ := ih hp'.1 (q.dropUntil u' hu'q) r
    exact ⟨m, by simp [hm1], q.support_dropUntil_subset_support hu'q hm2, hm3⟩

theorem helly3 (hT : tree.IsTree) {A B C : Set T} (hA : TreeConvex tree A) (hB : TreeConvex tree B)
    (hC : TreeConvex tree C) (hAB : (A ∩ B).Nonempty) (hBC : (B ∩ C).Nonempty)
    (hAC : (A ∩ C).Nonempty) : (A ∩ B ∩ C).Nonempty := by
  obtain ⟨x, hxA, hxB⟩ := hAB
  obtain ⟨y, hyB, hyC⟩ := hBC
  obtain ⟨z, hzA, hzC⟩ := hAC
  obtain ⟨p, hp⟩ := hT.connected.exists_isPath x y
  obtain ⟨q, hq⟩ := hT.connected.exists_isPath x z
  obtain ⟨r, hr⟩ := hT.connected.exists_isPath y z
  obtain ⟨m, h1, h2, h3⟩ := median hT.isAcyclic p hp q r
  exact ⟨m, ⟨hA x z hxA hzA q hq m h2, hB x y hxB hyB p hp m h1⟩, hC y z hyC hzC r hr m h3⟩

/-- Helly property for finitely many pairwise intersecting convex subsets of a tree -/
theorem helly {ι : Type} [DecidableEq ι] (hT : tree.IsTree) (C : Finset ι) :
    ∀ F : ι → Set T, (∀ j ∈ C, TreeConvex tree (F j)) → (∀ j ∈ C, ∀ k ∈ C, (F j ∩ F k).Nonempty) →
      C.Nonempty → ∃ t, ∀ j ∈ C, t ∈ F j := by
  induction C using Finset.induction_on with
  | empty => intro F _ _ h; exact absurd h Finset.not_nonempty_empty
  | insert a C ha ih =>
    intro F hconv hpair _
    rcases C.eq_empty_or_nonempty with rfl | hCne
    · obtain ⟨t, ht, -⟩ := hpair a (by simp) a (by simp)
      exact ⟨t, by simpa using ht⟩
    · have mem : ∀ j ∈ C, j ∈ insert a C := fun j hj => Finset.mem_insert_of_mem hj
      have amem : a ∈ insert a C := Finset.mem_insert_self a C
      obtain ⟨t, ht⟩ := ih (fun j => F j ∩ F a)
        (fun j hj => treeConvex_inter (hconv j (mem j hj)) (hconv a amem))
        (fun j hj k hk => by
          obtain ⟨t, ⟨h1, h2⟩, h3⟩ := helly3 hT (hconv j (mem j hj)) (hconv k (mem k hk)) (hconv a amem)
            (hpair j (mem j hj) k (mem k hk)) (hpair k (mem k hk) a amem) (hpair j (mem j hj) a amem)
          exact ⟨t, ⟨h1, h3⟩, ⟨h2, h3⟩⟩) hCne
      refine ⟨t, fun j hj => ?_⟩
      rcases Finset.mem_insert.1 hj with rfl | hj
      · obtain ⟨j0, hj0⟩ := hCne
        exact (ht j0 hj0).2
      · exact (ht j hj).1

end TreeFacts

section CliqueBags

variable {ι : Type} [DecidableEq ι]

/-- fact (C): the bags containing a nonempty clique form a nonempty connected subtree -/
theorem clique_bags {H : SimpleGraph ι} {w : ℕ} (D : TreeDecomp H w) (C : Finset ι) (hC : C.Nonempty)
    (hcl : ∀ j ∈ C, ∀ l ∈ C, j ≠ l → H.Adj j l) :
    (∃ t, C ⊆ D.bag t) ∧ (D.tree.induce {t | C ⊆ D.bag t}).Connected := by
  have hconv : ∀ j, TreeConvex D.tree {t | j ∈ D.bag t} :=
    fun j => treeConvex_of_connected D.isTree.isAcyclic (D.conn j)
  have hC' : TreeConvex D.tree {t | C ⊆ D.bag t} := by
    intro a b ha hb p hp x hx j hj
    exact hconv j a b (ha hj) (hb hj) p hp x hx
  obtain ⟨t, ht⟩ := helly D.isTree C (fun j => {t | j ∈ D.bag t}) (fun j _ => hconv j) (by
    intro j hj l hl
    by_cases hjl : j = l
    · subst hjl
      obtain ⟨t, ht⟩ := D.cover j
      exact ⟨t, ht, ht⟩
    · obtain ⟨t, h1, h2⟩ := D.edge j l (hcl j hj l hl hjl)
      exact ⟨t, h1, h2⟩) hC
  exact ⟨⟨t, fun j hj => ht j hj⟩, connected_of_treeConvex D.isTree.connected hC' ⟨t, fun j hj => ht j hj⟩⟩

omit [DecidableEq ι] in
/-- monotonicity of treewidth bounds -/
theorem twLe_mono {G : SimpleGraph ι} {k k' : ℕ} (h : TwLe G k) (hk : k ≤ k') : TwLe G k' := by
  obtain ⟨D⟩ := h
  exact ⟨{ D with width := fun t => (D.width t).trans (by omega) }⟩

end CliqueBags

section Lower

variable {V : Type} [LinearOrder V] {G : SimpleGraph V}

theorem zmod3_common : ∀ a b c a' b' c' : ZMod 3, a + b + c = 0 → a' + b' + c' = 0 →
    (a ≠ 0 ∨ b ≠ 0 ∨ c ≠ 0) → (a' ≠ 0 ∨ b' ≠ 0 ∨ c' ≠ 0) →
    (a ≠ 0 ∧ a' ≠ 0) ∨ (b ≠ 0 ∧ b' ≠ 0) ∨ (c ≠ 0 ∧ c' ≠ 0) := by
  decide

/-- (L1)+(L2): two kernel vectors, nonzero at vertex x resp. y, share a nonzero colour -/
theorem common_colour {z z' : Var G → ZMod 3} (hz : z ∈ Ker G) (hz' : z' ∈ Ker G) {x y : V}
    (hx : ∃ c, z (.inl (x, c)) ≠ 0) (hy : ∃ c, z' (.inl (y, c)) ≠ 0) :
    ∃ c, z (.inl (x, c)) ≠ 0 ∧ z' (.inl (y, c)) ≠ 0 := by
  have h3 : ∀ f : Fin 3 → ZMod 3, (∃ c, f c ≠ 0) → (f 0 ≠ 0 ∨ f 1 ≠ 0 ∨ f 2 ≠ 0) := by
    rintro f ⟨c, hc⟩
    fin_cases c
    · exact Or.inl hc
    · exact Or.inr (Or.inl hc)
    · exact Or.inr (Or.inr hc)
  rcases zmod3_common _ _ _ _ _ _ (hz.1 x) (hz'.1 y) (h3 (fun c => z (.inl (x, c))) hx)
      (h3 (fun c => z' (.inl (y, c))) hy) with h | h | h
  · exact ⟨0, h⟩
  · exact ⟨1, h⟩
  · exact ⟨2, h⟩

variable {ι : Type} [Fintype ι]

/-- S_v: indices of basis vectors that are nonzero at some colour of v -/
def suppV (b : ι → Var G → ZMod 3) (v : V) : Finset ι :=
  Finset.univ.filter fun j => ∃ c : Fin 3, b j (.inl (v, c)) ≠ 0

theorem mem_suppV {b : ι → Var G → ZMod 3} {v : V} {j : ι} :
    j ∈ suppV b v ↔ ∃ c : Fin 3, b j (.inl (v, c)) ≠ 0 := by
  simp [suppV]

theorem not_mem_suppV {b : ι → Var G → ZMod 3} {v : V} {j : ι} :
    j ∉ suppV b v ↔ ∀ c : Fin 3, b j (.inl (v, c)) = 0 := by
  simp [suppV]

/-- step (i): S_v is a clique of the coefficient graph -/
theorem suppV_clique {b : ι → Var G → ZMod 3} (hb : ∀ j, b j ∈ Ker G) (v : V) :
    ∀ j ∈ suppV b v, ∀ k ∈ suppV b v, j ≠ k → (coeffGraph b).Adj j k := by
  intro j hj k hk hjk
  obtain ⟨c, h1, h2⟩ := common_colour (hb j) (hb k) (mem_suppV.1 hj) (mem_suppV.1 hk)
  rw [coeffGraph, SimpleGraph.fromRel_adj]
  exact ⟨hjk, Or.inl ⟨_, h1, h2⟩⟩

theorem edge_coord {z : Var G → ZMod 3} (hz : z ∈ Ker G) (e : Edge G) {x y : V}
    (hxy : (x = e.1.1 ∧ y = e.1.2) ∨ (x = e.1.2 ∧ y = e.1.1)) (hy : ∀ c, z (.inl (y, c)) = 0)
    (c : Fin 3) : z (.inr (e, c)) = -z (.inl (x, c)) := by
  have h := hz.2 e c
  have h0 := hy c
  rcases hxy with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
  · linear_combination h - h0
  · linear_combination h - h0

variable [DecidableEq ι] in
/-- step (ii): S_u ∪ S_w is a clique for every edge -/
theorem union_clique {b : ι → Var G → ZMod 3} (hb : ∀ j, b j ∈ Ker G) (e : Edge G) :
    ∀ j ∈ suppV b e.1.1 ∪ suppV b e.1.2, ∀ k ∈ suppV b e.1.1 ∪ suppV b e.1.2, j ≠ k →
      (coeffGraph b).Adj j k := by
  have main : ∀ x y : V, ((x = e.1.1 ∧ y = e.1.2) ∨ (x = e.1.2 ∧ y = e.1.1)) → ∀ j k,
      j ∈ suppV b x → j ∉ suppV b y → k ∈ suppV b y → k ∉ suppV b x → j ≠ k → (coeffGraph b).Adj j k := by
    intro x y hxy j k hj hj' hk hk' hjk
    rw [not_mem_suppV] at hj' hk'
    have hyx : (y = e.1.1 ∧ x = e.1.2) ∨ (y = e.1.2 ∧ x = e.1.1) := by
      rcases hxy with ⟨h1, h2⟩ | ⟨h1, h2⟩
      · exact Or.inr ⟨h2, h1⟩
      · exact Or.inl ⟨h2, h1⟩
    obtain ⟨c, h1, h2⟩ := common_colour (hb j) (hb k) (mem_suppV.1 hj) (mem_suppV.1 hk)
    rw [coeffGraph, SimpleGraph.fromRel_adj]
    refine ⟨hjk, Or.inl ⟨.inr (e, c), ?_, ?_⟩⟩
    · rw [edge_coord (hb j) e hxy hj' c]; exact neg_ne_zero.2 h1
    · rw [edge_coord (hb k) e hyx hk' c]; exact neg_ne_zero.2 h2
  intro j hj k hk hjk
  rw [Finset.mem_union] at hj hk
  rcases hj with hj | hj <;> rcases hk with hk | hk
  · exact suppV_clique hb _ j hj k hk hjk
  · by_cases hk1 : k ∈ suppV b e.1.1
    · exact suppV_clique hb _ j hj k hk1 hjk
    by_cases hj2 : j ∈ suppV b e.1.2
    · exact suppV_clique hb _ j hj2 k hk hjk
    exact main _ _ (Or.inl ⟨rfl, rfl⟩) j k hj hj2 hk hk1 hjk
  · by_cases hk2 : k ∈ suppV b e.1.2
    · exact suppV_clique hb _ j hj k hk2 hjk
    by_cases hj1 : j ∈ suppV b e.1.1
    · exact suppV_clique hb _ j hj1 k hk hjk
    exact main _ _ (Or.inr ⟨rfl, rfl⟩) j k hj hj1 hk hk2 hjk
  · exact suppV_clique hb _ j hj k hk hjk

variable [DecidableEq ι] in
theorem adj_union_clique {b : ι → Var G → ZMod 3} (hb : ∀ j, b j ∈ Ker G) {u w : V} (h : G.Adj u w) :
    ∀ j ∈ suppV b u ∪ suppV b w, ∀ k ∈ suppV b u ∪ suppV b w, j ≠ k → (coeffGraph b).Adj j k := by
  rcases lt_or_gt_of_ne (G.ne_of_adj h) with hl | hl
  · exact union_clique hb ⟨(u, w), hl, h⟩
  · rw [Finset.union_comm]; exact union_clique hb ⟨(w, u), hl, h.symm⟩

variable [DecidableEq ι] in
/-- step (iii): |⋃_{v ∈ X} S_v| ≥ 2|X| -/
theorem two_card_le {b : ι → Var G → ZMod 3} (hspan : Submodule.span (ZMod 3) (Set.range b) = Ker G)
    (X : Finset V) : 2 * X.card ≤ (X.biUnion (suppV b)).card := by
  classical
  set J := X.biUnion (suppV b) with hJ
  let f : X × Fin 2 → Var G := fun p => .inl (p.1.1, Fin.castSucc p.2)
  let π := LinearMap.funLeft (ZMod 3) (ZMod 3) f
  have htop : Submodule.span (ZMod 3) (Set.range fun j : J => π (b j)) = ⊤ := by
    rw [eq_top_iff]
    intro a _
    let a' : V × Fin 2 → ZMod 3 := fun p => if h : p.1 ∈ X then a (⟨p.1, h⟩, p.2) else 0
    have hmem : phi (G := G) a' ∈ Submodule.span (ZMod 3) (Set.range b) := hspan ▸ phi_mem a'
    have h1 : π (phi a') ∈ Submodule.span (ZMod 3) (π '' Set.range b) :=
      Submodule.apply_mem_span_image_of_mem_span π hmem
    have h2 : π (phi a') = a := by
      funext ⟨⟨v, hv⟩, i⟩
      fin_cases i <;> simp [π, f, LinearMap.funLeft_apply, phi, xval, a', hv]
    rw [← h2]
    refine (Submodule.span_le.2 ?_) h1
    rintro _ ⟨_, ⟨j, rfl⟩, rfl⟩
    by_cases hj : j ∈ J
    · exact Submodule.subset_span ⟨⟨j, hj⟩, rfl⟩
    · have hz : π (b j) = 0 := by
        funext ⟨⟨v, hv⟩, i⟩
        have hjv : j ∉ suppV b v := fun h => hj (Finset.mem_biUnion.2 ⟨v, hv, h⟩)
        rw [not_mem_suppV] at hjv
        simp [π, f, LinearMap.funLeft_apply, hjv]
      rw [hz]
      exact Submodule.zero_mem _
  have hle := finrank_range_le_card (R := ZMod 3) (fun j : J => π (b j))
  rw [Set.finrank, htop, finrank_top, Module.finrank_fintype_fun_eq_card] at hle
  simpa [Fintype.card_prod, mul_comm] using hle

/-- MAIN (lower bound): if some basis of the GF(3) kernel of F(G) has a coefficient graph of treewidth <= w,
then G has treewidth <= k for some k with 2k+1 <= w; i.e. w*(F(G)) >= 2 tw(G) + 1. -/
theorem tw_le_of_coeff_tw [Fintype V] [Nonempty V] [DecidableEq ι] (b : ι → Var G → ZMod 3)
    (hli : LinearIndependent (ZMod 3) b) (hspan : Submodule.span (ZMod 3) (Set.range b) = Ker G)
    (w : ℕ) (h : TwLe (coeffGraph b) w) : ∃ k, 2 * k + 1 ≤ w ∧ TwLe G k := by
  obtain ⟨D⟩ := h
  have hb : ∀ j, b j ∈ Ker G := fun j => hspan ▸ Submodule.subset_span ⟨j, rfl⟩
  have hS2 : ∀ v, 2 ≤ (suppV b v).card := fun v => by simpa using two_card_le hspan {v}
  have hSne : ∀ v, (suppV b v).Nonempty := fun v => Finset.card_pos.1 (by have := hS2 v; omega)
  have hcov : ∀ v, ∃ t, suppV b v ⊆ D.bag t :=
    fun v => (clique_bags D _ (hSne v) (suppV_clique hb v)).1
  have hwid : ∀ t, 2 * (Finset.univ.filter fun v => suppV b v ⊆ D.bag t).card ≤ w + 1 := by
    intro t
    calc 2 * _ ≤ ((Finset.univ.filter fun v => suppV b v ⊆ D.bag t).biUnion (suppV b)).card :=
          two_card_le hspan _
      _ ≤ (D.bag t).card :=
          Finset.card_le_card (Finset.biUnion_subset.2 fun v hv => (Finset.mem_filter.1 hv).2)
      _ ≤ w + 1 := D.width t
  obtain ⟨v0⟩ := ‹Nonempty V›
  have hw : 1 ≤ w := by
    obtain ⟨t, ht⟩ := hcov v0
    have h1 := hS2 v0
    have h2 := Finset.card_le_card ht
    have h3 := D.width t
    omega
  refine ⟨(w - 1) / 2, (by omega), ⟨{
    T := D.T, tree := D.tree, isTree := D.isTree,
    bag := fun t => (Finset.univ.filter fun v => suppV b v ⊆ D.bag t),
    cover := ?_, edge := ?_, conn := ?_, width := ?_ }⟩⟩
  · intro v
    obtain ⟨t, ht⟩ := hcov v
    exact ⟨t, by simpa using ht⟩
  · intro u v huv
    obtain ⟨t, ht⟩ := (clique_bags D _ ((hSne u).mono Finset.subset_union_left)
      (adj_union_clique hb huv)).1
    rw [Finset.union_subset_iff] at ht
    exact ⟨t, by simpa using ht.1, by simpa using ht.2⟩
  · intro v
    have hs : {t | v ∈ (Finset.univ.filter fun v => suppV b v ⊆ D.bag t)} = {t | suppV b v ⊆ D.bag t} := by
      ext t; simp
    rw [hs]
    exact (clique_bags D _ (hSne v) (suppV_clique hb v)).2
  · intro t
    have := hwid t
    omega

/-- EQUALITY, packaged without a min: a kernel basis with coefficient treewidth <= 2k+1 exists iff tw(G) <= k. -/
theorem wstar_eq_iff [Fintype V] [Nonempty V] (k : ℕ) :
    (∃ b : V × Fin 2 → Var G → ZMod 3, LinearIndependent (ZMod 3) b ∧
      Submodule.span (ZMod 3) (Set.range b) = Ker G ∧ TwLe (coeffGraph b) (2 * k + 1)) ↔ TwLe G k := by
  constructor
  · rintro ⟨b, hli, hspan, h⟩
    obtain ⟨k', hk', h'⟩ := tw_le_of_coeff_tw b hli hspan _ h
    exact twLe_mono h' (by omega)
  · exact wstar_le_two_tw_add_one k

end Lower

end PNP001
