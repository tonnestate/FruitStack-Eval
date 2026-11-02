"""Production adapter of the Brother Mode closed loop (IMPLEMENTED; offline-tested only): builds the cooperation control whose every decision (weight update, action choice,
closing rule) is written to MangoMe with its inputs. No model call. Used by ogi013_qa1.run_T(loop=True) through cherryme.brother.run_rounds(control=...)."""
from __future__ import annotations

from fs_codemode.loop import CooperationControl, LoopParams


def make_control(mango_ledger, qid: str, models: tuple = (), params: LoopParams = LoopParams()) -> CooperationControl:
    n = {"i": 0}

    def log(record: dict) -> None:
        n["i"] += 1
        mango_ledger.write("LOOP_DECISION", f"{qid}:{n['i']}:{record.get('type')}", dict(record))
    ctl = CooperationControl(params, log=log, models=models)
    ctl.records = n
    return ctl
