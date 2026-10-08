#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-}"
REPO_DIR="${2:-}"

if [[ -z "$TARGET" || -z "$REPO_DIR" || ! -d "$REPO_DIR" ]]; then
  echo "Usage: $0 <target_arch> <path_to_repo_dir>" >&2
  echo "Example: $0 linux_amd64 dist/ifw_repo/linux_amd64" >&2
  exit 1
fi

if [[ -z "${CI_TOKEN:-}" ]]; then
  echo "Error: CI_TOKEN environment variable is required." >&2
  exit 1
fi

BUNDLE_TAR="$(mktemp --suffix=.tar.gz)"
trap 'rm -f "$BUNDLE_TAR"' EXIT

echo "Packaging IFW repository for $TARGET..."
tar -czf "$BUNDLE_TAR" -C "$REPO_DIR" .

echo "Uploading IFW repository to https://api.pornfetch.to/ci/deploy/ifw..."
curl -f -sS -X POST \
  -H "X-CI-TOKEN: $CI_TOKEN" \
  -H "X-CI-Target: $TARGET" \
  --data-binary @"$BUNDLE_TAR" \
  https://api.pornfetch.to/ci/deploy/ifw

echo "Successfully deployed IFW repository for $TARGET."
