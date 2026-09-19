#!/usr/bin/env bash
set -euo pipefail

umask 077

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
project_dir="$(cd -- "$script_dir/../../../.." && pwd)"
geneva_dir="${GENEVA_DIR:-/home/asuna/geneva}"
geneva_python="${GENEVA_PYTHON:-$geneva_dir/.venv/bin/python3}"
pornfetch_python="${PORNFETCH_PYTHON:-$project_dir/.venv/bin/python3}"
output_root="${PORNFETCH_GENEVA_OUTPUT_ROOT:-$project_dir/src/tests/manual/geneva_runs}"
ports="${GENEVA_PORTS:-80,443}"
strategy="${GENEVA_STRATEGY:-\/}"

for required in pasta "$geneva_python" "$pornfetch_python" "$geneva_dir/engine.py"; do
    if [[ "$required" == */* ]]; then
        [[ -e "$required" ]] || { printf 'Missing required path: %s\n' "$required" >&2; exit 1; }
    else
        command -v "$required" >/dev/null || { printf 'Missing required command: %s\n' "$required" >&2; exit 1; }
    fi
done

run_id="$(date -u +'%Y%m%dT%H%M%SZ')-$$"
run_dir="$output_root/$run_id"
mkdir -p -- "$run_dir"

if (( $# )); then
    app_command=("$@")
else
    app_command=("$pornfetch_python" "$project_dir/src/tests/smoke/sni_proxy_smoke.py" "https://example.com/")
fi

printf 'Starting a rootless, app-only network namespace.\n'
printf 'Run artifacts: %s\n' "$run_dir"
printf 'Application: '
printf '%q ' "${app_command[@]}"
printf '\n'

export PORNFETCH_PROJECT_DIR="$project_dir"
export PORNFETCH_GENEVA_RUN_DIR="$run_dir"

exec pasta \
    --config-net \
    --quiet \
    --ipv4-only \
    --no-map-gw \
    --tcp-ports none \
    --udp-ports none \
    --pcap "$run_dir/namespace-wire.pcap" \
    -- \
    "$geneva_python" "$script_dir/geneva_runner.py" \
    --geneva-dir "$geneva_dir" \
    --output-dir "$run_dir" \
    --ports "$ports" \
    --strategy "$strategy" \
    -- "${app_command[@]}"
