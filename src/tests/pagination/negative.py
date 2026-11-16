"""Live checks that empty/unavailable resources cannot become unrelated videos."""

import asyncio
import json

from base_api import BaseCore
from base_api.modules.config import RuntimeConfig
from selectolax.lexbor import LexborHTMLParser

from .common import OUTPUT, collect, config
from .complete_profiles import SourceCore


async def main():
    rows = []
    settings = RuntimeConfig()
    settings.request_attempts = 3
    async with SourceCore(configuration=settings) as core:
        core.source_site = "pornhub"
        core.source_pages = {}
        core.observer_errors = []
        core.last_source = None
        from pornhub_api.api import User

        user = User(core=core, url="https://www.pornhub.com/users/germanonex")
        for method in ["get_videos", "get_uploads"]:
            for pages, start in [(1, 1), (1, 2), ("all", 1)]:
                assert not await collect(getattr(user, method)(pages=pages, start_page=start, iterator_config=config))
            assert core.last_source is not None and not core.observer_errors
            tree = LexborHTMLParser(core.last_source[1])
            section = tree.css_first("div.profileVids")
            assert section is not None and not section.css("li.pcVideoListItem,li.videoBox")
            assert tree.css("li.pcVideoListItem,li.videoBox"), "Fixture no longer contains the unrelated sidebar cards"
            rows.append(
                {
                    "provider": "pornhub",
                    "method": method,
                    "status": "EMPTY_CONFIRMED",
                    "source_empty_section": True,
                    "unrelated_cards_excluded": True,
                    "offset_and_all_checked": True,
                    "nonempty_advancement_verified": False,
                }
            )
    async with BaseCore(configuration=settings) as core:
        from thumbzilla_api.api import Playlist

        try:
            await collect(Playlist(core=core, url="https://www.thumbzilla.com/").get_videos(iterator_config=config))
        except Exception as error:
            names = []
            while error is not None:
                names.append(type(error).__name__)
                error = error.__cause__ or error.__context__
            assert "NotFound" in names, "Wrong-page rejection did not identify the missing playlist"
        else:
            raise AssertionError("Homepage was accepted as a playlist")
        rows.append(
            {
                "provider": "thumbzilla",
                "check": "wrong_resource_type_rejected",
                "status": "EXPECTED_UNAVAILABLE",
                "playlist_pagination_verified": False,
            }
        )
    for row in rows:
        print(json.dumps(row), flush=True)
    (OUTPUT / "negative.json").write_text(json.dumps(rows, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
