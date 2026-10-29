"""Generate an isolated native probe using the already unpacked Qt kit."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

port = Path(__file__).resolve().parent
lab = port.parent
vendor = port / "vendor"
vendor.mkdir(exist_ok=True)
for source, name in [
    (port / "native/cffi-src/cffi-2.1.1/src/cffi", "cffi"),
    (port / "native/chompjs-src/chompjs-1.4.1/chompjs", "chompjs"),
    (lab / ".venv/lib/python3.13/site-packages/pycparser", "pycparser"),
    (port / "native/selectolax-src/selectolax-1.0.2/selectolax", "selectolax"),
    (port / "native/curl-cffi-src/curl_cffi-0.17.0/curl_cffi", "curl_cffi"),
    (lab / ".venv/lib/python3.13/site-packages/certifi", "certifi"),
    (port / "native/cryptography-src/cryptography-50.0.2/src/cryptography", "cryptography"),
]:
    shutil.copytree(source, vendor / name, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('*.c', '*.h', '*.pyx', '*.pxd', '*.pxi', '__pycache__'))
for package, version, directory in [
    ('curl_cffi', '0.17.0', 'curl-cffi-src/curl_cffi-0.17.0'),
    ('cryptography', '50.0.2', 'cryptography-src/cryptography-50.0.2'),
]:
    metadata = vendor / f'{package}-{version}.dist-info'
    metadata.mkdir(exist_ok=True)
    shutil.copy2(port / 'native' / directory / 'PKG-INFO', metadata / 'METADATA')
for binary in (port / "native/packages").rglob("*.so"):
    dest = vendor / binary.relative_to(port / "native/packages")
    dest.parent.mkdir(exist_ok=True, parents=True)
    shutil.copy2(binary, dest)
output = port / "probe/deployment/ios_x86_64_simulator"
output.mkdir(parents=True, exist_ok=True)
cache = output / "_wheels"
if not cache.exists():
    cache.symlink_to(lab / "qt/deployment/ios_x86_64_simulator/_wheels", target_is_directory=True)
env = os.environ.copy()
env["DEVELOPER_DIR"] = "/Users/asuna/Downloads/Xcode.app/Contents/Developer"
env["PATH"] = str(lab / ".venv/bin") + ":/usr/local/bin:/usr/bin:/bin"
subprocess.run([
    str(lab / ".venv/bin/pyside6-ios-deploy"), str(port / "probe/main.py"),
    "--name", "NativeProbe", "--bundle-id", "local.asuna.NativeProbe",
    "--wheel-pyside", str(next((lab / "wheels").glob("pyside6-*.whl"))),
    "--wheel-shiboken", str(next((lab / "wheels").glob("shiboken6-*.whl"))),
], cwd=port / "probe", env=env, check=True)
project = output / "NativeProbe.xcodeproj/project.pbxproj"
text = project.read_text()
pattern = r'(/\* Copy Python Packages \*/ = \{.*?shellScript = )("(?:\\.|[^"\\])*");'
match = re.search(pattern, text, re.S)
if not match:
    raise SystemExit("Generated project copy phase not found")
script = json.loads(match.group(2))
script += f'\n/bin/bash "{port}/bundle-vendor.sh"\n'
text = text[:match.start(2)] + json.dumps(script) + text[match.end(2):]
project.write_text(text)
print(project)
