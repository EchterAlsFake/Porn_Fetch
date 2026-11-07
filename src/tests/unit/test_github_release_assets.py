"""Exercise the release workflow's asset collection locally, without publishing."""

import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


@unittest.skipUnless(os.name == "posix" and shutil.which("bash") and shutil.which("zip"),
                     "Release collection requires a POSIX host with Bash and zip")
class GitHubReleaseAssetTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.artifacts = self.workspace / "all_artifacts"
        self.artifacts.mkdir()
        self.output = self.workspace / "dist_release"
        workflow = (ROOT / ".github/workflows/build_all.yml").read_text()
        step = workflow.split("      - name: Prepare Release Assets\n", 1)[1]
        step = step.split("      - name: Create or Update GitHub Release\n", 1)[0]
        self.script = textwrap.dedent(step.split("        run: |\n", 1)[1])

    def artifact(self, name, files):
        directory = self.artifacts / name
        directory.mkdir()
        for filename, content in files.items():
            target = directory / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)

    def prepare(self):
        return subprocess.run(["bash", "-c", self.script], cwd=self.workspace,
                              env=dict(os.environ, GITHUB_WORKSPACE=str(self.workspace)),
                              capture_output=True, text=True, timeout=20)

    def test_shared_legal_files_stay_bundled_and_prebuilt_packages_are_preserved(self):
        cli = "PornFetch_linux_CLI_x64"
        self.artifact(cli, {cli: b"cli", cli + ".sha256": b"checksum",
                            cli + "_LEGAL.zip": b"cli notices", "pocketbase": b"database",
                            "ffmpeg": b"media helper", "LICENSE": b"cli license"})
        gui = "PornFetch_windows_GUI_x64"
        self.artifact(gui, {gui + ".zip": b"signed windows archive", gui + ".zip.sha256": b"checksum",
                            gui + "_LEGAL.zip": b"windows notices", "LICENSE": b"windows license"})
        linux = "PornFetch_linux_GUI_arm64"
        self.artifact(linux, {linux + ".tar.gz": b"linux archive", linux + "_LEGAL.zip": b"linux notices",
                              "LICENSE": b"linux license"})
        for name in ("PornFetch_android_GUI_arm64-v8a.apk", "PornFetch_ios_GUI_arm64_resign.ipa",
                     "PornFetch_linux_GUI_x64_Setup.run", "PornFetch_ios_GUI_arm64_LEGAL.zip"):
            self.artifact(name, {name: b"direct asset"})
            self.artifact(name + ".sha256", {name + ".sha256": b"checksum"})
        self.artifact("IFW_repo_linux_x64", {"Updates.xml": b"repository"})
        self.artifact("build-gui-logs-linux-x64", {"build.log": b"diagnostics"})

        result = self.prepare()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.output / (gui + ".zip")).read_bytes(), b"signed windows archive")
        self.assertEqual((self.output / (linux + ".tar.gz")).read_bytes(), b"linux archive")
        self.assertFalse((self.output / (linux + ".zip")).exists())
        self.assertFalse((self.output / "LICENSE").exists())
        self.assertFalse((self.output / "pocketbase").exists())
        self.assertFalse((self.output / "ffmpeg").exists())
        self.assertFalse((self.output / "Updates.xml").exists())
        self.assertFalse((self.output / "build.log").exists())
        for directory in self.artifacts.glob("PornFetch_*"):
            for file in directory.glob("PornFetch_*"):
                self.assertEqual((self.output / file.name).read_bytes(), file.read_bytes())
        with zipfile.ZipFile(self.output / (cli + ".zip")) as archive:
            self.assertEqual(archive.read("LICENSE"), b"cli license")
            self.assertEqual(archive.read(cli + "_LEGAL.zip"), b"cli notices")
            self.assertEqual(archive.read("pocketbase"), b"database")
            self.assertEqual(archive.read("ffmpeg"), b"media helper")
            self.assertTrue(archive.getinfo(cli).external_attr >> 16 & 0o111)
            self.assertTrue(archive.getinfo("pocketbase").external_attr >> 16 & 0o111)
        self.assertTrue((self.output / "PornFetch_linux_GUI_x64_Setup.run").stat().st_mode & 0o111)

    def test_duplicate_platform_assets_still_fail(self):
        name = "PornFetch_windows_GUI_x64.zip"
        self.artifact("PornFetch_first", {name: b"first build"})
        self.artifact("PornFetch_second", {name: b"different build"})
        result = self.prepare()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Duplicate release asset: " + name, result.stderr)
