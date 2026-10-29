import concurrent.futures
import os
from pathlib import Path
import subprocess

port = Path(__file__).resolve().parent
source = port / "native/selectolax-src/selectolax-1.0.2"
build = port / "native/selectolax-build"
build.mkdir(exist_ok=True)
developer = Path(os.environ.get("DEVELOPER_DIR", "/Users/asuna/Downloads/Xcode.app/Contents/Developer"))
clang = developer / "Toolchains/XcodeDefault.xctoolchain/usr/bin/clang"
sdk = developer / "Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk"
headers = Path('/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework/ios-arm64_x86_64-simulator/Python.framework/Headers')
flags = [str(clang), '-target', 'x86_64-apple-ios18.0-simulator', '-isysroot', str(sdk),
         '-O2', '-fPIC', '-std=c99', '-DLEXBOR_STATIC', '-I', str(headers),
         '-I', str(source / 'lexbor/source')]
sources = [source / 'selectolax/lexbor.c'] + [
    p for p in (source / 'lexbor/source').rglob('*.c')
    if 'ports' not in p.parts or 'posix' in p.parts
]
def compile_one(path):
    output = build / (str(path.relative_to(source)).replace('/', '_') + '.o')
    subprocess.run(flags + ['-c', str(path), '-o', str(output)], check=True)
    return output
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    objects = list(pool.map(compile_one, sources))
response = build / 'objects.txt'
response.write_text('\n'.join(str(p) for p in objects))
target = port / 'native/packages/selectolax'
target.mkdir(exist_ok=True)
subprocess.run(flags + ['-dynamiclib', '-undefined', 'dynamic_lookup',
                       '@' + str(response), '-o', str(target / 'lexbor.cpython-315-iphonesimulator.so')], check=True)
print(f'Built selectolax from {len(objects)} source files')
