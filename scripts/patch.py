"""Mark packaged GUI builds as binary installations."""
import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import build_output  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    build_output.add_arguments(parser)
    args = parser.parse_args()
    build_output.configure(args)
    path = Path(__file__).resolve().parents[1] / "src/backend/config.py"
    try:
        original = path.read_text(encoding="utf-8")
        updated = original.replace("IS_SOURCE_RUN = True", "IS_SOURCE_RUN = False")
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            build_output.message("Binary build flag patched.", "ok")
        else:
            build_output.message("Binary build flag unchanged.", "ok")
        build_output.detail(f"Target: {path}")
    except OSError as error:
        build_output.message(str(error), "error")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
