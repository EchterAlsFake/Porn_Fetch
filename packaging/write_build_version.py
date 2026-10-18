"""Embed one workflow's artifact version and release timestamp before building."""
import argparse
import re
from pathlib import Path


def write_build_version(version: str, release_timestamp: int, source: Path | None = None) -> None:
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)+", version):
        raise ValueError("Release version must contain dot-separated numbers, for example 3.9.66")
    if release_timestamp <= 0:
        raise ValueError("Release timestamp must be positive")
    source = source or Path(__file__).resolve().parents[1] / "src/shared/version.py"
    text = source.read_text()
    for name in ("__version__", "BUILD_VERSION"):
        text, count = re.subn(
            rf'^{name} = "[0-9.]+"$', f'{name} = "{version}"', text, flags=re.MULTILINE,
        )
        if count != 1:
            raise ValueError(f"Missing {name} version constant")
    text, count = re.subn(
        r'^RELEASE_TIMESTAMP = .+$',
        f'RELEASE_TIMESTAMP = {release_timestamp}',
        text,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise ValueError("Missing release timestamp constant")
    source.write_text(text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="Full release version, for example 3.9.66")
    parser.add_argument("--release-timestamp", type=int, required=True)
    args = parser.parse_args()
    write_build_version(args.version, args.release_timestamp)
