"""Build pinned LGPL FFmpeg libraries and a Python remux bridge for iOS 15."""
from pathlib import Path
import hashlib
import os
import re
import shutil
import subprocess
import tarfile

device = Path(__file__).resolve().parent
root = device / "ffmpeg"
archive = device / "artifacts/ffmpeg-9.0.2.tar.xz"
assert hashlib.sha256(archive.read_bytes()).hexdigest() == "8c3850283eb25fa026482078a04051e0be17347b09ef81a0849bec15a96e002e"
source = root / "ffmpeg-9.0.2"
if not source.exists():
    with tarfile.open(archive) as bundle:
        bundle.extractall(root, filter="data")
build = root / "build"
build.mkdir(exist_ok=True)
developer = Path("/Users/asuna/Downloads/Xcode.app/Contents/Developer")
tools = developer / "Toolchains/XcodeDefault.xctoolchain/usr/bin"
sdk = developer / "Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk"
flags = Path("/Users/asuna/Porn_Fetch/packaging/ffmpeg_configure_flags.txt").read_text().splitlines()
flags.remove("--enable-ffmpeg")
flags += ["--disable-avfilter", "--enable-cross-compile", "--target-os=darwin", "--arch=aarch64",
          f"--cc={tools / 'clang'}", f"--ar={tools / 'ar'}", f"--ranlib={tools / 'ranlib'}",
          f"--sysroot={sdk}", "--extra-cflags=-target arm64-apple-ios15.0 -fPIC",
          "--extra-ldflags=-target arm64-apple-ios15.0", "--enable-demuxer=image2pipe,png_pipe,jpeg_pipe"]
if not (build / "config.h").exists():
    subprocess.run([str(source / "configure"), *flags], cwd=build, check=True)
subprocess.run(["make", "-j6"], cwd=build, check=True)
configuration = (build / "config.h").read_text()
assert all(f"#define CONFIG_{name} 0" in configuration for name in ["GPL", "VERSION3", "NONFREE", "NETWORK"])
assert not re.search(r"^#define CONFIG_\w+_ENCODER 1$", (build / "config_components.h").read_text(), re.M)
headers = Path("/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework/ios-arm64/Python.framework/Headers")
output = device / "native/packages/_ios_ffmpeg.cpython-315-iphoneos.so"
subprocess.run([str(tools / "clang"), "-target", "arm64-apple-ios15.0", "-isysroot", str(sdk),
    "-O2", "-dynamiclib", "-undefined", "dynamic_lookup", "-I", str(headers), "-I", str(source),
    "-I", str(build), str(root / "bridge.c"), str(root / "apple-probe.m"), str(build / "libavformat/libavformat.a"),
    str(build / "libavcodec/libavcodec.a"), str(build / "libavutil/libavutil.a"),
    "-lz", "-liconv", "-framework", "CoreFoundation", "-framework", "Security",
    "-framework", "AVFoundation", "-framework", "CoreMedia", "-framework", "Foundation",
    "-framework", "CoreVideo", "-framework", "AudioToolbox",
    "-Wl,-exported_symbol,_PyInit__ios_ffmpeg", "-o", str(output)], check=True)
legal = device / "native/packages/ffmpeg-legal"
legal.mkdir(exist_ok=True)
for name in ["COPYING.LGPLv2.1", "LICENSE.md"]:
    shutil.copy2(source / name, legal / name)
for name in ["config.h", "config_components.h"]:
    shutil.copy2(build / name, legal / name)
(legal / "configuration.txt").write_text("\n".join(flags) + "\n")
print(f"Built {output}: {output.stat().st_size / 1024**2:.2f} MiB")
