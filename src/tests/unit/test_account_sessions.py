"""Safe diagnoses for incomplete and server-rejected account sessions."""
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

from base_api import CachePolicy
from curl_cffi.requests import Cookies

from src.shared.provider_accounts import AccountSessionError, connect_xvideos_cookies


class AccountSessionTests(unittest.IsolatedAsyncioTestCase):
    def client(self):
        return SimpleNamespace(account=object(), get_account=Mock(),
                               core=SimpleNamespace(session=SimpleNamespace(cookies=Cookies()),
                                                    fetch_text=AsyncMock(return_value='{"is_logged": false}')))

    async def test_missing_auth_cookie_has_an_actionable_message_without_token_values(self):
        client = self.client()
        with self.assertRaises(AccountSessionError) as failure:
            await connect_xvideos_cookies(client, {"session_token": "private-value"})
        self.assertIn("session_token_auth", str(failure.exception))
        self.assertNotIn("private-value", str(failure.exception))
        self.assertIsNone(client.account)
        client.get_account.assert_not_called()
        client.core.fetch_text.assert_not_awaited()

    async def test_cookie_presence_does_not_replace_uncached_server_authentication(self):
        client = self.client()
        with self.assertRaises(AccountSessionError):
            await connect_xvideos_cookies(client, {"session_token": "private-value", "session_token_auth": "private-auth"})
        self.assertIsNone(client.account)
        client.core.fetch_text.assert_awaited_once_with("https://www.xvideos.com/", cache_policy=CachePolicy.BYPASS)
