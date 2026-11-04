#!/usr/bin/env bash
## Updates the entire frontend
set -euo pipefail

cd -- "$(dirname -- "$0")"

# Shared extraction, validation, catalog compilation and resource generation.
uv run --no-sync python ../../scripts/translations.py extract "$@"
uv run --no-sync python ../../scripts/translations.py build "$@"

# Ahead-of-time QML bytecode compilation
uv run --no-sync python ../../scripts/compile_qml.py "$@"
