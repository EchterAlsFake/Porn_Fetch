"""Read-only live user-feed checks with explicitly selected Brave sessions."""

from .common import *
import browser_cookie3
from urllib.parse import urlsplit, urljoin
from selectolax.lexbor import LexborHTMLParser


class UserCore(BaseCore):
    async def fetch_text(self, url, **kwargs):
        text = await super().fetch_text(url, **kwargs)
        if "/videos-data" in url:
            self.pages.append(json.loads(text))
        return text


async def main():
    rows = []
    for site in ("redtube", "tube8"):
        try:
            jar = await asyncio.to_thread(browser_cookie3.brave, domain_name=site + ".com")
            settings = RuntimeConfig()
            settings.request_attempts = 3
            async with UserCore(configuration=settings) as core:
                core.pages = []
                module = importlib.import_module(site + "_api.api")
                client = module.Client(core=core)
                core.session.cookies.update(jar)
                homepage = await core.fetch_text("https://www." + site + ".com/")
                tree = LexborHTMLParser(homepage)
                assert any("logout" in n.attributes["href"] for n in tree.css("a[href]")), "No authenticated session"
                candidates = [
                    n
                    for n in tree.css("a[href]")
                    if (
                        "userMenuItem" in n.attributes.get("class", "")
                        or n.text(strip=True).casefold() in {"my profile", "your profile", "profile"}
                    )
                    and "/user/" in urlsplit(n.attributes["href"]).path
                ]
                if candidates:
                    url = urljoin(homepage.url, candidates[0].attributes["href"])
                elif site == "redtube":
                    url = "https://www.redtube.com/user/emilscc"
                else:
                    raise AssertionError("Site did not expose its authenticated profile link")
                user = module.User(core=core, url=url)
                first = await collect(user.get_videos(pages=1, start_page=1, iterator_config=config))
                second = await collect(user.get_videos(pages=1, start_page=2, iterator_config=config))
                complete = await collect(user.get_videos(pages="all", iterator_config=config))
                assert core.pages, "No real JSON listing response was observed"
                first_block = core.pages[0]["data"]
                assert first_block["success"] is True, "Source did not expose the collection"
                if not first:
                    assert first_block["count"] == 0 and first_block["pagination"]["totalPages"] == 0, (
                        "Empty output did not match source metadata"
                    )
                    assert not second and not complete, "Empty collection produced subsequent items"
                else:
                    assert first != second, "Second page repeated first page"
                    assert complete[: len(first) + len(second)] == first + second, "Start/page-count mismatch"
                rows.append(
                    {
                        "provider": site,
                        "kind": "User.videos",
                        "status": "PASS",
                        "authenticated": True,
                        "counts": [len(first), len(second), len(complete)],
                        "empty_fixture": not first,
                        "source_metadata_checked": True,
                    }
                )
        except Exception as error:
            rows.append(
                {
                    "provider": site,
                    "kind": "User.videos",
                    "status": "FAIL",
                    "error_type": type(error).__name__,
                    "reason": str(error) if isinstance(error, AssertionError) else None,
                }
            )
        print(json.dumps(rows[-1]), flush=True)
    (OUTPUT / "user-feeds.json").write_text(json.dumps(rows, indent=2))
    if any(row["status"] != "PASS" for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())
