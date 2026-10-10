#!/usr/bin/env python3
"""Unified Android Build Automation for Porn Fetch.

Builds the Android APK for specified architecture(s) using PySide6 and buildozer.
Supports:
  - Single architecture: aarch64 (arm64-v8a), armv7a (armeabi-v7a), x86_64, i686 (x86)
  - All architectures: --architecture=all
  - Automatic PySide6 wheel verification and patching (QtAsyncio and QtContentFileEngine)
  - Dynamic spec file updating (buildozer.spec and pysidedeploy.spec)
  - Automatic injection of native Java bridge (PythonActivity.java) and theme/splash templates
  - Pre-flight validation of deployment patches

Example invocations:
  ./build_android.sh --architecture=aarch64 --wheel-pyside=<wheel> --wheel-shiboken=<wheel>
  ./build_android.sh --architecture=all --wheels-dir=/path/to/wheels
  ./build_android.sh --dry-run --architecture=aarch64 --wheel-pyside=<wheel> --wheel-shiboken=<wheel>
"""
from __future__ import annotations

import argparse
import base64
import configparser
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

# Architecture definitions & mappings
ARCH_MAP: dict[str, dict[str, object]] = {
    "aarch64": {
        "pyside_arch": "aarch64",
        "buildozer_arch": "arm64-v8a",
        "aliases": ["aarch64", "arm64-v8a", "arm64_v8a", "arm64", "android_aarch64"],
    },
    "armv7a": {
        "pyside_arch": "armv7a",
        "buildozer_arch": "armeabi-v7a",
        "aliases": ["armv7a", "armeabi-v7a", "armeabi_v7a", "armeabi", "arm7", "android_armv7a"],
    },
    "x86_64": {
        "pyside_arch": "x86_64",
        "buildozer_arch": "x86_64",
        "aliases": ["x86_64", "x64", "amd64", "android_x86_64"],
    },
    "i686": {
        "pyside_arch": "i686",
        "buildozer_arch": "x86",
        "aliases": ["i686", "x86", "ia32", "android_i686", "android_x86"],
    },
}

ALL_CANONICAL_ARCHS = ["aarch64", "armv7a", "x86_64", "i686"]

PATTERN_CAN_READ = bytes([0xb8, 0x00, 0x40, 0x4d, 0x2c, 0x2a, 0xb8, 0x00, 0x46])
PATCH_CAN_READ = bytes([0x04, 0xac])  # iconst_1; ireturn


def urlsafe_b64encode_nopad(data: bytes) -> str:
    """Encode bytes to base64 with URL-safe characters without padding '='."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def normalize_arch(arch_input: str) -> str:
    """Normalize user input to canonical architecture name or 'all'."""
    val = arch_input.strip().lower()
    if val in ("all", "*"):
        return "all"
    for canon, data in ARCH_MAP.items():
        if val == canon or val in data["aliases"]:
            return canon
    raise ValueError(
        f"Unsupported architecture '{arch_input}'. "
        f"Supported architectures: {', '.join(ALL_CANONICAL_ARCHS)} or 'all'"
    )


def detect_arch_from_filename(filename: str) -> str | None:
    """Detect canonical architecture from wheel filename."""
    lower = filename.lower()
    for canon, data in ARCH_MAP.items():
        for alias in data["aliases"]:
            if alias in lower:
                return canon
    return None


def find_android_sdk(user_sdk: Path | None = None) -> Path | None:
    """Find Android SDK directory."""
    if user_sdk and user_sdk.is_dir():
        return user_sdk.resolve()
    for env_var in ("ANDROID_SDK_ROOT", "ANDROID_HOME"):
        val = os.environ.get(env_var)
        if val and Path(val).is_dir():
            return Path(val).resolve()
    default_pyside = Path.home() / ".pyside6_android_deploy" / "android-sdk"
    if default_pyside.is_dir():
        return default_pyside.resolve()
    return None


def find_android_ndk(user_ndk: Path | None = None) -> Path | None:
    """Find Android NDK directory."""
    if user_ndk and user_ndk.is_dir():
        return user_ndk.resolve()
    for env_var in ("ANDROID_NDK_HOME", "ANDROID_NDK_ROOT"):
        val = os.environ.get(env_var)
        if val and Path(val).is_dir():
            return Path(val).resolve()
    pyside_ndk_dir = Path.home() / ".pyside6_android_deploy" / "android-ndk"
    if pyside_ndk_dir.is_dir():
        subdirs = sorted([d for d in pyside_ndk_dir.glob("android-ndk-*") if d.is_dir()], reverse=True)
        if subdirs:
            return subdirs[0].resolve()
    return None


def patch_pyside_wheel_if_needed(wheel_path: Path, venv_dir: Path) -> bool:
    """Inspect and patch PySide6 wheel with QtAsyncio and QtContentFileEngine fixes.
    
    Returns True if patching was applied, False if already patched.
    """
    if not wheel_path.is_file():
        raise FileNotFoundError(f"Wheel not found: {wheel_path}")

    # Check existing state
    with zipfile.ZipFile(wheel_path, "r") as zin:
        names = set(zin.namelist())
        events_name = "PySide6/QtAsyncio/events.py"
        jar_name = "PySide6/jar/Qt6Android.jar"

        needs_asyncio = False
        if events_name in names:
            events_text = zin.read(events_name).decode("utf-8", errors="ignore")
            if "qtasyncio-compat-v2" not in events_text and "_make_cancelled_error" not in events_text:
                needs_asyncio = True

        needs_jar = False
        if jar_name in names:
            jar_bytes = zin.read(jar_name)
            with zipfile.ZipFile(io.BytesIO(jar_bytes), "r") as jzin:
                cls_name = "org/qtproject/qt/android/QtContentFileEngine.class"
                if cls_name in jzin.namelist():
                    cls_bytes = jzin.read(cls_name)
                    if PATTERN_CAN_READ in cls_bytes:
                        needs_jar = True

    if not needs_asyncio and not needs_jar:
        print(f"[*] Wheel {wheel_path.name} is already patched.")
        return False

    print(f"[*] Patching wheel {wheel_path.name} (QtAsyncio: {needs_asyncio}, QtContentFileEngine: {needs_jar})...")

    # Create backup if not present
    backup = wheel_path.with_suffix(".whl.orig")
    if not backup.exists():
        shutil.copy2(wheel_path, backup)
        print(f"    Created backup: {backup.name}")

    # Discover host QtAsyncio files
    new_contents: dict[str, bytes] = {}
    if needs_asyncio:
        host_asyncio_dir = None
        for cand in venv_dir.glob("lib/python*/site-packages/PySide6/QtAsyncio"):
            if (cand / "events.py").is_file():
                host_asyncio_dir = cand
                break
        if not host_asyncio_dir or not (host_asyncio_dir / "events.py").is_file():
            raise RuntimeError(
                f"Cannot patch wheel QtAsyncio: host PySide6/QtAsyncio not found in {venv_dir}"
            )
        new_contents["PySide6/QtAsyncio/events.py"] = (host_asyncio_dir / "events.py").read_bytes()
        new_contents["PySide6/QtAsyncio/futures.py"] = (host_asyncio_dir / "futures.py").read_bytes()
        new_contents["PySide6/QtAsyncio/tasks.py"] = (host_asyncio_dir / "tasks.py").read_bytes()

    if needs_jar:
        with zipfile.ZipFile(wheel_path, "r") as zin:
            orig_jar = zin.read(jar_name)
        in_buf = io.BytesIO(orig_jar)
        out_buf = io.BytesIO()
        with zipfile.ZipFile(in_buf, "r") as j_in, zipfile.ZipFile(out_buf, "w", compression=zipfile.ZIP_DEFLATED) as j_out:
            for item in j_in.infolist():
                data = j_in.read(item.filename)
                if item.filename == "org/qtproject/qt/android/QtContentFileEngine.class":
                    idx = data.find(PATTERN_CAN_READ)
                    if idx != -1:
                        data = bytearray(data)
                        data[idx : idx + len(PATCH_CAN_READ)] = PATCH_CAN_READ
                        data = bytes(data)
                j_out.writestr(item, data)
        new_contents[jar_name] = out_buf.getvalue()

    # Rewrite wheel with updated RECORD
    with tempfile.NamedTemporaryFile(dir=wheel_path.parent, delete=False, suffix=".whl.tmp") as tmp_file:
        tmp_path = Path(tmp_file.name)

    try:
        with zipfile.ZipFile(wheel_path, "r") as zin, zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            record_name = next(n for n in zin.namelist() if n.endswith(".dist-info/RECORD"))
            record_lines = zin.read(record_name).decode("utf-8").splitlines()

            new_hashes = {}
            for name, data in new_contents.items():
                digest = hashlib.sha256(data).digest()
                new_hashes[name] = f"sha256={urlsafe_b64encode_nopad(digest)},{len(data)}"

            new_record_lines = []
            for line in record_lines:
                if not line.strip():
                    continue
                parts = line.split(",")
                file_path = parts[0]
                if file_path in new_hashes:
                    new_record_lines.append(f"{file_path},{new_hashes[file_path]}")
                elif file_path == record_name:
                    new_record_lines.append(f"{record_name},,")
                else:
                    new_record_lines.append(line)

            record_content = "\n".join(new_record_lines) + "\n"

            for item in zin.infolist():
                if item.filename in new_contents:
                    zout.writestr(item, new_contents[item.filename])
                elif item.filename == record_name:
                    zout.writestr(item, record_content.encode("utf-8"))
                else:
                    zout.writestr(item, zin.read(item.filename))

        tmp_path.replace(wheel_path)
        print(f"[✓] Successfully patched {wheel_path.name}")
        return True
    finally:
        tmp_path.unlink(missing_ok=True)


def inject_android_templates(project_root: Path, buildozer_arch: str) -> None:
    """Inject native Java bridge and custom Android assets into buildozer/p4a trees."""
    templates_dir = project_root / "deployment" / "android_templates"
    if not templates_dir.is_dir():
        print(f"[!] Templates dir not found: {templates_dir}")
        return

    python_activity = templates_dir / "PythonActivity.java"
    manifest_tmpl = templates_dir / "AndroidManifest.tmpl.xml"
    strings_tmpl = templates_dir / "strings.tmpl.xml"
    splash_screen = templates_dir / "splash_screen.xml"
    splash_logo = templates_dir / "splash_logo.png"

    # 1. Patch p4a repo if cloned
    p4a_dir = project_root / ".buildozer" / "android" / "platform" / "python-for-android"
    if p4a_dir.is_dir():
        qt_bootstrap = p4a_dir / "pythonforandroid" / "bootstraps" / "qt" / "build"
        if qt_bootstrap.is_dir():
            java_target = qt_bootstrap / "src" / "main" / "java" / "org" / "kivy" / "android"
            java_target.mkdir(parents=True, exist_ok=True)
            shutil.copy2(python_activity, java_target / "PythonActivity.java")

            tmpl_target = qt_bootstrap / "templates"
            tmpl_target.mkdir(parents=True, exist_ok=True)
            shutil.copy2(manifest_tmpl, tmpl_target / "AndroidManifest.tmpl.xml")
            shutil.copy2(strings_tmpl, tmpl_target / "strings.tmpl.xml")

            res_drawable = qt_bootstrap / "src" / "main" / "res" / "drawable"
            res_drawable.mkdir(parents=True, exist_ok=True)
            shutil.copy2(splash_screen, res_drawable / "splash_screen.xml")
            shutil.copy2(splash_logo, res_drawable / "splash_logo.png")

        # Ensure adaptive icon dir in build.py
        common_build_py = p4a_dir / "pythonforandroid" / "bootstraps" / "common" / "build" / "build.py"
        if common_build_py.is_file():
            txt = common_build_py.read_text(encoding="utf-8")
            if "ensure_dir(join(res_dir, 'mipmap-anydpi-v26'))" not in txt:
                target = "shutil.copy(args.icon_bg, join(res_dir, 'mipmap/icon_background.png'))"
                if target in txt:
                    txt = txt.replace(
                        target,
                        target + "\n        ensure_dir(join(res_dir, 'mipmap-anydpi-v26'))",
                    )
                    common_build_py.write_text(txt, encoding="utf-8")

    # 2. Patch arch-specific build and dist dirs
    arch_build_dir = project_root / ".buildozer" / "android" / "platform" / f"build-{buildozer_arch}"
    if arch_build_dir.is_dir():
        # bootstrap_builds/qt
        boot_qt = arch_build_dir / "build" / "bootstrap_builds" / "qt"
        if boot_qt.is_dir():
            dest_java = boot_qt / "src" / "main" / "java" / "org" / "kivy" / "android"
            dest_java.mkdir(parents=True, exist_ok=True)
            shutil.copy2(python_activity, dest_java / "PythonActivity.java")

            dest_res = boot_qt / "src" / "main" / "res" / "drawable"
            dest_res.mkdir(parents=True, exist_ok=True)
            shutil.copy2(splash_screen, dest_res / "splash_screen.xml")
            shutil.copy2(splash_logo, dest_res / "splash_logo.png")

        # dists/app
        dist_app = arch_build_dir / "dists" / "app"
        if dist_app.is_dir():
            dest_java = dist_app / "src" / "main" / "java" / "org" / "kivy" / "android"
            dest_java.mkdir(parents=True, exist_ok=True)
            shutil.copy2(python_activity, dest_java / "PythonActivity.java")

            dest_res = dist_app / "src" / "main" / "res" / "drawable"
            dest_res.mkdir(parents=True, exist_ok=True)
            shutil.copy2(splash_screen, dest_res / "splash_screen.xml")
            shutil.copy2(splash_logo, dest_res / "splash_logo.png")


def update_buildozer_spec(spec_path: Path, buildozer_arch: str, sdk_path: Path, ndk_path: Path, project_root: Path) -> None:
    """Update buildozer.spec for target architecture and current environment."""
    content = spec_path.read_text(encoding="utf-8")

    replacements = {
        r"^android\.archs\s*=.*$": f"android.archs = {buildozer_arch}",
        r"^android\.sdk_path\s*=.*$": f"android.sdk_path = {sdk_path}",
        r"^android\.ndk_path\s*=.*$": f"android.ndk_path = {ndk_path}",
        r"^p4a\.local_recipes\s*=.*$": f"p4a.local_recipes = {project_root / 'deployment' / 'recipes'}",
        r"^bin_dir\s*=.*$": f"bin_dir = {project_root}",
        r"^presplash\.filename\s*=.*$": f"presplash.filename = {project_root / 'src' / 'frontend' / 'graphics' / 'logo_square.png'}",
        r"^icon\.filename\s*=.*$": f"icon.filename = {project_root / 'src' / 'frontend' / 'graphics' / 'logo_square.png'}",
        r"^icon\.adaptive_foreground\.filename\s*=.*$": f"icon.adaptive_foreground.filename = {project_root / 'src' / 'frontend' / 'graphics' / 'icon_foreground.png'}",
        r"^icon\.adaptive_background\.filename\s*=.*$": f"icon.adaptive_background.filename = {project_root / 'src' / 'frontend' / 'graphics' / 'icon_background.png'}",
    }

    jar_dir = project_root / "deployment" / "jar" / "PySide6" / "jar"
    if jar_dir.is_dir():
        jars = sorted(str(p) for p in jar_dir.glob("*.jar"))
        if jars:
            replacements[r"^android\.add_jars\s*=.*$"] = f"android.add_jars = {','.join(jars)}"

    for pattern, repl in replacements.items():
        content, count = re.subn(pattern, repl, content, flags=re.MULTILINE)
        if count == 0 and not pattern.startswith(r"^android\.add_jars"):
            # If not found, append under [app]
            content = content.replace("[app]\n", f"[app]\n{repl}\n")

    spec_path.write_text(content, encoding="utf-8")


def update_pysidedeploy_spec(
    spec_path: Path,
    wheel_pyside: Path,
    wheel_shiboken: Path,
    sdk_path: Path,
    ndk_path: Path,
    project_root: Path,
    mode: str = "debug",
) -> None:
    """Update pysidedeploy.spec for target wheels and environment."""
    config = configparser.ConfigParser(interpolation=None)
    config.read(spec_path, encoding="utf-8")
    values = {
        "android": {
            "wheel_pyside": wheel_pyside.resolve(),
            "wheel_shiboken": wheel_shiboken.resolve(),
            "extra_recipes_dir": project_root / "p4a-recipes",
            "presplash": project_root / "src/frontend/graphics/logo_transparent.png",
        },
        "buildozer": {
            "sdk_path": sdk_path,
            "ndk_path": ndk_path,
            "recipe_dir": project_root / "deployment/recipes",
            "jars_dir": project_root / "deployment/jar/PySide6/jar",
            "mode": mode,
        },
        "app": {"icon": project_root / "src/frontend/graphics/logo_transparent.png"},
    }
    for section, options in values.items():
        if not config.has_section(section):
            config.add_section(section)
        for key, value in options.items():
            config.set(section, key, str(value))
    # Let PySide derive this from the selected wheel instead of reusing the last build's arch.
    config.remove_option("buildozer", "arch")
    with spec_path.open("w", encoding="utf-8") as destination:
        config.write(destination)


def ensure_host_patches(project_root: Path, venv_dir: Path) -> None:
    """Verify and apply host deployment and QtAsyncio patches."""
    patch_deploy = project_root / "scripts" / "patch_android_deploy.py"
    patch_qtasyncio = project_root / "scripts" / "patch_qtasyncio.py"

    if patch_deploy.is_file():
        # Verify first
        proc = subprocess.run([sys.executable, str(patch_deploy), str(venv_dir), "--verify"], capture_output=True, text=True)
        if proc.returncode != 0:
            print("[*] Applying PySide6 android_deploy patch to virtual environment...")
            subprocess.run([sys.executable, str(patch_deploy), str(venv_dir)], check=True)
        else:
            print("[✓] PySide6 android_deploy is properly patched.")

    if not patch_qtasyncio.is_file():
        raise FileNotFoundError(f"Required QtAsyncio patch script missing: {patch_qtasyncio}")
    print("[*] Applying and verifying QtAsyncio patch to virtual environment...")
    subprocess.run([sys.executable, str(patch_qtasyncio), str(venv_dir)], check=True)
    subprocess.run(
        [sys.executable, str(patch_qtasyncio), str(venv_dir), "--verify"], check=True
    )


def find_wheels_for_arch(
    canon_arch: str,
    search_dirs: list[Path],
    user_pyside: Path | None,
    user_shiboken: Path | None,
) -> tuple[Path | None, Path | None]:
    """Find PySide6 and Shiboken6 wheels for a given canonical architecture."""
    pyside_whl: Path | None = None
    shiboken_whl: Path | None = None

    if user_pyside and user_pyside.is_file():
        if detect_arch_from_filename(user_pyside.name) == canon_arch:
            pyside_whl = user_pyside
    if user_shiboken and user_shiboken.is_file():
        if detect_arch_from_filename(user_shiboken.name) == canon_arch:
            shiboken_whl = user_shiboken

    for search_dir in search_dirs:
        if not search_dir.is_dir():
            continue
        for whl in search_dir.glob("*.whl"):
            # Avoid .tmp or other files
            lower = whl.name.lower()
            if "android" in lower and detect_arch_from_filename(whl.name) == canon_arch:
                if "pyside6" in lower and not pyside_whl:
                    pyside_whl = whl
                elif "shiboken6" in lower and not shiboken_whl:
                    shiboken_whl = whl

    return pyside_whl, shiboken_whl


def build_single_arch(
    canon_arch: str,
    wheel_pyside: Path,
    wheel_shiboken: Path,
    project_root: Path,
    venv_dir: Path,
    sdk_path: Path,
    ndk_path: Path,
    build_mode: str = "debug",
    clean: bool = False,
    dry_run: bool = False,
    output_dir: Path | None = None,
) -> Path | None:
    """Build Android APK for a single canonical architecture."""
    arch_info = ARCH_MAP[canon_arch]
    buildozer_arch = str(arch_info["buildozer_arch"])
    pyside_arch = str(arch_info["pyside_arch"])

    print("\n" + "=" * 70)
    print(f"  BUILDING ARCHITECTURE: {canon_arch.upper()} (buildozer: {buildozer_arch}, pyside: {pyside_arch})")
    print("=" * 70)
    print(f"  PySide6 wheel:  {wheel_pyside}")
    print(f"  Shiboken wheel: {wheel_shiboken}")
    print(f"  Android SDK:    {sdk_path}")
    print(f"  Android NDK:    {ndk_path}")
    print(f"  Build mode:     {build_mode}")

    # Patch wheel if necessary
    if not dry_run:
        patch_pyside_wheel_if_needed(wheel_pyside, venv_dir)

    # Clean if requested
    arch_build_dir = project_root / ".buildozer" / "android" / "platform" / f"build-{buildozer_arch}"
    if clean and arch_build_dir.exists():
        print(f"[*] Cleaning build directory: {arch_build_dir}")
        if not dry_run:
            shutil.rmtree(arch_build_dir, ignore_errors=True)

    # Update specs
    buildozer_spec = project_root / "buildozer.spec"
    pysidedeploy_spec = project_root / "pysidedeploy.spec"

    if dry_run:
        print("[*] (dry-run) Would configure buildozer.spec and pysidedeploy.spec")
        print("[*] (dry-run) Would inject templates into build trees")
        print(f"[*] (dry-run) Would run pyside6-android-deploy for {canon_arch}")
        return None

    update_buildozer_spec(buildozer_spec, buildozer_arch, sdk_path, ndk_path, project_root)
    update_pysidedeploy_spec(pysidedeploy_spec, wheel_pyside, wheel_shiboken, sdk_path, ndk_path, project_root, mode=build_mode)

    # Inject templates into any existing p4a tree
    inject_android_templates(project_root, buildozer_arch)

    # Snapshot existing outputs so an old package cannot masquerade as this build.
    extensions = (".apk",) if build_mode == "debug" else (".aab", ".apk")
    output_roots = (project_root, project_root / "bin")
    previous_outputs = {
        path: path.stat().st_mtime_ns
        for root in output_roots for extension in extensions
        for path in root.glob(f"*{extension}")
    }

    # Execute pyside6-android-deploy
    env = os.environ.copy()
    env["PATH"] = f"{venv_dir / 'bin'}:{env.get('PATH', '')}"
    env["VIRTUAL_ENV"] = str(venv_dir)

    deploy_cmd = [
        str(venv_dir / "bin" / "python"),
        "-m",
        "PySide6.scripts.android_deploy",
        "-c",
        str(pysidedeploy_spec),
        "--buildozer-file",
        str(buildozer_spec),
        "--wheel-pyside",
        str(wheel_pyside.resolve()),
        "--wheel-shiboken",
        str(wheel_shiboken.resolve()),
        "--keep-deployment-files",
    ]

    print(f"[*] Running deployment command:\n    {' '.join(deploy_cmd)}\n")
    proc = subprocess.run(deploy_cmd, cwd=project_root, env=env)
    if proc.returncode != 0:
        raise RuntimeError(f"pyside6-android-deploy failed with exit code {proc.returncode}")

    # Re-inject templates into generated distribution and re-run buildozer if needed
    inject_android_templates(project_root, buildozer_arch)

    candidates = [
        path for root in output_roots for extension in extensions
        for path in root.glob(f"*{extension}")
        if path.stat().st_mtime_ns != previous_outputs.get(path)
        and (detect_arch_from_filename(path.name) == canon_arch
             or (detect_arch_from_filename(path.name) is None
                 and path.name.startswith("app-") and build_mode in path.stem))
    ]

    if not candidates:
        raise FileNotFoundError(f"Build succeeded but could not locate a new {build_mode} package for {canon_arch}")

    # Pick the newest candidate
    apk_path = max(candidates, key=lambda p: p.stat().st_mtime)
    print(f"[✓] Successfully built package: {apk_path} ({apk_path.stat().st_size / (1024*1024):.2f} MB)")

    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        dest_apk = output_dir / f"Porn_Fetch-3.9-{buildozer_arch}-{build_mode}{apk_path.suffix}"
        shutil.copy2(apk_path, dest_apk)
        print(f"[✓] Copied to output destination: {dest_apk}")
        return dest_apk

    return apk_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--architecture",
        "--arch",
        "-a",
        dest="architecture",
        default="aarch64",
        help="Target architecture: aarch64, armv7a, x86_64, i686, or 'all' (default: aarch64)",
    )
    parser.add_argument(
        "--wheel-pyside",
        type=Path,
        help="Path to PySide6 Android wheel (can also be comma-separated list for --architecture=all)",
    )
    parser.add_argument(
        "--wheel-shiboken",
        type=Path,
        help="Path to Shiboken6 Android wheel (can also be comma-separated list for --architecture=all)",
    )
    parser.add_argument(
        "--wheels-dir",
        type=Path,
        help="Directory to search for PySide6 and Shiboken6 wheels for target architectures",
    )
    parser.add_argument(
        "--sdk-path",
        type=Path,
        help="Custom path to Android SDK (auto-detected if omitted)",
    )
    parser.add_argument(
        "--ndk-path",
        type=Path,
        help="Custom path to Android NDK (auto-detected if omitted)",
    )
    parser.add_argument(
        "--build-mode",
        choices=["debug", "release"],
        default="debug",
        help="Build mode: debug or release (default: debug)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory where output APK(s) should be copied",
    )
    parser.add_argument(
        "--venv",
        type=Path,
        help="Path to Python virtual environment containing PySide6 (default: .venv)",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean the architecture's build cache before building",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be run without actually compiling APKs",
    )

    args = parser.parse_args()

    # Determine project root
    project_root = Path(__file__).resolve().parent.parent

    # Determine virtual environment
    if args.venv:
        venv_dir = args.venv.resolve()
    elif os.environ.get("VIRTUAL_ENV"):
        venv_dir = Path(os.environ["VIRTUAL_ENV"]).resolve()
    else:
        venv_dir = (project_root / ".venv").resolve()

    if not venv_dir.is_dir():
        print(f"ERROR: Virtual environment not found at {venv_dir}", file=sys.stderr)
        return 1

    # Verify and apply host patches
    if not args.dry_run:
        ensure_host_patches(project_root, venv_dir)

    # Resolve Android SDK and NDK
    sdk_path = find_android_sdk(args.sdk_path)
    ndk_path = find_android_ndk(args.ndk_path)

    if not sdk_path:
        print("ERROR: Android SDK not found. Specify --sdk-path or set $ANDROID_SDK_ROOT.", file=sys.stderr)
        return 1
    if not ndk_path:
        print("ERROR: Android NDK not found. Specify --ndk-path or set $ANDROID_NDK_HOME.", file=sys.stderr)
        return 1

    # Target architectures
    target_arch = normalize_arch(args.architecture)
    target_archs = ALL_CANONICAL_ARCHS if target_arch == "all" else [target_arch]

    search_dirs = [project_root]
    if args.wheels_dir:
        search_dirs.insert(0, args.wheels_dir.resolve())

    # Build loop
    built_apks: list[tuple[str, Path]] = []
    skipped_archs: list[str] = []
    planned_archs: list[str] = []

    for arch in target_archs:
        pyside_whl, shiboken_whl = find_wheels_for_arch(
            arch, search_dirs, args.wheel_pyside, args.wheel_shiboken
        )

        if not pyside_whl or not shiboken_whl:
            msg = f"Missing wheels for architecture '{arch}':"
            if not pyside_whl:
                msg += " (PySide6 wheel not found)"
            if not shiboken_whl:
                msg += " (Shiboken6 wheel not found)"
            if target_arch == "all":
                print(f"[!] {msg} - Skipping.")
                skipped_archs.append(arch)
                continue
            else:
                print(f"ERROR: {msg}", file=sys.stderr)
                print(f"Checked directories: {', '.join(str(d) for d in search_dirs)}", file=sys.stderr)
                return 1

        planned_archs.append(arch)
        apk = build_single_arch(
            canon_arch=arch,
            wheel_pyside=pyside_whl,
            wheel_shiboken=shiboken_whl,
            project_root=project_root,
            venv_dir=venv_dir,
            sdk_path=sdk_path,
            ndk_path=ndk_path,
            build_mode=args.build_mode,
            clean=args.clean,
            dry_run=args.dry_run,
            output_dir=args.output_dir,
        )
        if apk:
            built_apks.append((arch, apk))

    print("\n" + "=" * 70)
    print("  BUILD SUMMARY")
    print("=" * 70)
    if args.dry_run:
        print("  Dry-run completed successfully. Planned architectures:")
        for arch in planned_archs:
            print(f"  - {arch} ({ARCH_MAP[arch]['buildozer_arch']})")
    else:
        if built_apks:
            print(f"  Successfully built {len(built_apks)} package(s):")
            for arch, apk in built_apks:
                print(f"  - [{arch}] {apk} ({apk.stat().st_size / (1024*1024):.2f} MB)")
        if skipped_archs:
            print(f"  Skipped (no wheels found): {', '.join(skipped_archs)}")

    if not planned_archs:
        print("ERROR: No architectures had a complete wheel pair.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
