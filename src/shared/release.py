"""Authenticated release metadata shared by packaging and update clients."""
import re
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from tuf.api.metadata import Metadata, Root, Targets

ROOT_FILE = Path(__file__).resolve().parents[1] / "cli/update_root.json"


def validate_ifw_packages(xml, version, release_timestamp):
    """Bind every supported IFW component to the same authenticated release."""
    core = "to.pornfetch.echteralsfake"
    allowed = {core, f"{core}.ffmpeg", f"{core}.pocketbase"}
    packages = xml.findall("PackageUpdate")
    names = [package.findtext("Name") for package in packages]
    date = datetime.fromtimestamp(release_timestamp, timezone.utc).strftime("%Y-%m-%d")
    if (core not in names or len(names) != len(set(names)) or not set(names) <= allowed
            or any(package.findtext("Version") != version or package.findtext("ReleaseDate") != date
                   for package in packages)
            or xml.find("RepositoryUpdate") is not None):
        raise ValueError("Qt repository components do not match the authenticated release")


def release_time(value):
    if type(value) is not int or value <= 0:
        raise ValueError("Release timestamp is missing or invalid")
    return value


def safe_repo_path(value):
    path = PurePosixPath(value)
    # IFW preserves spaces in directory archive names, such as Porn Fetch.app.7z.
    if (not value or path.is_absolute() or str(path) != value
            or any(p in (".", "..") for p in path.parts)
            or not re.fullmatch(r"[A-Za-z0-9_./+~ -]+", value)):
        raise ValueError(f"Unsafe release repository path: {value!r}")
    return value


def verify_repository_manifest(blob, root_bytes, target_platform):
    root = Metadata[Root].from_bytes(root_bytes)
    metadata = Metadata[Targets].from_bytes(blob)
    root.signed.verify_delegate("targets", metadata.signed_bytes, metadata.signatures)
    if root.signed.is_expired() or metadata.signed.is_expired():
        raise ValueError("Release metadata needs refreshing")
    release = metadata.signed.unrecognized_fields["release"]
    release_time(release["release_timestamp"])
    if release["platform"] != target_platform or not re.fullmatch(r"\d+(?:\.\d+)+", release["version"]):
        raise ValueError("Release does not match this platform")
    if "Updates.xml" not in metadata.signed.targets:
        raise ValueError("Release repository has no Updates.xml")
    for name in metadata.signed.targets:
        safe_repo_path(name)
    return metadata, release


def update_eligibility(status, released):
    release_time(released)
    date = datetime.fromtimestamp(released, timezone.utc).strftime("%d %B %Y")
    if status.entitled_to(released):
        return True, f"Released {date}. This update is included in your entitlement."
    if status.license_expires_at is not None and released > status.license_expires_at:
        end = datetime.fromtimestamp(status.license_expires_at, timezone.utc).strftime("%d %B %Y")
        return False, f"Released {date}. Your update entitlement ended on {end}. Renew to receive this update. Your current installation is unchanged."
    return False, f"Released {date}. Validate a production license before installing this update."
