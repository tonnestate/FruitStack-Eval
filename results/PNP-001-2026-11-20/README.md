# PNP-001 results, 2026-11-20

- `completeness-n10/`: independent second completeness check of the n <= 10 enumeration - C implementation (no shared code with the
  Python enumerator) reproduces per witness type the minimal-core counts (n=9: 627,598; n=10: 22,333,134 over 12 types) and the exact
  set of 47,088 NS2-failing cores at n=10; randomized premise test (3,695 random blind cores, 0 violations of C4, D-018, ALLOWED).
  Hence 11 <= smallest blind core with PC degree >= 3 <= 16 rests on two independent implementations.
- `acc0-level3/`: ACC0 level 3 analysis. Positive 1-in-3 = SAT of AND o MOD3 over linear forms without auxiliaries (exact). Provable
  saving min(2^{n/2}, 2^{n-rank}) (Theorem A) but the class cannot compute OR (Theorem O): no new lower bound by transfer. Level 3 stays
  OPEN; next check: existential auxiliary variables (see specification, section "Level 3 - OPEN; next check").
  Section 6 (level 3b): linearising restrictions - Delta = r_min - k, exact on class D (equality rank); OR_n in D iff n <= 2;
  affine-hull bound Delta <= c - rho for gadget closures; checks l3b_checks.py, l3c_checks.py. Level 3 still OPEN.
- Specifications updated (ACC0 incl. level 3), proof book refreshed.
  Section 7 (level 3c): branch-sum criterion, Theorem L (degree 1: restriction never raises the rank surplus), Lean proofs
  acc0-level3/lean/ACC0L3.lean (OR not in C0; OR_n in D iff n<=2; affine Boolean functions are literals), evidence audit.
  Section 8 (correction): algorithm R counts complete solutions (x,y); projected #SAT only with unique witnesses (l3e_checks.py).
  Section 9 (brute force, acc0-level3/brute): all representations n+k <= 7; surplus at the affine-hull bound iff f in D (Theorem B).
- `mg3/`: Theorem MG-3 (no common GL2 basis makes EXACT1_3 and EQ_d, d>=3, planar matchgates; sharp at d=2), owner proof + independent review with exact Groebner check; spec: second Level-3 route (matchgate excess).
  Section 10 (holo/gates): no common GL2 matchgate basis for nonlinear gates and wire equalities; direct translation lambda >= #nonlinear gates.
