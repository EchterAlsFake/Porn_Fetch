"""Check that the APK's native Qt preloads can be extracted by Android's installer."""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


def check_apk(apk: Path, abi: str) -> None:
    with zipfile.ZipFile(apk) as archive:
        libraries = [entry for entry in archive.infolist() if entry.filename.startswith("lib/")
                     and not entry.is_dir()]
        invalid = [entry.filename for entry in libraries
                   if len(Path(entry.filename).parts) != 3
                   or Path(entry.filename).parts[1] != abi
                   or not Path(entry.filename).name.startswith("lib")
                   or not entry.filename.endswith(".so") or entry.file_size == 0]
        if invalid:
            raise ValueError(f"Invalid native libraries for Android {abi}: {', '.join(invalid)}")
        required = {f"lib/{abi}/{name}" for name in (
            "libQtCore.abi3.so", "libpyside6.abi3.so", "libshiboken6.abi3.so", "libpython3.15.so", "libTor.so",
        )}
        missing = required - set(archive.namelist())
        if missing:
            raise ValueError(f"Missing native Android runtime libraries: {', '.join(sorted(missing))}")
    print(f"Verified {len(libraries)} extractable native libraries for {abi}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("apk", type=Path)
    parser.add_argument("--abi", required=True, choices=("arm64-v8a", "armeabi-v7a", "x86", "x86_64"))
    args = parser.parse_args()
    check_apk(args.apk, args.abi)
