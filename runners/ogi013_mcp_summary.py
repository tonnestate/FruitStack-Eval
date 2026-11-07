"""Operator read of an episode through the evaluation-scoped READ-ONLY MangoMe MCP (real stdio round trip): prints a 10-line summary of positions, candidates, objections and release.
usage: ogi013_mcp_summary.py WORK_REF [DATABASE]"""
import asyncio
import json
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

work, db = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "mangome_ogi013_collab1")
params = StdioServerParameters(command=sys.executable, args=[str(Path(__file__).with_name("mangome_eval_mcp.py")), "--database", db], env={**os.environ, "MANGOME_WORKSPACE_ROOT": "/tmp"})


async def go():
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()
            tools = sorted(t.name for t in (await session.list_tools()).tools)
            res = await session.call_tool("mangome_query", {"operation": "WORK_CONTEXT", "payload": {"work_ref": work}})
            return tools, res.structured_content


tools, out = asyncio.run(go())
ctx = out.get("result", out)
st = ctx["progressive"]["latest_checkpoint"]["payload"]
c = st.get("candidates", [])
lines = [f"MCP tools exposed (read-only): {tools}",
         "positions: " + "; ".join(f"{p['id']} slot={p.get('slot')} model={p['model']} status={p['status']} rev={p['rev']} sha={p['sha256'][:10]}" for p in st["pos"]),
         f"candidates: {len(c)}: " + "; ".join(f"{x['id']} {x['status']}{'(' + x['reason'] + ')' if x.get('reason') else ''} sha={x['sha256'][:10]}" for x in c),
         f"objections: {len(st['objs'])} (grounded {sum(1 for o in st['objs'] if o.get('grounded'))}); states: {dict(__import__('collections').Counter(o['state'] for o in st['objs']))}",
         f"replies: {sum(len(o.get('replies', [])) for o in st['objs'])}; specialist-decided: {sum(1 for o in st['objs'] if o.get('decided_by') == 'specialist')}; decisions logged: {len(st['decisions'])}",
         f"votes: {len(st['votes'])}: {[v.get('verdict') for v in st['votes']]}",
         f"release: {json.dumps({k: (v if k != 'votes' else len(v)) for k, v in (st['release'] or {}).items() if k in ('class', 'released', 'candidate_sha256', 'guard', 'withdrawals')})}",
         f"roster: {st.get('roster')}; roster changes: {len(st.get('roster_changes', []))}",
         f"state version {st.get('version')}, latest checkpoint seq {ctx['progressive']['latest_checkpoint']['payload'].get('seq')}, work {work}"]
print("\n".join(lines[:10]))
