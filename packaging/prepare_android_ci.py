"""Prepare portable Android specs from the tracked deployment settings for CI."""

from __future__ import annotations

import argparse
import configparser
from pathlib import Path


def prepare(project: Path, venv: Path, version: str) -> None:
    buildozer_path = project / "buildozer.spec"
    buildozer = configparser.ConfigParser(interpolation=None)
    buildozer.read(buildozer_path, encoding="utf-8")
    app = buildozer["app"]
    # Keep application requirements, permissions and the minimum API from the
    # working spec. build_android.py replaces SDK/NDK, ABI, icon and hook paths.
    app["version"] = version
    app["source.dir"] = str(project)
    extensions = app.get("source.include_exts", "py,png,qml,js").split(",")
    app["source.include_exts"] = ",".join(dict.fromkeys([*extensions, "json", "txt"]))
    app["android.api"] = "36"
    app.pop("android.add_jars", None)
    buildozer["buildozer"]["bin_dir"] = str(project)
    with buildozer_path.open("w", encoding="utf-8") as destination:
        buildozer.write(destination)

    config = configparser.ConfigParser(interpolation=None)
    config.read(project / "packaging/pysidedeploy_android.spec", encoding="utf-8")
    config["app"].update({
        "project_dir": str(project), "input_file": str(project / "main.py"),
        "exec_directory": str(project),
        # Use the Android requirements below rather than desktop project metadata.
        "project_file": "",
    })
    config["python"]["python_path"] = str(venv / "bin/python")
    config["android"].update({
        "package_name": app["package.name"], "package_domain": app["package.domain"],
        "version": version,
        "requirements": ",".join(
            item for item in app["requirements"].split(",")
            if item.strip().lower() not in {"python3", "shiboken6", "pyside6"}
        ),
    })
    with (project / "pysidedeploy.spec").open("w", encoding="utf-8") as destination:
        config.write(destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--venv", type=Path, required=True)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    prepare(Path(__file__).resolve().parents[1], args.venv.resolve(), args.version)
