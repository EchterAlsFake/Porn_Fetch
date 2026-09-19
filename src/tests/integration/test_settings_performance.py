from __future__ import annotations

from src.tests.integration.settings_support import SettingsGUITestBase


class TestPerformanceTabGUI(SettingsGUITestBase):
    """Verifies that every change made on the Performance settings tab modifies the actual settings file."""

    def test_download_workers_spinbox(self) -> None:
        self.simulate_spinbox("downloadWorkersSpinBox", 32)
        self.assertEqual(self.settings_manager.download_workers, 32)
        self.assert_file_value("Performance/download_workers", 32)

    def test_network_delay_spinbox(self) -> None:
        self.simulate_spinbox("networkDelaySpinBox", 5)
        self.assertEqual(self.settings_manager.network_delay, 5)
        self.assert_file_value("Performance/network_delay", 5)

    def test_parallel_downloads_spinbox(self) -> None:
        self.simulate_spinbox("parallelDownloadsSpinBox", 4)
        self.assertEqual(self.settings_manager.parallel_downloads, 4)
        self.assert_file_value("Performance/semaphore", 4)

    def test_retries_spinbox(self) -> None:
        self.simulate_spinbox("retriesSpinBox", 8)
        self.assertEqual(self.settings_manager.retries, 8)
        self.assert_file_value("Performance/retries", 8)

    def test_timeout_spinbox(self) -> None:
        self.simulate_spinbox("timeoutSpinBox", 25)
        self.assertEqual(self.settings_manager.timeout, 25)
        self.assert_file_value("Performance/timeout", 25)

    def test_processing_delay_spinbox(self) -> None:
        self.simulate_spinbox("processingDelaySpinBox", 3)
        self.assertEqual(self.settings_manager.processing_delay, 3)
        self.assert_file_value("Performance/processing_delay", 3)

    def test_speed_limit_decimal_spinbox(self) -> None:
        self.simulate_decimal_spinbox("speedLimitSpinBox", 14.5)
        self.assertAlmostEqual(self.settings_manager.speed_limit, 14.5, places=2)
        self.assert_file_value("Performance/speed_limit", 14.5)

    def test_videos_concurrency_spinbox(self) -> None:
        self.simulate_spinbox("videosConcurrencySpinBox", 16)
        self.assertEqual(self.settings_manager.videos_concurrency, 16)
        self.assert_file_value("Performance/videos_concurrency", 16)

    def test_pages_concurrency_spinbox(self) -> None:
        self.simulate_spinbox("pagesConcurrencySpinBox", 5)
        self.assertEqual(self.settings_manager.pages_concurrency, 5)
        self.assert_file_value("Performance/pages_concurrency", 5)

    def test_response_cache_size_spinbox(self) -> None:
        self.simulate_spinbox("responseCacheSizeSpinBox", 64)
        self.assertEqual(self.settings_manager.response_cache_size, 64)
        self.assert_file_value("Performance/response_cache_size", 64)

    def test_response_cache_ttl_spinbox(self) -> None:
        self.simulate_spinbox("responseCacheTTLSpinBox", 600)
        self.assertEqual(self.settings_manager.response_cache_ttl, 600)
        self.assert_file_value("Performance/response_cache_ttl", 600)

    def test_segment_cache_size_spinbox(self) -> None:
        self.simulate_spinbox("segmentCacheSizeSpinBox", 16)
        self.assertEqual(self.settings_manager.segment_cache_size, 16)
        self.assert_file_value("Performance/segment_cache_size", 16)

    def test_segment_cache_ttl_spinbox(self) -> None:
        self.simulate_spinbox("segmentCacheTTLSpinBox", 900)
        self.assertEqual(self.settings_manager.segment_cache_ttl, 900)
        self.assert_file_value("Performance/segment_cache_ttl", 900)

    def test_request_initial_retry_delay_decimal_spinbox(self) -> None:
        self.simulate_decimal_spinbox("requestInitialRetryDelaySpinBox", 1.75)
        self.assertAlmostEqual(self.settings_manager.request_initial_retry_delay, 1.75, places=2)
        self.assert_file_value("Performance/request_initial_retry_delay", 1.75)

    def test_request_retry_max_delay_decimal_spinbox(self) -> None:
        self.simulate_decimal_spinbox("requestRetryMaxDelaySpinBox", 45.0)
        self.assertAlmostEqual(self.settings_manager.request_retry_max_delay, 45.0, places=2)
        self.assert_file_value("Performance/request_retry_max_delay", 45.0)

    def test_request_retry_multiplier_decimal_spinbox(self) -> None:
        self.simulate_decimal_spinbox("requestRetryMultiplierSpinBox", 3.5)
        self.assertAlmostEqual(self.settings_manager.request_retry_multiplier, 3.5, places=2)
        self.assert_file_value("Performance/request_retry_multiplier", 3.5)

    def test_request_retry_jitter_decimal_spinbox(self) -> None:
        self.simulate_decimal_spinbox("requestRetryJitterSpinBox", 0.8)
        self.assertAlmostEqual(self.settings_manager.request_retry_jitter, 0.8, places=2)
        self.assert_file_value("Performance/request_retry_jitter", 0.8)

