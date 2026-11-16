"""Release selection policy shared by every frontend and release publisher."""
import re

CHANNELS = ("stable", "beta")


def validate_channel(channel):
    if channel not in CHANNELS:
        raise ValueError("Update channel must be stable or beta")
    return channel


def eligible_channels(channel):
    return CHANNELS if validate_channel(channel) == "beta" else ("stable",)


def version_parts(version):
    if not isinstance(version, str) or not re.fullmatch(r"[0-9]+(?:\.[0-9]+)+", version):
        raise ValueError(f"Invalid release version: {version!r}")
    parts = [int(part) for part in version.split(".")]
    while len(parts) > 1 and parts[-1] == 0:
        parts.pop()
    return tuple(parts)


def validate_release(release, channel):
    """Bind authenticated metadata to the repository it was requested from."""
    if release.get("channel") != validate_channel(channel):
        raise ValueError("Signed release does not match the requested channel")
    version_parts(release.get("version"))
    return release


def newest(releases):
    return max(releases, key=lambda item: (version_parts(item["version"]), item["channel"] == "stable"), default=None)
