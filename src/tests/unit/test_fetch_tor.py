"""Regression check for Tor's static dependencies on Ubuntu ARM64."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.tests.unit.test_cli_self_update import load_script

builder = load_script("fetch_tor")


class TorBuildTests(unittest.TestCase):
    def test_configure_uses_multiarch_static_library_directories(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            build = root / "source/tor-fixture"
            build.mkdir(parents=True)
            library_dir = root / "usr/lib/aarch64-linux-gnu"
            library_dir.mkdir(parents=True)
            for name in ("libevent.a", "libssl.a", "libcrypto.a", "libz.a"):
                (library_dir / name).touch()

            # Stop at configure: this test must not download or compile Tor.
            with patch.object(builder, "download", return_value=root / "tor.tar.gz"), \
                    patch.object(builder.tarfile, "open"), \
                    patch.object(builder.subprocess, "check_output", return_value=f"{library_dir}\n") as pkg_config, \
                    patch.object(builder.subprocess, "run", side_effect=RuntimeError("configure reached")) as configure:
                with self.assertRaisesRegex(RuntimeError, "configure reached"):
                    builder.build_linux_arm64(
                        {"linux_arm64_source": {"url": "fixture", "sha256": "fixture"}}, root / "output", root)

            arguments = configure.call_args.args[0]
            self.assertIn("--enable-static-tor", arguments)
            for package in ("libevent", "openssl", "zlib"):
                pkg_config.assert_any_call(["pkg-config", "--variable=libdir", package], text=True)
                self.assertIn(f"--with-{package}-dir={library_dir}", arguments)
                self.assertNotIn(f"--with-{package}-dir=/usr", arguments)
            self.assertEqual(configure.call_args.kwargs, {"cwd": build, "check": True})
