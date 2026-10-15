"""Build-time automation tool to stage packages, run repogen, and build Qt IFW installers."""
from __future__ import annotations

import argparse
import logging
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.database.installer import resolve_platform  # noqa: E402
from src.shared.version import RELEASE_TIMESTAMP, __version__  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("qt_ifw_builder")


def prepare_staging_directory(
    staging_dir: Path,
    dist_dir: Path,
    pocketbase_binary: Path | None,
    target_platform: str,
    target_arch: str,
    version: str,
    ffmpeg_binary: Path | None = None,
) -> tuple[Path, Path]:
    """Prepare config/ and packages/ directories for binarycreator and repogen."""
    template_config = PROJECT_ROOT / "packaging" / "installer" / "config" / "config.xml.template"
    package_templates = PROJECT_ROOT / "packaging" / "installer" / "packages"

    config_dir = staging_dir / "config"
    packages_dir = staging_dir / "packages"
    pkg_comp = packages_dir / "to.pornfetch.echteralsfake"
    data_dest = pkg_comp / "data"

    # Staging may be reused; old payload files must not leak into another component.
    if packages_dir.exists():
        shutil.rmtree(packages_dir)
    config_dir.mkdir(parents=True, exist_ok=True)
    data_dest.mkdir(parents=True, exist_ok=True)
    for asset in template_config.parent.glob("*.qss"):
        shutil.copy2(asset, config_dir)

    graphics_dir = PROJECT_ROOT / "src" / "frontend" / "graphics"
    for suffix in ("png", "ico", "icns"):
        shutil.copy2(graphics_dir / f"logo_transparent.{suffix}", config_dir)

    # 1. Render config.xml
    repo_tag = f"{target_platform}_{target_arch}"
    config_xml_text = template_config.read_text(encoding="utf-8")
    config_xml_text = config_xml_text.replace("@TARGET_REPO@", repo_tag)
    config_xml_text = config_xml_text.replace("<Version>3.9.0</Version>", f"<Version>{version}</Version>")
    config_dest = config_dir / "config.xml"
    config_dest.write_text(config_xml_text, encoding="utf-8")

    # 2. Copy meta files (package.xml, installscript.qs)
    for template in package_templates.iterdir():
        meta_dest = packages_dir / template.name / "meta"
        meta_dest.mkdir(parents=True, exist_ok=True)
        for f in (template / "meta").iterdir():
            content = f.read_text(encoding="utf-8")
            if f.name == "package.xml":
                content = content.replace("<Version>3.9.0</Version>", f"<Version>{version}</Version>")
                release_date = datetime.fromtimestamp(RELEASE_TIMESTAMP, timezone.utc).strftime("%Y-%m-%d")
                content = re.sub(r"<ReleaseDate>.*?</ReleaseDate>", f"<ReleaseDate>{release_date}</ReleaseDate>", content)
            (meta_dest / f.name).write_text(content, encoding="utf-8")

    # 3. Copy application distribution files into data/
    logger.info("Copying standalone distribution files from %s to %s...", dist_dir, data_dest)
    for item in dist_dir.iterdir():
        dest = data_dest / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)

    # Ensure executable name matches expected "Porn Fetch" / "Porn Fetch.exe"
    if target_platform == "windows":
        if (data_dest / "main.exe").is_file() and not (data_dest / "Porn Fetch.exe").is_file():
            shutil.copy2(data_dest / "main.exe", data_dest / "Porn Fetch.exe")
    elif target_platform == "linux":
        if (data_dest / "main.bin").is_file() and not (data_dest / "Porn Fetch").is_file():
            shutil.copy2(data_dest / "main.bin", data_dest / "Porn Fetch")
            (data_dest / "Porn Fetch").chmod(0o755)

    # 4. Resolve the tools before removing bundled copies from the core payload.
    # Optional tools live outside the macOS app so adding/removing them does not
    # invalidate the application's code signature.
    pb_bin = pocketbase_binary
    if not pb_bin or not pb_bin.is_file():
        os_label, _, binary_name = resolve_platform(target_platform, target_arch)
        candidates = [
            PROJECT_ROOT / "third_party" / binary_name,
            PROJECT_ROOT / "packaging" / "pocketbase" / os_label / binary_name,
            PROJECT_ROOT / binary_name,
        ]
        for candidate in candidates:
            if candidate.is_file():
                pb_bin = candidate
                break

    if not pb_bin or not pb_bin.is_file():
        raise FileNotFoundError(
            f"PocketBase binary was not found for {target_platform}_{target_arch}. "
            "Pass --pocketbase-binary or fetch it before packaging."
        )

    ff_bin = ffmpeg_binary
    ff_name = "ffmpeg.exe" if target_platform == "windows" else "ffmpeg"
    if not ff_bin or not ff_bin.is_file():
        ff_candidates = [
            PROJECT_ROOT / "third_party" / ff_name,
            PROJECT_ROOT / "packaging" / "ffmpeg" / target_platform / target_arch / ff_name,
            PROJECT_ROOT / ff_name,
        ]
        for cand in ff_candidates:
            if cand.is_file():
                ff_bin = cand
                break

    if not ff_bin or not ff_bin.is_file():
        raise FileNotFoundError(
            f"FFmpeg binary was not found for {target_platform}_{target_arch}. "
            "Pass --ffmpeg-binary or fetch it before packaging."
        )

    pb_name = "pocketbase.exe" if target_platform == "windows" else "pocketbase"
    for tool, source, name in (("pocketbase", pb_bin, pb_name), ("ffmpeg", ff_bin, ff_name)):
        destination = packages_dir / f"to.pornfetch.echteralsfake.{tool}" / "data" / "third_party" / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        if target_platform != "windows":
            destination.chmod(0o755)

    tool_names = {"pocketbase", "pocketbase.exe", "ffmpeg", "ffmpeg.exe"}
    for path in data_dest.rglob("*"):
        if path.is_file() and (path.name in tool_names or path.name.removesuffix(".sha256") in tool_names):
            path.unlink()

    return config_dest, packages_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Stage files and run repogen / binarycreator for Qt Installer Framework.",
    )
    parser.add_argument(
        "--dist-dir",
        required=True,
        type=Path,
        help="Path to compiled Nuitka standalone output directory",
    )
    parser.add_argument(
        "--platform",
        default=platform.system().lower(),
        choices=["windows", "linux", "macos", "darwin", "win32"],
        help="Target OS platform (default: current OS)",
    )
    parser.add_argument(
        "--arch",
        default=platform.machine().lower(),
        help="Target CPU architecture: x64/amd64, arm64/aarch64 (default: current arch)",
    )
    parser.add_argument(
        "--pocketbase-binary",
        type=Path,
        default=None,
        help="Explicit path to PocketBase executable",
    )
    parser.add_argument(
        "--ffmpeg-binary",
        type=Path,
        default=None,
        help="Explicit path to FFmpeg executable",
    )
    parser.add_argument(
        "--output-repo",
        type=Path,
        default=None,
        help="Destination directory for repogen online repository",
    )
    parser.add_argument(
        "--output-installer",
        type=Path,
        default=None,
        help="Destination path for binarycreator installer binary (e.g. PornFetch-Setup.exe)",
    )
    parser.add_argument(
        "--staging-dir",
        type=Path,
        default=PROJECT_ROOT / "build_installer_tmp",
        help="Temporary directory for staging config and packages",
    )
    parser.add_argument(
        "--version",
        default=__version__,
        help=f"Application version (default: {__version__})",
    )

    args = parser.parse_args(argv)

    raw_os = "windows" if args.platform in {"win32", "windows"} else "darwin" if args.platform in {"darwin", "macos"} else "linux"
    raw_arch = "amd64" if args.arch in {"x86_64", "amd64", "x64"} else "arm64" if args.arch in {"aarch64", "arm64"} else args.arch

    if not args.dist_dir.is_dir():
        logger.error("Distribution directory does not exist: %s", args.dist_dir)
        return 1

    staging_dir = args.staging_dir.resolve()
    staging_dir.mkdir(parents=True, exist_ok=True)

    config_xml, packages_dir = prepare_staging_directory(
        staging_dir=staging_dir,
        dist_dir=args.dist_dir.resolve(),
        pocketbase_binary=args.pocketbase_binary.resolve() if args.pocketbase_binary else None,
        target_platform=raw_os,
        target_arch=raw_arch,
        version=args.version,
        ffmpeg_binary=args.ffmpeg_binary.resolve() if args.ffmpeg_binary else None,
    )

    if raw_os == "darwin":
        # Removing the previously bundled tools changes the signed app resources.
        app = packages_dir / "to.pornfetch.echteralsfake" / "data" / "Porn Fetch.app"
        subprocess.run(["codesign", "--force", "--deep", "--sign", "-", str(app)], check=True)
        subprocess.run(["codesign", "--verify", "--deep", "--strict", str(app)], check=True)

    # 1. Run repogen if --output-repo is specified
    if args.output_repo:
        repogen = shutil.which("repogen") or "repogen"
        repo_out = args.output_repo.resolve()
        repo_out.parent.mkdir(parents=True, exist_ok=True)
        cmd_repo = [repogen, "-p", str(packages_dir), str(repo_out)]
        logger.info("Generating online repository: %s", " ".join(cmd_repo))
        try:
            subprocess.run(cmd_repo, check=True)
            logger.info("Online repository successfully created at: %s", repo_out)
        except Exception as exc:
            logger.error("Failed to run repogen: %s", exc)
            return 1

    # 2. Run binarycreator if --output-installer is specified
    if args.output_installer:
        binarycreator = shutil.which("binarycreator") or "binarycreator"
        inst_out = args.output_installer.resolve()
        inst_out.parent.mkdir(parents=True, exist_ok=True)
        cmd_inst = [binarycreator, "--hybrid", "-c", str(config_xml), "-p", str(packages_dir), str(inst_out)]
        logger.info("Generating hybrid installer: %s", " ".join(cmd_inst))
        try:
            subprocess.run(cmd_inst, check=True)
            logger.info("Installer successfully created at: %s", inst_out)
        except Exception as exc:
            logger.error("Failed to run binarycreator: %s", exc)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
