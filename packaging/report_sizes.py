"""Inventory release payloads without extraction; optionally compare a previous JSON report."""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import tarfile
import zipfile
from collections import defaultdict
from pathlib import Path


def digest(stream):
    return hashlib.file_digest(stream, "sha256").hexdigest()


def inventory(path: Path) -> dict:
    entries = []
    if path.is_dir():
        for file in sorted(path.rglob("*")):
            if file.is_file() and not file.is_symlink():
                with file.open("rb") as stream:
                    entries.append({"path": file.relative_to(path).as_posix(),
                                    "bytes": file.stat().st_size, "sha256": digest(stream)})
    elif zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for entry in archive.infolist():
                if not entry.is_dir():
                    with archive.open(entry) as stream:
                        entries.append({"path": entry.filename, "bytes": entry.file_size,
                                        "compressed_bytes": entry.compress_size, "sha256": digest(stream)})
    elif path.name.endswith((".tar.gz", ".tar.xz", ".tar")):
        with tarfile.open(path) as archive:
            for entry in archive:
                if entry.isfile():
                    with archive.extractfile(entry) as stream:
                        entries.append({"path": entry.name, "bytes": entry.size, "sha256": digest(stream)})
    else:
        with path.open("rb") as stream:
            entries.append({"path": path.name, "bytes": path.stat().st_size, "sha256": digest(stream)})
    groups = defaultdict(list)
    for entry in entries:
        if entry["bytes"]:
            groups[(entry["sha256"], entry["bytes"])].append(entry["path"])
    return {"path": path.as_posix(), "file_bytes": path.stat().st_size if path.is_file() else None,
            "payload_bytes": sum(entry["bytes"] for entry in entries),
            "entries": sorted(entries, key=lambda entry: entry["bytes"], reverse=True),
            "duplicates": [{"bytes_each": size, "paths": paths, "redundant_bytes": size * (len(paths) - 1)}
                           for (_, size), paths in groups.items() if len(paths) > 1]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paths", required=True, help="Newline separated paths/globs")
    parser.add_argument("--label", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--baseline", type=Path)
    args = parser.parse_args()
    paths = sorted({Path(match) for pattern in args.paths.splitlines() if pattern.strip()
                    for match in glob.glob(pattern.strip())})
    if not paths:
        parser.error("No payloads matched")
    report = {"label": args.label, "artifacts": [inventory(path) for path in paths]}
    baseline = json.loads(args.baseline.read_text()) if args.baseline else {"artifacts": []}
    previous = {item["path"]: item for item in baseline["artifacts"]}
    lines = [f"### Release sizes: {args.label}", "", "| Payload | File bytes | Content bytes |", "| --- | ---: | ---: |"]
    for item in report["artifacts"]:
        old = previous.get(item["path"])
        if old:
            item["comparison"] = {}
            for key in ("file_bytes", "payload_bytes"):
                if item[key] is not None and old[key] is not None:
                    delta = item[key] - old[key]
                    item["comparison"][key] = {"delta_bytes": delta,
                                               "delta_percent": delta / old[key] * 100 if old[key] else None}
        lines.append(f"| {item['path']} | {item['file_bytes'] if item['file_bytes'] is not None else '—'} | {item['payload_bytes']} |")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("\n".join(lines))
    if summary := os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(summary, "a", encoding="utf-8") as stream:
            stream.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
