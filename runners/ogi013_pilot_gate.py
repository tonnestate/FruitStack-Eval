"""Pre-dispatch budget gate for the OGI-013 pilot (stdlib only). Inactive unless OGI013_PILOT_BUDGET is set (the frozen conditions never set it); once set, anything missing, unreadable
or over budget refuses the dispatch BEFORE it reaches a provider, writes PILOT_HALT and raises. Env (set by evidence/ogi013-pilot/run_pilot.sh): OGI013_PILOT_BUDGET, _GUARD (pilot_guard.py),
_RUNS (runs dir), _ARMS (comma list of arm dirs under it), _ARM (this process's arm), _START (epoch seconds)."""
import importlib.util
import json
import os


class PilotBudgetStop(RuntimeError):
    pass


def check() -> None:
    path = os.environ.get("OGI013_PILOT_BUDGET")
    if not path:
        return
    runs = os.environ.get("OGI013_PILOT_RUNS")
    try:
        missing = [k for k in ("OGI013_PILOT_GUARD", "OGI013_PILOT_RUNS", "OGI013_PILOT_ARMS", "OGI013_PILOT_ARM", "OGI013_PILOT_START") if not os.environ.get(k)]
        if missing:
            raise PilotBudgetStop(f"pilot gate misconfigured, missing {missing}")
        spec = importlib.util.spec_from_file_location("pilot_guard", os.environ["OGI013_PILOT_GUARD"])
        guard = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(guard)
        with open(path, encoding="utf-8") as f:
            budget = json.load(f)
        why = guard.precheck(budget, runs, os.environ["OGI013_PILOT_ARMS"].split(","), os.environ["OGI013_PILOT_ARM"], float(os.environ["OGI013_PILOT_START"]))
    except PilotBudgetStop as exc:
        why = [str(exc)]
    except Exception as exc:  # noqa: BLE001 - an unreadable budget or guard is a refusal, never a pass
        why = [f"pilot gate error {type(exc).__name__}: {str(exc)[:200]}"]
    if why:
        if runs and os.path.isdir(runs) and not os.path.exists(os.path.join(runs, "PILOT_HALT")):
            with open(os.path.join(runs, "PILOT_HALT"), "w", encoding="utf-8") as f:
                json.dump({"why": why, "by": "pre-dispatch gate"}, f)
        raise PilotBudgetStop("; ".join(why))
