import Mathlib.Combinatorics.SimpleGraph.Acyclic
import Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected
import Mathlib.Data.Fintype.Prod

/-! PNP-001, w*(F(G)) upper bound, step 2 (graph part).
Tree decompositions (not in Mathlib), the 2-blow-up of a graph, and: width k for G gives width 2k+1 for the blow-up. -/

namespace PNP001

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

end PNP001
