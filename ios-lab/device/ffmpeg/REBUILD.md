# Rebuild and replace the iOS FFmpeg extension

The iOS app uses FFmpeg's libavformat, libavcodec and libavutil, statically
linked into `_ios_ffmpeg.cpython-315-iphoneos.so`. Those libraries retain the
LGPL-2.1-or-later terms in `COPYING.LGPLv2.1`. The application license does not
restrict modification of these libraries or debugging their replacement.

This bundle contains the complete FFmpeg source archive, its recorded hash,
the actual build's configuration headers and flags, the bridge sources, and
the build script. `build.json` identifies the corresponding native extension.
The bridge sources and build instructions are also available in the application's
source release at <https://github.com/EchterAlsFake/Porn_Fetch>.

On an ARM64 Mac with Xcode, use the application source for the release you
received. Download the matching `python-3.15.0rc2-iOS-XCframework.tar.gz` and
`SHA256SUMS` from the public toolchain release at
<https://github.com/EchterAlsFake/PySide6-to-iOS/releases/tag/6.12.0-ios15-cp315>,
verify the archive against that checksum list, and extract it. Rebuilding this
extension and replacing it in your existing IPA does not need the private lab
snapshot, an original app signing key or a premium credential.

1. Place the included archive at `ios-lab/device/artifacts/ffmpeg-9.0.2.tar.xz`
   in that checkout. Extract it into `ios-lab/device/ffmpeg/`, then make your
   changes in `ffmpeg-9.0.2/`.
2. Set `DEVELOPER_DIR` to your Xcode directory and `IOS_PYTHON_XCFRAMEWORK`
   to the absolute path of the extracted `Python.xcframework`.
3. Remove any previous `ios-lab/device/ffmpeg/build/` directory, then run
   `python3 ios-lab/device/build-ffmpeg.py`. It builds the libraries and links
   your replacement bridge extension from source. Apple SDK libraries are
   provided by Xcode. For changes to the bridge itself, edit `bridge.c` or
   `apple-probe.m` before this step.
4. Extract your existing IPA as a ZIP archive into an empty `unpacked/`
   directory. Python's iOS framework loader uses a `.fwork` text file to locate
   the extension binary. Replace that binary using the following script from
   the application checkout:

   ```python
   import shutil
   from pathlib import Path

   app = next(Path("unpacked/Payload").glob("*.app")).resolve()
   marker, = (app / "packages").glob("_ios_ffmpeg*.fwork")
   target = (app / marker.read_text().strip()).resolve()
   assert target.is_relative_to(app / "Frameworks") and target.is_file()
   replacement = Path("ios-lab/device/native/packages/_ios_ffmpeg.cpython-315-iphoneos.so")
   shutil.copyfile(replacement, target)
   ```

   Leave the `.fwork` marker, framework metadata and all other app files in
   place. Repack the `Payload/` directory as a ZIP with an `.ipa` extension,
   then use a sideloading tool that re-signs the app and its embedded frameworks
   with your own identity. The unchanged interface of the extension is
   `PyInit__ios_ffmpeg`; preserve it when making compatible replacements.

Alternatively, restage and rebuild the full application using `docs/iOS.md`;
staging copies your rebuilt extension from `device/native/packages/` into the app.

The source archive hash check identifies the original upstream source. Modify
the extracted sources after that check; the build script does not overwrite an
existing extracted tree. If you distribute modified libraries, retain the LGPL
notices, identify your changes and provide their corresponding source as required
by the LGPL.
