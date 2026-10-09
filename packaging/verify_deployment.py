"""Verify the public metadata and representative payloads after repository deployment."""
from __future__ import annotations

import argparse
import asyncio
import sys
import tempfile
from pathlib import Path

from base_api import BaseCore
from base_api.modules.config import RuntimeConfig
from tuf.api.metadata import Metadata, Root, Targets
from tuf.ngclient import Updater

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.shared.release import ROOT_FILE, safe_repo_path, verify_repository_manifest  # noqa: E402


async def fetch(core: BaseCore, url: str) -> bytes:
    # fetch_bytes bypasses BaseCore's text cache.
    return await core.fetch_bytes(url, headers={"Cache-Control": "no-cache"}, allow_redirects=False)


async def verify_cli(core: BaseCore, repository: Path, remote_url: str, root_file: Path = ROOT_FILE) -> None:
    root = Metadata[Root].from_file(str(root_file))
    if root.signed.is_expired():
        raise ValueError("The CLI trust root has expired")
    if await fetch(core, f"{remote_url}/metadata/{root.signed.version}.root.json") != root_file.read_bytes():
        raise ValueError("Published CLI root does not match the build's trust root")
    # Run the same TUF client workflow as the CLI with a fresh cache on every attempt.
    await asyncio.to_thread(verify_cli_client, repository, remote_url, root_file)


def verify_cli_client(repository: Path, remote_url: str, root_file: Path) -> None:
    with tempfile.TemporaryDirectory() as temporary:
        cache = Path(temporary)
        updater = Updater(
            metadata_dir=str(cache / "metadata"),
            metadata_base_url=f"{remote_url}/metadata/",
            target_dir=str(cache / "targets"),
            target_base_url=f"{remote_url}/targets/",
            bootstrap=root_file.read_bytes(),
        )
        updater.refresh()
        for role in ("root", "timestamp", "snapshot", "targets"):
            blob = (cache / "metadata" / f"{role}.json").read_bytes()
            if blob != (repository / "metadata" / f"{role}.json").read_bytes():
                raise ValueError(f"Published CLI {role} metadata does not match this deployment")
        targets = Metadata[Targets].from_file(str(cache / "metadata" / "targets.json"))
        # Prefer freshly uploaded targets; refresh-only runs sample the existing repository.
        for target in targets.signed.targets.values():
            safe_repo_path(target.path)
        changed = [target for target in targets.signed.targets.values()
                   if (repository / "targets" / safe_repo_path(target.get_prefixed_paths()[0])).is_file()]
        candidates = changed or list(targets.signed.targets.values())
        if not candidates:
            raise ValueError("Published CLI repository has no targets")
        platforms = sorted({target.path.split("/", 1)[0] for target in candidates})
        for platform in platforms:
            target = min((item for item in candidates if item.path.startswith(platform + "/")),
                         key=lambda item: item.length)
            verified_target = updater.get_targetinfo(target.path)
            if verified_target is None:
                raise ValueError(f"Published CLI target is missing: {target.path}")
            updater.download_target(verified_target)
            print(f"Verified CLI payload: {target.path}")


async def verify_desktop(core: BaseCore, repository: Path, remote_url: str, platform: str,
                         root_file: Path = ROOT_FILE) -> None:
    blob = await fetch(core, f"{remote_url}/release.json")
    metadata, _ = verify_repository_manifest(blob, root_file.read_bytes(), platform)
    if blob != (repository / "release.json").read_bytes():
        raise ValueError("Published desktop manifest does not match this deployment")
    archives = [name for name in metadata.signed.targets if name.endswith(".7z")]
    if not archives:
        raise ValueError("Published desktop repository has no package archives")
    # The largest archive exercises the application payload rather than just IFW metadata.
    payload = max(archives, key=lambda name: metadata.signed.targets[name].length)
    for name in ("Updates.xml", payload):
        metadata.signed.targets[name].verify_length_and_hashes(await fetch(core, f"{remote_url}/{name}"))
        print(f"Verified desktop payload: {platform}/{name}")


async def verify(repository: Path, remote_url: str, kind: str, platform: str | None,
                 root_file: Path = ROOT_FILE) -> None:
    config = RuntimeConfig()
    config.timeout = 120
    async with BaseCore(configuration=config) as core:
        for attempt in range(3):
            try:
                if kind == "cli":
                    await verify_cli(core, repository, remote_url.rstrip("/"), root_file)
                else:
                    await verify_desktop(core, repository, remote_url.rstrip("/"), platform, root_file)
                return
            except Exception:
                if attempt == 2:
                    raise
                print("Deployment is not verified yet; retrying in five seconds", file=sys.stderr)
                await asyncio.sleep(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=("cli", "desktop"))
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--remote-url", required=True)
    parser.add_argument("--platform")
    parser.add_argument("--root-file", type=Path, default=ROOT_FILE, help="Local public trust anchor")
    args = parser.parse_args()
    if args.kind == "desktop" and not args.platform:
        parser.error("--platform is required for desktop verification")
    asyncio.run(verify(args.repository, args.remote_url, args.kind, args.platform, args.root_file))
