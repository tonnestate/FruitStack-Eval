"""Deterministic grader for inquiry tasks (protocol §5.5, gate G4: deterministic
verifiers for families 1 and 2), schema FSE-INQUIRY/1.

An inquiry task states a claim and asks for a verdict and one key value. Every arm must
end its answer with

    VERDICT: SUPPORTED | REFUTED
    KEY: <value>

The reference is a JSON object committed before the run:

    {"verdict": "REFUTED", "key_type": "date", "key": "1957-03-25",
     "accept": ["25 March 1957"], "tolerance": 0.0, "sources": ["https://..."]}

Grade (FSE-RUBRIC/1, INQUIRY scale): 1 if verdict and key are both correct, 0.5 if
exactly one is, 0 otherwise. The grader never sees which arm produced an answer, so
its grades are blinded by construction (provenance HARNESS_OBSERVED, blinded = true).
Missing or unparseable answers grade 0 and are counted separately; an abstention
(NOT_ENOUGH_INFO) also grades 0 and is counted as an abstention.
"""
from __future__ import annotations

import json
import math
import re
import unicodedata
from datetime import date, datetime

SCHEMA = "FSE-INQUIRY/1"
GRADER = "fse-inquiry/1"
VERDICTS = ("SUPPORTED", "REFUTED")
KEY_TYPES = ("integer", "number", "year", "date", "text")
FORMAT = ("End your answer with exactly these two lines:\n"
          "VERDICT: SUPPORTED or REFUTED\n"
          "KEY: <the value asked for>")
_SYNONYMS = {"SUPPORTED": "SUPPORTED", "SUPPORT": "SUPPORTED", "TRUE": "SUPPORTED", "CORRECT": "SUPPORTED",
             "CONFIRMED": "SUPPORTED", "REFUTED": "REFUTED", "REFUTE": "REFUTED", "FALSE": "REFUTED",
             "INCORRECT": "REFUTED", "WRONG": "REFUTED", "NOT_ENOUGH_INFO": "NOT_ENOUGH_INFO",
             "UNKNOWN": "NOT_ENOUGH_INFO", "UNVERIFIABLE": "NOT_ENOUGH_INFO", "CONFLICT": "NOT_ENOUGH_INFO"}
_MONTHS = {m: i for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july", "august",
                                       "september", "october", "november", "december"], start=1)}
_MONTHS.update({k[:3]: v for k, v in list(_MONTHS.items())})
_MONTHS.update({"januar": 1, "februar": 2, "märz": 3, "maerz": 3, "mai": 5, "juni": 6, "juli": 7, "oktober": 10,
                "dezember": 12})


def prompt(claim: str, question: str) -> str:
    return f"Claim: {claim}\nQuestion: {question}\n\n{FORMAT}"


def parse_reference(text: str) -> dict:
    ref = json.loads(text)
    if ref.get("verdict") not in VERDICTS:
        raise ValueError(f"reference verdict must be one of {VERDICTS}")
    if ref.get("key_type") not in KEY_TYPES:
        raise ValueError(f"reference key_type must be one of {KEY_TYPES}")
    if not isinstance(ref.get("key"), str) or not ref["key"].strip():
        raise ValueError("reference key must be a non-empty string")
    if _normalize_key(ref["key_type"], ref["key"]) is None:
        raise ValueError(f"reference key {ref['key']!r} is not a valid {ref['key_type']}")
    if not isinstance(ref.get("accept", []), list) or not isinstance(ref.get("sources", []), list):
        raise ValueError("accept and sources must be lists")
    if not ref.get("sources"):
        raise ValueError("a reference needs at least one source")
    tolerance = ref.get("tolerance", 0.0)
    if isinstance(tolerance, bool) or not isinstance(tolerance, (int, float)) or tolerance < 0:
        raise ValueError("tolerance must be a non-negative number")
    return ref


def _last(pattern: str, text: str) -> str | None:
    found = re.findall(pattern, text, flags=re.I | re.M)
    return found[-1].strip() if found else None


def parse_answer(output: str | None) -> dict:
    if not output or not output.strip():
        return {"status": "NO_ANSWER", "verdict": None, "key": None}
    text = output.replace("**", "").replace("__", "")
    raw_verdict = _last(r"^\W*VERDICT\s*[:=]\s*([A-Za-z_ ]+?)\W*$", text)
    raw_key = _last(r"^\W*KEY\s*[:=]\s*(.+?)\s*$", text)
    verdict = _SYNONYMS.get(re.sub(r"\s+", "_", raw_verdict.strip().upper())) if raw_verdict else None
    if verdict is None and raw_key is None:
        return {"status": "NO_STRUCTURED_ANSWER", "verdict": None, "key": None}
    return {"status": "PARSED", "verdict": verdict, "key": raw_key}


_FOLD = str.maketrans({"ł": "l", "Ł": "L", "ø": "o", "Ø": "O", "æ": "ae", "Æ": "AE", "œ": "oe", "Œ": "OE",
                       "ß": "ss", "đ": "d", "Đ": "D", "þ": "th", "Þ": "Th", "ı": "i"})


def _ascii(text: str) -> str:
    return unicodedata.normalize("NFKD", text.translate(_FOLD)).encode("ascii", "ignore").decode("ascii")


def _number(text: str) -> float | None:
    cleaned = text.strip().replace("−", "-").replace(" ", "").replace(" ", "")
    match = re.search(r"-?\d[\d,.' ]*", cleaned)
    if not match:
        return None
    token = match.group(0).strip().rstrip(".,")
    token = token.replace("'", "").replace(" ", "")
    if re.fullmatch(r"-?\d{1,3}(,\d{3})+(\.\d+)?", token):
        token = token.replace(",", "")
    elif re.fullmatch(r"-?\d{1,3}(\.\d{3})+(,\d+)?", token):
        token = token.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"-?\d+,\d+", token):
        token = token.replace(",", ".")
    try:
        value = float(token)
    except ValueError:
        return None
    scale = re.search(r"\b(thousand|million|billion|trillion|mio|mrd|bn|k)\b", cleaned.lower())
    if scale:
        value *= {"thousand": 1e3, "k": 1e3, "million": 1e6, "mio": 1e6, "billion": 1e9, "bn": 1e9, "mrd": 1e9,
                  "trillion": 1e12}[scale.group(1)]
    return value


def _date(text: str) -> str | None:
    t = _ascii(text).strip().lower().replace(",", " ")
    m = re.search(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b", t)
    if m:
        y, mo, d = map(int, m.groups())
    else:
        m = re.search(r"\b(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})\b", t)
        if m:
            d, mo, y = map(int, m.groups())
        else:
            m = re.search(r"\b(\d{1,2})(?:st|nd|rd|th)?\.?\s+([a-z]+)\.?\s+(\d{4})\b", t)
            if m and m.group(2) in _MONTHS:
                d, mo, y = int(m.group(1)), _MONTHS[m.group(2)], int(m.group(3))
            else:
                m = re.search(r"\b([a-z]+)\.?\s+(\d{1,2})(?:st|nd|rd|th)?\s+(\d{4})\b", t)
                if not (m and m.group(1) in _MONTHS):
                    return None
                mo, d, y = _MONTHS[m.group(1)], int(m.group(2)), int(m.group(3))
    try:
        return date(y, mo, d).isoformat()
    except ValueError:
        return None


def _text(text: str) -> str:
    words = re.sub(r"[^a-z0-9]+", " ", _ascii(text).casefold()).split()
    return " ".join(w for w in words if w not in {"the", "a", "an"})


def _normalize_key(key_type: str, value: str):
    if key_type == "integer":
        n = _number(value)
        return int(n) if n is not None and float(n).is_integer() else None
    if key_type == "number":
        return _number(value)
    if key_type == "year":
        m = re.search(r"\b(\d{3,4})\b", value)
        return int(m.group(1)) if m else None
    if key_type == "date":
        return _date(value)
    return _text(value) or None


def key_matches(ref: dict, given: str | None) -> bool:
    if given is None:
        return False
    kind = ref["key_type"]
    value = _normalize_key(kind, given)
    if value is None:
        return False
    targets = [ref["key"], *ref.get("accept", [])]
    for target in targets:
        expected = _normalize_key(kind, target)
        if expected is None:
            continue
        if kind == "number":
            tol = float(ref.get("tolerance", 0.0))
            if math.isclose(value, expected, rel_tol=tol, abs_tol=0.0 if tol else 1e-9):
                return True
        elif value == expected:
            return True
    return False


def grade(reference_text: str, output: str | None) -> dict:
    ref = parse_reference(reference_text)
    parsed = parse_answer(output)
    verdict_ok = parsed["verdict"] == ref["verdict"]
    key_ok = key_matches(ref, parsed["key"])
    value = 1.0 if verdict_ok and key_ok else 0.5 if (verdict_ok or key_ok) else 0.0
    return {"grade": value, "status": parsed["status"], "verdict_given": parsed["verdict"],
            "key_given": parsed["key"], "verdict_ok": verdict_ok, "key_ok": key_ok,
            "abstained": parsed["verdict"] == "NOT_ENOUGH_INFO", "grader": GRADER}


def evidence(reference_text: str, output: str | None) -> dict:
    """Evidence object for `fse compare` (rubric FSE-RUBRIC/1, family INQUIRY)."""
    g = grade(reference_text, output)
    return {"provenance": "HARNESS_OBSERVED", "blinded": True, "grade": g["grade"], "grader": GRADER,
            "parse_status": g["status"], "verdict_ok": g["verdict_ok"], "key_ok": g["key_ok"],
            "abstained": g["abstained"], "graded_at": datetime.now().astimezone().replace(microsecond=0).isoformat()}
