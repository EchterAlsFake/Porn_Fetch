"""Reject iOS artifacts missing the PyJWT package used during startup."""

import plistlib
import runpy
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
check_app = runpy.run_path(str(ROOT / "packaging/check_ios_app.py"))["check_app"]


class IOSAppTests(unittest.TestCase):
    def test_pyjwt_reaches_the_app_and_ipa_with_distribution_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            app = root / "Payload/PornFetch.app"
            jwt = app / "packages/jwt"
            jwt.mkdir(parents=True)
            for name in ("__init__", "api_jwt", "api_jws", "algorithms"):
                (jwt / f"{name}.py").write_text("# PyJWT module\n")
            metadata = app / "packages/PyJWT-2.15.1.dist-info/METADATA"
            metadata.parent.mkdir()
            metadata.write_text("Name: PyJWT\nVersion: 2.15.1\n")
            (app / "Info.plist").write_bytes(plistlib.dumps({"CFBundleExecutable": "PornFetch_bin"}))
            check_app(app)
            ipa = root / "app.ipa"
            with zipfile.ZipFile(ipa, "w") as archive:
                for path in app.rglob("*"):
                    if path.is_file():
                        archive.write(path, path.relative_to(root).as_posix())
            check_app(ipa)
            metadata.unlink()
            with self.assertRaisesRegex(ValueError, "PyJWT distribution metadata"):
                check_app(app)

    def test_snapshot_without_jwt_fails_even_when_the_host_has_pyjwt(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            app = root / "Payload/PornFetch.app"
            packages = app / "packages"
            packages.mkdir(parents=True)
            (app / "Info.plist").write_bytes(plistlib.dumps({"CFBundleExecutable": "PornFetch_bin"}))
            with self.assertRaisesRegex(ValueError, "jwt.*PyJWT"):
                check_app(app)
            ipa = root / "app.ipa"
            with zipfile.ZipFile(ipa, "w") as archive:
                archive.write(app / "Info.plist", "Payload/PornFetch.app/Info.plist")
            with self.assertRaisesRegex(ValueError, "jwt.*PyJWT"):
                check_app(ipa)


if __name__ == "__main__":
    unittest.main()
