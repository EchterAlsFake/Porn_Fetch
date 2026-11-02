"""Sign private copies of the CLI's native payload before creating the onefile EXE."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def sign_payload(entries: list[tuple[str, str, str]], workpath: str) -> list[tuple[str, str, str]]:
    destination = Path(workpath) / "signed-binaries"
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    result = []
    for name, source, kind in entries:
        if Path(source).suffix.lower() in {".exe", ".dll", ".pyd", ".sys"}:
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            source = str(target)
        result.append((name, source, kind))
    subprocess.run([
        "pwsh", "-NoProfile", "-File", str(Path(__file__).with_name("sign_windows.ps1")),
        "-Paths", str(destination),
    ], check=True)
    return result
