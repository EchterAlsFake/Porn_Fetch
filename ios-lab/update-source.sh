#!/bin/sh
set -eu
# User explicitly authorized discarding tracked edits that interfere with updating.
REPO=/Users/asuna/Porn_Fetch
git -C "$REPO" fetch --prune origin
git -C "$REPO" reset --hard origin/master
# Deliberately keep untracked files, app bundles, downloads and local configuration.
git -C "$REPO" log -1 --oneline
