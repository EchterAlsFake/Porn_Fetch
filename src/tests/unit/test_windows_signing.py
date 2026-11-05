"""Offline checks for signing payload isolation and the IFW maintenance component."""
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from src.shared.release import validate_ifw_packages
from src.shared.version import RELEASE_TIMESTAMP
from src.tests.unit.test_cli_self_update import load_script

payload = load_script("sign_pyinstaller_payload")
repository = load_script("generate_repository")


class WindowsSigningTests(unittest.TestCase):
    def test_cli_signs_private_native_copies_and_preserves_the_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "wheel"
            source.mkdir()
            entries = []
            for name, kind in (("tor.exe", "BINARY"), ("runtime.dll", "BINARY"),
                               ("extension.pyd", "EXTENSION"), ("helper.exe", "DATA"), ("ca.pem", "DATA")):
                path = source / name
                path.write_bytes(b"original")
                entries.append((f"nested/{name}", str(path), kind))

            def sign(command, **kwargs):
                self.assertEqual(command[:3], ["pwsh", "-NoProfile", "-File"])
                self.assertEqual(Path(command[3]).name, "sign_windows.ps1")
                self.assertIs(kwargs["check"], True)
                for path in Path(command[-1]).rglob("*"):
                    if path.is_file():
                        path.write_bytes(path.read_bytes() + b"-signed")

            with patch.object(payload.subprocess, "run", side_effect=sign):
                result = payload.sign_payload(entries, str(root / "build"))
            self.assertEqual([(name, kind) for name, _, kind in result],
                             [(name, kind) for name, _, kind in entries])
            for original, signed in zip(entries, result):
                self.assertEqual(Path(original[1]).read_bytes(), b"original")
                self.assertEqual(Path(signed[1]).read_bytes(),
                                 b"original" if signed[0].endswith(".pem") else b"original-signed")

    def test_cli_does_not_package_after_signing_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            binary = root / "tor.exe"
            binary.write_bytes(b"original")
            with patch.object(payload.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "pwsh")):
                with self.assertRaises(subprocess.CalledProcessError):
                    payload.sign_payload([("tor.exe", str(binary), "BINARY")], str(root / "build"))
            self.assertEqual(binary.read_bytes(), b"original")

    def test_signed_maintenance_component_survives_staging_and_release_validation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            dist = root / "dist"
            dist.mkdir()
            (dist / "Porn Fetch.exe").write_bytes(b"signed application")
            for name in ("pocketbase.exe", "ffmpeg.exe", "installerbase.exe"):
                (root / name).write_bytes(b"signed " + name.encode())
            _, packages = repository.prepare_staging_directory(
                root / "staging", dist, root / "pocketbase.exe", "windows", "amd64", "3.9.123",
                root / "ffmpeg.exe", maintenance_tool=root / "installerbase.exe",
            )
            core = "to.pornfetch.echteralsfake"
            component = packages / f"{core}.maintenance"
            self.assertEqual((component / "data/installerbase.exe").read_bytes(), b"signed installerbase.exe")
            metadata = ET.parse(component / "meta/package.xml")
            # IFW rejects Default and Virtual together, even when both are true.
            self.assertIsNone(metadata.find("Default"))
            # Essential splits every app release into a tool update and a second
            # app update after restart. The dependency keeps this tool required.
            self.assertIsNone(metadata.find("Essential"))
            for setting in ("ForcedInstallation", "Virtual"):
                self.assertEqual(metadata.findtext(setting), "true")
            self.assertEqual(metadata.findtext("Version"), "3.9.123")
            self.assertEqual(metadata.findtext("ReleaseDate"),
                             datetime.fromtimestamp(RELEASE_TIMESTAMP, timezone.utc).strftime("%Y-%m-%d"))
            self.assertIn('installer.setInstallerBaseBinary("@TargetDir@/installerbase.exe")',
                          (component / "meta/installscript.qs").read_text())
            self.assertEqual(ET.parse(packages / core / "meta/package.xml").findtext("Dependencies"),
                             f"{core}.maintenance")
            updates = ET.Element("Updates")
            for directory in packages.iterdir():
                package = ET.parse(directory / "meta/package.xml").getroot()
                package.tag = "PackageUpdate"
                ET.SubElement(package, "Name").text = directory.name
                updates.append(package)
            validate_ifw_packages(updates, "3.9.123", RELEASE_TIMESTAMP)
