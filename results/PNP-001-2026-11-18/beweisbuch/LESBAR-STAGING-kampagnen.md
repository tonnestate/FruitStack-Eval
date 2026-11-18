# Beweisbuch p_vs_np (STAGING-kampagnen)

Eintraege: 834, Hashkette intakt: True

PROOF LEDGER of this problem (kept across missions; 834 entries from 94 missions). It records what is PROVED, what is only observed and what is open. RULE: a statement that is not PROVED or CITED here must never be used as an established premise. You may use it as an explicitly named OPEN ASSUMPTION - your result is then conditional on it.
PROVED (the proof tool supported them over their whole domain):
  - Independent recheck of RC-6d52805a-R: GF(2)/GF(3) rank profile of A and [A|1] (with n, m) does not determine the positive-1in3 count C mod 2. Method limit, expected (parity of #1in3 presumably parity-P-hard), not novel.
  - Audit of Prop 7.3 of the OpenAI cubic border-dc preprint (2026-09-24): no error found. Scope: Sec. 3 (Prop 3.1, permanent projection of the coefficient polynomial G_D) verified by exact computation; Sec. 4 (Lemmas 4.1, 4.2, Prop 4.3) read by PI and tested on s
  - delta_lambda(D_4) = 1 = p_lambda and gamma_lambda(Y_{3,4}) = 1 for lambda=(6,6,4,4,4), degree 6 (function convention). Together with entry 214: both five-row degree-6 candidates with lambda_1 = 6 are closed; neither gives an equation of D_4 nor a separating eq
  - delta_lambda(D_4) = 1 = p_lambda for lambda=(6,6,6,4,2), degree 6 (multiplicity of S_lambda(V*) in the degree-6 functions on the orbit closure of det_4). The same highest weight function is nonzero on l*perm_3, so gamma_lambda(Y_{3,4}) = 1: this lambda gives n
  - Two owner corrections adopted + T11-P tool-boundary. (1) TAUTOLOGY dropped: 'det full multiplicity below d_first(n)' is vacuous (d_first is by definition the first degree with I!=0); not a theorem, does not resolve d=6. We need an INDEPENDENT lower bound on d_
  - T11-P NOTATION FIX (certificates valid): the engine evaluated the padded permanent as l*perm_3 = DEGREE 4 (verified: deg(l)=1, deg(perm_3)=3, product degree 4, matching det_4 degree 4). The ledger text 'x_11^4 perm_3' / 'z^4 perm_3' (degree 7) was a mis-transc
CITED from the literature (not machine-checked here):
  - Structural map (verified) for the forward separation perm vs det: (1) The length-4 non-separation lemma is CORRECT but must use DENSITY not 'every cubic': only SMOOTH cubic surfaces are determinantal (Beauville); determinantal cubics are DENSE + D_4 closed + P
  - VERIFIED: dim span{d^k f} = C(n,k)^2 exactly for f=det_n and f=perm_n (checked n=2,3, all k). Hence border Waring rank underline-WR(f) >= max_k C(n,k)^2 = C(n,floor(n/2))^2 = Theta(4^n/n), EXPONENTIAL for BOTH determinant and permanent. By BDI21 Prop 6.6 the m
  - T13-1/2 (asymptotic, primary-source verified): define uniform HWV covariant families P_{T_n}(coeff(f))=<HWV(T_n), f^{tensor d(n)}> and separate three complexities (BDI21): construction, REPRESENTATION (circuit size of P_{T_n}), EVALUATION at a specific f. BDI2
  - T13 algebraic natural proofs: a 'proof polynomial' P_N vanishes on coeff(f) for all f in C, is nonzero, and lies in an efficient algebraic class D. EQUIVALENCE (GKSS/FSV): no D-natural proof against C EXISTS iff C is a D-succinct hitting set (extreme PIT deran
  - T5 uniformity bridge: P subset P/poly so NP not subset P/poly => P != NP unconditionally (the easy direction T12 feeds). Karp-Lipton: NP subset P/poly => PH collapses to Sigma_2^p. Williams' algorithmic method: non-trivial Circuit-SAT algorithm + IKW collapse 
  - T12 Boolean hardness magnification: proven CONDITIONAL theorems turning near-linear circuit lower bounds for MCSP/MKtP (truth-table length N=2^n) into NP not subset P/poly (and NEXP, oplusP variants); premises open. NO-GO: CHOPRS Locality Barrier - local techn
  - T11-A extra: (IP) for n>3m^4 an occurring padded-perm lambda cannot obstruct merely via VANISHING of the rectangular Kronecker coefficient. (DIP) multiplicity obstructions provably succeed where occurrence obstructions fail, but in a DIFFERENT geometric settin
  - T11-A: GCT obstruction landscape for det_n vs padded permanent l^{n-m}perm_m. (1) OCCURRENCE obstructions EXCLUDED: BIP Thm 1.4, for n>=m^25, a_lambda(padded perm)>0 => a_lambda(det)>0; so occurrence obstructions cannot prove perm!=det in the relevant range. (
  - T10-B: EGOW rank-method meta-barrier. The quantitative no-go theorems are PROVEN for TENSOR RANK and WARING RANK (model-specific). This is NOT a universal proof that every rank method fails to separate perm from det. Keep separate and model-specific. (Efremenk
  - T10-A: There exists a constant M such that for all m > M and every n > 2m^2+2m, any tau, and any k<n, rank((l^{n-m} perm_m)_{(k,n-k)[tau]}) < rank((det_n)_{(k,n-k)[tau]}). So the shifted-partial-derivatives measure of the PADDED permanent never exceeds that of
HYPOTHESES on file, not proved:
  - Pitfall for the block-rank-1 cap question (is M_1(6,p) <= 20 = C(6,3)?): the naive argument 'every entry (u,v) lies in some R_j, so A = sum of pieces and rank(A) <= sum_j rank(A|R_j) <= 20' is INVALID, because the R_j = {u: j not in u} x {v: j in v} overlap an
  - [LIT-ATLAS2-GRAVER-AI] (UNVERIFIED - AI search summary pasted by owner, NOT owner-checked): families with Graver complexity independent of n - 3-way / multi-index transportation, privacy in statistical tables, integer multi-commodity flow (fixed suppliers), mu
  - [LIT-ATLAS2-MISC] GLS ellipsoid/separation; branch-price-and-cut label dominance (ESPPRC pricing NP-hard); bin packing APTAS (Fernandez de la Vega-Lueker, Karmarkar-Karp); Lenstra 1983 fixed-dimension ILP; Benders 1962; Held-Karp 1-trees; Chvatal 1979 greedy s
  - [LIT-ATLAS2-RIVER] river-crossing (Ito-Langerman-Yoshida): general variants polynomial without a trip bound, NP-hard with a bound on the number of trips; "Ferry Cover with Connectivity Constraints" (2026, UNVERIFIED): Boat-1 graphs characterised via block-cut 
  - [LIT-ATLAS2-VI] representation/proof-system lower bounds are not algorithm lower bounds - Rothvoss 2014 (matching polytope), Schoenebeck (Lasserre fails on random 3-XOR, XOR-SAT in P by Gaussian elimination). Control question for every negative result: propert
  - [LIT-ATLAS2-V] branch-and-cut is a proof system - Chvatal-Gomory rounding (sum lambda_i a_i)^T x <= floor(sum lambda_i b_i); derivation of 0 <= -1 refutes; Cook-Coullard-Turan 1987 cutting-plane proof length, relations to resolution / extended resolution. Long
REFUTED:
  - procedure alg-f496d8017c75 (cons2 and cons3 and rank_GF3(matrix_B) = m => SAT; author nemotron-3.5-bolt) is sound
  - procedure alg-381c8d76daac (The new step involves checking for a specific structural property in the graph formed by the clauses. Specifically, we will analyze the bipartite grap) is sound
  - procedure alg-cf4ba2054ce6 (Consider the problem through the lens of graph theory, where each variable represents a vertex and each clause forms a hyperedge connecting three vert) is sound
  - procedure alg-ca4f12006c0e (The exact-1 constraint structure can be related to properties of graph homomorphism or exact cover, but for polynomial time, we leverage the existence) is sound
APPROACHES already examined (do not repeat one without a new idea):
  - For the GF(2)-parity relaxation of 1-in-3-SAT, how large is the cancellation in its exact inclusion-exclusion expansion, and does that cancellation grow with the cycle rank of the clause hypergraph? C -> RC-a0f974c1-R (VALID || VALID for the quantities computed. The identity check passes, A and C are consistent with the formula, and E an)
  - None -> None
  - None -> None
  - None -> None
  - None -> None
  - Can a Gal matrix whose nonzero entries are all single-difference pairs, meaning |v \ u| = 1, ever beat the rank-to-block ratio k = C(n,3)? If not, every improvement on D-013 must use pairs with |v \ u -> RC-8fd9326f-R (VALID || VALID. The experiment measures the ratio correctly and the code's ratio, decomposition and sum-identity checks )
  - None -> None
  - None -> None
NUMERICAL EVIDENCE on file: 90 entries (finite cases; they prove nothing about all cases). Latest: None
OPEN RESEARCH QUESTIONS (derived from this ledger; questions, not facts):
  - Q-423db3b56b [UNEXPLAINED, OPEN] Does failure of the sum identity for |v \ u| ≥ 2 allow ratio > k at all? The decisive test is whether a multi-difference matrix on the 41-row domain can have every clause-restricted rank ≤ 1 while total rank ≥ 21. This i
  - Q-72027e8141 [UNEXPLAINED, OPEN] Can a structural argument prove that any Gal matrix formed only by single-difference pairs must satisfy $\text{rank}_F(A) / \max_j \text{rank}_F(A|R_j) \le C(n,3)$ for $n \ge 5$, without relying on empirical search resul
  - Q-c4564fe530 [UNEXPLAINED, OPEN] Does log of the cancellation ratio, measured against A, factor additively over clause components, and is its growth in m determined by the GF(2) nullity of the incidence system rather than by cycle rank? This decides whe
  - Q-0e39f4e56c [UNEXPLAINED, OPEN] Determine if the correlation between $\log_2 R$ and cycle rank is truly linear or exhibits different scaling (e.g., polynomial, logarithmic) by testing larger, structured instances or by refining the cycle rank metric to
  - Q-82fd28e6e6 [UNEXPLAINED, OPEN] Recompute the odd-row and profile counts on g mod 2, and test whether the mod-2 profile count (predicted 2^m on disjoint instances) tracks exact treewidth across families where width grows with m and where it stays bound
NEXT PROOF GAP: State this step formally and have it checked: #F equals the sum over clause sets S of (-1)^|S| N(S), where N(S) = 2^(n - |V(S)|) if S is consistent and 0 otherwise (inclusion-exclusion over falsified clauses)  (derived in words only: state it formally and have the proof tool check that it follows from its premises)
