#!/usr/bin/env python3
"""Simulator preflight for the pilot: is the pinned customer-simulator model executable RIGHT NOW? No inference. It builds a PlumMe service exactly as the arms do (fresh state dir, model-catalogue
snapshot, optional FLM_KEY source, metadata discovery) and asks PlumMe's own hard-eligibility gate whether a route of the pinned model passes. Exit 0 = executable, 1 = not (with PlumMe's reasons),
2 = the check itself could not run. usage: sim_preflight.py ROUTE_FILE STATE_DIR   (ROUTE_FILE = {"model_key": ...}); run with the host python and the same PYTHONPATH as the arms."""
import asyncio
import json
import os
import shutil
import sys
from pathlib import Path


def check(svc, model_key: str) -> dict:
    from ogi013_sim_supply import _earliest_retry, _explain
    known = any(str(o.model_key) == str(model_key) for o in svc.store.offers.values())
    wait = _earliest_retry(svc, model_key) if known else None
    return {"model_key": model_key, "model_known_to_plumme": known, "executable": known and wait == 0.0, "retry_after_s": wait, "explain": _explain(svc, model_key) if known else {}}


def build_service(state_dir: Path):
    from plumme.config import Settings
    from plumme.credentials import CredentialSource, CredentialSourceKind
    from plumme.service import PlumMeService, default_adapters
    os.environ["PLUMME_STATE_DIR"] = str(state_dir / "plumme-state")
    (state_dir / "plumme-state" / "knowledge").mkdir(parents=True, exist_ok=True)
    snap = Path("/root/fruits/research/FRUITSTACK-EVAL-004/inputs/models.dev-api.json")
    if snap.exists():
        shutil.copyfile(snap, state_dir / "plumme-state" / "knowledge" / "models.dev-api.json")
    settings = Settings.load()
    svc = PlumMeService(settings, adapters=default_adapters(settings))
    if os.environ.get("FLM_KEY"):
        svc.credentials.register_source(CredentialSource("freellmapi", CredentialSourceKind.ENV_REFERENCE, "freellmapi-isolated-instance", {"var": "FLM_KEY"}))
    asyncio.run(svc.discover())
    return svc


def main(argv) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2
    try:
        model_key = json.loads(Path(argv[1]).read_text())["model_key"]
        result = check(build_service(Path(argv[2])), model_key)
    except Exception as exc:  # noqa: BLE001 - a preflight that cannot run must not pass
        print(json.dumps({"executable": False, "error": f"{type(exc).__name__}: {str(exc)[:300]}"}))
        return 2
    print(json.dumps(result, default=str))
    return 0 if result["executable"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
