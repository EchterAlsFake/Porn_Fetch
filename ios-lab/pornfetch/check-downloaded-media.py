"""Read-only container and full audio/video decode check on a simulator download."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct
import time

import av

root = Path('/Users/asuna/Library/Developer/CoreSimulator/Devices/7DFE048D-AB3D-453F-AE58-D474EF4C4569/data/Containers/Data/Application/A591F6D8-7E9C-45B8-A431-C761F367620A')
files = list(root.rglob('*.mp4'))
if not files:
    raise SystemExit('No MP4 downloads found')
path = max(files, key=lambda p: p.stat().st_mtime)
before = path.stat()
report = {'path': str(path), 'size_bytes': before.st_size, 'pyav_version': av.__version__,
          'ffmpeg_libraries': av.library_versions, 'streams': [], 'decode_errors': [],
          'corrupt_packets': 0, 'timestamp_regressions': {}, 'decoded_frames': {}}
started = time.monotonic()
digest = hashlib.sha256()
with path.open('rb') as file:
    while data := file.read(1024 * 1024):
        digest.update(data)
report['sha256'] = digest.hexdigest()

boxes = Counter()
position = 0
with path.open('rb') as file:
    while position + 8 <= before.st_size:
        file.seek(position)
        length, kind = struct.unpack('>I4s', file.read(8))
        header = 8
        if length == 1:
            length = struct.unpack('>Q', file.read(8))[0]
            header = 16
        if length == 0:
            length = before.st_size - position
        if length < header or position + length > before.st_size:
            break
        boxes[kind.decode('ascii', 'replace')] += 1
        position += length
report['container_boxes'] = dict(boxes)
report['container_box_lengths_valid'] = position == before.st_size

av.logging.set_level(av.logging.WARNING)
with av.logging.Capture(local=False) as logs:
    with av.open(str(path)) as container:
        report['format'] = container.format.name
        report['duration_seconds'] = container.duration / av.time_base if container.duration else None
        streams = [s for s in container.streams if s.type in ('video', 'audio')]
        for stream in streams:
            codec = stream.codec_context
            item = {'index': stream.index, 'type': stream.type, 'codec': codec.name,
                    'time_base': str(stream.time_base),
                    'duration_seconds': float(stream.duration * stream.time_base) if stream.duration else None}
            if stream.type == 'video':
                codec.thread_type = 'AUTO'
                codec.thread_count = 6
                item.update(width=codec.width, height=codec.height,
                            frame_rate=str(stream.average_rate), pixel_format=codec.format.name)
            else:
                item.update(sample_rate=codec.sample_rate, channels=codec.channels)
            codec.options = dict(codec.options, err_detect='explode')
            report['streams'].append(item)
        counts = Counter()
        last_times = {}
        ranges = {}
        regressions = Counter()
        for packet in container.demux(streams):
            if packet.is_corrupt:
                report['corrupt_packets'] += 1
            try:
                frames = packet.decode()
            except av.error.FFmpegError as error:
                report['decode_errors'].append(str(error))
                continue
            for frame in frames:
                key = f'{packet.stream.type}:{packet.stream.index}'
                counts[key] += 1
                if frame.time is not None:
                    timestamp = frame.time
                    if key in last_times and timestamp < last_times[key] - 0.000001:
                        regressions[key] += 1
                    last_times[key] = timestamp
                    duration = (frame.samples / frame.sample_rate if packet.stream.type == 'audio'
                                else float(frame.duration * frame.time_base) if frame.duration else 0)
                    if key not in ranges:
                        ranges[key] = {'first_seconds': timestamp, 'last_end_seconds': timestamp + duration}
                    else:
                        ranges[key]['last_end_seconds'] = max(ranges[key]['last_end_seconds'], timestamp + duration)
            if sum(counts.values()) and sum(counts.values()) % 10000 == 0:
                print('Decoded frames:', dict(counts), flush=True)
        report['decoded_frames'] = dict(counts)
        report['decoded_time_ranges'] = ranges
        report['timestamp_regressions'] = dict(regressions)
report['ffmpeg_log_count'] = len(logs)
report['ffmpeg_logs'] = logs[:100]
report['elapsed_seconds'] = round(time.monotonic() - started, 2)
after = path.stat()
report['file_unchanged_during_check'] = before.st_size == after.st_size and before.st_mtime_ns == after.st_mtime_ns
report['decode_integrity_passed'] = bool(report['decoded_frames']) and not report['decode_errors'] and not report['corrupt_packets'] and report['container_box_lengths_valid'] and report['file_unchanged_during_check']
out = Path('/Users/asuna/ios-lab/build/download-integrity.json')
out.write_text(json.dumps(report, indent=2) + '\n')
summary = {key: value for key, value in report.items() if key not in ('path', 'ffmpeg_libraries')}
print(json.dumps(summary, indent=2), flush=True)
