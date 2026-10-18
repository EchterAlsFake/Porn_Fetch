"""Embed a monotonic CI build version in frozen CLI binaries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.shared.version import BUILD_VERSION, RELEASE_TIMESTAMP

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("platform", choices=("linux", "windows", "macos"))
    parser.add_argument("architecture", choices=("x64", "arm64", "x86", "x32", "riscv64", "s390x", "ppc64le"))
    args = parser.parse_args()
    output = Path(__file__).resolve().parents[1] / "src/cli/update_build.json"
    system = "darwin" if args.platform == "macos" else args.platform
    architecture = "amd64" if args.architecture == "x64" else args.architecture
    output.write_text(json.dumps({
        "release_timestamp": RELEASE_TIMESTAMP,
        "version": BUILD_VERSION,
        "target": f"{system}/{architecture}.zip",
    }), encoding="utf-8")
