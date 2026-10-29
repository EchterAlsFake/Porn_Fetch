"""Explicit, one-shot on-device remux diagnostic; no media/network requests."""
import base64
import json
from pathlib import Path
import struct
import sys
import time
import traceback
import zlib


def run(working):
    job = working / "ios-remux-job.json"
    if not job.is_file():
        return
    running = job.with_suffix(".running")
    job.replace(running)
    report = {"platform": sys.platform, "passed": False}
    started = time.monotonic()
    try:
        import _ios_ffmpeg
        from base_api.modules.ffmpeg import find_ffmpeg, remux_ts_to_mp4, write_metadata_tags
        options = json.loads(running.read_text())
        source = (working / options["input"]).resolve()
        destination = (working / options["output"]).resolve()
        assert source.parent == working.resolve() and destination.parent == working.resolve()
        assert source != destination and source.is_file() and not destination.exists()
        before = source.stat()
        report.update(version=_ios_ffmpeg.version, license=_ios_ffmpeg.license,
                      library=str(find_ffmpeg()), input_bytes=before.st_size)
        with source.open("rb") as stream:
            header = stream.read(188 * 5)
        report["input_is_mpegts"] = all(header[i * 188] == 0x47 for i in range(5))
        report["apple_before"] = json.loads(_ios_ffmpeg.apple_probe(str(source)))
        assert remux_ts_to_mp4(source, destination, metadata={"title": source.stem})
        report["remux_seconds"] = round(time.monotonic() - started, 3)
        report["output_bytes"] = destination.stat().st_size
        report["apple_after"] = json.loads(_ios_ffmpeg.apple_probe(str(destination)))
        assert report["apple_after"]["playable"] and report["apple_after"]["duration_seconds"] > 0
        report["original_unchanged"] = before.st_size == source.stat().st_size and before.st_mtime_ns == source.stat().st_mtime_ns
        assert report["original_unchanged"]
        # Exercise atomic metadata rewrite and embedded PNG cover through the same adapter.
        def chunk(kind, data):
            return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
        png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 16, 16, 8, 2, 0, 0, 0))
               + chunk(b"IDAT", zlib.compress((b"\0" + b"\x33\x66\x99" * 16) * 16)) + chunk(b"IEND", b""))
        assert write_metadata_tags(destination, {"title": source.stem}, thumbnail=png)
        report["metadata_and_cover"] = True
        report["apple_final"] = json.loads(_ios_ffmpeg.apple_probe(str(destination)))
        assert report["apple_final"]["playable"]
        from src.backend.application import FORCE_DISABLE_AV
        report["application_remux_enabled"] = not FORCE_DISABLE_AV
        assert not FORCE_DISABLE_AV
        report["passed"] = True
    except BaseException:
        report["error"] = traceback.format_exc()
    report["elapsed_seconds"] = round(time.monotonic() - started, 3)
    result = working / "ios-remux-result.json"
    temporary = result.with_suffix(".tmp")
    temporary.write_text(json.dumps(report, indent=2))
    temporary.replace(result)
    running.rename(running.with_suffix(".done"))
    print("IOS_FFMPEG_CHECK", json.dumps(report), flush=True)
