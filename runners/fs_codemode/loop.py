"""Brother Mode closed loop: verified contributions -> competence / cooperation weights -> EVC-chosen next action -> explicit closing rule where evidence outranks weights.
CherryMe's Brother Mode (cherryme.brother.run_rounds(control=...)) calls observe / decide / close; with no control it behaves as before (AlwaysCritique baseline).
Everything here is deterministic. Defaults are fixed constants (LoopParams) and are written to a dated parameter file before any study; they are NOT calibrated on data.
Invariants (link 3): weights never override a verified objection and never suppress one; a concession to a formal (non-executed) objection is recorded as CONCEDED_TO_FORMAL."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable, Dict, List, Optional

CRITIQUE, FINISH, REPLY, SPECIALIST = "CRITIQUE", "FINISH", "REPLY", "SPECIALIST"
LEVELS = ("verified", "formal", "none", "failed")


@dataclass(frozen=True)
class LoopParams:
    prior_competence: float = 0.5
    prior_cooperation: float = 0.5
    step_verified: float = 0.10          # weight raise for a verified contribution
    step_formal: float = 0.03            # smaller raise for a formal one; none / failed never raise
    max_weight: float = 0.95
    lam_c_per_1k_tokens: float = 0.001
    lam_t_per_second: float = 0.0005
    lam_r: float = 0.0                   # harm is already inside the expected utility change: no double counting
    extra_tokens: float = 10000.0        # a-priori planning constants for one more exchange (not fitted)
    extra_seconds: float = 40.0
    formal_concession_rate: float = 0.10  # chance that a formal-only exchange makes the better position concede wrongly
    detect_if_both_wrong: float = 0.5    # chance an exchange exposes an error of two agreeing members


def clamp(x: float, p: LoopParams) -> float:
    return max(0.0, min(p.max_weight, round(x, 6)))


class WeightBook:
    """Competence per model and cooperation per pair. Update table: verified +step_verified, formal +step_formal, none / failed +0. Bounded, deterministic, logged."""

    def __init__(self, params: LoopParams = LoopParams(), log: Optional[Callable[[dict], None]] = None):
        self.p, self.log = params, log or (lambda r: None)
        self.competence: Dict[str, float] = {}
        self.cooperation: Dict[frozenset, float] = {}

    def comp(self, m: str) -> float:
        return self.competence.get(m, self.p.prior_competence)

    def coop(self, a: str, b: str) -> float:
        return self.cooperation.get(frozenset((a, b)), self.p.prior_cooperation)

    def step(self, level: str) -> float:
        return {"verified": self.p.step_verified, "formal": self.p.step_formal}.get(level, 0.0)

    def update(self, critic: str, target: str, level: str) -> dict:
        s = self.step(level)
        before = {"competence": self.comp(critic), "cooperation": self.coop(critic, target)}
        if s:
            self.competence[critic] = clamp(before["competence"] + s, self.p)
            self.cooperation[frozenset((critic, target))] = clamp(before["cooperation"] + s, self.p)
        rec = {"type": "WEIGHT_UPDATE", "critic": critic, "target": target, "level": level, "step": s, "before": before,
               "after": {"competence": self.comp(critic), "cooperation": self.coop(critic, target)}}
        self.log(rec)
        return rec


def p_hi_correct(c_hi: float, c_lo: float) -> float:
    """P(the higher-competence member is the correct one | exactly one of the two is correct), independence assumed."""
    num, den = c_hi * (1 - c_lo), c_hi * (1 - c_lo) + c_lo * (1 - c_hi)
    return num / den if den > 0 else 0.5


class CooperationControl:
    """The control object Brother Mode calls. `models` order breaks ties (first model = the baseline's first author)."""

    def __init__(self, params: LoopParams = LoopParams(), log: Optional[Callable[[dict], None]] = None, models: tuple = ()):
        self.p, self.log, self.models = params, log or (lambda r: None), tuple(models)
        self.book = WeightBook(params, self.log)
        self.events: List[dict] = []
        self.concessions: List[dict] = []

    # ---- link 1: observe -> weights -----------------------------------------------------------------------------------------------------------------------
    def observe(self, event: dict) -> None:
        self.events.append(event)
        if event.get("kind") == "CRITIQUE" and event.get("hit") and event.get("critic") and event.get("target"):
            self.book.update(event["critic"], event["target"], event.get("verification") or "none")
        if event.get("kind") == "REVISION" and event.get("changed") and "formal" in (event.get("levels") or []) and "verified" not in (event.get("levels") or []):
            rec = {"type": "CONCEDED_TO_FORMAL", "author": event["author"], "before": event.get("before"), "after": event.get("after"), "critics": event.get("critics")}
            self.concessions.append(rec)
            self.log(rec)

    # ---- link 2: weights -> EVC -> next action ----------------------------------------------------------------------------------------------------------
    def _cost(self) -> float:
        return self.p.lam_c_per_1k_tokens * self.p.extra_tokens / 1000.0 + self.p.lam_t_per_second * self.p.extra_seconds

    def _exchange_gain(self, w: float, a: float) -> float:
        """Expected utility change of one more exchange: with probability w the better-evidenced side prevails (the correct one: 1 - a), and with probability (1-w) a formal-only
        exchange can make the better side concede wrongly (formal_concession_rate); a = P(current closing side correct | disagreement)."""
        return w * (1 - a) - (1 - w) * self.p.formal_concession_rate * a

    def evc(self, state: dict) -> dict:
        sig = state.get("signatures") or {}
        models = [m for m in (state.get("models") or list(sig)) if m in sig]
        cost = self._cost()
        scores = {FINISH: 0.0}
        if len(models) >= 2 and state.get("disagree"):
            hi, lo = sorted(models, key=lambda m: (-self.book.comp(m), self.models.index(m) if m in self.models else 99))[:2]
            a = p_hi_correct(self.book.comp(hi), self.book.comp(lo))
            w = self.book.coop(hi, lo)
            scores[CRITIQUE] = self._exchange_gain(w, a) - cost
            scores[SPECIALIST] = self._exchange_gain(self.p.prior_competence, a) - cost
        elif len(models) >= 2:
            c1, c2 = (self.book.comp(m) for m in models[:2])
            both_wrong = (1 - c1) * (1 - c2) / ((1 - c1) * (1 - c2) + c1 * c2)
            scores[CRITIQUE] = self.book.coop(models[0], models[1]) * both_wrong * self.p.detect_if_both_wrong - cost
        return {"scores": {k: round(v, 6) for k, v in scores.items()}, "cost": round(cost, 6)}

    def decide(self, state: dict) -> str:
        point, options = state["point"], tuple(state.get("options") or ())
        levels = list(state.get("verifications") or [])
        if point == "REPLY_OR_FINISH":
            if "verified" in levels:                       # link 3: evidence over weights; a low weight can never suppress a verified objection
                choice, why, scores = REPLY, "VERIFIED_OBJECTION_ALWAYS_ANSWERED", {}
            else:
                author, critic_ids = state.get("author"), [m for m in (state.get("models") or []) if m != state.get("author")]
                p_right = 0.0 if not levels or all(l in ("none", "failed") for l in levels) else self.book.comp(critic_ids[0]) if critic_ids else self.p.prior_competence
                w = self.book.coop(author, critic_ids[0]) if critic_ids else self.p.prior_cooperation
                gain = w * p_right - (1 - w) * self.p.formal_concession_rate * (1 - p_right) - self._cost()
                scores = {REPLY: round(gain, 6), FINISH: 0.0}
                choice, why = (REPLY if gain > 0 else FINISH), "EVC"
        else:
            ev = self.evc(state)
            scores = ev["scores"]
            target = {"CRITIQUE_OR_FINISH": CRITIQUE, "SPECIALIST_OR_FINISH": SPECIALIST}.get(point, FINISH)
            choice, why = (target if scores.get(target, -1.0) > 0 else FINISH), "EVC"
        if choice not in options:
            choice = options[0] if options else FINISH
        self.log({"type": "ACTION", "consolidation": consolidation_view(self.book, state.get("signatures") or {}, self.events), "point": point, "state": {k: state.get(k) for k in ("round", "calls", "signatures", "disagree", "author", "verifications")},
                  "weights": {"competence": dict(self.book.competence), "cooperation": {"|".join(sorted(k)): v for k, v in self.book.cooperation.items()}}, "scores": scores, "choice": choice, "why": why})
        return choice

    # ---- link 3: explicit closing rule, evidence over weights ------------------------------------------------------------------------------------------
    def close(self, state: dict) -> dict:
        sig, first = state.get("signatures") or {}, state.get("first") or {}
        order = [m for m in (self.models or tuple(sig)) if m in sig] + [m for m in sig if m not in self.models]
        verified = [e for e in self.events if e.get("kind") == "CRITIQUE" and e.get("hit") and e.get("verification") == "verified" and e.get("critic") in sig and e.get("target") in sig]
        rule, final, detail = None, None, {}
        distinct_now = len(set(sig.values())) > 1
        if verified and distinct_now:
            last = verified[-1]                            # the last verified objection decides; weights are not consulted
            rule, final, detail = "VERIFIED_LAST_OBJECTION", last["critic"], {"objection": last.get("row"), "target": last["target"]}
        else:
            cands = [(m, sig[m], "current") for m in order]
            if not verified:
                for c in self.concessions:                  # a conceder's first answer stays a candidate: a formal concession alone does not discard it
                    m = c["author"]
                    if m in first and first[m] not in {x[1] for x in cands if x[0] == m}:
                        cands.append((m, first[m], "first_answer_kept_after_CONCEDED_TO_FORMAL"))
            if len({x[1] for x in cands}) <= 1:
                rule, final = "CONSENSUS", order[0] if order else None
            else:
                best = max(cands, key=lambda x: (self.book.comp(x[0]), -order.index(x[0]) if x[0] in order else -99))
                rule, final = ("FORMAL_CONCESSION_KEEPS_FIRST_ANSWER_CANDIDATE" if self.concessions else "WEIGHTS_DECIDE_UNVERIFIED"), best[0]
                detail = {"candidates": [{"model": m, "answer": s, "source": src, "competence": self.book.comp(m)} for m, s, src in cands], "chosen_answer": best[1]}
        answer = detail.get("chosen_answer", sig.get(final))
        rec = {"type": "CLOSING", "rule": rule, "final_model": final, "final_answer": answer, "detail": detail, "signatures": sig, "first": first,
               "concessions": list(self.concessions), "verified_objections": len(verified), "weights_consulted": rule not in ("CONSENSUS", "VERIFIED_LAST_OBJECTION")}
        self.log(rec)
        return rec


def consolidation_view(book: WeightBook, signatures: dict, events: list) -> Optional[dict]:
    """The existing CherryMe consolidation (cherryme.responsibility.consolidate) over the duo: one responsibility per member, leans from the recorded verified objections, weights =
    competence. It records, never decides (truth_authority False); here it supplies the logged inputs agreement / weighted lean / uncertainty. None when CherryMe is not importable."""
    try:
        from cherryme import responsibility as resp
    except Exception:  # noqa: BLE001
        return None
    ids = {m: f"M{i}" for i, m in enumerate(signatures)}
    nodes = [resp.make_node(id=ids[m], mandate=f"position of {i}"[:200], function="CHALLENGE") for i, m in enumerate(signatures)]
    against = {e["target"] for e in events if e.get("kind") == "CRITIQUE" and e.get("hit") and e.get("verification") == "verified"}
    delivered = {ids[m]: [{"id": f"E_{ids[m]}", "verdict": "CONTRADICT" if m in against else "PASS", "family": m, "worker_id": m, "source_ref": "brother", "host_verified": m in against,
                           "model_key": m, "summary": ""}] for m in signatures}
    out = resp.consolidate(nodes, delivered, {ids[m]: book.comp(m) for m in signatures})
    return {k: out[k] for k in ("agreement", "weighted_lean", "uncertainty", "independent_voices", "dissent")}


def params_record(p: LoopParams = LoopParams()) -> dict:
    return {"name": "Brother Mode closed loop defaults", "calibrated": False, "note": "fixed a-priori constants; not fitted on any data, including the four QA-2D disagreement rows", "params": asdict(p)}
