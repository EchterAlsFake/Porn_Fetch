#!/usr/bin/env python3
"""
This script will basically generate the correct Info.plist file for macOS. The Info.plist file needs special
changes like the public key for sparkle, version and bundle identifier and so on.

I could of course manually copy this each time, but why not using a script to make my life simpler yk
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

import shutil
import argparse
import plistlib
import subprocess
from src.backend.config import __bundle_id__


def load_plist(plist_path: Path) -> dict:
    with plist_path.open("rb") as f:
        return plistlib.load(f)


def save_plist(plist_path: Path, data: dict) -> None:
    with plist_path.open("wb") as f:
        plistlib.dump(data, f, sort_keys=False)


def copy_into_frameworks(app: Path, sparkle_framework: Path | None, bridge_dylib: Path | None) -> None:
    frameworks_dir = app / "Contents" / "Frameworks"
    frameworks_dir.mkdir(parents=True, exist_ok=True)

    if sparkle_framework:
        dest = frameworks_dir / "Sparkle.framework"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(sparkle_framework, dest, symlinks=True)

    if bridge_dylib:
        dest = frameworks_dir / bridge_dylib.name
        shutil.copy2(bridge_dylib, dest)


def run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if proc.returncode != 0:
        print(proc.stdout)
        raise SystemExit(f"Command failed: {' '.join(cmd)}")
    if proc.stdout.strip():
        print(proc.stdout.strip())


def main() -> None:
    app = "PornFetch_Universal.app"
    bundle_id = __bundle_id__
    display_name = "Porn Fetch"
    feed_url = "https://echteralsfake.me/appcast.xml"
    public_ed_key = "haYqwZA03OrYQUrP0tBrBye6Sk+UXObkR+yb0rAK5TQ="
    sparkle_framework = "src/backend/sparkle/Sparkle.framework"
    bridge_dylib = "src/backend/sparkle/sparkle_bridge.dylib"

    ap = argparse.ArgumentParser()
    ap.add_argument("--category", default="public.app-category.utilities",
                    help="LSApplicationCategoryType value")
    ap.add_argument("--short-version", required=True, help='Human version, e.g. "2.1" or "1.0.0"')
    # Sparkle behavior
    ap.add_argument("--enable-auto-checks", action="store_true", default=True,
                    help="Enable automatic background checks (default on)")
    ap.add_argument("--scheduled-interval", type=int, default=86400,
                    help="Seconds between automatic checks (default 86400 = 1 day)")
    ap.add_argument("--allow-auto-updates", action="store_true", default=True,
                    help="Allow user to opt into automatic installs")
    ap.add_argument("--show-release-notes", action="store_true", default=True,
                    help="Show release notes/changelog when available")

    args = ap.parse_args()
    app = Path(app).expanduser().resolve()
    plist_path = app / "Contents" / "Info.plist"

    if not app.exists() or not plist_path.exists():
        raise SystemExit(f"Invalid app bundle or missing Info.plist: {plist_path}")

    build_version = args.short_version

    # 1) Copy Sparkle.framework + bridge dylib (optional)
    sparkle_framework = Path(sparkle_framework).expanduser().resolve()
    bridge_dylib = Path(bridge_dylib).expanduser().resolve()
    copy_into_frameworks(app, sparkle_framework, bridge_dylib)

    # 2) Patch Info.plist
    data = load_plist(plist_path)

    # Better general macOS metadata
    data["CFBundleIdentifier"] = bundle_id
    data["CFBundleDisplayName"] = display_name
    data["CFBundleName"] = display_name

    data["CFBundleShortVersionString"] = args.short_version
    data["CFBundleVersion"] = build_version

    data["LSApplicationCategoryType"] = args.category
    data["NSHighResolutionCapable"] = True

    # Sparkle required
    data["SUFeedURL"] = feed_url
    data["SUPublicEDKey"] = public_ed_key

    # Sparkle UX defaults
    data["SUEnableAutomaticChecks"] = bool(args.enable_auto_checks)
    data["SUScheduledCheckInterval"] = int(args.scheduled_interval)
    data["SUAllowsAutomaticUpdates"] = bool(args.allow_auto_updates)
    data["SUShowReleaseNotes"] = bool(args.show_release_notes)

    save_plist(plist_path, data)

    # Validate plist syntax
    run(["/usr/bin/plutil", "-lint", str(plist_path)])

    print("\n✅ Patched Info.plist values:")
    print(f"CFBundleIdentifier           = {data.get('CFBundleIdentifier')}")
    print(f"CFBundleShortVersionString   = {data.get('CFBundleShortVersionString')}")
    print(f"CFBundleVersion              = {data.get('CFBundleVersion')}")
    print(f"SUFeedURL                    = {data.get('SUFeedURL')}")
    print(f"SUPublicEDKey                = {data.get('SUPublicEDKey')}")
    print(f"SUEnableAutomaticChecks      = {data.get('SUEnableAutomaticChecks')}")
    print(f"SUScheduledCheckInterval     = {data.get('SUScheduledCheckInterval')}")
    print(f"SUAllowsAutomaticUpdates     = {data.get('SUAllowsAutomaticUpdates')}")
    print(f"SUAutomaticallyUpdate        = {data.get('SUAutomaticallyUpdate')}")

if __name__ == "__main__":
    main()
