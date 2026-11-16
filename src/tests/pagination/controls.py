"""Live shared pagination lifecycle and upstream-limit checks."""

import asyncio
import importlib
import json
from contextlib import aclosing
from dataclasses import replace
from urllib.parse import parse_qs, urlsplit

from base_api import BaseCore, ErrorMode
from base_api.modules.config import RuntimeConfig

from .common import OUTPUT, collect, config


class CountingCore(BaseCore):
    async def fetch_text(self, url, **kwargs):
        self.requests.append(url)
        return await super().fetch_text(url, **kwargs)


async def lifecycle():
    from bellesa_api.api import Channel

    settings = RuntimeConfig()
    settings.request_attempts = 3
    async with CountingCore(configuration=settings) as core:
        core.requests = []
        obj = Channel(core=core, url="https://www.bellesa.co/channels/zero-to-hero")
        for pages, start in [(0, 1), (-1, 1), (True, 1), ("2", 1), (1, 0), (1, True), (1.5, 1)]:
            try:
                obj.videos(pages=pages, start_page=start, iterator_config=config)
            except ValueError:
                pass
            else:
                raise AssertionError("Invalid pagination accepted")
        assert not core.requests, "Invalid parameters issued network requests"
        stream = obj.videos(pages="all", iterator_config=config)
        await anext(stream)
        await stream.aclose()
        assert stream.summary.status == "cancelled"
        assert len(core.requests) == 1, "Discovery fetched an unnecessary page"
        core.requests = []
        stream = obj.videos(pages="all", iterator_config=config)
        values = await collect(stream)
        assert values and stream.summary.exhausted
        assert stream.summary.pages == 2 and len(core.requests) == 2, "Page response was fetched twice"
        final = obj.videos(pages=1, start_page=2, iterator_config=config)
        tail = await collect(final)
        assert values[-len(tail) :] == tail and tail
        assert final.summary.exhausted
        beyond = obj.videos(pages="all", start_page=3, iterator_config=config)
        assert not await collect(beyond) and beyond.summary.exhausted
        finite = obj.videos(pages=1, iterator_config=config)
        assert await collect(finite)
        assert finite.summary.status == "limit_reached" and not finite.summary.exhausted
        return {
            "check": "shared_lifecycle",
            "status": "PASS",
            "complete_items": len(values),
            "complete_pages": stream.summary.pages,
            "response_reuse": True,
            "partial_close": True,
            "invalid_parameters": True,
            "offset_and_beyond": True,
        }


async def upstream_limit(site, url, *, terminal_hook=False):
    module = importlib.import_module(site + "_api.api")
    settings = RuntimeConfig()
    settings.request_attempts = 3
    async with CountingCore(configuration=settings) as core:
        core.requests = []
        obj = module.Channel(core=core, url=url)
        cfg = replace(config, page_error_mode=ErrorMode.YIELD)
        stream = obj.get_videos(pages="all", start_page=100, iterator_config=cfg)
        if terminal_hook:
            from functools import partial

            from base_api import paginated_stream, update_url_query
            from base_api.modules.pagination import http_status_is

            def page_url(page):
                return update_url_query(url, page=page)
            stream = paginated_stream(
                core=core,
                constructor=module.Video,
                page_url=page_url,
                item_extractor=partial(module.extractor_search, base_url=url),
                page_info=lambda content, page, rows: module._pagination_info(content, page, rows, page_url=page_url),
                pages="all",
                start_page=100,
                iterator_config=cfg,
                verify_first=True,
                terminal_error=lambda error, page: http_status_is(error, 404),
            )
        items, failures = 0, 0
        async with aclosing(stream):
            async for result in stream:
                if result.error:
                    from base_api.modules.pagination import http_status_is

                    assert http_status_is(result.error, 404), "Unexpected upstream failure"
                    failures += 1
                else:
                    result.unwrap()
                    items += 1
        assert items and failures == 1, "Did not observe the advertised page-101 failure"
        assert stream.summary.status == "incomplete" and not stream.summary.exhausted
        assert [parse_qs(urlsplit(u).query).get("page", ["1"])[0] for u in core.requests] == (
            ["1", "100", "101"] if terminal_hook else ["100", "101"]
        )
        return {
            "provider": site,
            "check": "upstream_page_101_limit",
            "status": "EXPECTED_UPSTREAM_FAILURE",
            "accessible_page_100_items": items,
            "page_101_http_status": 404,
            "summary": stream.summary.status,
            "false_exhaustion_prevented": True,
        }


async def main():
    rows = []
    checks = [
        lifecycle(),
        upstream_limit("thumbzilla", "https://www.thumbzilla.com/channel/brazzers/"),
        upstream_limit("tube8", "https://www.tube8.com/channel/teamskeet/"),
        upstream_limit("thumbzilla", "https://www.thumbzilla.com/channel/brazzers/", terminal_hook=True),
    ]
    for check in checks:
        try:
            row = await check
        except Exception as error:
            row = {"status": "FAIL", "error": type(error).__name__ + ": " + str(error)}
        rows.append(row)
        print(json.dumps(row), flush=True)
    (OUTPUT / "controls.json").write_text(json.dumps(rows, indent=2))
    if any(row["status"] == "FAIL" for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
