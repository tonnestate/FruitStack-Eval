"""Pre-dispatch budget gate for the OGI-013 pilot (stdlib only). Inactive unless OGI013_PILOT_BUDGET is set (the frozen conditions never set it); once set, anything missing, unreadable
or over budget refuses the dispatch BEFORE it reaches a provider, writes PILOT_HALT and raises. Env (set by evidence/ogi013-pilot/run_pilot.sh): OGI013_PILOT_BUDGET, _GUARD (pilot_guard.py),
_RUNS (runs dir), _ARMS (comma list of arm dirs under it), _ARM (this process's arm), _START (epoch seconds)."""
import contextlib
import importlib.util
import json
import os
import time


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
    the owner-approved per-step ceiling (max_tokens_per_step) and the provider requests still allowed (calls). Unreadable configuration = a stop, never a pass."""
    if not os.environ.get("OGI013_PILOT_BUDGET"):
        return None
    try:
        guard, budget = _guard_and_budget()
        arms, arm = os.environ["OGI013_PILOT_ARMS"].split(","), os.environ["OGI013_PILOT_ARM"]
        u = guard.usage(os.environ["OGI013_PILOT_RUNS"], arms, budget["reserve_tokens_per_dispatch"])
        head = min(guard.arm_cap(budget, arm)["max_tokens"] - u["per_arm"].get(arm, {"tokens": 0})["tokens"], budget["cumulative"]["max_tokens"] - u["tokens"])
        cap = guard.arm_cap(budget, arm)
        calls = min(cap["max_dispatches"] - u["per_arm"].get(arm, {"dispatches": 0})["dispatches"], budget["cumulative"]["max_dispatches"] - u["dispatches"])       # provider REQUESTS still allowed (receipts expanded by their attempts)
        return {"headroom": max(0, head), "per_step": int(budget["max_tokens_per_step"]), "calls": max(0, calls)}
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


@contextlib.contextmanager
def step_parent_budget(svc, tokens, calls, account_to=None, who="step"):
    """Pilot only: PlumMe's own cross-request control for ONE step. A PlumMe ParentBudget bound to the scheduler is checked before EVERY provider request of the step - the first attempt, each
    continuation of a truncated answer and each credential-rotation retry - against the step's total tokens (charged = the provider's recorded usage of the earlier requests + what is outstanding +
    this request's input estimate and output cap), its provider-request count and zero cash; each response is also limited to the headroom left (ParentBudget.output_headroom). Yields the
    ParentBudget (read its snapshot afterwards) or None when this is not the pilot or the service has no such control. An already bound parent budget (an enclosing inquiry) is left in charge."""
    set_parent = getattr(svc, "set_parent_budget", None)
    if tokens is None or calls is None or not callable(set_parent) or getattr(svc, "parent_budget", None) is not None:
        yield None
        return
    if tokens < 1 or calls < 1:
        raise PilotBudgetStop(f"no room for one more provider request (tokens {tokens}, requests {calls})")
    from plumme.budget import ParentBudget
    parent = ParentBudget(max_provider_calls=int(calls), max_total_tokens=int(tokens), max_cost_usd=0.0)
    parent.receipted = False                       # the caller sets it once the step's own receipt carries the usage of ALL its requests
    receipts_path = getattr(getattr(getattr(svc, "scheduler", None), "receipts", None), "path", None)
    receipts_before = len(_receipt_lines(receipts_path))
    set_parent(parent)
    try:
        yield parent
    finally:
        set_parent(None)
        if not parent.receipted:
            _account_unreceipted(account_to, who, parent, receipts_path, receipts_before)


def _receipt_lines(path) -> list[str]:
    try:
        return [x for x in open(path, encoding="utf-8").read().splitlines() if x.strip()] if path and os.path.exists(path) else []
    except OSError:
        return []


def _account_unreceipted(directory, who, parent, receipts_path=None, receipts_before=0) -> None:
    """A step that failed AFTER some of its requests were answered (e.g. a continuation refused by the step budget) can end in a failed receipt WITHOUT usage although the earlier requests consumed
    tokens. The parent budget holds the provider's recorded usage of ALL the step's requests. Whatever the step's own new receipts (by position after `receipts_before`, identified by receipt_id)
    already carry is NOT charged again; only the remainder is written next to the receipts (step-accounting.jsonl) for the guard, plus a conservative reserve for requests whose usage the
    provider did not report. Never silent."""
    if not directory:
        return
    snap = parent.snapshot()
    confirmed, ids = 0, []
    for line in _receipt_lines(receipts_path)[receipts_before:]:
        try:
            r = json.loads(line)
        except ValueError:
            continue
        u = r.get("usage") or {}
        known = u.get("total_tokens")
        if known is None and u.get("input_tokens") is not None and u.get("output_tokens") is not None:
            known = u["input_tokens"] + u["output_tokens"]
        confirmed += int(known or 0)
        ids.append(r.get("receipt_id"))
    extra = max(0, int(snap["charged_tokens"]) - confirmed)
    if extra > 0 or snap["unknown_usage_attempts"] > 0:
        with open(os.path.join(str(directory), "step-accounting.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps({"who": who, "requests": snap["provider_attempt_count"], "charged_tokens": extra, "parent_charged_tokens": snap["charged_tokens"], "in_receipts": confirmed,
                                "receipt_ids": ids, "unknown_usage_attempts": snap["unknown_usage_attempts"], "ts": time.time()}) + "\n")
