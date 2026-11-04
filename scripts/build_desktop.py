"""Build an unsigned desktop application folder or a standalone CLI."""
from __future__ import annotations

import argparse
import configparser
import os
import platform
import plistlib
import shutil
import subprocess
import sys
import tempfile
from importlib.metadata import version
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*arguments: str | Path, env: dict[str, str] | None = None) -> None:
    subprocess.run([str(arg) for arg in arguments], cwd=ROOT, env=env, check=True)


def python(*arguments: str | Path) -> None:
    run(sys.executable, *arguments)


def gui_payload(staging: Path, project: Path = ROOT) -> Path:
    """Handle PySide's normal output and Windows' long-command fallback."""
    suffix = ".app" if sys.platform == "darwin" else ".dist"
    output = staging / ("Porn Fetch" + suffix)
    if sys.platform == "win32" and (project / "deployment/deploy_main.dist").is_dir():
        shutil.copytree(project / "deployment/deploy_main.dist", output, dirs_exist_ok=True)
    if not output.is_dir():
        raise FileNotFoundError(f"Compiler did not produce {output}")
    if sys.platform == "darwin":
        with (output / "Contents/Info.plist").open("rb") as stream:
            name = plistlib.load(stream)["CFBundleExecutable"]
        executable = output / "Contents/MacOS" / name
    else:
        names = ("Porn Fetch.exe", "main.exe", "deploy_main.exe") if sys.platform == "win32" else ("Porn Fetch", "main.bin")
        executable = next((output / name for name in names if (output / name).is_file()), None)
        if executable is None:
            raise FileNotFoundError(f"No executable in {output}")
        target = output / names[0]
        if executable != target:
            executable.rename(target)
        executable = target
    if not executable.is_file():
        raise FileNotFoundError(executable)
    return executable


def build(args: argparse.Namespace) -> Path:
    target = {"win32": "windows", "darwin": "macos", "linux": "linux"}.get(sys.platform)
    arch = {"amd64": "x64", "x86_64": "x64", "aarch64": "arm64", "arm64": "arm64"}.get(platform.machine().lower())
    if target is None or arch is None:
        raise ValueError("Use this builder on Windows, macOS or Linux with x64 or ARM64 Python.")
    output = args.output.resolve() if args.output else ROOT / "dist" / f"local-{args.target}"
    if args.target == "gui" and sys.platform == "darwin":
        if args.output is None:
            output = output / "Porn Fetch.app"
        elif output.suffix != ".app":
            raise ValueError("macOS GUI output must end in .app")
    if output.exists():
        raise FileExistsError(f"Output already exists: {output}. Choose a new --output folder or move the old build.")
    if (ROOT / "deployment/deploy_main.dist").exists():
        raise FileExistsError("Move or remove deployment/deploy_main.dist before building; it may be an old Windows build.")
    print("Local builds have no publisher signature. macOS builds are ad-hoc signed, not notarized.\n"
          "Windows SmartScreen, Gatekeeper or antivirus software may warn about these files.", flush=True)
    with tempfile.TemporaryDirectory(prefix="pornfetch-desktop-") as temporary:
        work = Path(temporary)
        tools = work / "third_party"
        tools.mkdir()
        if not args.without_pocketbase:
            python("scripts/fetch_pocketbase.py", "--platform", target, "--arch", arch, "--dest", tools)
        if not args.without_ffmpeg:
            command = ["packaging/build_ffmpeg.py", "--dest", tools, "--work-dir", work / "ffmpeg"]
            if args.msys2_root:
                command.extend(["--msys2-root", args.msys2_root])
            python(*command)
        if not args.without_tor:
            python("packaging/fetch_tor.py", "--platform", target, "--arch", arch, "--work-dir", work / "tor")
        elif (ROOT / "src/shared/tor").exists():
            raise ValueError("--without-tor needs a checkout without a previously staged src/shared/tor folder.")
        if args.target == "gui":
            python("scripts/patch_qtasyncio.py", sys.prefix)
            python("scripts/patch_qtasyncio.py", sys.prefix, "--verify")
            python("scripts/translations.py", "build")
            python("scripts/compile_qml.py")
            spec = work / "desktop.spec"
            python("packaging/prepare_deploy.py", "--template", f"packaging/pysidedeploy_{target}.spec", "--output", spec)
            config = configparser.ConfigParser(interpolation=None)
            config.read(spec)
            config["app"]["exec_directory"] = str(work)
            with spec.open("w") as stream:
                config.write(stream)
            deploy = Path(sys.executable).parent / ("pyside6-deploy.exe" if sys.platform == "win32" else "pyside6-deploy")
            python("scripts/build_output.py", "--label", "Compile desktop GUI", "--", deploy,
                   "-c", spec, "-f", "-v", "--keep-deployment-files", "--no-install", "--nuitka-version", version("Nuitka"))
            executable = gui_payload(work)
            payload = work / ("Porn Fetch.app" if sys.platform == "darwin" else "Porn Fetch.dist")
            runtime = executable.parent
        else:
            python("scripts/build_output.py", "--label", "Compile CLI", "--", sys.executable, "-m", "PyInstaller",
                   "--clean", "--noconfirm", "--distpath", work / "cli", "--workpath", work / "pyinstaller",
                   "packaging/pyinstaller_cli.spec")
            payload = work / "cli"
            executable = payload / ("Porn_Fetch_CLI.exe" if sys.platform == "win32" else "Porn_Fetch_CLI")
            runtime = payload
        shutil.copytree(tools, runtime / "third_party", dirs_exist_ok=True)
        if args.target == "gui" and not args.without_tor and (ROOT / "src/shared/tor").is_dir():
            shutil.copytree(ROOT / "src/shared/tor", runtime / "src/shared/tor", dirs_exist_ok=True)
        legal_args = ["packaging/collect_legal.py", runtime / "LEGAL", "--offline"]
        if not args.without_ffmpeg:
            legal_args.extend(["--ffmpeg-legal", tools / "ffmpeg-legal"])
        python(*legal_args)
        if args.target == "gui" and sys.platform == "darwin":
            python("packaging/repair_macos_bundle.py", payload)
        if args.target == "gui":
            env = dict(os.environ, QT_QPA_PLATFORM="cocoa" if sys.platform == "darwin" else "offscreen", QT_QUICK_BACKEND="software")
            run(executable, "--smoke-test", env=env)
        else:
            run(executable, "--test-mode", "--filter", "offline")
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(payload, output, symlinks=True)
    print(f"Build ready: {output}\nKeep the whole folder when copying the app.")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("gui", "cli"), default="gui")
    parser.add_argument("--output", type=Path, help="New output directory; existing folders are never overwritten")
    parser.add_argument("--msys2-root", type=Path, help="MSYS2 directory for Windows FFmpeg builds, e.g. C:/msys64")
    parser.add_argument("--without-ffmpeg", action="store_true", help="Use an FFmpeg already on the user's PATH")
    parser.add_argument("--without-pocketbase", action="store_true", help="Omit bundled history/statistics server")
    parser.add_argument("--without-tor", action="store_true", help="Omit managed Tor; use direct service routing or system Tor")
    args = parser.parse_args()
    if sys.platform == "win32" and not args.without_ffmpeg and args.msys2_root is None:
        parser.error("Windows FFmpeg builds need --msys2-root C:/msys64; see docs/INSTALLATION.md")
    build(args)


if __name__ == "__main__":
    main()
