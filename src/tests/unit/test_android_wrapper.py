"""Unit tests for Android wrapper and lazy loading of optional dependencies."""
from __future__ import annotations

import http.cookiejar
import os
import sys
import unittest
from unittest.mock import patch


class TestAndroidWrapperAndLazyImports(unittest.TestCase):
    def test_get_site_cookies_without_browser_cookie3(self) -> None:
        """get_site_cookies should gracefully return empty CookieJar if browser_cookie3 is missing."""
        import src.backend.login_manager as lm

        with patch.dict(sys.modules, {"browser_cookie3": None}):
            jar = lm.get_site_cookies("pornhub")
            self.assertIsInstance(jar, http.cookiejar.CookieJar)
            self.assertEqual(len(list(jar)), 0)

    def test_cli_read_browser_cookies_without_browser_cookie3(self) -> None:
        """_read_browser_cookies should gracefully return empty CookieJar if browser_cookie3 is missing."""
        import src.cli.accounts as accounts

        with patch.dict(sys.modules, {"browser_cookie3": None}):
            jar = accounts._read_browser_cookies("pornhub")
            self.assertIsInstance(jar, http.cookiejar.CookieJar)
            self.assertEqual(len(list(jar)), 0)

    def test_import_entire_backend(self) -> None:
        """import_entire_backend should successfully load all backend modules."""
        import android_wrapper

        # Should execute without raising any exception
        android_wrapper.import_entire_backend()

    def test_wrapper_main_success_headless(self) -> None:
        """android_wrapper.py should run with --test in headless mode and return 0."""
        import subprocess

        env = os.environ.copy()
        env["QT_QPA_PLATFORM"] = "offscreen"
        cmd = [sys.executable, "android_wrapper.py", "--test", "--android"]
        proc = subprocess.run(cmd, env=env, capture_output=True, text=True, check=False)
        self.assertEqual(proc.returncode, 0, f"STDOUT: {proc.stdout}\nSTDERR: {proc.stderr}")
        self.assertIn("Backend imported successfully!", proc.stdout)
