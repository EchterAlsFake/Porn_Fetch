"""Check required Python startup packages in an iOS app or IPA before shipping."""

import argparse
import zipfile
from pathlib import Path


def check_packages(files: set[str]) -> None:
    required = {f"packages/jwt/{name}.py" for name in ("__init__", "api_jwt", "api_jws", "algorithms")}
    missing = required - files
    if missing:
        raise ValueError(f"Missing iOS Python startup module jwt; bundle PyJWT: {', '.join(sorted(missing))}")
    if not any(name.lower().startswith("packages/pyjwt-") and name.endswith(".dist-info/METADATA")
               for name in files):
        raise ValueError("Missing iOS PyJWT distribution metadata; bundle the complete wheel")


def check_app(path: Path) -> None:
    if path.is_dir():
        files = {p.relative_to(path).as_posix() for p in (path / "packages").rglob("*")
                 if p.is_file() and p.stat().st_size}
    else:
        with zipfile.ZipFile(path) as archive:
            entries = {entry.filename for entry in archive.infolist() if not entry.is_dir() and entry.file_size}
            roots = {name.removesuffix("Info.plist") for name in entries
                     if len(name.split("/")) == 3 and name.startswith("Payload/")
                     and name.endswith(".app/Info.plist")}
            if len(roots) != 1:
                raise ValueError("Expected one application under Payload in the IPA")
            root = roots.pop()
            files = {name.removeprefix(root) for name in entries if name.startswith(root)}
    check_packages(files)
    print(f"Verified iOS PyJWT startup package and distribution metadata in {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("app", type=Path, help="Built .app directory or packaged .ipa")
    check_app(parser.parse_args().app)
