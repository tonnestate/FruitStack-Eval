#!/bin/bash
# Local replica of .github/workflows/tests.yml (GitHub Actions has not started a single job on this account since the billing failure: "recent account payments have failed").
# Same steps as the workflow - fresh venv per Python, `pip install -e .[dev]`, `pytest -q`, `compileall` - from a CLEAN CLONE of the given ref, so nothing of this machine's extra components leaks in.
# usage: evidence/ogi013-pilot/ci_local.sh [REF=HEAD]     needs uv; exit 0 only if every Python passes
set -u
REF=${1:-HEAD}; SRC=$(cd "$(dirname "$0")/../.." && pwd); W=$(mktemp -d); rc=0
git clone -q "$SRC" "$W/src" && git -C "$W/src" checkout -q "$(git -C "$SRC" rev-parse "$REF")" || exit 2
for v in 3.11 3.12 3.13; do
  uv venv -q -p "$v" "$W/venv$v" && uv pip install -q -p "$W/venv$v/bin/python" -e "$W/src[dev]" || { echo "python $v: install FAILED"; rc=1; continue; }
  res=$(cd "$W/src" && "$W/venv$v/bin/python" -m pytest -q 2>&1 | tail -1); (cd "$W/src" && "$W/venv$v/bin/python" -m compileall -q fruitstack_eval) && c=ok || c=FAILED
  echo "python $v: $res | compile $c"; case "$res" in *failed*|*error*) rc=1;; esac; [ "$c" = ok ] || rc=1
done
rm -rf "$W"; exit $rc
