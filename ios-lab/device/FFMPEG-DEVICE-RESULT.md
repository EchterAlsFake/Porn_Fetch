# FFmpeg on the physical iPhone 7

FFmpeg 9.0.2 is bundled inside PornFetch as a small CPython extension, `_ios_ffmpeg`, linked with libavformat, libavcodec and libavutil. It runs entirely in the app and copies the encoded streams into faststart MP4. No subprocess, external FFmpeg installation, video encoder, network protocol, new entitlement or global jailbreak change is required.

## Build and integration

- Official source: `https://ffmpeg.org/releases/ffmpeg-9.0.2.tar.xz`.
- Source SHA-256: `8c3850283eb25fa026482078a04051e0be17347b09ef81a0849bec15a96e002e`, matching the application's pinned build.
- Target: arm64 / minimum iOS 15.0, Xcode 26.3 / iPhoneOS 26.2 SDK.
- LGPL 2.1 or later; GPL/version3/nonfree/network disabled. No encoders. Original source archive, static libraries and bridge source are retained locally; license/configuration files are included in the app's packages/ffmpeg-legal directory.
- Build: `build-ffmpeg.py`, C bridge `ffmpeg/bridge.c`, native playback check `ffmpeg/apple-probe.m`. Extension is approximately 1.68 MiB.
- Python adapter: `native/packages/ios_ffmpeg.py`. Supports stream-copy remux, metadata and JPEG/PNG cover art. Tagging rewrites a temporary MP4 and replaces the original only on success.
- `patch-ios-ffmpeg.py` makes three small, iOS-only dispatch changes to the staged base_api FFmpeg module; patch saved as `patches/base-api-ios-ffmpeg.patch`. Upstream desktop paths are retained. `prepare-application.py` reapplies this after staging vendor packages.
- The shared application's existing FFmpeg detection now enables normal HLS remuxing. The provider library already calls its remux operation through `asyncio.to_thread`; the extension additionally releases the Python GIL during media I/O.
- `process_dylibs` packages the extension into the usual signed iOS framework. No simulator artifacts are changed.

## Physical device result

Evidence: `../build/ffmpeg-phone-result.json`.

- User's downloaded file: 445,108,800 bytes, MPEG-TS, H.264 1280×720 at 30 fps, AAC audio, about 17m15s. Original retained unchanged.
- Before: AVFoundation reports not readable, not playable, no tracks.
- Remux: 4.893 seconds on the iPhone 7. Result before cover metadata: 431,414,383 bytes.
- After: AVFoundation reports readable/playable and successfully decodes a video sample and an audio sample. Duration 1034.733333 seconds.
- Second pass: metadata plus generated generic PNG cover art successfully written; native audio/video decoding still passes.
- Application's `FORCE_DISABLE_AV` is false.
- Converted copy: Files → PornFetch → PornFetch → `Remuxed video.mp4`.

Independent validation of the complete resulting file passed (`../build/phone-remuxed-integrity.json`). All 31,040 video frames, 44,562 audio frames and the PNG cover decoded successfully: zero corrupt packets, zero decoding errors and zero timestamp regressions. MP4 box lengths are valid; the `moov` index precedes `mdat` (faststart). Final size is 431,414,546 bytes, SHA-256 `d58e4a194eac8a08136c6af72b22f721da7f5075d42b1bb14da843bde531b5d5`. PyAV logged one timescale warning while probing the file with attached cover art; native playback sample decoding and complete independent decoding both passed. The diagnostic report retains that warning.

The user confirmed that `Remuxed video.mp4` plays with video and sound in Files. The user also completed a fresh download through the app and confirmed that it was successfully remuxed automatically. This confirms the real UI download → automatic remux → playable MP4 workflow on the physical iPhone 7.

The one-shot diagnostic `ios_remux_check.py` runs only when explicitly queued with an `ios-remux-job.json` in the app's working directory. It consumes that job, retains the original input, writes a JSON result and does not fetch media or contact providers. Normal launches do not run it.

## Rebuild

Run as the macOS user asuna, after the source archive above is available in `artifacts`:

```sh
cd /Users/asuna/ios-lab/device
/usr/local/bin/python3 build-ffmpeg.py
/usr/local/bin/python3 prepare-application.py --stage-only
sh build-application.sh > ../build/device-app-ffmpeg-build.log 2>&1
sh deploy-app.sh PornFetch
```

`--stage-only` reuses the already generated Xcode project. For initial generation, use `prepare-application.py` without that flag. Install updates preserve the app's data container and downloads. The deploy script stops both native and Python launcher process names before replacing its own app bundle.

Transcoding and codecs beyond the configured remux formats are outside this build. iOS background transfers remain unverified.
