# T46 — Learning from a refutation: what the matroid-port property actually measures (director, 2026-11-18)

Owner addendum 2026-11-18 ("Discovery through errors"), required demonstration. Scripts: lab/transfer/p4_control.py,
port_vs_polymorphism.py, nand3_candidate.py; lab/ports/nae6_port.py. Critique: PlumMe W-e969a14e0b2b4ebc.

1. Original statement (K, implicit since D-011): "failure to be a matroid port (D-013 obstruction) indicates computational hardness".
2. Why it failed: the only control was XOR-SAT, a GF(2) port BY CONSTRUCTION; the property was never tested on a tractable non-affine problem.
3. Counterexample (D-020): 2-SAT n=3 has a P4 minor, hence is a non-port for all n >= 3, yet is in P.
4. New search space revealed: if port-ness does not track hardness, the contrast "1-in-3 vs XOR" (hard vs easy) was confounded with
   "non-affine vs affine". Port-ness may track an ALGEBRAIC property of the constraint language (Schaefer / polymorphism level), not complexity.
   Supporting coincidence found during this analysis: the first n=6 non-port certificate of D-013 is built around the D-008 witness
   {012, 013, 023, 045, 124}, which is exactly an orbit representative of the first GF(3) GAP cores (T44) - the non-port obstruction of
   1-in-3 appears exactly when its GF(3)-affine description stops being exact (n=6).
5. New hypothesis H_aff: for a Boolean constraint language G with non-trivial UNSAT, UNSAT_n(G) is a matroid port for every n iff every
   relation of G is GF(2)-affine (closed under x^y^z). "If": proved (UNSAT = GF(2) inconsistency = ideal GF(2) monotone span program).
   "Only if": conjecture. 1-in-3 refines it: GF(3)-affine description exact for n <= 5 (D-012, T44) <=> port for n <= 5.
6. Tests (P4 minor = non-port certificate; absence proves nothing):
   | language | Schaefer class | complexity | result |
   | XOR-3 (n=4), XOR-2 (n=4) | affine | P | no P4 (consistent: ports for all n, proved) |
   | 2-SAT (n=3) | bijunctive | P | P4 |
   | Horn (n=3: x, ~x|~y, ~x|y) | Horn | P | P4 |
   | dual Horn (n=3) | dual Horn | P | P4 |
   | positive 1-in-3 | none | NP-c | port n<=5 (GF(3)), P4-type obstruction n>=6 (D-013) |
   | positive NAE-3 | none | NP-c | no P4 at n=5; n=6 search inconclusive (all 428 minimal UNSAT sets have size 10) |
   | C0, C1, NAND3 (referee's candidate counterexample) | non-affine | P? (with constants: Horn-type) | P4 at n=3 (a=[x0=0], b=[x0=1], c=[x1=1], d=[x1=0] with C1(x2), NAND(x0,x1,x2) fixed) - candidate refuted |
   Independent critique: Haiku found no counterexample, proposed the NAND3 candidate (refuted above), noted the open case of non-affine
   ternary relations mixed with affine ones and NAE. Gemma asserted "port preserved under pp-definitions" - UNSUPPORTED (no argument;
   existential quantification is not a clutter minor operation) - rejected.
7. Result and relevance. H_aff survives every test; tractable non-affine (2-SAT, Horn, dual Horn) and hard non-affine (1-in-3) behave
   ALIKE, affine behaves differently. So the matroid-port property is an algebraic affineness detector, orthogonal to the P / NP-complete
   divide of Schaefer's theorem. Relevance to P != NP: NEGATIVE but precise - it explains WHY the D-011..D-013 programme could not carry
   hardness (it measured affineness), and it explains the n=6 threshold of D-013 by the T44 GAP cores (the end of 1-in-3's GF(3)-affine
   description). Open mathematical obligation (not complexity-relevant, kept as mathematics): prove "only if" of H_aff, e.g. via a
   pp-style construction of P4 from any non-affine relation plus the relations needed for non-trivial UNSAT; decide NAE-3 by a
   certified (non-random) port test.
