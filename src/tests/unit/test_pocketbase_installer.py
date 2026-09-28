"""Unit tests for PocketBase installer, platform resolution, and automated installation flows."""
from __future__ import annotations

import io
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.database.errors import PocketBaseError
from src.database.installer import (
    check_system_path,
    download_and_extract_pocketbase,
    get_default_bin_dir,
    get_pocketbase_download_url,
    install_pocketbase,
    resolve_platform,
    verify_pocketbase_binary,
)


class PocketBasePlatformResolutionTests(unittest.TestCase):
    def test_resolve_linux_amd64(self):
        os_label, arch_label, bin_name = resolve_platform("Linux", "x86_64")
        self.assertEqual(os_label, "linux")
        self.assertEqual(arch_label, "amd64")
        self.assertEqual(bin_name, "pocketbase")

    def test_resolve_linux_arm64(self):
        os_label, arch_label, bin_name = resolve_platform("linux", "aarch64")
        self.assertEqual(os_label, "linux")
        self.assertEqual(arch_label, "arm64")
        self.assertEqual(bin_name, "pocketbase")

    def test_resolve_windows_amd64(self):
        os_label, arch_label, bin_name = resolve_platform("Windows", "AMD64")
        self.assertEqual(os_label, "windows")
        self.assertEqual(arch_label, "amd64")
        self.assertEqual(bin_name, "pocketbase.exe")

    def test_resolve_windows_arm64(self):
        os_label, arch_label, bin_name = resolve_platform("win32", "arm64")
        self.assertEqual(os_label, "windows")
        self.assertEqual(arch_label, "arm64")
        self.assertEqual(bin_name, "pocketbase.exe")

    def test_resolve_macos_arm64(self):
        os_label, arch_label, bin_name = resolve_platform("Darwin", "arm64")
        self.assertEqual(os_label, "darwin")
        self.assertEqual(arch_label, "arm64")
        self.assertEqual(bin_name, "pocketbase")

    def test_resolve_macos_x64(self):
        os_label, arch_label, bin_name = resolve_platform("macos", "x86_64")
        self.assertEqual(os_label, "darwin")
        self.assertEqual(arch_label, "amd64")
        self.assertEqual(bin_name, "pocketbase")

    def test_unsupported_os_raises(self):
        with self.assertRaises(PocketBaseError):
            resolve_platform("Solaris", "x86_64")

    def test_unsupported_arch_raises(self):
        with self.assertRaises(PocketBaseError):
            resolve_platform("Linux", "mips64")

    def test_download_url_format(self):
        url, bin_name = get_pocketbase_download_url("0.40.4", "linux", "x86_64")
        expected = "https://github.com/pocketbase/pocketbase/releases/download/v0.40.4/pocketbase_0.40.4_linux_amd64.zip"
        self.assertEqual(url, expected)
        self.assertEqual(bin_name, "pocketbase")


class PocketBaseInstallerTests(unittest.TestCase):
    def test_check_system_path_found(self):
        with tempfile.NamedTemporaryFile(suffix=".exe" if sys.platform == "win32" else "", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            if sys.platform != "win32":
                tmp_path.chmod(0o755)
            with patch("shutil.which", return_value=str(tmp_path)):
                found = check_system_path()
                self.assertIsNotNone(found)
                self.assertEqual(found, tmp_path.resolve())
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_check_system_path_missing(self):
        with patch("shutil.which", return_value=None):
            found = check_system_path()
            self.assertIsNone(found)

    def test_get_default_bin_dir(self):
        bin_dir = get_default_bin_dir()
        self.assertIsInstance(bin_dir, Path)
        self.assertTrue(str(bin_dir).endswith("bin"))

    def test_verify_binary_missing_file_raises(self):
        with self.assertRaises(PocketBaseError):
            verify_pocketbase_binary(Path("/path/to/nonexistent/pocketbase"))

    def test_verify_binary_success(self):
        with tempfile.NamedTemporaryFile(suffix=".exe" if sys.platform == "win32" else "", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            if sys.platform != "win32":
                tmp_path.chmod(0o755)
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stdout="pocketbase version 0.40.4\n", stderr="")
                ver = verify_pocketbase_binary(tmp_path)
                self.assertEqual(ver, "pocketbase version 0.40.4")
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_download_and_extract(self):
        with tempfile.TemporaryDirectory() as dest_tmp:
            dest_dir = Path(dest_tmp)
            bin_name = "pocketbase.exe" if sys.platform == "win32" else "pocketbase"

            # Create in-memory zip archive
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zf:
                zf.writestr(bin_name, b"dummy pocketbase content")
            zip_bytes = zip_buffer.getvalue()

            # Mock urlopen to return our zip bytes
            mock_response = MagicMock()
            mock_response.read.side_effect = [zip_bytes, b""]
            mock_response.headers.get.return_value = str(len(zip_bytes))
            mock_response.__enter__.return_value = mock_response

            with patch("urllib.request.urlopen", return_value=mock_response):
                with patch("src.database.installer.verify_pocketbase_binary", return_value="v0.40.4"):
                    installed = download_and_extract_pocketbase(
                        target_dir=dest_dir,
                        version="0.40.4",
                    )
                    self.assertEqual(installed, dest_dir / bin_name)
                    self.assertTrue(installed.exists())
                    self.assertEqual(installed.read_bytes(), b"dummy pocketbase content")

    def test_install_pocketbase_uses_path(self):
        with tempfile.NamedTemporaryFile(suffix=".exe" if sys.platform == "win32" else "", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            if sys.platform != "win32":
                tmp_path.chmod(0o755)
            with patch("src.database.installer.check_system_path", return_value=tmp_path):
                with patch("src.database.installer.verify_pocketbase_binary", return_value="v0.40.4"):
                    path, source = install_pocketbase(force_download=False)
                    self.assertEqual(path, tmp_path)
                    self.assertEqual(source, "path")
        finally:
            tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
