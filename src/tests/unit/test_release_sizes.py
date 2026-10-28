"""Focused payload accounting and compression selection checks."""
import configparser
import io
import json
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from src.tests.unit.test_cli_self_update import load_script

reporter = load_script("report_sizes")
repository = load_script("generate_repository")
android = load_script("prepare_android_ci")


class ReleaseSizeTests(unittest.TestCase):
    def test_directory_zip_and_tar_report_same_content_and_duplicates(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            folder = root / "payload"
            folder.mkdir()
            (folder / "a").write_bytes(b"content")
            (folder / "b").write_bytes(b"content")
            (folder / "alias").symlink_to("a")
            zipped = root / "payload.apk"
            with zipfile.ZipFile(zipped, "w", zipfile.ZIP_DEFLATED) as archive:
                for name in ("a", "b"):
                    archive.write(folder / name, name)
            tarred = root / "payload.tar.gz"
            with tarfile.open(tarred, "w:gz") as archive:
                for name in ("a", "b"):
                    info = tarfile.TarInfo(name)
                    info.size = 7
                    archive.addfile(info, io.BytesIO(b"content"))
            for path in (folder, zipped, tarred):
                report = reporter.inventory(path)
                self.assertEqual(report["payload_bytes"], 14)
                self.assertEqual(report["duplicates"][0]["redundant_bytes"], 7)

    def test_android_excludes_development_sources_but_keeps_runtime_assets(self):
        project_root = Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "packaging").mkdir()
            for name in ("buildozer.spec", "packaging/pysidedeploy_android.spec"):
                (root / name).write_text((project_root / name).read_text())
            android.prepare(root, root / ".venv", "3.9")
            config = configparser.ConfigParser()
            config.read(root / "buildozer.spec")
            excluded = config["app"]["source.exclude_dirs"].split(",")
            self.assertIn("src/tests", excluded)
            self.assertIn("src/frontend/translations/ts", excluded)
            self.assertNotIn("docs", excluded)
            self.assertNotIn("src/frontend/translations/qm", excluded)
            self.assertIn("json", config["app"]["source.include_exts"].split(","))

    def test_compression_benchmark_keeps_smallest_candidate_and_measurements(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "setup.exe"

            def build(command, **kwargs):
                level = int(command[command.index("--compression") + 1])
                Path(command[-1]).write_bytes(b"x" * {5: 100, 7: 80, 9: 90}[level])

            with patch.object(repository.subprocess, "run", side_effect=build):
                repository.run_archive_tool(["binarycreator", "--hybrid", str(output)], output, 5, True)
            self.assertEqual(output.stat().st_size, 80)
            results = json.loads(output.with_name("setup.exe.compression.json").read_text())
            self.assertEqual(results["selected_level"], 7)
            self.assertEqual(len(results["results"]), 3)


if __name__ == "__main__":
    unittest.main()
