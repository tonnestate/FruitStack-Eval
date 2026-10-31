"""Invariant-preserving compaction and per-message keep / compact / drop (training-free; the idea of MessageSieve, EMNLP 2026, built from existing parts).

Invariants (CogC rule): exact values, identifiers, option letters and references must survive. If a compact form loses any of them, the full text is
used instead (fail safe). A message whose claim and result duplicate one already delivered to the same receiver is dropped."""
from __future__ import annotations

import hashlib
import re
from typing import Dict, Iterable, List, Set, Tuple

_NUMBER = re.compile(r"(?<![A-Za-z])[-+]?\d+(?:[.,]\d+)?(?:e[-+]?\d+)?", re.I)
_IDENT = re.compile(r"\b(?:O|S|Q)\d+\b|\b[A-Za-z_][A-Za-z0-9_]*\([^)]{0,40}\)")
_OPTION = re.compile(r"\b(?:option|answer|choice)\s*\(?([A-J])\)?\b|\(([A-J])\)|ANSWER:\s*\(?([A-J])\)?", re.I)
_SENT = re.compile(r"(?<=[.!?])\s+|\n+")
_BOILER = re.compile(r"^(?:let me|i will|i'll|okay|ok|sure|first,? let|to solve this|we need to|let's)\b", re.I)


def invariants(text: str) -> Set[str]:
    inv: Set[str] = set()
    inv.update(m.group(0).replace(",", ".") for m in _NUMBER.finditer(text or ""))
    inv.update(m.group(0) for m in _IDENT.finditer(text or ""))
    for m in _OPTION.finditer(text or ""):
        inv.add("opt:" + next(g for g in m.groups() if g).upper())
    return inv


def missing_invariants(full: str, compact: str) -> Set[str]:
    return invariants(full) - invariants(compact)


def compact(text: str, max_chars: int = 1200) -> Tuple[str, bool]:
    """(text_to_send, compacted). Keeps sentences that carry an invariant, drops boilerplate; falls back to the full text if any invariant would be lost
    or the result is not shorter."""
    text = text or ""
    if len(text) <= max_chars:
        return text, False
    sentences = [s.strip() for s in _SENT.split(text) if s and s.strip()]
    kept = [s for s in sentences if invariants(s) and not _BOILER.match(s)]
    candidate = "\n".join(kept)
    if not candidate or len(candidate) >= len(text) or missing_invariants(text, candidate):
        return text, False
    return candidate, True


def sieve(messages: Iterable[dict], delivered: Dict[str, Set[str]], receiver: str, max_chars: int = 1200) -> List[dict]:
    """messages: [{"id", "claim", "result", "text"}]. Returns [{"id", "action": keep|compact|drop, "text"}] for `receiver`.
    `delivered[receiver]` holds signatures already sent to that receiver and is updated."""
    seen = delivered.setdefault(receiver, set())
    out = []
    for m in messages:
        claim = (m.get("claim") or "").strip().lower()
        # with a labelled claim, the same claim + answer is redundant; without one, only an exact repeat of the text is
        sig = f"claim:{claim}|{m.get('result')}" if claim else "text:" + hashlib.sha256((m.get("text") or "").encode()).hexdigest()
        if sig in seen:
            out.append({"id": m.get("id"), "action": "drop", "text": ""})
            continue
        seen.add(sig)
        body, did = compact(m.get("text") or "", max_chars)
        out.append({"id": m.get("id"), "action": "compact" if did else "keep", "text": body})
    return out
