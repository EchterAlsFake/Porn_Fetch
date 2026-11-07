"""Read the application license and notices in source and packaged CLI builds."""

from __future__ import annotations

import sys
from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path


def legal_document(name: str) -> str:
    if name not in {"LICENSE", "THIRD_PARTY_NOTICES.md"}:
        raise ValueError(f"Unknown legal document: {name}")
    bundle_root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    document = bundle_root / name
    if document.is_file():
        return document.read_text(encoding="utf-8")
    # Wheels put PEP 639 license files in the distribution's metadata directory.
    try:
        text = distribution("Porn_Fetch").read_text(f"licenses/{name}")
    except PackageNotFoundError:
        text = None
    if text is not None:
        return text
    raise FileNotFoundError(f"The application legal document is missing: {name}")
