"""OGI-013 host structure policy: chooses the responsibility_context (structure requirements) for one CherryMe decision.

CherryMe keeps cognitive authority. This policy only sets REQUIREMENTS (challenge / verify) through the trusted host
frame key 'responsibility_context'. OFF returns None so the engine's own triage ('auto') decides.
Decision rows and completion rows are append-only JSONL under <store_dir>/training/decisions.jsonl (SPEC: OGI013-ORG-DECISION/1)."""
from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cherryme.experiment import epsilon_floor_draw

STRUCTURES = {'S0': {}, 'S1': {'challenge': True}, 'S2': {'verify': True}, 'S3': {'challenge': True, 'verify': True}}
MODES = ('OFF', 'FIXED', 'RANDOMIZED', 'LEARNED')
PERMITTED = 'LEARNED_POLICY_PERMITTED_FOR_AUTHORIZED_ARM'
OFF_TUPLE = (None, None, None, 'OFF')


class HostStructurePolicy:
    def __init__(self, mode: str, *, task_ref: str, domain: str, store_dir: str | Path, fixed_arm: str | None = None,
                 learned: Any = None, authorized: bool = False, seed_salt: str = '') -> None:
        if mode not in MODES:
            raise ValueError(f'unknown mode {mode!r}')
        if mode == 'FIXED' and fixed_arm not in STRUCTURES:
            raise ValueError(f'FIXED needs fixed_arm in {sorted(STRUCTURES)}')
        if mode == 'LEARNED':
            self._check_learned(learned, authorized)
        self.mode, self.task_ref, self.domain, self.fixed_arm = mode, task_ref, domain, fixed_arm
        self.learned, self.store_dir = learned, Path(store_dir)
        self.seed = int(hashlib.sha256(f'{task_ref}|{seed_salt}'.encode()).hexdigest()[:16], 16)
        self.pool = list(STRUCTURES)

    @staticmethod
    def _check_learned(learned: Any, authorized: bool) -> None:
        # Refuse before any decision is made: no silent fallback to OFF or to a random arm.
        if learned is None or authorized is not True:
            raise RuntimeError('LEARNED_POLICY_NOT_AUTHORIZED')
        # The learner (train_org_policy.OrgPolicy) has already verified weight hashes against its attestation; the host additionally requires the permitting verdict itself.
        att = getattr(learned, 'attestation', None)
        if getattr(learned, 'permitted', False) is not True or not isinstance(att, dict) or att.get('verdict') != PERMITTED:
            raise RuntimeError('LEARNED_POLICY_NOT_AUTHORIZED')

    def choose(self, features: dict, decision_index: int) -> tuple[str | None, dict | None, float | None, str]:
        if self.mode == 'OFF':
            return OFF_TUPLE
        if self.mode == 'FIXED':
            return self.fixed_arm, dict(STRUCTURES[self.fixed_arm]), None, 'FIXED'
        if self.mode == 'RANDOMIZED':
            name, propensity, _explored = epsilon_floor_draw(self.pool, epsilon=1.0, seed=self.seed, draw_index=decision_index)
            return name, dict(STRUCTURES[name]), propensity, 'RANDOMIZED'
        name = self.learned.recommend(features)
        if name is None:
            return OFF_TUPLE                               # the learner abstains: engine triage decides
        if name not in STRUCTURES:
            raise ValueError(f'learned policy returned unknown structure {name!r}')
        return name, dict(STRUCTURES[name]), None, 'LEARNED'

    def _append(self, row: dict) -> None:
        path = self.store_dir / 'training' / 'decisions.jsonl'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('a', encoding='utf-8') as handle:
            handle.write(json.dumps(row, sort_keys=True, default=str) + '\n')

    def record_decision(self, *, features: dict, structure: str | None, propensity: float | None, arm_mode: str, claim_id: str) -> str:
        row_id = uuid.uuid4().hex
        self._append({'schema': 'OGI013-ORG-DECISION/1', 'row_id': row_id, 'task_ref': self.task_ref, 'domain': self.domain,
                      'arm_mode': arm_mode, 'structure': structure, 'propensity': propensity, 'features': features, 'claim_id': claim_id,
                      'plumme_ensemble_decision_id': None, 'accounting': None, 'contributions': None, 'revised': None,
                      'action_changed': None, 'provider_calls': None, 'provider_dispatches': None,
                      'created_at': datetime.now(timezone.utc).isoformat()})
        return row_id

    def finish_decision(self, row_id: str, **fields: Any) -> None:
        allowed = {'accounting', 'contributions', 'revised', 'action_changed', 'provider_calls', 'provider_dispatches', 'plumme_ensemble_decision_id'}
        unknown = set(fields) - allowed
        if unknown:
            raise ValueError(f'unknown completion fields {sorted(unknown)}')
        self._append({'schema': 'OGI013-ORG-DECISION-RESULT/1', 'row_id': row_id, **fields,
                      'created_at': datetime.now(timezone.utc).isoformat()})
