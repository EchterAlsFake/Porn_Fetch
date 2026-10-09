"""Launcher for the QML desktop and Android applications."""
from __future__ import annotations

import os
import sys

# Ensure mobile flag is set on Android environments
if (
    "ANDROID_ARGUMENT" in os.environ
    or "ANDROID_BOOTSTRAP" in os.environ
    or hasattr(sys, "getandroidapilevel")
    or sys.platform == "android"
) and "--android" not in sys.argv:
    sys.argv.append("--android")

if __name__ == "__main__" and "--smoke-test" in sys.argv:
    from src.backend.packaging_smoke import run_isolated_smoke

    raise SystemExit(run_isolated_smoke())

from src.backend.application import Backend, ProcessVideos, main

__all__ = ["Backend", "ProcessVideos", "main"]


if __name__ == "__main__":
    main()
