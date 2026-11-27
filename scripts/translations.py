"""Extract, validate, generate and package Qt GUI catalogs."""
import argparse
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import build_output  # noqa: E402
from src.backend.ui_languages import LANGUAGES, RELEASE_LOCALES  # noqa: E402

FRONTEND = ROOT / "src/frontend"
CATALOGS = FRONTEND / "translations/ts"
CATALOG_NAMES = tuple(catalog for _, _, catalog in LANGUAGES if catalog)
# Explicit shared sources with GUI messages. Keep CLI code out of extraction.
SOURCES = (
    *sorted((ROOT / "src/backend").rglob("*.py")),
    *sorted((FRONTEND / "UI").rglob("*.qml")),
    ROOT / "src/database/bridge.py",
    ROOT / "src/licensing/service.py",
    ROOT / "src/shared/account_capabilities.py",
    ROOT / "src/shared/error_reporting.py",
)
TOKENS = re.compile(
    r"https?://[a-zA-Z0-9._~:/?#@!$&*+,;=%+-]+(?<![.,;:!?])"
    r"|[a-zA-Z0-9_.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    r"|`[^`]+`|</?[a-zA-Z][^<>]*>|%L?\d+(?!\d|\$)|%Ln|%n|%(?:\([^)]+\))?[sdif]"
    r"|\$\{[a-zA-Z_][\w.]*\}|\$[a-zA-Z_][a-zA-Z0-9_]*|\*\.[a-zA-Z0-9*]+|\(\*\)"
)
INACTIVE = {"vanished", "obsolete"}
INVALID_XML = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\ud800-\udfff\ufffe\uffff]")


def run(tool, *args):
    executable = Path(sys.executable).parent / (tool + (".exe" if sys.platform == "win32" else ""))
    build_output.run([str(executable), *map(str, args)], cwd=ROOT, label=tool)


def messages(tree):
    for context in tree.findall("context"):
        for message in context.findall("message"):
            translation = message.find("translation")
            if translation is not None and translation.get("type") in INACTIVE:
                continue
            key = (context.findtext("name"), message.findtext("source", ""), message.findtext("comment", ""),
                   message.get("numerus") == "yes")
            yield key, message


def form_names(locale, key):
    if not key[3]:
        return ("translation",)
    return ("other",) if locale.startswith("zh") else ("one", "other")


def protected_tokens(text):
    return Counter(TOKENS.findall(text))


def validate_forms(locale, key, forms):
    source = key[1]
    if len(forms) != len(form_names(locale, key)):
        raise ValueError(f"wrong number of translation forms for {source[:80]!r}")
    for form in forms:
        if not isinstance(form, str) or not form.strip():
            raise ValueError(f"empty translation for {source[:80]!r}")
        if INVALID_XML.search(form):
            raise ValueError(f"invalid control character for {source[:80]!r}")
        if protected_tokens(source) != protected_tokens(form):
            raise ValueError(f"changed placeholders or protected text for {source[:80]!r}")


def extract_catalogs(paths, locations, *options):
    run("pyside6-lupdate", *SOURCES, "-source-language", "en", "-locations", locations,
        "-disable-heuristic", "sametext", "-disable-heuristic", "similartext", *options, "-ts", *paths)


def fresh_catalog():
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "en.ts"
        extract_catalogs([path], "absolute")
        return ET.parse(path), path.parent


def validate(*, compile_catalogs=True):
    fresh, _ = fresh_catalog()
    expected = dict(messages(fresh))
    errors = []
    coverage = {}
    for locale in CATALOG_NAMES:
        path = CATALOGS / f"{locale}.ts"
        tree = ET.parse(path)
        if tree.getroot().get("language") != locale:
            errors.append(f"{path.name}: TS language must be {locale}")
        entries = list(messages(tree))
        actual = dict(entries)
        if len(entries) != len(actual):
            errors.append(f"{path.name}: duplicate active messages")
        missing, extra = expected.keys() - actual.keys(), actual.keys() - expected.keys()
        changed = sum(expected[key].findtext("extracomment") != actual[key].findtext("extracomment")
                      for key in expected.keys() & actual.keys())
        if missing or extra or changed:
            errors.append(f"{path.name}: {len(missing)} missing, {len(extra)} stale, "
                          f"{changed} changed translator notes. Run extract.")
        finished = 0
        for key, message in entries:
            translation = message.find("translation")
            if translation is None or translation.get("type") == "unfinished":
                if locale == "en" and key[3]:
                    errors.append(f"{path.name}: add source-language plural forms for {key[1]!r}")
                continue
            try:
                forms = translation.findall("numerusform") if key[3] else [translation]
                validate_forms(locale, key, ["".join(form.itertext()) for form in forms])
            except ValueError as error:
                errors.append(f"{path.name}: {error}")
            finished += 1
        coverage[locale] = (finished, len(entries))
        build_output.detail(f"{path.name}: {finished}/{len(entries)} finished")
    if errors:
        raise SystemExit("\n".join(errors))
    if compile_catalogs:
        with tempfile.TemporaryDirectory() as directory:
            for locale in CATALOG_NAMES:
                release(locale, Path(directory) / f"{locale}.qm")
    return coverage


def extract():
    paths = [CATALOGS / f"{locale}.ts" for locale in CATALOG_NAMES]
    existing = [path for path in paths if path.exists()]
    if existing:
        extract_catalogs(existing, "relative")
    for path in paths:
        if not path.exists():
            extract_catalogs([path], "relative", "-target-language", path.stem)


def release(locale, destination):
    run("pyside6-lrelease", "-nounfinished", CATALOGS / f"{locale}.ts", "-qm", destination)


def build():
    coverage = validate(compile_catalogs=False)
    for locale in CATALOG_NAMES:
        release(locale, FRONTEND / f"translations/qm/{locale}.qm")
    manifest = ET.parse(FRONTEND / "resources.qrc")
    resource = next(item for item in manifest.getroot() if item.get("prefix") == "/translations")
    resource.clear()
    resource.set("prefix", "/translations")
    ET.SubElement(resource, "file", alias="en.qm").text = "translations/qm/en.qm"
    for locale in RELEASE_LOCALES:
        finished, total = coverage[locale]
        if finished:
            alias = f"{locale}.qm" if finished == total else f"drafts/{locale}.qm"
            ET.SubElement(resource, "file", alias=alias).text = f"translations/qm/{locale}.qm"
    ET.indent(manifest, space="    ")
    manifest.write(FRONTEND / "resources.qrc", encoding="unicode")
    with (FRONTEND / "resources.qrc").open("a", encoding="utf-8") as output:
        output.write("\n")
    for output in ("resources.rcc", "UI/resources.py"):
        args = ["--binary"] if output.endswith(".rcc") else []
        run("pyside6-rcc", *args, "--compress-algo", "zlib", "--compress", "9", FRONTEND / "resources.qrc", "-o", FRONTEND / output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["extract", "check", "build", "context", "generate"])
    parser.add_argument("--locale", choices=RELEASE_LOCALES, action="append", help="target locale, repeatable")
    parser.add_argument("--model", help="OpenAI model that supports structured outputs")
    parser.add_argument("--limit", type=int, help="manage at most this many pending messages per locale")
    build_output.add_arguments(parser)
    args = parser.parse_args()
    build_output.configure(args)
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    build_output.message(f"Translations: {args.command}")
    if args.command in {"context", "generate"}:
        from scripts.translation_ai import context_or_generate
        context_or_generate(args)
    else:
        {"extract": extract, "check": validate, "build": build}[args.command]()
    build_output.message(f"Translations {args.command} complete.", "ok")


if __name__ == "__main__":
    # Use the same module for the CLI and the generation pipeline.
    sys.modules["scripts.translations"] = sys.modules[__name__]
    main()
