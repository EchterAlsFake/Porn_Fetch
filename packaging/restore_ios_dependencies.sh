#!/usr/bin/env bash
# Restore only the device extensions and Python overlay, never the Intel tools.
set -euo pipefail
destination=${1:?Usage: restore_ios_dependencies.sh DESTINATION}
snapshot_manifest=${2:-ios-lab/snapshot-assets.json}
mkdir -p "$destination/parts"
python3 - "$snapshot_manifest" > "$destination/parts.tsv" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text())
for part in manifest["parts"]:
    print(part["name"], part["sha256"], sep="\t")
PY

# Each part is verified before entering the decompressor and discarded after
# streaming. The runner needs space for one part plus the selected 72 MB payload.
while IFS=$'\t' read -r name digest; do
    echo "Downloading and verifying $name" >&2
    gh release download ios-iphone7-snapshot-2026-10-28 \
        --repo EchterAlsFake/Porn_Fetch --pattern "$name" --dir "$destination/parts"
    archive="$destination/parts/$name"
    printf '%s  %s\n' "$digest" "$archive" | sha256sum --check --status
    cat -- "$archive"
    rm -- "$archive"
done < "$destination/parts.tsv" | zstd -dc | tar -xf - --no-same-owner \
    -C "$destination" ios-lab/pornfetch/vendor ios-lab/device/native/packages
