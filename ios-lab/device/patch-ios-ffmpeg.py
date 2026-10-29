"""Apply the small platform adapter to staged base_api, retaining upstream logic."""
from pathlib import Path
import difflib

device = Path(__file__).resolve().parent
target = device / "vendor/base_api/modules/ffmpeg.py"
original = target.read_text()
if "from ios_ffmpeg import library_path" in original:
    raise SystemExit(0)
updated = original.replace(
    '    binary_name = "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"',
    '    if sys.platform == "ios":\n'
    '        from ios_ffmpeg import library_path\n'
    '        return library_path()\n'
    '    binary_name = "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"', 1)
needle = '    ffmpeg = find_ffmpeg(ffmpeg_bin, extra_roots=extra_roots)'
updated = updated.replace(needle,
    '    if sys.platform == "ios":\n'
    '        from ios_ffmpeg import remux_ts_to_mp4 as native_remux\n'
    '        return native_remux(input_path, output_path, metadata=metadata, thumbnail=thumbnail)\n'
    + needle, 1)
index = updated.index('def write_metadata_tags(')
updated = updated[:index] + updated[index:].replace(needle,
    '    if sys.platform == "ios":\n'
    '        from ios_ffmpeg import write_metadata_tags as native_tags\n'
    '        return native_tags(path, data, thumbnail=thumbnail)\n'
    + needle, 1)
assert updated.count('if sys.platform == "ios":') == 3
target.write_text(updated)
(device / "patches/base-api-ios-ffmpeg.patch").write_text("".join(difflib.unified_diff(
    original.splitlines(True), updated.splitlines(True),
    fromfile="a/base_api/modules/ffmpeg.py", tofile="b/base_api/modules/ffmpeg.py")))
