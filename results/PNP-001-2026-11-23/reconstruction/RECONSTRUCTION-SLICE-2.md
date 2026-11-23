# PNP-001 reconstruction, slice 2: route B (2026-11-23)

Source: MMW19, STOC 2019, Section 5, proof of Theorem 1.4 (primary PDF, sha256 prefix `bc6d4178bac7aa09`).

## B.1 What Thm 1.4, bullet 3 asks for (read from its proof)
- **The proof is by contrapositive.** If NP ⊂ P/poly, then PH ⊂ P/poly. Lemma 3.1 with ℓ(n) = s(n)^3 then gives, for every
  n, a circuit of size O(N) and depth O(log N / log s) with Circuit-Min-Merge^A gates. Replacing those gates by poly(s)-size
  circuits gives size N·poly(s) and depth poly(s), at every input length.
- **The hypothesis therefore needs only an infinitely-often lower bound.** Exact form:
  > (B-prem) there are s(n) >= n and A in PH such that for every c, for infinitely many n, search-MCSP^A[s(n)] on
  > N = 2^n inputs has no circuit of size N·s(n)^c and depth s(n)^c.
- **(8) in manuscript v0.25 (line ~79) is almost-everywhere.** Its quantifiers are ∀c,d ∃m0 ∀m >= m0, and it concerns staged
  realizations, i.e. streaming-shaped circuits. A staged realization unrolls to depth of about N, not poly(s).
- **Consequence:** (8) and B-prem are logically different premises for different circuit shapes. Neither implies the
  other by unrolling. Both are sufficient: (8) via Theorem 3, B-prem via MMW Thm 1.4 bullet 3, giving NP not in P/poly and
  hence P != NP.

## B.2 Connection to the gate-elimination target (owner assignment 2026-11-23, Q-10bbdfaf2a target)
- **T_B:** for every k, CC_{B2}(MCSP[m^c]) is not in O(N·m^k), for decision MCSP, any depth, no oracle.
- **Chain**, where A is the empty oracle (in PH) and s(n) = n^c, so poly(s) = polylog N:
  1. T_B gives infinitely many m with no decision circuit of size C·N·m^k.
  2. A search circuit of size N·s^c and any depth would give a decision circuit of the same size up to an additive
     O(s log s) term (the output "is not none").
     - This conversion is the only small lemma in the chain. It depends on the output convention of search-MCSP and
       must be reviewed by a non-Claude family.
     - Seq 9652/9656 (R1421) states the same step.
  3. So B-prem holds. It even holds without the depth bound, which makes B-prem easier to meet, not harder.
  4. MMW Thm 1.4 bullet 3 then gives NP not in P/poly, hence P != NP.
- **Status: CONDITIONAL on T_B.** The best bound in the corpus is linear: the Wittcop claim of about 2N for MCSP[m-1] is an
  unverified preprint (LIT-11). No proof-state step proves T_B.
- **First missing implication of route B:** T_B itself. This is exactly the owner assignment GE-1 to GE-3
  (Q-9154b244de, Q-f269573fe5, Q-d56ff318ed).

## B.3 Corrections to the record
- Seq 11387 (R1809), "Thm 1.4 is a TC0 result", is wrong: it reads bullet 1 only.
- Seq 9656 (R1421) is right on bullet 3. It flagged the quantifier as inferred; the proof text above confirms "infinitely
  often".
- Manuscript v0.25: (8) is stronger than needed in two respects, almost-everywhere quantifiers and staged circuits. The
  manuscript itself says (8) is sufficient, not necessary (line ~451). B-prem with depth poly(s) is a published alternative
  premise. The manuscript is not changed (owner rule).

Verdict for H on route B: **H-NOT-ESTABLISHED**. The first missing implication is T_B, an open lower bound and not a
composition gap. Routes A and C to G are not done yet.
