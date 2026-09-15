from __future__ import annotations

import unittest

from src.backend import clients
from src.backend.config import app_settings


class ClientRefreshTests(unittest.IsolatedAsyncioTestCase):
    async def test_active_sni_proxy_replaces_live_sessions(self) -> None:
        original_active_url = app_settings.active_sni_proxy_url
        original_session = clients.core.session
        app_settings.active_sni_proxy_url = "socks5://127.0.0.1:49099"
        try:
            clients.refresh_clients()
            self.assertIsNot(clients.core.session, original_session)
            self.assertEqual(clients.config.proxy, app_settings.active_sni_proxy_url)
            self.assertEqual(clients.config.http_version, "v2")
            self.assertIsNone(clients.config.interface)
            self.assertEqual(
                clients.core.session.proxies,
                {"all": app_settings.active_sni_proxy_url},
            )
        finally:
            app_settings.active_sni_proxy_url = original_active_url
            clients.refresh_clients()
            await clients.close_retired_sessions()


if __name__ == "__main__":
    unittest.main()
