"""Split the full snapshot into GitHub release assets and hash every part."""
import argparse
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("directory", type=Path)
args = parser.parse_args()
directory = args.directory
archive = directory / "ios-lab-full-snapshot.tar.zst"
part_limit = 1_900_000_000  # Below GitHub's 2 GiB per-release-asset limit.
parts = []
whole = hashlib.sha256()
with archive.open("rb") as source:
    number = 0
    while source.tell() < archive.stat().st_size:
        part = directory / f"{archive.name}.part-{number:03d}"
        if part.exists():
            raise SystemExit(f"Refusing to overwrite {part}")
        digest = hashlib.sha256()
        remaining = part_limit
        with part.open("wb") as target:
            while remaining and (block := source.read(min(remaining, 1024**2))):
                target.write(block)
                digest.update(block)
                whole.update(block)
                remaining -= len(block)
        parts.append({"name": part.name, "bytes": part.stat().st_size, "sha256": digest.hexdigest()})
        print(f"Prepared {part.name}: {part.stat().st_size:,} bytes", flush=True)
        number += 1
manifest = json.loads((directory / "snapshot-manifest.json").read_text())
assets = {
    "repository": "EchterAlsFake/Porn_Fetch",
    "branch": "ios/iphone7-port-snapshot-2026-10-28",
    "tag": "ios-iphone7-snapshot-2026-10-28",
    "base_commit": "b38c98e27b9318da374c1cf3a639b3e813b436e6",
    "archive": archive.name,
    "archive_bytes": archive.stat().st_size,
    "archive_sha256": whole.hexdigest(),
    "archive_format": "tar compressed with zstd; concatenate all parts in numbered order",
    "uncompressed_file_bytes": manifest["uncompressed_file_bytes"],
    "entries": manifest["entries"],
    "signing_fingerprint": "7082BBFF855D47C6BB13C3BF6AC58B8CA26D1C5F",
    "parts": parts,
}
metadata = directory / "snapshot-assets.json"
metadata.write_text(json.dumps(assets, indent=2) + "\n")
checksums = [f'{p["sha256"]}  {p["name"]}' for p in parts]
for path in [directory / "snapshot-manifest.json", metadata]:
    with path.open("rb") as stream:
        checksums.append(f'{hashlib.file_digest(stream, "sha256").hexdigest()}  {path.name}')
(directory / "SHA256SUMS").write_text("\n".join(checksums) + "\n")
here = Path(__file__).resolve().parent
for path in [metadata, directory / "SHA256SUMS"]:
    (here / path.name).write_bytes(path.read_bytes())
print(f'Hashed {len(parts)} parts; full archive SHA-256 {whole.hexdigest()}', flush=True)
