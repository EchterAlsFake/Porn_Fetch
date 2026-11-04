#!/usr/bin/env bash
# Porn Fetch Android Build Automation Wrapper
set -euo pipefail

# Resolve symlinks to determine actual project root
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
    DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
PROJECT_ROOT="$(cd -P "$(dirname "$SOURCE")" && pwd)"

# Prefer virtual environment python
if [[ -n "${VIRTUAL_ENV:-}" && -x "$VIRTUAL_ENV/bin/python" ]]; then
    PYTHON_EXE="$VIRTUAL_ENV/bin/python"
elif [[ -x "$PROJECT_ROOT/.venv/bin/python" ]]; then
    PYTHON_EXE="$PROJECT_ROOT/.venv/bin/python"
else
    PYTHON_EXE="$(command -v python3 || command -v python)"
fi

export PATH="$(dirname "$PYTHON_EXE"):$PATH"

exec "$PYTHON_EXE" "$PROJECT_ROOT/scripts/build_android.py" "$@"
