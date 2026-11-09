# Android storage smoke test

Build a new APK using the updated `buildozer.spec` or `scripts/build_android.py`.
The `p4a.hook` must run before Gradle assembly; changing Python files alone does
not repair the native activity's picker callbacks.

1. In Settings, choose a writable folder such as `Movies/Porn Fetch` using the
   system picker. Confirm its name replaces “App storage” in Settings and Downloads.
2. Restart the app. Download a short video and confirm the selected folder contains
   a playable, nonempty copy. Downloads are staged in private app storage first.
3. On a fresh Android 10+ installation, choose **Use shared Downloads/Porn Fetch**
   in setup instead of opening the picker. Finish setup and download a short
   video. Check shared Downloads/Porn Fetch from another app, including the
   exported file's size/playback. Repeat on a TV/Automotive device without a
   working document-tree picker and verify D-pad-only setup completion.
4. Cancel a folder picker and confirm the existing selection stays unchanged.
5. If testing an installation upgraded from the broken activity, select the folder
   again once to grant persistent write access.
6. For shared Downloads, repeat an export with skip-existing enabled and verify
   it does not create a duplicate. Export failures must retain the original
   private file and keep the failed download available for retry. MediaStore
   files are intentionally retained after uninstall; remove test files yourself.

Use the system file manager to inspect document-provider locations. A `content://`
URI is a document identifier, not a filesystem path that can be passed to `adb ls`.
