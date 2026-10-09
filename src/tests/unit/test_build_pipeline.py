"""Focused offline regression checks for build artifact handling."""
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.tests.unit.test_cli_self_update import load_script

merger = load_script("merge_macos_bundles")
PROJECT_ROOT = Path(__file__).resolve().parents[3]


class MacBundleTests(unittest.TestCase):
    def test_merge_extracts_slices_from_fat_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            intel, arm, output = (root / name for name in ("intel", "arm", "universal"))
            for bundle in (intel, arm):
                bundle.mkdir()
                (bundle / "main").write_bytes(b"Mach-O")
            (arm / "arm-resource.txt").write_text("resource")
            with patch.object(merger, "is_macho", side_effect=lambda path: path.name == "main"), \
                 patch.object(merger.subprocess, "check_output", return_value="x86_64 arm64"), \
                 patch.object(merger.subprocess, "run") as run:
                merger.merge_bundles(intel, arm, output)
            commands = [call.args[0] for call in run.call_args_list]
            self.assertEqual(sum("-thin" in command for command in commands), 2)
            create = next(command for command in commands if "-create" in command)
            self.assertNotIn(str(output / "main"), create[2:-2])
            self.assertEqual(commands[-1], ["lipo", str(output / "main"), "-verify_arch", "x86_64", "arm64"])
            self.assertEqual((output / "arm-resource.txt").read_text(), "resource")

    def test_unmatched_native_binary_is_verified(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            intel, arm, output = (root / name for name in ("intel", "arm", "universal"))
            intel.mkdir()
            arm.mkdir()
            (intel / "main").write_bytes(b"intel only")
            with patch.object(merger, "is_macho", return_value=True), \
                 patch.object(merger.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "lipo")):
                with self.assertRaises(subprocess.CalledProcessError):
                    merger.merge_bundles(intel, arm, output)


class DeploymentInputTests(unittest.TestCase):
    def test_cli_upload_contract_includes_only_repository_directories(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            repository = base / "repository"
            (repository / "metadata").mkdir(parents=True)
            for role in ("root", "targets", "snapshot", "timestamp"):
                (repository / "metadata" / f"{role}.json").write_text("{}")
            (repository / "unrelated.pem").write_text("must not be uploaded")
            (base / "curl").write_text(
                '#!/bin/bash\n'
                'printf "%s\\n" "$@" > "$CAPTURE_ARGS"\n'
                'while [[ $# -gt 0 ]]; do\n'
                '  if [[ "$1" == --data-binary ]]; then cp "${2#@}" "$CAPTURE_TAR"; break; fi\n'
                '  shift\n'
                'done\n'
            )
            (base / "curl").chmod(0o755)
            for with_targets in (False, True):
                with self.subTest(with_targets=with_targets):
                    if with_targets:
                        (repository / "targets").mkdir()
                        (repository / "targets" / "bundle.zip").write_bytes(b"test bundle")
                    archive = base / "upload.tar.gz"
                    arguments = base / "curl-args.txt"
                    subprocess.run(
                        ["bash", str(PROJECT_ROOT / "scripts/deploy_cli_updates.sh"), str(repository)],
                        env={"PATH": f"{base}:/usr/bin:/bin", "CI_TOKEN": "disposable-token",
                             "CAPTURE_ARGS": str(arguments), "CAPTURE_TAR": str(archive)},
                        check=True, capture_output=True,
                    )
                    with tarfile.open(archive) as bundle:
                        self.assertEqual({name.split("/")[0] for name in bundle.getnames()},
                                         {"metadata", "targets"} if with_targets else {"metadata"})
                    args = arguments.read_text().splitlines()
                    self.assertIn("X-CI-TOKEN: disposable-token", args)
                    self.assertIn("https://api.pornfetch.to/ci/deploy/cli", args)
                    self.assertIn("POST", args)

    def test_raw_artifacts_cannot_be_uploaded_as_signed_repositories(self):
        with tempfile.TemporaryDirectory() as temporary:
            for script, arguments in (
                ("deploy_cli_updates.sh", [temporary]),
                ("deploy_ifw_repositories.sh", ["linux_amd64", temporary]),
            ):
                with self.subTest(script=script):
                    result = subprocess.run(["bash", str(PROJECT_ROOT / "scripts" / script), *arguments],
                                            env={"CI_TOKEN": "test", "PATH": "/usr/bin:/bin"},
                                            capture_output=True, text=True)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("signed", result.stderr)


if __name__ == "__main__":
    unittest.main()
