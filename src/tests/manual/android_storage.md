# Android storage smoke test

Build a new APK using the updated `buildozer.spec` or `scripts/build_android.py`.
The `p4a.hook` must run before Gradle assembly; changing Python files alone does
not repair the native activity's picker callbacks.

1. In Settings, choose a writable folder such as `Movies/Porn Fetch` using the
   system picker. Confirm its name replaces “App storage” in Settings and Downloads.
2. Restart the app. Download a short video and confirm the selected folder contains
   a playable, nonempty copy. Downloads are staged in private app storage first.
3. On a completed download, choose “Save elsewhere”. Confirm the picker proposes
   the video's filename, then save and check the exported file's size/playback.
4. Cancel a folder picker and confirm the existing selection stays unchanged.
5. If testing an installation upgraded from the broken activity, select the folder
   again once to grant persistent write access.

Use the system file manager to inspect document-provider locations. A `content://`
URI is a document identifier, not a filesystem path that can be passed to `adb ls`.
