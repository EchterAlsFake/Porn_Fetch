"""TUF-verified Android downloads. Installation is delegated to Android itself."""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

from tuf.ngclient import Updater

from .release import ROOT_FILE, release_time, update_eligibility
from .service_transport import ServiceFetcher

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


def updater(settings, progress=None):
    cache = android_private() / "verified-updates"
    metadata, targets = cache / "metadata", cache / "targets"
    metadata.mkdir(parents=True, exist_ok=True, mode=0o700)
    targets.mkdir(exist_ok=True, mode=0o700)
    fetcher = ServiceFetcher(settings)
    fetcher.on_chunk = progress
    return Updater(str(metadata), REPOSITORY + "metadata/", str(targets), REPOSITORY + "targets/",
                   fetcher=fetcher, bootstrap=ROOT_FILE.read_bytes())


def check(settings, current):
    info = platform_info()
    client = updater(settings)
    target = client.get_targetinfo("android/" + info["abi"] + ".apk")
    if target is None:
        return None
    custom = target.custom or {}
    version = custom.get("version", "")
    def parts(value):
        return tuple(int(part) for part in value.split("."))
    if custom.get("package") != info["package"] or custom.get("abi") != info["abi"]:
        raise ValueError("Android update does not match this application")
    if parts(version) <= parts(current):
        return None
    return {**custom, "release_timestamp": release_time(custom.get("release_timestamp")),
            "source": "signed_android", "release_url": "https://pornfetch.to/download/android",
            "changelog_format": "markdown"}


def download_and_request_install(settings, current, license_status, progress=None, cancel=None):
    def on_chunk(size):
        if cancel is not None and cancel.is_set():
            raise InterruptedError("Android update cancelled")
        if progress:
            progress(size)
    info = platform_info()
    client = updater(settings, on_chunk)
    target = client.get_targetinfo("android/" + info["abi"] + ".apk")
    if target is None:
        raise ValueError("No signed Android update available")
    custom = target.custom or {}
    if custom.get("abi") != info["abi"] or custom.get("package") != info["package"]:
        raise ValueError("Android update has the wrong identity")
    if tuple(map(int, custom["version"].split("."))) <= tuple(map(int, current.split("."))):
        raise ValueError("The Android update is not newer")
    entitled, reason = update_eligibility(license_status, release_time(custom.get("release_timestamp")))
    if not entitled:
        raise PermissionError(reason)
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
