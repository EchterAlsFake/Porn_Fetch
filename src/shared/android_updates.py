"""TUF-verified Android downloads. Installation is delegated to Android itself."""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

from tuf.api.exceptions import DownloadHTTPError
from tuf.ngclient import Updater

from .release import ROOT_FILE, release_time
from .service_transport import ServiceFetcher
from .update_channels import eligible_channels, newest, validate_channel, validate_release, version_parts

REPOSITORY = "https://pornfetch.to/repo/android/"


def is_android_device():
    return sys.platform == "android" or hasattr(sys, "getandroidapilevel") or bool(os.environ.get("ANDROID_ARGUMENT"))


def android_private():
    value = os.environ.get("ANDROID_PRIVATE")
    if not value:
        raise RuntimeError("Android app-private storage is unavailable")
    return Path(value)


def platform_info():
    value = json.loads((android_private() / "pornfetch-platform.json").read_text())
    if value.get("package") != "to.pornfetch.app" or value.get("abi") not in {"arm64-v8a", "armeabi-v7a", "x86", "x86_64"}:
        raise ValueError("Unsupported Android application identity")
    return value


def updater(settings, progress=None, *, channel="stable"):
    validate_channel(channel)
    repository = REPOSITORY + channel + "/"
    cache = android_private() / "verified-updates" / channel
    metadata, targets = cache / "metadata", cache / "targets"
    metadata.mkdir(parents=True, exist_ok=True, mode=0o700)
    targets.mkdir(exist_ok=True, mode=0o700)
    fetcher = ServiceFetcher(settings)
    fetcher.on_chunk = progress
    return Updater(str(metadata), repository + "metadata/", str(targets), repository + "targets/",
                   fetcher=fetcher, bootstrap=ROOT_FILE.read_bytes())


def check(settings, current, *, channel=None):
    info = platform_info()
    offers = []
    selected = channel or getattr(settings, "update_channel", "stable")
    for feed in eligible_channels(selected):
        client = updater(settings, channel=feed)
        try:
            target = client.get_targetinfo("android/" + info["abi"] + ".apk")
        except DownloadHTTPError as error:
            if error.status_code == 404:
                continue
            raise
        if target is None:
            continue
        custom = validate_release(target.custom or {}, feed)
        if custom.get("package") != info["package"] or custom.get("abi") != info["abi"]:
            raise ValueError("Android update does not match this application")
        if version_parts(custom["version"]) <= version_parts(current):
            continue
        offers.append({**custom, "release_timestamp": release_time(custom.get("release_timestamp")),
                       "download_size": target.length, "sha256": target.hashes["sha256"],
                       "source": "signed_android", "release_url": "https://pornfetch.to/download/android",
                       "changelog_format": "markdown"})
    return newest(offers)


def download_and_request_install(settings, current, progress=None, cancel=None, offer=None):
    """Report APK bytes and the signed total; metadata traffic is excluded."""
    downloaded = 0
    total = 0

    def on_chunk(size):
        nonlocal downloaded
        if cancel is not None and cancel.is_set():
            raise InterruptedError("Android update cancelled")
        if progress and total:
            downloaded += size
            progress(downloaded, total)
    info = platform_info()
    offer = offer or check(settings, current)
    if offer is None:
        raise ValueError("No signed Android update available")
    client = updater(settings, on_chunk, channel=offer["channel"])
    target = client.get_targetinfo("android/" + info["abi"] + ".apk")
    if target is None:
        raise ValueError("No signed Android update available")
    custom = validate_release(target.custom or {}, offer["channel"])
    if custom["version"] != offer["version"] or target.hashes["sha256"] != offer["sha256"]:
        raise ValueError("The published update changed. Check for updates again.")
    if custom.get("abi") != info["abi"] or custom.get("package") != info["package"]:
        raise ValueError("Android update has the wrong identity")
    if version_parts(custom["version"]) <= version_parts(current):
        raise ValueError("The Android update is not newer")
    release_time(custom.get("release_timestamp"))
    total = target.length
    if progress:
        progress(0, total)
    path = Path(client.download_target(target))
    if cancel is not None and cancel.is_set():
        raise InterruptedError("Android update cancelled")
    with path.open("rb") as source:
        target.verify_length_and_hashes(source)
    private = android_private()
    destination = private / "pornfetch-update.apk"
    with tempfile.NamedTemporaryFile(dir=private, delete=False) as staged:
        temporary = Path(staged.name)
        try:
            with path.open("rb") as source:
                shutil.copyfileobj(source, staged)
            staged.flush()
            os.fsync(staged.fileno())
            os.replace(temporary, destination)
        finally:
            temporary.unlink(missing_ok=True)
    command = {"version": custom["version"], "abi": info["abi"]}
    if cancel is not None and cancel.is_set():
        raise InterruptedError("Android update cancelled")
    temporary = private / ".install-update.json"
    temporary.write_text(json.dumps(command), encoding="utf-8")
    os.replace(temporary, private / "install-update.json")
