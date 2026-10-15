# Minimal FFmpeg builds

Official desktop builds compile FFmpeg 9.0.2 for each native Linux, macOS, and
Windows x64/ARM64 runner. No third-party precompiled FFmpeg binaries are downloaded.
The source URL and SHA-256 are pinned in `packaging/build_ffmpeg.py`; the shared
configure profile lives in `packaging/ffmpeg_configure_flags.txt`.

The profile explicitly disables GPL, version-3 and nonfree code, external codec
libraries, networking, device capture, assembly optimizations, and all encoders.
FFmpeg's libraries are linked into the separate FFmpeg executable, not into Porn
Fetch. Linux/macOS use system C/math/zlib libraries. Windows uses Clang's MinGW
runtime and static zlib, without MSYS runtime DLLs.

Enabled formats and operations:

- MPEG-TS and MOV/MP4 input, MP4 output, and local-file access.
- H.264, HEVC, AAC, MPEG audio/video, AV1 and VP9 bitstream parsing, with the
  required AAC/extradata bitstream filters and dependencies selected by FFmpeg.
- MP4 metadata and JPEG/PNG attached pictures through the image2 demuxer.
- AAC, JPEG and PNG decoders for probing sample rates, channel layouts and image
  dimensions. They are necessary even for stream-copy operations; no encoders
  or audio-transcoding fallback are provided.

The initial Linux x64 build measured about 2.1 MiB for the stripped executable.
Other platforms/compiler versions can differ. The full corresponding source
archive and notices add space to the distribution; the executable size is not
an estimate for the entire installer.

## Build locally

From the synced project environment:

```bash
uv run --no-sync python packaging/build_ffmpeg.py --dest third_party
```

Linux requires a C compiler, GNU make, Bash, pkg-config and zlib headers
(`build-essential pkg-config zlib1g-dev` on Ubuntu). macOS uses the Xcode Command
Line Tools. For Windows, run from MSYS2 CLANG64/CLANGARM64 with Python/uv on PATH;
install `make diffutils pkgconf`, the matching `mingw-w64-clang-*-toolchain`, and
`mingw-w64-clang-*-zlib` packages. Build on the target architecture; this script
does not cross-compile.

On Windows, add `--msys2-root C:/msys64` (or your actual installation directory).
The builder uses that installation's Bash and make explicitly and prepends its
Clang tools to the build environment. CI obtains this path from the MSYS2 action.

`--work-dir`, `--jobs`, and `--source-archive` customize the working directory,
parallelism, or a local source archive. Local archives must match the pinned hash.
The old `scripts/fetch_ffmpeg.py` and `packaging/fetch_ffmpeg.py` entry points run
this same source builder.

## Distribution and verification

`third_party/ffmpeg-legal/` contains the unchanged source archive, FFmpeg license
texts, configure invocation, generated configuration headers, version report,
and source/binary hashes. Windows also includes the statically linked zlib's
header containing its license. Portable bundles include this directory, and
`collect_legal.py` includes it in each GUI release's legal ZIP. The IFW installer
includes the legal ZIP. The universal macOS legal bundle records both builds.
FFmpeg retains its own LGPL terms; the application's custom license does not
cover it. See [FFmpeg's licensing guidance](https://ffmpeg.org/legal.html).

Every native FFmpeg CI build runs the offline media checks against its resulting
executable. These remux a procedural H.264/AAC TS fixture, check faststart and
stream presence, and rewrite MP4 tags with both JPEG and PNG covers:

```bash
PORN_FETCH_TEST_FFMPEG=third_party/ffmpeg uv run --no-sync python -m unittest src.tests.unit.test_ffmpeg
```

The normal unit suite skips these media checks unless the executable is explicitly
selected. User-selected system FFmpeg remains supported through `PATH` or
`PORN_FETCH_FFMPEG_BINARY`.
