"""Offline cost-class count of PlumMe's bundled donor free-allowance registry (no network, no inference).

Classification follows PlumMe main: FREE = freeType in free_registry.ADMIT_FREE_TYPES and tos in ADMIT_TOS;
TRIAL = freeType in free_supply.TRIAL_TYPES; everything else EXCLUDED (discontinued, or terms avoid/ambiguous/unknown).
Paid (LOW/NORMAL/PREMIUM) routes are not in this registry; counting them needs live provider discovery.

    PYTHONPATH=<PlumMe main>/src python route_classes.py > route_classes.json
"""
import json
from collections import Counter, defaultdict

import plumme
from plumme.free_registry import ADMIT_FREE_TYPES, ADMIT_TOS, free_registry
from plumme.free_supply import TRIAL_TYPES

reg = free_registry()
models, providers = Counter(), defaultdict(set)
for provider, entry in reg.items():
    if provider == '_donor':
        continue
    for row in entry['models'].values():
        cls = ('FREE' if row['freeType'] in ADMIT_FREE_TYPES and row['tos'] in ADMIT_TOS
               else 'TRIAL' if row['freeType'] in TRIAL_TYPES else 'EXCLUDED')
        models[cls] += 1
        providers[cls].add(provider)
print(json.dumps({'plumme_version': plumme.__version__, 'donor': reg['_donor'],
                  'model_routes': dict(models),
                  'providers': {k: len(v) for k, v in providers.items()},
                  'paid_routes': 'not in the offline registry; needs live discovery'}, indent=1))
