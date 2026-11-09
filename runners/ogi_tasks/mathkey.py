"""MATH-500 level-5 adapter. Grader: math-verify (HF, Apache-2.0) symbolic/numeric equivalence on sympy,
as declared for D4 in evidence/ogi-study-package/task_domains.md. Unparsable = wrong.
The answer key and the reference solution never enter the prompt (see build())."""
from __future__ import annotations

from math_verify import parse, verify

PROMPT = """Solve the following problem. Reason step by step, then give the final answer as \\boxed{{...}}.

{problem}"""


def build(row: dict) -> tuple[dict, dict]:
    public = {"id": row["unique_id"], "family": "math", "prompt": PROMPT.format(problem=row["problem"].strip()),
              "visible_checks": ""}
    return public, {"answer": row["answer"], "solution": row.get("solution")}


def gold(key: str) -> list:
    g = parse("\\boxed{" + key + "}")
    if not g:
        raise ValueError(f"answer key not parsable: {key!r}")
    return g


def extract(answer: str) -> list:
    return parse(answer)


def equivalent(gold_parsed: list, pred_parsed: list) -> bool:
    return bool(pred_parsed) and verify(gold_parsed, pred_parsed)
