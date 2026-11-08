"""Stage the proven real app with device extensions and generate its project."""
import configparser
import json
import os
import plistlib
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib

device = Path(__file__).resolve().parent
lab = device.parent
deploy_venv = Path(os.environ.get('IOS_DEPLOY_VENV', lab / '.venv'))
repo = Path(os.environ.get('PORN_FETCH_SOURCE',
    lab.parent if (lab.parent / 'pyproject.toml').is_file() else lab.parent / 'Porn_Fetch'))
app = device / "app"
vendor = device / "vendor"
shutil.rmtree(app / 'src', ignore_errors=True)
shutil.copytree(repo / "src", app / "src", dirs_exist_ok=True,
    ignore=shutil.ignore_patterns("__pycache__", "tests", "screenshots", "resources.py"))
shutil.copytree(lab / "pornfetch/vendor", vendor, dirs_exist_ok=True,
    ignore=shutil.ignore_patterns("__pycache__", "*.so", "*.fwork"))
shutil.copytree(device / "native/packages", vendor, dirs_exist_ok=True)
# The archived overlay predates PyJWT. Install its pure Python wheel explicitly;
# resolving dependencies here could replace the matching iOS native packages.
requirements = tomllib.loads((repo / "pyproject.toml").read_text())["project"]["dependencies"]
pyjwt_requirement = next(requirement for requirement in requirements if re.match(r"(?i)^pyjwt\b", requirement))
subprocess.run([str(deploy_venv / "bin/python"), "-m", "pip", "install", "--disable-pip-version-check",
                "--no-deps", "--only-binary=:all:", "--platform", "any", "--python-version", "3.15",
                "--upgrade", "--target", str(vendor), pyjwt_requirement], check=True)
subprocess.run([sys.executable, str(device / "patch-ios-ffmpeg.py")], check=True)
subprocess.run([str(deploy_venv / "bin/pyside6-rcc"), "--binary", str(repo / "src/frontend/resources.qrc"),
                "-o", str(app / "src/frontend/resources.rcc")], check=True)
if "--stage-only" in sys.argv:
    print("Staged real app source, resources, patched QtAsyncio, and ARM64 native extensions")
    raise SystemExit(0)

config = configparser.ConfigParser()
config.read(device / "python-qt-hello/pysidedeploy.spec")
config["app"].update(title="PornFetch", input_file=str(app / "main.py"), project_dir=str(app))
config["app"]["icon"] = ""
config["qt"]["modules"] = "Core,Gui,Network,Qml,Quick,QuickControls2,OpenGL,Svg"
config["qt"]["qml_files"] = ",".join(str(p.relative_to(app)) for p in (app / "src/frontend/UI").rglob("*.qml"))
config["ios"].update(bundle_id="local.asuna.PornFetch", deployment_target="15.0",
    wheel_pyside=str(device / "wheels/pyside6-6.12.0-6.12.0-cp315-cp315-ios_arm64.whl"),
    wheel_shiboken=str(device / "wheels/shiboken6-6.12.0-6.12.0-cp315-cp315-ios_arm64.whl"))
for key in ("wheel_pyside", "wheel_shiboken"):
    if not Path(config["ios"][key]).is_file():
        raise SystemExit(f"Missing Python 3.15 device wheel: {config['ios'][key]}")
if os.environ.get("IOS_PYTHON_XCFRAMEWORK"):
    config["ios"]["xcframework_path"] = os.environ["IOS_PYTHON_XCFRAMEWORK"]
if os.environ.get("IOS_APP_VERSION"):
    config["ios"]["version"] = os.environ["IOS_APP_VERSION"]
config_path = app / "pysidedeploy.spec"
with config_path.open("w") as stream:
    config.write(stream)
output = app / "deployment/ios_arm64"
cache = output / "_wheels"
if cache.exists():
    shutil.rmtree(cache)
env = os.environ.copy()
if not env.get("DEVELOPER_DIR"):
    env["DEVELOPER_DIR"] = subprocess.check_output(["xcode-select", "-p"], text=True).strip()
env["PATH"] = str(deploy_venv / "bin") + os.pathsep + env.get("PATH", "")
subprocess.run([str(deploy_venv / "bin/pyside6-ios-deploy"), "-c", str(config_path)],
               cwd=app, env=env, check=True)
project = output / "PornFetch.xcodeproj/project.pbxproj"
# Keep both visible and internal bundle versions aligned with the shared release.
# Qt's generator otherwise hardcodes CFBundleVersion to "1".
plist_path = output / "Info.plist"
info = plistlib.loads(plist_path.read_bytes())
info["CFBundleShortVersionString"] = config["ios"]["version"]
info["CFBundleVersion"] = config["ios"]["version"]
plist_path.write_bytes(plistlib.dumps(info))
text = project.read_text()
# Qt's iOS generator leaves its Resources phase empty, even with an app icon
# configured. Attach the opaque icon catalog so Xcode generates every device size.
catalog = output / "Assets.xcassets"
shutil.copytree(app / "src/frontend/graphics/ios/Assets.xcassets", catalog, dirs_exist_ok=True)
icon_file_id = "AF1000000000000000000001"
icon_build_id = "AF1000000000000000000002"
for section, entry in (
    ("PBXFileReference", f'{icon_file_id} /* Assets.xcassets */ = {{isa = PBXFileReference; '
     'lastKnownFileType = folder.assetcatalog; path = Assets.xcassets; sourceTree = SOURCE_ROOT; };'),
    ("PBXBuildFile", f'{icon_build_id} /* Assets.xcassets in Resources */ = {{isa = PBXBuildFile; '
     f'fileRef = {icon_file_id}; }};'),
):
    marker = f"/* End {section} section */"
    if text.count(marker) != 1:
        raise SystemExit(f"Generated iOS project is missing {section}")
    text = text.replace(marker, f"\t\t{entry}\n{marker}")
text, icon_phases = re.subn(
    r"(isa = PBXResourcesBuildPhase;.*?files = \()",
    rf"\g<1>\n\t\t\t\t{icon_build_id} /* Assets.xcassets in Resources */,",
    text, flags=re.S,
)
if icon_phases != 1:
    raise SystemExit("Generated iOS project must have one Resources phase")
pattern = r'(/\* Copy Python Packages \*/ = \{.*?shellScript = )("(?:\\.|[^"\\])*");'
match = re.search(pattern, text, re.S)
if not match:
    raise SystemExit("Generated bundle copy phase missing")
script = (f'set -e\nrsync -a --delete --exclude="__pycache__/" "{app}/src/" '
          '"$CODESIGNING_FOLDER_PATH/src/"\n'
          f'cp "{app}/main.py" "$CODESIGNING_FOLDER_PATH/main.py"\n'
          f'/bin/bash "{device}/bundle-vendor.sh"\n'
          f'"{sys.executable}" "{repo}/packaging/check_ios_app.py" "$CODESIGNING_FOLDER_PATH"\n')
project.write_text(text[:match.start(2)] + json.dumps(script) + text[match.end(2):])

# The notification bridge uses the existing Qt event loop and Apple's local
# notifications framework. Compile the generated entry point as Objective-C++.
notification_source = app / "src/backend/native/ios_notifications.mm"
if notification_source.is_file():
    candidates = [p for p in output.rglob("main.*") if p.suffix in {".cpp", ".mm"} and "_wheels" not in p.parts]
    if len(candidates) != 1:
        raise SystemExit("Cannot locate the generated iOS entry point for notifications")
    entry = candidates[0]
    entry.write_text(entry.read_text() + '\n#include "' + str(notification_source) + '"\n')
    if entry.suffix != ".mm":
        entry.rename(entry.with_suffix(".mm"))
    text = project.read_text().replace("main.cpp", "main.mm")
    text = text.replace("sourcecode.cpp.cpp", "sourcecode.cpp.objcpp")
    # Inherit all deployment link flags while linking the native notification API.
    def add_notification_framework(match):
        value = match.group(2).strip()
        if value.startswith("("):
            value = '("-framework", "UserNotifications", ' + value[1:]
        else:
            value = '("$(inherited)", "-framework", "UserNotifications", ' + value + ')'
        return match.group(1) + value + ";"
    text = re.sub(r'(OTHER_LDFLAGS\s*=\s*)(\([^;]*\)|"(?:\\.|[^"\\])*"|[^;]+);',
                  add_notification_framework, text)
    if "UserNotifications" not in text:
        text = text.replace("buildSettings = {", 'buildSettings = {\nOTHER_LDFLAGS = ("$(inherited)", "-framework", "UserNotifications");')
    project.write_text(text)
print(project)
