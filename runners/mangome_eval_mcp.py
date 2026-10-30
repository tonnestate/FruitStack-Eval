#!/usr/bin/env python3
"""Evaluation-scoped, READ-ONLY MangoMe MCP instance (lead decision D1).

Binds to the evaluation database through MangoMe's own binding guard (MANGOME_DATABASE == MANGOME_EXPECTED_DATABASE, state BOUND) and exposes only the three observation tools
(mangome_status / mangome_observe / mangome_query); mangome_work / _effect / _verify / _control are removed, so the operator cannot write evaluation state.
Evaluations never write the canonical database `mangome`; this server refuses to start on it.
usage: mangome_eval_mcp.py [--database NAME]     (default NAME=mangome_ogi013_collab1)
Register (operator, name chosen so MangoMe's shadow check does not mistake it for a second canonical server):
  claude mcp add ogi013-eval-ledger -- <managed python> /root/fruits/integration/ogi013-collab-proof/runners/mangome_eval_mcp.py
"""
from __future__ import annotations

import argparse
import os
import sys

READ_TOOLS = {"mangome_status", "mangome_observe", "mangome_query"}


def build(database: str):
    if database == "mangome":
        raise SystemExit("REFUSED: the evaluation-scoped instance never binds the canonical database 'mangome'")
    os.environ.update({"MANGOME_BACKEND": os.environ.get("MANGOME_BACKEND", "mongo"), "MANGOME_DATABASE": database, "MANGOME_EXPECTED_DATABASE": database,
                       "MANGOME_ZERO_TOUCH_BOOTSTRAP": "0", "MANGOME_RUNTIME_ROLE": "WORKER"})
    from mangome import worker_mcp_server
    mcp = worker_mcp_server.mcp
    manager = mcp._tool_manager
    for name in [t.name for t in manager.list_tools()]:
        if name not in READ_TOOLS:
            manager.remove_tool(name)
    left = {t.name for t in manager.list_tools()}
    if left != READ_TOOLS:
        raise SystemExit(f"READ_ONLY_SURFACE_MISMATCH: {sorted(left)}")
    return mcp


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--database", default="mangome_ogi013_collab1")
    build(ap.parse_args(argv).database).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
