"""Independent check of iteration 1 (PNP-001): exact ranks of the satisfying-assignment tensor of CNF formulas across variable cuts.
Run as www-data through the live PhysalisMe sandbox (tool call, no model call). Prints one JSON result."""
import asyncio, json, httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client

CODE = r'''
import numpy as np, random
def tensor(n, clauses):
    a = np.arange(1 << n)
    ok = np.ones(1 << n, dtype=bool)
    for cl in clauses:
        sat = np.zeros(1 << n, dtype=bool)
        for lit in cl:
            v = abs(lit) - 1
            bit = (a >> (n - 1 - v)) & 1          # variable 1 is the most significant index, so a cut after i variables is a reshape
            sat |= (bit == 1) if lit > 0 else (bit == 0)
        ok &= sat
    return ok.astype(float)
def ranks(n, clauses):
    t = tensor(n, clauses)
    return [int(np.linalg.matrix_rank(t.reshape(1 << i, 1 << (n - i)))) for i in range(1, n)]
def crossing(n, clauses, i):
    return sum(1 for cl in clauses if min(abs(l) for l in cl) <= i < max(abs(l) for l in cl))
def main(I):
    rng = random.Random(I["seed"]); out = {"bound_violations": 0, "families": []}
    for n in range(3, 13):
        for trial in range(I["trials"]):
            m = int(round(4.26 * n * rng.uniform(0.3, 1.2)))
            cl = [[v * rng.choice((1, -1)) for v in rng.sample(range(1, n + 1), 3)] for _ in range(m)]
            r = ranks(n, cl)
            out["bound_violations"] += sum(1 for i, x in enumerate(r, 1) if x > min(2 ** i, 2 ** (n - i)))
            if trial == 0:
                out["families"].append({"n": n, "m": m, "ranks": r, "naive_2_pow_i": [2 ** i for i in range(1, n)], "max_possible": [min(2 ** i, 2 ** (n - i)) for i in range(1, n)]})
    # C-0039: "the exact bond dimension across a cut is determined by the number of crossing clauses, regardless of logical redundancy"
    n = 8; base = [[1, -5, 6], [2, 7, -8], [-3, 5, 4], [4, -6, 8]]
    dup = base + [base[0]]                                  # the same clause twice: more crossing clauses, identical function
    i = 4
    out["C-0039"] = {"cut_after": i, "crossing_base": crossing(n, base, i), "rank_base": ranks(n, base)[i - 1],
                     "crossing_with_duplicate": crossing(n, dup, i), "rank_with_duplicate": ranks(n, dup)[i - 1]}
    out["C-0039"]["refuted"] = out["C-0039"]["crossing_base"] != out["C-0039"]["crossing_with_duplicate"] and out["C-0039"]["rank_base"] == out["C-0039"]["rank_with_duplicate"]
    return out
'''

async def main():
    c = Client(streamable_http_client('http://physalisme/mcp', http_client=httpx2.AsyncClient(transport=httpx2.AsyncHTTPTransport(uds='/run/physalisme/mcp.sock'), timeout=300)))
    async with c:
        r = await c.call_tool("physalis_code_run", {"code": CODE, "input": {"seed": 7, "trials": 5}, "timeout_s": 240})
        print(json.dumps(r.structured_content, default=str))

asyncio.run(main())
