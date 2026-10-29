"""Resolve the checked-in runtime graph for iOS, keeping native builds separate."""
from pathlib import Path
import os
import subprocess
import sys
import tomllib
from pip._vendor.packaging.markers import Marker, default_environment

port = Path(__file__).resolve().parent
lab = port.parent
repo = Path(os.environ.get('PORN_FETCH_SOURCE',
    lab.parent if (lab.parent / 'pyproject.toml').is_file() else lab.parent / 'Porn_Fetch'))
lock = tomllib.loads((repo / 'uv.lock').read_text())
packages = {p['name']: p for p in lock['package']}
root = packages['porn-fetch']
environment = default_environment()
environment.update(sys_platform='ios', platform_system='iOS', platform_machine='x86_64',
                   python_version='3.15', python_full_version='3.15.0', extra='')
# Browser extraction is desktop-only and imported lazily by the real backend.
separate = {'browser-cookie3', 'cffi', 'chompjs', 'cryptography', 'curl-cffi',
            'selectolax', 'shiboken6'}
seen = set()
queue = list(root.get('dependencies', [])) + root.get('optional-dependencies', {}).get('gui', [])
requirements = []
while queue:
    dependency = queue.pop()
    name = dependency['name']
    if name in seen or (dependency.get('marker') and not Marker(dependency['marker']).evaluate(environment)):
        continue
    seen.add(name)
    if name in separate or name.startswith('pyside6'):
        continue
    package = packages[name]
    requirements.append(f'{name}=={package["version"]}')
    queue.extend(package.get('dependencies', []))
requirements_file = port / 'pure-requirements.txt'
requirements_file.write_text('\n'.join(sorted(requirements)) + '\n')
subprocess.run([sys.executable, '-m', 'pip', 'install', '--disable-pip-version-check',
                '--no-deps', '--only-binary=:all:', '--platform', 'any',
                '--python-version', '3.15', '--upgrade', '--target', str(port / 'vendor'),
                '-r', str(requirements_file)], check=True)
