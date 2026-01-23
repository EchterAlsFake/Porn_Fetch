#!/usr/bin/env python3
"""
patch_app_bundle.py

Patch a macOS .app bundle (built by Nuitka or similar) with recommended Info.plist
settings + Sparkle 2 keys.

Usage example:
  python3 patch_app_bundle.py \
    --app "dist/Porn Fetch.app" \
    --bundle-id "me.echteralsfake.pornfetch" \
    --display-name "Porn Fetch" \
    --short-version "2.1" \
    --feed-url "https://echteralsfake.me/appcast.xml" \
    --public-ed-key "haYqwZA03OrYQUrP0tBrBye6Sk+UXObkR+yb0rAK5TQ=" \
    --sparkle-framework "/path/to/Sparkle.framework" \
    --bridge-dylib "/path/to/sparkle_bridge.dylib" \
    --adhoc-sign
"""


import shutil
import argparse
import plistlib
import subprocess
from pathlib import Path


def compute_build_version(short_version: str) -> str:
    """
    Convert "1.0" / "2.1" / "1.10.3" into a monotonically increasing integer-like string.
    Examples:
      1.0     -> 10000
      1.9     -> 10900
      2.0     -> 20000
      2.1     -> 20100
      1.10.3  -> 11003
    """
    parts = short_version.strip().split(".")
    nums = [int(p) for p in parts if p != ""]
    while len(nums) < 3:
        nums.append(0)
    major, minor, patch = nums[:3]
    return str(major * 10000 + minor * 100 + patch)


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
    app = "Porn Fetch.app"
    bundle_id = "me.echteralsfake.pornfetch"
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

    build_version = compute_build_version(args.short_version)

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
    print(f"  CFBundleIdentifier           = {data.get('CFBundleIdentifier')}")
    print(f"  CFBundleShortVersionString   = {data.get('CFBundleShortVersionString')}")
    print(f"  CFBundleVersion              = {data.get('CFBundleVersion')}")
    print(f"  SUFeedURL                    = {data.get('SUFeedURL')}")
    print(f"  SUPublicEDKey                = {data.get('SUPublicEDKey')}")
    print(f"  SUEnableAutomaticChecks      = {data.get('SUEnableAutomaticChecks')}")
    print(f"  SUScheduledCheckInterval     = {data.get('SUScheduledCheckInterval')}")
    print(f"  SUAllowsAutomaticUpdates     = {data.get('SUAllowsAutomaticUpdates')}")
    print(f"  SUAutomaticallyUpdate        = {data.get('SUAutomaticallyUpdate')}")

    # 3) Optional ad-hoc sign
    if args.adhoc_sign:
        print("\n🔐 Ad-hoc signing the app (no Developer ID required)…")
        run(["/usr/bin/codesign", "--force", "--deep", "--sign", "-", str(app)])
        run(["/usr/bin/codesign", "--verify", "--deep", "--strict", str(app)])
        print("✅ codesign verification OK")

    print("\nDone.")


if __name__ == "__main__":
    main()
