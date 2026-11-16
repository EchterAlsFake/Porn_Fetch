"""Build signed TUF metadata and CLI bundles for one update channel."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from securesystemslib.signer import Signer
from tuf.api.exceptions import DownloadError, DownloadLengthMismatchError, ExpiredMetadataError
from tuf.api.metadata import Metadata, MetaFile, Root, Snapshot, TargetFile, Targets, Timestamp
from tuf.ngclient import Updater
from tuf.ngclient.urllib3_fetcher import Urllib3Fetcher

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.shared.update_channels import validate_channel, validate_release, version_parts
from src.shared.version import BUILD_CHANNEL, RELEASE_TIMESTAMP

ROOT_FILE = Path(__file__).resolve().parents[1] / "src/cli/update_root.json"
ARTIFACT_TARGETS = {
    "PornFetch_linux_CLI_x64": "linux/amd64.zip",
    "PornFetch_linux_CLI_arm64": "linux/arm64.zip",
    "PornFetch_windows_CLI_x64": "windows/amd64.zip",
    "PornFetch_windows_CLI_arm64": "windows/arm64.zip",
    "PornFetch_windows_CLI_x86": "windows/x86.zip",
    "PornFetch_macos_CLI_x64": "darwin/amd64.zip",
    "PornFetch_macos_CLI_arm64": "darwin/arm64.zip",
    "PornFetch_Linux_CLI_x32": "linux/x32.zip",
    "PornFetch_Linux_CLI_riscv64": "linux/riscv64.zip",
    "PornFetch_Linux_CLI_s390x": "linux/s390x.zip",
    "PornFetch_Linux_CLI_ppc64le": "linux/ppc64le.zip",
}


def previous_metadata(remote_url: str, root_bytes: bytes, cache_dir: Path) -> tuple[Metadata[Targets], Metadata[Snapshot], Metadata[Timestamp]] | None:
    for attempt in range(3):
        try:
            return fetch_previous_metadata(remote_url, root_bytes, cache_dir)
        except (urllib.error.URLError, TimeoutError, DownloadError) as exc:
            status = getattr(exc, "code", None) or getattr(exc, "status_code", None)
            if (attempt == 2 or isinstance(exc, DownloadLengthMismatchError)
                    or (status is not None and status not in (408, 429) and status < 500)):
                raise
            print(f"CLI metadata download failed ({exc}); retrying ({attempt + 2}/3)", flush=True)
            time.sleep(5 * (attempt + 1))

def fetch_previous_metadata(remote_url: str, root_bytes: bytes, cache_dir: Path) -> tuple[Metadata[Targets], Metadata[Snapshot], Metadata[Timestamp]] | None:
    timestamp_url = f"{remote_url.rstrip('/')}/metadata/timestamp.json"
    try:
        with urllib.request.urlopen(timestamp_url, timeout=60) as response:
            response.read(1)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            exc.close()
            return None
        raise

    metadata_dir = cache_dir / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)
    updater = Updater(
        metadata_dir=str(metadata_dir),
        metadata_base_url=f"{remote_url.rstrip('/')}/metadata/",
        bootstrap=root_bytes,
        fetcher=Urllib3Fetcher(socket_timeout=60),
    )
    try:
        updater.refresh()
    except ExpiredMetadataError:
        root = Metadata[Root].from_bytes(root_bytes)
        if root.signed.is_expired():
            raise ValueError("The update trust root has expired") from None
        recovered = {}
        for role in ("timestamp", "snapshot", "targets"):
            with urllib.request.urlopen(f"{remote_url.rstrip('/')}/metadata/{role}.json", timeout=60) as response:
                blob = response.read()
            metadata = Metadata.from_bytes(blob)
            root.signed.verify_delegate(role, metadata.signed_bytes, metadata.signatures)
            recovered[role] = metadata, blob
        for parent, child in (("timestamp", "snapshot"), ("snapshot", "targets")):
            parent_md = recovered[parent][0]
            reference = parent_md.signed.snapshot_meta if parent == "timestamp" else parent_md.signed.meta["targets.json"]
            reference.verify_length_and_hashes(recovered[child][1])
            if reference.version != recovered[child][0].signed.version:
                raise ValueError("Inconsistent expired repository metadata")
        return tuple(recovered[role][0] for role in ("targets", "snapshot", "timestamp"))
    return (
        Metadata[Targets].from_file(str(metadata_dir / "targets.json")),
        Metadata[Snapshot].from_file(str(metadata_dir / "snapshot.json")),
        Metadata[Timestamp].from_file(str(metadata_dir / "timestamp.json")),
    )


def create_bundle(artifact: Path, target_name: str, version: str, destination: Path, *, channel=BUILD_CHANNEL) -> TargetFile:
    validate_channel(channel)
    binary = artifact / (artifact.name + (".exe" if target_name.startswith("windows/") else ""))
    if not binary.is_file():
        raise FileNotFoundError(f"CLI executable missing: {binary}")
    files = sorted(path for path in artifact.iterdir() if path.is_file() and not path.name.endswith(".sha256"))
    manifest = {"release_timestamp": RELEASE_TIMESTAMP, "version": version, "target": target_name, "executable": binary.name, "files": [path.name for path in files]}
    manifest["channel"] = channel
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        bundle.writestr("manifest.json", json.dumps(manifest, separators=(",", ":")))
        for path in files:
            info = zipfile.ZipInfo(path.name)
            info.external_attr = (0o755 if path == binary or path.name.startswith("pocketbase") else 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            with path.open("rb") as source, bundle.open(info, "w") as output:
                shutil.copyfileobj(source, output)
    target = TargetFile.from_file(target_name, str(destination))
    target.unrecognized_fields["custom"] = {"version": version, "release_timestamp": RELEASE_TIMESTAMP, "channel": channel}
    return target


def publish(artifact_dir: Path | None, remote_url: str, output_dir: Path, private_key: Path, version: str | None,
            *, allow_empty: bool = False, root_file: Path | None = None, channel=BUILD_CHANNEL, legacy=False) -> None:
    validate_channel(channel)
    if legacy and artifact_dir is not None and channel != "stable":
        raise ValueError("Only Stable builds can update the compatibility feed")
    root_bytes = (root_file or ROOT_FILE).read_bytes()
    root = Metadata[Root].from_bytes(root_bytes)
    online_keyid = root.signed.roles["targets"].keyids[0]
    signer = Signer.from_priv_key_uri(f"file2:{private_key.resolve()}", root.signed.keys[online_keyid])

    with tempfile.TemporaryDirectory() as temporary:
        previous = previous_metadata(remote_url, root_bytes, Path(temporary))
        old_targets, old_snapshot, old_timestamp = previous if previous else (None, None, None)
        targets = dict(old_targets.signed.targets) if old_targets else {}
        if not legacy:
            for target in targets.values():
                validate_release(target.custom or {}, channel)
        new_files: list[tuple[Path, TargetFile]] = []
        if artifact_dir is not None:
            if not version:
                raise ValueError("--version is required when publishing artifacts")
            for artifact in sorted(artifact_dir.iterdir()):
                target_name = ARTIFACT_TARGETS.get(artifact.name)
                if not artifact.is_dir() or target_name is None:
                    continue
                existing = targets.get(target_name)
                if existing and legacy and version_parts(existing.custom["version"]) >= version_parts(version):
                    continue  # Older clients wait until Stable overtakes their existing feed.
                if existing and version_parts(existing.custom["version"]) > version_parts(version):
                    raise ValueError(f"Target version must increase: {target_name}")
                archive = Path(temporary) / "bundles" / artifact.name
                target = create_bundle(artifact, target_name, version, archive, channel=channel)
                if existing and version_parts(existing.custom["version"]) == version_parts(version):
                    if existing.to_dict() != target.to_dict():
                        raise ValueError(f"Same release version has different bytes or identity: {target_name}")
                targets[target_name] = target
                new_files.append((archive, target))
            if not new_files and not (legacy and targets):
                raise ValueError("No recognized CLI artifact directories found; do not merge artifact downloads")
        if not targets:
            if allow_empty and artifact_dir is None:
                print("No CLI update repository exists yet; nothing to refresh")
                return
            raise ValueError("No CLI artifacts or existing update repository found")

        now = datetime.now(timezone.utc)
        targets_md = Metadata(Targets(version=old_targets.signed.version + 1 if old_targets else 1, expires=now + timedelta(days=30), targets=targets))
        targets_md.sign(signer)
        root.signed.verify_delegate("targets", targets_md.signed_bytes, targets_md.signatures)
        targets_bytes = targets_md.to_bytes()
        snapshot_md = Metadata(Snapshot(
            version=old_snapshot.signed.version + 1 if old_snapshot else 1,
            expires=now + timedelta(days=14),
            meta={"targets.json": MetaFile.from_data(targets_md.signed.version, targets_bytes, ["sha256"])},
        ))
        snapshot_md.sign(signer)
        root.signed.verify_delegate("snapshot", snapshot_md.signed_bytes, snapshot_md.signatures)
        snapshot_bytes = snapshot_md.to_bytes()
        timestamp_md = Metadata(Timestamp(
            version=old_timestamp.signed.version + 1 if old_timestamp else 1,
            expires=now + timedelta(days=7),
            snapshot_meta=MetaFile.from_data(snapshot_md.signed.version, snapshot_bytes, ["sha256"]),
        ))
        timestamp_md.sign(signer)
        root.signed.verify_delegate("timestamp", timestamp_md.signed_bytes, timestamp_md.signatures)

        metadata = output_dir / "metadata"
        metadata.mkdir(parents=True, exist_ok=True)
        for name, data in (
            ("root.json", root_bytes),
            (f"{root.signed.version}.root.json", root_bytes),
            ("targets.json", targets_bytes),
            (f"{targets_md.signed.version}.targets.json", targets_bytes),
            ("snapshot.json", snapshot_bytes),
            (f"{snapshot_md.signed.version}.snapshot.json", snapshot_bytes),
            ("timestamp.json", timestamp_md.to_bytes()),
        ):
            (metadata / name).write_bytes(data)
        for archive, target in new_files:
            prefixed = target.get_prefixed_paths()[0]
            destination = output_dir / "targets" / prefixed
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(archive, destination)
        print(f"Prepared {len(new_files)} CLI bundles; metadata version {timestamp_md.signed.version}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, help="Downloaded CLI build artifacts; omit to refresh metadata only")
    parser.add_argument("--remote-url", required=True, help="Published CLI TUF repository base URL")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--private-key", required=True, type=Path)
    parser.add_argument("--version", help="Monotonic application build version")
    parser.add_argument("--channel", choices=("stable", "beta"), default=BUILD_CHANNEL)
    parser.add_argument("--legacy-feed", action="store_true", help="Refresh the compatibility feed or publish a newer Stable bridge build")
    parser.add_argument("--allow-empty", action="store_true", help="Succeed if a scheduled refresh has no repository yet")
    parser.add_argument("--root-file", type=Path, default=ROOT_FILE, help="Local public trust anchor")
    args = parser.parse_args()
    publish(args.artifacts, args.remote_url, args.output, args.private_key, args.version,
            allow_empty=args.allow_empty, root_file=args.root_file, channel=args.channel, legacy=args.legacy_feed)
