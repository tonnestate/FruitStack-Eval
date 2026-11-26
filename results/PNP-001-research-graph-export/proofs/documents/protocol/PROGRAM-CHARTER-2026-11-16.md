# PNP-001 — Program charter (owner reframing, 2026-11-16 late)

Supersedes the narrow GODMODE mandate ("investigate the SOSA 2026 subtraction reduction"). The SOSA reduction was the FIRST concrete
object, not the boundary of the program (owner, 2026-11-16).

## Leitfrage

> **Which new algebraic structure enables a provably more efficient exact computation?**
> Every structure found is then tested for its actual contribution to P vs NP.

Sub-questions (owner): new computation operations (combine/summarize/eliminate possibilities instead of enumerating them); alternative
information representations (historical arithmetic, graphs, polynomials, other algebras); exactly proven algebraic methods from quantum
and nanophysics outside their original models; structural causes of the easy/hard transition (bioinformatics, statistical physics);
transferable constructions (not analogies) from astrophysics / mathematical physics; **computation, not representation** — a real
reduction of work, not a more compact notation.

## PI finding that shapes the search: the fields converge on a few objects

Status: map from the PI's knowledge of the literature. Each anchor is marked **[verify]** until checked against the primary text; nothing
from this table enters the ledger before that check.

| Field / method | Exact mathematical object | Known boundary (efficient vs. hard) |
|---|---|---|
| Generalized distributive law, semirings, variable elimination | sum-product over a hypergraph; cost exponential in treewidth | ETH-tight: treewidth cannot be beaten for CSP/#CSP (Marx, ToC 2010) [verify] |
| Möbius/zeta transforms | subset lattice transforms, subset convolution O(2^n n^2) | improve the base of 2^n, never polynomial for NP-hard problems (Björklund–Husfeldt–Kaski–Koivisto, STOC 2007) [verify] |
| Holographic algorithms, Fibonacci gates, Pfaffians (FKT) | matchgates + local basis change | complete dichotomies for #CSP / Holant: tractable iff affine, product type, or holographically matchgate-realizable (planar); else #P-hard (Cai–Chen JACM 2017; Cai–Lu–Xia) [verify] |
| Quantum: free fermions; stabilizer circuits | free fermions = matchgates (Valiant SICOMP 2002; Terhal–DiVincenzo PRA 2002); stabilizer = affine (Gottesman–Knill) | the classically simulable quantum models ARE the tractable cases of the Holant dichotomy; bosons → permanent → #P-hard (Aaronson–Arkhipov 2011) [verify] |
| Fermion vs. boson ↔ algebra | determinant (Pfaffian) vs. permanent | VP vs VNP; determinantal complexity dc(perm_n) ≥ n²/2 (Mignon–Ressayre 2004), best upper 2^n; GCT occurrence obstructions ruled out (Bürgisser–Ikenmeyer–Panova, JAMS 2019) [verify] |
| Statistical physics: exactly solvable models, zero-free regions | Kasteleyn/Pfaffian for planar Ising; Lee–Yang zeros; Barvinok interpolation | approximate counting is efficient exactly up to phase transitions (Weitz STOC 2006; Sly FOCS 2010; Patel–Regts SICOMP 2017) [verify] |
| Lovász local lemma ↔ statistical physics | Shearer region = zero-free region of the independence polynomial (Scott–Sokal 2005); algorithmic via Moser–Tardos (JACM 2010) | for (k,s)-SAT the LLL bound is asymptotically the exact NP-completeness threshold: f(k) = (2/e + o(1))·2^k/k (Gebauer–Szabó–Tardos; Kratochvíl–Savický–Tuza) [verify] |
| Bioinformatics: RNA folding | non-crossing structures → interval dynamic programming | pseudoknots (crossing) → NP-hard (Lyngsø–Pedersen 2000): planarity/non-crossing is the transition [verify] |
| Mathematical physics: integrable vertex models (Yang–Baxter, Bethe ansatz) | six-/eight-vertex models as Holant problems | covered by the Holant dichotomies for these models (Cai et al.) [verify] |
| Historical arithmetic; FFT; Strassen | change of representation (positional notation, logarithms, Fourier basis) | polynomial speed-ups; the counting-world analogue of a basis change is exactly Valiant's holographic transformation |
| Decision CSP (existence, not counting) | polymorphism algebra | Bulatov / Zhuk 2017: CSP(Γ) ∈ P iff Γ has a weak near-unanimity polymorphism, else NP-complete [verify] |
| Representation vs. computation | knowledge compilation (OBDD, d-DNNF, SDD), extended formulations, SoS, IPS | proven size lower bounds for whole families: d-DNNF (Bova–Capelli–Mengel–Slivovsky 2016), LP extended formulations (Fiorini et al. 2012; Rothvoss 2014), SoS (Grigoriev 2001), IPS ⟺ algebraic circuit lower bounds (Grochow–Pitassi 2018) [verify] |

**Consequence (the structural test every candidate must pass).**
- **S1 Placement.** Where does the candidate fall on this map? Inside a known tractable class → known mathematics, no P vs NP
  contribution. On the hard side of a dichotomy → its claim IS "P = NP" (resp. FP = #P) and must be checked hardest — this is exactly
  what happened to the SOSA reduction (T4: lands in GapP, the shortcut would be SAT itself).
- **S2 Computation, not representation.** Does the needed query run in polynomial time on the representation? Does a proven size lower
  bound for the representation family (compilation, extended formulation, SoS, monotone, ROABP) already exclude it?
- **S3 Contribution.** Real room exists only where the dichotomies and the representation lower bounds do not reach: non-local or
  instance-dependent transformations (the Holant dichotomies fix the signature set and use local basis changes), and unrestricted
  algebraic models (VP vs VNP, IPS, dc(perm)). On the lower-bound side the barriers apply (relativization, natural proofs,
  algebrization, locality — T3, T5). An ALGORITHM is not subject to these barriers; there the dichotomies are the test.

## Objects (status)

- **O0 — SOSA 2026 paired cancellation:** CLOSED (T4; refutation + LIMITATION in the ledger, seq 90–92).
- **O1 — Fermion/boson boundary (det vs perm):** can non-local or instance-dependent transformations bring permanent-type sums into
  Pfaffian form on families that matter? Test against the Holant dichotomy and Mignon–Ressayre.
- **O2 — Zero-free regions as decision procedures:** DE-PRIORITIZED, not closed by a barrier (T6 §7, correction 2026-11-17, ledger
  seq 101–104). Counting/zero-free/sampling live in the pD² regime (D ≲ 2^{k/2}, tight under NP≠RP; Liu–Wang–Yin–Zhang–Zhou
  arXiv:2608.08616), strictly inside the all-YES decision region (pD regime, D ≲ 2^k), so they say nothing new about decision hardness.
  The earlier "intrinsic padding obstruction / LIMITATION_ESTABLISHED" was WITHDRAWN as a normalization artifact (PhysalisMe
  cm-673ff95932cb4a11: zeros of the partition polynomial under padding lie only at 0 and −7). A certificate deciding SAT above f(k) would
  itself be P=NP (no free lunch, as O0). Reopen per T6 §7.
- **O3 — Representation vs. computation:** use the proven compilation / extended-formulation lower bounds as filters for every new
  representation proposed.
- **Lower-bound side (kept):** T3 §13 / T5 uniform magnification; T5 under independent review.

## Working rules (unchanged)
Primary text before use; independent adversarial review before any result or LIMITATION enters the ledger; finite computations are
evidence, not proofs; failed approaches close the approach, not the program.
