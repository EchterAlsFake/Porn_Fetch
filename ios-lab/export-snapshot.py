"""Preserve the experimental iOS lab, including build output, for GitHub transfer.

Writes small, inspectable first-party files into this directory and a complete
sanitized tar.zst snapshot outside the repository. Does not change the live lab.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import time

HERE = Path(__file__).resolve().parent
DEFAULT_LAB = Path("/Users/asuna/ios-lab")
SKIP_DIRS = {".git", ".ssh", ".gnupg", ".DS_Store", "xcuserdata"}
SKIP_PATHS = {
    "ssh": "private SSH identity and host configuration",
    "build/phone-original.ts": "downloaded media",
    "build/phone-remuxed.mp4": "downloaded media",
    "build/pornfetch-screenshot.png": "application screenshot may contain media thumbnails",
}
PRIVATE_NAMES = {"credentials", "credentials.toml", ".netrc", ".env", "cookies.txt",
                 "cookies.json", "id_ed25519", "id_rsa", "hosts.yml"}
SECRET = re.compile(rb"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,})")
URL = re.compile(r"https?://[^\s\"'<>]+")
PRIVATE_QUERY = re.compile(r"[?&](?:hash|token|access_token|session|signature|sig|key|password|ipa|hdl|validfrom|validto)=", re.I)


def sanitize(path: Path, data: bytes) -> bytes:
    """Scrub runtime URLs and local download titles without changing source code."""
    if SECRET.search(data):
        raise ValueError(f"Possible GitHub credential found in {path}; refusing export")
    if path.suffix.lower() not in {".log", ".json", ".txt", ".md", ".ips", ".err"}:
        return data
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    text = URL.sub(lambda m: m[0].split("?", 1)[0] + "?<redacted>"
                   if PRIVATE_QUERY.search(m[0]) else m[0], text)
    # Actual authorization headers/cookies in diagnostics must never be published.
    text = re.sub(r"(?im)^([^\n]*(?:Authorization|Cookie|Set-Cookie)\s*:\s*)[^\n]+$", r"\1<redacted>", text)
    if any(name in path.name for name in ["download-integrity", "phone-remuxed-integrity"]):
        text = re.sub(r'(?m)("path"\s*:\s*")[^"\n]+', r'\1<local-download>.mp4', text)
        text = re.sub(r"(?m)^(File:\s*).+$", r"\1<local-download>.mp4", text)
    return text.encode("utf-8")


def excluded(relative: Path) -> str | None:
    if relative.as_posix() in SKIP_PATHS:
        return SKIP_PATHS[relative.as_posix()]
    if relative.name in SKIP_DIRS:
        return "Git internals, per-user Xcode state or platform noise"
    if relative.name in PRIVATE_NAMES:
        return "private runtime configuration or credentials"
    return None


def first_party(relative: Path) -> bool:
    """Keep all experiments; bulk dependencies/output remain in the full archive."""
    s = relative.as_posix()
    if len(relative.parts) == 1:
        return True
    if s.startswith("native/"):
        return True
    if s.startswith("qt/") and not s.startswith("qt/deployment/"):
        return True
    if s.startswith("pornfetch/"):
        tail = Path(*relative.parts[1:])
        return (len(tail.parts) == 1 and tail.suffix in {".py", ".sh", ".md", ".txt", ".json"}
                or tail.parts[0] in {"app", "probe"} and "deployment" not in tail.parts)
    if s.startswith("device/"):
        tail = Path(*relative.parts[1:])
        if len(tail.parts) == 1:
            return True
        if tail.parts[0] in {"patches", "python-native", "qt-hello", "qt-quick-hello"}:
            return True
        if tail.parts[0] in {"app", "python-qt-hello"} and "deployment" not in tail.parts:
            return True
        if tail.parts[0] == "ffmpeg" and len(tail.parts) == 2:
            return True
        if s.startswith("device/native/packages/") and relative.name in {"ios_ffmpeg.py", "ios_remux_check.py"}:
            return True
    if s.startswith("build/") and len(relative.parts) == 2 and relative.suffix in {
        ".json", ".md", ".log", ".txt", ".png", ".ips", ".err", ".cmake", ".h", ".mm", ".cpp", ".mk"
    }:
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lab", type=Path, default=DEFAULT_LAB)
    parser.add_argument("--python-ios", type=Path, default=Path("/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    archive = args.output / "ios-lab-full-snapshot.tar.zst"
    if archive.exists():
        raise SystemExit(f"Refusing to overwrite {archive}")
    entries, omitted, changed = [], [], []
    copied = 0
    compressor = subprocess.Popen(["zstd", "-T4", "-3", "--quiet", "-o", str(archive)], stdin=subprocess.PIPE)
    started = time.monotonic()
    try:
        with tarfile.open(fileobj=compressor.stdin, mode="w|", format=tarfile.PAX_FORMAT) as bundle:
            for source_root, prefix in [(args.lab, Path("ios-lab")), (args.python_ios, Path("python-ios/3.15.0rc2"))]:
                for base, dirs, files in os.walk(source_root, followlinks=False):
                    dirs.sort(); files.sort()
                    relative_dir = Path(base).relative_to(source_root)
                    for name in dirs[:]:
                        relative = relative_dir / name
                        reason = excluded(relative)
                        if reason:
                            omitted.append({"path": str(prefix / relative), "reason": reason})
                            dirs.remove(name)
                    # Tar symlinked directories without following them.
                    links = [name for name in dirs if (Path(base) / name).is_symlink()]
                    for name in files + links:
                        path = Path(base) / name
                        relative = path.relative_to(source_root)
                        reason = excluded(relative)
                        if reason:
                            omitted.append({"path": str(prefix / relative), "reason": reason})
                            continue
                        if path.name.endswith(('.pyc', '.pyo')) and '__pycache__' not in path.parts:
                            # Retained in full archive; never copied to the source view.
                            pass
                        info = bundle.gettarinfo(str(path), str(prefix / relative))
                        entry = {"path": info.name, "size": info.size,
                                 "type": "symlink" if info.issym() else "hardlink" if info.islnk() else "file"}
                        if info.issym() or info.islnk():
                            entry["target"] = info.linkname
                            bundle.addfile(info)
                        elif info.isfile():
                            # Only text-like diagnostics need an in-memory transformation.
                            data = None
                            if path.stat().st_size < 16 * 1024**2 and path.suffix.lower() in {
                                ".log", ".json", ".txt", ".md", ".ips", ".err", ".sh", ".py", ".ini", ".conf", ".spec"
                            }:
                                original = path.read_bytes()
                                data = sanitize(path, original)
                                if data != original:
                                    changed.append(info.name)
                                info.size = len(data)
                                entry["size"] = info.size
                                bundle.addfile(info, io.BytesIO(data))
                            else:
                                with path.open("rb") as stream:
                                    bundle.addfile(info, stream)
                            if source_root == args.lab and first_party(relative) and "__pycache__" not in relative.parts:
                                dest = HERE / relative
                                dest.parent.mkdir(parents=True, exist_ok=True)
                                if data is not None:
                                    dest.write_bytes(data)
                                    dest.chmod(path.stat().st_mode & 0o777)
                                else:
                                    shutil.copy2(path, dest)
                                copied += 1
                        else:
                            raise ValueError(f"Unsupported special file: {path}")
                        entries.append(entry)
                        if len(entries) % 10000 == 0:
                            print(f"Archived {len(entries):,} entries ({time.monotonic()-started:.0f}s)", flush=True)
        compressor.stdin.close()
        if compressor.wait() != 0:
            raise RuntimeError("zstd failed")
    except BaseException:
        compressor.kill()
        compressor.wait()
        raise
    manifest = {"format": 1, "source_roots": [str(args.lab), str(args.python_ios)],
        "entries": len(entries), "uncompressed_file_bytes": sum(e["size"] for e in entries),
        "source_view_files": copied, "exclusions": omitted, "sanitized_text_files": changed,
        "files": entries}
    (args.output / "snapshot-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (HERE / "SNAPSHOT-CONTENTS.json").write_text(json.dumps({k:v for k,v in manifest.items() if k != "files"}, indent=2) + "\n")
    print(f"Snapshot complete: {archive.stat().st_size / 1024**3:.2f} GiB, {len(entries):,} entries; copied {copied} first-party files", flush=True)


if __name__ == "__main__":
    main()
