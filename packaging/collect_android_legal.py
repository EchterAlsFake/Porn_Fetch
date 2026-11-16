"""Collect Android notices from target staging and native recipe sources."""
import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from collect_legal import NOTICE_NAMES, collect_legal  # noqa: E402


def collect(project: Path, abi: str, output: Path) -> Path:
    build = project / '.buildozer/android/platform' / f'build-{abi}'
    packages = build / 'build/python-installs/app' / abi
    if not list(packages.glob('*.dist-info/METADATA')):
        raise FileNotFoundError(f'Android target metadata missing: {packages}')
    # Native recipes do not necessarily install dist-info notices.
    native = output / 'native'
    for source in sorted((build / 'build/other_builds').rglob('*')):
        if source.is_file() and source.name.lower().startswith(NOTICE_NAMES):
            relative = source.relative_to(build / 'build/other_builds')
            destination = native / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    pocketbase = project / 'native/pocketbase/build' / abi / 'legal'
    # PocketBase's generated build output is also embedded as APK assets.
    assets = build / 'dists/app/src/main/assets/pocketbase-legal'
    if assets.is_dir():
        shutil.copytree(assets, native / 'pocketbase', dirs_exist_ok=True)
    elif pocketbase.is_dir():
        shutil.copytree(pocketbase, native / 'pocketbase', dirs_exist_ok=True)
    else:
        raise FileNotFoundError('Embedded PocketBase notices missing from Android staging')
    return collect_legal(output, distribution_paths=[packages])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--abi', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(collect(Path(__file__).resolve().parents[1], args.abi, args.output))
