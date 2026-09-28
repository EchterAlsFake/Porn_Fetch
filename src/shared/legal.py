"""Read the application license and notices in source and packaged CLI builds."""

from __future__ import annotations

import sys
from pathlib import Path


def legal_document(name: str) -> str:
    if name not in {"LICENSE", "THIRD_PARTY_NOTICES.md"}:
        raise ValueError(f"Unknown legal document: {name}")
    bundle_root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    return (bundle_root / name).read_text(encoding="utf-8")
