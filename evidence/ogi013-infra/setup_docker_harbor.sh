#!/bin/bash
# OGI-013 external-benchmark machine setup (SWE-bench Verified official harness + Terminal-Bench via Harbor). For a machine the OWNER PROVIDES (option 2). DRY-RUN BY DEFAULT.
#   dry run (default): read-only preflight checks + the exact commands that --apply would run. Changes nothing.
#   --apply          : executes them. Refused on the production host (markers below) and unless OGI013_INFRA_OWNER_MACHINE=1 is exported on the target machine.
# Nothing here was run on the production host. Package names/versions are to be verified by the operator against the benchmark documentation before --apply.
set -uo pipefail
APPLY=0; [ "${1:-}" = "--apply" ] && APPLY=1
MIN_DISK_GB=250; MIN_RAM_GB=16; MIN_CPU=4
PROD_MARKERS=("/var/www/avcos" "/var/lib/avcos" "/root/fruits/integration")      # any of these means: this is the production host
ok=1
check() { printf '  %-34s %s\n' "$1" "$2"; }
echo "== preflight (read-only) =="
OS=$(. /etc/os-release 2>/dev/null; echo "${PRETTY_NAME:-unknown}"); check "OS" "$OS"
ARCH=$(uname -m); check "architecture" "$ARCH $([ "$ARCH" = x86_64 ] && echo ok || { echo 'WARN: images are x86_64'; ok=0; })"
CPU=$(nproc); check "cpus" "$CPU $([ "$CPU" -ge $MIN_CPU ] && echo ok || { echo "WARN: < $MIN_CPU"; ok=0; })"
RAM=$(free -g | awk '/Mem:/{print $2}'); check "ram (GB)" "$RAM $([ "$RAM" -ge $MIN_RAM_GB ] && echo ok || { echo "WARN: < $MIN_RAM_GB"; ok=0; })"
DISK=$(df -BG --output=avail "${DOCKER_DATA_ROOT:-/var/lib}" 2>/dev/null | tail -1 | tr -dc 0-9); check "free disk for docker (GB)" "${DISK:-?} $([ "${DISK:-0}" -ge $MIN_DISK_GB ] && echo ok || { echo "WARN: < $MIN_DISK_GB (SWE-bench Verified images ~100-120 GB, Terminal-Bench ~20 GB, plus layers/logs)"; ok=0; })"
check "root" "$([ "$(id -u)" = 0 ] && echo yes || echo 'no (sudo needed for --apply)')"
check "docker already installed" "$(command -v docker >/dev/null && docker --version || echo no)"
for u in https://registry-1.docker.io/v2/ https://pypi.org https://github.com https://huggingface.co; do check "egress $u" "$(curl -sI --max-time 6 -o /dev/null -w '%{http_code}' "$u" 2>/dev/null || echo none)"; done
PROD=0; for m in "${PROD_MARKERS[@]}"; do [ -e "$m" ] && { PROD=1; check "production marker" "$m EXISTS"; }; done
[ $PROD = 0 ] && check "production host markers" "none (looks like a separate machine)"
echo "== plan =="
run() { echo "  + $*"; [ $APPLY = 1 ] && "$@"; return 0; }
run sudo apt-get update
run sudo apt-get install -y ca-certificates curl gnupg git python3-venv
run sudo install -m 0755 -d /etc/apt/keyrings
run bash -c 'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg'
run bash -c 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list'
run sudo apt-get update
run sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
run bash -c 'printf "{\"log-driver\":\"json-file\",\"log-opts\":{\"max-size\":\"50m\",\"max-file\":\"3\"}}\n" | sudo tee /etc/docker/daemon.json'
run sudo systemctl enable --now docker
run sudo usermod -aG docker "${SUDO_USER:-$USER}"
run bash -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'
run uv tool install harbor          # Terminal-Bench harness; verify the package name against the Terminal-Bench 2.x documentation first
run uv venv ~/swebench-venv
run uv pip install --python ~/swebench-venv/bin/python swebench
echo "== verification (after --apply; not run in a dry run) =="
for v in "docker run --rm hello-world" "docker info --format '{{.DockerRootDir}} {{.ServerVersion}}'" "harbor --help" "~/swebench-venv/bin/python -m swebench.harness.run_evaluation --help"; do echo "  ? $v"; done
echo "== gold calibration before any model run (owner-gated, later) =="
echo "  ? SWE-bench: run the harness on the gold patch of 1 instance and 1 instance of the sample; Terminal-Bench: oracle agent on 1 task"
if [ $APPLY = 1 ]; then
  [ $PROD = 1 ] && { echo "REFUSED: production host markers present"; exit 2; }
  [ "${OGI013_INFRA_OWNER_MACHINE:-0}" = 1 ] || { echo "REFUSED: export OGI013_INFRA_OWNER_MACHINE=1 on the owner-provided machine"; exit 2; }
  [ $ok = 1 ] || { echo "REFUSED: preflight warnings (resources)"; exit 2; }
else
  echo "(dry run: nothing was changed; production markers found: $PROD, resource checks ok: $ok)"
fi
