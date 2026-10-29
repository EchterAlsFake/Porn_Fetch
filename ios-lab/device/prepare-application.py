"""Stage the proven real app with device extensions and generate its project."""
import configparser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

device = Path(__file__).resolve().parent
lab = device.parent
repo = Path("/Users/asuna/Porn_Fetch")
app = device / "app"
vendor = device / "vendor"
shutil.copytree(repo / "src", app / "src", dirs_exist_ok=True,
    ignore=shutil.ignore_patterns("__pycache__", "tests", "screenshots", "resources.py"))
shutil.copytree(lab / "pornfetch/vendor", vendor, dirs_exist_ok=True,
    ignore=shutil.ignore_patterns("__pycache__", "*.so", "*.fwork"))
shutil.copytree(device / "native/packages", vendor, dirs_exist_ok=True)
subprocess.run([sys.executable, str(device / "patch-ios-ffmpeg.py")], check=True)
subprocess.run([str(lab / ".venv/bin/pyside6-rcc"), "--binary", str(repo / "src/frontend/resources.qrc"),
                "-o", str(app / "src/frontend/resources.rcc")], check=True)
if "--stage-only" in sys.argv:
    print("Staged real app source, resources, patched QtAsyncio, and ARM64 native extensions")
    raise SystemExit(0)

config = configparser.ConfigParser()
config.read(device / "python-qt-hello/pysidedeploy.spec")
config["app"].update(title="PornFetch", input_file=str(app / "main.py"), project_dir=str(app))
config["qt"]["modules"] = "Core,Gui,Network,Qml,Quick,QuickControls2,OpenGL,Svg"
config["qt"]["qml_files"] = ",".join(str(p.relative_to(app)) for p in (app / "src/frontend/UI").rglob("*.qml"))
config["ios"].update(bundle_id="local.asuna.PornFetch", deployment_target="15.0",
    wheel_pyside=str(next((device / "wheels").glob("pyside6-*.whl"))),
    wheel_shiboken=str(next((device / "wheels").glob("shiboken6-*.whl"))))
config_path = app / "pysidedeploy.spec"
with config_path.open("w") as stream:
    config.write(stream)
output = app / "deployment/ios_arm64"
cache = output / "_wheels"
if cache.exists():
    shutil.rmtree(cache)
env = os.environ.copy()
env["DEVELOPER_DIR"] = "/Users/asuna/Downloads/Xcode.app/Contents/Developer"
env["PATH"] = str(lab / ".venv/bin") + ":/usr/local/bin:/usr/bin:/bin"
subprocess.run([str(lab / ".venv/bin/pyside6-ios-deploy"), "-c", str(config_path)],
               cwd=app, env=env, check=True)
project = output / "PornFetch.xcodeproj/project.pbxproj"
text = project.read_text()
pattern = r'(/\* Copy Python Packages \*/ = \{.*?shellScript = )("(?:\\.|[^"\\])*");'
match = re.search(pattern, text, re.S)
if not match:
    raise SystemExit("Generated bundle copy phase missing")
script = (f'set -e\nrsync -a --delete --exclude="__pycache__/" "{app}/src/" '
          '"$CODESIGNING_FOLDER_PATH/src/"\n'
          f'cp "{app}/main.py" "$CODESIGNING_FOLDER_PATH/main.py"\n'
          f'/bin/bash "{device}/bundle-vendor.sh"\n')
project.write_text(text[:match.start(2)] + json.dumps(script) + text[match.end(2):])
print(project)
