#!/bin/bash
# The offline proof of the collaboration integration and the pilot package: scripted models only, zero network, zero inference. Same interpreter and component sources as the arms use.
# usage: evidence/ogi013-pilot/offline_tests.sh [extra pytest args]
cd "$(dirname "$0")/../.." || exit 2
C=${OGI013_COMPONENTS:-/root/fruits/integration/ogi013-org-components}
export PYTHONPATH=$C/CherryMe:$C/PeachMe/src:$C/PlumMe/src:$C/AppleMe/src:runners:tests:.
exec ${OGI013_HOSTPY:-/root/fruits/integration/ogi013-hostpython-org/bin/python} -m pytest -q -p no:cacheprovider \
  tests/test_ogi013_org_collab.py tests/test_ogi013_lineage_heart.py tests/test_ogi013_integrated_runtime.py tests/test_ogi013_pilot_guard.py tests/test_ogi013_pilot_gate.py \
  tests/test_ogi013_pilot_package.py tests/test_ogi013_real_plumme.py tests/test_ogi013_trace_report.py tests/test_ogi013_org_economy.py tests/test_ogi013_tau2_host.py tests/test_ogi013_single_e.py \
  tests/test_ogi013_decisionlog_roundtrip.py tests/test_ogi013_org_policy.py tests/test_ogi013_measurement_amendment.py tests/test_ogi013_pilot_e2e.py "$@"
