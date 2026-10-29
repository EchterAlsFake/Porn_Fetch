#!/bin/bash
set -eu
DEVICE_DIR=$(cd -- "$(dirname -- "$0")" && pwd)
rsync -a --exclude='__pycache__/' "$DEVICE_DIR/vendor/" "$CODESIGNING_FOLDER_PATH/packages/"
PYFRAMEWORK=/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework
REL_FRAMEWORK=$(/usr/local/bin/python3 -c 'import os,sys; print(os.path.relpath(sys.argv[1],sys.argv[2]))' "$PYFRAMEWORK" "$PROJECT_DIR")
source "$PYFRAMEWORK/build/utils.sh"
export EXPANDED_CODE_SIGN_IDENTITY="${EXPANDED_CODE_SIGN_IDENTITY:--}"
export EXPANDED_CODE_SIGN_IDENTITY_NAME="${EXPANDED_CODE_SIGN_IDENTITY_NAME:-ad-hoc}"
process_dylibs "$REL_FRAMEWORK" packages
