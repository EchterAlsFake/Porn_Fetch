"""Prepare native libraries and repair Qt platform bridges before Gradle packaging.

Loaded by python-for-android through p4a.hook, including on clean builds.
"""
from __future__ import annotations

import configparser
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

MARKER = "porn-fetch-storage-results-v1"


def prepare_native_libraries(native: Path, resources: Path) -> None:
    """Give Qt's preload copies Android-extractable names, keeping wheel modules intact."""
    renamed = {}
    for library in native.glob("*/*.so"):
        if library.name.startswith("lib"):
            # A subsequent build regenerates libs.xml but can reuse the already
            # renamed files in the distribution's native directory.
            renamed[(library.parent.name, library.name[3:])] = library.name
        else:
            name = "lib" + library.name
            renamed[(library.parent.name, library.name)] = name
            library.replace(library.with_name(name))
    for resource in resources.glob("values*/*.xml"):
        xml = ET.parse(resource)
        changed = False
        for item in xml.iter("item"):
            abi, separator, name = (item.text or "").strip().partition(";")
            if separator and (abi, name) in renamed:
                item.text = abi + ";" + renamed[(abi, name)]
                changed = True
        if changed:
            xml.write(resource, encoding="utf-8", xml_declaration=True)


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
    dist_dir = Path(toolchain._dist.dist_dir)
    # Android 13 extracts lib*.so only. QtCore.abi3.so in APK/lib is silently
    # skipped, so QtLoader cannot preload it from nativeLibraryDir on tablets.
    prepare_native_libraries(dist_dir / "libs", dist_dir / "src/main/res")
    activity = dist_dir / "src/main/java/org/kivy/android/PythonActivity.java"
    project = Path(__file__).resolve().parents[1]
    tor = project / "src/shared/tor/libTor.so"
    if tor.is_file():
        config = configparser.ConfigParser(interpolation=None)
        config.read(project / "buildozer.spec")
        abi = config["app"]["android.archs"]
        if abi not in {"arm64-v8a", "armeabi-v7a", "x86", "x86_64"}:
            raise ValueError("Tor native library requires a single supported Android ABI")
        native = Path(toolchain._dist.dist_dir) / "libs" / abi
        native.mkdir(parents=True, exist_ok=True)
        shutil.copy2(tor, native / "libTor.so")
    source = activity.read_text(encoding="utf-8")
    patched = patch_activity(source)
    call = "org.kivy.android.PornFetchDisplay.install(this);"
    if call not in patched:
        anchor = "super.onCreate(savedInstanceState);"
        if anchor not in patched:
            raise ValueError("Cannot locate Qt activity onCreate for display outline")
        patched = patched.replace(anchor, anchor + "\n        " + call, 1)
    platform_call = "org.kivy.android.PornFetchPlatform.install(this);"
    if platform_call not in patched:
        patched = patched.replace(call, call + "\n        " + platform_call, 1)
    notification_call = "org.kivy.android.PornFetchNotifications.install(this);"
    if notification_call not in patched:
        patched = patched.replace(platform_call, platform_call + "\n        " + notification_call, 1)
    storage_call = "org.kivy.android.PornFetchStorage.install(this);"
    if storage_call not in patched:
        # Publish capabilities before Qt starts Python, so QML's constant
        # availability property cannot observe a half-initialized bridge.
        anchor = "super.onCreate(savedInstanceState);"
        patched = patched.replace(anchor, storage_call + "\n        " + anchor, 1)
    helper = Path(__file__).parent / "android" / "PornFetchDisplay.java"
    (activity.parent / helper.name).write_text(helper.read_text(encoding="utf-8"), encoding="utf-8")
    for name in ("PornFetchPlatform.java", "PornFetchUpdateProvider.java", "PornFetchNotifications.java", "PornFetchStorage.java"):
        helper = Path(__file__).parent / "android" / name
        (activity.parent / name).write_text(helper.read_text(encoding="utf-8"), encoding="utf-8")
    for manifest in (Path(toolchain._dist.dist_dir) / "src/main/AndroidManifest.xml",
                     Path(toolchain._dist.dist_dir) / "AndroidManifest.xml"):
        if manifest.is_file():
            text = manifest.read_text(encoding="utf-8")
            if "android.permission.POST_NOTIFICATIONS" not in text:
                text = text.replace("<application", '<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />\n<application', 1)
            if "PornFetchUpdateProvider" not in text:
                text = text.replace("</application>", '<provider android:name="org.kivy.android.PornFetchUpdateProvider" '
                                    'android:authorities="to.pornfetch.app.updates" android:exported="false" '
                                    'android:grantUriPermissions="true" /></application>')
                text = text.replace("<application", '<uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES" />\n<application', 1)
            import re
            text = re.sub(r'android:extractNativeLibs="[^"]*"', 'android:extractNativeLibs="true"', text)
            if 'android:extractNativeLibs=' not in text:
                text = text.replace("<application", '<application android:extractNativeLibs="true"', 1)
            manifest.write_text(text, encoding="utf-8")
    if patched != source:
        activity.write_text(patched, encoding="utf-8")
