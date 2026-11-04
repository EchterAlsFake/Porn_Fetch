#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

for argument in "$@"; do
  case "$argument" in
    -v|--verbose) export PORN_FETCH_BUILD_VERBOSE=1 ;;
    -h|--help) echo "Usage: bash $0 [--verbose]"; exit 0 ;;
    *) echo "Unknown option: $argument" >&2; exit 2 ;;
  esac
done
build_status() {
  local label="$1" color=36; shift
  case "$label" in FAIL) color=31 ;; OK) color=32 ;; WARN) color=33 ;; esac
  if [[ -z "${NO_COLOR+x}" ]] && { [[ -t 2 || "${GITHUB_ACTIONS:-}" == true || "${FORCE_COLOR:-0}" != 0 ]]; }; then
    printf '\033[1;%sm[%s]\033[0m %s\n' "$color" "$label" "$*" >&2
  else
    printf '[%s] %s\n' "$label" "$*" >&2
  fi
}
run() {
  local label="$1" command_log result; shift
  command_log=$(mktemp "${TMPDIR:-/tmp}/pornfetch-build.XXXXXX")
  build_status INFO "$label — log: $command_log"
  case "${PORN_FETCH_BUILD_VERBOSE:-0}" in
    1|true|yes)
      if "$@" 2>&1 | tee "$command_log"; then result=0; else result=$?; fi ;;
    *)
      if "$@" >"$command_log" 2>&1; then result=0; else result=$?; fi ;;
  esac
  if [[ "$result" != 0 ]]; then
    tail -n 25 "$command_log" >&2
    build_status FAIL "$label failed (exit $result). Full log: $command_log"
    return "$result"
  fi
}

run "Update packages" pkg update -y
run "Install build tools" pkg install -y python git clang rust make pkg-config binutils libxml2 libxslt libffi openssl ffmpeg
python -c 'import sys; assert (3, 15) <= sys.version_info < (3, 16), "Porn Fetch needs Python 3.15. Update Termux packages first."'
if [[ -f pyproject.toml && -f Porn_Fetch_CLI.py ]]; then
  project_dir="$PWD"
elif [[ -f "$(dirname "${BASH_SOURCE[0]}")/../Porn_Fetch_CLI.py" ]]; then
  project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
else
  if [[ -e Porn_Fetch ]]; then
    build_status FAIL "Porn_Fetch already exists. Run this script from your checkout, or choose an empty folder."
    exit 1
  fi
  run "Fetch sources" git clone https://github.com/EchterAlsFake/Porn_Fetch
  project_dir="$PWD/Porn_Fetch"
fi
cd "$project_dir"
run "Create environment" python -m venv .venv-termux
run "Install dependencies" .venv-termux/bin/python -m pip install --upgrade --upgrade-strategy eager -e .
build_status OK "Ready. Start with: $project_dir/.venv-termux/bin/python $project_dir/Porn_Fetch_CLI.py"
