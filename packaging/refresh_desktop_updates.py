"""Renew signed desktop manifests without rebuilding or changing release targets."""
import argparse
import asyncio
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from base_api import BaseCore
from base_api.modules.errors import HTTPStatusError
from securesystemslib.signer import Signer
from tuf.api.metadata import Metadata, Root

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.shared.release import ROOT_FILE
from src.shared.update_channels import validate_release

PLATFORMS = ("linux_amd64", "windows_amd64", "darwin_amd64", "darwin_arm64")


def renew(blob, root_bytes, private_key, platform, channel):
    root, metadata = Metadata[Root].from_bytes(root_bytes), Metadata.from_bytes(blob)
    if root.signed.is_expired():
        raise ValueError("The update trust root has expired")
    root.signed.verify_delegate("targets", metadata.signed_bytes, metadata.signatures)
    release = metadata.signed.unrecognized_fields["release"]
    if release["platform"] != platform:
        raise ValueError("Desktop repository platform mismatch")
    if channel is not None:
        validate_release(release, channel)
    keyid = root.signed.roles["targets"].keyids[0]
    signer = Signer.from_priv_key_uri(f"file2:{private_key.resolve()}", root.signed.keys[keyid])
    metadata.signed.expires = datetime.now(timezone.utc) + timedelta(days=30)
    metadata.signed.version += 1
    metadata.sign(signer)
    root.signed.verify_delegate("targets", metadata.signed_bytes, metadata.signatures)
    return metadata.to_bytes()


async def refresh(private_key, channel):
    token = os.environ["CI_TOKEN"]
    root_bytes = ROOT_FILE.read_bytes()
    async with BaseCore() as core:
        for platform in PLATFORMS:
            prefix = (channel + "/") if channel else ""
            url = f"https://api.pornfetch.to/repo/{prefix}{platform}/release.json"
            try:
                response = await core.request(url, allow_redirects=False)
            except HTTPStatusError as error:
                if error.status_code != 404:
                    raise
                print(f"No desktop release published yet: {prefix}{platform}")
                continue
            if response.status_code == 404:
                continue
            response.raise_for_status()
            blob = renew(response.content, root_bytes, private_key, platform, channel)
            headers = {"X-CI-TOKEN": token, "X-CI-Target": platform, "Content-Type": "application/json"}
            if channel:
                headers["X-CI-Channel"] = channel
            response = await core.request("https://api.pornfetch.to/ci/deploy/ifw-metadata", method="POST",
                                          headers=headers, data=blob, allow_redirects=False)
            response.raise_for_status()
            published = await core.fetch_bytes(url, headers={"Cache-Control": "no-cache"}, allow_redirects=False)
            if published != blob:
                raise ValueError("Published desktop metadata differs from the renewed manifest")
            print(f"Renewed {prefix}{platform}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-key", type=Path, required=True)
    parser.add_argument("--channel", choices=("stable", "beta"))
    args = parser.parse_args()
    asyncio.run(refresh(args.private_key, args.channel))
