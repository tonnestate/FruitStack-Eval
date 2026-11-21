"""Executed refutation of the iteration-2 hypothesis "#F is even iff all satisfying assignments are monochromatic" (both directions),
by brute force and an independent SAT model enumeration in the PhysalisMe sandbox (tool call, no model call)."""
import asyncio, json, httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client

CODE = r'''
from itertools import product
from pysat.solvers import Glucose4
def models_brute(n, cnf):
    return [a for a in product((0, 1), repeat=n) if all(any((a[abs(l) - 1] == 1) == (l > 0) for l in c) for c in cnf)]
def models_sat(n, cnf):
    with Glucose4(bootstrap_with=cnf + [[v, -v] for v in range(1, n + 1)]) as s:
        return sorted(tuple(int(x > 0) for x in m[:n]) for m in s.enum_models())
def main(I):
    out = {}
    for name, n, cnf in (("F1 = x1 over 2 variables", 2, [[1]]), ("F2 = x1 and x2", 2, [[1], [2]])):
        b, s = sorted(models_brute(n, cnf)), models_sat(n, cnf)
        mono = all(len(set(m)) == 1 for m in b)
        out[name] = {"models": b, "count": len(b), "even": len(b) % 2 == 0, "all_monochromatic": mono, "methods_agree": b == s,
                     "hypothesis_holds": (len(b) % 2 == 0) == mono}
    return out
'''

async def main():
    c = Client(streamable_http_client('http://physalisme/mcp', http_client=httpx2.AsyncClient(transport=httpx2.AsyncHTTPTransport(uds='/run/physalisme/mcp.sock'), timeout=200)))
    async with c:
        r = await c.call_tool("physalis_code_run", {"code": CODE, "input": {}, "timeout_s": 120})
        print(json.dumps(r.structured_content, default=str))
asyncio.run(main())
