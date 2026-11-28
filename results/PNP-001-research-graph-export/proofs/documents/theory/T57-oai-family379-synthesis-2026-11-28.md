# T57 — OpenAI family 379: source record, extracted mathematics, and transfer test against P = NP (2026-11-28)

Status: CLAIMED (Claude family only). Symbolic only; no computation, no Lean build. External works are UNVERIFIED by us.
Desk workers stayed stopped. This file only adds; nothing existing was changed.

## 1. Source record (openai/math, HEAD 3344da59991ed94f9ba711217b29c1d760badfa6, 2026-11-25T00:18:47Z, "Merge pull request #6 from openai/codex/update-11-24")
Only the listed PDFs, READMEs, CONTENTS.md entry 379, lean/docs/379.md, lean/formalization.yaml, lean/ComparatorChallenges/MatrixExponent.{lean,json}
and lean/OAI/LinearAlgebra/SpectralBooks/ExactExponent.lean were fetched. No clone. Lean was not built; Comparator was not run.
Repository statement (README): results are "at different stages of verification", "some of the unformalized results could have issues", ~42 % top-line results formalized.

| Paper (preprints/ directory) | paper.pdf sha256 |
|---|---|
| Euclidean-geometry-in-the-asymptotic-spectrum-of-tensors-November-24-2026 | 7800f8d812fefb03a080baf10662fa905cb932aaa3da94c8897eb8477fc385e5 |
| The-matrix-multiplication-exponent-is-nine-fourths-November-24-2026 | ddde9ab7755596c6f0210c148985f9761f2c291582e4d0a045987ad1766e5a01 |
| Paths-trees-and-grids-separate-Valiants-hierarchy-November-24-2026 | 5fb87fe08aba63af8258ae71d8105b6a26c94dd8fec1fe57a45e68e6303edb99 |
| Circuit-lower-bounds-for-Hamiltonian-cycle-and-the-permanent-November-24-2026 | a7bab8a78dfe73c3f59f190d7c6cc289c30c6340e06afaa5514621f88e62be01 |
| The-logarithmic-exponent-of-finite-Fourier-transforms-November-24-2026 | 275bf75a814d5dcffb57ee906e5b7b90d817fbfb0eef66dfd89940b118047523 |
| The-logarithmic-exponent-of-integer-multiplication-on-tapes-November-24-2026 | 238c2cb21352a0fa6aeb2d694fa9a8cae5fae8f0186897222f1c6b911f69daff |
| An-exponential-bound-for-sunflowers-November-24-2026 | 47b3518a852dfa303732ff3158124b4f8d700ac1d4ea983140ff86c649ee990c |
| VP-and-VNP-are-different-November-23-2026 (earlier, T50) | a5c07d8591d5d5cd93620c429e4ba4f9e86cf0ff5b6c3a5f213d36edcd94e811 |
| The-Exponential-Time-Hypothesis-is-False-October-25-2026 (earlier) | 5b1612dc2eebb2cad5b4cbe62d1fed2982f01ab1908c26f70010a651487e8123 |

Only the abstracts, introductions, and for the 9/4 paper §1–§4 (statements and the proof of Prop. 2.3, Lemma 4.1) were read. Sections 5–27 of the 9/4 paper
(sphere tensors, rigidity, synchronization, compression, ~100 pages) were NOT read; nothing below claims to have checked them.

## 2. Exact statements extracted
E1 (Euclid, Thm 1.1). Over any field k and real Hilbert space K there is an assignment H(T;x) to every tensor and placement of its indices, with H(wire between u,v)=||u−v||,
H(Δ_S(q)) = W(S) log2 q (W = mean width of the convex hull), and for each finite S of positive diameter H = W(S) log2 F_S(T) with F_S a Strassen spectral point:
additive under ⊕, multiplicative under ⊗, non-increasing under LOCAL linear maps at each site, F(1)=1. Symmetry group of the invariant: local GL at every site (monotone), isometries of K.
Lean: only "finite-dimensional convex Euclidean chart in a CAT(0) space with jointly convex diagonal prices" (lean/docs/379.md); the general statement is not described as formalized.

E2 (9/4, Thm 1.1 and Cor 1.2). ω_F = 9/4 over every field, model: formal arithmetic circuits (+,−,×, division by nonzero rational function), identities of rational functions;
every circuit needs ≥ ⌈n^{9/4}/2⌉ multiplication/division gates, linear ops free; geometric border rank of T_n ≥ n^{9/4}; asymptotic rank = n^{9/4}.
Lean (ComparatorChallenges/MatrixExponent.lean, solution OAI.LinearAlgebra.SpectralBooks.ExactExponent, permitted axioms propext/Quot.sound/Classical.choice): formalOmega F 1 1 1 = 9/4 for
division-free formal programs (statement read; ExactExponent.lean has 0 occurrences of "sorry"; imported modules not inspected; NOT built by us). The ⌈n^{9/4}/2⌉ gate bound is listed as unformalized.

E3 (mechanism of E2, from §1–§4). Not a rank argument on T_n alone:
 (a) Thm 2.1 (compression of tensor powers): if ω_k < 9/4 then every trivalent k-network of size m ≤ n^{1.05} with e ≥ n exterior bits has, for some d ≤ n^{o(1)}, a network for V^{⊗d} of size ≤ d·m·h^{−γ} + e·h^{η}.
 (b) Thm 2.2 (volume of list distinctness): vol_k(D_w^{⊗t}) > t·n_w·w^{σ} for 1 ≤ t ≤ 2^w, σ>0 depending on k only; D_w = "2^w words of 2w bits pairwise distinct", n_w = 2^w·2w exterior bits.
 (c) Prop 2.3: sorting gives a trivalent network of size O(n_w w^2); J = O(1) applications of (a) give volume O(n_w w^η) per list, η<σ, contradicting (b). Lemma 2.5 passes from finite fields to every field.
 (d) Proof of (b): reduces to checking a tagged permutation by two D_w tests (§4.1); then two cases: fields "without ports" via Lemma 4.1 (routing a distribution of permutations needs size Ω(r log q), by price monotonicity plus a graph entropy bound from the companion papers [42],[43]);
     finite fields "with ports": "cheap distinctness tests would make it possible to compress a family of tensors with a known lower bound" (text only, not read further).
 Essential to E2: (i) a hypothesis ω<9/4 that supplies a polynomial saving; (ii) universality of matrix multiplication for contracting bounded-arity bit networks; (iii) a network-volume lower bound at log-factor scale for an explicit function in P.
 Specific to matrix multiplication: the tripod ratio 6/(8/3)=9/4, sphere tensors, rigidity of polynomial multiplication.

E4 (Hamiltonian cycle / permanent). Degree-component border size L^{[N]}_F(HC_N) ≥ exp(c (log N)^2/(loglog N)^2) for N ≥ N_0(char), every field; same for Per_N if char ≠ 2. Model: formal arithmetic circuits, unrestricted depth, nonuniform.
Lean: only "exceeds N^C for every C" (exact circuits); the exp(...) bound is unformalized. Also a path-count polynomial P*_n with 2^{c(log n)^{5/4}} border bound.

E5 (Valiant). VF ⊊ VBP ⊊ VP ⊊ VNP over every field; grid state sum needs n^{Ω((log n)^{1/12})} (n states per edge). Lean: three separations proved, quantitative grid bound unformalized.
E5' (VP and VNP are different, 2026-11-23): exp(Ω((log n)^{5/4})) border-circuit bound; Lean comparator ComparatorChallenges/VPVNP.lean ("separation of exact VP and VNP over every field").

E6 (Fourier). N·(log N)^{1/2+o(1)} binary linear gates, batches of J transforms cost J×; formal polynomial multiplication has the same exponent (division-free). Linear/arithmetic model.

E7 (tapes). Fixed multitape TM multiplies n-bit integers in n(1+log n)^{1/2+o(1)}, O(n) cells. Lower bound Ω(n·√(log n)) (Lean doc wording) ONLY under variable-count Weak ETH (no fixed δ: 3-SAT in 2^{O(v^{1−δ})}·poly). Lean: both statements (comparator MultitapeWeakETH.lean).

E8 (sunflowers). r-sunflower exists in any family of > B_r^k sets of size ≤ k, log B_r = O((log r)^4 (loglog 2r)^{5/2}). Combinatorial; Lean: only C_r^k with unspecified C_r.

E9 (ETH is false, 2026-10-25). Deterministic #k-SAT in poly space and (n+m)^{O(1)}·2^{n/(log n)^{1/2+o(1)}}. Does not refute variable-count Weak ETH.

## 3. Reconciliation of the proofbook count
Entries with seq ≥ 17926: 353 = 18278 − 17926 + 1; no gaps, no duplicates inside that range. The only anomaly in the file is one duplicate sequence number (5309) in the old history; 18278 lines, 18277 distinct seq values, file not sorted by seq. The 353 is NOT explained by anomalies; it is exactly the range length.

## 4. Graph status (research_graph.duckdb, read-only, 2026-11-27 19:54)
obligation_register has 28 obligations, all OPEN, none closed. (8)/(40a) = OBL-R1 (formula for (8)/(40a)) and OBL-UNIFORM-QE (uniform O*/(40a), MMW Thm 1.3). OBL-W-D (uniform AC0 selection of simple DISJ counterexamples) and OBL-W-D-COLLIDE: OPEN, desk lemmas after 18111 cover only special classes.
established_results has 13 rows: 3 PROVED (T07-LEMMA, R10-BRIDGE, CJW20-T5.5-GAP, assessor-unvalidated), R5-MINKT elementary, 2 external theorems read at source, 6 REFUTED_TRANSFER (R11-SYM, R10-PNPXOR, R11-CW, R6-FORMULA, U1-TW, U1-MINOR), 1 restriction (CJW20 formulas only). None of them is touched by family 379.
Obligations are indexed by the older MCSP/streaming programme; T48–T56 are not registered as obligations. "Closed but unreused" could not be determined from the register (nothing is closed); USCCL, Lemmas M/N/O/T, QE* in its T-file form and theorems 12/14/16 were not found by grep in theory/*.md, so they were not integrated here.

## 5. New connections (each with its exact assumptions)
C1 (T53 + E4). T53 §1: the degree-h homogeneous component of the formal functional QE polynomial F_C of the Hamiltonian-cycle check C over F3 is ±HC_h. E4 bounds the degree-component border size of HC_h from below.
  Hence, GIVEN E4 over F3: every arithmetic circuit (border, arbitrary depth) for F_C has size ≥ exp(c (log h)^2/(loglog h)^2). Formal functional QE of poly-size functional 1-in-3 encodings is therefore NOT in VP (conditional on E4; the Lean-backed part is only the exact superpolynomial version).
  This is a quantitative strengthening of T53's equivalence "all such QE in VP ⇔ VP = VNP". It does not touch the Boolean object F_C|_Boolean = ±Π(−1−X_i)·C(X), which is poly-time.
C2 (E3(c) + T49 Lemma 2). A Boolean witness circuit W of size s gives a trivalent bit-tensor network of volume O(s) for its graph tensor over every field (parsimonious: one consistent internal assignment per input; this is Prop 2.3's construction). No formal degree and no t-saturation is used.
  So "circuit correctness induces a tensor network directly" holds. It induces an UPPER bound on the price of the graph tensor, never a lower bound (prices decrease under contraction: price ≤ Σ wire lengths × log dim).
C3 (T55 vs E1). The Euclidean invariants are spectral points for local GL at the sites; they are NOT invariant under G = Π_x Sym(Z_x) (permutations of the fibre depending on x, which are not local linear maps). T55's G-invariance obstruction therefore does not apply to them as stated.
  But on two sites a spectral point is the matrix rank (Strassen), and rank(Γ_S) = |X| for every selector S: complexity-blind. On n+m bit sites the price is not classified, and a lower bound on the price of Γ_S for a hard S is exactly a network-volume lower bound for S, i.e. the circuit lower bound of T49 §6 in new words. No gain without a lower-bound source.
C4 (T54 vs E2). T54's first failing step (E.4: gate values t-saturated, degree up to 2^s) concerns passing from Boolean circuits to GRADED formal objects. E3 avoids that step because its objects are bit tensors, not graded polynomial rings. The price paid is in C5.
C5 (direction of the MM mechanism). E3(a) turns an ARITHMETIC saving (fast matrix multiplication = contraction of arbitrary bounded-arity bit networks) into a Boolean network saving. The needed direction for P ≠ NP is the reverse: a Boolean consequence of P = NP into a contradiction.
  Under P = NP we have NP-decision in P (PH = P), not contraction. Contraction of F_2 networks is ⊕P-complete; T56 §4 (NP ⊆ ⊕P/poly) says decision reduces to contraction, not conversely. P = NP does not give ⊕P ⊆ P.
C6 (scale). E3(b) is a volume bound at log-factor scale for a function in P that sorting already meets up to w^{2−σ}. P = NP cannot compress an explicit P function below its complexity. A contradiction in the style of E3 needs a superpolynomial bound for a search function, which is the circuit lower bound again.
C7 (tapes). Weak ETH ⇒ P ≠ NP (SAT ∈ P gives time poly(L) ≤ 2^{O(v^{1−δ})}·poly(L)). Therefore E7's lower bound is conditional on a hypothesis STRONGER than P ≠ NP and false under P = NP: it cannot serve as the independent lower bound, and gives no bridge to uniform machines for our purpose.
C8 (U_G). The Valiant/grid state sum has n states per edge and free vertex tables, so it is not a specialization of U_G (3 colours, vertex weights X_{v,c}); a lower bound for a general polynomial does not transfer to a projection of it. No statement about U_G follows from E4–E5' unless VNP-hardness of {U_G} under projection is established (not checked here).
C9 (sunflowers). E8 may improve parameters in sunflower/plucking-based approximation arguments, but no connection to OBL-R7 (slice of an NP function) is established; the known slice obstruction is untouched.
C10 (ETH paper and E6/E7). The exponent 1/2 occurs in E9 (SAT counting, 2^{n/(log n)^{1/2+o(1)}}), E6 and E7. This is an observation about a shared shape, not a proved relation; E7's reduction only runs from multiplication to SAT.

## 6. Previously excluded approaches (control checks kept)
Nothing from family 379 restores a refuted assumption. Boolean circuit correctness does NOT imply formal identity, bounded formal degree or t-saturation (T48 L3, T49 L3, T54): used as such in no step above.
Relativization / natural proofs / algebrization: not assessed for E3 (the argument is for networks with arbitrary arity-3 tables, no oracle gates); unassessed, not cleared.

## 7. Closed obligations
None. No new theorem derived here closes an entry of obligation_register.

## 8. Strongest chain and first failing implication
P = NP
 ⇒ uniform poly-time W, hence uniform poly-size Boolean circuits W_n (T49 L2, T45 T2/T3)                                 [proved]
 ⇒ bit-tensor network of volume O(|W_n|) for the selector/graph tensor, over every field                                  [proved, standard, C2]
 ⇒ an upper bound on a Euclidean price of that tensor                                                                      [from E1 if E1 holds; not verified]
 ⇒ contradiction with a lower bound on the same price                                                                      [FIRST UNPROVED IMPLICATION]
First failing implication (exact): there is no known source of a lower bound on the price (equivalently on network volume) of the selector tensor Γ_S of an NP search problem that is superpolynomial.
 E3 supplies lower bounds only (i) for matrix multiplication in P-scale and (ii) for batched list distinctness at factor w^σ, and its compression theorem needs fast CONTRACTION (⊕P-type power), which P = NP does not provide.
Equivalent statement in T49/T55 language: for every poly-size Boolean W satisfying R(G,x)(1−R(G,W(G))) = 0, a white-box property Π(W) with ¬Π proved; the new tools give no such Π.

## 9. Next decisive step
Read Thm 2.2, case "finite field with ports", with k = F_2 (Boolean circuits live there), and decide whether it gives a superlinear UNRESTRICTED Boolean circuit lower bound n·(log n)^σ for AND_t of element distinctness. If it does, that is a stand-alone result far beyond the known ~3.1 n bounds
and must be checked by independent experts and Lean (the Comparator statement covers the exponent, not the volume theorem) before any use; even then it is log-scale and does not yet touch P vs NP.
If it does not (F_2 excluded), record that explicitly. Only after that, test whether a SEARCH-type tensor (U_G coloured-state sum with ⊕P-contraction replaced by NP-decision) admits any volume lower bound in the same price system.

## Correction (2026-11-28)
See T58: T57 searched theory/*.md only. Proofbook 17584/17585/17879 already contain the projection/transfer; HC_h=rho_h(U_G) derived there.

## Correction 2 (2026-11-28, T58 v2)
Superseded statements: (1) any use of the unpinned polynomial U in char 2 (vanishes; use pinned/fully weighted W); (2) "formal upper bound ⇒ Boolean-semiring/finite-field computation" (false; only F⇒E⇒B(F_p)); (3) HC gadget size O(h⁴ log h) (now O(h² log h)); (4) 17584 AND gadget computes XNOR (erratum, Proofbook 18279); (5) bound L ≥ exp((c/4−o(1))(log n)²/(loglog n)²) is an arithmetic bound on the pinned polynomial, no Boolean bound. §9 'next decisive step': Thm 2.2 with k=F_2 gives only n·polylog-type volume bounds in the Boolean-input F_2-sum model; no unrestricted Boolean circuit bound is claimed. See T58 v2 §D–E.
