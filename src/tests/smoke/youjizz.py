"""Opt-in live YouJizz Video/Collection/Pornstar/User application checks.

Run: python -m src.tests.smoke.youjizz --gui --report /tmp/youjizz-app.json
Importing this module starts neither network requests nor downloads.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import tempfile
from contextlib import aclosing
from datetime import datetime, timezone
from html.parser import HTMLParser
from importlib.metadata import version
from pathlib import Path
from urllib.parse import urljoin

from base_api import IteratorConfig
from base_api.modules.config import RuntimeConfig

from src.cli.downloads import DownloadController, download_video
from src.cli.media import prepare_video
from src.cli.providers import ClientPool
from src.cli.settings import CliSettings
from src.shared.access import public_collection_items
from src.shared.media import VideoFilters
from src.shared.provider_routing import ContentKind, container_stream, route_url, unwrap_scrape_result
from src.tests.smoke.bellesa import probe


class LiveListing(HTMLParser):
    """Independent extraction from the actual listing links and Next controls."""

    def __init__(self, content):
        super().__init__()
        self.ids, self.next = [], None
        self.feed(content)

    def handle_starttag(self, tag, attributes):
        data = dict(attributes)
        classes = set(data.get('class', '').split())
        if tag == 'a' and 'frame' in classes and 'related-thumb' not in classes and data.get('data-video-id'):
            if data['data-video-id'] not in self.ids:
                self.ids.append(data['data-video-id'])
        if tag == 'a' and 'pagination-next' in classes:
            self.next = data.get('href')


async def collect(stream):
    async with aclosing(stream):
        return [unwrap_scrape_result(item) async for item in stream]


async def observed(core, url, *, all_pages):
    ids, pages, visited = [], [], set()
    while url:
        assert url not in visited, 'Repeated live page'
        visited.add(url)
        page = LiveListing(await core.fetch_text(url))
        ids.extend(page.ids)
        pages.append(len(page.ids))
        url = urljoin(url, page.next) if all_pages and page.next else None
    return ids, pages


async def run(args, workspace):
    from youjizz_api import Collection, Pornstar, User, Video

    report = {'package': version('unofficial-api-for-youjizz'),
              'started_at_utc': datetime.now(timezone.utc).isoformat(),
              'routes': [], 'collections': [], 'downloads': [], 'gui': []}

    def save():
        args.report.write_text(json.dumps(report, indent=2) + '\n')

    runtime = RuntimeConfig()
    runtime.timeout = 25
    runtime.request_attempts = 2
    runtime.pages_concurrency = 1
    runtime.videos_concurrency = 2
    runtime.max_workers_download = 3
    settings = CliSettings(skip_existing=False, write_metadata=True, download_workers=3, request_attempts=2)
    async with ClientPool(runtime) as pool:
        for host in ('youjizz.com', 'www.youjizz.com'):
            for path, expected, kind in (
                ('/videos/video-55374481.html', Video, ContentKind.VIDEO),
                ('/most-popular/1.html', Collection, ContentKind.COLLECTION),
                ('/search/Abby-Marie-1.html', Pornstar, ContentKind.PROFILE),
                ('/profile/user/15100401', User, ContentKind.PROFILE),
            ):
                route, target = await pool.resolve('https://' + host + path)
                assert route.provider == 'youjizz' and route.kind == kind and type(target) is expected
                if expected is Video:
                    media = await prepare_video(target, 'youjizz')
                    assert media.video_id == '55374481' and media.length == 1
                    assert media.qualities == [240, 360, 480, 720, 1080]
                    assert media.thumbnail_url and media.tags and media.publish_date
                report['routes'].append({'host': host, 'class': expected.__name__, 'kind': str(kind)})
                save()
        for path, expected, all_pages in (
            ('/most-popular/1.html', Collection, False),
            ('/search/Abby-Marie-1.html', Pornstar, True),
            ('/search/Abby-Paradise-1.html', Pornstar, True),
            ('/profile/user/15100401', User, True),
        ):
            url = 'https://www.youjizz.com' + path
            _, target = await pool.resolve(url)
            assert type(target) is expected
            if expected is User:
                raw = json.loads(await target.core.fetch_text('https://www.youjizz.com/api/socialVideos/15100401?order=recent'))
                expected_ids = list(map(str, raw))
                pages = [len(raw[i:i+24]) for i in range(0, len(raw), 24)]
                for i in range(0, len(raw), 24):
                    chunk = raw[i:i+24]
                    thumbs = json.loads(await target.core.fetch_text('https://www.youjizz.com/api/thumbs?ids=' + '-'.join(map(str, chunk))))
                    assert [str(v['record_num']) for v in thumbs] == list(map(str, chunk))
            else:
                # Establish cookies before comparing the public live session.
                await target.core.fetch_text(url)
                expected_ids, pages = await observed(target.core, url, all_pages=all_pages)
            actual = await collect(container_stream(target, provider='youjizz', pages=len(pages) + (1 if all_pages else 0),
                                                    iterator_config=IteratorConfig(order='original')))
            assert expected_ids and [v.video_id for v in actual] == expected_ids
            preview = await collect(public_collection_items(pool.media_stream(url, pages=1), False))
            assert [v.video_id for v in preview] == expected_ids[:5]
            report['collections'].append({'url': url, 'class': expected.__name__, 'pages': pages,
                                           'expected': len(expected_ids), 'actual': len(actual),
                                           'free_preview': len(preview), 'directory_count': getattr(target, 'video_count', None)})
            print(expected.__name__, len(expected_ids), len(actual), 'pages', len(pages), flush=True)
            save()
        for path in ('/', '/random', '/tags', '/tags/anal-1.html', '/categories/anal-1.html',
                     '/pornstars', '/pornstars/name/A', '/profile/my/favorites', '/profile/user/15100401/favorites'):
            try:
                route_url('https://www.youjizz.com' + path)
            except ValueError:
                continue
            raise AssertionError('Excluded method route accepted: ' + path)
        try:
            await pool.resolve('https://www.youjizz.com/search/not-a-real-performer-1.html')
        except ValueError:
            pass
        else:
            raise AssertionError('Keyword search was exposed')
        sources = {}
        for uid in ('55374481', '48914471', '75799072', '80517371', '51957501'):
            _, source = await pool.resolve('https://www.youjizz.com/videos/video-' + uid + '.html')
            media = await prepare_video(source, 'youjizz')
            sources[uid] = source, media
        assert sources['48914471'][1].qualities == [240, 288, 360, 480, 720]
        assert sources['75799072'][1].qualities == [240, 360, 368]
        assert sources['80517371'][1].qualities == [134, 202, 270, 404, 1080]
        assert sources['51957501'][1].qualities == [404]
        if not args.metadata_only:
            cases = [(uid, str(q), True, q) for uid, (_, row) in sources.items() for q in row.qualities]
            cases += [('55374481', 'best', False, 720), ('80517371', 'best', False, 404),
                      ('55374481', 'half', True, 480), ('55374481', 'worst', True, 240),
                      ('55374481', '999', True, 1080), ('55374481', '1080', False, 720)]
            for index, (uid, request, premium, expected_quality) in enumerate(cases):
                source, media = sources[uid]
                path = workspace / f'{index}-{uid}-{expected_quality}.mp4'
                controller = DownloadController(url=source.url, target=path, provider='youjizz', state_directory=workspace/'state')
                outcome = await download_video(source, path, request, settings, has_premium=premium,
                                               available_qualities=None, metadata=media, controller=controller)
                assert outcome.status == 'completed' and not outcome.missing_segments
                info = await asyncio.to_thread(probe, path)
                assert min(info['width'], info['height']) == expected_quality
                assert abs(info['duration'] - source.duration) < 2
                assert info['audio'] == (uid != '51957501')
                assert info['tags'].get('title') == media.title and info['tags'].get('artist') == media.author
                report['downloads'].append({'id': uid, 'request': request, 'premium': premium, 'quality': expected_quality, **info})
                save()
                print('DOWNLOAD', uid, expected_quality, info['width'], info['height'], flush=True)
    if args.gui:
        from PySide6.QtGui import QGuiApplication

        from src.backend import clients
        from src.backend.application import stop_flag
        from src.backend.profile_diagnostics import diagnostic_settings, make_test_backend, test_profile_url

        app = QGuiApplication.instance() or QGuiApplication([])
        app.setQuitOnLastWindowClosed(False)
        try:
            for path in ('/search/Abby-Marie-1.html', '/profile/user/15100401'):
                stop_flag.clear()
                backend = make_test_backend()
                case = {'provider': 'youjizz', 'url': 'https://www.youjizz.com' + path}
                evidence = await test_profile_url(backend, backend._downloads_model, case, items=1)
                assert evidence['rows'] == 1
                report['gui'].append({'url': case['url'], **evidence})
                save()
            stop_flag.clear()
            backend = make_test_backend()
            with diagnostic_settings(items=2):
                await backend._process_playlist_url('https://www.youjizz.com/most-popular/1.html', '$index-$title', VideoFilters())
            assert backend._downloads_model.rowCount() == 2
            report['gui'].append({'class': 'Collection', 'rows': 2})
            source = await clients.get_video('https://www.youjizz.com/videos/video-80517371.html')
            row = await clients.load_video_attributes(source)
            assert row.qualities == [134, 202, 270, 404, 1080] and row.length == 1
            old_core, old_client = clients.core_yj, clients.yj_client
            clients.refresh_clients()
            await clients.close_retired_sessions()
            assert clients.core_yj is old_core and clients.yj_client is old_client
            assert (await clients.load_video_attributes(await clients.get_video(source.url))).qualities == row.qualities
        finally:
            stop_flag.clear()
            await clients.close_all_clients()
    report['passed'] = True
    report['metadata_only'] = args.metadata_only
    save()
    print('PASS YouJizz integration:', args.report, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--metadata-only', action='store_true')
    parser.add_argument('--gui', action='store_true')
    parser.add_argument('--report', type=Path, default=Path('/tmp/youjizz-app.json'))
    args = parser.parse_args()
    args.report = args.report.resolve()
    args.report.parent.mkdir(parents=True, exist_ok=True)
    logging.disable(logging.CRITICAL)
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    os.environ.setdefault('QT_QUICK_BACKEND', 'software')
    with tempfile.TemporaryDirectory(prefix='porn-fetch-youjizz-') as folder:
        workspace = Path(folder)
        for kind in ('CONFIG', 'CACHE', 'DATA'):
            os.environ[f'XDG_{kind}_HOME'] = str(workspace/kind.lower())
        asyncio.run(run(args, workspace))


if __name__ == '__main__':
    main()
