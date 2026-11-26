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

end PNP001
