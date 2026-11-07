"""Brother Mode closed loop: independently confirmed contributions -> competence / cooperation weights -> EVC-chosen next action -> explicit closing rule where evidence outranks weights.
CherryMe's Brother Mode (cherryme.brother.run_rounds(control=...)) calls observe / decide / close; with no control it behaves as before (AlwaysCritique baseline).
Everything here is deterministic. Defaults are fixed constants (LoopParams) and are written to a dated parameter file before any study; they are NOT calibrated on data.
Invariants: weights never override or suppress an independently confirmed objection; formal concessions remain separate and unverified."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Callable, Dict, List, Optional

CRITIQUE, FINISH, REPLY, SPECIALIST = "CRITIQUE", "FINISH", "REPLY", "SPECIALIST"
LEVELS = ("independently_confirmed", "reproduced", "formal", "none", "failed")


@dataclass(frozen=True)
class LoopParams:
    prior_competence: float = 0.5
    prior_cooperation: float = 0.5
    step_verified: float = 0.10          # heuristic weight raise for an independently confirmed contribution
    step_formal: float = 0.03            # retained for the documented heuristic baseline; not used for learning
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


def independently_confirmed(evidence: dict) -> bool:
    return (isinstance(evidence, dict)
            and evidence.get("verification") == "independently_confirmed"
            and evidence.get("relevance_assessed") is True
            and evidence.get("independent_confirmation") is True)


def _member(key) -> str:
    """The member behind a signature key: CherryMe suffixes a second sample of the SAME model key with '#<n>'; such a sample is the same member (same lineage), never an independent one."""
    return re.sub(r"#\d+$", "", str(key))


class WeightBook:
    """Uncalibrated heuristic competence and pair weights; only independent confirmation can raise them."""

    def __init__(self, params: LoopParams = LoopParams(), log: Optional[Callable[[dict], None]] = None):
        self.p, self.log = params, log or (lambda r: None)
        self.competence: Dict[str, float] = {}
        self.cooperation: Dict[frozenset, float] = {}
        self.seen_contributions: set[str] = set()

    def comp(self, m: str) -> float:
        return self.competence.get(m, self.p.prior_competence)

    def coop(self, a: str, b: str) -> float:
        return self.cooperation.get(frozenset((a, b)), self.p.prior_cooperation)

    def step(self, level: str, relevance_assessed: bool = False, independent_confirmation: bool = False) -> float:
        # Technical reproduction and formal completeness do not establish truth or contribution quality.
        return self.p.step_verified if level == "independently_confirmed" and relevance_assessed and independent_confirmation else 0.0

    def update(self, critic: str, target: str, level: str, *, relevance_assessed: bool = False, independent_confirmation: bool = False, contribution_id: str | None = None) -> dict:
        s = self.step(level, relevance_assessed, independent_confirmation)
        if s and contribution_id and contribution_id in self.seen_contributions:
            rec = {"type": "WEIGHT_UPDATE", "critic": critic, "target": target, "level": level, "step": 0.0,
                   "duplicate": True, "contribution_id": contribution_id,
                   "after": {"competence": self.comp(critic), "cooperation": self.coop(critic, target)}}
            self.log(rec)
            return rec
        if s and contribution_id:
            self.seen_contributions.add(contribution_id)
        before = {"competence": self.comp(critic), "cooperation": self.coop(critic, target)}
        if s:
            self.competence[critic] = clamp(before["competence"] + s, self.p)
            self.cooperation[frozenset((critic, target))] = clamp(before["cooperation"] + s, self.p)
        rec = {"type": "WEIGHT_UPDATE", "critic": critic, "target": target, "level": level, "relevance_assessed": relevance_assessed,
               "independent_confirmation": independent_confirmation, "contribution_id": contribution_id, "step": s, "before": before,
               "after": {"competence": self.comp(critic), "cooperation": self.coop(critic, target)}}
        self.log(rec)
        return rec


def p_hi_correct(c_hi: float, c_lo: float) -> float:
    """P(the higher-competence member is the correct one | exactly one of the two is correct), independence assumed."""
    num, den = c_hi * (1 - c_lo), c_hi * (1 - c_lo) + c_lo * (1 - c_hi)
    return num / den if den > 0 else 0.5


class CooperationControl:
    """The control object Brother Mode calls. `models` order breaks ties (first model = the baseline's first author)."""

    def __init__(self, params: LoopParams = LoopParams(), log: Optional[Callable[[dict], None]] = None, models: tuple = (), reviewer_history: Optional[dict] = None):
        self.p, self.log, self.models = params, log or (lambda r: None), tuple(models)
        self.book = WeightBook(params, self.log)
        self.reviewer_history = reviewer_history or {}
        self.events: List[dict] = []
        self.concessions: List[dict] = []
        self.primary_first: Optional[Callable[[], Optional[str]]] = None          # optional: the designated primary's first answer (solver1's), not the first-finished sample

    # ---- link 1: observe -> weights -----------------------------------------------------------------------------------------------------------------------
    def observe(self, event: dict) -> None:
        self.events.append(event)
        self.log({"type": "EVIDENCE_OBSERVED", **event})
        if (event.get("kind") == "CRITIQUE" and event.get("hit") and event.get("critic") and event.get("target")
                and _member(event["critic"]) != _member(event["target"])):                  # a critique between two samples of one model cannot move any weight
            self.book.update(event["critic"], event["target"], event.get("verification") or "none",
                             relevance_assessed=event.get("relevance_assessed") is True,
                             independent_confirmation=event.get("independent_confirmation") is True,
                             contribution_id=event.get("row"))
        levels = event.get("levels") or []
        if (event.get("kind") == "REVISION" and event.get("answer_changed") is True
                and any(x == "formal" or isinstance(x, dict) and x.get("verification") == "formal" for x in levels)
                and not any(isinstance(x, dict) and independently_confirmed(x) for x in levels)):
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
        history = []
        if len(models) >= 2 and state.get("disagree"):
            hi, lo = sorted(models, key=lambda m: (-self.book.comp(m), self.models.index(m) if m in self.models else 99))[:2]
            a = p_hi_correct(self.book.comp(hi), self.book.comp(lo))
            w = self.book.coop(hi, lo)
            gain = self._exchange_gain(w, a)
            observed = [self.reviewer_history.get((reviewer, proposer)) for reviewer, proposer in ((hi, lo), (lo, hi))]
            observed = [x for x in observed if x and x["n"]]
            if observed:
                n = sum(x["n"] for x in observed)
                improved = sum(x["improved"] for x in observed)
                # Beta(1,1) shrinkage over independently verified, task-matched PlumMe review outcomes.
                quality = (improved + 1) / (n + 2)
                gain *= quality / 0.5
                history = [{"n": x["n"], "improved": x["improved"], "task_class": x["task_class"]} for x in observed]
            scores[CRITIQUE] = gain - cost
            scores[SPECIALIST] = self._exchange_gain(self.p.prior_competence, a) - cost
        elif len(models) >= 2:
            c1, c2 = (self.book.comp(m) for m in models[:2])
            both_wrong = (1 - c1) * (1 - c2) / ((1 - c1) * (1 - c2) + c1 * c2)
            scores[CRITIQUE] = self.book.coop(models[0], models[1]) * both_wrong * self.p.detect_if_both_wrong - cost
        return {"scores": {k: round(v, 6) for k, v in scores.items()}, "cost": round(cost, 6), "cost_basis": "A_PRIORI_ESTIMATE", "review_history": history, "calibrated": False}

    def decide(self, state: dict) -> str:
        point, options = state["point"], tuple(state.get("options") or ())
        evidence = list(state.get("verifications") or [])
        levels = [x for x in evidence if isinstance(x, dict) and independently_confirmed(x)]
        review_history = []
        if point == "REPLY_OR_FINISH":
            if levels:                                       # weights cannot suppress an independently confirmed objection
                choice, why, scores = REPLY, "CONFIRMED_OBJECTION_ALWAYS_ANSWERED", {}
            else:
                author = state.get("author")
                critic_ids = [m for m in (state.get("critic_models") or state.get("models") or []) if m and m != author]
                labels = [x.get("verification") if isinstance(x, dict) else x for x in evidence]
                p_right = 0.0 if not labels or all(l in ("none", "failed") for l in labels) else self.book.comp(critic_ids[0]) if critic_ids else self.p.prior_competence
                w = self.book.coop(author, critic_ids[0]) if critic_ids else self.p.prior_cooperation
                gain = w * p_right - (1 - w) * self.p.formal_concession_rate * (1 - p_right)
                history = self.reviewer_history.get((critic_ids[0], author)) if critic_ids else None
                if history and history["n"]:
                    quality = (history["improved"] + 1) / (history["n"] + 2)
                    gain *= quality / 0.5
                    review_history = [{"n": history["n"], "improved": history["improved"], "task_class": history["task_class"]}]
                gain -= self._cost()
                scores = {REPLY: round(gain, 6), FINISH: 0.0}
                choice, why = (REPLY if gain > 0 else FINISH), "EVC"
        else:
            ev = self.evc(state)
            scores = ev["scores"]
            review_history = ev["review_history"]
            target = {"CRITIQUE_OR_FINISH": CRITIQUE, "SPECIALIST_OR_FINISH": SPECIALIST}.get(point, FINISH)
            choice, why = (target if scores.get(target, -1.0) > 0 else FINISH), "EVC"
        if choice not in options:
            choice = options[0] if options else FINISH
        self.log({"type": "ACTION", "calibrated": False, "cost_basis": "A_PRIORI_ESTIMATE", "consolidation": consolidation_view(self.book, state.get("signatures") or {}, self.events), "point": point, "state": {k: state.get(k) for k in ("round", "calls", "signatures", "disagree", "author", "verifications")},
                  "weights": {"competence": dict(self.book.competence), "cooperation": {"|".join(sorted(k)): v for k, v in self.book.cooperation.items()}}, "review_history": review_history, "scores": scores, "choice": choice, "why": why})
        return choice

    # ---- link 3: explicit closing rule, evidence over weights ------------------------------------------------------------------------------------------
    def close(self, state: dict) -> dict:
        sig_all, first_all = state.get("signatures") or {}, state.get("first") or {}
        reg = [k for k in (state.get("models") or []) if k in sig_all] + [k for k in sig_all if k not in (state.get("models") or [])]
        canon: dict = {}
        for k in reg:
            canon.setdefault(_member(k), k)                   # one member = one lineage; its canonical sample is the first registered
        sig = {m: sig_all[k] for m, k in canon.items()}
        first = {m: first_all[k] for m, k in canon.items() if first_all.get(k) is not None}
        order = [m for m in self.models if m in sig] + [m for m in sig if m not in self.models]
        primary = order[0] if order else None
        pf = self.primary_first() if callable(self.primary_first) else None
        if primary is not None and pf:
            first[primary] = pf                               # the designated initial answer, not whichever sample finished first
        extra = [{"member": _member(k), "sample": k, "answer": sig_all[k], "status": "same_lineage_sample_not_evidence"} for k in reg if k not in canon.values()]
        independent = len(order) >= 2                         # same-lineage duplication is never independent collaboration
        confirmed = [e for e in self.events if e.get("kind") == "CRITIQUE" and e.get("hit") and independently_confirmed(e)
                     and _member(e.get("critic")) in sig and _member(e.get("target")) in sig and _member(e.get("critic")) != _member(e.get("target"))]
        rule, final, detail = None, None, {}
        distinct_now = len(set(sig.values())) > 1
        if not independent and len(reg) >= 2:                # several samples of ONE lineage (a single executed candidate passed through by a caller is not duplication)
            rule, final = "SAME_LINEAGE_NO_INDEPENDENCE", primary
            detail = {"chosen_answer": first.get(primary, sig.get(primary)), "samples": [{"sample": k, "answer": sig_all[k]} for k in reg]}
        elif confirmed and distinct_now:
            last = confirmed[-1]                            # weights cannot overrule an independently confirmed objection; this is how a justified change of the first answer happens
            rule, final, detail = "INDEPENDENTLY_CONFIRMED_LAST_OBJECTION", _member(last["critic"]), {"objection": last.get("row"), "target": last["target"]}
        else:
            cands = [(m, sig[m], "current") for m in order]
            if not confirmed:
                for c in self.concessions:                  # a conceder's first answer stays a candidate: a formal concession alone does not discard it
                    m = _member(c["author"])
                    if m in first and first[m] not in {x[1] for x in cands if x[0] == m}:
                        cands.append((m, first[m], "first_answer_kept_after_CONCEDED_TO_FORMAL"))
            if len({x[1] for x in cands}) <= 1:
                rule, final = "CONSENSUS", order[0] if order else None
            else:
                best = max(cands, key=lambda x: (self.book.comp(x[0]), -order.index(x[0]) if x[0] in order else -99))
                if self.concessions:
                    rule = "FORMAL_CONCESSION_KEEPS_FIRST_ANSWER_CANDIDATE"
                elif self.book.comp(best[0]) - self.book.comp(primary) < self.p.step_verified:   # weights without evidence worth one verified update never override the initial answer
                    best, rule = (primary, first.get(primary, sig[primary]), "primary_initial"), "UNRESOLVED_PRIMARY_RETAINED"
                else:
                    rule = "WEIGHTS_DECIDE_UNVERIFIED"
                final = best[0]
                detail = {"candidates": [{"model": m, "answer": s_, "source": src, "competence": self.book.comp(m)} for m, s_, src in cands], "chosen_answer": best[1]}
        answer = detail.get("chosen_answer", sig.get(final))
        provisional = rule not in ("INDEPENDENTLY_CONFIRMED_LAST_OBJECTION", "CONSENSUS")
        disagreement = (detail.get("candidates", []) if rule not in ("SAME_LINEAGE_NO_INDEPENDENCE", "INDEPENDENTLY_CONFIRMED_LAST_OBJECTION", "CONSENSUS") else []) + extra
        if rule == "SAME_LINEAGE_NO_INDEPENDENCE" and len({x["answer"] for x in detail["samples"]}) > 1:
            disagreement = [{"model": x["sample"], "answer": x["answer"], "source": "same_lineage_sample_not_evidence"} for x in detail["samples"]]
        rec = {"type": "CLOSING", "rule": rule, "final_model": final, "final_answer": answer, "detail": detail, "signatures": sig_all, "first": first_all,
               "concessions": list(self.concessions), "independently_confirmed_objections": len(confirmed), "weights_consulted": rule not in ("INDEPENDENTLY_CONFIRMED_LAST_OBJECTION", "SAME_LINEAGE_NO_INDEPENDENCE", "UNRESOLVED_PRIMARY_RETAINED"),
               "independent_collaboration": independent, "provisional": provisional, "verified_improvement": rule == "INDEPENDENTLY_CONFIRMED_LAST_OBJECTION",
               "unresolved_disagreement": disagreement if provisional else []}
        self.log(rec)
        return rec


def consolidation_view(book: WeightBook, signatures: dict, events: list) -> Optional[dict]:
    """The existing CherryMe consolidation (cherryme.responsibility.consolidate) over the duo: one responsibility per member, leans from recorded independently confirmed objections, weights =
    competence. It records, never decides (truth_authority False); here it supplies the logged inputs agreement / weighted lean / uncertainty. None when CherryMe is not importable."""
    try:
        from cherryme import responsibility as resp
    except Exception:  # noqa: BLE001
        return None
    ids = {m: f"M{i}" for i, m in enumerate(signatures)}
    nodes = [resp.make_node(id=ids[m], mandate=f"position of {i}"[:200], function="CHALLENGE") for i, m in enumerate(signatures)]
    against = {e["target"] for e in events if e.get("kind") == "CRITIQUE" and e.get("hit") and independently_confirmed(e)}
    delivered = {ids[m]: [{"id": f"E_{ids[m]}", "verdict": "CONTRADICT" if m in against else "PASS", "family": m, "worker_id": m, "source_ref": "brother", "host_verified": m in against,
                           "model_key": m, "summary": ""}] for m in signatures}
    out = resp.consolidate(nodes, delivered, {ids[m]: book.comp(m) for m in signatures})
    return {k: out[k] for k in ("agreement", "weighted_lean", "uncertainty", "independent_voices", "dissent")}


def params_record(p: LoopParams = LoopParams()) -> dict:
    return {"name": "Brother Mode closed loop defaults", "calibrated": False, "note": "fixed a-priori constants; not fitted on any data, including the four QA-2D disagreement rows", "params": asdict(p)}
