"""Offline storage regressions; device SAF permissions still need an Android smoke test."""
import asyncio
import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from PySide6.QtCore import QUrl

from scripts.android_storage_hook import before_apk_assemble, before_apk_build, patch_activity, prepare_native_libraries
from src.backend.android_storage import copy_download_file, folder_destination, save_shared_download

ACTIVITY = '''public class PythonActivity extends QtActivity {
    public void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); }
    protected void onActivityResult(int requestCode, int resultCode, Intent intent) {
        if (this.activityResultListeners == null) return;
        listener.onActivityResult(requestCode, resultCode, intent);
    }
}'''


class AndroidActivityTests(unittest.TestCase):
    def test_qt_preloads_use_extractable_names_for_every_android_abi(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            libraries = root / "libs"
            resources = root / "res/values"
            resources.mkdir(parents=True)
            abis = ("arm64-v8a", "armeabi-v7a", "x86", "x86_64")
            entries = []
            for abi in abis:
                native = libraries / abi
                native.mkdir(parents=True)
                (native / "QtCore.abi3.so").write_bytes(b"qt binding")
                (native / "libpyside6.abi3.so").write_bytes(b"pyside")
                entries.append(f"<item>{abi};QtCore.abi3.so</item><item>{abi};libpyside6.abi3.so</item>")
            loader = resources / "libs.xml"
            original = '<resources><array name="load_local_libs">' + ''.join(entries) + '</array></resources>'
            loader.write_text(original)
            prepare_native_libraries(libraries, resources.parent)
            for abi in abis:
                self.assertEqual((libraries / abi / "libQtCore.abi3.so").read_bytes(), b"qt binding")
                self.assertFalse((libraries / abi / "QtCore.abi3.so").exists())
                self.assertIn(f"{abi};libQtCore.abi3.so", loader.read_text())
                self.assertEqual((libraries / abi / "libpyside6.abi3.so").read_bytes(), b"pyside")
            first = loader.read_bytes()
            prepare_native_libraries(libraries, resources.parent)
            self.assertEqual(loader.read_bytes(), first)
            loader.write_text(original)  # p4a regenerates resources on an incremental build.
            prepare_native_libraries(libraries, resources.parent)
            self.assertEqual(loader.read_bytes(), first)

    def test_result_forwarded_before_listener_early_return_and_write_grant_retained(self):
        source = patch_activity(ACTIVITY)
        self.assertLess(source.index('super.onActivityResult('), source.index('if (this.activityResultListeners'))
        self.assertIn('Intent.FLAG_GRANT_WRITE_URI_PERMISSION', source)
        self.assertIn('takePersistableUriPermission(intent.getData(), grants)', source)
        self.assertEqual(patch_activity(source), source)

    def test_update_permission_result_forwarded_on_fresh_and_incremental_builds(self):
        call = 'org.kivy.android.PornFetchPlatform.onActivityResult(this, requestCode);'
        source = patch_activity(ACTIVITY)
        self.assertEqual(source.count(call), 1)
        self.assertLess(source.index(call), source.index('if (this.activityResultListeners'))
        # Previously patched distributions must also receive the new bridge.
        previous = source.replace(call, '')
        upgraded = patch_activity(previous)
        self.assertEqual(upgraded.count(call), 1)
        self.assertEqual(patch_activity(upgraded), upgraded)

    def test_existing_super_call_is_not_duplicated(self):
        source = ACTIVITY.replace('listener.onActivityResult', 'super.onActivityResult')
        self.assertEqual(patch_activity(source).count('super.onActivityResult('), 1)

    def test_hook_updates_generated_distribution(self):
        with tempfile.TemporaryDirectory() as directory:
            activity = Path(directory) / 'src/main/java/org/kivy/android/PythonActivity.java'
            activity.parent.mkdir(parents=True)
            activity.write_text(ACTIVITY)
            before_apk_assemble(SimpleNamespace(_dist=SimpleNamespace(dist_dir=directory)))
            self.assertIn('PornFetchDisplay.install(this);', activity.read_text())
            self.assertTrue((activity.parent / 'PornFetchDisplay.java').exists())
            self.assertTrue((activity.parent / 'PornFetchStorage.java').exists())
            self.assertIn('PornFetchStorage.install(this);', activity.read_text())
            self.assertLess(activity.read_text().index('PornFetchStorage.install(this);'),
                            activity.read_text().index('super.onCreate(savedInstanceState);'))
            first = activity.read_text()
            before_apk_assemble(SimpleNamespace(_dist=SimpleNamespace(dist_dir=directory)))
            self.assertEqual(activity.read_text(), first)

    def test_hook_patches_build_py_adaptive_icon(self):
        with tempfile.TemporaryDirectory() as directory:
            build_py = Path(directory) / 'build.py'
            build_py.write_text("shutil.copy(args.icon_bg, join(res_dir, 'mipmap/icon_background.png'))\n")
            before_apk_build(SimpleNamespace(_dist=SimpleNamespace(dist_dir=directory)))
            self.assertIn("ensure_dir(join(res_dir, 'mipmap-anydpi-v26'))", build_py.read_text())


class StorageCopyTests(unittest.TestCase):
    def test_uri_preserves_tree_id_and_encodes_filename(self):
        tree = 'content://com.android.externalstorage.documents/tree/primary%3AMovies%2FTest'
        destination = folder_destination(QUrl(tree), '100% #é.mp4')
        self.assertEqual(destination, tree + '/100%25%20%23%C3%A9.mp4')

    def test_copy_and_same_file_preserve_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'source.mp4'
            source.write_bytes(b'video' * 300000)
            destination = folder_destination(QUrl.fromLocalFile(directory), 'copy.mp4')
            copy_download_file(source, destination)
            self.assertEqual(Path(destination).read_bytes(), source.read_bytes())
            copy_download_file(source, str(source))
            self.assertEqual(source.stat().st_size, 1500000)

    def test_flush_failure_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'source.mp4'
            source.write_bytes(b'video')
            with patch('src.backend.android_storage.QFile') as file_type:
                target = file_type.return_value
                target.open.return_value = True
                target.write.return_value = 5
                target.flush.return_value = False
                target.errorString.return_value = 'write failed'
                with self.assertRaisesRegex(OSError, 'write failed'):
                    copy_download_file(source, 'content://provider/document/1')
                target.close.assert_called_once()


class SharedDownloadsTests(unittest.IsolatedAsyncioTestCase):
    async def test_native_result_is_awaited_and_export_errors_propagate(self):
        for result in ({"ok": True, "uri": "content://media/external_primary/downloads/7"},
                       {"ok": False, "error": "Storage unavailable"}):
            with self.subTest(result=result), tempfile.TemporaryDirectory() as directory:
                private = Path(directory)
                (private / "storage-capabilities.json").write_text('{"sharedDownloads": true}')
                source = private / "video.mp4"
                source.write_bytes(b"completed download")
                watcher = Mock()
                with patch.dict(os.environ, {"ANDROID_PRIVATE": directory}), \
                     patch("src.backend.android_storage.QFileSystemWatcher", return_value=watcher):
                    task = asyncio.create_task(save_shared_download(source, True))
                    await asyncio.sleep(0)
                    request, = (private / "storage-requests").glob("*.request.json")
                    self.assertEqual(json.loads(request.read_text()), {"source": str(source), "skipExisting": True})
                    response = request.with_name(request.name.replace('.request.json', '.result.json'))
                    response.write_text(json.dumps(result))
                    watcher.directoryChanged.connect.call_args.args[0]()
                    if result['ok']:
                        self.assertEqual(await task, result['uri'])
                    else:
                        with self.assertRaisesRegex(OSError, 'Storage unavailable'):
                            await task
                    self.assertFalse(request.exists())
                    self.assertFalse(response.exists())
                    self.assertEqual(source.read_bytes(), b"completed download")
