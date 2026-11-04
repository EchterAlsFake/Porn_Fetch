"""Tube8's Vue user header still uses the native source-loading contract."""
import unittest
from unittest.mock import AsyncMock, patch

from base_api import BaseCore

from src.shared.tube8 import Client


class Tube8UserTests(unittest.IsolatedAsyncioTestCase):
    async def test_current_and_legacy_identity_load_through_native_media_fields(self):
        for html in ('<div id="user_profile_container"><div class="banner"><img alt="Example User"></div></div>',
                     '<h1 class="name-title">Example User</h1>'):
            async with BaseCore() as core:
                with patch.object(core, "fetch_text", AsyncMock(return_value=html)):
                    user = await Client(core=core).get_user("https://www.tube8.com/user/123/")
                self.assertEqual(user.name, "Example User")
                self.assertIs(user.core, core)

    async def test_generic_page_is_not_accepted_as_a_user_identity(self):
        async with BaseCore() as core:
            with patch.object(core, "fetch_text", AsyncMock(return_value='<img alt="Advertisement">')):
                with self.assertRaisesRegex(Exception, "Profile identity not found"):
                    await Client(core=core).get_user("https://www.tube8.com/user/123/")
