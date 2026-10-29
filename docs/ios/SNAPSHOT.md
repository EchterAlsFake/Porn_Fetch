# Restoring the original iOS build inputs

The original experiment is preserved at branch
`ios/iphone7-port-snapshot-2026-10-28`, tag
`ios-iphone7-snapshot-2026-10-28`, commit `d0b2029`.
The associated **draft GitHub release** contains the full lab. Draft access
requires repository collaborator permissions; this is not a public app release.
The draft and its nine asset names were checked during documentation cleanup.

The archive includes compiled Qt kits, patched Qt/PySide sources, wheels, native
builds, dependency overlays, virtual environments, Rust toolchains, generated
projects, app bundles, logs and the official cached CPython iOS framework.
The maintained Git tree contains first-party recipes, patches and selected
evidence only. A clone alone is insufficient to reproduce this build.

## Download and verify

Install the GitHub CLI, GnuPG and zstd, authenticate `gh` with an account that
can read the draft, then download into an empty directory:

```sh
gh release download ios-iphone7-snapshot-2026-10-28 \
  --repo EchterAlsFake/Porn_Fetch --dir ios-snapshot
cd ios-snapshot
gpg --verify SHA256SUMS.asc SHA256SUMS
shasum -a 256 -c SHA256SUMS
cat ios-lab-full-snapshot.tar.zst.part-* | zstd -d | tar -xf -
```

Import the signer's public key through your trusted channel before verifying.
The recorded fingerprint is
`7082BBFF855D47C6BB13C3BF6AC58B8CA26D1C5F` (Johannes Habel).
On Linux, `sha256sum -c SHA256SUMS` can replace `shasum`.

The four numbered parts are **one** zstd-compressed tar archive; concatenate
them in filename order. Compressed size is about 7.43 GB and the archived file
contents total about 21.16 GB. Allow additional disk space for downloads,
extraction, the current checkout, Xcode and rebuilding. All part sizes and hashes
are in [`snapshot-assets.json`](../../ios-lab/snapshot-assets.json).

Extraction produces:

```text
ios-lab/
python-ios/3.15.0rc2/
```

Keep an untouched extracted copy if you need the historical state. For a baseline
rebuild, place these trees at the original macOS paths without overwriting an
existing lab:

```text
/Users/asuna/ios-lab/
/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/
```

For example, if neither destination exists:

```sh
test ! -e /Users/asuna/ios-lab && mv ios-lab /Users/asuna/ios-lab
mkdir -p /Users/asuna/.pyside6_ios/Python-iOS
test ! -e /Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2 && \
  mv python-ios/3.15.0rc2 /Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2
```

The original paths appear in generated projects, venv shebangs and native build
configuration. Restoring elsewhere requires updating those paths and rebuilding
or regenerating affected components. The snapshot's macOS tools and iOS binaries
cannot build or run natively on Linux.

## What must be supplied separately

- Xcode and Apple SDKs; the baseline used Xcode 26.3, SDK 26.2.
- macOS, host Python 3.13 and host tools. See
  [`HOST-ENVIRONMENT.json`](../../ios-lab/HOST-ENVIRONMENT.json) for recorded versions.
- Simulator runtime and devices; CoreSimulator data is not archived.
- The current Porn Fetch checkout and maintained lab scripts; overlay those and
  regenerate the app project as described in [Building](BUILDING.md).
- Your phone SSH identity and `ios-lab/ssh/config`, using alias `ios-phone`.

Xcode, the macOS VM, Homebrew's installation tree, personal GitHub/GPG settings,
private SSH keys and downloaded media are excluded. Selected reports retain
hashes and decode results with media names/URLs redacted. See
[`SNAPSHOT-CONTENTS.json`](../../ios-lab/SNAPSHOT-CONTENTS.json) for the original
archive policy; its source-view count describes the historical export rather
than the cleaned tree. The full inventory is the release's `snapshot-manifest.json`.

The release's `GITHUB-SNAPSHOT.md` is the original handoff. Its historical
instructions may be superseded by the maintained [build guide](BUILDING.md).
