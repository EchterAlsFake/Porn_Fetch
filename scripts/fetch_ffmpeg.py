#!/usr/bin/env python3
"""Build the minimal LGPL-only FFmpeg executable (keeps the existing command name)."""
import runpy
from pathlib import Path

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[1] / "packaging/build_ffmpeg.py"), run_name="__main__")
