#!/usr/bin/env python3

import argparse
import plistlib
import subprocess
from pathlib import Path

FEED_URL = "https://echteralsfake.me/appcast.xml"
PUBLIC_ED_KEY = "haYqwZA03OrYQUrP0tBrBye6Sk+UXObkR+yb0rAK5TQ="


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("app", type=Path)
    args = parser.parse_args()

    plist_path = args.app / "Contents" / "Info.plist"

    with plist_path.open("rb") as f:
        data = plistlib.load(f)

    data.update({
        "SUFeedURL": FEED_URL,
        "SUPublicEDKey": PUBLIC_ED_KEY,

        "SUEnableAutomaticChecks": True,
        "SUScheduledCheckInterval": 86400,
        "SUAllowsAutomaticUpdates": True,
        "SUShowReleaseNotes": True,
    })

    with plist_path.open("wb") as f:
        plistlib.dump(data, f, sort_keys=False)

    subprocess.run(
        ["/usr/bin/plutil", "-lint", str(plist_path)],
        check=True,
    )

    print("✅ Sparkle configuration added to Info.plist")


if __name__ == "__main__":
    main()