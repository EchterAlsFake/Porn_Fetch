# iOS build sources

Start with the [iOS overview](../docs/iOS.md) and
[build guide](../docs/ios/BUILDING.md).

| Location | Purpose |
| --- | --- |
| `device/` | arm64/iOS 15 Qt/PySide, native dependencies, FFmpeg, signing and deployment |
| `device/patches/` | Qt compatibility and base_api FFmpeg dispatch patches |
| `device/app/main.py` | Device launcher; application source is staged from the main repository |
| `pornfetch/` | Intel simulator dependency builds, vendor preparation and application launcher |
| `qt/`, `native/` | Small Qt/Python and UIKit simulator probes |
| `results/` | Selected recorded checks from 2026-10-28; not results of a new build |
| `device/BUILD-REVISIONS.json` | Device source revisions and artifact hashes |
| `pornfetch/native-build-manifest.json` | Native dependency archive hashes |
| `HOST-ENVIRONMENT.json` | Recorded host tool versions |
| `snapshot-assets.json`, `SHA256SUMS*`, `SNAPSHOT-CONTENTS.json` | Original archive inventory and integrity metadata |

Generated application source copies, build logs, kits, vendor packages, wheels,
and generated projects are excluded from the maintained tree. The
[original snapshot](../docs/ios/SNAPSHOT.md) retains the full historical lab.
The scripts still require that lab's macOS toolchain and dependency inputs;
a clone alone does not contain a complete iOS SDK or bootstrap environment.
