"""Create a platform-specific bundle of license texts for a built artifact."""

from __future__ import annotations

import argparse
import re
import shutil
from importlib.metadata import distributions
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZIP_DEFLATED, ZipFile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LGPL_URL = "https://www.gnu.org/licenses/lgpl-3.0.txt"
NOTICE_NAMES = ("license", "licence", "copying", "notice", "copyright")


def collect_legal(output: Path, *, offline: bool = False) -> Path:
    output.mkdir(parents=True, exist_ok=True)
    for name in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
        shutil.copy2(PROJECT_ROOT / name, output / name)
    shutil.copytree(PROJECT_ROOT / "LICENSES", output / "LICENSES", dirs_exist_ok=True)
    inventory = [
        "# Python distributions in the build environment",
        "",
        "The list may include build tools absent from the executable. Compare it with the finished artifact before publication.",
        "",
        "Package | Version | Declared license | License files",
        "--- | --- | --- | ---",
    ]
    review = []
    has_qt = False
    for dist in sorted(distributions(), key=lambda item: (item.metadata.get("Name") or "").lower()):
        name = dist.metadata.get("Name") or "unknown"
        if name.lower() == "porn-fetch":
            continue
        has_qt |= name.lower() in {"pyside6", "pyside6-essentials", "pyside6-addons", "shiboken6"}
        safe_name = re.sub(r"[^A-Za-z0-9.-]", "-", name)
        license_id = dist.metadata.get("License-Expression") or dist.metadata.get("License") or "unidentified"
        license_id = " ".join(license_id.split())
        found = []
        for entry in dist.files or []:
            source = Path(dist.locate_file(entry))
            if not source.is_file() or not source.name.lower().startswith(NOTICE_NAMES):
                continue
            target = output / "python" / safe_name / source.name
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and target.read_bytes() != source.read_bytes():
                target = target.with_name(f"{len(found) + 1}-{source.name}")
            shutil.copy2(source, target)
            found.append(target.relative_to(output).as_posix())
        if not found:
            review.append(f"- {name} {dist.version}: no license file found in installed metadata")
        inventory.append(f"{name} | {dist.version} | {license_id.replace('|', '/')} | {', '.join(found) or 'review required'}")

    if has_qt:
        qt_text = output / "LICENSES" / "LGPL-3.0-only.txt"
        if not offline:
            with urlopen(LGPL_URL, timeout=20) as response:
                data = response.read()
            if b"GNU LESSER GENERAL PUBLIC LICENSE" not in data[:500]:
                raise ValueError("Downloaded LGPL text is not recognized")
            qt_text.write_bytes(data)
        elif not qt_text.exists():
            review.append("- Qt: LGPL-3.0 text must be included; rerun without --offline")
        review.append("- Qt: verify shipped modules, replacement of LGPL libraries, and source availability")

    (output / "PYTHON_INVENTORY.md").write_text("\n".join(inventory) + "\n", encoding="utf-8")
    (output / "REVIEW_REQUIRED.md").write_text(
        "# Checks before publication\n\n" + "\n".join(review) + "\n"
        + "\nCheck FFmpeg linkage, PocketBase, assets, and rights to other contributors' code.\n",
        encoding="utf-8",
    )
    archive = output.with_suffix(".zip")
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as bundle:
        for file in sorted(output.rglob("*")):
            if file.is_file():
                bundle.write(file, file.relative_to(output))
    return archive


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--offline", action="store_true")
    arguments = parser.parse_args()
    print(collect_legal(arguments.output, offline=arguments.offline))
