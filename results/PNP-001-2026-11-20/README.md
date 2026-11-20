# PNP-001 results, 2026-11-20

- `completeness-n10/`: independent second completeness check of the n <= 10 enumeration - C implementation (no shared code with the
  Python enumerator) reproduces per witness type the minimal-core counts (n=9: 627,598; n=10: 22,333,134 over 12 types) and the exact
  set of 47,088 NS2-failing cores at n=10; randomized premise test (3,695 random blind cores, 0 violations of C4, D-018, ALLOWED).
  Hence 11 <= smallest blind core with PC degree >= 3 <= 16 rests on two independent implementations.
- `acc0-level3/`: ACC0 level 3 analysis. Positive 1-in-3 = SAT of AND o MOD3 over linear forms without auxiliaries (exact). Provable
  saving min(2^{n/2}, 2^{n-rank}) (Theorem A) but the class cannot compute OR (Theorem O): no new lower bound by transfer. Level 3 stays
  OPEN; next check: existential auxiliary variables (see specification, section "Level 3 - OPEN; next check").
- Specifications updated (ACC0 incl. level 3), proof book refreshed.
