"""Verify app full-scan integration against real source pages with duplicates."""

import asyncio
import json
from contextlib import aclosing
from urllib.parse import urlsplit

from base_api.modules.config import RuntimeConfig

from src.shared.creator_scans import discover
from src.shared.provider_routing import route_url

from .common import OUTPUT, config
from .complete_profiles import SourceCore


async def main():
    from pornhat_api.api import Channel

    url = "https://www.pornhat.com/sites/60-plus-milfs/"
    settings = RuntimeConfig()
    settings.request_attempts = 3
    async with SourceCore(configuration=settings) as core:
        core.source_site = "pornhat"
        core.source_pages = {}
        core.observer_errors = []
        core.last_source = None
        target = Channel(core=core, url=url)
        actual, identities = [], []
        async with aclosing(discover(target, route_url(url), iterator_config=config)) as stream:
            async for identity, video in stream:
                actual.append(urlsplit(video.url).path.rstrip("/"))
                identities.append(identity)
        expected = [urlsplit(u).path.rstrip("/") for _, _, urls in core.source_pages.values() for u in urls]
        assert expected and actual
        assert not core.observer_errors
        assert len(identities) == len(set(identities)), "Creator scan repeated an identity"
        assert actual == list(dict.fromkeys(expected)), "Creator scan differs from source membership/order"
        row = {
            "status": "PASS",
            "provider": "pornhat",
            "check": "app_creator_scan",
            "source_entries": len(expected),
            "unique_entries": len(actual),
            "source_pages": len(core.source_pages),
            "ordered_membership_match": True,
        }
        print(json.dumps(row), flush=True)
        (OUTPUT / "creator-scan.json").write_text(json.dumps(row, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
