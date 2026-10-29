#!/bin/sh
# Source this file; no system-wide Xcode setting needs changing.
if [ -z "${DEVELOPER_DIR:-}" ]; then
    if [ -d /Applications/Xcode.app/Contents/Developer ]; then
        DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
    else
        DEVELOPER_DIR=/Users/asuna/Downloads/Xcode.app/Contents/Developer
    fi
fi
export DEVELOPER_DIR
export TMPDIR=/private/tmp
