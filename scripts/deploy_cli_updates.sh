#!/usr/bin/env bash
# Make signed targets available before publishing the new TUF timestamp.
set -euo pipefail

repository=${1:?Pass the generated CLI update repository directory}
: "${IFW_DEPLOY_HOST:?Set IFW_DEPLOY_HOST}"
: "${IFW_DEPLOY_USER:?Set IFW_DEPLOY_USER}"
: "${IFW_DEPLOY_ROOT:?Set IFW_DEPLOY_ROOT}"
: "${IFW_SSH_KEY_FILE:?Set IFW_SSH_KEY_FILE}"
: "${IFW_KNOWN_HOSTS_FILE:?Set IFW_KNOWN_HOSTS_FILE}"

[[ $IFW_DEPLOY_HOST =~ ^[a-zA-Z0-9.-]+$ ]] || { echo "Invalid deploy host" >&2; exit 1; }
[[ $IFW_DEPLOY_USER =~ ^[a-zA-Z0-9._-]+$ ]] || { echo "Invalid deploy user" >&2; exit 1; }
[[ $IFW_DEPLOY_ROOT =~ ^/[a-zA-Z0-9._/-]+$ ]] || { echo "Invalid deploy root" >&2; exit 1; }
[[ -f $repository/metadata/timestamp.json ]] || { echo "Missing signed CLI timestamp" >&2; exit 1; }

remote="$IFW_DEPLOY_USER@$IFW_DEPLOY_HOST"
destination="$IFW_DEPLOY_ROOT/cli"
run_id=${GITHUB_RUN_ID:-manual}
ssh_options=(-i "$IFW_SSH_KEY_FILE" -o "UserKnownHostsFile=$IFW_KNOWN_HOSTS_FILE" -o StrictHostKeyChecking=yes -o BatchMode=yes)

ssh "${ssh_options[@]}" "$remote" "mkdir -p '$destination/metadata' '$destination/targets'"
rsync -a --delay-updates --exclude='/metadata/timestamp.json' \
  -e "ssh -i $IFW_SSH_KEY_FILE -o UserKnownHostsFile=$IFW_KNOWN_HOSTS_FILE -o StrictHostKeyChecking=yes -o BatchMode=yes" \
  "$repository/" "$remote:$destination/"
scp "${ssh_options[@]}" "$repository/metadata/timestamp.json" "$remote:$destination/metadata/timestamp.json.next-$run_id"
ssh "${ssh_options[@]}" "$remote" \
  "mv -f '$destination/metadata/timestamp.json.next-$run_id' '$destination/metadata/timestamp.json'"
echo "Published signed CLI update repository"
