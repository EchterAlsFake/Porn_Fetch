#!/usr/bin/env bash
# Publish Qt IFW archives before exposing their new Updates.xml metadata.
set -euo pipefail

artifacts_dir=${1:?Pass the downloaded IFW artifact directory}
: "${IFW_DEPLOY_HOST:?Set IFW_DEPLOY_HOST}"
: "${IFW_DEPLOY_USER:?Set IFW_DEPLOY_USER}"
: "${IFW_DEPLOY_ROOT:?Set IFW_DEPLOY_ROOT}"
: "${IFW_SSH_KEY_FILE:?Set IFW_SSH_KEY_FILE}"
: "${IFW_KNOWN_HOSTS_FILE:?Set IFW_KNOWN_HOSTS_FILE}"

[[ $IFW_DEPLOY_HOST =~ ^[a-zA-Z0-9.-]+$ ]] || { echo "Invalid deploy host" >&2; exit 1; }
[[ $IFW_DEPLOY_USER =~ ^[a-zA-Z0-9._-]+$ ]] || { echo "Invalid deploy user" >&2; exit 1; }
[[ $IFW_DEPLOY_ROOT =~ ^/[a-zA-Z0-9._/-]+$ ]] || { echo "Deploy root must be an absolute path without spaces" >&2; exit 1; }

ssh_options=(
  -i "$IFW_SSH_KEY_FILE"
  -o "UserKnownHostsFile=$IFW_KNOWN_HOSTS_FILE"
  -o StrictHostKeyChecking=yes
  -o BatchMode=yes
)
remote="$IFW_DEPLOY_USER@$IFW_DEPLOY_HOST"
run_id=${GITHUB_RUN_ID:-manual}

shopt -s nullglob
repositories=("$artifacts_dir"/IFW_repo_*/*)
((${#repositories[@]} > 0)) || { echo "No IFW repositories were downloaded" >&2; exit 1; }

for repository in "${repositories[@]}"; do
  [[ -d $repository && -f $repository/Updates.xml && -f $repository/release.json ]] || { echo "Invalid IFW repository: $repository" >&2; exit 1; }
  tag=${repository##*/}
  [[ $tag =~ ^(linux|windows|darwin)_(amd64|arm64)$ ]] || { echo "Unexpected IFW repository: $tag" >&2; exit 1; }
  destination="$IFW_DEPLOY_ROOT/$tag"

  ssh "${ssh_options[@]}" "$remote" "mkdir -p '$destination'"
  rsync -a --delay-updates --exclude='/Updates.xml' --exclude='/release.json' \
    -e "ssh -i $IFW_SSH_KEY_FILE -o UserKnownHostsFile=$IFW_KNOWN_HOSTS_FILE -o StrictHostKeyChecking=yes -o BatchMode=yes" \
    "$repository/" "$remote:$destination/"
  scp "${ssh_options[@]}" "$repository/Updates.xml" "$remote:$destination/Updates.xml.next-$run_id"
  ssh "${ssh_options[@]}" "$remote" \
    "mv -f '$destination/Updates.xml.next-$run_id' '$destination/Updates.xml'"
  scp "${ssh_options[@]}" "$repository/release.json" "$remote:$destination/release.json.next-$run_id"
  ssh "${ssh_options[@]}" "$remote" \
    "mv -f '$destination/release.json.next-$run_id' '$destination/release.json'"
  echo "Published IFW repository: $tag"
done
