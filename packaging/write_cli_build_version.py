"""Embed a monotonic CI build version in frozen CLI binaries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.shared.version import __version__

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_number", type=int)
    args = parser.parse_args()
    if args.build_number <= 0:
        parser.error("build number must be positive")
    output = Path(__file__).resolve().parents[1] / "src/cli/update_build.json"
    output.write_text(json.dumps({"version": f"{__version__}.{args.build_number}"}), encoding="utf-8")
