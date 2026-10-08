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
if [[ -x "$PROJECT_ROOT/.venv/bin/python" ]]; then
    PYTHON_EXE="$PROJECT_ROOT/.venv/bin/python"
elif [[ -n "${VIRTUAL_ENV:-}" && -x "$VIRTUAL_ENV/bin/python" ]]; then
    PYTHON_EXE="$VIRTUAL_ENV/bin/python"
else
    PYTHON_EXE="$(command -v python3 || command -v python)"
fi

# Ensure .venv/bin is in PATH for tools like buildozer / pyside6-android-deploy
if [[ -d "$PROJECT_ROOT/.venv/bin" ]]; then
    export PATH="$PROJECT_ROOT/.venv/bin:$PATH"
fi

exec "$PYTHON_EXE" "$PROJECT_ROOT/scripts/build_android.py" "$@"
