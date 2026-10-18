"""Sign the complete Qt repository with the existing TUF targets release key.

Run only in release CI/operator tooling. The private key is never bundled.
"""
import argparse
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from securesystemslib.signer import Signer
from tuf.api.metadata import Metadata, Root, TargetFile, Targets

from src.shared.release import (
    GITHUB_RELEASES_URL,
    ROOT_FILE,
    STATIC_CHANGELOG_NAME,
    safe_repo_path,
    validate_ifw_packages,
)
from src.shared.version import RELEASE_TIMESTAMP


def release_notes(path: Path) -> str:
    """Publish the separately maintained current release notes."""
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError("Current release changelog is empty")
    return text.strip()


def sign_repository(repository, platform, version, private_key, root_file=ROOT_FILE, *, changelog=""):
    repository = Path(repository)
    xml = ET.parse(repository / "Updates.xml")
    validate_ifw_packages(xml, version, RELEASE_TIMESTAMP)
    (repository / STATIC_CHANGELOG_NAME).write_text(changelog + "\n", encoding="utf-8")
    targets = {}
    for path in sorted(repository.rglob("*")):
        if path.is_file() and path.name != "release.json":
            name = safe_repo_path(path.relative_to(repository).as_posix())
            targets[name] = TargetFile.from_file(name, str(path))
    metadata = Metadata(Targets(expires=datetime.now(timezone.utc) + timedelta(days=30), targets=targets))
    metadata.signed.unrecognized_fields["release"] = {
        "version": version, "release_timestamp": RELEASE_TIMESTAMP, "platform": platform,
        "changelog": changelog, "changelog_format": "markdown", "release_url": GITHUB_RELEASES_URL,
        "changelog_path": STATIC_CHANGELOG_NAME,
    }
    root = Metadata[Root].from_file(str(root_file))
    keyid = root.signed.roles["targets"].keyids[0]
    metadata.sign(Signer.from_priv_key_uri(f"file2:{Path(private_key).resolve()}", root.signed.keys[keyid]))
    root.signed.verify_delegate("targets", metadata.signed_bytes, metadata.signatures)
    metadata.to_file(str(repository / "release.json"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--platform", required=True, help="Qt repo tag, e.g. linux_amd64")
    parser.add_argument("--version", required=True)
    parser.add_argument("--private-key", type=Path, required=True)
    parser.add_argument("--changelog-file", type=Path, default=Path(__file__).resolve().parents[1] / STATIC_CHANGELOG_NAME)
    args = parser.parse_args()
    sign_repository(
        args.repository, args.platform, args.version, args.private_key,
        changelog=release_notes(args.changelog_file),
    )
