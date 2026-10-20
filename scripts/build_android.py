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
  - Reuse of Buildozer downloads and compiled dependencies unless --clean is requested
  - Release APK alignment, signing and verification (use --unsigned to skip)

Release signing defaults to my-release-key.jks / my-key-alias in the project root.
The signing tools must be on PATH. apksigner prompts for passwords interactively.
Single-architecture builds produce app-aligned.apk and app-signed.apk in the
project root (or --output-dir). Multi-architecture builds add architecture suffixes.
Debug builds retain the build tool's debug signature.

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
ANDROID_NDK_VERSION = "28c"
ANDROID_NDK_REVISION = "28.2.13676358"

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
    """Find r28c using its package metadata, ignoring stale environment paths."""
    def is_required_ndk(path: Path) -> bool:
        properties = path / "source.properties"
        return properties.is_file() and re.search(
            rf"^Pkg\.Revision\s*=\s*{re.escape(ANDROID_NDK_REVISION)}\s*$",
            properties.read_text(encoding="utf-8"), re.MULTILINE,
        ) is not None

    if user_ndk:
        if not is_required_ndk(user_ndk):
            raise ValueError(f"Android NDK r{ANDROID_NDK_VERSION} ({ANDROID_NDK_REVISION}) required: {user_ndk}")
        return user_ndk.resolve()
    for env_var in ("ANDROID_NDK_HOME", "ANDROID_NDK_ROOT", "ANDROIDNDK"):
        val = os.environ.get(env_var)
        if val and is_required_ndk(Path(val)):
            return Path(val).resolve()
    candidates = [Path.home() / ".pyside6_android_deploy" / "android-ndk" / f"android-ndk-r{ANDROID_NDK_VERSION}"]
    sdk = find_android_sdk()
    if sdk:
        candidates.append(sdk / "ndk" / ANDROID_NDK_REVISION)
    for candidate in candidates:
        if is_required_ndk(candidate):
            return candidate.resolve()
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


def patch_p4a_adaptive_icon(project_root: Path) -> None:
    """Ensure all p4a build.py files create mipmap-anydpi-v26 before writing icon.xml."""
    buildozer_dir = project_root / ".buildozer"
    if not buildozer_dir.is_dir():
        return
    for build_py in buildozer_dir.rglob("build.py"):
        try:
            txt = build_py.read_text(encoding="utf-8")
            target = "shutil.copy(args.icon_bg, join(res_dir, 'mipmap/icon_background.png'))"
            patch = "\n        ensure_dir(join(res_dir, 'mipmap-anydpi-v26'))"
            if target in txt and patch not in txt:
                txt = txt.replace(target, target + patch, 1)
                build_py.write_text(txt, encoding="utf-8")
                print(f"[✓] Patched adaptive icon directory in {build_py.relative_to(project_root)}")
        except Exception:
            pass


def inject_android_templates(project_root: Path, buildozer_arch: str) -> None:
    """Inject native Java bridge and custom Android assets into buildozer/p4a trees."""
    patch_p4a_adaptive_icon(project_root)
    templates_dir = project_root / "deployment" / "android_templates"
    if not templates_dir.is_dir():
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
        r"^p4a\.branch\s*=.*$": "p4a.branch = develop",
        r"^p4a\.commit\s*=.*$": "p4a.commit = HEAD",
        r"^p4a\.hook\s*=.*$": f"p4a.hook = {project_root / 'scripts' / 'android_storage_hook.py'}",
        r"^android\.archs\s*=.*$": f"android.archs = {buildozer_arch}",
        r"^android\.sdk_path\s*=.*$": f"android.sdk_path = {sdk_path}",
        r"^android\.ndk_path\s*=.*$": f"android.ndk_path = {ndk_path}",
        r"^android\.ndk\s*=.*$": f"android.ndk = {ANDROID_NDK_VERSION}",
        r"^android\.release_artifact\s*=.*$": "android.release_artifact = apk",
        r"^p4a\.local_recipes\s*=.*$": f"p4a.local_recipes = {project_root / 'deployment' / 'recipes'}",
        r"^bin_dir\s*=.*$": f"bin_dir = {project_root}",
        r"^presplash\.filename\s*=.*$": f"presplash.filename = {project_root / 'src' / 'frontend' / 'graphics' / 'logo_square.png'}",
        r"^icon\.filename\s*=.*$": f"icon.filename = {project_root / 'src' / 'frontend' / 'graphics' / 'logo_square.png'}",
        r"^icon\.adaptive_foreground\.filename\s*=.*$": f"icon.adaptive_foreground.filename = {project_root / 'src' / 'frontend' / 'graphics' / 'icon_foreground.png'}",
        r"^icon\.adaptive_background\.filename\s*=.*$": f"icon.adaptive_background.filename = {project_root / 'src' / 'frontend' / 'graphics' / 'icon_background.png'}",
    }

    # PySide can regenerate buildozer.spec with the display title as the package
    # name and omit our dependencies. With --buildozer-file it no longer applies
    # these settings itself, so recover them from the deployment config here.
    deploy_config = configparser.ConfigParser(interpolation=None)
    deploy_config.read(project_root / "pysidedeploy.spec", encoding="utf-8")
    for option, buildozer_option in (
        ("package_name", "package.name"),
        ("package_domain", "package.domain"),
        ("version", "version"),
        ("requirements", "requirements"),
    ):
        value = (deploy_config.get("android", option, fallback="")
                 or deploy_config.get("app", option, fallback=""))
        if value:
            if option == "requirements":
                value = f"python3,shiboken6,PySide6,{value}"
            replacements[rf"^{re.escape(buildozer_option)}\s*=.*$"] = f"{buildozer_option} = {value}"

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
    mode: str = "release",
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


def ensure_android_deploy_deps(venv_dir: Path) -> None:
    """Verify that required deployment dependencies are installed in the venv."""
    missing_deps = []
    for pkg in ("jinja2", "pkginfo", "tqdm"):
        try:
            subprocess.run([str(venv_dir / "bin" / "python"), "-c", f"import {pkg}"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            missing_deps.append(pkg)
    if missing_deps:
        print(f"[*] Installing required Android deployment dependencies: {', '.join(missing_deps)}...")
        subprocess.run(["uv", "pip", "install", *missing_deps], check=True)


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


def restore_buildozer_cache(project_root: Path) -> None:
    """Recover the cache moved into deployment/ by older PySide deploy patches."""
    previous_cache = project_root / "deployment" / ".buildozer"
    build_dir = project_root / ".buildozer"
    if previous_cache.is_dir():
        if build_dir.exists():
            raise FileExistsError(
                f"Both {build_dir} and {previous_cache} exist. "
                "Move one aside before building so neither cache is deleted."
            )
        print(f"[*] Restoring Buildozer cache from {previous_cache}")
        shutil.move(str(previous_cache), str(build_dir))


def build_single_arch(
    canon_arch: str,
    wheel_pyside: Path,
    wheel_shiboken: Path,
    project_root: Path,
    venv_dir: Path,
    sdk_path: Path,
    ndk_path: Path,
    build_mode: str = "release",
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
        # Restore before --clean and template injection, which operate on .buildozer.
        restore_buildozer_cache(project_root)

    # Clean if requested
    arch_build_dir = project_root / ".buildozer" / "android" / "platform" / f"build-{buildozer_arch}"
    ndk_stamp = arch_build_dir / ".porn-fetch-ndk"
    cached_ndk = ndk_stamp.read_text(encoding="utf-8").strip() if ndk_stamp.is_file() else None
    if cached_ndk != ANDROID_NDK_REVISION and any(
        directory.exists() for directory in (arch_build_dir / "build", arch_build_dir / "dists")
    ):
        print(f"[*] Rebuilding native cache for NDK r{ANDROID_NDK_VERSION}; keeping downloaded archives")
        clean = True
    if clean:
        # p4a keeps downloaded archives in packages/ beside these directories.
        for directory in (arch_build_dir / "build", arch_build_dir / "dists"):
            if directory.exists():
                print(f"[*] Cleaning build directory: {directory}")
                if not dry_run:
                    shutil.rmtree(directory)

    # Update specs
    buildozer_spec = project_root / "buildozer.spec"
    pysidedeploy_spec = project_root / "pysidedeploy.spec"

    if dry_run:
        print("[*] (dry-run) Would configure buildozer.spec and pysidedeploy.spec")
        print("[*] (dry-run) Would inject templates into build trees")
        print(f"[*] (dry-run) Would run pyside6-android-deploy for {canon_arch}")
        return None

    arch_build_dir.mkdir(parents=True, exist_ok=True)
    ndk_stamp.write_text(ANDROID_NDK_REVISION + "\n", encoding="utf-8")
    update_buildozer_spec(buildozer_spec, buildozer_arch, sdk_path, ndk_path, project_root)
    update_pysidedeploy_spec(pysidedeploy_spec, wheel_pyside, wheel_shiboken, sdk_path, ndk_path, project_root, mode=build_mode)

    # Inject templates into any existing p4a tree
    inject_android_templates(project_root, buildozer_arch)

    # Snapshot existing outputs so an old package cannot masquerade as this build.
    extensions = (".apk",)
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
    for variable in ("ANDROIDNDK", "ANDROID_NDK_HOME", "ANDROID_NDK_ROOT"):
        env[variable] = str(ndk_path)

    pyside_scripts_dirs = list(venv_dir.glob("lib/python*/site-packages/PySide6/scripts"))
    if pyside_scripts_dirs:
        env["PYTHONPATH"] = f"{pyside_scripts_dirs[0]}:{env.get('PYTHONPATH', '')}".rstrip(":")

    pyside_deploy_bin = venv_dir / "bin" / "pyside6-android-deploy"
    if pyside_deploy_bin.is_file():
        deploy_cmd = [str(pyside_deploy_bin)]
    else:
        deploy_cmd = [str(venv_dir / "bin" / "python"), "-m", "PySide6.scripts.android_deploy"]

    deploy_cmd.extend([
        "-c",
        str(pysidedeploy_spec),
        "--buildozer-file",
        str(buildozer_spec),
        "--wheel-pyside",
        str(wheel_pyside.resolve()),
        "--wheel-shiboken",
        str(wheel_shiboken.resolve()),
        "--keep-deployment-files",
    ])

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
        and build_mode in path.stem
        and (detect_arch_from_filename(path.name) == canon_arch
             or (detect_arch_from_filename(path.name) is None
                 and path.name.startswith("app-") and build_mode in path.stem))
    ]

    if not candidates:
        raise FileNotFoundError(
            f"No new {build_mode} package found for {canon_arch}; "
            "check the deployment log above for build errors"
        )

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


def sign_apk(apk: Path, output_dir: Path, keystore: Path, key_alias: str,
             architecture: str | None = None) -> Path:
    """Align, sign and verify a release APK; inherit stdin for password prompts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    suffix = f"-{architecture}" if architecture else ""
    aligned = output_dir / f"app-aligned{suffix}.apk"
    signed = output_dir / f"app-signed{suffix}.apk"
    # Publish only verified output, preserving a previous signed build on failure.
    with tempfile.TemporaryDirectory(prefix="apk-sign-", dir=output_dir) as temporary:
        staged_aligned = Path(temporary) / aligned.name
        staged_signed = Path(temporary) / signed.name
        subprocess.run(["zipalign", "-p", "-f", "-v", "4", str(apk), str(staged_aligned)], check=True)
        subprocess.run(["apksigner", "sign", "--ks", str(keystore),
                        "--ks-key-alias", key_alias, "--out", str(staged_signed),
                        str(staged_aligned)], check=True)
        subprocess.run(["apksigner", "verify", "--verbose", str(staged_signed)], check=True)
        staged_aligned.replace(aligned)
        staged_signed.replace(signed)
        signature = Path(str(staged_signed) + ".idsig")
        destination_signature = Path(str(signed) + ".idsig")
        if signature.exists():
            signature.replace(destination_signature)
        else:
            destination_signature.unlink(missing_ok=True)
    print(f"[✓] Signed and verified APK: {signed}")
    return signed


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
        help="Path to Android NDK r28c (auto-detected and revision-checked if omitted)",
    )
    parser.add_argument(
        "--build-mode",
        choices=["debug", "release"],
        default="release",
        help="Build mode: debug or release APK (default: release)",
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
        help="Recompile the selected architecture; keep downloaded dependency archives",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be run without actually compiling APKs",
    )

    parser.add_argument("--keystore", type=Path, default=Path("my-release-key.jks"),
                        help="Release keystore, relative to project root (default: my-release-key.jks)")
    parser.add_argument("--key-alias", default="my-key-alias", help="Signing key alias (default: my-key-alias)")
    parser.add_argument("--unsigned", action="store_true", help="Skip automatic release APK signing")

    args = parser.parse_args()

    # Determine project root
    project_root = Path(__file__).resolve().parent.parent

    signing = args.build_mode == "release" and not args.unsigned
    keystore = args.keystore if args.keystore.is_absolute() else project_root / args.keystore
    if signing and not args.dry_run:
        if not keystore.is_file():
            print(f"ERROR: Signing keystore not found: {keystore}. Use --keystore or --unsigned.", file=sys.stderr)
            return 1
        for tool in ("zipalign", "apksigner"):
            if not shutil.which(tool):
                print(f"ERROR: {tool} not found on PATH; required for release signing.", file=sys.stderr)
                return 1

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
        ensure_android_deploy_deps(venv_dir)

    # Resolve Android SDK and NDK
    sdk_path = find_android_sdk(args.sdk_path)
    try:
        ndk_path = find_android_ndk(args.ndk_path)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if not sdk_path:
        print("ERROR: Android SDK not found. Specify --sdk-path or set $ANDROID_SDK_ROOT.", file=sys.stderr)
        return 1
    if not ndk_path:
        print("ERROR: Android NDK r28c not found. Specify --ndk-path or set $ANDROID_NDK_HOME.", file=sys.stderr)
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
        if signing:
            signing_output = args.output_dir.resolve() if args.output_dir else project_root
            suffix = arch if target_arch == "all" else None
            if args.dry_run:
                print(f"[*] (dry-run) Would zipalign, sign with {keystore} (alias {args.key_alias}), "
                      f"and verify app-signed{'-' + suffix if suffix else ''}.apk in {signing_output}")
            elif apk:
                try:
                    apk = sign_apk(apk, signing_output, keystore, args.key_alias, suffix)
                except (OSError, subprocess.CalledProcessError) as error:
                    print(f"ERROR: APK signing failed: {error}", file=sys.stderr)
                    return 1
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
