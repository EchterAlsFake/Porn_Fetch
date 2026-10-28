"""Release signatures, artifact binding, and license-free installation."""
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from urllib.parse import unquote

from src.backend.update_service import AutoUpdater, CheckUpdates
from src.cli import self_update
from src.shared.release import (
    STATIC_CHANGELOG_NAME,
    safe_repo_path,
    validate_ifw_packages,
    verify_repository_manifest,
)
from src.shared.version import RELEASE_TIMESTAMP
from src.tests.unit.test_cli_self_update import keys_script, load_script

signer = load_script("sign_desktop_release")
deployment = load_script("verify_deployment")


@contextmanager
def streamed_responses(request):
    downloads = AsyncMock(side_effect=request)

    @asynccontextmanager
    async def stream(method, url, **kwargs):
        response = await downloads(url=url, **kwargs)

        async def chunks(**_kwargs):
            yield response.content

        yield SimpleNamespace(status_code=200, aiter_content=chunks)

    with patch("src.backend.update_service.service_core.initialize_session"), \
         patch("src.backend.update_service.service_core.session", SimpleNamespace(stream=stream)):
        yield downloads


class SignedReleaseTests(unittest.IsolatedAsyncioTestCase):
    async def test_tor_update_check_never_launches_networked_maintenance_tool(self):
        with (
            patch("src.backend.update_service.service_core", SimpleNamespace(tor_enabled=True)),
            patch.object(CheckUpdates, "check_signed_repository", new=AsyncMock(return_value={"version": "3.10"})) as check,
            patch("src.backend.update_service.asyncio.create_subprocess_exec", new=AsyncMock()) as launch,
        ):
            self.assertEqual(await CheckUpdates.check_via_maintenancetool(), {"version": "3.10"})
            check.assert_awaited_once()
            launch.assert_not_called()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        (self.repo / "Updates.xml").write_text('<Updates><PackageUpdate><Name>to.pornfetch.echteralsfake</Name><Version>3.10</Version><ReleaseDate>2026-10-06</ReleaseDate></PackageUpdate></Updates>')
        (self.repo / "payload.7z").write_bytes(b"test binary")
        self.root = self.base / "root.json"
        keys_script.initialize(self.base / "keys", self.root)
        signer.sign_repository(self.repo, "linux_amd64", "3.10", self.base / "keys/online.pem", self.root)

    def verify(self):
        return verify_repository_manifest((self.repo / "release.json").read_bytes(), self.root.read_bytes(), "linux_amd64")

    def test_signed_version_release_and_artifact_hashes(self):
        metadata, release = self.verify()
        self.assertEqual(release["release_timestamp"], RELEASE_TIMESTAMP)
        metadata.signed.targets["payload.7z"].verify_length_and_hashes(b"test binary")
        with self.assertRaises(Exception):
            metadata.signed.targets["payload.7z"].verify_length_and_hashes(b"bad binary")

    def test_changelog_is_signed_with_the_release(self):
        signer.sign_repository(
            self.repo, "linux_amd64", "3.10", self.base / "keys/online.pem", self.root,
            changelog="### Fixes\n- Updated the beta release.",
        )
        metadata, release = self.verify()
        self.assertEqual(release["changelog"], "### Fixes\n- Updated the beta release.")
        self.assertEqual(release["changelog_format"], "markdown")
        self.assertEqual(release["changelog_path"], STATIC_CHANGELOG_NAME)
        metadata.signed.targets[STATIC_CHANGELOG_NAME].verify_length_and_hashes(
            (self.repo / STATIC_CHANGELOG_NAME).read_bytes(),
        )
        payload = json.loads((self.repo / "release.json").read_text())
        payload["signed"]["release"]["changelog"] = "Modified notes"
        with self.assertRaises(Exception):
            verify_repository_manifest(json.dumps(payload).encode(), self.root.read_bytes(), "linux_amd64")

    async def test_update_fetches_and_verifies_server_changelog(self):
        notes = "### Fixes\n- Current release notes."
        signer.sign_repository(
            self.repo, "linux_amd64", "3.10", self.base / "keys/online.pem", self.root,
            changelog=notes,
        )
        with (
            patch("src.backend.update_service.platform.system", return_value="Linux"),
            patch("src.backend.update_service.platform.machine", return_value="x86_64"),
            patch("src.backend.update_service.QFile") as resource,
            patch("src.backend.update_service.ROOT_FILE", self.root),
            patch("src.backend.update_service.__version__", "3.9.0"),
            patch("src.backend.update_service.service_core.request", new=AsyncMock(return_value=SimpleNamespace(
                content=(self.repo / "release.json").read_bytes(),
            ))),
            patch("src.backend.update_service.service_core.fetch_bytes", new=AsyncMock(
                return_value=(self.repo / STATIC_CHANGELOG_NAME).read_bytes(),
            )) as fetch,
        ):
            resource.return_value.exists.return_value = False
            update = await CheckUpdates.check_signed_repository()
            self.assertEqual(update["changelog"].strip(), notes)
            fetch.assert_awaited_once_with(
                "https://api.pornfetch.to/repo/linux_amd64/CHANGELOG_STATIC.md",
                allow_redirects=False,
            )
            fetch.return_value = b"Unverified replacement notes"
            update = await CheckUpdates.check_signed_repository()
            self.assertEqual(update["changelog"], notes)

    def test_changed_release_date_and_wrong_root_rejected(self):
        payload = json.loads((self.repo / "release.json").read_text())
        payload["signed"]["release"]["release_timestamp"] -= 86400
        with self.assertRaises(Exception):
            verify_repository_manifest(json.dumps(payload).encode(), self.root.read_bytes(), "linux_amd64")
        other = self.base / "other.json"
        keys_script.initialize(self.base / "other-keys", other)
        with self.assertRaises(Exception):
            verify_repository_manifest((self.repo / "release.json").read_bytes(), other.read_bytes(), "linux_amd64")

    async def test_qt_stage_verifies_all_bytes_before_launch(self):
        metadata, release = self.verify()
        update = {**release, "metadata": metadata, "repository_url": "https://updates.example/"}
        async def request(url, **kwargs):
            return SimpleNamespace(content=(self.repo / url.rsplit("/", 1)[-1]).read_bytes())
        updater = AutoUpdater()
        with patch("src.backend.update_service.shared_data_dir", return_value=self.base), streamed_responses(request):
            stage = await updater._stage_repository(update)
            self.assertEqual((stage / "payload.7z").read_bytes(), b"test binary")
            (self.repo / "payload.7z").write_bytes(b"tampering")
            with self.assertRaises(Exception):
                await updater._stage_repository(update)

    async def test_ifw_bundle_archives_with_spaces_can_be_signed_and_downloaded(self):
        name = "to.pornfetch.echteralsfake/3.10Porn Fetch.app.7z"
        archive = self.repo / name
        archive.parent.mkdir()
        archive.write_bytes(b"macOS application bundle")
        archive.with_suffix(".7z.sha1").write_bytes(b"IFW checksum")
        signer.sign_repository(self.repo, "darwin_arm64", "3.10", self.base / "keys/online.pem", self.root)
        metadata, release = verify_repository_manifest(
            (self.repo / "release.json").read_bytes(), self.root.read_bytes(), "darwin_arm64",
        )
        metadata.signed.targets[name].verify_length_and_hashes(archive.read_bytes())
        base_url = "https://updates.example/"

        async def request(url, **kwargs):
            self.assertNotIn(" ", url)
            return SimpleNamespace(content=(self.repo / unquote(url.removeprefix(base_url))).read_bytes())

        with patch("src.backend.update_service.shared_data_dir", return_value=self.base), \
                streamed_responses(request) as download:
            stage = await AutoUpdater()._stage_repository({
                **release, "metadata": metadata, "repository_url": base_url,
            })
            self.assertEqual((stage / name).read_bytes(), archive.read_bytes())
            self.assertIn(base_url + name.replace(" ", "%20"), [call.kwargs["url"] for call in download.call_args_list])

        async def fetch(url, **kwargs):
            return (await request(url, **kwargs)).content

        core = SimpleNamespace(fetch_bytes=AsyncMock(side_effect=fetch))
        await deployment.verify_desktop(core, self.repo, base_url.rstrip("/"), "darwin_arm64", self.root)
        self.assertIn(base_url + name.replace(" ", "%20"), [call.args[0] for call in core.fetch_bytes.call_args_list])

    def test_repository_paths_still_reject_traversal(self):
        for name in ("../Porn Fetch.app.7z", "/Porn Fetch.app.7z", "component/../Porn Fetch.app.7z"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                safe_repo_path(name)

    async def test_optional_components_can_be_signed_and_staged(self):
        xml = ET.parse(self.repo / "Updates.xml")
        for tool in ("ffmpeg", "pocketbase"):
            package = ET.SubElement(xml.getroot(), "PackageUpdate")
            ET.SubElement(package, "Name").text = f"to.pornfetch.echteralsfake.{tool}"
            ET.SubElement(package, "Version").text = "3.10"
            ET.SubElement(package, "ReleaseDate").text = "2026-10-06"
        xml.write(self.repo / "Updates.xml")
        signer.sign_repository(self.repo, "linux_amd64", "3.10", self.base / "keys/online.pem", self.root)
        metadata, release = self.verify()
        update = {**release, "metadata": metadata, "repository_url": "https://updates.example/"}

        async def request(url, **kwargs):
            return SimpleNamespace(content=(self.repo / url.rsplit("/", 1)[-1]).read_bytes())

        with patch("src.backend.update_service.shared_data_dir", return_value=self.base), \
                streamed_responses(request):
            stage = await AutoUpdater()._stage_repository(update)
            self.assertEqual((stage / "payload.7z").read_bytes(), b"test binary")
        xml.find("PackageUpdate/Version").text = "3.9"
        with self.assertRaises(ValueError):
            validate_ifw_packages(xml, "3.10", RELEASE_TIMESTAMP)

    async def test_qt_update_without_license_launches_after_cleanup(self):
        updater = AutoUpdater(before_update=AsyncMock())
        with (
            patch("src.backend.update_service.find_maintenance_tool", return_value=self.base / "tool"),
            patch.object(CheckUpdates, "check_signed_repository", AsyncMock(return_value={"release_timestamp": RELEASE_TIMESTAMP})),
            patch.object(updater, "_stage_repository", AsyncMock(return_value=self.base)) as stage,
            patch("subprocess.Popen") as launch,
            patch("src.backend.update_service.QCoreApplication.quit") as quit_app,
            patch("src.licensing.service.create_license_service", side_effect=AssertionError("Updates must not contact licensing")),
        ):
            await updater._run()
            stage.assert_awaited_once()
            updater.before_update.assert_awaited_once()
            launch.assert_called_once()
            quit_app.assert_called_once()

    async def test_unsigned_discovery_never_offers_install(self):
        with patch.object(CheckUpdates,"check_signed_repository", AsyncMock(side_effect=ValueError)), patch.object(CheckUpdates,"check_via_http", AsyncMock(return_value={"version":"4.0"})):
            self.assertFalse((await CheckUpdates.check())["install_allowed"])


class CliFreeUpdateTests(unittest.TestCase):
    def test_cli_installs_without_license(self):
        from unittest.mock import MagicMock
        target = SimpleNamespace(custom={"version": "999.0", "release_timestamp": RELEASE_TIMESTAMP})
        updater = MagicMock()
        updater.get_targetinfo.return_value = target
        with tempfile.TemporaryDirectory() as cache:
            executable = Path(cache) / "pornfetch"
            executable.write_bytes(b"installed CLI")
            with (
                patch.object(self_update, "Updater", return_value=updater),
                patch.object(self_update, "user_cache_dir", return_value=cache),
                patch("src.licensing.service.create_license_service", side_effect=AssertionError("Updates must not contact licensing")) as licensing,
                patch.object(self_update, "_installation_path", return_value=executable),
                patch.object(self_update, "_download_update") as download,
                patch.object(self_update, "_stage_bundle") as stage,
                patch("subprocess.Popen") as launch,
            ):
                self.assertEqual(self_update.run_self_update(check_only=False, assume_yes=True), 0)
                download.assert_called_once()
                stage.assert_called_once()
                launch.assert_called_once()
                licensing.assert_not_called()

    def test_cli_missing_release_date_cannot_install(self):
        from unittest.mock import MagicMock
        updater = MagicMock()
        updater.get_targetinfo.return_value = SimpleNamespace(custom={"version":"999.0"})
        with tempfile.TemporaryDirectory() as cache, patch.object(self_update, "Updater", return_value=updater), patch.object(self_update,"user_cache_dir",return_value=cache):
            self.assertEqual(self_update.run_self_update(check_only=False,assume_yes=True),1)
            updater.download_target.assert_not_called()
