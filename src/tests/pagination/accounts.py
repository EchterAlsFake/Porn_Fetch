import sys, pathlib, asyncio, json, logging, importlib
from .common import *
from base_api import BaseCore, IteratorConfig, ResultOrder, ErrorMode
from base_api.modules.config import RuntimeConfig
from src.shared.provider_accounts import connect_pornhub_cookies, connect_xvideos_cookies, verify_account_session
from contextlib import aclosing
import browser_cookie3

logging.disable(logging.CRITICAL)


async def collect(stream):
    async with aclosing(stream):
        return [r.unwrap().url async for r in stream]


async def main():
    results = []
    for site in ["xvideos", "xhamster", "pornhub"]:
        try:
            jar = await asyncio.wait_for(asyncio.to_thread(browser_cookie3.brave, domain_name=site + ".com"), 45)
            cfg = RuntimeConfig()
            cfg.request_attempts = 3
            async with BaseCore(configuration=cfg) as core:
                module = importlib.import_module(site + "_api.api")
                client = module.Client(core=core)
                if site == "pornhub":
                    await connect_pornhub_cookies(client, jar)
                    target = client.account
                    methods = ["get_history", "get_favorites", "get_recommended", "get_feed", "get_subscriptions"]
                elif site == "xvideos":
                    await connect_xvideos_cookies(client, {c.name: c.value for c in jar}, browser_jar=jar)
                    target = client.account
                    methods = ["get_recommended_videos", "get_liked_videos", "get_watch_later_videos"]
                else:
                    core.session.cookies.update(jar)
                    await verify_account_session(client, site)
                    target = module.Account(core=core)
                    methods = ["get_liked_videos"]
                for name in methods:
                    try:
                        ic = IteratorConfig(
                            order=ResultOrder.ORIGINAL, page_error_mode=ErrorMode.RAISE, item_error_mode=ErrorMode.RAISE
                        )
                        fn = getattr(target, name)
                        a = await collect(fn(pages=1, start_page=1, iterator_config=ic))
                        b = await collect(fn(pages=1, start_page=2, iterator_config=ic))
                        ab = await collect(fn(pages=2, iterator_config=ic))
                        assert a + b == ab, "page slicing mismatch"
                        assert not b or a != b, "page two repeats page one"
                        row = {
                            "provider": site,
                            "method": name,
                            "status": "PASS" if a else "EMPTY_UNVERIFIED",
                            "counts": [len(a), len(b), len(ab)],
                        }
                    except Exception as e:
                        row = {"provider": site, "method": name, "status": "FAIL", "error_type": type(e).__name__}
                    print(json.dumps(row), flush=True)
                    results.append(row)
        except Exception as e:
            row = {"provider": site, "status": "BLOCKED", "error_type": type(e).__name__}
            print(json.dumps(row), flush=True)
            results.append(row)
    (OUTPUT / "accounts.json").write_text(json.dumps(results, indent=2))
    if any(row["status"] != "PASS" for row in results):
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
