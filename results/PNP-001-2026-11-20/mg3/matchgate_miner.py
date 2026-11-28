#!/usr/bin/env python3
"""Exact GL(2,C) matchgate signature verifier and bounded basis search.

Requires: sympy >= 1.12. Works with Python 3.10+ on Windows/Linux.

Input JSON (see --example): signature families, NOT a SAT-to-Pfaffian reduction.
A FOUND certificate proves local matchgate signature compatibility under a
single bipartite holographic basis; it does NOT prove planarity of a network,
validity of a quotient, or correctness of any global Pfaffian contraction.

The complete matchgate identities (MGI) are Cai--Gorenstein (2014), Theorem 2.1:
  sum_{j=1}^l (-1)^j f(alpha xor e_{p_j}) f(beta xor e_{p_j}) = 0,
where p_j are the positions in alpha xor beta in increasing order. Together
with the parity condition, they characterize planar matchgate signatures.

Use this research tool only on SMALL tensor arities (default max 5, can set 6).
(Provided by the owner, 2026-11-18; stored verbatim in PNP-001 lab/onein3.)
"""
from __future__ import annotations

import argparse
import itertools
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Any

import sympy as sp


@dataclass(frozen=True)
class Signature:
    name: str
    arity: int
    values: tuple[sp.Expr, ...]  # Binary indexes 000..111


def make_signature(spec: dict[str, Any]) -> Signature:
    kind = spec.get("kind")
    if kind == "exact_one":
        d = int(spec["arity"])
        if d < 1:
            raise ValueError("exact_one arity must be >= 1")
        vals = [sp.Integer(int(i.bit_count() == 1)) for i in range(1 << d)]
        return Signature(spec.get("name", f"EXACT1_{d}"), d, tuple(vals))
    if kind == "equality":
        d = int(spec["arity"])
        if d < 1:
            raise ValueError("equality arity must be >= 1")
        vals = [sp.Integer(int(i in (0, (1 << d) - 1))) for i in range(1 << d)]
        return Signature(spec.get("name", f"EQ_{d}"), d, tuple(vals))
    if kind == "fused_exact_one":
        scope = list(spec["scope"])
        if not scope or len(scope) != len(set(scope)):
            raise ValueError("scope must be a nonempty list of distinct variable IDs")
        pos = {str(v): j for j, v in enumerate(scope)}
        clauses = list(spec["clauses"])
        if not clauses:
            raise ValueError("fused_exact_one needs at least one clause")
        d = len(scope)
        for clause in clauses:
            if len(clause) != 3 or any(str(v) not in pos for v in clause):
                raise ValueError("every fused clause needs 3 IDs drawn from scope")
        vals = []
        for mask in range(1 << d):
            bits = [(mask >> (d - j - 1)) & 1 for j in range(d)]
            valid = all(sum(bits[pos[str(v)]] for v in clause) == 1 for clause in clauses)
            vals.append(sp.Integer(int(valid)))
        return Signature(spec.get("name", "FUSED_EXACT1"), d, tuple(vals))
    if kind == "values":
        raw = spec["values"]
        count = len(raw)
        if count < 2 or count & (count - 1):
            raise ValueError("values length must be a power of 2 >= 2")
        d = count.bit_length() - 1
        vals = []
        for v in raw:
            expr = sp.sympify(v)
            if not expr.is_Rational:
                raise ValueError("Explicit values must be exact rational constants")
            vals.append(expr)
        return Signature(spec.get("name", "CUSTOM"), d, tuple(vals))
    raise ValueError(f"Unknown signature kind: {kind!r}")


def parse_families(data: dict[str, Any], max_arity: int = 5) -> tuple[list[Signature], list[Signature]]:
    if not isinstance(data.get("clauses"), list) or not isinstance(data.get("variables"), list):
        raise ValueError("Input requires 'clauses' and 'variables' lists")
    clause_sigs = [make_signature(s) for s in data["clauses"]]
    var_sigs = [make_signature(s) for s in data["variables"]]
    if not clause_sigs or not var_sigs:
        raise ValueError("Input requires at least one signature on each side")
    if any(s.arity > max_arity for s in clause_sigs + var_sigs):
        raise ValueError(f"Signature arity exceeds --max-arity {max_arity}")
    def distinct(items: list[Signature]) -> list[Signature]:
        seen: set[tuple] = set()
        result = []
        for item in items:
            key = (item.arity, item.values)
            if key not in seen:
                seen.add(key)
                result.append(item)
        return result
    return distinct(clause_sigs), distinct(var_sigs)


def matrix_transformed(sig: Signature, mat: sp.MatrixBase) -> tuple[sp.Expr, ...]:
    """Apply mat^(tensor arity); preserves the specified port order."""
    d = sig.arity
    support = [(i, v) for i, v in enumerate(sig.values) if v != 0]
    out = []
    for out_mask in range(1 << d):
        expr = 0
        for in_mask, val in support:
            prod = val
            for j in range(d):
                row = (out_mask >> (d - 1 - j)) & 1
                col = (in_mask >> (d - 1 - j)) & 1
                prod *= mat[row, col]
            expr += prod
        out.append(sp.expand(expr))
    return tuple(out)


def matchgate_equations(values: tuple[sp.Expr, ...], arity: int, mode: str) -> list[sp.Expr]:
    n = 1 << arity
    allowed_parity = 0 if mode == "EVEN" else 1
    constraints: list[sp.Expr] = [values[i] for i in range(n) if i.bit_count() % 2 != allowed_parity]
    for alpha in range(n):
        if alpha.bit_count() % 2 == allowed_parity:
            continue
        for beta in range(alpha + 1, n):
            if beta.bit_count() % 2 == allowed_parity:
                continue
            diff = alpha ^ beta
            if diff.bit_count() < 4:
                continue
            positions = [1 << (arity - 1 - j) for j in range(arity) if diff & (1 << (arity - 1 - j))]
            poly = sum((-1) ** j * values[alpha ^ pos] * values[beta ^ pos]
                       for j, pos in enumerate(positions))
            constraints.append(sp.expand(poly))
    seen: set[sp.Expr] = set()
    result: list[sp.Expr] = []
    for expr in constraints:
        expr = sp.expand(expr)
        if expr == 0 or expr in seen or -expr in seen:
            continue
        seen.add(expr)
        result.append(expr)
    return result


def verify_matchgate(values: tuple[sp.Expr, ...], arity: int) -> tuple[bool, str, str | None]:
    n = 1 << arity
    vals = tuple(sp.simplify(x) for x in values)
    even_nz = any(vals[i] != 0 for i in range(n) if i.bit_count() % 2 == 0)
    odd_nz = any(vals[i] != 0 for i in range(n) if i.bit_count() % 2 == 1)
    if even_nz and odd_nz:
        return False, "MIXED", "parity violation"
    mode = "ODD" if odd_nz else "EVEN"
    for alpha in range(n):
        for beta in range(alpha + 1, n):
            diff = alpha ^ beta
            positions = [1 << (arity - 1 - j) for j in range(arity) if diff & (1 << (arity - 1 - j))]
            if not positions:
                continue
            residual = sum((-1) ** j * vals[alpha ^ p] * vals[beta ^ p]
                           for j, p in enumerate(positions))
            residual = sp.simplify(residual)
            if residual != 0:
                return False, mode, f"MGI(alpha={alpha:0{arity}b}, beta={beta:0{arity}b}) = {residual}"
    return True, mode, None


def forward_verify(T: sp.MatrixBase, clauses: list[Signature], variables: list[Signature]) -> dict[str, Any]:
    if T.shape != (2, 2):
        return {"valid": False, "reason": "T must be 2x2"}
    if any(sp.sympify(x).free_symbols for x in T):
        return {"valid": False, "reason": "T must be concrete (no free parameters)"}
    det = sp.simplify(T.det())
    if det == 0 or det.is_zero is None:
        return {"valid": False, "reason": "det(T) must be provably nonzero"}
    dual = T.inv().T
    checks = []
    for side, sigs, mat in (("CLAUSE", clauses, T), ("VARIABLE", variables, dual)):
        for sig in sigs:
            transformed = matrix_transformed(sig, mat)
            ok, parity, failure = verify_matchgate(transformed, sig.arity)
            checks.append({"side": side, "name": sig.name, "arity": sig.arity,
                           "matchgate": ok, "parity": parity, "failure": failure})
            if not ok:
                return {"valid": False, "det_T": str(det), "checks": checks,
                        "reason": f"{side} {sig.name}: {failure}"}
    return {"valid": True, "det_T": str(det), "T": [[str(x) for x in row] for row in T.tolist()],
            "checks": checks, "meaning": "local matchgate compatibility; global topology not checked"}


def fast_candidates() -> list[tuple[str, sp.Matrix]]:
    return [
        ("identity", sp.eye(2)),
        ("hadamard", sp.Matrix([[1, 1], [1, -1]])),
        ("swap", sp.Matrix([[0, 1], [1, 0]])),
        ("diagonal_phase", sp.diag(1, sp.I)),
        ("complex_fourier", sp.Matrix([[1, 1], [sp.I, -sp.I]])),
        ("triangular", sp.Matrix([[1, 1], [0, 1]])),
    ]


def branch_equations(clauses: list[Signature], variables: list[Signature],
                     parity_profile: tuple[str, ...]) -> tuple[list[sp.Expr], tuple[sp.Symbol, ...]]:
    a, b, c, d, z = sp.symbols("a b c d z")
    mat = sp.Matrix([[a, b], [c, d]])
    dual_scaled = sp.Matrix([[d, -c], [-b, a]])
    equations = [z * (a * d - b * c) - 1]
    for sig, mode in zip(clauses, parity_profile[:len(clauses)]):
        equations.extend(matchgate_equations(matrix_transformed(sig, mat), sig.arity, mode))
    for sig, mode in zip(variables, parity_profile[len(clauses):]):
        equations.extend(matchgate_equations(matrix_transformed(sig, dual_scaled), sig.arity, mode))
    return equations, (a, b, c, d, z)


def groebner_branch(data: dict[str, Any]) -> dict[str, Any]:
    clauses, variables = parse_families(data["instance"], max_arity=int(data["max_arity"]))
    eqs, (a, b, c, d, z) = branch_equations(clauses, variables, tuple(data["profile"]))
    gauge = data["gauge"]
    if gauge == "a1":
        subs = {a: 1}
        vars_ = (b, c, d, z)
    elif gauge == "a0c1":
        subs = {a: 0, c: 1}
        vars_ = (b, d, z)
    else:
        raise ValueError("Invalid gauge")
    eqs = [sp.expand(e.subs(subs)) for e in eqs]
    eqs = [e for e in eqs if e != 0]
    gb = sp.groebner(eqs, *vars_, order="grevlex", domain=sp.QQ)
    if gb.contains(sp.Integer(1)):
        return {"status": "INCONSISTENT", "proof": "reduced Groebner basis = <1>",
                "profile": data["profile"], "gauge": gauge}
    candidates: list[dict] = []
    try:
        sols = sp.solve(list(gb), list(vars_), dict=True, simplify=False)
        if isinstance(sols, list):
            candidates = sols[:8]
    except (NotImplementedError, ValueError, TypeError):
        pass
    for sol in candidates:
        trial = {s: sol.get(s, sp.Integer(1)) for s in vars_}
        T = sp.Matrix([[a, b], [c, d]]).subs(subs).subs(trial)
        if T.free_symbols:
            continue
        cert = forward_verify(T, clauses, variables)
        if cert["valid"]:
            return {"status": "FOUND", "certificate": cert,
                    "profile": data["profile"], "gauge": gauge}
    return {"status": "EXISTS_NO_WITNESS", "proof": "proper ideal implies a complex solution exists",
            "profile": data["profile"], "gauge": gauge,
            "note": "No explicit matrix extracted; not a constructive certificate"}


def solve_instance(instance: dict[str, Any], timeout: float, max_arity: int,
                   max_profiles: int) -> dict[str, Any]:
    clauses, variables = parse_families(instance, max_arity=max_arity)
    for name, T in fast_candidates():
        cert = forward_verify(T, clauses, variables)
        if cert["valid"]:
            return {"status": "FOUND", "method": f"direct:{name}", "certificate": cert}
    n_types = len(clauses) + len(variables)
    profiles = 1 << n_types
    if profiles > max_profiles:
        return {"status": "INCONCLUSIVE", "reason": f"{profiles} parity profiles exceed --max-profiles {max_profiles}"}
    deadline = time.monotonic() + timeout
    inconsistent = 0
    branches = 0
    exists_proven = []
    for parity_profile in itertools.product(("EVEN", "ODD"), repeat=n_types):
        for gauge in ("a1", "a0c1"):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return {"status": "INCONCLUSIVE", "reason": "time budget exceeded",
                        "branches_completed": branches, "branches_inconsistent": inconsistent,
                        "branches_with_solutions": len(exists_proven)}
            request = {"instance": instance, "max_arity": max_arity,
                       "profile": parity_profile, "gauge": gauge}
            try:
                proc = subprocess.run([sys.executable, os.path.abspath(__file__), "--worker"],
                                      input=json.dumps(request), capture_output=True,
                                      text=True, timeout=remaining, check=False)
            except subprocess.TimeoutExpired:
                return {"status": "INCONCLUSIVE", "reason": "Groebner branch time budget exceeded",
                        "branches_completed": branches, "branches_inconsistent": inconsistent,
                        "branches_with_solutions": len(exists_proven)}
            if proc.returncode != 0:
                return {"status": "INCONCLUSIVE", "reason": "worker failed",
                        "detail": proc.stderr[-1200:]}
            result = json.loads(proc.stdout)
            branches += 1
            if result["status"] == "FOUND":
                cert = result["certificate"]
                T = sp.Matrix([[sp.sympify(x) for x in row] for row in cert["T"]])
                independent = forward_verify(T, clauses, variables)
                if independent["valid"]:
                    return {"status": "FOUND", "method": "groebner+forward_verify",
                            "certificate": independent, "branches_completed": branches}
                return {"status": "INCONCLUSIVE", "reason": "worker witness failed parent validation"}
            if result["status"] == "INCONSISTENT":
                inconsistent += 1
            else:
                exists_proven.append(result)
    if exists_proven:
        return {"status": "EXISTS_NO_WITNESS", "reason": "At least one GL2 branch has a proper Groebner ideal; no concrete T extracted",
                "branches_completed": branches, "examples": exists_proven[:3]}
    return {"status": "PROVED_NO_BASIS", "method": "exhaustive parity branches + Groebner ideals + det(T) saturation",
            "branches_completed": branches, "branches_inconsistent": inconsistent,
            "meaning": "No global 2x2 basis makes all specified signatures matchgates; not a hardness proof"}


def example_instances() -> dict[str, dict[str, Any]]:
    return {
        "read2": {"clauses": [{"kind": "exact_one", "arity": 3}],
                  "variables": [{"kind": "equality", "arity": 2}]},
        "mg3": {"clauses": [{"kind": "exact_one", "arity": 3}],
                "variables": [{"kind": "equality", "arity": 3}]},
        "super4": {"clauses": [{"kind": "fused_exact_one", "scope": [0, 1, 2, 3],
                                "clauses": [[0, 1, 2], [0, 1, 3]]}],
                   "variables": [{"kind": "equality", "arity": 3}]},
        "eq4": {"clauses": [{"kind": "exact_one", "arity": 3}],
                "variables": [{"kind": "equality", "arity": 4}]},
    }


def run_self_test() -> dict[str, Any]:
    examples = example_instances()
    checks: dict[str, bool] = {}
    e3 = make_signature({"kind": "exact_one", "arity": 3})
    eq3 = make_signature({"kind": "equality", "arity": 3})
    eq4 = make_signature({"kind": "equality", "arity": 4})
    fused = make_signature(examples["super4"]["clauses"][0])
    checks["F_super support 1000,0100,0011"] = {f"{i:04b}" for i,v in enumerate(fused.values) if v} == {"1000","0100","0011"}
    checks["EXACT1_3 matchgate"] = verify_matchgate(e3.values, 3)[0]
    checks["EQ3 fails parity"] = not verify_matchgate(eq3.values, 3)[0]
    checks["EQ4 fails MGI"] = not verify_matchgate(eq4.values, 4)[0]
    checks["super4 fails parity"] = not verify_matchgate(fused.values, 4)[0]
    checks["Read2 identity works"] = forward_verify(sp.eye(2), [e3], [make_signature({"kind":"equality","arity":2})])["valid"]
    checks["MG3 identity fails"] = not forward_verify(sp.eye(2), [e3], [eq3])["valid"]
    checks["MG3 Hadamard fails"] = not forward_verify(sp.Matrix([[1,1],[1,-1]]), [e3], [eq3])["valid"]
    A01,A02,A03,A12,A13,A23 = 2,3,5,7,11,13
    vals = [sp.Integer(0)]*16
    vals[0] = 1
    for idx, x in {12:A01,10:A02,9:A03,6:A12,5:A13,3:A23}.items():
        vals[idx] = x
    vals[15] = A01*A23-A02*A13+A03*A12
    checks["valid Pfaffian chart passes"] = verify_matchgate(tuple(vals),4)[0]
    vals[15] += 1
    checks["invalid Pfaffian chart fails"] = not verify_matchgate(tuple(vals),4)[0]
    return {"passed": sum(checks.values()), "total": len(checks), "checks": checks}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", help="JSON file with clauses and variables signature families")
    ap.add_argument("--demo", choices=["read2", "mg3", "super4", "eq4"])
    ap.add_argument("--example", action="store_true", help="Print example input JSON")
    ap.add_argument("--self-test", action="store_true", help="Run exact regression checks")
    ap.add_argument("--timeout", type=float, default=45.0, help="Total basis-search timeout, seconds (default 45)")
    ap.add_argument("--max-arity", type=int, default=5, help="Maximum supported tensor arity (default 5, may use 6)")
    ap.add_argument("--max-profiles", type=int, default=32, help="Maximum parity profiles to explore")
    ap.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args()
    if args.worker:
        try:
            print(json.dumps(groebner_branch(json.loads(sys.stdin.read())), default=str))
            return 0
        except Exception as exc:
            print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
            return 2
    if args.example:
        print(json.dumps(example_instances()["super4"], indent=2))
        return 0
    if args.self_test:
        report = run_self_test()
        print(json.dumps(report, indent=2))
        return 0 if report["passed"] == report["total"] else 1
    if (args.input is None) == (args.demo is None):
        ap.error("Specify exactly one of --demo or --input (or --example / --self-test)")
    try:
        if args.demo:
            instance = example_instances()[args.demo]
        else:
            with open(args.input, encoding="utf-8") as fh:
                instance = json.load(fh)
        if args.timeout <= 0 or args.max_arity < 1 or args.max_arity > 6 or args.max_profiles < 1:
            raise ValueError("Set --timeout > 0, --max-arity between 1 and 6, --max-profiles >= 1")
        result = solve_instance(instance, args.timeout, args.max_arity, args.max_profiles)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({"status": "INPUT_ERROR", "reason": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
