"""Maintain Qt catalogs. Run with uv run python scripts/translations.py COMMAND."""
import argparse
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import build_output  # noqa: E402
from src.backend.ui_languages import LANGUAGES  # noqa: E402

FRONTEND = ROOT / "src/frontend"
CATALOGS = FRONTEND / "translations/ts"
TOKENS = re.compile(r"%L?\d+|%Ln|%n|%(?:\([^)]+\))?[sdif]|\$\{?[a-z_]+\}?")


def run(tool, *args):
    executable = Path(sys.executable).parent / (tool + (".exe" if sys.platform == "win32" else ""))
    result = subprocess.run([str(executable), *map(str, args)], cwd=ROOT, capture_output=True, text=True)
    if build_output.verbose() or result.returncode:
        print(result.stdout, end="", file=sys.stderr)
        print(result.stderr, end="", file=sys.stderr)
    result.check_returncode()


def validate():
    errors = []
    for path in sorted(CATALOGS.glob("*.ts")):
        tree = ET.parse(path)
        finished = total = 0
        for message in tree.findall(".//message"):
            translation = message.find("translation")
            if translation is None or translation.get("type") in {"vanished", "obsolete"}:
                continue
            total += 1
            if translation.get("type") == "unfinished":
                continue
            source = message.findtext("source", "")
            forms = translation.findall("numerusform") or [translation]
            if message.get("numerus") == "yes" and not translation.findall("numerusform"):
                errors.append(f"{path.name}: missing plural forms: {source[:70]}")
            for form in forms:
                target = "".join(form.itertext())
                if not target.strip() or Counter(TOKENS.findall(source)) != Counter(TOKENS.findall(target)):
                    errors.append(f"{path.name}: empty translation or changed placeholders: {source[:70]}")
            finished += 1
        build_output.detail(f"{path.name}: {finished}/{total} finished")
    if errors:
        raise SystemExit("\n".join(errors))
    # Compilation is deliberately temporary in check mode: CI must not rewrite catalogs.
    with tempfile.TemporaryDirectory() as directory:
        for path in CATALOGS.glob("*.ts"):
            run("pyside6-lrelease", "-nounfinished", path, "-qm", Path(directory) / (path.stem + ".qm"))


def extract():
    sources = sorted((ROOT / "src/backend").glob("*.py")) + sorted((FRONTEND / "UI").glob("*.qml"))
    paths = [CATALOGS / f"{catalog}.ts" for _, _, catalog in LANGUAGES if catalog]
    run("pyside6-lupdate", *sources, "-locations", "relative", "-ts", *paths)


def build():
    validate()
    for _, _, catalog in LANGUAGES:
        if catalog:
            run("pyside6-lrelease", "-nounfinished", CATALOGS / f"{catalog}.ts", "-qm", FRONTEND / f"translations/qm/{catalog}.qm")
    manifest = ET.parse(FRONTEND / "resources.qrc")
    resource = next(item for item in manifest.getroot() if item.get("prefix") == "/translations")
    resource.clear()
    resource.set("prefix", "/translations")
    for _, _, catalog in LANGUAGES:
        if catalog:
            ET.SubElement(resource, "file").text = f"translations/qm/{catalog}.qm"
    ET.indent(manifest, space="    ")
    manifest.write(FRONTEND / "resources.qrc", encoding="unicode")
    with (FRONTEND / "resources.qrc").open("a", encoding="utf-8") as output:
        output.write("\n")
    for output in ("resources.rcc", "UI/resources.py"):
        args = ["--binary"] if output.endswith(".rcc") else []
        run("pyside6-rcc", *args, "--compress-algo", "zlib", "--compress", "9", FRONTEND / "resources.qrc", "-o", FRONTEND / output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["extract", "check", "build"])
    build_output.add_arguments(parser)
    args = parser.parse_args()
    build_output.configure(args)
    build_output.message(f"Translations: {args.command}")
    {"extract": extract, "check": validate, "build": build}[args.command]()
    build_output.message(f"Translations {args.command} complete.", "ok")
