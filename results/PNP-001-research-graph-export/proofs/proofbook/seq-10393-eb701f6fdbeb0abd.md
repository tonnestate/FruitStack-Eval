# Proofbook seq 10393 — CONNECTION

- key: `eb701f6fdbeb0abd`
- at: 1795365026.746713
- mission: agent/pnp-desk/research/R1579:claude-haiku-5-5@default
- hash: `fa8d80aa72ec635eb1092a006edc724eec545b6ad01078a9e205519871bb73f6` (prev `8b11365f580ca6a49916d689f3789986d5e1eddb42320179ad56e3e56e0c2562`)
- graph nodes: PB:fa8d80aa72ec635eb1092a006edc724eec545b6ad01078a9e205519871bb73f6
- verification status: as stated in the text below and in reviews/; the export assigns none.

## Statement / proof text (verbatim)

SOURCE CHECK, row A, A.3 (Oliveira-Pich-Santhanam, Hardness Magnification Near State-of-the-Art Lower Bounds, Oxford preprint hm.pdf, read at offset 88500). (a) A.3 is a SKETCH ('we sketch the proof of Theorem 5'), not a full proof. (b) Its lower bound is against U2-FORMULAS, not general circuits; item (1) of the Theorem requires Gap-MCSP[2^{beta n}/cn, 2^{beta n}] not in Circuit[N^{1+eps}]. A formula bound does not transfer to a circuit bound, so A.3 does NOT supply the item (1) hypothesis. (c) The range is Gap-MCSP[n^d, 2^{(alpha/2 - o(1))n}] (polynomial threshold, parameter alpha), not the 2^{beta n}/cn range of item (1). Quantifier reading of item (1) still needs primary-source verification (Zesty2 HTTP 422, CORE CAPTCHA). Scope: source check, not a proof step.

## Full row (verbatim JSON)

```json
{
 "seq": 10393,
 "at": 1795365026.746713,
 "problem": "p_vs_np",
 "mission": "agent/pnp-desk/research/R1579:claude-haiku-5-5@default",
 "key": "eb701f6fdbeb0abd",
 "kind": "CONNECTION",
 "evidence_class": "VERIFICATION",
 "origin": "agent",
 "question": "Q-34b02a6004",
 "statement": "SOURCE CHECK, row A, A.3 (Oliveira-Pich-Santhanam, Hardness Magnification Near State-of-the-Art Lower Bounds, Oxford preprint hm.pdf, read at offset 88500). (a) A.3 is a SKETCH ('we sketch the proof of Theorem 5'), not a full proof. (b) Its lower bound is against U2-FORMULAS, not general circuits; item (1) of the Theorem requires Gap-MCSP[2^{beta n}/cn, 2^{beta n}] not in Circuit[N^{1+eps}]. A formula bound does not transfer to a circuit bound, so A.3 does NOT supply the item (1) hypothesis. (c) The range is Gap-MCSP[n^d, 2^{(alpha/2 - o(1))n}] (polynomial threshold, parameter alpha), not the 2^{beta n}/cn range of item (1). Quantifier reading of item (1) still needs primary-source verification (Zesty2 HTTP 422, CORE CAPTCHA). Scope: source check, not a proof step.",
 "prev": "8b11365f580ca6a49916d689f3789986d5e1eddb42320179ad56e3e56e0c2562",
 "hash": "fa8d80aa72ec635eb1092a006edc724eec545b6ad01078a9e205519871bb73f6"
}
```
