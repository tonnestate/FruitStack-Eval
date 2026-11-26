# Proofbook seq 17156 — PROOF_STEP

- key: `a9afea61db91dfaf`
- at: 1795727556.3211217
- mission: director/closure-exclusions
- hash: `801918dbc58a6bb4e0b015410c5c54b33633e953aabec3ef197a99910cacf56e` (prev `265aaa22958cd0f3123a230321f6a2d1e4d4b36fbba22cf0113ac4150e7f58f5`)
- graph nodes: PB:801918dbc58a6bb4e0b015410c5c54b33633e953aabec3ef197a99910cacf56e
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

AF-IMPLICATION (for review; seq 16762 was filed as HYPOTHESIS and therefore never reviewed although D6', COV1 and the PRG chain use it): the implication (P1 AND P2) => conclusion of AF, with the proof as stated: AF (conditional, replaces the size budget by a correlation budget): let beta in (0,1), eta>0. Assume (P1) a local PRG fooling De Morgan formulas of size s with error delta <= 2^{-gamma}/10, seed and per-bit circuit size <= N^{beta-eta}; (P2) a pseudorandom restriction rho with >= N^{beta+eta/2} stars such that, w.p. >= 0.9, the principal-formula forest Phi of C|rho (reused-gate leaves kept as never-restricted variables) has size <= s. Then Gap-MCSP[N^beta] has no gamma-almost-formula of size S. Proof: fix such rho; YES = G(z) o rho has circuit size <= N^beta, NO = random fill has circuit size >= N^{beta+eta/2-o(1)} w.p. 1-2^{-N^{Omega(1)}}, so Adv(C|rho) >= 1/2; by D4 some F_a of size <= s has advantage >= 2^{-gamma-1} > delta, contradicting P1. BUDGET: gamma <= log2(1/delta) - 4 instead of r + log2(2S+1) <= 3 beta log2 N; since any PRG needs seed >= log(1/delta), gamma can reach N^{beta-eta} (polynomial) instead of O(log N).

## Full row (verbatim JSON)

```json
{
 "seq": 17156,
 "at": 1795727556.3211217,
 "problem": "p_vs_np",
 "mission": "director/closure-exclusions",
 "key": "a9afea61db91dfaf",
 "kind": "PROOF_STEP",
 "conclusion": "AF-IMPLICATION (for review; seq 16762 was filed as HYPOTHESIS and therefore never reviewed although D6', COV1 and the PRG chain use it): the implication (P1 AND P2) => conclusion of AF, with the proof as stated: AF (conditional, replaces the size budget by a correlation budget): let beta in (0,1), eta>0. Assume (P1) a local PRG fooling De Morgan formulas of size s with error delta <= 2^{-gamma}/10, seed and per-bit circuit size <= N^{beta-eta}; (P2) a pseudorandom restriction rho with >= N^{beta+eta/2} stars such that, w.p. >= 0.9, the principal-formula forest Phi of C|rho (reused-gate leaves kept as never-restricted variables) has size <= s. Then Gap-MCSP[N^beta] has no gamma-almost-formula of size S. Proof: fix such rho; YES = G(z) o rho has circuit size <= N^beta, NO = random fill has circuit size >= N^{beta+eta/2-o(1)} w.p. 1-2^{-N^{Omega(1)}}, so Adv(C|rho) >= 1/2; by D4 some F_a of size <= s has advantage >= 2^{-gamma-1} > delta, contradicting P1. BUDGET: gamma <= log2(1/delta) - 4 instead of r + log2(2S+1) <= 3 beta log2 N; since any PRG needs seed >= log(1/delta), gamma can reach N^{beta-eta} (polynomial) instead of O(log N).",
 "premises": [
  "seq 16760 (D4)",
  "P1 (hypothesis)",
  "P2 (hypothesis)"
 ],
 "prev": "265aaa22958cd0f3123a230321f6a2d1e4d4b36fbba22cf0113ac4150e7f58f5",
 "hash": "801918dbc58a6bb4e0b015410c5c54b33633e953aabec3ef197a99910cacf56e"
}
```
