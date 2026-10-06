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

from src.shared.release import ROOT_FILE, safe_repo_path
from src.shared.version import RELEASE_TIMESTAMP


def sign_repository(repository, platform, version, private_key, root_file=ROOT_FILE):
    repository = Path(repository)
    xml = ET.parse(repository / "Updates.xml")
    packages = xml.findall("PackageUpdate")
    date = datetime.fromtimestamp(RELEASE_TIMESTAMP, timezone.utc).strftime("%Y-%m-%d")
    if len(packages) != 1 or packages[0].findtext("Version") != version or packages[0].findtext("ReleaseDate") != date:
        raise ValueError("Repository version/date must match the compiled release")
    targets = {}
    for path in sorted(repository.rglob("*")):
        if path.is_file() and path.name != "release.json":
            name = safe_repo_path(path.relative_to(repository).as_posix())
            targets[name] = TargetFile.from_file(name, str(path))
    metadata = Metadata(Targets(expires=datetime.now(timezone.utc) + timedelta(days=30), targets=targets))
    metadata.signed.unrecognized_fields["release"] = {
        "version": version, "release_timestamp": RELEASE_TIMESTAMP, "platform": platform,
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
    args = parser.parse_args()
    sign_repository(args.repository, args.platform, args.version, args.private_key)
