/- PNP-001 ACC0 level 3 (director, 2026-11-20): formal checks of
   claim:53f46be7d6fc (OR_n not an AND of GF(3)-linear equalities, n >= 2),
   claim:03fced129264 (OR_n not an AND of equalities and dis-equalities, n >= 3 - Davenport),
   claim:1a3685a2808b (a GF(3)-affine function with Boolean values on the cube depends on at most one variable). -/
import Mathlib

namespace ACC0L3
open BigOperators

/-- linear form `∑ a_i x_i` over GF(3) -/
def lf {n : ℕ} (a x : Fin n → ZMod 3) : ZMod 3 := ∑ i, a i * x i

/-- unit vector -/
def e {n : ℕ} (i : Fin n) : Fin n → ZMod 3 := fun j => if j = i then 1 else 0

def IsBool {n : ℕ} (x : Fin n → ZMod 3) : Prop := ∀ i, x i = 0 ∨ x i = 1

lemma lf_add {n : ℕ} (a x y : Fin n → ZMod 3) : lf a (x + y) = lf a x + lf a y := by
  simp [lf, mul_add, Finset.sum_add_distrib]

lemma lf_zero {n : ℕ} (a : Fin n → ZMod 3) : lf a 0 = 0 := by simp [lf]

lemma lf_single {n : ℕ} (a : Fin n → ZMod 3) (i : Fin n) : lf a (e i) = a i := by
  simp [lf, e]

lemma bool_single {n : ℕ} (i : Fin n) : IsBool (e i) := by
  intro j; by_cases h : j = i <;> simp [e, h]

lemma bool_single_add {n : ℕ} (i j : Fin n) (hij : i ≠ j) : IsBool (e i + e j) := by
  intro k; by_cases h1 : k = i <;> by_cases h2 : k = j <;> simp_all [e]

lemma single_ne_zero {n : ℕ} (i : Fin n) : (e i) ≠ 0 := by
  intro h; have := congrFun h i; simp [e] at this

lemma single_add_ne_zero {n : ℕ} (i j : Fin n) (hij : i ≠ j) : (e i + e j) ≠ 0 := by
  intro h; have := congrFun h i; simp [e, hij] at this

lemma bool_triple {n : ℕ} (i j k : Fin n) (hij : i ≠ j) (hik : i ≠ k) (hjk : j ≠ k) : IsBool (e i + e j + e k) := by
  intro q; simp only [Pi.add_apply, e]; split_ifs <;> subst_vars <;> simp_all

lemma triple_ne_zero {n : ℕ} (i j k : Fin n) (hij : i ≠ j) (hik : i ≠ k) : (e i + e j + e k) ≠ 0 := by
  intro h; have := congrFun h i; simp [e, hij, hik] at this

/-- one GF(3) equality that holds at e_i, e_j, e_i + e_j holds at 0 (coefficients 1 + 1 - 1 = 1) -/
lemma eq_at_zero {n : ℕ} (a : Fin n → ZMod 3) (c : ZMod 3) (i j : Fin n)
    (h1 : lf a (e i) = c) (h2 : lf a (e j) = c)
    (h3 : lf a (e i + e j) = c) : lf a 0 = c := by
  rw [lf_add, h1, h2] at h3
  have key : ∀ c : ZMod 3, c + c = c → c = 0 := by decide
  rw [lf_zero, key c h3]

/-- claim:53f46be7d6fc: no AND of GF(3)-linear equalities accepts exactly the nonzero Boolean vectors (n ≥ 2). -/
theorem or_not_C0 (n m : ℕ) (hn : 2 ≤ n) (g : Fin m → (Fin n → ZMod 3) × ZMod 3) :
    ¬ (∀ x : Fin n → ZMod 3, IsBool x → ((∀ j, lf (g j).1 x = (g j).2) ↔ x ≠ 0)) := by
  intro h
  let i : Fin n := ⟨0, by omega⟩
  let j : Fin n := ⟨1, by omega⟩
  have hij : i ≠ j := by simp [i, j, Fin.ext_iff]
  have A := (h _ (bool_single i)).2 (single_ne_zero i)
  have B := (h _ (bool_single j)).2 (single_ne_zero j)
  have C := (h _ (bool_single_add i j hij)).2 (single_add_ne_zero i j hij)
  have Z : ∀ k, lf (g k).1 0 = (g k).2 := fun k => eq_at_zero _ _ i j (A k) (B k) (C k)
  exact ((h 0 (fun _ => Or.inl rfl)).1 Z) rfl

/-- Davenport constant of Z_3 is 3: three elements always have a nonempty zero-sum subsequence. -/
lemma zero_sum3 : ∀ a b c : ZMod 3,
    a = 0 ∨ b = 0 ∨ c = 0 ∨ a + b = 0 ∨ a + c = 0 ∨ b + c = 0 ∨ a + b + c = 0 := by decide

/-- claim:03fced129264: no AND of GF(3) equalities and dis-equalities accepts exactly the nonzero Boolean vectors (n ≥ 3). -/
theorem or_not_D (n m p : ℕ) (hn : 3 ≤ n) (g : Fin m → (Fin n → ZMod 3) × ZMod 3)
    (d : Fin p → (Fin n → ZMod 3) × ZMod 3) :
    ¬ (∀ x : Fin n → ZMod 3, IsBool x →
        (((∀ j, lf (g j).1 x = (g j).2) ∧ (∀ k, lf (d k).1 x ≠ (d k).2)) ↔ x ≠ 0)) := by
  intro h
  let i0 : Fin n := ⟨0, by omega⟩
  let i1 : Fin n := ⟨1, by omega⟩
  let i2 : Fin n := ⟨2, by omega⟩
  have h01 : i0 ≠ i1 := by simp [i0, i1, Fin.ext_iff]
  have h02 : i0 ≠ i2 := by simp [i0, i2, Fin.ext_iff]
  have h12 : i1 ≠ i2 := by simp [i1, i2, Fin.ext_iff]
  -- 0 is rejected
  have rej : ¬ ((∀ j, lf (g j).1 0 = (g j).2) ∧ (∀ k, lf (d k).1 0 ≠ (d k).2)) :=
    fun hh => ((h 0 (fun _ => Or.inl rfl)).1 hh) rfl
  have A := (h _ (bool_single i0)).2 (single_ne_zero i0)
  have B := (h _ (bool_single i1)).2 (single_ne_zero i1)
  have C := (h _ (bool_single_add i0 i1 h01)).2 (single_add_ne_zero i0 i1 h01)
  have E0 : ∀ j, lf (g j).1 0 = (g j).2 := fun k => eq_at_zero _ _ i0 i1 (A.1 k) (B.1 k) (C.1 k)
  -- so some dis-equality k has lf a 0 = c, i.e. c = 0
  obtain ⟨k, hk⟩ : ∃ k, lf (d k).1 0 = (d k).2 := by
    by_contra hne; push Not at hne; exact rej ⟨E0, hne⟩
  rw [lf_zero] at hk
  set a := (d k).1
  -- every nonzero Boolean x satisfies lf a x ≠ 0
  have acc : ∀ x, IsBool x → x ≠ 0 → lf a x ≠ 0 := fun x hb hx => by
    have := ((h x hb).2 hx).2 k; exact fun hz => this (hz.trans hk)
  have s0 := acc _ (bool_single i0) (single_ne_zero i0); rw [lf_single] at s0
  have s1 := acc _ (bool_single i1) (single_ne_zero i1); rw [lf_single] at s1
  have s2 := acc _ (bool_single i2) (single_ne_zero i2); rw [lf_single] at s2
  have s01 := acc _ (bool_single_add i0 i1 h01) (single_add_ne_zero i0 i1 h01)
  have s02 := acc _ (bool_single_add i0 i2 h02) (single_add_ne_zero i0 i2 h02)
  have s12 := acc _ (bool_single_add i1 i2 h12) (single_add_ne_zero i1 i2 h12)
  rw [lf_add, lf_single, lf_single] at s01 s02 s12
  -- the triple e0 + e1 + e2
  have b3 := bool_triple i0 i1 i2 h01 h02 h12
  have n3 := triple_ne_zero i0 i1 i2 h01 h02
  have s012 := acc _ b3 n3
  rw [lf_add, lf_add, lf_single, lf_single, lf_single] at s012
  rcases zero_sum3 (a i0) (a i1) (a i2) with z | z | z | z | z | z | z <;> contradiction

/-- claim:1a3685a2808b: if c + ∑ a_i u_i ∈ {0,1} for every Boolean u, then no two coefficients are nonzero
    (the function is a constant or a literal). -/
theorem affine_bool_is_literal (n : ℕ) (a : Fin n → ZMod 3) (c : ZMod 3)
    (h : ∀ u : Fin n → ZMod 3, IsBool u → c + lf a u = 0 ∨ c + lf a u = 1) :
    ∀ i j, i ≠ j → a i = 0 ∨ a j = 0 := by
  intro i j hij
  have h0 := h 0 (fun _ => Or.inl rfl); rw [lf_zero, add_zero] at h0
  have hi := h _ (bool_single i); rw [lf_single] at hi
  have hj := h _ (bool_single j); rw [lf_single] at hj
  have hij' := h _ (bool_single_add i j hij); rw [lf_add, lf_single, lf_single, ← add_assoc] at hij'
  have key : ∀ c x y : ZMod 3, (c = 0 ∨ c = 1) → (c + x = 0 ∨ c + x = 1) → (c + y = 0 ∨ c + y = 1) →
      (c + x + y = 0 ∨ c + x + y = 1) → x = 0 ∨ y = 0 := by decide
  exact key c (a i) (a j) h0 hi hj hij'

/-- the other direction of claim:03fced129264 for n = 2: OR_2 is the single dis-equality x0 + x1 ≠ 0 -/
theorem or2_in_D (x : Fin 2 → ZMod 3) (hb : IsBool x) : (lf (fun _ => 1) x ≠ 0 ↔ x ≠ 0) := by
  have hx : x = fun i => if i = 0 then x 0 else x 1 := by
    funext i; fin_cases i <;> rfl
  rcases hb 0 with h0 | h0 <;> rcases hb 1 with h1 | h1 <;>
    · rw [hx]; simp only [lf, Fin.sum_univ_two, ne_eq, funext_iff, Fin.forall_fin_two, Pi.zero_apply]; simp [h0, h1] <;> decide

/-- ... and for n = 1: OR_1 is the equality x0 = 1 -/
theorem or1_in_C0 (x : Fin 1 → ZMod 3) (hb : IsBool x) : (lf (fun _ => 1) x = 1 ↔ x ≠ 0) := by
  rcases hb 0 with h0 | h0 <;> simp [lf, h0, funext_iff, Fin.forall_fin_one]

/-- finishing step of claim:1a3685a2808b: the function is a constant, u_i (c = 0, a_i = 1) or 1 - u_i (c = 1, a_i = 2) -/
theorem affine_bool_classified (n : ℕ) (a : Fin n → ZMod 3) (c : ZMod 3)
    (h : ∀ u : Fin n → ZMod 3, IsBool u → c + lf a u = 0 ∨ c + lf a u = 1) :
    ((∀ i, a i = 0) ∧ (c = 0 ∨ c = 1)) ∨
    ∃ i, (∀ j, j ≠ i → a j = 0) ∧ ((c = 0 ∧ a i = 1) ∨ (c = 1 ∧ a i = 2)) := by
  have h0 := h 0 (fun _ => Or.inl rfl); rw [lf_zero, add_zero] at h0
  by_cases hall : ∀ i, a i = 0
  · exact Or.inl ⟨hall, h0⟩
  · push Not at hall
    obtain ⟨i, hi⟩ := hall
    refine Or.inr ⟨i, fun j hj => ?_, ?_⟩
    · rcases affine_bool_is_literal n a c h i j (Ne.symm hj) with z | z
      · exact absurd z hi
      · exact z
    · have he := h _ (bool_single i); rw [lf_single] at he
      have key : ∀ c x : ZMod 3, x ≠ 0 → (c = 0 ∨ c = 1) → (c + x = 0 ∨ c + x = 1) →
          (c = 0 ∧ x = 1) ∨ (c = 1 ∧ x = 2) := by decide
      exact key c (a i) hi h0 he

end ACC0L3
