"""Offline checks for media Tor routing; no provider or public Tor traffic."""
import asyncio
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from base_api import BaseCore
from base_api.modules.config import DownloadConfigRAW, RuntimeConfig
from curl_cffi.const import CurlOpt

from src.shared.service_transport import ServicePolicy
from src.shared.tor_runtime import TorUnavailable
from src.shared.tor_transport import MediaCore


class MediaRoutingTests(unittest.IsolatedAsyncioTestCase):
    async def test_pages_segments_and_mp4_stream_use_remote_socks_dns(self):
        destinations = []
        payload = b"synthetic media payload"

        async def socks_peer(reader, writer):
            try:
                version, methods = await reader.readexactly(2)
                self.assertEqual(version, 5)
                await reader.readexactly(methods)
                writer.write(b"\x05\x00")
                await writer.drain()
                header = await reader.readexactly(4)
                self.assertEqual(header, b"\x05\x01\x00\x03")
                length = (await reader.readexactly(1))[0]
                hostname = (await reader.readexactly(length)).decode()
                await reader.readexactly(2)
                writer.write(b"\x05\x00\x00\x01\x7f\x00\x00\x01\x00\x50")
                await writer.drain()
                request = await reader.readuntil(b"\r\n\r\n")
                destinations.append((hostname, request.split(b"\r\n", 1)[0]))
                writer.write(f"HTTP/1.1 200 OK\r\nContent-Length: {len(payload)}\r\nConnection: close\r\n\r\n".encode())
                if not request.startswith(b"HEAD "):
                    writer.write(payload)
                await writer.drain()
            finally:
                writer.close()
                await writer.wait_closed()

        server = await asyncio.start_server(socks_peer, "127.0.0.1", 0)
        self.addAsyncCleanup(server.wait_closed)
        self.addCleanup(server.close)
        port = server.sockets[0].getsockname()[1]
        manager = MagicMock()
        manager.ensure_ready.return_value = f"socks5h://127.0.0.1:{port}"
        config = RuntimeConfig()
        config.service_transport = "tor_all"
        config.proxy = "http://unused.invalid:9999"
        config.dns_over_https = "https://unused.invalid/dns-query"
        config.interface = "unused-interface"
        config.request_attempts = 1
        config.timeout = 3
        async with server, MediaCore(config, manager=manager) as core:
            with patch.dict("os.environ", {"NO_PROXY": "*", "ALL_PROXY": "http://unused.invalid:9999"}):
                self.assertEqual(await core.fetch_bytes("http://provider.invalid/page"), payload)
                self.assertEqual(await core.download_segment("http://cdn.invalid/segment.ts", timeout=3),
                                 ("http://cdn.invalid/segment.ts", payload, True))
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "video.mp4"
                    await core.legacy_download("http://cdn.invalid/video.mp4", DownloadConfigRAW(
                        quality="best", path=str(path), allow_multipart=True, max_workers=1,
                        callback=lambda *_: None, max_retries=1, read_timeout=3,
                    ))
                    self.assertEqual(path.read_bytes(), payload)
        self.assertEqual({host for host, _ in destinations}, {"provider.invalid", "cdn.invalid"})
        self.assertTrue(any(line.startswith(b"HEAD /video.mp4") for _, line in destinations))
        self.assertTrue(any(line.startswith(b"GET /video.mp4") for _, line in destinations))

    async def test_bootstrap_failure_never_calls_http_or_streaming_session(self):
        config = RuntimeConfig()
        config.service_transport = "tor_all"
        manager = MagicMock()
        manager.ensure_ready.side_effect = TorUnavailable("Tor offline")
        core = MediaCore(config, manager=manager)
        request = AsyncMock()
        core.session = SimpleNamespace(request=request, curl_options={})
        with patch.object(BaseCore, "initialize_session"):
            core.initialize_session()
            for kwargs in ({}, {"stream": True}):
                with self.assertRaises(TorUnavailable):
                    await core.session.request("GET", "https://cdn.invalid/video.mp4", **kwargs)
        request.assert_not_awaited()
        core.session = None

    async def test_service_only_mode_leaves_media_proxy_unchanged(self):
        config = RuntimeConfig()
        config.service_transport = "tor"
        manager = MagicMock()
        core = MediaCore(config, manager=manager)
        request = AsyncMock()
        core.session = SimpleNamespace(request=request, curl_options={})
        with patch.object(BaseCore, "initialize_session"):
            core.initialize_session()
            await core.session.request("GET", "https://cdn.invalid/video.mp4")
        manager.ensure_ready.assert_not_called()
        request.assert_awaited_once_with("GET", "https://cdn.invalid/video.mp4")
        core.session = None

    async def test_existing_session_is_guarded_when_all_traffic_is_enabled(self):
        config = RuntimeConfig()
        config.service_transport = "direct"
        manager = MagicMock()
        manager.ensure_ready.return_value = "socks5h://127.0.0.1:12345"
        core = MediaCore(config, manager=manager)
        request = AsyncMock()
        core.session = SimpleNamespace(request=request, curl_options={}, proxy_auth=("custom", "secret"))
        with patch.object(BaseCore, "initialize_session"):
            core.initialize_session()
            config.service_transport = "tor_all"
            await core.session.request("GET", "https://cdn.invalid/video.mp4", proxy="http://bypass.invalid", stream=True)
        options = request.await_args.kwargs
        self.assertEqual(options["proxy"], manager.ensure_ready.return_value)
        self.assertEqual(options["http_version"], "v2")
        self.assertTrue(options["verify"])
        self.assertIsNone(core.session.proxy_auth)
        self.assertEqual(core.session.curl_options[CurlOpt.NOPROXY], b"")
        self.assertEqual(core.session.curl_options[CurlOpt.DOH_URL], b"")
        core.session = None

    async def test_all_traffic_keeps_onion_service_route(self):
        manager = MagicMock()
        manager.ensure_ready.return_value = "socks5h://127.0.0.1:12345"
        policy = ServicePolicy(SimpleNamespace(service_transport="tor_all"), manager=manager)
        url, proxy = policy.route("https://api.pornfetch.to/update")
        self.assertIn(".onion/update", url)
        self.assertEqual(proxy, manager.ensure_ready.return_value)

    async def test_error_reports_use_tor_and_do_not_fall_back_when_unavailable(self):
        from src.shared.error_reporting import report_public_error
        settings = SimpleNamespace(service_transport="tor_all")
        session = AsyncMock()
        session.post.return_value.status_code = 204
        with patch("src.shared.tor_transport._settings", settings), \
             patch("src.shared.tor_transport.runtime.ensure_ready", return_value="socks5h://127.0.0.1:12345") as ready, \
             patch("src.shared.error_reporting.AsyncSession", return_value=session) as factory:
            self.assertTrue(await report_public_error("synthetic diagnostic"))
            self.assertEqual(factory.call_args.kwargs["proxy"], ready.return_value)
            factory.reset_mock()
            ready.side_effect = TorUnavailable("offline")
            self.assertFalse(await report_public_error("synthetic diagnostic"))
            factory.assert_not_called()


class InstallerRoutingTests(unittest.TestCase):
    def test_pocketbase_download_uses_tor_and_never_urllib(self):
        from urllib.request import Request

        from src.database.installer import _download_response
        settings = SimpleNamespace(service_transport="tor_all")
        with patch("src.shared.tor_transport._settings", settings), \
             patch("src.shared.tor_transport.runtime.ensure_ready", return_value="socks5h://127.0.0.1:12345") as ready, \
             patch("curl_cffi.requests.Session") as factory, \
             patch("urllib.request.urlopen") as direct:
            response = factory.return_value.__enter__.return_value.stream.return_value.__enter__.return_value
            response.headers = {"Content-Length": "7"}
            response.iter_content.return_value = iter([b"fixture"])
            with _download_response(Request("https://github.com/pocketbase/archive.zip")) as (headers, chunks):
                self.assertEqual(headers["Content-Length"], "7")
                self.assertEqual(b"".join(chunks), b"fixture")
            self.assertEqual(factory.call_args.kwargs["proxy"], ready.return_value)
            factory.reset_mock()
            ready.side_effect = TorUnavailable("offline")
            with self.assertRaises(TorUnavailable), _download_response(Request("https://github.com/pocketbase/archive.zip")):
                self.fail("Tor startup failure must stop installation")
            factory.assert_not_called()
            direct.assert_not_called()
