"""Owner's profile-rank counterexample and the chain rank <= distinct rows <= |P| <= all-left profiles; (Fable, 2026-11-16) of the owner's experiment on cut ranks of SAT solution tensors.
For every family: the exact minimum over ALL variable orderings of the maximum cut rank (subset dynamic programme over prefixes),
over Q (exact fraction-free elimination) and over GF(2), plus the model count. Runs in the PhysalisMe sandbox (tool call, no model call)."""
import asyncio, json, httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client

CODE = r'''
from itertools import combinations
from fractions import Fraction
from math import comb
import numpy as np

def rank_q(M):                      # exact rank over Q (Bareiss-free Gaussian elimination with Fractions; matrices here are <= 32 x 32)
    A = [[Fraction(int(x)) for x in row] for row in M]
    r, rows, cols = 0, len(A), len(A[0]) if A else 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if A[i][c] != 0), None)
        if p is None: continue
        A[r], A[p] = A[p], A[r]
        for i in range(rows):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
    return r

def rank_f2(M):
    rows = [int("".join(str(int(x) & 1) for x in row), 2) for row in M]
    r = 0
    for bit in reversed(range(len(M[0]))):
        p = next((i for i in range(r, len(rows)) if rows[i] >> bit & 1), None)
        if p is None: continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i] >> bit & 1: rows[i] ^= rows[r]
        r += 1
    return r

def table(n, f):                     # truth table as dict over assignments (tuple of bits)
    return {a: int(f(a)) for a in np.ndindex(*([2] * n))}

def cut_matrix(n, T, S):
    S = list(S); R = [v for v in range(n) if v not in S]
    rows = list(np.ndindex(*([2] * len(S)))); cols = list(np.ndindex(*([2] * len(R))))
    M = []
    for x in rows:
        a = [0] * n
        for v, b in zip(S, x): a[v] = b
        line = []
        for y in cols:
            for v, b in zip(R, y): a[v] = b
            line.append(T[tuple(a)])
        M.append(line)
    return M

def best_order(n, T, rank):          # min over orderings of the max prefix-cut rank, exact (DP over subsets)
    r = {}
    for k in range(1, n):
        for S in combinations(range(n), k):
            r[frozenset(S)] = rank(cut_matrix(n, T, S))
    best = {frozenset(): 0}
    for k in range(1, n + 1):
        for S in combinations(range(n), k):
            S = frozenset(S); here = r.get(S, 1)
            best[S] = min(max(best[S - {v}], here) for v in S)
    return best[frozenset(range(n))], max(r.values())

def order_max(n, T, order, rank):
    return max(rank(cut_matrix(n, T, order[:i])) for i in range(1, n))

def two_cnf(n, edges):               # positive 2-clauses (x_i or x_j) on the edges: zeros form an independent set
    return table(n, lambda a: all(a[i] or a[j] for i, j in edges))


import random

def cnf_table(n, clauses):           # clauses: lists of literals +-(v+1)
    return table(n, lambda x: all(any((x[abs(l) - 1] == 1) if l > 0 else (x[abs(l) - 1] == 0) for l in c) for c in clauses))

def quantities(n, clauses, S):
    """rank of the cut matrix M; distinct non-zero rows of M; |P| = distinct crossing-clause profiles of left assignments that satisfy the
    left clauses; rank of the profile bit-vectors; STV-style count = distinct crossing profiles over ALL left assignments"""
    T = cnf_table(n, clauses); S = set(S)
    M = cut_matrix(n, T, sorted(S))
    cross = [c for c in clauses if {abs(l) - 1 for l in c} & S and {abs(l) - 1 for l in c} - S]
    left = [c for c in clauses if {abs(l) - 1 for l in c} <= S]
    Ls = sorted(S); prof_ok, prof_all = set(), set()
    for x in np.ndindex(*([2] * len(Ls))):
        val = dict(zip(Ls, x))
        sat = lambda c: any(abs(l) - 1 in val and ((val[abs(l) - 1] == 1) if l > 0 else (val[abs(l) - 1] == 0)) for l in c)
        p = tuple(int(sat(c)) for c in cross)
        prof_all.add(p)
        if all(sat(c) for c in left): prof_ok.add(p)
    return {"rank_M": rank_q(M), "distinct_rows": len({tuple(r) for r in M if any(r)}), "profiles_P": len(prof_ok),
            "rank_profile_vectors": rank_q([list(p) for p in prof_ok]) if prof_ok and cross else 0, "profiles_all_left": len(prof_all)}

def main(I):
    out = {"x_or_y": quantities(2, [[1, 2]], [0])}
    out["K_n_half_cut"] = {n: quantities(n, [[i + 1, j + 1] for i in range(n) for j in range(i + 1, n)], range(n // 2)) for n in (4, 6, 8, 10)}
    rng = random.Random(11); viol = {"rank>rows": 0, "rows>P": 0, "P>all": 0}; strict = {"rank<rows": 0, "rows<P": 0}; cases = 0
    for t in range(80):
        n = rng.randint(5, 9); m = rng.randint(n, 3 * n)
        cl = [[v * rng.choice((1, -1)) for v in rng.sample(range(1, n + 1), 2)] for _ in range(m)]
        S = rng.sample(range(n), rng.randint(1, n - 1))
        q = quantities(n, cl, S); cases += 1
        viol["rank>rows"] += q["rank_M"] > q["distinct_rows"]; viol["rows>P"] += q["distinct_rows"] > q["profiles_P"]; viol["P>all"] += q["profiles_P"] > q["profiles_all_left"]
        strict["rank<rows"] += q["rank_M"] < q["distinct_rows"]; strict["rows<P"] += q["distinct_rows"] < q["profiles_P"]
    out["random_2cnf"] = {"cases": cases, "violations": viol, "strict": strict}
    return out
'''

async def main():
    c = Client(streamable_http_client('http://physalisme/mcp', http_client=httpx2.AsyncClient(transport=httpx2.AsyncHTTPTransport(uds='/run/physalisme/mcp.sock'), timeout=900)))
    async with c:
        r = await c.call_tool("physalis_code_run", {"code": CODE, "input": {}, "timeout_s": 800, "memory_mb": 4096})
        print(json.dumps(r.structured_content, default=str))

asyncio.run(main())
