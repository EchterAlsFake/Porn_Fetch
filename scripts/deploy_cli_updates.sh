#!/usr/bin/env bash
set -euo pipefail

CLI_DIR="${1:-dist/cli_tuf}"

if [[ ! -d "$CLI_DIR" ]]; then
  echo "Usage: $0 <path_to_cli_tuf_dir>" >&2
  exit 1
fi

if [[ -z "${CI_TOKEN:-}" ]]; then
  echo "Error: CI_TOKEN environment variable is required." >&2
  exit 1
fi

for metadata in root targets snapshot timestamp; do
  if [[ ! -f "$CLI_DIR/metadata/$metadata.json" ]]; then
    echo "Error: signed CLI metadata is missing: $metadata.json" >&2
    exit 1
  fi
done

BUNDLE_TAR="$(mktemp --suffix=.tar.gz)"
trap 'rm -f "$BUNDLE_TAR"' EXIT

echo "Packaging CLI updates..."
CONTENTS=(metadata)
if [[ -d "$CLI_DIR/targets" ]]; then CONTENTS+=(targets); fi
tar -czf "$BUNDLE_TAR" -C "$CLI_DIR" "${CONTENTS[@]}"

echo "Uploading CLI updates to https://api.pornfetch.to/ci/deploy/cli..."
curl -f -sS -X POST \
  -H "X-CI-TOKEN: $CI_TOKEN" \
  -H "Content-Type: application/gzip" \
  --data-binary @"$BUNDLE_TAR" \
  https://api.pornfetch.to/ci/deploy/cli

echo "Successfully deployed CLI TUF updates."
