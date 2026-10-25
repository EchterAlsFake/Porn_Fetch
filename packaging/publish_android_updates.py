"""Sign the Android APK feed after immutable website release publication."""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

from securesystemslib.signer import Signer
from tuf.api.exceptions import ExpiredMetadataError
from tuf.api.metadata import Metadata, MetaFile, Root, Snapshot, TargetFile, Targets, Timestamp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from publish_cli_updates import ROOT_FILE, previous_metadata

ABIS = {"arm64": "arm64-v8a", "armv7": "armeabi-v7a", "x64": "x86_64", "x86": "x86"}


def select_targets(releases):
    chosen = {}
    for release in releases:
        for artifact in release["artifacts"]:
            abi = ABIS.get(artifact["arch"])
            if artifact["kind"] != "apk" or artifact["platform"] != "android" or not abi:
                continue
            previous = chosen.get(abi)
            if previous and (previous[0]["channel"] == "stable" or release["channel"] != "stable"):
                continue
            chosen[abi] = release, artifact
    targets = {}
    for abi, (release, artifact) in chosen.items():
        target = TargetFile(artifact["size"], {"sha256": artifact["sha256"]}, f"android/{abi}.apk")
        target.unrecognized_fields["custom"] = {
            "abi": abi, "package": "to.pornfetch.app", "version": release["version"],
            "filename": artifact["filename"], "channel": release["channel"],
            "release_timestamp": int(datetime.fromisoformat(release["published_at"]).timestamp()),
            "changelog": release["notes"],
        }
        targets[target.path] = target
    return targets


def signed_files(root_bytes, targets, signer, previous=None):
    now = datetime.now(timezone.utc)
    old_targets, old_snapshot, old_timestamp = previous or (None, None, None)
    targets_md = Metadata(Targets(version=old_targets.signed.version + 1 if old_targets else 1,
                                  expires=now + timedelta(days=30), targets=targets))
    targets_md.sign(signer)
    targets_bytes = targets_md.to_bytes()
    snapshot = Metadata(Snapshot(version=old_snapshot.signed.version + 1 if old_snapshot else 1,
                                  expires=now + timedelta(days=14), meta={
                                      "targets.json": MetaFile.from_data(targets_md.signed.version, targets_bytes, ["sha256"])}))
    snapshot.sign(signer)
    snapshot_bytes = snapshot.to_bytes()
    timestamp = Metadata(Timestamp(version=old_timestamp.signed.version + 1 if old_timestamp else 1,
                                    expires=now + timedelta(days=7),
                                    snapshot_meta=MetaFile.from_data(snapshot.signed.version, snapshot_bytes, ["sha256"])))
    timestamp.sign(signer)
    root = Metadata[Root].from_bytes(root_bytes)
    for role, metadata in (("targets", targets_md), ("snapshot", snapshot), ("timestamp", timestamp)):
        root.signed.verify_delegate(role, metadata.signed_bytes, metadata.signatures)
    return {"root.json": root_bytes, "targets.json": targets_bytes,
            "snapshot.json": snapshot_bytes, "timestamp.json": timestamp.to_bytes()}


def publish(origin, private_key, *, allow_empty=False):
    from publish_website_release import send
    token = os.environ.get("WEBSITE_RELEASE_TOKEN", "")
    if not token:
        raise ValueError("WEBSITE_RELEASE_TOKEN is required")
    # send() validates the HTTPS origin and refuses redirecting the bearer token.
    releases = json.loads(send(origin, "GET", "/download/catalog.json", ""))["releases"]
    targets = select_targets(releases)
    if not targets:
        if allow_empty:
            print("No Android release published yet")
            return
        raise ValueError("No Android APKs in the website release catalog")
    root_bytes = ROOT_FILE.read_bytes()
    root = Metadata[Root].from_bytes(root_bytes)
    keyid = root.signed.roles["targets"].keyids[0]
    signer = Signer.from_priv_key_uri(f"file2:{private_key.resolve()}", root.signed.keys[keyid])
    with tempfile.TemporaryDirectory() as cache:
        try:
            previous = previous_metadata(origin + "/repo/android/", root_bytes, Path(cache))
        except ExpiredMetadataError:
            # Publisher recovery is allowed to renew expired, still-authentic
            # metadata. Clients continue to reject expired metadata normally.
            previous = tuple(Metadata.from_bytes(send(origin, "GET", "/repo/android/metadata/" + role + ".json", ""))
                             for role in ("targets", "snapshot", "timestamp"))
            for role, metadata in zip(("targets", "snapshot", "timestamp"), previous):
                root.signed.verify_delegate(role, metadata.signed_bytes, metadata.signatures)
    files = signed_files(root_bytes, targets, signer, previous)
    payload = {"files": {name: base64.b64encode(data).decode("ascii") for name, data in files.items()}}
    send(origin, "POST", "/ci/android-updates", token, json.dumps(payload).encode())
    for name, data in files.items():
        if send(origin, "GET", "/repo/android/metadata/" + name, "") != data:
            raise RuntimeError("Published Android metadata does not match the signed snapshot")
    print("Published and verified Android update metadata")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--origin", default="https://pornfetch.to")
    parser.add_argument("--private-key", type=Path, required=True)
    parser.add_argument("--allow-empty", action="store_true")
    args = parser.parse_args()
    publish(args.origin, args.private_key, allow_empty=args.allow_empty)
