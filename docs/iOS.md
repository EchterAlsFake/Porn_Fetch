# iOS port

Porn Fetch has an experimental GUI port verified on an **iPhone 7 (arm64),
iOS 15.8.8, with palera1n rootless**, on 2026-10-28. The user confirmed the
interface, downloads, automatic MP4 remuxing, and video/audio playback in Files.
An Intel iOS simulator build was also verified.

There is no public iOS installer or iOS CI release target. The device build uses
jailbreak signing and a patched Qt kit; ordinary iPhone installation and App Store
distribution have not been established. Other devices have not been tested.

- [Build and deploy](ios/BUILDING.md): restore the build inputs, generate an Xcode
  project, build the app, and install it on the tested device; separate simulator
  and dependency rebuild instructions.
- [Implementation and validation](ios/ARCHITECTURE.md): platform handling, Qt
  compatibility patches, native extensions, FFmpeg, evidence, and remaining work.
- [Original build snapshot](ios/SNAPSHOT.md): authenticated download, integrity
  verification, and restoration of the preserved macOS lab.
- [Build sources](../ios-lab/README.md): scripts, patches, probes, and manifests.

## Verified scope

| Capability | Physical iPhone 7 | Intel simulator |
| --- | --- | --- |
| Real backend and mobile QML interface | Confirmed by user | Confirmed |
| Qt Quick rendering and touch | Metal rendering; five recorded button taps | OpenGL CPU rendering in the tested VM |
| Native parsers, CFFI, verified HTTPS, asynchronous HTTPS, cryptography | Passed dependency probes | Passed dependency probes |
| Real media download | Confirmed by user | User download independently decoded |
| Automatic FFmpeg remux to playable MP4 | Confirmed by user | Adapter not integrated |
| Metadata and PNG cover art | Passed device check | Not validated |

The device build embeds **CPython 3.15.0rc2 and Qt/PySide 6.12.0**. The repository's
normal Python requirement remains `>=3.14,<3.15`; the lab stages dependencies
separately. A successful port experiment does not extend that supported range.

Background transfers, memory-pressure behavior, account flows, and the complete
application regression suite remain unverified on iOS. Desktop tracking, browser
cookie extraction, installer/updater, and Tor workflows are not provided as
validated iOS features. See the implementation notes for the precise limits.

The old jailbreak CLI experiment used Python 3.12 and an earlier dependency stack.
It is superseded by this GUI port and is not a build method for the current source.
