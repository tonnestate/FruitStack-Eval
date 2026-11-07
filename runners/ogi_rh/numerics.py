"""mpmath numerics harness for OGI-RH (design §3.3, §8.4).

Every record is NUMERICAL_EVIDENCE. mpmath is multiprecision floating point, not
interval/ball arithmetic: no output here is a certified enclosure, and none may be
promoted by the claim gate. Zeros are located independently of mpmath.zetazero:
sign changes of Hardy's Z (mpmath.siegelz) between consecutive Gram points, refined
by a bracketing root finder, then recomputed at a second, higher precision.
"""

from __future__ import annotations

import mpmath

LABEL = "NUMERICAL_EVIDENCE"


def _precision_note(dps: int, check_dps: int) -> str:
    return (f"NON-RIGOROUS: mpmath floating point at {dps} and {check_dps} decimal digits; "
            "no interval enclosure, no certified error bound")


def gram_point(n: int, dps: int = 30):
    with mpmath.workdps(dps):
        return mpmath.grampoint(n)


def gram_law_holds(n: int, dps: int = 30) -> dict:
    """Gram's law at g_n: (-1)^n Z(g_n) > 0. Known to fail for some n."""
    with mpmath.workdps(dps):
        z = mpmath.siegelz(mpmath.grampoint(n))
        holds = bool((-1) ** n * z > 0)
    return {"label": LABEL, "kind": "GRAM_LAW", "n": n, "Z_at_gram": mpmath.nstr(z, 15),
            "holds": holds, "precision": _precision_note(dps, dps)}


def _zero_in(a, b, dps: int):
    with mpmath.workdps(dps):
        return mpmath.findroot(mpmath.siegelz, (a, b), solver="anderson")


def zeros_by_gram(count: int, dps: int = 30, check_dps: int | None = None) -> list[dict]:
    """First `count` zeros 1/2+iγ on the line, one per Gram interval [g_{k-1}, g_k).

    Stops at the first Gram interval without a sign change (Gram's law failure); the
    caller then gets fewer than `count` records. ponytail: no Rosser-block handling,
    add it when items need zeros past the first Gram failure.
    """
    check_dps = check_dps or dps + 20
    out = []
    for k in range(count):
        with mpmath.workdps(dps):
            a, b = mpmath.grampoint(k - 1), mpmath.grampoint(k)
            if mpmath.sign(mpmath.siegelz(a)) == mpmath.sign(mpmath.siegelz(b)):
                break
        gamma = _zero_in(a, b, dps)
        gamma_hi = _zero_in(a, b, check_dps)
        with mpmath.workdps(check_dps):
            diff = abs(gamma_hi - gamma)
            agree = int(-mpmath.log10(diff / gamma_hi)) if diff else check_dps
        out.append({"label": LABEL, "kind": "ZETA_ZERO", "index": k + 1,
                    "gamma": mpmath.nstr(gamma, dps - 2), "gram_interval": [k - 1, k],
                    "agreeing_digits_between_precisions": min(agree, dps),
                    "precision": _precision_note(dps, check_dps)})
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(zeros_by_gram(5) + [gram_law_holds(n) for n in range(3)], indent=1))
