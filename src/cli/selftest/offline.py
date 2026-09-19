"""Fast, deterministic CLI diagnostics that never use the network."""
from __future__ import annotations

import tempfile
import time
from pathlib import Path

from src.database import PocketBaseTracker
from src.shared.media import select_allowed_quality

from ..model_store import ModelStore
from ..providers import ContentKind, route_url
from ..settings import CliSettings, SettingsStore
from .models import TestResult


async def run_offline_tests() -> list[TestResult]:
    results: list[TestResult] = []

    started = time.perf_counter()
    try:
        samples = {
            "https://pornhub.com/view_video.php?viewkey=test": ("pornhub", ContentKind.VIDEO),
            "https://xvideos.com/pornstars/test": ("xvideos", ContentKind.PROFILE),
            "https://youporn.com/collections/12/test": ("youporn", ContentKind.COLLECTION),
            "https://xfreehd.com/album/12/test": ("xfreehd", ContentKind.GALLERY),
        }
        for url, expected in samples.items():
            route = route_url(url)
            assert (route.provider, route.kind) == expected
        results.append(TestResult("Offline", "URL routing", f"{len(samples)} routes", True, "All routes matched", time.perf_counter() - started))
    except Exception as error:
        results.append(TestResult("Offline", "URL routing", "routing table", False, "", time.perf_counter() - started, str(error)))

    started = time.perf_counter()
    try:
        qualities = [360, 720, 1080, 2160]
        assert select_allowed_quality("best", qualities, False) == "720"
        assert select_allowed_quality("best", qualities, True) == "2160"
        results.append(TestResult("Offline", "Quality access", "free and premium", True, "Quality limits verified", time.perf_counter() - started))
    except Exception as error:
        results.append(TestResult("Offline", "Quality access", "quality rules", False, "", time.perf_counter() - started, str(error)))

    started = time.perf_counter()
    try:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            settings_store = SettingsStore(root / "settings.json")
            settings = settings_store.load(legacy_paths=[]).overridden(quality="720")
            settings_store.save(settings)
            assert settings_store.load().quality == "720"

            model_store = ModelStore(root / "models.json", legacy_paths=[])
            model_store.add("https://example.test/model")
            model_store.update_pending("https://example.test/model", ["one", "two"])
            model_store.mark_downloaded("https://example.test/model", "one")
            assert model_store.counts("https://example.test/model") == (1, 1)
        results.append(TestResult("Offline", "Persistence", "settings and tracked models", True, "Atomic stores verified", time.perf_counter() - started))
    except Exception as error:
        results.append(TestResult("Offline", "Persistence", "local stores", False, "", time.perf_counter() - started, str(error)))

    started = time.perf_counter()
    try:
        assert PocketBaseTracker.status_bucket("completed") == "successful"
        assert PocketBaseTracker.status_bucket("failed") == "failed"
        assert PocketBaseTracker.status_bucket("paused") == "other"
        CliSettings().validate()
        results.append(TestResult("Offline", "Core models", "database status and settings", True, "Models validated", time.perf_counter() - started))
    except Exception as error:
        results.append(TestResult("Offline", "Core models", "core models", False, "", time.perf_counter() - started, str(error)))

    return results
