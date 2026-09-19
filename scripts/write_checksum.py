#!/usr/bin/env python3
"""Write a portable SHA-256 sidecar file for a build artifact."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    artifact = args.artifact.resolve()
    if not artifact.is_file():
        parser.error(f"artifact does not exist: {artifact}")
    sidecar = artifact.with_name(f"{artifact.name}.sha256")
    sidecar.write_text(f"{sha256(artifact)}  {artifact.name}\n", encoding="utf-8")
    print(sidecar)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
