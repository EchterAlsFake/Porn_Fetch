"""No Tor-enabled service request may escape through a direct connection."""
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from src.shared.service_transport import (
    ONION_ORIGIN,
    ServiceCore,
    ServiceFetcher,
    ServicePolicy,
    TorServiceFailure,
    service_mode,
)
from src.shared.tor_runtime import TorBinaryMissing, TorRuntime, TorUnavailable


class RoutingTests(unittest.TestCase):
    def test_migration_and_routes(self):
        self.assertEqual(service_mode(SimpleNamespace(enable_tor=True, enable_tor_server_routing=True)), "tor")
        manager = MagicMock()
        manager.ensure_ready.return_value = "socks5h://127.0.0.1:12345"
        policy = ServicePolicy(SimpleNamespace(service_transport="tor"), manager=manager)
        url, proxy = policy.route("https://licenses.pornfetch.to/v1/accounts/demo/machines")
        self.assertEqual(url, ONION_ORIGIN + "/licensing/v1/accounts/demo/machines")
        self.assertTrue(proxy.startswith("socks5h://"))
        self.assertEqual(policy.route("https://api.pornfetch.to/repo/cli/metadata/root.json")[0],
                         ONION_ORIGIN + "/repo/cli/metadata/root.json")
        with self.assertRaises(TorUnavailable):
            policy.route("https://github.com/example/update")
        with self.assertRaises(ValueError):
            ServicePolicy().route("http://licenses.pornfetch.to/v1/")

    def test_failed_bootstrap_never_starts_a_download(self):
        manager = MagicMock()
        manager.ensure_ready.side_effect = TorUnavailable("offline")
        policy = ServicePolicy(SimpleNamespace(service_transport="tor"), manager=manager)
        with patch("src.shared.service_transport.requests.Session") as session, \
             patch("src.shared.service_transport.failure_listener") as notice:
            with self.assertRaises(TorUnavailable):
                list(ServiceFetcher(policy=policy)._fetch("https://pornfetch.to/repo/android/metadata/root.json"))
            session.assert_not_called()
            self.assertIn("Tor could not start or connect", notice.call_args.args[0])

    def test_missing_binary_keeps_actionable_reason_in_service_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            manager = TorRuntime(binary=Path(temporary) / "missing-tor")
            policy = ServicePolicy(SimpleNamespace(service_transport="tor"), manager=manager)
            with patch("src.shared.service_transport.failure_listener") as notice, \
                 patch("src.shared.service_transport.requests.Session") as session:
                with self.assertRaises(TorServiceFailure) as raised:
                    list(ServiceFetcher(policy=policy)._fetch("https://api.pornfetch.to/update"))
            self.assertIsInstance(raised.exception.__cause__, TorBinaryMissing)
            self.assertIn("Tor executable could not be found", str(raised.exception))
            self.assertIn("PORNFETCH_TOR_BINARY", str(raised.exception))
            self.assertIn("No direct connection was attempted", str(raised.exception))
            self.assertEqual(notice.call_args.args[0], str(raised.exception))
            self.assertEqual(policy.last_failure, str(raised.exception))
            session.assert_not_called()

    def test_sync_update_stream_failure_notifies_before_tuf_wraps_it(self):
        manager = MagicMock()
        manager.ensure_ready.return_value = "socks5h://127.0.0.1:12345"
        policy = ServicePolicy(SimpleNamespace(service_transport="tor"), manager=manager)

        def chunks(**_kwargs):
            yield b"partial update"
            raise ConnectionError("dropped")

        @contextmanager
        def stream(*_args, **_kwargs):
            start = int(_kwargs.get("headers", {}).get("Range", "bytes=0-")[6:-1])
            yield SimpleNamespace(status_code=206 if start else 200, iter_content=chunks,
                                  headers={"Content-Range": f"bytes {start}-99/100"})

        with patch("src.shared.service_transport.requests.Session") as session, \
             patch("src.shared.service_transport.time.sleep"), \
             patch("src.shared.service_transport.failure_listener") as notice:
            session.return_value.__enter__.return_value.stream = stream
            with self.assertRaises(TorServiceFailure):
                list(ServiceFetcher(policy=policy)._fetch("https://pornfetch.to/repo/android/targets/update.apk"))
            notice.assert_called_once()
            self.assertIn("could not be reached through Tor", notice.call_args.args[0])

    def test_update_stream_resumes_without_repeating_bytes_and_keeps_tuf_verification(self):
        from tuf.api.metadata import TargetFile

        calls = []
        chunks_seen = []

        def interrupted(**_kwargs):
            yield b"first"
            raise ConnectionError("stream reset")

        @contextmanager
        def stream(*args, **kwargs):
            calls.append(kwargs)
            if len(calls) == 1:
                yield SimpleNamespace(status_code=200, iter_content=interrupted)
            else:
                yield SimpleNamespace(status_code=206, headers={"Content-Range": "bytes 5-8/9"},
                                      iter_content=lambda **_: iter([b"last"]))

        fetcher = ServiceFetcher()
        fetcher.on_chunk = chunks_seen.append
        with patch("src.shared.service_transport.requests.Session") as session, \
             patch("src.shared.service_transport.time.sleep"):
            session.return_value.__enter__.return_value.stream = stream
            data = b"".join(fetcher._fetch("https://api.pornfetch.to/repo/cli/targets/update.zip"))
        self.assertEqual(data, b"firstlast")
        TargetFile.from_data("update.zip", b"firstlast").verify_length_and_hashes(data)
        self.assertEqual(calls[1]["headers"]["Range"], "bytes=5-")
        self.assertEqual([options["http_version"] for options in calls], ["v1", "v1"])
        self.assertEqual(sum(chunks_seen), len(data))
        self.assertTrue(all(options["proxy"] == "" for options in calls))

    def test_missing_runtime_and_owned_process_cleanup(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime = TorRuntime(binary=root / "missing", directory=root / "data")
            with patch("src.shared.tor_runtime.subprocess.Popen") as launch:
                with self.assertRaises(TorBinaryMissing):
                    runtime.ensure_ready()
                self.assertEqual(runtime.state, "missing")
                launch.assert_not_called()
            binary = root / "tor"
            binary.touch()
            process = MagicMock()
            process.poll.return_value = None
            runtime = TorRuntime(binary=binary, directory=root / "data")
            with patch("src.shared.tor_runtime.subprocess.Popen", return_value=process), \
                 patch.object(runtime, "_control", return_value='250 OK\n250-status/bootstrap-phase=NOTICE BOOTSTRAP PROGRESS=100\n250-net/listeners/socks="127.0.0.1:40001"\n250 OK'):
                self.assertEqual(runtime.ensure_ready(), "socks5h://127.0.0.1:40001")
                runtime.stop()
                process.terminate.assert_called_once()


class AsyncRoutingTests(unittest.IsolatedAsyncioTestCase):
    async def test_connect_failure_notifies_only_for_service_tor_route(self):
        for mode in ("tor", "direct"):
            with self.subTest(mode=mode):
                manager = MagicMock()
                manager.ensure_ready.return_value = "socks5h://127.0.0.1:12345"
                core = ServiceCore(policy=ServicePolicy(SimpleNamespace(service_transport=mode), manager=manager))
                core.session = SimpleNamespace(request=AsyncMock(side_effect=ConnectionError("unreachable")))
                with patch.object(core, "initialize_session"), \
                     patch("src.shared.service_transport.failure_listener") as notice:
                    with self.assertRaises(ConnectionError):
                        await core.request("https://licenses.pornfetch.to/v1/accounts/demo/machines")
                    self.assertEqual(notice.call_count, 1 if mode == "tor" else 0)
                core.session = None
                await core.close()

    async def test_third_party_failure_does_not_raise_service_tor_notification(self):
        manager = MagicMock()
        core = ServiceCore(policy=ServicePolicy(SimpleNamespace(service_transport="tor"), manager=manager))
        with patch("src.shared.service_transport.failure_listener") as notice, \
             patch.object(core, "initialize_session") as initialize:
            with self.assertRaises(TorUnavailable):
                await core.request("https://video.example/video")
            initialize.assert_not_called()
            manager.ensure_ready.assert_not_called()
            notice.assert_not_called()
        await core.close()

    async def test_server_error_is_distinct_from_bootstrap_and_license_denial(self):
        manager = MagicMock()
        manager.ensure_ready.return_value = "socks5h://127.0.0.1:12345"
        core = ServiceCore(policy=ServicePolicy(SimpleNamespace(service_transport="tor"), manager=manager))
        core.session = SimpleNamespace(request=AsyncMock(return_value=SimpleNamespace(status_code=503)))
        with patch.object(core, "initialize_session"), \
             patch("src.shared.service_transport.failure_listener") as notice:
            response = await core.request("https://licenses.pornfetch.to/v1/accounts/demo/machines")
            self.assertEqual(response.status_code, 503)
            self.assertIn("Tor itself may still be connected", notice.call_args.args[0])
            notice.reset_mock()
            core.session.request.return_value.status_code = 403
            await core.request("https://licenses.pornfetch.to/v1/accounts/demo/machines")
            notice.assert_not_called()
        core.session = None
        await core.close()

    async def test_interrupted_download_notifies_and_removes_partial_file(self):
        from contextlib import asynccontextmanager
        manager = MagicMock()
        manager.ensure_ready.return_value = "socks5h://127.0.0.1:12345"
        core = ServiceCore(policy=ServicePolicy(SimpleNamespace(service_transport="tor"), manager=manager))

        async def chunks(**_kwargs):
            yield b"partial update"
            raise ConnectionError("dropped")

        @asynccontextmanager
        async def stream(*_args, **_kwargs):
            yield SimpleNamespace(status_code=200, aiter_content=chunks)

        core.session = SimpleNamespace(stream=stream)
        with tempfile.TemporaryDirectory() as temporary, \
             patch.object(core, "initialize_session"), \
             patch("src.shared.service_transport.failure_listener") as notice:
            path = Path(temporary) / "update"
            with self.assertRaises(TorServiceFailure):
                await core.download_verified("https://api.pornfetch.to/repo/payload.7z", SimpleNamespace(length=100), path)
            self.assertFalse(path.exists())
            notice.assert_called_once()
        core.session = None
        await core.close()

    async def test_license_offline_reason_keeps_tor_failure_explanation(self):
        from src.licensing.client import LicenseStatus
        from src.licensing.service import LicenseService
        policy = ServicePolicy(SimpleNamespace(service_transport="tor"))
        with patch("src.shared.service_transport.failure_listener"):
            policy.failed("connection")
        core = ServiceCore(policy=policy)
        service = LicenseService(SimpleNamespace(), core)
        service.status = LicenseStatus("offline_grace", True, failure="network_unavailable")
        self.assertIn("Using the last successful validation", service.reason)
        self.assertIn("turn off", service.reason)
        policy._set_mode("direct")
        self.assertNotIn("through Tor", service.reason)
        await core.close()

    async def test_license_requests_keep_errors_and_explicit_proxy(self):
        manager = MagicMock()
        manager.ensure_ready.return_value = "socks5h://127.0.0.1:12345"
        core = ServiceCore(policy=ServicePolicy(SimpleNamespace(service_transport="tor"), manager=manager))
        response = SimpleNamespace(status_code=403)
        core.session = SimpleNamespace(request=AsyncMock(return_value=response))
        with patch.object(core, "initialize_session"):
            result = await core.request("https://licenses.pornfetch.to/v1/accounts/demo/machines", method="POST")
        self.assertIs(result, response)
        options = core.session.request.call_args.kwargs
        self.assertEqual(options["proxy"], "socks5h://127.0.0.1:12345")
        self.assertEqual(options["http_version"], "v1")
        self.assertFalse(options["allow_redirects"])
        self.assertTrue(options["verify"])
        core.session = None
        await core.close()

    async def test_failed_bootstrap_never_initializes_http(self):
        manager = MagicMock()
        manager.ensure_ready.side_effect = TorUnavailable("offline")
        core = ServiceCore(policy=ServicePolicy(SimpleNamespace(service_transport="tor"), manager=manager))
        with patch.object(core, "initialize_session") as initialize:
            with self.assertRaises(TorUnavailable):
                await core.request("https://licenses.pornfetch.to/v1/accounts/demo/machines")
            initialize.assert_not_called()
        await core.close()
