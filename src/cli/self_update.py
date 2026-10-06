"""Verified updates for standalone, frozen CLI builds."""

from __future__ import annotations

import asyncio
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

from platformdirs import user_cache_dir
from tuf.ngclient import Updater

from src.shared.release import release_time, update_eligibility

REPOSITORY_URL = os.environ.get("PORNFETCH_CLI_UPDATE_REPO_URL", "https://api.pornfetch.to/repo/cli/").rstrip("/") + "/"
ROOT_FILE = Path(__file__).with_name("update_root.json")
BUILD_FILE = Path(__file__).with_name("update_build.json")


def target_name(system: str | None = None, machine: str | None = None) -> str:
    system = (system or platform.system()).lower()
    machine = (machine or platform.machine()).lower()
    if system == "darwin":
        system = "darwin"
    elif system not in {"linux", "windows"}:
        raise ValueError(f"No CLI update target for {system}/{machine}")
    aliases = {"x86_64": "amd64", "x64": "amd64", "aarch64": "arm64", "i386": "x86", "i686": "x86"}
    machine = aliases.get(machine, machine)
    if system == "linux" and machine == "x86":
        machine = "x32"
    allowed = {
        "linux": {"amd64", "arm64", "x32", "riscv64", "s390x", "ppc64le"},
        "windows": {"amd64", "arm64", "x86"},
        "darwin": {"amd64", "arm64"},
    }
    if machine not in allowed[system]:
        raise ValueError(f"No CLI update target for {system}/{machine}")
    return f"{system}/{machine}.zip"


def version_parts(version: str) -> tuple[int, ...]:
    parts = version.split(".")
    if not parts or not all(part.isdecimal() for part in parts):
        raise ValueError(f"Invalid CLI update version: {version}")
    return tuple(int(part) for part in parts)


def _installation_path() -> Path:
    if not getattr(sys, "frozen", False):
        raise RuntimeError("Source and package-manager installations must be updated with their original installer")
    executable = Path(sys.executable).resolve()
    restricted = ("/usr/", "/bin/", "/sbin/", "/opt/", "/Applications/", "/System/")
    if sys.platform == "win32":
        program_files = [os.environ.get("ProgramFiles", "C:\\Program Files"), os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")]
        if any(executable.is_relative_to(Path(directory).resolve()) for directory in program_files):
            raise RuntimeError("This installation is managed by an installer; update it with that installer")
    elif str(executable).startswith(restricted):
        raise RuntimeError("This installation is managed by the system; update it with the system package manager")
    if not os.access(executable.parent, os.W_OK):
        raise RuntimeError(f"The install directory is not writable: {executable.parent}")
    return executable


def _safe_name(name: str) -> str:
    if name in {"", ".", ".."} or Path(name).name != name or "/" in name or "\\" in name:
        raise ValueError(f"Unsafe update archive filename: {name}")
    return name


def _stage_bundle(archive: Path, destination: Path, expected_target: str, expected_version: str, executable: Path, expected_release: int | None = None) -> Path:
    with zipfile.ZipFile(archive) as bundle:
        names = bundle.namelist()
        if len(names) != len(set(names)) or "manifest.json" not in names:
            raise ValueError("Invalid CLI update archive")
        manifest = json.loads(bundle.read("manifest.json"))
        if expected_release is not None and manifest.get("release_timestamp") != expected_release:
            raise ValueError("CLI archive release date does not match signed metadata")
        files = manifest.get("files")
        if (manifest.get("target") != expected_target or manifest.get("version") != expected_version
                or not isinstance(files, list) or set(names) != set(files) | {"manifest.json"}
                or manifest.get("executable") not in files):
            raise ValueError("CLI update archive does not match signed target metadata")
        if not all(isinstance(name, str) and _safe_name(name) for name in files):
            raise ValueError("Invalid CLI update archive filenames")
        new_dir = destination / "new"
        new_dir.mkdir()
        install_files = []
        for name in files:
            item = bundle.getinfo(name)
            if item.is_dir() or (item.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("CLI update archive contains a directory or link")
            installed_name = executable.name if name == manifest["executable"] else name
            _safe_name(installed_name)
            if installed_name in install_files:
                raise ValueError("CLI update archive contains conflicting file names")
            install_files.append(installed_name)
            with bundle.open(item) as source, (new_dir / installed_name).open("wb") as output:
                shutil.copyfileobj(source, output)
            if name == manifest["executable"] and sys.platform != "win32":
                (new_dir / installed_name).chmod(0o755)
        plan = {"executable": executable.name, "files": install_files, "version": expected_version}
        plan_path = destination / "plan.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        return plan_path


def _apply_update(stage: Path, executable: Path) -> int:
    plan = json.loads((stage / "plan.json").read_text(encoding="utf-8"))
    files = plan["files"]
    if not files or not all(isinstance(name, str) and _safe_name(name) for name in files):
        raise ValueError("Invalid staged update plan")
    if plan["executable"] != executable.name or stage.parent.resolve() != executable.parent.resolve():
        raise ValueError("Staged update does not match installation")

    backup = stage / "previous"
    backup.mkdir(exist_ok=True)
    installed: list[Path] = []
    moved: list[Path] = []
    deadline = time.monotonic() + 60
    try:
        for name in files:
            old = executable.parent / name
            new = stage / "new" / name
            if not new.is_file():
                raise FileNotFoundError(new)
            if old.exists():
                while True:
                    try:
                        os.replace(old, backup / name)
                        moved.append(old)
                        break
                    except PermissionError:
                        if time.monotonic() >= deadline:
                            raise
                        time.sleep(0.2)
            os.replace(new, old)
            installed.append(old)
        (stage / "result.txt").write_text(f"Installed {plan['version']}; previous files: {backup}\n", encoding="utf-8")
        return 0
    except Exception as exc:
        for path in reversed(installed):
            path.unlink(missing_ok=True)
        for path in reversed(moved):
            os.replace(backup / path.name, path)
        (stage / "result.txt").write_text(f"Update failed and was rolled back: {exc}\n", encoding="utf-8")
        return 1


def apply_from_helper(stage_arg: str, executable_arg: str) -> int:
    stage = Path(stage_arg).resolve()
    executable = Path(executable_arg).resolve()
    return _apply_update(stage, executable)


async def _license_status():
    from src.licensing.service import create_license_service
    service = create_license_service(None)
    try:
        return await service.check(force=True)
    finally:
        await service.close()


def run_self_update(*, check_only: bool, assume_yes: bool) -> int:
    try:
        build = json.loads(BUILD_FILE.read_text(encoding="utf-8"))
        current = build["version"]
        name = build.get("target") or target_name()
        cache = Path(user_cache_dir("PornFetch")) / "cli-update"
        metadata_dir = cache / "metadata"
        target_dir = cache / "targets"
        metadata_dir.mkdir(parents=True, exist_ok=True)
        target_dir.mkdir(parents=True, exist_ok=True)
        updater = Updater(
            metadata_dir=str(metadata_dir),
            metadata_base_url=REPOSITORY_URL + "metadata/",
            target_dir=str(target_dir),
            target_base_url=REPOSITORY_URL + "targets/",
            bootstrap=ROOT_FILE.read_bytes(),
        )
        target = updater.get_targetinfo(name)
        if target is None or not isinstance(target.custom, dict):
            print(f"No signed CLI update is published for {name}.")
            return 0
        latest = target.custom.get("version")
        if not isinstance(latest, str):
            raise ValueError("Signed CLI target has no version")
        if version_parts(latest) <= version_parts(current):
            print(f"Porn Fetch CLI is up to date ({current}).")
            return 0
        print(f"Porn Fetch CLI {latest} is available for {name} (installed: {current}).")
        released = release_time(target.custom.get("release_timestamp"))
        status = asyncio.run(_license_status())
        entitled, reason = update_eligibility(status, released)
        print(reason)
        if not entitled:
            print("Purchase / renew: https://pornfetch.to/ — then refresh your license.")
            return 0 if check_only else 1
        if check_only:
            return 0
        executable = _installation_path()
        if not assume_yes:
            if not sys.stdin.isatty() or input("Download and install this signed update? [y/N] ").strip().lower() not in {"y", "yes"}:
                print("Update cancelled.")
                return 0
        archive = Path(updater.download_target(target))
        stage = Path(tempfile.mkdtemp(prefix=".pornfetch-update-", dir=executable.parent))
        _stage_bundle(archive, stage, name, latest, executable, released)
        helper = stage / ("pornfetch-update-helper.exe" if sys.platform == "win32" else "pornfetch-update-helper")
        shutil.copy2(executable, helper)
        if sys.platform != "win32":
            helper.chmod(0o755)
        flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
        subprocess.Popen(
            [str(helper), "--apply-update", str(stage), str(executable)],
            cwd=str(stage),
            creationflags=flags,
            start_new_session=sys.platform != "win32",
            close_fds=True,
        )
        print(f"Update staged. Exit now; the helper will replace the CLI. Result: {stage / 'result.txt'}")
        return 0
    except Exception as exc:
        print(f"CLI update failed: {exc}", file=sys.stderr)
        return 1
