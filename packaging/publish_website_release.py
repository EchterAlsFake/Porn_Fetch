"""Prepare CI build artifacts and publish an independent website release.

No application/update-feed changes. --dry-run prepares files and a manifest only.
Uses the standard library; tokens are never arguments or printed.
"""

import argparse
import gzip
import hashlib
import http.client
import io
import json
import os
import re
import shutil
import subprocess
import tarfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlsplit

NAME = re.compile(
    r"PornFetch_(linux|windows|macos|android)_(GUI|CLI)_(arm64-v8a|armeabi-v7a|x86_64|x64|arm64|x86|x32|riscv64|universal)(_Setup)?(_LEGAL)?(?:\.(?:zip|dmg|exe|run|bin|apk))?",
    re.I,
)
ARCH = {"arm64-v8a": "arm64", "armeabi-v7a": "armv7", "x86_64": "x64"}
MIN_OS = {
    "windows": "Windows 10 or later",
    "macos": "macOS 14.4 or later",
    "linux": "Compatible Linux system",
    "android": "Android 9.0 or later (API 28)",
}


def classify(name):
    match = NAME.fullmatch(name)
    if not match:
        return None
    platform, kind, arch, setup, legal = match.groups()
    platform, arch = platform.lower(), arch.lower()
    kind = "notices" if legal else "installer" if setup else "apk" if name.lower().endswith(".apk") else kind.lower()
    return dict(
        platform=platform, arch=ARCH.get(arch, arch), kind=kind, experimental=bool(setup), min_os=MIN_OS[platform]
    )


def add_file(path, attributes, output, artifacts):
    destination = output / path.name
    if destination.exists():
        raise ValueError(f"Duplicate website artifact: {path.name}")
    if path != destination:
        shutil.copyfile(path, destination)
    with destination.open("rb") as source:
        digest = hashlib.file_digest(source, "sha256").hexdigest()
    artifacts.append(dict(attributes, filename=path.name, size=destination.stat().st_size, sha256=digest))


def cli_bundle(directory, output, timestamp):
    """Bundle the executable with its helpers/notices, restoring Unix permissions."""
    destination = output / (directory.name + ".zip")
    if destination.exists():
        raise ValueError("Duplicate CLI bundle")
    executable = directory.name + (".exe" if "_windows_" in directory.name.lower() else "")
    if not (directory / executable).is_file():
        raise ValueError(f"CLI executable missing from {directory.name}")
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(directory.rglob("*")):
            if path.is_symlink():
                raise ValueError("Artifact directories cannot contain symlinks")
            if not path.is_file() or path.name.endswith(".sha256"):
                continue
            info = zipfile.ZipInfo.from_file(path, path.relative_to(directory))
            info.date_time = datetime.fromtimestamp(timestamp, timezone.utc).timetuple()[:6]
            if path.name in {executable, "pocketbase", "ffmpeg"}:
                info.external_attr = 0o100755 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            with path.open("rb") as source, archive.open(info, "w") as target:
                shutil.copyfileobj(source, target, length=1024 * 1024)
    return destination


def source_bundle(root, output, version, timestamp):
    """Archive tracked source only, including the workflow-stamped version file."""
    raw = output / ".source.tar"
    destination = output / f"PornFetch_source_{version}.tar.gz"
    try:
        with raw.open("wb") as stream:
            subprocess.run(["git", "archive", "--format=tar", "HEAD"], cwd=root, stdout=stream, check=True)
        with (
            raw.open("rb") as stream,
            tarfile.open(fileobj=stream, mode="r|") as original,
            destination.open("wb") as compressed,
            gzip.GzipFile(fileobj=compressed, mode="wb", mtime=timestamp) as gz,
            tarfile.open(fileobj=gz, mode="w|") as archive,
        ):
            for member in original:
                data = original.extractfile(member) if member.isfile() else None
                if member.name == "src/shared/version.py":
                    stamped = (root / member.name).read_bytes()
                    member.size = len(stamped)
                    data = io.BytesIO(stamped)
                member.name = f"porn-fetch-{version}/" + member.name
                member.mtime = timestamp
                archive.addfile(member, data)
    finally:
        raw.unlink(missing_ok=True)
    return destination


def prepare(artifact_root, output, version, channel, timestamp, commit, notes, source_root=None):
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError("Use an empty website output directory")
    artifacts = []
    for directory in sorted(artifact_root.iterdir()):
        if directory.name.endswith(".sha256") or directory.name.startswith("IFW_repo_"):
            continue
        if directory.is_symlink() or not directory.is_dir():
            raise ValueError("Expected downloaded artifact directories")
        target = classify(directory.name)
        if target and target["kind"] == "cli":
            bundle = cli_bundle(directory, output, timestamp)
            # add_file normally copies; the generated bundle already lives here.
            with bundle.open("rb") as source:
                digest = hashlib.file_digest(source, "sha256").hexdigest()
            artifacts.append(dict(target, filename=bundle.name, size=bundle.stat().st_size, sha256=digest))
            for legal in directory.glob("*_LEGAL.zip"):
                add_file(legal, dict(target, kind="notices"), output, artifacts)
            continue
        found = False
        for path in sorted(directory.iterdir()):
            if path.is_symlink():
                raise ValueError("Artifact directories cannot contain symlinks")
            attributes = classify(path.name)
            if path.is_file() and attributes:
                add_file(path, attributes, output, artifacts)
                found = True
        if not found:
            raise ValueError(f"No recognized release package in {directory.name}")
    if not artifacts:
        raise ValueError("No built application artifacts to publish")
    if source_root:
        source = source_bundle(source_root, output, version, timestamp)
        with source.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        artifacts.append(
            dict(
                platform="any",
                arch="any",
                kind="source",
                experimental=False,
                min_os="Release-specific Python dependencies; mobile setup differs",
                filename=source.name,
                size=source.stat().st_size,
                sha256=digest,
            )
        )
    manifest = dict(
        schema=1,
        version=version,
        channel=channel,
        commit=commit,
        published_at=datetime.fromtimestamp(timestamp, timezone.utc).isoformat(),
        notes=notes,
        artifacts=sorted(artifacts, key=lambda item: item["filename"]),
    )
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def send(origin, method, path, token, payload=None, byte_range=False):
    parsed = urlsplit(origin)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Website origin must be an HTTPS origin")
    connection = http.client.HTTPSConnection(parsed.hostname, parsed.port, timeout=900)
    try:
        connection.putrequest(method, path)
        if token:
            connection.putheader("Authorization", "Bearer " + token)
        if byte_range:
            connection.putheader("Range", "bytes=0-0")
        if payload is not None:
            size = payload.stat().st_size if isinstance(payload, Path) else len(payload)
            connection.putheader("Content-Length", str(size))
            connection.putheader(
                "Content-Type", "application/octet-stream" if isinstance(payload, Path) else "application/json"
            )
        connection.endheaders()
        if isinstance(payload, Path):
            with payload.open("rb") as source:
                while chunk := source.read(1024 * 1024):
                    connection.send(chunk)
        elif payload is not None:
            connection.send(payload)
        response = connection.getresponse()
        data = response.read(1024 * 1024)
        expected = {206} if byte_range else {200, 201}
        if response.status not in expected:
            raise RuntimeError(f"Website publishing request failed (HTTP {response.status})")
        if byte_range and len(data) != 1:
            raise RuntimeError("Published download failed range verification")
        return data
    finally:
        connection.close()


def publish(origin, token, output, manifest):
    version = quote(manifest["version"], safe="")
    result = json.loads(send(origin, "POST", "/ci/website-releases", token, json.dumps(manifest).encode()))
    if not result["published"]:
        for artifact in manifest["artifacts"]:
            name = quote(artifact["filename"], safe="")
            send(origin, "PUT", f"/ci/website-releases/{version}/files/{name}", token, output / artifact["filename"])
    send(origin, "POST", f"/ci/website-releases/{version}/publish", token, b"{}")
    catalog = json.loads(send(origin, "GET", f"/download/catalog.json?version={version}", ""))
    if not any(item["version"] == manifest["version"] for item in catalog["releases"]):
        raise RuntimeError("Published release is absent from the website catalog")
    for artifact in manifest["artifacts"]:
        name = quote(artifact["filename"], safe="")
        path = f"/downloads/{version}/{name}"
        checksum = send(origin, "GET", path + ".sha256", "").decode("ascii").split()[0]
        if checksum != artifact["sha256"]:
            raise RuntimeError("Published checksum differs from the prepared release")
        send(origin, "GET", path, "", byte_range=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--version", required=True)
    parser.add_argument("--channel", choices=("stable", "beta"), default="beta")
    parser.add_argument("--timestamp", type=int, required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--notes", type=Path, required=True)
    parser.add_argument("--origin", default="https://pornfetch.to")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    manifest = prepare(
        args.artifacts,
        args.output,
        args.version,
        args.channel,
        args.timestamp,
        args.commit,
        args.notes.read_text(encoding="utf-8"),
        args.source_root,
    )
    if not args.dry_run:
        token = os.environ.get("WEBSITE_RELEASE_TOKEN", "")
        if not token:
            raise SystemExit("WEBSITE_RELEASE_TOKEN is required")
        publish(args.origin, token, args.output, manifest)
    print(
        f"Prepared {len(manifest['artifacts'])} website artifacts for {args.version}"
        + (" (dry run)" if args.dry_run else "; published and verified")
    )


if __name__ == "__main__":
    main()
