"""Observable settings effects: native HTTP/TLS, real providers and real files."""
from __future__ import annotations

import asyncio
import hashlib
import io
import json
import logging
import os
import re
import sys
import time
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlsplit

from PySide6.QtCore import QMetaObject, QObject

from src.tests.settings_cases import CASE_BY_PROPERTY
from src.tests.smoke.download_lifecycle import lifecycle_fixtures, require, validate_media


async def pump(gui, seconds=0):
    deadline = time.monotonic() + seconds
    while True:
        gui.pump()
        if time.monotonic() >= deadline:
            return
        await asyncio.sleep(.01)


async def wait(gui, predicate, message="Settings effect did not finish"):
    while not predicate():
        gui.pump()
        await asyncio.sleep(.01)
    gui.pump()


async def change(gui, prop, value):
    gui.activate(prop, value)
    await gui.clients.close_retired_sessions()
    await pump(gui)


async def baseline(gui):
    for prop, value in {"service_transport": "direct", "sni_obfuscation": False,
                        "proxy": "", "interface": "", "custom_ja3": "", "impersonation": "chrome",
                        "encrypted_ch": False, "dns_over_https": False, "trust_environment": False,
                        "retries": 1, "timeout": 20, "network_delay": 0, "processing_delay": 0,
                        "download_workers": 1, "videos_concurrency": 1, "pages_concurrency": 1,
                        "speed_limit": 0, "response_cache_size": 0, "segment_cache_size": 0,
                        "enable_logging": False, "supress_errors": False, "anonymous_mode": False}.items():
        if getattr(gui.settings, prop) != value:
            await change(gui, prop, value)
    gui.errors.clear()


def control(gui, name, job=None):
    from src.backend.account_diagnostics import visual_items
    root = gui.window.contentItem()
    if job is not None:
        root = next(item for item in visual_items(root) if item.objectName() == "downloadRow" and item.property("jobId") == job)
    found = [item for item in visual_items(root) if item.objectName() == name]
    require(len(found) == 1, f"Expected one {name}")
    return found[0]


def click(gui, name, job=None):
    item = control(gui, name, job)
    require(item.property("enabled"), f"{name} is disabled")
    item.clicked.emit()
    gui.pump()


async def prepare(gui, provider="pornhub", filename="settings.mp4"):
    fixtures = {name: url for name, _, url in lifecycle_fixtures()}
    before = gui.model.rowCount()
    control(gui, "downloadTitlePattern").setProperty("text", filename)
    control(gui, "videoUrlInput").setProperty("text", fixtures[provider])
    gui.pump()
    click(gui, "getVideoButton")
    task = gui.backend._video_fetch_task
    require(task is not None, "Get Video did not start preparation")
    await wait(gui, task.done)
    await task
    await asyncio.sleep(0)
    require(gui.model.rowCount() == before + 1 and not gui.errors, f"Real video did not reach the list: {gui.errors}")
    from PySide6.QtCore import Qt
    QMetaObject.invokeMethod(control(gui, "downloadList"), "forceLayout", Qt.ConnectionType.DirectConnection)
    await pump(gui, .05)
    job = gui.model.data(gui.model.index(before, 0), gui.model.JobIdRole)
    return job, gui.model.get_video(job)


async def transfer(gui, job):
    click(gui, "downloadStartButton", job)
    task = gui.backend._download_tasks.get(job)
    require(task is not None, "Download control did not create a task")
    await wait(gui, lambda: job not in gui.backend._download_tasks)
    await task
    await asyncio.sleep(0)


async def clear(gui):
    for row in reversed(range(gui.model.rowCount())):
        gui.backend.remove_video(gui.model.data(gui.model.index(row, 0), gui.model.JobIdRole))
    await pump(gui, .05)


@contextmanager
def requests(core):
    """Observe the real session without replacing responses or changing options."""
    core.initialize_session()
    original = core.session.request
    entries = []

    async def observe(method, url, **options):
        record = {"method": method, "path": urlsplit(str(url)).path, "at": time.monotonic()}
        entries.append(record)
        try:
            response = await original(method, url, **options)
            record.update(status=response.status_code, bytes=len(response.content) if not options.get("stream") else None)
            return response
        finally:
            record["finished"] = time.monotonic()

    core.session.request = observe
    try:
        yield entries
    finally:
        core.session.request = original


async def network(gui, lab):
    from src.backend.sni_fragment_proxy_lite import FragmentingProxyConfig, FragmentingProxyProcess
    core = gui.clients.ph_client.core
    user_agents = []
    for value in ("safari", "chrome"):
        await change(gui, "impersonation", value)
        reply = await core.request(lab.url + "/agent")
        user_agents.append(reply.json()["headers"].get("user-agent", ""))
    require(user_agents[0] != user_agents[1] and all(user_agents), "Impersonation did not change wire headers")
    for value in ("de-DE", "fr-FR"):
        await change(gui, "locale", value)
        reply = await core.request(lab.url + "/locale")
        headers = reply.json()["headers"]
        require(headers["accept-language"].startswith(value), "Content locale did not change wire language")
        require("lang=" + value.split("-")[0] in headers.get("cookie", ""), "Language cookies were not sent")
    await change(gui, "interface", "127.0.0.1")
    require((await core.request(lab.url + "/bound")).status_code == 200, "Valid interface binding failed")
    await change(gui, "interface", "pf-invalid-if")
    try:
        await core.request(lab.url + "/unreachable")
    except Exception:
        pass
    else:
        raise AssertionError("Invalid interface was silently ignored")
    await change(gui, "interface", "")
    before = len(lab.requests)
    await change(gui, "proxy", "http://127.0.0.1:9")
    try:
        await core.request(lab.url + "/blocked-proxy")
    except Exception:
        pass
    else:
        raise AssertionError("Invalid proxy was silently bypassed")
    require(len(lab.requests) == before, "Proxy failure fell back to a direct connection")
    await change(gui, "proxy", "")
    with patch.dict(os.environ, {key: value for key, value in {
        "HTTP_PROXY": "http://127.0.0.1:9", "http_proxy": "http://127.0.0.1:9",
        "HTTPS_PROXY": "http://127.0.0.1:9", "https_proxy": "http://127.0.0.1:9",
        "ALL_PROXY": "", "all_proxy": "", "NO_PROXY": "", "no_proxy": ""}.items()}):
        await change(gui, "trust_environment", True)
        try:
            await core.request(lab.url + "/environment")
        except Exception:
            pass
        else:
            raise AssertionError("Trust Environment ignored the configured proxy")
        await change(gui, "trust_environment", False)
        require((await core.request(lab.url + "/environment")).status_code == 200, "Disabled environment proxy still affected requests")
    proxy = FragmentingProxyProcess(FragmentingProxyConfig(listen_host="127.0.0.1", listen_port=0))
    try:
        proxy_url = await asyncio.to_thread(proxy.start)
        await change(gui, "proxy", proxy_url)
        require((await core.request(lab.url + "/real-proxy")).status_code == 200, "Real native proxy forwarding failed")
    finally:
        await change(gui, "proxy", "")
        await asyncio.to_thread(proxy.stop)
    return {"wire_user_agents_changed": True, "locale_headers_and_cookies": True,
            "interface_and_proxy_failure_verified": True, "environment_proxy_verified": True}


async def timeout_and_delay(gui, lab):
    core = gui.clients.ph_client.core
    await change(gui, "timeout", 1)
    started = time.monotonic()
    try:
        await core.request(lab.url + "/slow?seconds=1.3")
    except Exception:
        require(.7 <= time.monotonic() - started < 2.2, "Configured timeout was not respected")
    else:
        raise AssertionError("One-second timeout did not interrupt the slow response")
    await change(gui, "timeout", 2)
    require((await core.request(lab.url + "/slow?seconds=1.3")).status_code == 200, "Longer timeout did not allow the same response")
    await change(gui, "network_delay", 1)
    started = time.monotonic()
    await core.request(lab.url + "/delay-one")
    await core.request(lab.url + "/delay-two")
    require(time.monotonic() - started >= 1, "Network delay had no timing effect")
    await change(gui, "network_delay", 0)
    return {"timeout_changes_observed": True, "request_delay_seconds": 1}


async def retry(gui, lab):
    core = gui.clients.ph_client.core
    await change(gui, "network_delay", 0)
    await change(gui, "request_initial_retry_delay", .1)
    await change(gui, "request_retry_multiplier", 3.0)
    await change(gui, "request_retry_max_delay", .5)
    await change(gui, "request_retry_jitter", 0.0)
    await change(gui, "retries", 4)
    target = "/retry?fail=3&test=backoff"
    require((await core.request(lab.url + target)).status_code == 200, "Native retries did not recover")
    entries = [r for r in lab.requests if r["target"] == target]
    require(len(entries) == 4, "Retry count did not match the setting")
    gaps = [b["at"] - a["at"] for a, b in zip(entries, entries[1:])]
    require(gaps[0] >= .08 and gaps[1] >= .27 and .43 <= gaps[2] < .75, "Native exponential/capped delays were not applied")
    await change(gui, "request_retry_max_delay", 1.0)
    await change(gui, "request_initial_retry_delay", 0.0)
    await change(gui, "request_retry_jitter", .3)
    with patch("random.uniform", wraps=__import__("random").uniform) as random_wait:
        await core.request(lab.url + "/retry?fail=1&test=jitter")
        require(random_wait.called, "The native retryer did not sample jitter")
    await change(gui, "retries", 1)
    target = "/retry?fail=10&test=single"
    try:
        await core.request(lab.url + target)
    except Exception:
        pass
    else:
        raise AssertionError("A terminal retry failure was hidden")
    require(lab.counts[target] == 1, "One-attempt setting still retried")
    return {"attempts": len(entries), "observed_backoff_seconds": gaps, "native_jitter_sampled": True}


async def cache(gui, lab):
    core = gui.clients.ph_client.core
    await change(gui, "response_cache_size", 1)
    await change(gui, "response_cache_ttl", 1)
    target = "/cache-enabled"
    first = await core.fetch_text(lab.url + target)
    require(await core.fetch_text(lab.url + target) == first and lab.counts[target] == 1, "Response cache did not reuse a real response")
    await asyncio.sleep(1.1)
    await core.fetch_text(lab.url + target)
    require(lab.counts[target] == 2, "Response cache TTL did not expire")
    await change(gui, "response_cache_size", 0)
    await core.fetch_text(lab.url + target)
    await core.fetch_text(lab.url + target)
    require(lab.counts[target] == 4, "Disabled response cache still hid requests")
    job, video = await prepare(gui, filename="cache-metadata.mp4")
    source = video.source_video
    await change(gui, "segment_cache_size", 1)
    await change(gui, "segment_cache_ttl", 1)
    with requests(core) as observed:
        first = await core.get_segments(source.m3u8_base_url, "240")
        count = len(observed)
        require(first and await core.get_segments(source.m3u8_base_url, "240") == first and len(observed) == count,
                "Segment URL cache did not reuse the real playlist")
        await asyncio.sleep(1.1)
        await core.get_segments(source.m3u8_base_url, "240")
        require(len(observed) > count, "Segment URL cache TTL did not cause another playlist request")
    await change(gui, "segment_cache_size", 0)
    with requests(core) as observed:
        await core.get_segments(source.m3u8_base_url, "240")
        count = len(observed)
        await core.get_segments(source.m3u8_base_url, "240")
        require(len(observed) > count, "Disabled segment URL cache still hid playlist requests")
    await clear(gui)
    return {"response_cache_hit_expiry_disable": True, "real_playlist_cache_hit_expiry_disable": True}


async def speed(gui, lab):
    core = gui.clients.ph_client.core
    times = []
    size = 2 * 1024 * 1024
    for limit in (.5, 1.0):
        await change(gui, "speed_limit", limit)
        started = time.monotonic()
        result = await core.fetch_bytes(lab.url + f"/blob?bytes={size}&limit={limit}")
        elapsed = time.monotonic() - started
        require(len(result) == size and elapsed >= size / (limit * 1024 * 1024) * .65,
                "Native curl bandwidth limit had no measurable effect")
        times.append(elapsed)
    require(times[0] > times[1] * 1.25, "Changing bandwidth did not change actual transfer timing")
    return {"body_bytes": size, "elapsed_seconds": times}


async def tls(gui, lab):
    from src.backend.sni_fragment_proxy_lite import FragmentingProxyConfig, FragmentingProxyProcess
    core = gui.clients.ph_client.core
    proxy = FragmentingProxyProcess(FragmentingProxyConfig(listen_host="127.0.0.1", listen_port=0))
    try:
        proxy_url = await asyncio.to_thread(proxy.start)
        await change(gui, "proxy", proxy_url)
        await change(gui, "proxy_ssl_verification", True)
        try:
            await core.request(lab.tls_url + "/untrusted")
        except Exception:
            pass
        else:
            raise AssertionError("SSL verification accepted the lab's untrusted certificate")
        await change(gui, "proxy_ssl_verification", False)
        require((await core.request(lab.tls_url + "/untrusted")).status_code == 200,
                "Disabling verification did not permit the isolated test certificate")
        fingerprints = []
        for name in ("safari", "chrome"):
            await change(gui, "impersonation", name)
            await core.request(lab.tls_url + "/fingerprint")
            fingerprints.append(lab.hellos[-1])
        require(fingerprints[0] != fingerprints[1], "Browser impersonation did not change the real ClientHello")
        custom = "771,4865-4866-4867-49195-49199,0-10-11-13-16-23-43-45-51-65281,29-23-24,0"
        await change(gui, "custom_ja3", custom)
        await core.request(lab.tls_url + "/custom-ja3")
        require(lab.hellos[-1].get("ciphers") == [4865, 4866, 4867, 49195, 49199],
                "Custom JA3 did not change ciphers on the wire")
        await change(gui, "custom_ja3", "")
        offers = []
        for enabled in (False, True):
            await change(gui, "encrypted_ch", enabled)
            await core.request(lab.tls_url + "/ech")
            offers.append(65037 in lab.hellos[-1].get("extensions", []))
        require(offers == [False, True], "ECH toggle did not change the ClientHello offer")
        return {"self_signed_verification_toggle": True, "real_tls_fingerprints_differ": True,
                "custom_ja3_cipher_offer": True, "ech_offers": offers,
                "limitation": "Client offer verified; successful ECH negotiation requires an ECH-capable server"}
    finally:
        await change(gui, "proxy", "")
        await change(gui, "encrypted_ch", False)
        await change(gui, "custom_ja3", "")
        await asyncio.to_thread(proxy.stop)


async def dns_and_protocol(gui, lab):
    from curl_cffi.const import CurlHttpVersion
    core = gui.clients.ph_client.core
    url = next(url for name, _, url in lifecycle_fixtures() if name == "pornhub")
    versions = []
    for version in ("v1", "v2"):
        await change(gui, "http_version", version)
        response = await core.request(url)
        require(response.status_code == 200, "Real provider metadata request failed")
        versions.append(response.http_version)
    require(versions[0] in {CurlHttpVersion.V1_0, CurlHttpVersion.V1_1}
            and versions[1] == CurlHttpVersion.V2_0, "HTTP version did not affect real negotiated protocol")
    await change(gui, "dns_over_https", True)
    for resolver in ("https://cloudflare-dns.com/dns-query", "https://dns.quad9.net/dns-query"):
        await change(gui, "dns_server", resolver)
        response = await core.request(url)
        require(response.status_code == 200, "Configured DNS resolver could not load real metadata")
    # A closed loopback endpoint is a genuine resolver outage, not a fake HTTP response.
    await change(gui, "dns_server", "https://127.0.0.1:9/dns-query")
    await change(gui, "fallback_dns", "https://cloudflare-dns.com/dns-query")
    response = await core.request(url)
    require(response.status_code == 200 and core._dns_fallback_core is not None,
            "A real failed primary resolver did not use the configured fallback")
    await change(gui, "dns_over_https", False)
    require((await core.request(url)).status_code == 200 and core.configuration.dns_over_https is None,
            "Disabling DoH did not restore normal resolution")
    return {"negotiated_http_versions": [int(v) for v in versions], "two_live_resolvers": True,
            "real_primary_outage_fallback": True, "doh_disabled_resolution": True}


async def probe(path, ffmpeg):
    process = await asyncio.create_subprocess_exec(str(ffmpeg), "-hide_banner", "-nostdin", "-i", str(path),
                                                   stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    _, stderr = await process.communicate()
    text = stderr.decode(errors="replace")
    dimensions = re.search(r"Video:.*?\b(\d{2,5})x(\d{2,5})\b", text)
    assert dimensions is not None, "FFmpeg could not read the actual video dimensions"
    return text, min(int(dimensions[1]), int(dimensions[2]))


async def media(gui, lab):
    from src.shared.ffmpeg import find_ffmpeg
    core = gui.clients.ph_client.core
    ffmpeg = find_ffmpeg()
    require(ffmpeg is not None, "FFmpeg is required for settings media checks")
    timings = []
    worker_peaks = []
    outputs = []
    old_segment = core.download_segment
    active = 0
    peak = 0

    async def segment(*args, **kwargs):
        nonlocal active, peak
        active += 1
        peak = max(peak, active)
        try:
            return await old_segment(*args, **kwargs)
        finally:
            active -= 1

    core.download_segment = segment
    try:
        for index, quality, metadata, workers, delay in ((0, 11, False, 1, 0), (1, 8, True, 2, 1)):
            for prop, value in {"quality": quality, "write_metadata": metadata, "download_workers": workers,
                                "processing_delay": delay,
                                "output_path": str(gui.directory / f"media-{index}")}.items():
                await change(gui, prop, value)
            peak = 0
            started = time.monotonic()
            with requests(core) as observed:
                job, video = await prepare(gui, filename="settings.mp4")
                require(observed and observed[0]["at"] - started >= delay * .9,
                        "Processing delay was not applied before real metadata requests")
            require(video.selected_quality == str(gui.settings.mappings_quality[quality]),
                    "Default quality did not reach the prepared row")
            calls = []
            original_download = type(video.source_video).download

            async def download(source, configuration):
                calls.append(time.monotonic())
                return await original_download(source, configuration)

            started = time.monotonic()
            with patch.object(type(video.source_video), "download", download):
                await transfer(gui, job)
            require(video.status == "completed" and calls and calls[0] - started >= delay * .9,
                    "Download processing delay did not affect the real native start")
            require(video.output_path.parent == Path(gui.settings.output_path) and video.output_path.is_file(),
                    "Output path did not affect the actual file destination")
            text, actual_quality = await probe(video.output_path, ffmpeg)
            require(actual_quality == int(video.selected_quality), "Selected quality did not change the encoded resolution")
            tag = re.search(r"(?im)^\s*title\s*:\s*(.*)$", text)
            require((tag is not None and tag[1].strip() == video.title) if metadata else tag is None,
                    "Write metadata did not affect the output's real title tag")
            require(peak == workers, "Download workers did not change native segment concurrency")
            worker_peaks.append(peak)
            timings.append(round(calls[0] - started, 3))
            outputs.append(await validate_media(video.output_path, ffmpeg, video.length))
        await change(gui, "processing_delay", 0)
        await change(gui, "skip_existing_files", True)
        target = video.output_path
        stamp = target.stat().st_mtime_ns
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        job, skipped = await prepare(gui, filename="settings.mp4")
        with requests(core) as observed:
            await transfer(gui, job)
            require(not observed, "Skip existing files made media requests")
        require(target.stat().st_mtime_ns == stamp and hashlib.sha256(target.read_bytes()).hexdigest() == digest,
                "Skip existing files modified a completed output")
        await change(gui, "skip_existing_files", False)
        job, replaced = await prepare(gui, filename="settings.mp4")
        with requests(core) as observed:
            await transfer(gui, job)
            require(any(".ts" in entry["path"] for entry in observed), "Disabling skip did not fetch real media again")
        require(replaced.status == "completed" and target.stat().st_mtime_ns != stamp,
                "Disabling skip did not replace the output")
        return {"outputs": outputs, "worker_peaks": worker_peaks, "native_start_delays": timings,
                "encoded_quality_and_metadata_verified": True, "skip_and_replace_verified": True}
    finally:
        core.download_segment = old_segment


async def parallel(gui, lab):
    from src.tests.smoke.download_queue import NativeDownloads
    peaks = []
    # Keep each real transfer bounded: stop at genuine partial progress.
    for limit in (1, 2):
        await change(gui, "parallel_downloads", limit)
        videos = {}
        for provider in ("pornhub", "eporner"):
            job, video = await prepare(gui, provider, f"parallel-{limit}-{provider}.mp4")
            videos[job] = video
            control(gui, "downloadSelectCheck", job).setProperty("checked", True)
            control(gui, "downloadSelectCheck", job).toggled.emit()
        control(gui, "cleanupStopCheck").setProperty("checked", True)
        observer = NativeDownloads(videos, limit, gui.errors)
        stopped = set()

        def interrupt(*_):
            for row in range(gui.model.rowCount()):
                index = gui.model.index(row, 0)
                job = gui.model.data(index, gui.model.JobIdRole)
                progress = gui.model.data(index, gui.model.ProgressRole)
                if (job in videos and job not in stopped and gui.model.get_status(job) == "downloading"
                        and 1 <= progress < 95):
                    stopped.add(job)
                    click(gui, "downloadStopResumeButton", job)

        gui.model.dataChanged.connect(interrupt)
        try:
            with observer:
                click(gui, "downloadSelectedButton")
                await wait(gui, lambda: not gui.backend._download_tasks)
                require(stopped == set(videos) and not gui.errors, "Parallel setting test missed a real partial transfer")
                require(observer.peak == limit, "Changing the parallel setting did not change active native concurrency")
                require(all(video.status == "cancelled" for video in videos.values()), "Partial transfers did not stop")
                peaks.append(observer.peak)
        finally:
            gui.model.dataChanged.disconnect(interrupt)
        await clear(gui)
    return {"native_peaks_after_settings_changes": peaks}


async def profiles(gui, lab):
    from base_api import BaseMedia, Helper, make_iterator_config

    from src.backend import application
    from src.cli.selftest.cases import PROFILE_TESTS
    from src.shared.media import VideoFilters
    url = next(url for name, url in PROFILE_TESTS if name == "PornHub Model")
    modes = []
    original_stream = application.container_stream

    def stream(*args, **options):
        modes.append(options.get("profile_mode"))
        return original_stream(*args, **options)

    active = {"pages": 0, "items": 0}
    peaks = {"pages": 0, "items": 0}

    def observe_worker(original, kind):
        async def observed(helper, *params, **options):
            active[kind] += 1
            peaks[kind] = max(peaks[kind], active[kind])
            try:
                return await original(helper, *params, **options)
            finally:
                active[kind] -= 1
        return observed

    rows = []
    with (patch.object(application, "container_stream", stream),
          patch.object(Helper, "_process_page", observe_worker(Helper._process_page, "pages")),
          patch.object(Helper, "_process_item", observe_worker(Helper._process_item, "items"))):
        for maximum, mode in ((1, 1), (2, 2)):
            for prop, value in {"result_limit": maximum, "model_videos": mode,
                                "pages_concurrency": maximum, "videos_concurrency": maximum}.items():
                await change(gui, prop, value)
            peaks.update(pages=0, items=0)
            await gui.backend._process_model_url(url, "profile-$index", VideoFilters(), pages=2,
                                                  iterator_config=make_iterator_config(load_specific_sources=("html",)))
            require(gui.model.rowCount() == maximum and not gui.errors, "Result limit did not bound real profile rows")
            require(all(gui.model.get_video(gui.model.data(gui.model.index(i, 0), gui.model.JobIdRole)).source_video is not None
                        for i in range(gui.model.rowCount())), "Profile rows lost native videos")
            require(peaks["pages"] == maximum and peaks["items"] == maximum,
                    "Native scraper exceeded changed page/item concurrency")
            rows.append({"limit": maximum, "rows": gui.model.rowCount(), "native_request_peaks": dict(peaks)})
            await clear(gui)
    require(modes == ["uploads", "videos"], "Model Videos did not select the requested native feed")
    # Verify strict mode through the real loader: no API-backed sources may load.
    from src.cli.selftest.cases import SINGLE_VIDEO_TESTS
    eporner = next(url for name, url in SINGLE_VIDEO_TESTS if name == "Eporner")
    sources = []
    original_load = BaseMedia.load_sources

    async def load(media, *names, **options):
        if type(media).__module__.startswith("eporner_api"):
            sources.extend(names)
        return await original_load(media, *names, **options)

    for strict in (False, True):
        await change(gui, "strict_enforcement", strict)
        sources.clear()
        with patch.object(BaseMedia, "load_sources", load):
            native = await gui.clients.get_video(eporner)
            require(native is not None, "Strict-language loader returned no real video")
        require(("api" not in sources) if strict else ("api" in sources), "Strict enforcement did not change native metadata sources")
    return {"profiles": rows, "feed_modes": modes, "strict_mode_changes_api_loading": True}


async def errors(gui, lab):
    from src.shared import error_reporting
    broken = gui.directory / "not-a-directory"
    broken.write_text("A real file blocks creation of the output directory.")
    await change(gui, "output_path", str(broken))
    deliveries = []
    with patch.object(error_reporting, "ERROR_REPORT_URL", lab.url + "/report"):
        for suppress, reporting in ((False, False), (True, True)):
            await change(gui, "supress_errors", suppress)
            await change(gui, "enable_logging", reporting)
            gui.errors.clear()
            before = sum(r["target"] == "/report" for r in lab.requests)
            job, video = await prepare(gui, filename="blocked.mp4")
            await transfer(gui, job)
            require(video.status == "failed", "A real filesystem failure was hidden")
            require(bool(gui.errors) == (not suppress), "Ignore Errors did not control the actual GUI message")
            received = [r for r in lab.requests if r["target"] == "/report"][before:]
            require(len(received) == int(reporting), "Error-report consent did not control real HTTP delivery")
            if received:
                require(video.url not in received[0]["body"] and video.title not in received[0]["body"],
                        "Error report leaked real media metadata")
            deliveries.append(len(received))
            gui.errors.clear()
            await clear(gui)
    await change(gui, "enable_logging", False)
    return {"real_filesystem_fault": True, "messages_suppressed": True, "local_http_report_deliveries": deliveries,
            "production_telemetry_contacted": False}


async def logging_effect(gui, lab):
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    logger = logging.getLogger("base_api.base")
    logger.addHandler(handler)
    disabled = logging.root.manager.disable
    logging.disable(logging.NOTSET)
    try:
        await change(gui, "debug_mode", False)
        await change(gui, "log_level", 3)
        gui.backend.logger.addHandler(handler)
        gui.backend.logger.info("settings-hidden-info")
        gui.backend.logger.error("settings-visible-error")
        gui.clients.ph_client.core.logger.info("settings-hidden-core-info")
        require("settings-hidden-info" not in stream.getvalue() and "settings-hidden-core-info" not in stream.getvalue()
                and "settings-visible-error" in stream.getvalue(), "Log Level did not filter actual records")
        await change(gui, "debug_mode", True)
        gui.clients.ph_client.core.logger.debug("settings-native-debug")
        require("settings-native-debug" in stream.getvalue(), "Debug Mode did not enable native debug output")
        require(any(gui.directory.glob("BaseCore*.log")), "Debug Mode did not create its native log files")
        await change(gui, "debug_mode", False)
        return {"actual_log_filtering": True, "native_debug_record_and_files": True}
    finally:
        gui.backend.logger.removeHandler(handler)
        logger.removeHandler(handler)
        handler.close()
        logging.disable(disabled)


async def ui(gui, lab):
    from PySide6.QtGui import QGuiApplication

    from src.backend.account_diagnostics import visual_items
    job, video = await prepare(gui, filename="ui-metadata.mp4")
    for hidden in (True, False):
        await change(gui, "anonymous_mode", hidden)
        labels = [item.property("text") for item in visual_items(control(gui, "downloadRow", job))]
        require((video.title not in " ".join(str(v) for v in labels) and video.author not in labels)
                if hidden else (any(str(v).endswith(video.title) for v in labels) and video.author in labels),
                "Anonymous Mode did not change rendered sensitive text")
    await change(gui, "font_size", 16)
    require(QGuiApplication.font().pointSize() == 16 and gui.window.property("font").pointSize() == 16,
            "Font size did not reach the live application/window")
    backgrounds = []
    for dark in (False, True):
        await change(gui, "dark_mode", dark)
        require(gui.theme.themeMode == ("Dark" if dark else "Light"), "Dark mode did not change the active theme")
        backgrounds.append(gui.window.property("appliedBackground").name())
    require(backgrounds[0] != backgrounds[1], "Dark mode did not change actual rendered Material colors")
    await change(gui, "accent_color", "#f44336")
    accent = gui.window.property("appliedAccent")
    require(accent.name() == "#f44336", "Accent color did not reach the rendered Material style")
    edge = gui.window.findChild(QObject, "settingsActivity")
    for enabled in (False, True):
        await change(gui, "activity_glow_enabled", enabled)
        await pump(gui, .4)
        require(edge.property("enabled") == enabled and edge.property("visible") == enabled,
                "Activity glow did not change actual visibility")
    await clear(gui)
    return {"rendered_privacy_masking": True, "global_font_and_color_scheme": True,
            "material_accent": True, "activity_visibility": True}


async def translation(gui, lab):
    from src.backend.account_diagnostics import visual_items
    rendered = []
    for index, expected in ((2, "Video-URL:"), (4, "URL de la vidéo :"), (3, "视频网址："), (1, "Video URL:")):
        await change(gui, "language", index)
        texts = [item.property("text") for item in visual_items(gui.window.contentItem())]
        require(expected in texts, "GUI language did not retranslate a production label")
        rendered.append(expected)
    return {"live_production_labels": rendered,
            "limitation": "Untranslated catalog entries retain their English fallback"}


async def style(gui, lab):
    styles = []
    for value in ("Fusion", "Material"):
        await change(gui, "core_style", value)
        code = '''
import sys,json
from PySide6.QtCore import QSettings,QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtQml import QQmlEngine,QQmlComponent
settings=QSettings(sys.argv[1],QSettings.Format.IniFormat)
saved=settings.value('UI/core_style')
QQuickStyle.setStyle(saved)
app=QGuiApplication([])
engine=QQmlEngine()
component=QQmlComponent(engine)
component.setData(b'import QtQuick.Controls; Button { text: "Style probe" }',QUrl())
item=component.create()
assert item is not None, str(component.errors())
print(json.dumps({'saved':saved,'active':QQuickStyle.name()}))
'''
        process = await asyncio.create_subprocess_exec(sys.executable, "-c", code, str(gui.path),
                                                       stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
        require(process.returncode == 0, f"Restarted style probe failed: {stderr.decode()[:200]}")
        result = json.loads(stdout)
        require(result == {"saved": value, "active": value}, "Saved style did not apply in a fresh Qt process")
        styles.append(result)
    return {"real_restart_styles": styles}


async def updates(gui, lab):
    from PySide6.QtCore import QUrl
    from PySide6.QtQml import QQmlComponent

    from src.backend.account_diagnostics import UI
    source = (UI / "Main.qml").read_text()
    function = re.search(r"function continueStartup\(\)\s*\{.*?\n    \}", source, re.S)
    assert function is not None, "Startup update gate disappeared from the production page"
    scheduled = []
    for enabled in (False, True):
        await change(gui, "update_checks", enabled)
        gui.backend._update_check_requested = False
        gui.backend._update_check_task = None
        component = QQmlComponent(gui.engine)
        component.setData(('import QtQml; QtObject { property bool startupContinued: false; '
                           + function[0] + ' }').encode(), QUrl())
        obj = component.create()
        require(obj is not None, "Production startup gate did not load")
        QMetaObject.invokeMethod(obj, "continueStartup")
        task = gui.backend._update_check_task
        require((task is not None) == enabled, "Update Checks did not control actual update-task scheduling")
        scheduled.append(task is not None)
        if task is not None:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
        obj.deleteLater()
        await asyncio.sleep(0)
    return {"native_update_tasks_scheduled": scheduled,
            "scope": "Startup scheduling gate; no production update/install action is performed"}


async def database(gui, lab):
    from src.database.bridge import DatabaseBridge
    from src.database.installer import download_and_extract_pocketbase
    from src.database.service import PocketBaseService
    try:
        binary = PocketBaseService(gui.directory / "probe").find_binary()
    except Exception:
        binary = await asyncio.to_thread(download_and_extract_pocketbase, target_dir=gui.directory / "pb-bin")
    job, video = await prepare(gui, filename="database-metadata.mp4")
    directories = []
    for label in ("tracking-a", "tracking-b"):
        directory = gui.directory / label
        await change(gui, "pocketbase_data_path", str(directory))
        await change(gui, "track_videos", True)
        # Reconstruct the actual startup consumer after restart-required changes.
        # Only executable discovery is redirected; enabled/path must come from settings.
        with patch.dict(os.environ, {"PORN_FETCH_POCKETBASE_BINARY": str(binary)}):
            bridge = DatabaseBridge()
            tracker = bridge.tracker
            try:
                require(tracker.enabled and tracker.data_path == directory,
                        "The real database startup consumer ignored the saved settings")
                await tracker.start()
                bridge.on_video_updated(video)
                await wait(gui, lambda: not bridge.busy)
                require(tracker.get_dashboard_stats()["total"] >= 1, "Enabled tracking did not save real video metadata")
                require(any(directory.rglob("*.db")), "Selected PocketBase folder contains no real database")
            finally:
                await bridge.close()
        directories.append(label)
    await change(gui, "track_videos", False)
    disabled = DatabaseBridge()
    try:
        require(not disabled.tracker.enabled, "Disabled tracking still enabled the real database consumer")
        disabled.on_video_updated(video)
        require(not disabled.busy and disabled.tracker._service is None, "Disabled tracking still started a service")
    finally:
        await disabled.close()
    await clear(gui)
    return {"real_pocketbase_directories": directories, "enabled_saves_and_disabled_no_service": True}


async def sni(gui, lab, *, strict=False):
    from src.backend.sni_fragment_proxy_strict import StrictFragmentingProxyProcess
    from src.backend.sni_proxy_manager import SNIProxyManager
    core = gui.clients.ph_client.core
    url = next(url for name, _, url in lifecycle_fixtures() if name == "pornhub")
    manager = SNIProxyManager(gui.settings)
    profiles = ["Strict Fragmentation", "Strict Reverse", "Strict Desync"] if strict else ["Lite"]
    routes = []
    try:
        await change(gui, "sni_obfuscation", True)
        for profile in profiles:
            if strict:
                await change(gui, "sni_obfuscation_strict_profile", profile)
            else:
                await change(gui, "sni_obfuscation_lite", True)
            proxy = await asyncio.to_thread(manager.start)
            require(proxy and manager.is_running, f"SNI proxy failed: {manager.last_error}")
            if strict:
                require(isinstance(manager._process, StrictFragmentingProxyProcess),
                        "Strict mode fell back to Lite; packet-level effect remains unverified")
            gui.clients.refresh_clients()
            response = await core.request(url)
            require(response.status_code == 200 and core.configuration.proxy == proxy,
                    "SNI selection did not route real metadata through its active helper")
            routes.append(profile)
            await asyncio.to_thread(manager.stop)
            gui.clients.refresh_clients()
        return {"real_helper_routes": routes, "scope": "Native helper routing; not a claim of wire-level hostname secrecy"}
    finally:
        await asyncio.to_thread(manager.stop)
        await change(gui, "sni_obfuscation", False)
        gui.clients.refresh_clients()


async def tor(gui, lab):
    from src.shared.service_transport import ServiceCore
    from src.shared.tor_runtime import runtime
    core = gui.clients.ph_client.core
    previous_directory = runtime.directory
    runtime.directory = gui.directory / "tor-client"
    try:
        await change(gui, "service_transport", "tor")
        # A real read-only app-service request exercises the onion route.
        async with ServiceCore(gui.settings) as service:
            response = await service.request("https://api.pornfetch.to/", method="HEAD")
            require(200 <= response.status_code < 500, "Real Tor service route did not respond")
        require(core.configuration.proxy is None, "Services-only Tor changed provider routing")
        await change(gui, "service_transport", "tor_all")
        response = await core.request("https://check.torproject.org/api/ip")
        require(response.status_code == 200 and response.json().get("IsTor") is True,
                "All-traffic setting did not produce a real Tor-routed provider-core request")
        return {"actual_onion_service_request": True, "provider_core_is_tor": True,
                "media_downloaded_through_tor": False}
    finally:
        await change(gui, "service_transport", "direct")
        await asyncio.to_thread(runtime.stop)
        runtime.directory = previous_directory


async def run_effects(gui, args, report, save, log):
    from src.backend.account_diagnostics import AccountAccessGuard, extend_timeout_for_wait
    from src.tests.smoke.settings_network import NetworkLab
    lab = await NetworkLab(gui.directory).start()
    active_timeout = None
    access = AccountAccessGuard(on_wait=lambda seconds: extend_timeout_for_wait(active_timeout, seconds))
    specs = [
        ("wire-network", ("impersonation", "locale", "interface", "proxy", "trust_environment"), network),
        ("timeout-delay", ("timeout", "network_delay"), timeout_and_delay),
        ("native-retry", ("retries", "request_initial_retry_delay", "request_retry_max_delay", "request_retry_multiplier", "request_retry_jitter"), retry),
        ("response-playlist-cache", ("response_cache_size", "response_cache_ttl", "segment_cache_size", "segment_cache_ttl"), cache),
        ("bandwidth", ("speed_limit",), speed),
        ("wire-tls", ("custom_ja3", "proxy_ssl_verification", "encrypted_ch"), tls),
        ("live-dns-protocol", ("dns_server", "fallback_dns", "dns_over_https", "http_version"), dns_and_protocol),
        ("real-media", ("quality", "output_path", "write_metadata", "skip_existing_files", "processing_delay", "download_workers"), media),
        ("live-parallel", ("parallel_downloads",), parallel),
        ("real-profiles", ("model_videos", "result_limit", "strict_enforcement", "pages_concurrency", "videos_concurrency"), profiles),
        ("error-controls", ("supress_errors", "enable_logging"), errors),
        ("actual-log-output", ("debug_mode", "log_level"), logging_effect),
        ("rendered-ui", ("anonymous_mode", "font_size", "dark_mode", "accent_color", "activity_glow_enabled"), ui),
        ("live-translation", ("language",), translation),
        ("restart-style", ("core_style",), style),
        ("startup-update-gate", ("update_checks",), updates),
        ("real-pocketbase", ("track_videos", "pocketbase_data_path"), database),
        ("lite-sni-route", ("sni_obfuscation", "sni_obfuscation_lite"), sni),
        ("strict-sni-routes", ("sni_obfuscation_strict", "sni_obfuscation_strict_profile"), None),
        ("real-tor-routes", ("service_transport",), tor if args.tor else None),
    ]
    covered = {prop for _, props, _ in specs for prop in props}
    require(covered == set(CASE_BY_PROPERTY), f"Missing effect inventory: {set(CASE_BY_PROPERTY) - covered}")
    try:
        with access:
            for name, props, operation in specs:
                if args.effect and name not in args.effect:
                    continue
                print(f"EFFECT {name}", flush=True)
                result = {"effect": name, "settings": list(props), "status": "UNVERIFIED"}
                started = time.monotonic()
                try:
                    if name == "strict-sni-routes" and args.strict:
                        async def strict_operation(window, network_lab):
                            return await sni(window, network_lab, strict=True)
                        operation = strict_operation
                    if operation is None:
                        result["reason"] = "Requires --strict and native elevation" if name.startswith("strict") else "Requires --tor (real Tor bootstrap)"
                    else:
                        with redirect_stdout(log), redirect_stderr(log):
                            active_timeout = asyncio.timeout(args.timeout)
                            async with active_timeout:
                                await baseline(gui)
                                result["evidence"] = await operation(gui, lab)
                        result["status"] = "PASS"
                except asyncio.CancelledError:
                    if access.blocked:
                        result.update(status="BLOCKED", access_control=access.blocked)
                        report["blocked"] = access.blocked
                    else:
                        result["status"] = "INTERRUPTED"
                        report["interrupted"] = True
                    raise
                except Exception as error:
                    import traceback
                    traceback.print_exc(file=log)
                    result.update(status="FAIL", error_type=type(error).__name__, error=str(error))
                finally:
                    active_timeout = None
                    result["elapsed_seconds"] = round(time.monotonic() - started, 3)
                    report["effects"].append(result)
                    for row in report["settings"]:
                        if row["setting"] in props:
                            row["effect"] = result["status"]
                            row["effect_group"] = name
                    save()
                    print(f"{result['status']} {name}" + (f": {result['error']}" if result.get('error') else ""), flush=True)
                if result["status"] == "FAIL":
                    with redirect_stdout(log), redirect_stderr(log):
                        gui.errors.clear()
                        await clear(gui)
                        await baseline(gui)
    finally:
        await lab.close()
        report["rate_limit_recovery"] = access.rate_limit_events
        save()


async def auxiliary_controls(gui):
    """Exercise alternate inputs and safe maintenance against isolated files only."""
    from PySide6.QtCore import QUrl

    from src.backend import application
    for name, prop, suffix in (("outputFolderDialog", "output_path", "chosen-output"),
                               ("pocketbaseFolderDialog", "pocketbase_data_path", "chosen-database")):
        selected = gui.directory / suffix
        selected.mkdir()
        dialog = gui.control(name)
        dialog.setProperty("currentFolder", QUrl.fromLocalFile(str(selected)))
        dialog.setProperty("selectedFolder", QUrl.fromLocalFile(str(selected)))
        dialog.accepted.emit()
        gui.settings.sync()
        require(getattr(gui.settings, prop) == str(selected), f"{name} did not apply its selected folder")
        gui.verify_disk(CASE_BY_PROPERTY[prop], str(selected))
    directory = Path(application.TEMP_DIRECTORY).resolve()
    require(directory.is_relative_to(gui.directory), "Refusing to clear temporary files outside this diagnostic workspace")
    for target in (Path(application.TEMP_DIRECTORY_STATES), Path(application.TEMP_DIRECTORY_SEGMENTS)):
        target.mkdir(parents=True, exist_ok=True)
        (target / "settings-test-partial").write_bytes(b"owned diagnostic partial")
    notices = []
    with patch.object(application, "ui_popup", lambda message: notices.append(message)):
        gui.backend.clear_temporary_files()
        require(not list(directory.rglob("settings-test-partial")), "Clear temporary files did not remove owned partials")
        gui.control("resetSettingsButton").clicked.emit()
        parser = __import__("configparser").ConfigParser(interpolation=None)
        parser.read(gui.path)
        require(not parser.sections(), "Reset left settings on disk")
        gui.backend.load_clients()
        require(gui.clients.config.timeout == 10 and gui.settings.result_limit == 50,
                "Reset values did not apply when clients were reconstructed")
    require(len(notices) == 2, "Maintenance actions did not issue their real user notifications")
    return {"folder_dialogs": True, "temporary_file_cleanup": True, "reset_and_runtime_reconstruction": True,
            "installer_uninstaller": "Not invoked: these are installation actions, not saved settings"}
