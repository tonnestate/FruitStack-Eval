"""Calibration tasks with exact answers for readiness gate G2.

Every task is generated from a seed and has exactly one correct answer, so a worker's
answer is checked by the harness (HARNESS_OBSERVED), never by another model. Six kinds
at graded difficulty keep error rates away from 0 and 1; error correlation between
provider groups cannot be measured on tasks that every group solves or fails.

Answer format, stated in every prompt: the last line reads `ANSWER: <value>`.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
import string
from datetime import date, timedelta

SCHEMA = "FSE-CALIB/1"
KINDS = ("multiply", "count_letter", "kth_smallest", "date_shift", "mod_chain", "word_sort")
FORMAT = "Reply with your reasoning if you like, but end with one final line of the form: ANSWER: <value>"
_ANSWER = re.compile(r"ANSWER\s*[:=]\s*(.+)", re.I)


def _multiply(rng: random.Random, level: int) -> tuple[str, str]:
    digits = [(3, 2), (4, 3), (5, 4), (7, 5)][level]
    a = rng.randrange(10 ** (digits[0] - 1), 10 ** digits[0])
    b = rng.randrange(10 ** (digits[1] - 1), 10 ** digits[1])
    return f"Compute {a} × {b} exactly. Give the integer without separators.", str(a * b)


def _count_letter(rng: random.Random, level: int) -> tuple[str, str]:
    length = [30, 60, 100, 160][level]
    letter = rng.choice("aeiorstn")
    text = "".join(rng.choice(string.ascii_lowercase) for _ in range(length))
    return f"How many times does the letter '{letter}' occur in this string?\n{text}", str(text.count(letter))


def _kth_smallest(rng: random.Random, level: int) -> tuple[str, str]:
    size = [9, 17, 29, 45][level]
    values = rng.sample(range(-999, 1000), size)
    k = rng.randrange(2, size)
    return (f"Here is a list of {size} distinct integers: {', '.join(map(str, values))}.\n"
            f"Sorted in ascending order, which number is at position {k} (position 1 is the minimum)?",
            str(sorted(values)[k - 1]))


def _date_shift(rng: random.Random, level: int) -> tuple[str, str]:
    start = date(1990, 1, 1) + timedelta(days=rng.randrange(0, 365 * 40))
    span = [rng.randrange(5, 40), rng.randrange(40, 400), rng.randrange(400, 3000), rng.randrange(3000, 20000)][level]
    sign = rng.choice([1, -1]) if level >= 2 else 1
    target = start + timedelta(days=sign * span)
    verb = "after" if sign > 0 else "before"
    weekday = level == 3
    question = (f"Which date is {span} days {verb} {start.isoformat()}? "
                + ("Give the weekday in English." if weekday else "Give the date as YYYY-MM-DD."))
    return question, (target.strftime("%A").lower() if weekday else target.isoformat())


def _mod_chain(rng: random.Random, level: int) -> tuple[str, str]:
    steps = [3, 6, 9, 13][level]
    modulus = rng.choice([97, 101, 211, 997])
    value = rng.randrange(2, 500)
    ops, current = [], value
    for _ in range(steps):
        op = rng.choice(["add", "mul", "sub"])
        n = rng.randrange(2, 60)
        if op == "add":
            current += n
            ops.append(f"add {n}")
        elif op == "sub":
            current -= n
            ops.append(f"subtract {n}")
        else:
            current *= n
            ops.append(f"multiply by {n}")
        current %= modulus
        ops[-1] += f", then reduce modulo {modulus}"
    text = "; ".join(ops)
    return (f"Start with {value}. Apply these steps in order: {text}. "
            f"Each reduction gives a result between 0 and {modulus - 1}. What is the final number?", str(current))


def _word_sort(rng: random.Random, level: int) -> tuple[str, str]:
    count = [5, 8, 11, 15][level]
    words = set()
    while len(words) < count:
        words.add("".join(rng.choice("bcdfghklmnprstvz" if i % 2 == 0 else "aeiou")
                          for i in range(rng.randrange(4, 8))))
    shuffled = list(words)
    rng.shuffle(shuffled)
    return (f"Sort these words alphabetically and list them separated by commas: {', '.join(shuffled)}",
            ",".join(sorted(words)))


_BUILDERS = {"multiply": _multiply, "count_letter": _count_letter, "kth_smallest": _kth_smallest,
             "date_shift": _date_shift, "mod_chain": _mod_chain, "word_sort": _word_sort}


def generate(n: int, seed: int) -> list[dict]:
    """n tasks, cycling through kinds and four difficulty levels."""
    if n < len(KINDS):
        raise ValueError(f"need at least {len(KINDS)} tasks")
    rng = random.Random(seed)
    tasks = []
    for i in range(n):
        kind = KINDS[i % len(KINDS)]
        level = (i // len(KINDS)) % 4
        question, answer = _BUILDERS[kind](rng, level)
        prompt = f"{question}\n\n{FORMAT}"
        tasks.append({"schema": SCHEMA, "task_id": f"calib-{seed}-{i:04d}", "kind": kind, "level": level,
                      "prompt": prompt, "answer": answer})
    return tasks


def task_set_digest(tasks: list[dict]) -> str:
    body = [{"task_id": t["task_id"], "prompt": t["prompt"], "answer": t["answer"]} for t in tasks]
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def extract(output: str | None) -> str | None:
    if not output:
        return None
    matches = _ANSWER.findall(output)
    return matches[-1].strip() if matches else None


def normalize(kind: str, value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip().strip("`*_ ").rstrip(".").strip()
    if kind in ("multiply", "count_letter", "kth_smallest", "mod_chain"):
        text = re.sub(r"[\s,_'’]", "", text).replace("−", "-")
        return text if re.fullmatch(r"-?\d+", text) else text.lower()
    if kind == "word_sort":
        return ",".join(w.strip().lower() for w in re.split(r"[,\s]+", text) if w.strip())
    if kind == "date_shift":
        return text.lower()
    return text


def score(tasks: list[dict], results: list[dict]) -> tuple[list[dict], list[str]]:
    """Attach `answer_given`, `parsed` and `correct` to each result row.

    A row without a successful execution keeps `executed = False` and no correctness.
    A row whose output has no ANSWER line is executed but unparsed and counts as wrong.
    """
    by_id = {t["task_id"]: t for t in tasks}
    scored, warnings = [], []
    for row in results:
        task = by_id.get(row.get("task_id"))
        if task is None:
            warnings.append(f"result for unknown task {row.get('task_id')}")
            continue
        executed = bool(row.get("success")) and row.get("structural_state") == "WELL_FORMED"
        given = normalize(task["kind"], extract(row.get("output"))) if executed else None
        out = {k: row.get(k) for k in ("task_id", "offer_id", "group", "provider", "model", "receipt_id",
                                       "decision_id", "model_fingerprint")}
        out.update({"kind": task["kind"], "level": task["level"], "executed": executed,
                    "parsed": given is not None, "answer_given": given,
                    "correct": (given == task["answer"]) if executed else None})
        scored.append(out)
    return scored, warnings
