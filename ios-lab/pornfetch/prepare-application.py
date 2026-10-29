"""Stage real application source and customize Qt's generated bundle phase."""
import configparser
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

port = Path(__file__).resolve().parent
lab = port.parent
repo = Path(os.environ.get('PORN_FETCH_SOURCE',
    lab.parent if (lab.parent / 'pyproject.toml').is_file() else lab.parent / 'Porn_Fetch'))
app = port / 'app'
env = os.environ.copy()
env.setdefault('DEVELOPER_DIR', '/Users/asuna/Downloads/Xcode.app/Contents/Developer')
env['PATH'] = str(lab / '.venv/bin') + ':/usr/local/bin:/usr/bin:/bin'

# Preserve the repository's generated resources.py; the binary resource file
# is generated independently for this bundle.
shutil.rmtree(app / 'src', ignore_errors=True)
shutil.copytree(repo / 'src', app / 'src', dirs_exist_ok=True,
                ignore=shutil.ignore_patterns('__pycache__', 'tests', 'screenshots', 'resources.py'))
subprocess.run([str(lab / '.venv/bin/pyside6-rcc'), '--binary',
                str(repo / 'src/frontend/resources.qrc'),
                '-o', str(app / 'src/frontend/resources.rcc')], check=True)

# Apply the existing application's asyncio patch to an isolated iOS overlay,
# using the embedded interpreter's version rather than the host's version.
qtasyncio = port / 'vendor/PySide6/QtAsyncio'
kit = lab / 'qt/deployment/ios_x86_64_simulator/_wheels'
shutil.copytree(kit / 'PySide6/QtAsyncio', qtasyncio, dirs_exist_ok=True)
spec = importlib.util.spec_from_file_location('ios_qtasyncio_patch', repo / 'scripts/patch_qtasyncio.py')
patcher = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = patcher
spec.loader.exec_module(patcher)
target = patcher.EnvironmentInfo(target=port, python=Path(sys.executable), prefix=port,
                                pyside_version='6.12.0', python_version=(3, 15, 0),
                                events_path=qtasyncio / 'events.py', futures_path=qtasyncio / 'futures.py',
                                tasks_path=qtasyncio / 'tasks.py')
for change in patcher.build_changes(target, force=False):
    change.path.write_text(change.modified)

output = app / 'deployment/ios_x86_64_simulator'
output.mkdir(parents=True, exist_ok=True)
if not (output / '_wheels').exists():
    (output / '_wheels').symlink_to(kit, target_is_directory=True)
config_path = app / 'pysidedeploy.spec'
config = configparser.ConfigParser()
config.read(lab / 'qt/pysidedeploy.spec')
config['app']['title'] = 'PornFetch'
config['app']['input_file'] = str(app / 'main.py')
config['app']['project_dir'] = str(app)
config['qt']['modules'] = 'Core,Gui,Qml,Quick,QuickControls2,Widgets,Network,Svg'
config['qt']['qml_files'] = ','.join(str(p.relative_to(app)) for p in (app / 'src/frontend/UI').glob('*.qml'))
config['ios']['bundle_id'] = 'to.pornfetch.ioslab'
with config_path.open('w') as f:
    config.write(f)
subprocess.run([str(lab / '.venv/bin/pyside6-ios-deploy'), '-c', str(config_path)],
               cwd=app, env=env, check=True)

project = output / 'PornFetch.xcodeproj/project.pbxproj'
text = project.read_text()
pattern = r'(/\* Copy Python Packages \*/ = \{.*?shellScript = )("(?:\\.|[^"\\])*");'
match = re.search(pattern, text, re.S)
if not match:
    raise SystemExit('Generated copy phase not found')
# Copy the complete real source tree, QML, resource files and data, preserving
# paths. Qt's default QML copy phase flattens nested folders.
script = (f'set -e\nrsync -a --delete --exclude="__pycache__/" "{app}/src/" '
          '"$CODESIGNING_FOLDER_PATH/src/"\n'
          f'cp "{app}/main.py" "$CODESIGNING_FOLDER_PATH/main.py"\n'
          f'/bin/bash "{port}/bundle-vendor.sh"\n')
text = text[:match.start(2)] + json.dumps(script) + text[match.end(2):]
project.write_text(text)
print(project)
