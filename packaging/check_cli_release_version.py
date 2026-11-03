"""Reject stale CLI publication versions before starting platform builds."""

import argparse
import runpy
import tempfile
from pathlib import Path

publisher = runpy.run_path(str(Path(__file__).with_name("publish_cli_updates.py")))
previous_metadata = publisher["previous_metadata"]


def check_version(version: str, remote_url: str, root_file: Path) -> None:
    requested = tuple(map(int, version.split(".")))
    with tempfile.TemporaryDirectory() as temporary:
        previous = previous_metadata(remote_url, root_file.read_bytes(), Path(temporary))
        if previous is None:
            return
        conflicts = {
            name: target.custom["version"]
            for name, target in previous[0].signed.targets.items()
            if tuple(map(int, target.custom["version"].split("."))) >= requested
        }
    if conflicts:
        published = max(conflicts.values(), key=lambda value: tuple(map(int, value.split("."))))
        raise ValueError(
            f"CLI release {version} must be newer than published version {published}. "
            "Choose a newer release_version, or disable CLI publishing for a build-only run."
        )
    print(f"CLI release {version} is newer than the published targets.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version")
    parser.add_argument("--remote-url", default="https://api.pornfetch.to/repo/cli/")
    parser.add_argument("--root-file", type=Path, default=publisher["ROOT_FILE"])
    args = parser.parse_args()
    check_version(args.version, args.remote_url, args.root_file)
