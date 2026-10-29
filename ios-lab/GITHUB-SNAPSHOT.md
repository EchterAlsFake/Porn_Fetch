# iPhone 7 port: complete experimental handoff

Branch: `ios/iphone7-port-snapshot-2026-10-28`  
Snapshot tag: `ios-iphone7-snapshot-2026-10-28`  
Repository: `EchterAlsFake/Porn_Fetch`

This preserves the successful macOS VM experiment rather than a cleaned-up production port. Porn Fetch runs on a real iPhone 7 (`iPhone9,1`) with iOS 15.8.8 and palera1n rootless. The user confirmed smooth UI operation, downloads, video/audio playback in Files, and automatic FFmpeg remuxing of a fresh download. The Intel iOS simulator build is preserved too.

## Where everything is

This branch contains the application adjustment in `src/backend/application.py` and an inspectable copy of the lab's first-party scripts, patches, deployment specifications, diagnostics, reports and earlier experiments under `ios-lab/`. Start with:

- [Device build and deployment](device/PORN-FETCH-DEVICE-RESULT.md)
- [FFmpeg integration and full-file integrity results](device/FFMPEG-DEVICE-RESULT.md)
- [Device source revisions and artifact hashes](device/BUILD-REVISIONS.json)
- [Qt/Python device build notes](device/README.md)
- [Original simulator notes](pornfetch/README.md)
- [Original full lab notes](README.md)

The **full lab snapshot is attached to a draft GitHub release**, tagged `ios-iphone7-snapshot-2026-10-28`. It preserves the compiled Qt kits, patched Qt/PySide sources, all native builds, wheels, vendor packages, virtual environments, Rust toolchains, generated Xcode projects, app bundles, intermediate files, logs and experiments. The official cached CPython iOS framework is included separately inside the same archive. Large artifacts are release assets because GitHub limits individual Git blobs to 100 MB and pushes to 2 GiB. This avoids adding gigabytes of compiled output to every clone.

Draft releases are visible to repository collaborators with the necessary access. Use the authenticated GitHub CLI or the repository's Releases page; nothing here publishes a new production release or changes `master`.

`SNAPSHOT-CONTENTS.json` summarizes the included data and every intentional exclusion/redaction. The complete file inventory is `snapshot-manifest.json` among the release assets. `snapshot-assets.json` and `SHA256SUMS` identify the downloadable parts. `SHA256SUMS.asc`, the commit and the tag are signed by Johannes Habel, GPG fingerprint `7082BBFF855D47C6BB13C3BF6AC58B8CA26D1C5F`, email `EchterAlsFake@proton.me`.

## Download and restore on Linux

Log in with `gh auth login` if needed, then:

```sh
gh release download ios-iphone7-snapshot-2026-10-28 \
  --repo EchterAlsFake/Porn_Fetch --dir ios-snapshot
cd ios-snapshot
gpg --verify SHA256SUMS.asc SHA256SUMS
sha256sum -c SHA256SUMS
cat ios-lab-full-snapshot.tar.zst.part-* | zstd -d | tar -xf -
```

Import your existing public GPG key on that machine before verification if necessary. The files are split parts of **one** compressed tar archive; concatenate all parts in their numbered order before extraction. macOS can verify hashes with `shasum -a 256 -c SHA256SUMS`. An ordinary Git clone alone contains the inspectable source view; download the release assets for the complete build state.

Extraction creates:

```text
ios-lab/                 # complete lab, build output included
python-ios/3.15.0rc2/    # cached official Python.xcframework and testbed
```

The scripts and generated projects deliberately retain their original absolute paths, mostly `/Users/asuna/ios-lab`, `/Users/asuna/Porn_Fetch`, `/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2` and `/Users/asuna/Downloads/Xcode.app`. For an immediate macOS restore, place the extracted directories at those locations. On your regular machine, inspect/refactor the paths before rebuilding. macOS tools and iOS binaries in this snapshot do not run natively on Linux; Linux is suitable for browsing and cleaning up the port.

Xcode/Apple SDKs, the macOS VM itself, CoreSimulator device data, Homebrew's installation tree, personal GitHub/GPG configuration, private SSH keys and downloaded videos are outside this handoff. Reinstall Xcode 26.3, Python 3.13 and the host build tools before rebuilding. Establish your own phone SSH identity/configuration at `ios-lab/ssh/config`; the scripts expect the host alias `ios-phone`. No passwords are in the export. Public cryptographic test fixtures and license files in third-party source archives are retained.

## Important implementation details

- The host VM is Intel macOS 15.7.2; simulator and physical-device native builds are distinct.
- Embedded runtime: CPython 3.15.0rc2 and Qt/PySide 6.12.0. The desktop project's Python version remains unchanged.
- Qt 6.12 normally requires a newer iOS release. `device/patches/qtbase-ios15.patch` records the compatibility work for this experimental iOS 15 build, including the Mach semaphore fallback and availability checks.
- The app's GPU entitlement is necessary for the ad-hoc signed jailbreak app to obtain an Apple A10 Metal context. Earlier black-screen failures and diagnostics are retained.
- FFmpeg 9.0.2 is an in-process CPython extension; it stream-copies local audio/video into faststart MP4 and handles metadata/cover art without launching a subprocess. Its source/configuration/license files and static build output are preserved.
- Raw download data is excluded. Integrity reports retain the hashes and decoding results; diagnostic download filenames and signed media URLs are redacted.
- Background downloads and memory-pressure behavior remain unverified.

`export-snapshot.py` documents the actual copy/archive policy. It never changes the working lab. This branch is intentionally a large, untidy handoff; the draft assets preserve the material that would be inconvenient to reconstruct after leaving this VM.
