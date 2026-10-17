"""Offline storage regressions; device SAF permissions still need an Android smoke test."""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from PySide6.QtCore import QUrl

from scripts.android_storage_hook import before_apk_assemble, before_apk_build, patch_activity
from src.backend.android_storage import copy_download_file, folder_destination

ACTIVITY = '''public class PythonActivity extends QtActivity {
    protected void onActivityResult(int requestCode, int resultCode, Intent intent) {
        if (this.activityResultListeners == null) return;
        listener.onActivityResult(requestCode, resultCode, intent);
    }
}'''


class AndroidActivityTests(unittest.TestCase):
    def test_result_forwarded_before_listener_early_return_and_write_grant_retained(self):
        source = patch_activity(ACTIVITY)
        self.assertLess(source.index('super.onActivityResult('), source.index('if (this.activityResultListeners'))
        self.assertIn('Intent.FLAG_GRANT_WRITE_URI_PERMISSION', source)
        self.assertIn('takePersistableUriPermission(intent.getData(), grants)', source)
        self.assertEqual(patch_activity(source), source)

    def test_existing_super_call_is_not_duplicated(self):
        source = ACTIVITY.replace('listener.onActivityResult', 'super.onActivityResult')
        self.assertEqual(patch_activity(source).count('super.onActivityResult('), 1)

    def test_hook_updates_generated_distribution(self):
        with tempfile.TemporaryDirectory() as directory:
            activity = Path(directory) / 'src/main/java/org/kivy/android/PythonActivity.java'
            activity.parent.mkdir(parents=True)
            activity.write_text(ACTIVITY)
            before_apk_assemble(SimpleNamespace(_dist=SimpleNamespace(dist_dir=directory)))
            self.assertEqual(activity.read_text(), patch_activity(ACTIVITY))

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
