"""Embed the CI artifact version without changing the committed release timestamp."""
import argparse
import re
from pathlib import Path


def write_build_version(build_number: int) -> None:
    if build_number <= 0:
        raise ValueError("Build number must be positive")
    source = Path(__file__).resolve().parents[1] / "src/shared/version.py"
    text = source.read_text()
    version = re.search(r'^__version__ = "([0-9.]+)"$', text, re.MULTILINE).group(1)
    text, count = re.subn(r'^BUILD_VERSION = "[0-9.]+"$', f'BUILD_VERSION = "{version}.{build_number}"', text, flags=re.MULTILINE)
    if count != 1:
        raise ValueError("Missing build version constant")
    source.write_text(text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_number", type=int)
    write_build_version(parser.parse_args().build_number)
