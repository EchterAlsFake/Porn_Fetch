"""Run an explicit live pagination suite against installed or workspace providers."""

from __future__ import annotations

import argparse
import os
import runpy
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--suite",
        required=True,
        choices=(
            "profiles",
            "clients",
            "full",
            "indexed",
            "images",
            "accounts",
            "complete_profiles",
            "account_complete",
            "user_feeds",
            "controls",
            "creator_scan",
            "negative",
        ),
    )
    parser.add_argument("--workspace", type=Path, help="Use eaf_base_api and provider sources under this directory")
    parser.add_argument("--output-dir", type=Path, default=Path("/tmp/pornfetch-pagination-live"))
    args, remaining = parser.parse_known_args()
    project = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project))
    if args.workspace:
        root = args.workspace.resolve()
        sys.path[:0] = [str(root / "eaf_base_api"), *(str(p) for p in sorted(root.glob("unofficial-api-for-*")))]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    os.environ["PAGINATION_LIVE_OUTPUT"] = str(args.output_dir.resolve())
    sys.argv = [sys.argv[0], *remaining]
    runpy.run_module("src.tests.pagination." + args.suite, run_name="__main__")


if __name__ == "__main__":
    main()
