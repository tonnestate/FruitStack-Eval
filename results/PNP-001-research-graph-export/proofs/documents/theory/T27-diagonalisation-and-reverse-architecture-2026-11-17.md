# T27 — Diagonalisation (owner's language D) and the reverse architecture "P = NP ⇒ faster simulation ⇒ hierarchy contradiction" (PI, 2026-11-17)

STATUS: classical facts, assembled and checked. Lemma E independently checked through FruitStack/PlumMe (gpt-oss-120b, receipt
receipt_c1a0fc2fc8744cf994155e5a65417246: all six claims CORRECT). No new theorem; no ledger entry.

## 1. The owner's language and Lemma E
x = <M, 1^k, 0^r>, N = |x|; D = { x valid : M does not accept x within N^k steps }; U = valid encodings minus D.
- D ∉ P: correct (owner's proof = time-hierarchy diagonalisation; it relativises).
- Lemma E: U and D are EXP-complete under polynomial-time many-one reductions.
  In EXP: k <= N (unary), N^k <= 2^{N log N}. Hard: for L ∈ DTIME(2^{n^c}) via T, map y to <M_y, 1^k, 0^r> with M_y ignoring its
  input and running T on the hard-wired y; padding gives N >= 2|y|^c + |M_y| and k = floor(N/2), so N^k >= 2^{|y|^c}.
- Consequence: D ∈ NP ⇔ EXP ⊆ NP ⇔ NP = EXP. A certificate mechanism for D would prove NP = EXP — open, strictly stronger than
  P ≠ NP (P ≠ EXP by the hierarchy), and generally believed false. Any such proof must be non-relativizing: relative to a
  Baker–Gill–Solovay oracle O with P^O = NP^O, D^O ∉ P^O = NP^O.
- Variant D_g (exponent k <= g(N), g unbounded, slowly growing): still D_g ∉ P; D_g ∈ NP would put a superpolynomial deterministic
  time class DTIME(N^{g(N)}) inside NP — still strictly stronger than P ≠ NP (status open).
- Owner's corrections of the pasted text adopted: relativization does not forbid diagonalisation combined with non-relativizing
  arguments (indirect diagonalisation, Williams' ACC lower bounds); a hierarchy theorem does not place a SPECIFIC language outside a
  class; non-acceptance with a variable exponent is not automatically coNP-complete (for D it is EXP-complete, Lemma E).

## 2. The reverse architecture: the exact runtime inequality it needs
Assume P = NP. Then PH = P, so for every k there is c_k with Σ_k TIME(n) ⊆ DTIME(n^{c_k}), and by padding
Σ_k TIME(t) ⊆ DTIME(t^{c_k}) for time-constructible t >= n. The exponent c_k is NOT under our control.
SUFFICIENT speed-up lemma S: there is a FIXED k such that for every ε > 0, DTIME(t) ⊆ Σ_k TIME(t^ε) (for t >= n^{1/ε}, so the
alternating machine can read its input), with all costs of producing and using the existential/universal guesses included.
Proof that S suffices: P = NP ⇒ DTIME(t) ⊆ Σ_k TIME(t^ε) ⊆ DTIME(t^{ε c_k}); pick ε < 1/(2c_k) ⇒ DTIME(t) ⊆ DTIME(t^{1/2}),
contradicting the deterministic time hierarchy for t = n^K, K large. Hence S ⇒ P ≠ NP.
Why the owner's first attempt fails, in these terms: the tableau/SAT encoding of a T-step computation has size poly(T); a poly-time
SAT algorithm takes poly(T) on it — no speed-up, i.e. no fixed-alternation compression of deterministic time.
Why a fixed k is essential: with UNBOUNDED alternation, time can be compressed (DTIME(t) ⊆ DSPACE(t/log t) by Hopcroft–Paul–Valiant;
DSPACE(s) ⊆ ATIME(s^2); Williams' square-root-space simulation, not re-checked here) — but ATIME(poly) = PSPACE does not collapse to
P under P = NP, so no contradiction follows.
Strength of S: S ⇒ DTIME(t) ⊆ DSPACE(t^ε) for all ε ⇒ P ≠ PSPACE (if P = PSPACE then DSPACE(n) ⊆ DTIME(n^K) ⊆ DSPACE(n^{Kε}),
contradicting the space hierarchy for ε < 1/K). S is therefore itself a major open statement.

## 3. What is known about this architecture (primary literature)
- This is the "alternation-trading" method: speed-up steps (simulate deterministic time with fewer steps and more alternations) and
  slow-down steps (remove alternations using the assumption), ending in a hierarchy contradiction.
- It works where speed-up lemmas exist: with small space, DTISP(t, s) ⊆ Σ_{2k} TIME(t^{1/k}·s)-type lemmas (Nepomnjaščij, Kannan)
  give polynomial speed-ups with a fixed number of alternations. Results: SAT ∉ DTISP(n^c, n^{o(1)}) for c < 2cos(π/7) ≈ 1.8019
  (Fortnow; Fortnow–Lipton–van Melkebeek–Viglas; Williams).
- Buss–Williams (CCC 2012; Comput. Complexity 24 (2015) 533–600, read in abstract): 2cos(π/7) is the BEST exponent obtainable by
  alternation-trading proofs for SAT vs DTISP(n^c, n^ε) with ε = 0 — a proven limit of the method.
- Without a space bound, the only known fixed-alternation speed-up is tiny: Paul–Pippenger–Szemerédi–Trotter (multitape TMs)
  DTIME(t) ⊆ Σ_4 TIME(t/log* t), which yields DTIME(n) ≠ NTIME(n) — a factor log* t, far below the polynomial factor t^{1-ε} that
  Lemma S needs to absorb the unknown exponent c_k.

## Decision (gate)
Diagonal route via D: equivalent to NP = EXP — NO LEVER (strictly stronger than the target, believed false).
Reverse architecture: well-defined target = Lemma S (fixed-alternation polynomial speed-up of deterministic time). Open; implies
P ≠ PSPACE as well; the known machinery (alternation trading) has a proven ceiling in the space-bounded setting and only a log*
speed-up without space bounds. Recorded as the precise open runtime inequality; no computation.

## 4. Owner's reformulation as a translation problem (2026-11-17)
A polynomial-time map f with x ∈ D ⇔ f(x) ∈ SAT would transfer D's proven hardness to SAT — and would itself prove D ∈ NP.
By Lemma E such f exists iff NP = EXP. General form: a language provably outside P via a hierarchy theorem is complete for some class
X ⊋ P (EXP; or DTIME(n^{g(n)}) for unbounded slowly growing g); a reduction from it to SAT exists iff X ⊆ NP. The translation route
therefore proves "NP contains a superpolynomial deterministic time class" — strictly stronger than P ≠ NP. If P ≠ NP holds but NP
contains no DTIME(t) with t superpolynomial, the route is impossible in principle. No lever beyond §1–§3.
