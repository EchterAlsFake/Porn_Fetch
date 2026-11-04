"""Native Tube8 client with support for its current Vue user-profile header.

Keep upstream networking, source loading and video feeds. The published 1.3.3
extractor only recognizes the old heading; remove this adapter when upstream
also reads the identity in #user_profile_container.
"""
from selectolax.lexbor import LexborHTMLParser
from tube8_api import Client as NativeClient
from tube8_api import User as NativeUser


class User(NativeUser):
    __slots__ = ()

    def _extract_html(self, html_content: str) -> dict:
        data = super()._extract_html(html_content)
        if not data.get("name"):
            banner = LexborHTMLParser(html_content).css_first("#user_profile_container .banner img[alt]")
            if banner is not None:
                data["name"] = (banner.attributes.get("alt") or "").strip() or None
        return data


class Client(NativeClient):
    async def get_user(self, url: str, load_html: bool = True) -> User:
        user = User(core=self.core, url=url)
        if load_html:
            await user.load_sources("html")
        return user
