import os
from pathlib import Path
import subprocess
from cffi import FFI

port = Path(__file__).resolve().parent
source = port / 'native/curl-cffi-src/curl_cffi-0.17.0'
libcurl = port / 'native/libcurl-ios'
build = port / 'native/curl-wrapper-build'
build.mkdir(exist_ok=True)
ffi = FFI()
ffi.cdef((source / 'ffi/cdef.c').read_text())
ffi.set_source('curl_cffi._wrapper', '#include "shim.h"')
generated = build / 'wrapper.c'
ffi.emit_c_code(str(generated))
developer = Path(os.environ.get('DEVELOPER_DIR', '/Users/asuna/Downloads/Xcode.app/Contents/Developer'))
sdk = developer / 'Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk'
headers = Path('/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework/ios-arm64_x86_64-simulator/Python.framework/Headers')
out = port / 'native/packages/curl_cffi'
out.mkdir(exist_ok=True)
command = [str(developer / 'Toolchains/XcodeDefault.xctoolchain/usr/bin/clang'),
           '-target', 'x86_64-apple-ios18.0-simulator', '-isysroot', str(sdk),
           '-O2', '-dynamiclib', '-undefined', 'dynamic_lookup',
           '-I', str(headers), '-I', str(source / 'ffi'), '-I', str(libcurl / 'include'),
           str(generated), str(source / 'ffi/shim.c'), str(libcurl / 'libcurl-impersonate.a'),
           '-lc++', '-lz', '-liconv', '-lresolv',
           '-framework', 'Security', '-framework', 'SystemConfiguration',
           '-framework', 'CoreFoundation', '-framework', 'Network',
           '-Wl,-exported_symbol,_PyInit__wrapper',
           '-o', str(out / '_wrapper.cpython-315-iphonesimulator.so')]
subprocess.run(command, check=True)
print('Built curl-cffi wrapper for the Intel iOS simulator')
