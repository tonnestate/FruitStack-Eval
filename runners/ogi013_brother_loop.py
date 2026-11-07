"""Production adapter of the Brother Mode closed loop (IMPLEMENTED; offline-tested only): builds the cooperation control whose every decision (weight update, action choice,
closing rule) is written to MangoMe with its inputs. No model call. Used by ogi013_qa1.run_T(loop=True) through cherryme.brother.run_rounds(control=...)."""
from __future__ import annotations

from fs_codemode.loop import CooperationControl, LoopParams


def _reviewer_history(decision_log, task_class: str) -> dict:
    """Read task-matched, independently verified PlumMe reviews without creating another store."""
    if decision_log is None or not task_class:
        return {}
    counts = {}
    seen = set()
    for review in decision_log.reviews:
        if (review.review_id in seen or review.task_class != task_class or review.improved_outcome is None
                or not review.verifier.strip() or not review.proposer_model_key):
            continue
        decision = decision_log.decisions.get(review.decision_id)
        choice = getattr(decision, "model_choice", None)
        groups = (getattr(decision, "independence", None) or {}).get("selected_groups", []) if decision else []
        models = choice.selected_model_key.split(",") if choice and choice.selected_model_key else []
        if (not decision or decision.request_features.get("question_type") != task_class
                or len(models) != len(groups) or review.reviewer_model_key not in models
                or review.proposer_model_key not in models):
            continue
        independence = dict(zip(models, groups))
        if (not independence.get(review.reviewer_model_key) or not independence.get(review.proposer_model_key)
                or independence[review.reviewer_model_key] == independence[review.proposer_model_key]):
            continue
        key = (review.reviewer_model_key, review.proposer_model_key)
        row = counts.setdefault(key, {"n": 0, "improved": 0, "task_class": task_class})
        row["n"] += 1
        row["improved"] += int(review.improved_outcome)
        seen.add(review.review_id)
    return counts


def reviewer_improvement_signal(decision_log, reviewer_model_key: str, task_class: str) -> dict:
    rows = [row for (reviewer, _), row in _reviewer_history(decision_log, task_class).items() if reviewer == reviewer_model_key]
    n, improved = sum(x["n"] for x in rows), sum(x["improved"] for x in rows)
    return {"n": n, "improved": improved, "rate": improved / n if n else None}


def make_control(mango_ledger, qid: str, models: tuple = (), params: LoopParams = LoopParams(), *, decision_log=None, task_class: str = "", log_sink=None) -> CooperationControl:
    n = {"i": 0}

    def log(record: dict) -> None:
        n["i"] += 1
        if sink is not None:
            sink(dict(record))
        else:
            mango_ledger.write("LOOP_DECISION", f"{qid}:{n['i']}:{record.get('type')}", dict(record))
    sink = log_sink
    ctl = CooperationControl(params, log=log, models=models, reviewer_history=_reviewer_history(decision_log, task_class))
    ctl.records = n
    return ctl
