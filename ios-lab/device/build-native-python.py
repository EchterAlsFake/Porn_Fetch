"""Build ARM64/iOS 15 extensions without modifying simulator artifacts."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import subprocess

from cffi import FFI

device = Path(__file__).resolve().parent
source_root = device.parent / "pornfetch/native"
native = device / "native"
packages = native / "packages"
packages.mkdir(parents=True, exist_ok=True)
developer = Path(os.environ.get("DEVELOPER_DIR", "/Users/asuna/Downloads/Xcode.app/Contents/Developer"))
clang = developer / "Toolchains/XcodeDefault.xctoolchain/usr/bin/clang"
sdk = developer / "Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk"
headers = Path("/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework/ios-arm64/Python.framework/Headers")
flags = [str(clang), "-target", "arm64-apple-ios15.0", "-isysroot", str(sdk), "-O2", "-fPIC", "-I", str(headers)]
link = ["-dynamiclib", "-undefined", "dynamic_lookup"]
suffix = ".cpython-315-iphoneos.so"

def run(args):
    subprocess.run(args, check=True)

chomp = source_root / "chompjs-src/chompjs-1.4.1/_chompjs"
run(flags + link + [str(chomp / f"{name}.c") for name in ("module", "parser", "buffer")]
    + ["-o", str(packages / ("_chompjs" + suffix))])
ffi_prefix = native / "libffi-ios"
run(flags + link + ["-I", str(ffi_prefix / "include"), "-DFFI_BUILDING=1", "-DUSE__THREAD", "-DHAVE_SYNC_SYNCHRONIZE",
    "-DFFI_AVAILABLE_APPLE=1", "-DFFI_EXEC_TRAMPOLINE_TABLE=1",
    str(source_root / "cffi-src/cffi-2.1.1/src/c/_cffi_backend.c"), str(ffi_prefix / "lib/libffi.a"),
    "-o", str(packages / ("_cffi_backend" + suffix))])

curl_source = source_root / "curl-cffi-src/curl_cffi-0.17.0"
curl_build = native / "curl-wrapper-build"
curl_build.mkdir(exist_ok=True)
ffi = FFI()
ffi.cdef((curl_source / "ffi/cdef.c").read_text())
ffi.set_source("curl_cffi._wrapper", '#include "shim.h"')
generated = curl_build / "wrapper.c"
ffi.emit_c_code(str(generated))
curl_out = packages / "curl_cffi"
curl_out.mkdir(exist_ok=True)
curl = native / "libcurl-ios"
run(flags + link + ["-I", str(curl_source / "ffi"), "-I", str(curl / "include"), str(generated),
    str(curl_source / "ffi/shim.c"), str(curl / "libcurl-impersonate.a"),
    "-lc++", "-lz", "-liconv", "-lresolv", "-framework", "Security", "-framework", "SystemConfiguration",
    "-framework", "CoreFoundation", "-framework", "Network", "-Wl,-exported_symbol,_PyInit__wrapper",
    "-o", str(curl_out / ("_wrapper" + suffix))])

selecto = source_root / "selectolax-src/selectolax-1.0.2"
selecto_build = native / "selectolax-build"
selecto_build.mkdir(exist_ok=True)
selecto_flags = flags + ["-std=c99", "-DLEXBOR_STATIC", "-I", str(selecto / "lexbor/source")]
sources = [selecto / "selectolax/lexbor.c"] + sorted(
    p for p in (selecto / "lexbor/source").rglob("*.c") if "ports" not in p.parts or "posix" in p.parts)

def compile_one(path):
    output = selecto_build / (str(path.relative_to(selecto)).replace("/", "_") + ".o")
    if not output.exists() or output.stat().st_mtime < path.stat().st_mtime:
        run(selecto_flags + ["-c", str(path), "-o", str(output)])
    return output

with ThreadPoolExecutor(max_workers=2) as pool:
    objects = list(pool.map(compile_one, sources))
response = selecto_build / "objects.txt"
response.write_text("\n".join(str(p) for p in objects))
selecto_out = packages / "selectolax"
selecto_out.mkdir(exist_ok=True)
run(selecto_flags + link + ["@" + str(response), "-o", str(selecto_out / ("lexbor" + suffix))])
print(f"Built ARM64/iOS 15 cffi, chompjs, curl-cffi, selectolax ({len(objects)} C sources)")
