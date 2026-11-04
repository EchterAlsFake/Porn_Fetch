"""Developer ID signing and notarization using a temporary CI keychain."""

from __future__ import annotations

import argparse
import base64
import json
import os
import plistlib
import re
import secrets
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILE = "pornfetch-notary"
MACHO_MAGIC = {
    bytes.fromhex(value)
    for value in (
        "feedface",
        "cefaedfe",
        "feedfacf",
        "cffaedfe",
        "cafebabe",
        "bebafeca",
        "cafebabf",
        "bfbafeca",
    )
}


def run(command, *, sensitive=False, check=True, timeout=None):
    arguments = list(map(str, command))
    tools = {name: "/usr/bin/" + name for name in ("security", "codesign", "xcrun", "ditto", "hdiutil")}
    tools["spctl"] = "/usr/sbin/spctl"
    arguments[0] = tools.get(arguments[0], arguments[0])
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=timeout)
    if check and result.returncode:
        # Never include subprocess arguments: security/notarytool setup receives credentials.
        detail = "" if sensitive else "\n" + result.stderr.strip()[-4000:]
        raise RuntimeError(f"{command[0]} failed (exit {result.returncode}).{detail}")
    return result


def signing_directory():
    return Path(os.environ["RUNNER_TEMP"]) / "pornfetch-macos-signing"


def cleanup():
    directory = signing_directory()
    state = directory / "state.json"
    if not state.is_file():
        return
    original = json.loads(state.read_text())["keychains"]
    keychain = directory / "signing.keychain-db"
    try:
        run(["security", "list-keychains", "-d", "user", "-s", *original], sensitive=True)
    finally:
        result = run(["security", "delete-keychain", keychain], sensitive=True, check=False)
        if result.returncode and keychain.exists():
            raise RuntimeError("Could not delete the temporary macOS signing keychain")
        shutil.rmtree(directory)


def setup():
    names = ("MACOS_CERT_P12_BASE64", "MACOS_CERT_PASSWORD", "APPLE_ID", "APPLE_APP_PASSWORD", "APPLE_TEAM_ID")
    missing = [name for name in names if not os.environ.get(name)]
    if missing:
        raise ValueError("Missing signing environment secrets: " + ", ".join(missing))
    team = os.environ["APPLE_TEAM_ID"]
    if not re.fullmatch(r"[A-Z0-9]{10}", team):
        raise ValueError("APPLE_TEAM_ID must be the ten-character Apple Developer team ID")
    directory = signing_directory()
    directory.mkdir(mode=0o700)
    keychain = directory / "signing.keychain-db"
    certificate = directory / "certificate.p12"
    original = shlex.split(run(["security", "list-keychains", "-d", "user"], sensitive=True).stdout)
    (directory / "state.json").write_text(json.dumps({"keychains": original}), encoding="utf-8")
    try:
        certificate.write_bytes(base64.b64decode("".join(os.environ["MACOS_CERT_P12_BASE64"].split()), validate=True))
        certificate.chmod(0o600)
        password = secrets.token_urlsafe(32)
        run(["security", "create-keychain", "-p", password, keychain], sensitive=True)
        run(["security", "set-keychain-settings", "-lut", "21600", keychain], sensitive=True)
        run(["security", "unlock-keychain", "-p", password, keychain], sensitive=True)
        run(
            [
                "security",
                "import",
                certificate,
                "-k",
                keychain,
                "-P",
                os.environ["MACOS_CERT_PASSWORD"],
                "-t",
                "cert",
                "-f",
                "pkcs12",
                "-T",
                "/usr/bin/codesign",
                "-T",
                "/usr/bin/security",
            ],
            sensitive=True,
        )
        run(
            [
                "security",
                "set-key-partition-list",
                "-S",
                "apple-tool:,apple:,codesign:",
                "-s",
                "-k",
                password,
                keychain,
            ],
            sensitive=True,
        )
        run(["security", "list-keychains", "-d", "user", "-s", str(keychain), *original], sensitive=True)
        identities = run(["security", "find-identity", "-v", "-p", "codesigning", keychain], sensitive=True).stdout
        matches = re.findall(
            r'\b([A-Fa-f0-9]{40})\s+"Developer ID Application:[^"\n]*\(' + re.escape(team) + r'\)"', identities
        )
        if len(matches) != 1:
            raise ValueError(
                "The P12 must contain exactly one valid Developer ID Application certificate and private key for APPLE_TEAM_ID"
            )
        run(
            [
                "xcrun",
                "notarytool",
                "store-credentials",
                PROFILE,
                "--keychain",
                keychain,
                "--apple-id",
                os.environ["APPLE_ID"],
                "--password",
                os.environ["APPLE_APP_PASSWORD"],
                "--team-id",
                team,
            ],
            sensitive=True,
        )
        with Path(os.environ["GITHUB_ENV"]).open("a", encoding="utf-8") as output:
            output.write(
                f"PORN_FETCH_MACOS_SIGNING=1\nPORN_FETCH_MACOS_SIGN_IDENTITY={matches[0]}\n"
                f"PORN_FETCH_MACOS_KEYCHAIN={keychain}\nPORN_FETCH_MACOS_TEAM_ID={team}\n"
            )
    except BaseException:
        cleanup()
        raise
    finally:
        certificate.unlink(missing_ok=True)
    print("Developer ID identity and notarization credentials are ready in the temporary keychain.")


def is_macho(path):
    if path.is_symlink() or not path.is_file():
        return False
    with path.open("rb") as source:
        return source.read(4) in MACHO_MAGIC


def verify(path):
    team = os.environ["PORN_FETCH_MACOS_TEAM_ID"]
    requirement = (
        "anchor apple generic and certificate leaf[field.1.2.840.113635.100.6.1.13] exists "
        f'and certificate leaf[subject.OU] = "{team}"'
    )
    command = ["codesign", "--verify", "--all-architectures", "--strict", "--verbose=2", "-R", requirement]
    if path.suffix == ".app":
        command.append("--deep")
    run([*command, path])


def sign(path, runtime="none"):
    """Sign physical Mach-O files, then enclosing bundles; never sign using --deep."""
    path = Path(path).absolute()
    if path.is_symlink() or not path.exists():
        raise ValueError(f"Missing or symlinked signing input: {path}")
    files = [item for item in path.rglob("*") if is_macho(item)] if path.is_dir() else [path]
    if not files or (path.is_file() and path.suffix != ".dmg" and not is_macho(path)):
        raise ValueError(f"No Mach-O code to sign: {path}")
    containers = set()
    for binary in files:
        for parent in binary.parents:
            if parent.is_relative_to(path) and parent.suffix in {".app", ".framework", ".xpc", ".appex", ".bundle"}:
                containers.add(parent)
    entitlements = ROOT / "packaging" / f"macos-{runtime}.entitlements.plist" if runtime != "none" else None
    if runtime != "none" and path.is_dir() and path.suffix != ".app":
        raise ValueError("Runtime entitlements require an app bundle or a standalone executable")
    main_binary = path
    if path.suffix == ".app":
        with (path / "Contents/Info.plist").open("rb") as source:
            executable = plistlib.load(source)["CFBundleExecutable"]
        if Path(executable).name != executable:
            raise ValueError("Invalid CFBundleExecutable")
        main_binary = path / "Contents/MacOS" / executable
    for item in [*sorted(files), *sorted(containers, key=lambda p: (-len(p.parts), str(p)))]:
        command = [
            "codesign",
            "--force",
            "--sign",
            os.environ["PORN_FETCH_MACOS_SIGN_IDENTITY"],
            "--keychain",
            os.environ["PORN_FETCH_MACOS_KEYCHAIN"],
            "--timestamp",
        ]
        if item.suffix != ".dmg":
            command.extend(["--options", "runtime"])
        if entitlements and item in {path, main_binary}:
            command.extend(["--entitlements", entitlements, "--generate-entitlement-der"])
        run([*command, item])
        verify(item)
    print(f"Developer ID signature verified: {path.name}")


def submit(archive):
    arguments = ["--keychain-profile", PROFILE, "--keychain", os.environ["PORN_FETCH_MACOS_KEYCHAIN"]]
    result = run(
        ["xcrun", "notarytool", "submit", archive, *arguments, "--wait", "--timeout", "30m", "--output-format", "json"],
        check=False,
    )
    try:
        response = json.loads(result.stdout)
    except ValueError:
        raise RuntimeError(
            "notarytool did not return a submission result; check Apple service availability and the signing credentials"
        ) from None
    identifier = response.get("id", "")
    if re.fullmatch(r"[A-Za-z0-9-]+", identifier):
        reports = Path(os.environ["RUNNER_TEMP"]) / "porn-fetch-build-logs/notarization"
        reports.mkdir(parents=True, exist_ok=True)
        (reports / f"{identifier}.json").write_text(json.dumps(response, indent=2), encoding="utf-8")
        run(["xcrun", "notarytool", "log", identifier, *arguments, reports / f"{identifier}.log.json"], check=False)
    if result.returncode or response.get("status") != "Accepted":
        raise RuntimeError(
            f"Apple notarization was not accepted (submission {identifier or 'unknown'}). See the notarization build logs."
        )
    print(f"Apple notarization accepted: {identifier}")


def staple(path):
    run(["xcrun", "stapler", "staple", path])
    run(["xcrun", "stapler", "validate", path])
    verify(path)
    if path.suffix == ".app":
        run(["spctl", "--assess", "--type", "execute", "--verbose=2", path])
    else:
        run(["spctl", "--assess", "--type", "open", "--context", "context:primary-signature", "--verbose=2", path])


def notarize(path):
    path = Path(path).absolute()
    if path.suffix not in {".app", ".dmg"}:
        raise ValueError("Use notarize-files for standalone command-line executables")
    verify(path)
    if path.suffix == ".app":
        with tempfile.TemporaryDirectory(prefix="pornfetch-notary-", dir=os.environ["RUNNER_TEMP"]) as temporary:
            archive = Path(temporary) / "application.zip"
            run(["ditto", "-c", "-k", "--sequesterRsrc", "--keepParent", path, archive])
            submit(archive)
    else:
        submit(path)
    staple(path)


def notarize_files(paths):
    # Apple records the executable hashes. ZIPs and bare Mach-O files cannot be stapled.
    with tempfile.TemporaryDirectory(prefix="pornfetch-notary-cli-", dir=os.environ["RUNNER_TEMP"]) as temporary:
        directory = Path(temporary)
        payload = directory / "payload"
        payload.mkdir()
        for path in paths:
            verify(path)
            if (payload / path.name).exists():
                raise ValueError("Notarization inputs must have distinct names")
            if path.is_dir() and path.suffix == ".app":
                shutil.copytree(path, payload / path.name, symlinks=True)
            else:
                shutil.copy2(path, payload / path.name)
        archive = directory / "command-line-tools.zip"
        run(["ditto", "-c", "-k", "--keepParent", payload, archive])
        submit(archive)
        for path in paths:
            if path.suffix == ".app":
                staple(path)


def verify_install(installer):
    """Exercise IFW's signed maintenance-bundle installation on an isolated target."""
    with tempfile.TemporaryDirectory(prefix="pornfetch-install-check-", dir=os.environ["RUNNER_TEMP"]) as temporary:
        target = Path(temporary) / "application"
        with (installer / "Contents/Info.plist").open("rb") as source:
            executable = plistlib.load(source)["CFBundleExecutable"]
        run(
            [
                installer / "Contents/MacOS" / executable,
                "--root",
                target,
                "--accept-licenses",
                "--default-answer",
                "--confirm-command",
                "install",
            ],
            timeout=180,
        )
        for bundle in (target / "Porn Fetch.app", target / "maintenancetool.app"):
            verify(bundle)
            run(["xcrun", "stapler", "validate", bundle])
        maintenance = target / "maintenancetool.app"
        with (maintenance / "Contents/Info.plist").open("rb") as source:
            executable = plistlib.load(source)["CFBundleExecutable"]
        run(
            [maintenance / "Contents/MacOS" / executable, "--default-answer", "--confirm-command", "purge"], timeout=180
        )


def sign_installer(image):
    """IFW generates a DMG; its installer application must be signed before the image."""
    image = image.absolute()
    with tempfile.TemporaryDirectory(prefix="pornfetch-installer-", dir=os.environ["RUNNER_TEMP"]) as temporary:
        directory = Path(temporary)
        mount = directory / "mount"
        mount.mkdir()
        stage = directory / "stage"
        stage.mkdir()
        run(["hdiutil", "attach", "-readonly", "-nobrowse", "-mountpoint", mount, image])
        try:
            for item in mount.iterdir():
                if item.name in {".Trashes", ".fseventsd", ".Spotlight-V100", ".DocumentRevisions-V100"}:
                    continue
                if item.is_symlink():
                    (stage / item.name).symlink_to(os.readlink(item))
                else:
                    run(["ditto", item, stage / item.name])
        finally:
            run(["hdiutil", "detach", mount])
        apps = [p for p in stage.glob("*.app") if p.is_dir() and not p.is_symlink()]
        if len(apps) != 1:
            raise ValueError("Expected exactly one installer application in the IFW disk image")
        sign(apps[0], "qt")
        notarize(apps[0])
        verify_install(apps[0])
        rebuilt = directory / "installer.dmg"
        run(
            [
                "hdiutil",
                "create",
                "-volname",
                "Porn Fetch Setup",
                "-srcfolder",
                stage,
                "-ov",
                "-format",
                "UDZO",
                rebuilt,
            ]
        )
        sign(rebuilt)
        notarize(rebuilt)
        shutil.copy2(rebuilt, image)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("setup")
    commands.add_parser("cleanup")
    signer = commands.add_parser("sign")
    signer.add_argument("paths", type=Path, nargs="+")
    signer.add_argument("--runtime", choices=("none", "python", "qt"), default="none")
    for name in ("notarize", "sign-installer"):
        commands.add_parser(name).add_argument("path", type=Path)
    commands.add_parser("notarize-files").add_argument("paths", type=Path, nargs="+")
    args = parser.parse_args()
    if sys.platform != "darwin":
        parser.error("macOS signing requires Apple's security, codesign, notarytool and stapler tools")
    try:
        if args.command == "setup":
            setup()
        elif args.command == "cleanup":
            cleanup()
        elif args.command == "sign":
            for path in args.paths:
                sign(path, args.runtime)
        elif args.command == "notarize":
            notarize(args.path)
        elif args.command == "notarize-files":
            notarize_files(args.paths)
        else:
            sign_installer(args.path)
    except (RuntimeError, ValueError, OSError) as error:
        parser.exit(1, f"macOS signing failed: {error}\n")


if __name__ == "__main__":
    main()
