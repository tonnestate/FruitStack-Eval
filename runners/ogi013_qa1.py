"""OGI-013 QA-1 runner: arms T (team), E (equal effort, majority vote), S (best constituent), L (Luna alone), exactly as pre-registered (OGI013_QA1_PREREG.md).
Pure logic first (parsing, grading, E's k, specialist rule); the stack parts import lazily. Question texts are never written to any committed file; results hold ids, letters, hashes and grades."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter

ANSWER_RE = re.compile(r"ANSWER:\s*([A-J])\b")
LETTERS = "ABCDEFGHIJ"

QUESTION_PROMPT = ("Answer the following multiple-choice question. Think it through, then finish with exactly one line of the form 'ANSWER: <letter>' (a single capital letter naming one option).\n\n"
                   "Question: {question}\n\nOptions:\n{options}\n")


def render_options(options: list) -> str:
    return "\n".join(f"{LETTERS[i]}. {o}" for i, o in enumerate(options))


def question_prompt(q: dict) -> str:
    return QUESTION_PROMPT.format(question=q["question"], options=render_options(q["options"]))


def parse_letter(text: str | None, n_options: int) -> str | None:
    """Strict `ANSWER: <letter>`, the LAST occurrence; a letter outside the option range or no match is None (graded incorrect)."""
    m = ANSWER_RE.findall(text or "")
    if not m or LETTERS.index(m[-1]) >= n_options:
        return None
    return m[-1]


def grade(letter: str | None, key: str) -> bool:
    return letter is not None and letter == key


def majority(letters: list) -> str | None:
    """Majority vote over the letters of the drafts; ties go to the earliest draft; unparsable drafts do not vote."""
    votes = [l for l in letters if l]
    if not votes:
        return None
    counts = Counter(votes)
    top = max(counts.values())
    return next(l for l in votes if counts[l] == top)


def final_answer(position_letters: dict, specialist_letter: str | None, earliest: str | None = None) -> tuple:
    """T's final answer: the agreed final position; without agreement the specialist chooses among the EXISTING final positions. A specialist letter that is not one of them is rejected
    (the earliest position's letter stands). Returns (letter, how)."""
    existing = [l for l in position_letters.values() if l]
    if existing and len(set(existing)) == 1 and len(existing) == len(position_letters):
        return existing[0], "agreed"
    if specialist_letter is not None:
        if specialist_letter in existing:
            return specialist_letter, "specialist"
        return (earliest or (existing[0] if existing else None)), "specialist_new_letter_rejected"
    return (earliest or (existing[0] if existing else None)), "no_agreement_no_specialist"


def e_draft_count(t_record: dict) -> int:
    """E's k = the number of model calls T used on that question (CherryMe calls recorded by T)."""
    return int(t_record["calls"])


def sha(text: str) -> str:
    return hashlib.sha256((text or "").encode()).hexdigest()


def load_jsonl(path) -> list:
    return [json.loads(l) for l in open(path) if l.strip()]
