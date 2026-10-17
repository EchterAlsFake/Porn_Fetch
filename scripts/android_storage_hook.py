"""Repair the Qt activity's SAF result handling before Gradle builds the package.

Loaded by python-for-android through p4a.hook, including on clean builds.
"""
from __future__ import annotations

import re
from pathlib import Path

MARKER = "porn-fetch-storage-results-v1"


def patch_activity(source: str) -> str:
    if MARKER in source:
        return source
    if "extends QtActivity" not in source:
        raise ValueError("Storage hook requires the Qt PythonActivity")
    pattern = (
        r"(protected void onActivityResult\(int requestCode, int resultCode, Intent (\w+)\)\s*\{)"
    )
    match = re.search(pattern, source)
    if match is None:
        raise ValueError("Cannot locate PythonActivity.onActivityResult")
    intent = match.group(2)
    # Some p4a versions forward to Qt already; move that call before the early return.
    call = f"super.onActivityResult(requestCode, resultCode, {intent});"
    source = source.replace(call, "")
    match = re.search(pattern, source)
    insertion = f'''
        // {MARKER}
        // Qt's folder picker only persists read access. Retain the write grant
        // returned by ACTION_OPEN_DOCUMENT_TREE before passing the result to Qt.
        if (resultCode == android.app.Activity.RESULT_OK && {intent} != null
                && {intent}.getData() != null
                && android.provider.DocumentsContract.isTreeUri({intent}.getData())) {{
            int grants = {intent}.getFlags() & (Intent.FLAG_GRANT_READ_URI_PERMISSION
                    | Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
            if (({intent}.getFlags() & Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION) != 0) {{
                try {{
                    getContentResolver().takePersistableUriPermission({intent}.getData(), grants);
                }} catch (SecurityException error) {{
                    android.util.Log.w("PornFetchStorage", "Could not retain folder access", error);
                }}
            }}
        }}
        // Qt must receive the result even when no Python listeners are registered.
        {call}
'''
    return source[:match.end()] + insertion + source[match.end():]


def before_apk_build(toolchain) -> None:
    """p4a invokes this before build.py runs parse_args_and_make_package."""
    dist_dir = Path(toolchain._dist.dist_dir)
    build_py = dist_dir / "build.py"
    if build_py.is_file():
        source = build_py.read_text(encoding="utf-8")
        target = "shutil.copy(args.icon_bg, join(res_dir, 'mipmap/icon_background.png'))"
        patch = "\n        ensure_dir(join(res_dir, 'mipmap-anydpi-v26'))"
        if target in source and patch not in source:
            source = source.replace(target, target + patch, 1)
            build_py.write_text(source, encoding="utf-8")


def before_apk_assemble(toolchain) -> None:
    """p4a invokes this for APK and AAB builds, after generating Java sources."""
    activity = (Path(toolchain._dist.dist_dir) / "src/main/java/org/kivy/android/PythonActivity.java")
    source = activity.read_text(encoding="utf-8")
    patched = patch_activity(source)
    if patched != source:
        activity.write_text(patched, encoding="utf-8")
