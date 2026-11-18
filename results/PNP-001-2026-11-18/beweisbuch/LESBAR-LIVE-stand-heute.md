# Beweisbuch p_vs_np (LIVE-stand-heute)

Eintraege: 410, Hashkette intakt: True

PROOF LEDGER of this problem (kept across missions; 410 entries from 92 missions). It records what is PROVED, what is only observed and what is open. RULE: a statement that is not PROVED or CITED here must never be used as an established premise. You may use it as an explicitly named OPEN ASSUMPTION - your result is then conditional on it.
PROVED (the proof tool supported them over their whole domain):
  - Audit of Prop 7.3 of the OpenAI cubic border-dc preprint (2026-09-24): no error found. Scope: Sec. 3 (Prop 3.1, permanent projection of the coefficient polynomial G_D) verified by exact computation; Sec. 4 (Lemmas 4.1, 4.2, Prop 4.3) read by PI and tested on s
  - delta_lambda(D_4) = 1 = p_lambda and gamma_lambda(Y_{3,4}) = 1 for lambda=(6,6,4,4,4), degree 6 (function convention). Together with entry 214: both five-row degree-6 candidates with lambda_1 = 6 are closed; neither gives an equation of D_4 nor a separating eq
  - delta_lambda(D_4) = 1 = p_lambda for lambda=(6,6,6,4,2), degree 6 (multiplicity of S_lambda(V*) in the degree-6 functions on the orbit closure of det_4). The same highest weight function is nonzero on l*perm_3, so gamma_lambda(Y_{3,4}) = 1: this lambda gives n
  - Two owner corrections adopted + T11-P tool-boundary. (1) TAUTOLOGY dropped: 'det full multiplicity below d_first(n)' is vacuous (d_first is by definition the first degree with I!=0); not a theorem, does not resolve d=6. We need an INDEPENDENT lower bound on d_
  - T11-P NOTATION FIX (certificates valid): the engine evaluated the padded permanent as l*perm_3 = DEGREE 4 (verified: deg(l)=1, deg(perm_3)=3, product degree 4, matching det_4 degree 4). The ledger text 'x_11^4 perm_3' / 'z^4 perm_3' (degree 7) was a mis-transc
  - T11-P: T11-L lifted CONDITIONALLY_VERIFIED -> VERIFIED. Independent minor certificates produced from the CORRECTED (binomial-normalized) engine for all five p=2 partitions (12,4),(10,6),(10,4,2),(8,6,2),(8,4,4) at (3,4,4). Each certificate: (i) both HWVs valid
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
  - Answer to "PNP-001, Iteration 7 (P versus NP), narrow falsification test. Frage: Laesst sich ein Informationstransfer-Mass so definieren, dass es (i) fuer deterministische Rechnungen nicht trivial ist, (ii) sich unter Aenderungen der Speicherorganisation kontr
  - RESTATE_RESTRICTION on 'N': Restate the restriction that block-respecting, oblivious, and reversible normal forms cost only polynomial overhead in terms of the computational complexity classes they belong to. -> opens: This restatement clarifies the relationsh
  - ADD_RESTRICTION on 'E1': Add a restriction that the measure must also account for the temporal dynamics of the computation, not just the spatial distribution of crossing sequences. -> opens: This change introduces a new dimension to the measure, potentially le
  - REMOVE_ASSUMPTION on 'F': Remove the restriction that the measure must not fall under the category described in F. -> opens: This change allows us to explore measures that might be based on the variety of crossing sequences or other properties that were previo
  - state the problem in Spiral Time-Entropy Diagram: Each boundary $i$ is mapped to a point on a spiral where the radial distance represents $\log_2(|\tau_i(M, x)|)$ and the angular position corresponds to $i$. The entire transcript $\tau_e(M, x)$ is visualized a
  - state the problem in Crossing Sequence Graph: Each crossing sequence $\tau_i(M, x)$ is mapped to a vertex in the Crossing Sequence Graph. Edges connect vertices if their corresponding sequences share a common subsequence. The entire transcript $\tau_e(M, x)$ i
REFUTED:
  - Padding-floor EQUIVALENCE REFUTED (certified counterexample, independently verified); proven (<=) direction retained; replaced by a TWO-CONDITION necessary filter. COUNTEREXAMPLE (owner): (m,n,d)=(2,3,6), lambda=(8,2,2,2,2,2)|-18 has p_lambda>0 and lambda_1=8 
  - REJECTED: the proposed extension of the null-cone lemma to NON-rectangular partitions, and the claimed d_min^sep(3,4) >= 9. MATH ERROR: for a non-rectangular lambda with ell=k, the HWV transforms as P_lambda(g(t).f) = t^w P_lambda(f) with w = k*lambda_1 - |lam
  - Task split + ell=5 scope correction (owner). TWO distinct questions must NOT be conflated: (A) FIRST_NONZERO_IDEAL_DEGREE d_min(4) = first d with I(D_4)_d != 0; (B) FIRST_SEPARATING_EQUATION = first HWV in I(D_4) not in I(Y_{3,4}) (ker E_D not subset ker E_Y).
  - WR correction (owner): the earlier 'border Waring rank of perm/det = Theta(4^n/n)' is too strong. PROVEN is only the LOWER bound underline-WR(f) >= C(n,floor(n/2))^2 = Theta(4^n/n), i.e. underline-WR = Omega(4^n/n) (exponential). Theta would need a matching up
APPROACHES already examined (do not repeat one without a new idea):
  - state the problem in Algebraic Geometry Space: Each SAT instance is mapped to a variety in projective space, where variables correspond to coordinates and clauses to polynomial equations. Solutions to -> INVESTIGATED_NO_PROOF (the rounds of criticism were used up; nothing was proved)
  - state the problem in Hypergraph Representation: Each variable in the SAT problem is represented as a vertex, and each clause as a hyperedge connecting the vertices corresponding to the variables it co -> INVESTIGATED_NO_PROOF (the critics raised no objection; nothing was proved)
  - Assume that the transport of input information is not bounded by input length but instead scales superpolynomially with the input size. -> INVESTIGATED_NO_PROOF (the rounds of criticism were used up; nothing was proved)
  - state the problem in Tensor Network Diagrams: Each deterministic TM transition is represented as a tensor node, with input/output states as indices. Crossing sequences become paths in the network, and -> INVESTIGATED_NO_PROOF (the revisions changed nothing; nothing was proved)
  - The total variation distance \( \delta_\pi(t) \) decreases monotonically with time \( t \) for the cat map \( U \) on a finite set \( \Omega \). -> NOT_INVESTIGATED (no second agent was available for an independent solution)
  - The inverse of a poly-time injective function \( g \) is not necessarily poly-time computable even if \( P = NP \). -> NOT_INVESTIGATED (no second agent was available for an independent solution)
  - The clustering threshold in k-XORSAT instances does not inherently correlate with computational hardness for all algorithms. -> INVESTIGATED_NO_PROOF (the revisions changed nothing; nothing was proved)
  - state the problem in Spiral Coordinate System: Each element \( g \in G \) is mapped to a point on a spiral in the complex plane, where the angle corresponds to the element's position in a cyclic order -> INVESTIGATED_NO_PROOF (the rounds of criticism were used up; nothing was proved)
NUMERICAL EVIDENCE on file: 77 entries (finite cases; they prove nothing about all cases). Latest: {"script_mode": true, "variables": {"n": 8, "ok": true}, "note": "no main() and no result dict: printed output is in stdout_tail, small top-level values in variables"} | printed: 1 True
2 True
3 True
4 True
5 True
6 True
7 True
8 True

OPEN RESEARCH QUESTIONS (derived from this ledger; questions, not facts):
  - Q-d41254d122 [UNEXPLAINED, OPEN] Objection by Qwen2.5-VL-72B-Instruct against "CONJECTURE (O8 SUPPORTED by symbolic verification, O7 SUPPORTED by finite computation for n≤10, O3 DISPUTED - circuit complexity bound appears inconsistent with known lower b
  - Q-54356f7b4b [UNEXPLAINED, OPEN] Objection by laguna-xs-2.1 against "CONJECTURE (tested for \( n = 1 \) to \( n = 9 \), not proved; the transfer of the approximative F_2-grade to SAT withstands adversarial verification within the specified bounds for AC
  - Q-5c1e93ff1a [UNEXPLAINED, OPEN] Objection by laguna-xs-2.1 against "": I need to analyze this task systematically. Let me first check which scientific methods are appropriate for this problem.</think><tool_call>physalis_discover<arg_key>query</arg_key>
  - Q-1c4a676701 [UNEXPLAINED, OPEN] Objection by Qwen2.5-VL-72B-Instruct against "": ISSUES: FOUND The colleague's solution does not address the specific tasks outlined in the problem statement. Here are the specific issues: 1. **No Direct Address of Claim
  - Q-dc08749193 [UNEXPLAINED, OPEN] Objection by Qwen2.5-VL-72B-Instruct against "": ISSUES: FOUND The colleague's solution lacks a concrete, checkable response to the task requirements. Specifically: 1. **No Explicit Arguments for Claims**: The colleague 
NEXT PROOF GAP: State this step formally and have it checked: #F equals the sum over clause sets S of (-1)^|S| N(S), where N(S) = 2^(n - |V(S)|) if S is consistent and 0 otherwise (inclusion-exclusion over falsified clauses)  (derived in words only: state it formally and have the proof tool check that it follows from its premises)
