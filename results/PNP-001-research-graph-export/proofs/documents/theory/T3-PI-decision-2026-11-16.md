# PNP-001 — PI decision after T1/T2 (Claude, 2026-11-16)

## 1. Proof check T1 Satz 3/4 (by the PI, line by line)

**Greedy lemma.** A chosen crossing edge uv blocks only edges with an endpoint in N[u] ∪ N[v]: at most 2D vertices with at most D edges each,
so at most 2D² edges. Hence the crossing edges contain an induced matching of size μ ≥ e/(2D²).

**Satz 3.** Set every variable outside the induced matching to 1; all clauses touching them are satisfied. Because the matching is induced,
exactly ∏(x_i ∨ y_i) remains. Its cut matrix contains the μ-fold Kronecker power of [[0,1],[1,1]] as a submatrix; that matrix has determinant
−1 over every field, so the rank is ≥ 2^μ. **Correct.**

**Satz 4.** Edge expansion h:
- a balanced order has ≥ hn/2 crossing edges → rank ≥ 2^{hn/(4D²)};
- every cubic tree has a 1/3–2/3 separator edge, giving ≥ hn/3 crossing edges → rank ≥ 2^{hn/(6D²)}.

**Correct, given the cited existence of expanders.** The ledger status stays PROPOSED until a proof tool checks it.

**Primary source checked by the PI (PDF of arXiv 2110.13014, 2026-11-16).** de Colnet & Mengel, KR 2021, §5:
- **Model:** "positive AC" — circuits computing non-negative functions to ℝ, but "allow for negative constant inputs or equivalently
  subtraction". Cancellation is therefore allowed.
- **Theorem 2:** a smooth structured-decomposable AC of size N gives F as a sum of at most N balanced decomposable products for one partition.
- **Lemma 13:** rank ≤ that number.
- **Lemma 14:** an induced matching m across (X,Y) gives rk(M_{F_G}) ≥ 2^{|m|}. The proof is the determinant recursion on [[1,2],[2,2]] ⊗ ….
- **Lemma 15:** (c,3)-expanders.
- **Proposition 4:** 2^{Ω(n)} for F_G = ∏_{(i,j)∈E} (1 + max(x_i, x_j)), which has a polynomial-size AC.

**Verdict:**
- The arithmetic, cancellation-allowed structured-circuit lower bound for expander-based functions is in the literature, over ℝ.
- T1 Satz 3/4 for the 2-CNF indicator ∏(x_u ∨ x_v) is the same argument with [[0,1],[1,1]] (det −1). Its "every field" form is an immediate
  variant; it is not stated there explicitly.
- Not a new result.

A claim heard that de Colnet & Mengel cover only Boolean/monotone circuits is contradicted by §4–5 of the PDF.

arXiv 2611.10842 (de Colnet & Szeider, 7 Nov 2026, "Factor Rank", ATDDs = tree tensor networks with cut-matrix rank) is related work on
the same rank notion. Its abstract mentions neither expanders nor CNF lower bounds.

**Earlier subagent check (abstracts / ar5iv):**
- **Arithmetic structured circuits.** de Colnet & Mengel, "A Compilation of Succinctness Results for Arithmetic Circuits", KR 2021 (arXiv
  2110.13014), use the same method:
  - Lemma 13: rank ≤ size for structured decomposable arithmetic circuits;
  - Lemma 14: an induced matching across the cut gives rank 2^m;
  - Lemma 15: expanders have an Ω(n) induced matching across every balanced partition;
  - Proposition 4: 2^{Ω(n)} for ∏(1+max(x_i,x_j)) over ℝ, cancellation allowed.
- **Boolean OBDD in every order.** Razgon (KR 2014) and Bova–Slivovsky.
- **Boolean DNNF.** Bova–Capelli–Mengel–Slivovsky (arXiv 1411.1995).

**Verdict:** T1 Satz 3/4 (indicator function, every field, every order or vtree) is a routine variant of known work. **Not new.**

## 2. Limitation of the T1/T2 direction (rigorous)

Any measure that bounds general circuit size from below must be small on functions with small circuits.
- F_G (monotone 2-CNF of a bounded-degree expander) is a CNF with m = O(n) clauses, so it has circuits of size O(n).
- By Satz 4, its cut rank is 2^{Ω(n)} in every variable order and every tree decomposition.

Therefore cut rank — equivalently ROABP width, or structured / decomposable compression — is **not** a lower-bound measure for general
circuits. It separates restricted models only.

T2 adds: the partial-derivative rank method (Raz) cannot certify multilinear-formula hardness for the counting polynomials of these CNFs.

**Decision:** the T1/T2 algebraic-compression line is closed as a route to P ≠ NP (outcome LIMITATION_ESTABLISHED). It remains a correct
result about restricted models.

## 3. Consequence for the program (honest)

A rigorous resolution of P vs NP must get past:
- relativization (Baker–Gill–Solovay),
- natural proofs (Razborov–Rudich),
- algebrization (Aaronson–Wigderson).

No technique that does this for general circuits and NP is known. The only lower-bound programme that has passed relativization and natural
proofs for a non-trivial class is the **algorithmic method** (Williams: a faster-than-brute-force SAT algorithm for a class C implies
NEXP ⊄ C; NEXP ⊄ ACC⁰).

T1's Satz 2 (counting in time poly(cut rank)) yields nothing new there: classes with small cut rank are ROABP-like, and #SAT for those is
already polynomial.

## 4. Next justified obligation (PI)

Formulate precisely, with the literature on file, the frontier question of the algorithmic method nearest to what FruitStack can compute,
and check whether any computational step there is open and checkable:
- SAT algorithms for depth-2 threshold circuits (THR∘THR) and the NEXP ⊄ THR∘THR target;
- the known barrier for the alternation-trading time-space lower bounds for SAT (n^{2cos(π/7)}; Buss–Williams).

Nothing here is a claim of progress on P vs NP. A result at that frontier would be a genuine contribution, not a resolution.

## 5. Revision of section 4 (same day, after the owner's review)

**THR∘THR via Williams is withdrawn as the programme direction.**

Its theorem would be NEXP (or E^NP) ⊄ THR∘THR. That says nothing about P vs NP; two unproved steps are missing:
- NP instead of NEXP;
- general circuits instead of THR∘THR.

Chen–Tal–Wang (ECCC TR26-039, STOC 2026) already prove E^NP ⊄ n^{2.5−ε}-gate THR∘THR with exactly this method.

**The only known bridge from restricted-model lower bounds to P ≠ NP is hardness magnification.** For specific NP problems Q (MCSP
variants), slightly superlinear lower bounds against weak models already imply NP ⊄ P/poly.

**Its known obstacle is the locality barrier** (Chen–Hirahara–Oliveira–Pich–Rajgopal–Santhanam, ITCS 2020 / JACM 2022):
- such Q have efficient circuits with small-fan-in oracle gates;
- standard lower-bound techniques extend to such oracle circuits.

**Next PI obligation (connected to P ≠ NP):**
1. Prove precisely whether the T1/T2 rank method localizes.
   - Conjectured lemma: an oracle gate with fan-in k raises the cut rank by at most a factor 2^k across any cut.
   - If true, rank lower bounds survive local oracles, so the method is blocked by the locality barrier and cannot be the
     magnification engine.
2. Check whether CHOPRS already state this for rank / ROABP methods. Do not reproduce it if they do.
3. Only then judge whether any non-localizing ingredient is available.

The existing ledger obligations (formalizing T1/T2 lemmas) are kept; they are rigor work on known results, not a bridge.

## 6. Localization of the rank method — answered by the literature (PI read of ECCC TR19-168, 2026-11-16)

**Lemma (proved here, for the record).** For h(x) = F(x, g_1(x_{S_1}), …, g_s(x_{S_s})) and a cut (X,Y):

  rank M_h ≤ Σ_b rank M_{F(·,b)} · Π_j 2^{c_j},   c_j = min(|S_j∩X|, |S_j∩Y|).

Proof: h = Σ_b F(·,b) · Π_j [g_j = b_j]; each indicator has cut rank ≤ 2^{c_j}; rank is submultiplicative under Hadamard products and
subadditive under sums.

One crossing gate costs a factor ≤ 2^{1+k/2}; s gates cost ≤ 2^{s(1+k/2)}. For magnification-relevant oracle circuits with many gates this
bound is vacuous by itself; what matters is how many gates cross the critical cut.

**Chen–Hirahara–Oliveira–Pich–Rajgopal–Santhanam (Theorem 2, Proposition 43, Lemma 45):**
- Tal's sign-rank and discrepancy lower bounds for Formula-XOR localize ("we actually localize all proofs of the lower bounds from B3 and
  B4 we are aware of").
- Rank- and communication-type measures are therefore blocked in their frontiers. Not reproduced here.

**Exception — non-localizable lower bounds:**
- their Theorem 49 (a language in E, GapAND-Formula frontier D);
- [Oli19], via indirect diagonalization and pseudorandomness.

**Their open problem (§1.4):** "come up with non-localizable lower bounds similar to Theorem 49 which would be above the magnification
threshold and work for a problem more closely related to the one from the corresponding HM frontier".

**PI consequence.** The bridge to P ≠ NP has to go through a magnification frontier for general circuits (MCSP-type: a slightly
superlinear lower bound would give NP ⊄ P/poly, hence P ≠ NP). The exact statement must be verified in [OS18]/[OPS19]/[CJW19a] before use.

The candidate tool is a non-localizable technique of the Oli19 / Theorem 49 kind (diagonalization + pseudorandomness), not a rank or
communication measure.

**Next:**
1. Read §3.3 / Theorem 49 / [Oli19] and the MCSP general-circuit magnification theorem verbatim.
2. Then decide whether a concrete, checkable sub-claim exists.

## 7. The bridge theorem, verbatim (Oliveira–Pich–Santhanam, Theorem 1.4; CCC 2019 / Theory of Computing 17(11), 2021)

> There is a universal constant c ≥ 1 such that, if there is ε > 0 with
> Gap-MCSP[2^{βn}/cn, 2^{βn}] ∉ Circuit[N^{1+ε}] for every sufficiently small β > 0,
> then NP ⊄ Circuit[poly]   (N = 2^n = input length; hence P ≠ NP).

**PNP-001 target, precise.** Prove, for some ε > 0 and all small β, that Gap-MCSP[2^{βn}/cn, 2^{βn}] requires general (fan-in-2) Boolean
circuits of size N^{1+ε}.

**What stands against it:**
1. No superlinear lower bound against general circuits is known for ANY explicit function. The state of the art is ≈ 3.1·N, linear
   (to be cited from the primary source before use).
2. Locality barrier (Chen et al.): Gap-MCSP has near-linear circuits with small-fan-in oracle gates. Every technique that tolerates such
   oracles is ruled out — this includes gate elimination as usually applied (to be checked) and all rank, sign-rank and discrepancy measures
   (§6).
3. Natural proofs: OPS19 discuss whether this magnification instance is non-naturalizable; to be read.

**Remaining candidate tool:** a non-localizable argument — Chen et al. Theorem 49 (a language in E, formula model) and [Oli19] (indirect
diagonalization + pseudorandomness).

**Precise next obligation (PI):** determine whether the Theorem-49/Oli19 mechanism can be aimed at Gap-MCSP and general circuits.
Concretely: what exactly prevents Theorem 49 from giving a language in NP (rather than E), and from going against Circuit (rather than
GapAND-Formula)? That is a question with a definite answer in their proof; it is read first, then judged.

## 8. Theorem 49 read (CHOPRS proof text) — the obligation of §7 answered

**The mechanism of Theorem 49:**
1. f_hard on m = log N bits that no N^{1−ε/2}-size formula 0.8-approximates. It exists by counting and is FOUND by exhaustive search over all
   functions and all such formulas (time 2^{O(N)}).
2. L(x) = f_hard(PARITY(x_1), …, PARITY(x_m)) on m blocks (Andreev-style).
3. Lower bound: a random restriction leaving one variable per block alive turns a small (GapAND-)formula for L into a small formula for
   f_hard (shrinkage, Tal 2014) — contradiction.
4. Non-localizable for a trivial reason: an oracle gate of fan-in m = log N computes f_hard directly, so L has small oracle formulas.

**Why it cannot be aimed at Gap-MCSP vs general circuits (the two missing steps, both fundamental):**

(a) **Uniformity (E vs NP).** Hardness of f_hard is certified by exhaustive search. An NP version would need NP-verifiable hardness of an
    m-bit function, i.e. the complement of MCSP on truth tables of length N. Brute force over N^{1−ε/2}-size formulas takes
    2^{N^{1−ε/2+o(1)}} time — not polynomial. Certifying hardness inside NP is essentially the problem itself (circular).

(b) **Shrinkage (formulas vs circuits).** Step 3 uses that formulas shrink under random restrictions. General circuits do not shrink. The
    explicit general-circuit lower bounds come from gate elimination and are linear (≈3.1N). Limits of gate elimination are studied
    (Golovnev–Hirsch–Knop–Kulikov, "On the limits of gate elimination") — to be read before citing exact constants.

**PI conclusion (honest).** Every known technique fails at one of the following for the bridge theorem of §7:
- superlinear general-circuit lower bounds (none known for any explicit function);
- the locality barrier;
- natural proofs.

Theorem 49 escapes locality only by combining exhaustive search (E, not NP) with formula shrinkage (not circuits).

A proof of P ≠ NP along this bridge needs a NEW technique that gives N^{1+ε} general-circuit lower bounds for Gap-MCSP, does not survive
small-fan-in oracles, and is not natural. No such technique is known, and none follows from PNP-001's results so far.

**Ledger action (pending the end of mission 662fc9d5):** record this as an APPROACH with outcome LIMITATION_ESTABLISHED and the precise
open obligation, so it is never re-investigated without a new idea.

**Note (2026-11-16).** OPS state that NP-completeness is not known for this Gap-MCSP variant, and the magnification theorem does not need it.
The premise must hold for this exact variant AND for all sufficiently small β; a single computed bound does not satisfy it.

**Observation (PI) — no shortcut through cryptography.** Under exponentially secure pseudorandom functions computable by circuits of size
2^{βn}, a circuit of size N^{1+ε} = 2^{(1+ε)n} deciding Gap-MCSP[2^{βn}/cn, 2^{βn}] would distinguish them from random functions. So the
premise is plausible under strong cryptographic assumptions. But those assumptions already imply P ≠ NP, so this is circular and not a
route.

## 9. How hard the bridge premise is — an equivalence (CHOPRS, Theorem 1, read verbatim 2026-11-16)

The following are EQUIVALENT:
- **(a)** approximate MCSP[(n^c,0),(2^{n^γ},n^{−c})] ∉ Circuit[N^{1+ε}];
- **(b)** worst-case MCSP[n^c, 2^{n^γ}/n^c] ∉ Circuit[N^{1+ε}];
- **(c)** Circuit[n^ℓ] cannot be learned to error O(1/n^ℓ) by 2^{O(n^γ)}-size circuits with non-adaptive membership queries;
- **(d)** no Circuit[poly(N)]-natural property is useful against Circuit[n^d], for some d;
- **(e)** non-uniform PRFs in Circuit[n^d] exist that (1/N^{ω(1)})-fool oracle circuits of size 2^{a·n}.

**Consequence (PI).** For the MCSP variants (a)/(b), proving the magnification premise is EXACTLY as hard as:
- proving that natural properties do not exist;
- equivalently, proving unconditionally that sub-exponentially secure PRFs exist — a cryptographic statement that in particular
  implies P ≠ NP.

This turns the remark of §7 into a theorem for these variants. The premise cannot be "slightly superlinear" in difficulty; any proof of it
is a proof of cryptographic hardness.

**Open for OPS Theorem 1.4** (Gap-MCSP with thresholds 2^{βn}/cn, 2^{βn}): whether the same equivalence holds there is not stated in what I
read. Next: read the corresponding discussion in OPS (Theory of Computing 2021) and CHOPRS Appendix A.2, which interprets magnification
as oracle-circuit constructions.

**What this rules out:** any finite-computation "test" of the premise (§ reply to the owner's protocol, 2026-11-16). The premise is
equivalent to an unconditional cryptographic lower bound.

## 10. PNP-001 ACTIVE (owner, 2026-11-16 evening) — first investigation: the strength of the bridge premise (H)

(H) = OPS Theorem 1.4 premise: ∃ε>0 ∀ small β: Gap-MCSP[2^{βn}/cn, 2^{βn}] ∉ Circuit[N^{1+ε}].

**Proposition P1 (PI; proof below; adversarial review running; novelty NOT claimed — a variant of Razborov–Rudich / Kabanets–Cai).**
If one-way functions secure against non-uniform poly-size adversaries exist, then (H) holds for every ε>0 and β∈(0,1); indeed
Gap-MCSP[2^{βn}/cn, 2^{βn}] ∉ Circuit[N^K] for every constant K.

Proof:
1. A PRF {f_k}, k∈{0,1}^ℓ, with circuit size ℓ^a for the key hardwired.
2. Take ℓ = 2^{βn/(a+1)}, so every tt(f_k) is a YES instance.
3. A uniform T is a NO instance with probability 1−o(1), because the number of circuits of size s₂ is 2^{O(s₂ log s₂)} ≪ 2^N for β<1.
4. A deciding circuit of size N^K reads 2^n = ℓ^{(a+1)/β} bits, so it is a poly(ℓ)-size distinguisher with advantage 1−o(1),
   contradicting PRF security.

**Chain:** OWF ⟹ (H) ⟹ NP ⊄ P/poly ⟹ P ≠ NP. (H) sits between OWF and P ≠ NP.

**Contrast:** for thresholds n^c, CHOPRS Theorem 1 needs sub-exponentially secure PRFs (§9).

**Q2: does (H) imply OWF?** If yes, proving (H) = proving OWF (believed strictly stronger than P ≠ NP), and the route would be a detour.

Literature status found (search 2026-11-16; to be read verbatim before citing):
- OWF ⟺ average-case hardness of K^t (Liu–Pass, FOCS 2020).
- OWF ⟺ average-case MCSP hardness on samplable distributions (Ilango–Ren–Santhanam).
- Weak Perebor Hypothesis for MCSP (over a natural distribution) ⟹ OWF (Ren–Santhanam, CCC 2021, "Hardness of KT characterizes parallel
  cryptography").
- All of these are AVERAGE-case. No result found that worst-case Gap-MCSP hardness alone implies OWF; that is the worst-case vs.
  average-case meta-complexity question (Pessiland / Heuristica).

**Conclusion (provisional):** (H) is not known to be as strong as OWF, so the OPS route is NOT shown to be a detour; it remains justified.
A proof of (H) must give a worst-case lower bound and need not yield cryptography.

**Next mathematical question (PI):** OPS's magnification proof uses anti-checkers, and CHOPRS refute the Anti-Checker Hypothesis of [OPS19]
(their §5.2.2). Read exactly which hypothesis was refuted and what remains of the anti-checker route. That determines which structural
property of Gap-MCSP instances a non-localizable proof of (H) could still exploit.

**P1 review (independent agent, adversarial; checked by the PI):** VALID WITH FIXES, no substantive error.
- a = a₀+1: GGM uses n PRG calls of size ℓ^{a₀}, n = O(log ℓ); independent of β.
- ℓ = ⌈2^{βn/(a+1)}⌉.
- D outputs 0 on every NO instance, so Pr[D(T)=1] ≤ Pr[CC(T) ≤ s₂]; fix randomized coins non-uniformly.
- Use the non-uniform oracle PRF notion: poly sizes and query counts, with the hybrid loss of GGM.
- Quantifiers: success for infinitely many n gives a distinguisher for infinitely many ℓ, which contradicts security for all large ℓ.
- Remark: with arbitrary K the statement says Gap-MCSP ∉ P/poly (in N) for each fixed β, c.

**Known:** Razborov–Rudich (JCSS 1997), Kabanets–Cai (STOC 2000). P1 is recorded as a known result applied to the OPS parameters, not as new.

## 11. Anti-checker route (CHOPRS Corollary 61 / Theorem 59, read verbatim 2026-11-16)

**Anti-Checker Hypothesis [OPS19].** There is a UNIVERSAL collection Y of 2^{(2−ε)n} sets of size 2^{n^{1−ε}} such that every f ∉ Circuit[2^{n^λ}]
has an anti-checker in Y (each circuit of size 2^n/10n errs on some y in it).

**This hypothesis is FALSE** (Corollary 61). With it, MCSP[2^{n^{1/3}}, 2^{n^{2/3}}] would have N^{2−ε}-size formulas with N^{o(1)}-fan-in oracles
at the bottom, which contradicts Theorem 59 (the localized Hirahara–Santhanam near-quadratic formula lower bound, via k-wise independent
pseudorandom restrictions).

**PI consequence.**
- Refuted: compact universal anti-checker families.
- Not refuted: function-dependent anti-checkers (Lemma 27, after Arora–Barak Lemma 17.19). These exist for every hard f; the magnification
  proof computes them under NP ⊆ NC¹.

**Q3 (next, PI).** Can a proof of (H) use function-dependent anti-checkers in a way that does NOT tolerate small-fan-in oracles?
- The failure mode to avoid is Theorem 59's: pseudorandom restrictions that simplify oracle formulas too.
- A candidate must act where restrictions do not simplify general circuits.
- First step: write down exactly what property of a size-N^{1+ε} circuit for Gap-MCSP the existence of function-dependent anti-checkers
  forces, and test whether the known oracle circuits for Gap-MCSP already have that property. If they do, the idea localizes and is
  discarded at once.

## 12. [SUPERSEDED by §13 — parameters and the strength of O3 were wrong] Q3: magnification relocates the difficulty (PI, 2026-11-16)

**Construction verified (CHOPRS §3.2, Theorem 21 / Lemma 22).** Worst-case MCSP is reduced to approximate MCSP by encoding tt(f) with an
explicit linear error-correcting code E_N:
- rate b, distance δ;
- each code bit is a PARITY of input bits ([Jus72, SS96]).

The oracle circuits then read a few code positions and pass them to small-fan-in oracle gates, which decide the small instance.

**PI observation O3 (derived; a reformulation, not new — CHOPRS App. A.2 interprets magnification as oracle-circuit construction).**
1. **Linear layer is cheap.** Asymptotically good codes are encodable by linear-size circuits (Spielman 1996, linear-time encodable
   codes). In GENERAL circuits the whole linear layer costs O(N). Any lower-bound argument that only uses "the circuit must compute many
   parities / encode its input / depend on many code positions" is met by the oracle circuits, so it localizes.
2. **The remaining cost sits entirely in the oracle task.** That task is a partial / approximate MCSP decision on N^{o(1)} sampled bits.
   Contrapositive of OPS Theorem 1.4: if NP ⊆ P/poly, the oracle task has poly(N^{o(1)}) = N^{o(1)} circuits, and Gap-MCSP gets
   N^{1+o(1)}-size circuits.
3. **Hence:** proving (H) = proving that the oracle task — an NP-type meta-computational problem on its own input length — has NO
   polynomial-size circuits. The "slightly superlinear" bound at size N is a superpolynomial bound at size N^{o(1)}. The difficulty
   is relocated, not reduced.

**Consequence for PNP-001.** Hardness magnification gives an exact bridge, but no leverage: any proof of (H) must contain a superpolynomial
general-circuit lower bound for an NP-type problem, i.e. the original difficulty. Combined with §6–§11, the relevant unsolved core is:

> a technique giving superpolynomial lower bounds against general circuits for some problem in NP that avoids relativization, natural
> proofs, algebrization and locality.

**Next mathematical question (PI).** The only family known to avoid relativization and natural proofs for a non-trivial class is the
algorithmic method, and its conclusions are for NEXP / E^NP, not NP (the uniformity gap).

Investigate the uniformity gap precisely:
- which known theorems move circuit lower bounds from NEXP / E^NP down toward NP (e.g. Karp–Lipton-type collapses, Kannan-type fixed-
  polynomial bounds for Σ₂P / S₂P / MA-type classes), and with what loss;
- whether any of them composes with an algorithmic-method lower bound to give a statement about NP.

This is a question with definite literature answers; read before reasoning further.


## 13. Correction of §12 (owner review, checked against CHOPRS Proposition 63, 2026-11-16)

**Correct parameters.** CHOPRS Appendix A.2, Proposition 63, item [OPS19]:
  Gap-MCSP ∈ [N·poly(s), poly(s), poly(s)]–Circuit[N·poly(s)]   (oracle circuits; s ≤ 2^n/poly(n)).

With s = 2^{βn} = N^β, poly(s) = N^{O(β)}. The oracle instances have size N^{O(β)} — polynomially smaller than N, NOT N^{o(1)} for a fixed β.
§12 point 2 was wrong.

**What follows (structural interpretation, NOT a separately proved lemma).**
- Suppose the oracle task has circuits of size m^d (m = its input length). Substituting them gives circuits of size N^{1+β·C(d)} for a
  constant C(d).
- For every fixed d, β can be taken small enough that this is below N^{1+ε}.
- This is why OPS quantify over ALL sufficiently small β, and why (H) implies that the oracle-task family has no circuits of any fixed
  polynomial size.
- It does NOT follow that a proof of (H) must first prove a separate lower bound for the oracle task. CHOPRS themselves: "not every
  hardness magnification theorem needs to lead to an unconditional construction of efficient oracle circuits".
- O3 is kept only as a literature-based structural interpretation.

**Second correction.** Theorem 21 / Lemma 22 (CHOPRS §3.2) belong to the Formula-XOR frontier (NQP ⊄ NC¹ type), not to OPS Theorem 1.4.
The linear-code layer argument (Spielman, O(N)) was transferred to general circuits without justification; the relevant construction for
Theorem 1.4 is Proposition 63 with size N·poly(s). §12 point 1 is withdrawn.

**Third correction.** Kannan: ∀k ∃L_k ∈ Σ₂P with L_k ∉ SIZE(n^k) — a different language for each k, not one language beyond all
polynomials. The barriers limit specific proof methods; they do not show that every transfer from NEXP-type bounds to NP must fail.

**Status.** Magnification is NOT closed as a route; §12's "LIMITATION_ESTABLISHED" for it is withdrawn (see the ledger revision entry).
The uniformity-gap question stays open and is investigated without presupposing a new barrier.
