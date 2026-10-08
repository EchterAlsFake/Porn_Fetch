#!/usr/bin/env python3
"""Add --buildozer-file and remove the Python 3.11 gate in PySide6 Android deploy.

Usage: python scripts/patch_android_deploy.py .venv [--dry-run | --verify | --restore]
Reapply after upgrading PySide6. Backups are stored inside the target venv.

After patching, run from the Android project directory, for example:
    pyside6-android-deploy -c pysidedeploy.spec --buildozer-file=some_file.spec
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

MARKER = "porn-fetch-buildozer-file-v1"
BUILDOZER_MARKER = "porn-fetch-qt-priority-v1"
CONFIG_MARKER = "porn-fetch-custom-recipes-v1"
RECIPE_TMPL_MARKER = "porn-fetch-all-abi3-v1"
VERSION_GUARD = '''    # check if the Python version is greater than 3.12
    if sys.version_info >= (3, 12):
        raise RuntimeError("[DEPLOY] Android deployment requires Python version 3.11 or lower. "
                           "This is due to a restriction in buildozer.")

'''


def target_python(venv: Path) -> Path:
    for name in ("bin/python", "Scripts/python.exe"):
        candidate = venv / name
        if candidate.is_file():
            return candidate
    raise ValueError(f"No Python interpreter found in {venv}")


def android_deploy_path(venv: Path) -> Path:
    probe = (
        "import json, pathlib, PySide6; "
        "print(json.dumps({'version': PySide6.__version__, "
        "'path': str(pathlib.Path(PySide6.__file__).parent / "
        "'scripts' / 'android_deploy.py')}))"
    )
    result = subprocess.run(
        [str(target_python(venv)), "-I", "-c", probe],
        capture_output=True, text=True, check=True,
    )
    details = json.loads(result.stdout)
    if tuple(map(int, details["version"].split(".")[:2])) != (6, 11):
        raise ValueError(f"Unsupported PySide6 version: {details['version']} (expected 6.11.x)")
    path = Path(details["path"]).resolve()
    if not path.is_file() or not path.is_relative_to(venv):
        raise ValueError(f"Android deploy script is outside {venv}: {path}")
    return path


def deploy_buildozer_path(venv: Path) -> Path:
    probe = (
        "import json, pathlib, PySide6; "
        "print(json.dumps({'path': str(pathlib.Path(PySide6.__file__).parent / "
        "'scripts' / 'deploy_lib' / 'android' / 'buildozer.py')}))"
    )
    result = subprocess.run(
        [str(target_python(venv)), "-I", "-c", probe],
        capture_output=True, text=True, check=True,
    )
    details = json.loads(result.stdout)
    path = Path(details["path"]).resolve()
    if not path.is_file() or not path.is_relative_to(venv):
        raise ValueError(f"Buildozer deploy script is outside {venv}: {path}")
    return path


def deploy_android_config_path(venv: Path) -> Path:
    probe = (
        "import json, pathlib, PySide6; "
        "print(json.dumps({'path': str(pathlib.Path(PySide6.__file__).parent / "
        "'scripts' / 'deploy_lib' / 'android' / 'android_config.py')}))"
    )
    result = subprocess.run(
        [str(target_python(venv)), "-I", "-c", probe],
        capture_output=True, text=True, check=True,
    )
    details = json.loads(result.stdout)
    path = Path(details["path"]).resolve()
    if not path.is_file() or not path.is_relative_to(venv):
        raise ValueError(f"Android config script is outside {venv}: {path}")
    return path


def deploy_pyside_recipe_tmpl_path(venv: Path) -> Path:
    probe = (
        "import json, pathlib, PySide6; "
        "print(json.dumps({'path': str(pathlib.Path(PySide6.__file__).parent / "
        "'scripts' / 'deploy_lib' / 'android' / 'recipes' / 'PySide6' / '__init__.tmpl.py')}))"
    )
    result = subprocess.run(
        [str(target_python(venv)), "-I", "-c", probe],
        capture_output=True, text=True, check=True,
    )
    details = json.loads(result.stdout)
    path = Path(details["path"]).resolve()
    if not path.is_file() or not path.is_relative_to(venv):
        raise ValueError(f"PySide6 recipe template is outside {venv}: {path}")
    return path


def replace_once(source: str, old: str, new: str) -> str:
    if source.count(old) != 1:
        raise ValueError(f"PySide6 source changed; expected one occurrence of: {old[:90]!r}")
    return source.replace(old, new, 1)


def patched_source(source: str) -> str:
    if MARKER not in source:
        source = add_buildozer_file_support(source)
    if VERSION_GUARD in source:
        source = replace_once(source, VERSION_GUARD, "")
    elif "Android deployment requires Python version 3.11 or lower" in source:
        raise ValueError("PySide6 Python version guard changed; refusing an incomplete patch")
    ast.parse(source)
    return source


def patch_buildozer_source(source: str) -> str:
    if "pkg_domain = " not in source:
        old_identity = (
            '        self.set_value("app", "title", pysidedeploy_config.title)\n'
            '        self.set_value("app", "package.name", pysidedeploy_config.title)\n'
            '        self.set_value("app", "package.domain",\n'
            '                       f"org.{pysidedeploy_config.title}")'
        )
        new_identity = (
            '        pkg_domain = (\n'
            '            pysidedeploy_config.get_value("android", "package_domain", ignore_fail=True)\n'
            '            or pysidedeploy_config.get_value("app", "package_domain", ignore_fail=True)\n'
            '            or f"org.{pysidedeploy_config.title}"\n'
            '        )\n'
            '        pkg_name = (\n'
            '            pysidedeploy_config.get_value("android", "package_name", ignore_fail=True)\n'
            '            or pysidedeploy_config.get_value("app", "package_name", ignore_fail=True)\n'
            '            or pysidedeploy_config.title.replace(" ", "_").lower()\n'
            '        )\n'
            '        version = (\n'
            '            pysidedeploy_config.get_value("android", "version", ignore_fail=True)\n'
            '            or pysidedeploy_config.get_value("app", "version", ignore_fail=True)\n'
            '        )\n'
            '        presplash = (\n'
            '            pysidedeploy_config.get_value("android", "presplash", ignore_fail=True)\n'
            '            or pysidedeploy_config.get_value("app", "presplash", ignore_fail=True)\n'
            '            or pysidedeploy_config.icon\n'
            '        )\n'
            '        self.set_value("app", "title", pysidedeploy_config.title)\n'
            '        self.set_value("app", "package.name", pkg_name)\n'
            '        self.set_value("app", "package.domain", pkg_domain)\n'
            '        if version:\n'
            '            self.set_value("app", "version", str(version))\n'
            '        if presplash:\n'
            '            self.set_value("app", "presplash.filename", str(presplash))'
        )
        source = replace_once(source, old_identity, new_identity)

    if "extra_reqs = pysidedeploy_config" not in source:
        old_reqs = '        self.set_value("app", "requirements", "python3,shiboken6,PySide6")'
        new_reqs = (
            '        extra_reqs = pysidedeploy_config.get_value("android", "requirements", ignore_fail=True)\n'
            '        requirements = f"python3,shiboken6,PySide6,{extra_reqs}" if extra_reqs else "python3,shiboken6,PySide6"\n'
            '        self.set_value("app", "requirements", requirements)'
        )
        source = replace_once(source, old_reqs, new_reqs)

    if "qt_priority" not in source:
        old = (
            '        # extra arguments specific to Qt\n'
            '        modules = ",".join(pysidedeploy_config.modules)\n'
            '        local_libs = ",".join(pysidedeploy_config.local_libs)\n'
            '        init_classes = ",".join(init_classes)\n'
            '        extra_args = (f"--qt-libs={modules} --load-local-libs={local_libs}"\n'
            '                      f" --init-classes={init_classes}")\n'
            '        self.set_value("app", "p4a.extra_args", extra_args)'
        )
        new = (
            '        # extra arguments specific to Qt\n'
            '        qt_priority = {\n'
            '            "Core": 0, "Network": 10, "Sql": 11, "Gui": 20, "OpenGL": 30,\n'
            '            "Widgets": 40, "Qml": 50, "Quick": 60, "QuickControls2": 70,\n'
            '        }\n'
            '        sorted_modules = sorted(pysidedeploy_config.modules, key=lambda m: (qt_priority.get(m, 80), m))\n'
            '        modules = ",".join(sorted_modules)\n'
            '        local_libs = ",".join(pysidedeploy_config.local_libs)\n'
            '        init_classes = ",".join(init_classes)\n'
            '        extra_args = (f"--qt-libs={modules} --load-local-libs={local_libs}"\n'
            '                      f" --init-classes={init_classes}")\n'
            '        self.set_value("app", "p4a.extra_args", extra_args)'
        )
        source = replace_once(source, old, new)
    ast.parse(source)
    return source


def patch_android_config_source(source: str) -> str:
    if "import shutil" not in source:
        source = replace_once(source, "import tempfile\n", "import shutil\nimport tempfile\n")
    if "recipe_dir = None" in source:
        source = replace_once(source, "        recipe_dir = None\n", "        recipe_dir = self.recipe_dir\n")
    if CONFIG_MARKER not in source:
        custom_recipes_logic = (
            f"        # {CONFIG_MARKER}\n"
            '        if recipe_dir and not self.dry_run:\n'
            '            recipe_dir.mkdir(parents=True, exist_ok=True)\n'
            '            extra_recipes = self.get_value("android", "extra_recipes_dir", ignore_fail=True)\n'
            '            candidate_dirs = []\n'
            '            if extra_recipes:\n'
            '                candidate_dirs.append(Path(extra_recipes).expanduser().resolve())\n'
            '            candidate_dirs.append((self.source_file.parent / "p4a-recipes").resolve())\n'
            '            candidate_dirs.append((Path(self.project_dir) / "p4a-recipes").resolve())\n\n'
            '            seen = set()\n'
            '            for extra_dir in candidate_dirs:\n'
            '                if extra_dir.is_dir() and extra_dir.resolve() != recipe_dir.resolve() and extra_dir not in seen:\n'
            '                    seen.add(extra_dir)\n'
            '                    for item in extra_dir.iterdir():\n'
            '                        if item.is_dir() and not item.name.startswith(".") and (item / "__init__.py").exists():\n'
            '                            target = recipe_dir / item.name\n'
            '                            logging.info(f"[DEPLOY] Copying custom recipe {item.name} from {item} to {target}")\n'
            '                            shutil.copytree(item, target, dirs_exist_ok=True)\n\n'
            '        return recipe_dir'
        )
        old_half = (
            '        if recipe_dir and not self.dry_run:\n'
            '            recipe_dir.mkdir(parents=True, exist_ok=True)\n'
            '            extra_recipes = self.get_value("android", "extra_recipes_dir", ignore_fail=True)\n'
            '            candidate_dirs = []\n'
            '            if extra_recipes:\n'
            '                candidate_dirs.append(Path(extra_recipes).expanduser().resolve())\n'
            '            candidate_dirs.append((self.source_file.parent / "p4a-recipes").resolve())\n'
            '            candidate_dirs.append((Path(self.project_dir) / "p4a-recipes").resolve())\n\n'
            '            seen = set()\n'
            '            for extra_dir in candidate_dirs:\n'
            '                if extra_dir.is_dir() and extra_dir.resolve() != recipe_dir.resolve() and extra_dir not in seen:\n'
            '                    seen.add(extra_dir)\n'
            '                    for item in extra_dir.iterdir():\n'
            '                        if item.is_dir() and not item.name.startswith(".") and (item / "__init__.py").exists():\n'
            '                            target = recipe_dir / item.name\n'
            '                            logging.info(f"[DEPLOY] Copying custom recipe {item.name} from {item} to {target}")\n'
            '                            shutil.copytree(item, target, dirs_exist_ok=True)\n\n'
            '        return recipe_dir'
        )
        old_tail = (
            '            recipe_dir = ((self.generated_files_path\n'
            '                           / "recipes").resolve())\n\n'
            '        return recipe_dir'
        )
        if old_half in source:
            source = replace_once(source, old_half, custom_recipes_logic)
        elif old_tail in source:
            new_tail = (
                '            recipe_dir = ((self.generated_files_path\n'
                '                           / "recipes").resolve())\n\n'
                + custom_recipes_logic
            )
            source = replace_once(source, old_tail, new_tail)
        else:
            raise ValueError("Could not find recipe_dir block to patch in android_config.py")
    ast.parse(source)
    return source


def patch_pyside_recipe_tmpl_source(source: str) -> str:
    if RECIPE_TMPL_MARKER in source:
        return source

    new_block = (
        f'        # {RECIPE_TMPL_MARKER}\n'
        '        info("Copying PySide6 and Qt Python abi3 libraries")\n'
        '        for so_file in (lib_dir.parent.parent).glob("*.abi3.so"):\n'
        '            shutil.copyfile(so_file, Path(self.ctx.get_libs_dir(arch.arch)) / so_file.name)'
    )

    already_unmarked = (
        '        info("Copying PySide6 and Qt Python abi3 libraries")\n'
        '        for so_file in (lib_dir.parent.parent).glob("*.abi3.so"):\n'
        '            shutil.copyfile(so_file, Path(self.ctx.get_libs_dir(arch.arch)) / so_file.name)'
    )

    original_loop = (
        '        {% for module in qt_modules %}  # noqa: E999\n'
        '        shutil.copyfile(lib_dir.parent.parent / f"Qt{{ module }}.abi3.so",\n'
        '                        Path(self.ctx.get_libs_dir(arch.arch)) / "Qt{{ module }}.abi3.so")\n'
        '        {% if module == "Qml" -%}  # noqa: E999\n'
        '        shutil.copyfile(lib_dir.parent.parent / "libpyside6qml.abi3.so",\n'
        '                        Path(self.ctx.get_libs_dir(arch.arch)) / "libpyside6qml.abi3.so")\n'
        '        {% endif %}  # noqa: E999\n'
        '        {% endfor %}  # noqa: E999'
    )

    if already_unmarked in source:
        source = replace_once(source, already_unmarked, new_block)
    elif original_loop in source:
        source = replace_once(source, original_loop, new_block)
    else:
        raise ValueError("Could not find Qt module loop in PySide6 recipe template")

    return source


def verify_android_deploy(content: str) -> None:
    if MARKER not in content:
        raise ValueError("Patch is not installed in android_deploy.py")
    if VERSION_GUARD in content:
        raise ValueError("Python 3.11 version guard is still present in android_deploy.py")


def verify_buildozer(content: str) -> None:
    if "extra_reqs = pysidedeploy_config" not in content:
        raise ValueError("extra_reqs patch is not installed in buildozer.py")
    if "qt_priority" not in content:
        raise ValueError("qt_priority patch is not installed in buildozer.py")
    if "pkg_domain = " not in content:
        raise ValueError("identity patch is not installed in buildozer.py")


def verify_android_config(content: str) -> None:
    if CONFIG_MARKER not in content:
        raise ValueError("custom recipes patch is not installed in android_config.py")
    if "import shutil" not in content:
        raise ValueError("import shutil is missing in android_config.py")


def verify_pyside_recipe_tmpl(content: str) -> None:
    if RECIPE_TMPL_MARKER not in content:
        raise ValueError("all-abi3 patch is not installed in __init__.tmpl.py")


@dataclass
class PatchTarget:
    name: str
    path: Path
    patch_fn: Callable[[str], str]
    verify_fn: Callable[[str], None]
    is_python: bool = True


def add_buildozer_file_support(source: str) -> str:
    source = replace_once(
        source,
        '\n\ndef main(name: str = None,',
        f'''

def _cleanup_with_custom_spec(config, preserve_spec: bool) -> None:
    # {MARKER}: PySide6's Android cleanup otherwise deletes buildozer.spec.
    cleanup(config=config, is_android=not preserve_spec)
    if preserve_spec:
        build_dir = config.project_dir / ".buildozer"
        if build_dir.exists():
            shutil.rmtree(build_dir)


def main(name: str = None,''',
    )
    source = replace_once(
        source,
        '         force: bool = False, extra_ignore_dirs: str = None, extra_modules_grouped: str = None):',
        '         force: bool = False, extra_ignore_dirs: str = None, extra_modules_grouped: str = None,\n'
        '         buildozer_file: Path = None):',
    )
    source = replace_once(
        source,
        '    android_data = AndroidData(wheel_pyside=pyside_wheel, wheel_shiboken=shiboken_wheel,',
        '''    custom_spec = Path(buildozer_file).expanduser().resolve() if buildozer_file else None
    project_spec = main_file.parent / "buildozer.spec"
    if custom_spec and not custom_spec.is_file():
        raise FileNotFoundError(f"[DEPLOY] Buildozer spec not found: {custom_spec}")
    preserve_spec = custom_spec == project_spec
    if custom_spec and not preserve_spec and project_spec.exists():
        raise FileExistsError(
            f"[DEPLOY] {project_spec} already exists. Move it before supplying {custom_spec}"
        )

    android_data = AndroidData(wheel_pyside=pyside_wheel, wheel_shiboken=shiboken_wheel,''',
    )
    source = replace_once(
        source,
        '    cleanup(config=config, is_android=True)\n\n    python.install_dependencies',
        '    _cleanup_with_custom_spec(config, preserve_spec)\n\n    python.install_dependencies',
    )
    source = replace_once(
        source,
        '''        logging.info("[DEPLOY] Creating buildozer.spec file")
        Buildozer.initialize(pysidedeploy_config=config)
''',
        '''        if custom_spec:
            logging.info(f"[DEPLOY] Using buildozer spec {custom_spec}")
            if not dry_run and not preserve_spec:
                shutil.copyfile(custom_spec, project_spec)
        else:
            logging.info("[DEPLOY] Creating buildozer.spec file")
            Buildozer.initialize(pysidedeploy_config=config)
''',
    )
    source = replace_once(
        source,
        '            cleanup(config=config, is_android=True)',
        '            _cleanup_with_custom_spec(config, preserve_spec)',
    )
    source = replace_once(
        source,
        '    parser.add_argument(\n        "--init", action="store_true",',
        '''    parser.add_argument(
        "--buildozer-file", type=lambda p: Path(p).expanduser().resolve(),
        help="Use this buildozer.spec alongside the PySide deploy config")

    parser.add_argument(
        "--init", action="store_true",''',
    )
    source = replace_once(
        source,
        '         args.force, args.extra_ignore_dirs, args.extra_modules)',
        '         args.force, args.extra_ignore_dirs, args.extra_modules, args.buildozer_file)',
    )
    ast.parse(source)
    return source


def write_atomic(path: Path, content: bytes) -> None:
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(content)
    try:
        os.chmod(temporary, path.stat().st_mode)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("venv", type=Path, help="PySide6 virtual environment")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--dry-run", action="store_true")
    actions.add_argument("--verify", action="store_true")
    actions.add_argument("--restore", action="store_true")
    args = parser.parse_args()

    try:
        venv = args.venv.expanduser().resolve()
        targets = [
            PatchTarget(
                name="android_deploy",
                path=android_deploy_path(venv),
                patch_fn=patched_source,
                verify_fn=verify_android_deploy,
                is_python=True,
            ),
            PatchTarget(
                name="buildozer",
                path=deploy_buildozer_path(venv),
                patch_fn=patch_buildozer_source,
                verify_fn=verify_buildozer,
                is_python=True,
            ),
            PatchTarget(
                name="android_config",
                path=deploy_android_config_path(venv),
                patch_fn=patch_android_config_source,
                verify_fn=verify_android_config,
                is_python=True,
            ),
            PatchTarget(
                name="pyside_recipe_tmpl",
                path=deploy_pyside_recipe_tmpl_path(venv),
                patch_fn=patch_pyside_recipe_tmpl_source,
                verify_fn=verify_pyside_recipe_tmpl,
                is_python=False,
            ),
        ]
        backup_dir = venv / ".pyside6_android_deploy_patch"

        if args.verify:
            for target in targets:
                content = target.path.read_text(encoding="utf-8")
                target.verify_fn(content)
                if target.is_python:
                    ast.parse(content)
                print(f"Verified {target.path}")
            return 0

        if args.restore:
            restored_any = False
            for target in targets:
                backups = sorted(backup_dir.glob(f"{target.name}-*"))
                if not backups:
                    continue
                restored_data = backups[0].read_bytes()
                if target.is_python:
                    ast.parse(restored_data.decode("utf-8"))
                write_atomic(target.path, restored_data)
                print(f"Restored {target.path} from {backups[0]}")
                restored_any = True
            if not restored_any:
                raise ValueError(f"No backups found in {backup_dir}")
            return 0

        patches: list[tuple[PatchTarget, str, str]] = []
        for target in targets:
            content = target.path.read_text(encoding="utf-8")
            modified = target.patch_fn(content)
            if target.is_python:
                ast.parse(modified)
            patches.append((target, content, modified))

        changed_targets = [p for p in patches if p[1] != p[2]]
        if not changed_targets:
            print("All targets are already patched.")
            return 0

        if args.dry_run:
            for target, _, _ in changed_targets:
                print(f"Would patch {target.path}")
            return 0

        backup_dir.mkdir(exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        for target, original, modified in changed_targets:
            backup = backup_dir / f"{target.name}-{stamp}.bak"
            backup.write_bytes(target.path.read_bytes())
            try:
                write_atomic(target.path, modified.encode("utf-8"))
                if target.is_python:
                    ast.parse(target.path.read_text(encoding="utf-8"))
            except Exception:
                write_atomic(target.path, backup.read_bytes())
                raise
            print(f"Patched {target.path}\nBackup: {backup}")
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
