"""Pre-dispatch budget gate for the OGI-013 pilot (stdlib only). Inactive unless OGI013_PILOT_BUDGET is set (the frozen conditions never set it); once set, anything missing, unreadable
or over budget refuses the dispatch BEFORE it reaches a provider, writes PILOT_HALT and raises. Env (set by evidence/ogi013-pilot/run_pilot.sh): OGI013_PILOT_BUDGET, _GUARD (pilot_guard.py),
_RUNS (runs dir), _ARMS (comma list of arm dirs under it), _ARM (this process's arm), _START (epoch seconds)."""
import importlib.util
import json
import os


class PilotBudgetStop(RuntimeError):
    pass


def _guard_and_budget():
    spec = importlib.util.spec_from_file_location("pilot_guard", os.environ["OGI013_PILOT_GUARD"])
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)
    with open(os.environ["OGI013_PILOT_BUDGET"], encoding="utf-8") as f:
        return guard, json.load(f)


def token_limits() -> dict | None:
    """Pilot only (None otherwise): the tokens this arm may still commit to ONE step - min(arm cap - arm usage, pilot cap - pilot usage), agent AND simulator usage from the provider ledger -
    and the owner-approved per-step ceiling (max_tokens_per_step). Unreadable configuration = a stop, never a pass."""
    if not os.environ.get("OGI013_PILOT_BUDGET"):
        return None
    try:
        guard, budget = _guard_and_budget()
        arms, arm = os.environ["OGI013_PILOT_ARMS"].split(","), os.environ["OGI013_PILOT_ARM"]
        u = guard.usage(os.environ["OGI013_PILOT_RUNS"], arms, budget["reserve_tokens_per_dispatch"])
        head = min(budget["arms"][arm]["max_tokens"] - u["per_arm"].get(arm, {"tokens": 0})["tokens"], budget["cumulative"]["max_tokens"] - u["tokens"])
        return {"headroom": max(0, head), "per_step": int(budget["max_tokens_per_step"])}
    except Exception as exc:  # noqa: BLE001
        raise PilotBudgetStop(f"pilot token limits unavailable {type(exc).__name__}: {str(exc)[:200]}") from exc


def check() -> None:
    path = os.environ.get("OGI013_PILOT_BUDGET")
    if not path:
        return
    runs = os.environ.get("OGI013_PILOT_RUNS")
    try:
        missing = [k for k in ("OGI013_PILOT_GUARD", "OGI013_PILOT_RUNS", "OGI013_PILOT_ARMS", "OGI013_PILOT_ARM", "OGI013_PILOT_START") if not os.environ.get(k)]
        if missing:
            raise PilotBudgetStop(f"pilot gate misconfigured, missing {missing}")
        guard, budget = _guard_and_budget()
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
