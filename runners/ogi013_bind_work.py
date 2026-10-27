#!/usr/bin/env python3
"""Admit ONE real MangoMe WorkIdentity + EXECUTE turn (isolated eval DB) and print the OGI013_* exports the tau2 runner requires.
Usage: ogi013_bind_work.py "<request text>" > work.env"""
import os
import sys
import uuid

from mangome.runtime import get_service
from orangeme.runtime import OrangeRuntime

ACTOR = os.environ.get("ORANGEME_AGENT_ID", "claude-code-ogi")
text = sys.argv[1]
m = get_service()
e = m.enter_work(workspace_id=f"/ogi013/exp-{uuid.uuid4().hex[:8]}", workspace_title="OGI-013 tau2 experiment", actor_id=ACTOR, request_text=text)
work, project = e["work_identity"]["entity_id"], e["project"]["project_key"]
turn = m.bind_work_turn(work_ref=work, request_text=text, mode="EXECUTE", actor_id=ACTOR, authorized_by=ACTOR)
turn_id = turn["turn"]["entity_id"]  # the work_turn_bindings key MangoWorkAdapter.turn_authorized re-reads
ort = OrangeRuntime()
try:
    ort.register_project(project, os.environ["ORANGEME_SOURCE_REPO"], "main", {"vps": os.environ["ORANGEME_SOURCE_REPO"]})
except Exception:
    pass
led = ort.project_ledger(project)
if led.get("memory/working") is None:
    led.put("memory/working", {"verified_findings": []}, expected_revision=0)
print(f"export OGI013_WORK_REF={work} OGI013_PROJECT_REF={project} OGI013_TURN_ID={turn_id} OGI013_ACTOR_ID={ACTOR}")
