"""Protocol fixtures exercise the real BaseCore handler without provider HTTP."""
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from base_api import BaseCore
from base_api.modules.config import RuntimeConfig
from curl_cffi.requests import Cookies, Response
from curl_cffi.requests.headers import Headers

from src.backend.account_diagnostics import AccountAccessGuard, AccountAccessStopped

URL = "https://www.pornhub.com/protocol-fixture"
MATH = (b'<body onload="go()"><script>function go(){'
        b'var p=15; var s=7; n=leastFactor(p);'
        b'document.cookie="KEY="+n+"*"+(p/n)+":"+s+":123:1";'
        b'}</script></body>')


def response(content, *, status=200, url=""):
    value = Response()
    value.status_code, value.content, value.url = status, content, url
    value.headers = Headers({"content-type": "text/html; charset=utf-8"})
    return value


class NativeChallengeGuardTests(unittest.IsolatedAsyncioTestCase):
    def core(self, transport):
        config = RuntimeConfig()
        config.request_attempts = 2
        core = BaseCore(configuration=config)
        core.session = SimpleNamespace(headers=Headers(), cookies=Cookies(), request=transport, close=AsyncMock())
        return core

    async def test_native_pornhub_math_handler_receives_response_and_retries(self):
        transport = AsyncMock(side_effect=[response(MATH), response(b"Protocol fixture completed")])
        core = self.core(transport)
        try:
            with patch.object(BaseCore, "initialize_session", lambda _core: None), AccountAccessGuard() as guard:
                text = await core.fetch_text(URL)
            self.assertEqual(text, "Protocol fixture completed")
            self.assertEqual(transport.await_count, 2)
            self.assertEqual(core._challenge_generation, 1)
            self.assertEqual(core.latest_key, "3*5:7:123:1")
            self.assertIsNone(guard.blocked)
            self.assertEqual(guard.native_challenge_events, [
                {"kind": "pornhub-math-challenge", "http_status": 200,
                 "host": "www.pornhub.com", "handler": "eaf_base_api"},
            ])
        finally:
            await core.close()

    async def test_exception_does_not_allow_captcha_denials_other_hosts_or_unknown_scripts(self):
        cases = [
            ("https://www.xvideos.com/account", response(MATH)),
            (URL, response(MATH, status=403)),
            (URL, response(MATH, status=451)),
            (URL, response(b'<body onload="go()">unsupported script</body>')),
            (URL, response(b"<title>CAPTCHA verification</title>" + MATH)),
            (URL, response(MATH, url="https://example.test/verification")),
        ]
        for url, item in cases:
            with self.subTest(url=url, status=item.status_code):
                transport = AsyncMock(return_value=item)
                core = self.core(transport)
                try:
                    with patch.object(BaseCore, "initialize_session", lambda _core: None), AccountAccessGuard() as guard:
                        with self.assertRaises(AccountAccessStopped):
                            await core.fetch_text(url)
                    self.assertEqual(transport.await_count, 1)
                    self.assertEqual(core._challenge_generation, 0)
                    self.assertIsNotNone(guard.blocked)
                    self.assertEqual(guard.native_challenge_events, [])
                finally:
                    await core.close()
