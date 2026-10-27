"""Official regional links advertised by provider watch pages."""
import unittest

from src.shared.provider_routing import PROVIDER_MODULES, ContentKind, route_url


class RegionalApiRoutes(unittest.TestCase):
    def test_official_regional_video_links(self):
        for url, provider in (
            ('https://www.xnxx.es/video-1gav4l94/example', 'xnxx'),
            ('https://www.xnxx-ru.com/video-1gav4l94/example', 'xnxx'),
            ('https://www.xnxx-arabic.com/video-abc/example', 'xnxx'),
            ('https://www.xnxx-india.com/video-abc/example', 'xnxx'),
            ('https://de.tube8.com/porn-video/264330411/', 'tube8'),
            ('https://www.tube8.fr/porn-video/264330411/', 'tube8'),
            ('https://www.tube8.es/porn-video/264330411/', 'tube8'),
        ):
            with self.subTest(url=url):
                route = route_url(url)
                self.assertEqual(route.provider, provider)
                self.assertEqual(route.kind, ContentKind.VIDEO)
                self.assertEqual(route.url, url)

    def test_suffix_lookalikes_are_rejected(self):
        for host in ('xnxx.es.example.com', 'evilxnxx-ru.com', 'tube8.fr.example.com', 'eviltube8.fr'):
            with self.subTest(host=host), self.assertRaises(ValueError):
                route_url('https://' + host + '/video-abc/example')

    def test_excluded_providers_stay_out(self):
        self.assertNotIn('hqporner', PROVIDER_MODULES)
        self.assertNotIn('missav', PROVIDER_MODULES)
        for url in ('https://hqporner.com/hdporn/123.html', 'https://missav.ws/en/example'):
            with self.assertRaises(ValueError):
                route_url(url)
