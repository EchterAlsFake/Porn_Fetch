"""Opt-in live account checks using one browser's real site-scoped cookies.

Run: uv run python -m src.tests.smoke.account_cookies --browser brave
No credentials, account names, cookie values or video URLs are written to reports.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import re
import tempfile
import time
from contextlib import aclosing
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from selectolax.lexbor import LexborHTMLParser

from src.cli.accounts import AccountService
from src.cli.media import prepare_video
from src.cli.providers import ClientPool
from src.cli.settings import CliSettings
from src.shared.provider_accounts import valid_xhamster_playlist_url, verify_account_session
from src.shared.provider_routing import ContentKind, route_url, unwrap_scrape_result
from src.shared.tor_transport import MediaCore

PROVIDERS = ("pornhub", "xhamster", "xvideos")
COLLECTIONS = {"pornhub": ("history", "favorites", "recommended", "feed"),
               "xhamster": ("liked",), "xvideos": ("history", "liked", "watch_later")}


class CheckFailed(Exception):
    """A diagnostic with a deliberately non-sensitive message."""


class AccountCore(MediaCore):
    async def download(self, *args, **kwargs):
        raise CheckFailed("Media downloads are forbidden in account checks")

    async def legacy_download(self, *args, **kwargs):
        raise CheckFailed("Media downloads are forbidden in account checks")

    async def download_segment(self, *args, **kwargs):
        raise CheckFailed("Media downloads are forbidden in account checks")


async def sample(stream, provider, limit, *, require_items=True):
    rows = []
    async with aclosing(stream):
        async for result in stream:
            source = unwrap_scrape_result(result)
            route = route_url(source.url)
            if route.provider != provider or route.kind != ContentKind.VIDEO:
                raise CheckFailed("Account iterator returned an unexpected provider or media type")
            media = await prepare_video(source, provider)
            if not media.title or media.title == "Untitled":
                raise CheckFailed("Video metadata has no usable title")
            rows.append({"title_present": True, "duration_minutes": media.length,
                         "qualities": media.qualities})
            if len(rows) >= limit:
                break
    if require_items and not rows:
        raise CheckFailed("Seeded account collection returned no videos")
    return {"status": "PASS" if rows else "EMPTY", "rows_sampled": len(rows), "metadata": rows}


async def discover_playlist(client, provider):
    if provider == "pornhub":
        url = f"https://www.pornhub.com/users/{client.account.name}/playlists"
        pattern = r"/playlist/\d+(?:/|$)"
    elif provider == "xhamster":
        url = "https://xhamster.com/my/favorites/videos"
        pattern = r"/my/(?:favorites/videos|playlists)/[^/]+"
    else:
        url = "https://www.xvideos.com/account/playlists"
        pattern = r"/(?:favorite|playlist)/\d+(?:/|$)"
    html = await client.core.fetch_text(url)
    tree = LexborHTMLParser(html)
    for node in tree.css("a[href]"):
        candidate = urljoin(url, node.attributes["href"])
        parsed = urlsplit(candidate)
        if parsed.hostname == urlsplit(url).hostname and re.fullmatch(pattern, parsed.path):
            return candidate
    return None


async def run(args, *, password=None, usernames=None):
    import xhamster_api

    report = {
        "scope": "Real account authentication, native account iterators and video metadata",
        "authentication": "password" if password is not None else "browser-cookies",
        "browser": args.browser if password is None else None,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "libraries": {name: version(name) for name in ("eaf-base-api", "browser-cookie3", *(
            f"unofficial-api-for-{provider}" for provider in args.providers))},
        "xhamster_source": str(Path(xhamster_api.__file__).resolve()),
        "checks": [], "interrupted": False,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)

    def save():
        report["counts"] = {status: sum(row["status"] == status for row in report["checks"])
                            for status in ("PASS", "EMPTY", "FAIL", "UNVERIFIED", "UNSUPPORTED", "INTERRUPTED")}
        descriptor = os.open(args.report, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=2)
            file.write("\n")

    async def check(provider, name, operation):
        print(f"RUN {provider} {name}", flush=True)
        row = {"provider": provider, "check": name, "status": "FAIL"}
        started = time.monotonic()
        try:
            async with asyncio.timeout(args.timeout):
                row.update(await operation())
        except asyncio.CancelledError:
            row["status"] = "INTERRUPTED"
            report["interrupted"] = True
            raise
        except Exception as error:
            row["error_type"] = type(error).__name__
            # Upstream exception messages can contain signed URLs or session data.
            row["error"] = str(error) if isinstance(error, CheckFailed) else "See error_type; upstream details omitted"
        finally:
            row["elapsed_seconds"] = round(time.monotonic() - started, 2)
            report["checks"].append(row)
            save()
            print(f"{row['status']} {provider} {name}"
                  f"{': ' + row['error'] if row.get('error') else ''}", flush=True)
        return row["status"]

    settings = CliSettings(timeout=20, request_attempts=2, response_cache_mb=0, segment_cache_mb=0,
                           pages_concurrency=1, videos_concurrency=1)
    save()
    try:
        for provider in args.providers:
            async with ClientPool(settings.to_runtime_config(), core_factory=AccountCore) as pool:
                service = AccountService(pool)

                async def login():
                    if password is None:
                        ok = await service.login(provider, browser=True, browser_name=args.browser,
                                                 username=args.pornhub_username if provider == "pornhub" else "")
                    else:
                        if provider == "xvideos" and not hasattr(pool.client(provider), "login"):
                            return {"status": "UNSUPPORTED", "reason": "The provider library exposes cookie authentication only"}
                        ok = await service.login(provider, username=(usernames or {})[provider], password=password)
                        await verify_account_session(pool.client(provider), provider)
                    if not ok or not service.logged_in(provider):
                        raise CheckFailed("Account login was not confirmed")
                    return {"status": "PASS", "server_authenticated": True}

                if await check(provider, "password-login" if password is not None else "cookie-login", login) != "PASS":
                    continue

                for collection in COLLECTIONS[provider]:
                    async def listing(name=collection):
                        stream, _ = service.collection(provider, name, pages=1)
                        return await sample(stream, provider, args.items,
                                            require_items=name in {"history", "favorites", "liked"})

                    await check(provider, collection, listing)

                async def playlist():
                    client = pool.client(provider)
                    url = args.playlists.get(provider) or await discover_playlist(client, provider)
                    if not url:
                        return {"status": "UNVERIFIED", "reason": "No account playlist URL discovered; supply --playlist PROVIDER=URL"}
                    if provider == "pornhub":
                        source = await client.get_playlist(url, load_html=True)
                        stream = source.get_videos(pages=1)
                    elif provider == "xhamster":
                        stream, _ = service.collection(provider, "playlist", url, pages=1)
                    else:
                        stream = client.get_playlist(url, pages=1)
                    return await sample(stream, provider, args.items)

                await check(provider, "account-playlist", playlist)

            async def anonymous():
                async with ClientPool(settings.to_runtime_config(), core_factory=AccountCore) as clean:
                    client = clean.client(provider)
                    try:
                        await verify_account_session(client, provider)
                    except ValueError:
                        return {"status": "PASS", "anonymous_session_rejected": True}
                    raise CheckFailed("An anonymous session was incorrectly accepted as authenticated")

            await check(provider, "anonymous-rejected", anonymous)
    except asyncio.CancelledError:
        print(f"Stopped. Partial report: {args.report}", flush=True)
        return 130
    counts = report["counts"]
    print(", ".join(f"{count} {status.lower()}" for status, count in counts.items()) + f". Report: {args.report}")
    return int(bool(counts["FAIL"] or counts["UNVERIFIED"] or counts["UNSUPPORTED"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", choices=("brave", "chrome", "firefox", "edge", "vivaldi", "opera", "librewolf"), default="brave")
    parser.add_argument("--provider", choices=PROVIDERS, action="append")
    parser.add_argument("--pornhub-username", default="", help="Optional expected account username; otherwise discovered from the authenticated menu")
    parser.add_argument("--playlist", action="append", default=[], metavar="PROVIDER=URL")
    parser.add_argument("--items", type=int, choices=(1, 2, 3), default=2)
    parser.add_argument("--timeout", type=float, default=90, help="Seconds per account check")
    parser.add_argument("--report", type=Path, default=Path(tempfile.gettempdir()) / "porn-fetch-account-cookies.json")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    args.providers = list(dict.fromkeys(args.provider or PROVIDERS))
    args.playlists = {}
    for item in args.playlist:
        provider, separator, url = item.partition("=")
        if separator != "=" or provider not in PROVIDERS:
            parser.error("--playlist must be PROVIDER=URL")
        parsed = urlsplit(url)
        try:
            if provider == "xhamster":
                valid = valid_xhamster_playlist_url(url)
            else:
                route = route_url(url)
                valid = parsed.scheme == "https" and route.provider == provider and route.kind == ContentKind.COLLECTION
        except ValueError:
            valid = False
        if not valid:
            parser.error("Playlist must be an HTTPS collection URL on the selected provider's website")
        args.playlists[provider] = url
    logging.disable(logging.CRITICAL)
    try:
        return asyncio.run(run(args))
    except KeyboardInterrupt:
        print(f"Stopped. Last saved report: {args.report}", flush=True)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
