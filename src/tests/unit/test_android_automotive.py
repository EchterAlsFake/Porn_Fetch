"""Android car packaging must stay optional and preserve existing activity handlers."""
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from scripts.android_storage_hook import (
    before_apk_assemble,
    patch_automotive_activity,
    prepare_automotive_manifest,
)

ANDROID = "{http://schemas.android.com/apk/res/android}"
ACTIVITY = '''public class PythonActivity extends QtActivity {
    public void onCreate(Bundle savedInstanceState) { super.onCreate(savedInstanceState); }
    protected void onActivityResult(int requestCode, int resultCode, Intent intent) {}
    public boolean dispatchKeyEvent(android.view.KeyEvent key) { return super.dispatchKeyEvent(key); }
}'''


class AutomotivePackagingTests(unittest.TestCase):
    def test_shared_apk_keeps_car_library_optional_and_activities_parked(self):
        source = '''<manifest xmlns:android="http://schemas.android.com/apk/res/android">
          <application><activity android:name="org.kivy.android.PythonActivity">
            <meta-data android:name="distractionOptimized" android:value="true"/>
          </activity></application></manifest>'''
        result = prepare_automotive_manifest(source)
        root = ET.fromstring(result)
        self.assertEqual(root.find("uses-feature").get(ANDROID + "required"), "false")
        self.assertEqual(root.find("application/uses-library").get(ANDROID + "required"), "false")
        self.assertEqual(root.find("application/meta-data").get(ANDROID + "value"), "true")
        self.assertIsNone(root.find("application/activity/meta-data"))
        self.assertNotIn("CAR_LAUNCHER", result)
        self.assertNotIn("appCategory", result)
        self.assertEqual(prepare_automotive_manifest(result), result)

    def test_input_hooks_preserve_existing_handlers_and_are_idempotent(self):
        result = patch_automotive_activity(ACTIVITY)
        self.assertIn("onKey(this, key)", result)
        self.assertEqual(result.count("public boolean dispatchKeyEvent"), 1)
        self.assertLess(result.index("onKey(this, key)"), result.index("super.dispatchKeyEvent(key)"))
        self.assertIn("onGenericMotion(this, event)", result)
        self.assertIn("onTouch(this, event)", result)
        self.assertEqual(patch_automotive_activity(result), result)

    def test_hook_stages_car_helpers_and_patches_only_the_android_gradle_module(self):
        with tempfile.TemporaryDirectory() as directory, patch("scripts.android_storage_hook.stage_pocketbase"):
            root = Path(directory)
            activity = root / "src/main/java/org/kivy/android/PythonActivity.java"
            activity.parent.mkdir(parents=True)
            activity.write_text(ACTIVITY)
            (root / "build.gradle").write_text("// Root build script\n")
            (root / "app").mkdir()
            module = root / "app/build.gradle"
            module.write_text("apply plugin: 'com.android.application'\nandroid {}\n")
            toolchain = SimpleNamespace(_dist=SimpleNamespace(dist_dir=directory))
            before_apk_assemble(toolchain)
            self.assertTrue((activity.parent / "PornFetchAutomotive.java").is_file())
            self.assertTrue((activity.parent / "PornFetchCarService.java").is_file())
            self.assertNotIn("useLibrary", (root / "build.gradle").read_text())
            self.assertIn("useLibrary 'android.car'", module.read_text())
            before_apk_assemble(toolchain)
            self.assertEqual(module.read_text().count("useLibrary 'android.car'"), 1)
