"""Typed message contract. A message carries only what the next step needs; the full model output stays outside the model context and is
referenced by its sha256 (`full_ref`). A structured message never raises trust: `verification` is set only by the host verifier."""
from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field
from typing import Callable, Dict, List, Optional

KINDS = ("ANSWER", "OBJECTION", "REPLY", "VERDICT")
VERIFICATION = ("none", "formal", "reproduced", "independently_confirmed", "failed")
_LABEL = re.compile(r"^[ \t>*_#-]*(CLAIM|EVIDENCE|CONSEQUENCE)[ \t*_]*[:\-][ \t*_]*", re.I | re.M)
ANSWER_RE = re.compile(r"ANSWER:\s*\(?([A-J])\)?")
LETTERS = "ABCDEFGHIJ"


def sha(text: Optional[str]) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def parse_parts(text: str) -> Dict[str, str]:
    """Labelled CLAIM / EVIDENCE / CONSEQUENCE parts (same grammar as ogi013_argument.parse_parts)."""
    marks = list(_LABEL.finditer(text or ""))
    parts: Dict[str, str] = {}
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        parts.setdefault(m.group(1).upper(), text[m.end():end].strip())
    return parts


def parse_letter(text: Optional[str], n_options: int) -> Optional[str]:
    """Strict `ANSWER: <letter>`, LAST occurrence, inside the option range (same rule as ogi013_qa1.parse_letter)."""
    m = ANSWER_RE.findall(text or "")
    if not m or LETTERS.index(m[-1]) >= n_options:
        return None
    return m[-1]


@dataclass
class Resources:
    calls: int = 0
    tokens: int = 0
    seconds: float = 0.0

    def add(self, other: "Resources") -> "Resources":
        return Resources(self.calls + other.calls, self.tokens + other.tokens, round(self.seconds + other.seconds, 3))


@dataclass
class Msg:
    kind: str
    member: str
    lineage: str
    result: Optional[str] = None
    claim: str = ""
    evidence: str = ""
    consequence: str = ""
    target: Optional[str] = None
    refs: List[str] = field(default_factory=list)
    verification: str = "none"
    uncertainty: Optional[dict] = None
    resources: Resources = field(default_factory=Resources)
    next_action: Optional[str] = None
    full_ref: str = ""
    id: str = ""

    def __post_init__(self):
        if self.kind not in KINDS:
            raise ValueError(f"unknown kind {self.kind!r}")
        if self.verification not in VERIFICATION:
            raise ValueError(f"unknown verification {self.verification!r}")
        if self.uncertainty is not None:
            src = self.uncertainty.get("source") if isinstance(self.uncertainty, dict) else None
            if not src or src == "simulated" or "value" not in self.uncertainty:
                raise ValueError("uncertainty must be a measured value with its source (never simulated)")

    @classmethod
    def from_output(cls, kind: str, member: str, lineage: str, text: str, n_options: int, *, target: Optional[str] = None,
                    resources: Optional[Resources] = None, msg_id: str = "") -> "Msg":
        parts = parse_parts(text)
        return cls(kind=kind, member=member, lineage=lineage, result=parse_letter(text, n_options), claim=parts.get("CLAIM", ""),
                   evidence=parts.get("EVIDENCE", ""), consequence=parts.get("CONSEQUENCE", ""), target=target, full_ref=sha(text),
                   resources=resources or Resources(), id=msg_id)

    def to_dict(self) -> dict:
        return asdict(self)

    def render(self, body: Optional[str] = None) -> str:
        """The compact text a model receives. `body` is the (possibly compacted) reasoning when the message has no labelled parts."""
        head = f"[{self.kind} {self.id or ''} by {self.member}{' on ' + self.target if self.target else ''}]".replace("  ", " ")
        lines = [head]
        if self.claim or self.evidence or self.consequence:
            lines += [f"CLAIM: {self.claim}", f"EVIDENCE: {self.evidence}", f"CONSEQUENCE: {self.consequence}"]
        elif body:
            lines.append(body)
        lines.append(f"VERIFICATION (host): {self.verification}")
        if self.result:
            lines.append(f"ANSWER: {self.result}")
        return "\n".join(lines)


def verification_level(classified: dict) -> str:
    """Map an ogi013_argument.classify_argument result to the contract's verification field."""
    kind = (classified or {}).get("kind")
    if kind == "independently_confirmed":
        checks = (classified or {}).get("checks") or classified or {}
        return ("independently_confirmed" if checks.get("relevance_assessed") is True
                and checks.get("independent_confirmation") is True else "none")
    if kind in ("verified", "reproduced"):
        return "reproduced"
    if kind == "formal":
        return "formal"
    if (classified or {}).get("argument", {}).get("executed"):
        return "failed"
    return "none"


Verifier = Callable[[str], dict]
