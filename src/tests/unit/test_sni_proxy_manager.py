from __future__ import annotations

import unittest
from unittest.mock import patch

from src.backend.sni_proxy_manager import FAIL_CLOSED_PROXY_URL, SNIProxyManager


class _Signal:
    def __init__(self) -> None:
        self.callbacks = []

    def connect(self, callback) -> None:
        self.callbacks.append(callback)

    def emit(self, value=None) -> None:
        for callback in tuple(self.callbacks):
            callback(value)


class _Settings:
    def __init__(self) -> None:
        self.sni_obfuscation = True
        self.sni_obfuscation_lite = True
        self.sni_obfuscation_strict = False
        self.sni_obfuscation_strict_profile = "Strict Fragmentation"
        self.proxy = ""
        self.interface = ""
        self.active_sni_proxy_url = None
        self.proxyChanged = _Signal()
        self.interfaceChanged = _Signal()


class _Process:
    instances = []

    def __init__(self, config) -> None:
        self.config = config
        self.stopped = False
        self.is_running = True
        self.instances.append(self)

    def start(self) -> str:
        return f"socks5://127.0.0.1:{41000 + len(self.instances)}"

    def stop(self) -> None:
        self.stopped = True
        self.is_running = False


class SNIProxyManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        _Process.instances.clear()

    @patch("src.backend.sni_proxy_manager.FragmentingProxyProcess", _Process)
    def test_lite_start_and_upstream_proxy_restart(self) -> None:
        settings = _Settings()
        manager = SNIProxyManager(settings)

        first_url = manager.start()
        self.assertEqual(first_url, "socks5://127.0.0.1:41001")
        self.assertEqual(settings.active_sni_proxy_url, first_url)
        self.assertIsNone(_Process.instances[0].config.upstream_proxy)

        settings.proxy = "socks5h://127.0.0.1:9050"
        settings.proxyChanged.emit(settings.proxy)

        self.assertTrue(_Process.instances[0].stopped)
        self.assertEqual(len(_Process.instances), 2)
        self.assertEqual(_Process.instances[1].config.upstream_proxy, settings.proxy)
        self.assertEqual(settings.active_sni_proxy_url, "socks5://127.0.0.1:41002")
        manager.stop()

    @patch("src.backend.sni_proxy_manager.FragmentingProxyProcess", _Process)
    def test_invalid_mode_fails_closed(self) -> None:
        settings = _Settings()
        settings.sni_obfuscation_strict = True
        manager = SNIProxyManager(settings)

        self.assertEqual(manager.start(), FAIL_CLOSED_PROXY_URL)
        self.assertEqual(settings.active_sni_proxy_url, FAIL_CLOSED_PROXY_URL)
        self.assertIsNotNone(manager.last_error)
        self.assertFalse(manager.is_running)

    @patch("src.backend.sni_proxy_manager.StrictFragmentingProxyProcess", _Process)
    def test_strict_desync_profile_enables_reverse_and_decoy(self) -> None:
        settings = _Settings()
        settings.sni_obfuscation_lite = False
        settings.sni_obfuscation_strict = True
        settings.sni_obfuscation_strict_profile = "Strict Desync"
        manager = SNIProxyManager(settings)

        manager.start()

        config = _Process.instances[0].config
        self.assertTrue(config.reverse_fragments)
        self.assertEqual(config.desync_config.mode, "seq_ack")
        manager.stop()


if __name__ == "__main__":
    unittest.main()
