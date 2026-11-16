# Embedded Android PocketBase

The project uses PocketBase 0.40.4, matching the desktop runtime, compiled as a
Go C shared library for arm64-v8a, armeabi-v7a, x86 and x86_64. Python loads the
APK's extracted native library using ctypes. Its authenticated HTTP server
listens only on an ephemeral loopback port and uses the application's private
data directory. The existing Python client and JavaScript migrations are shared
with desktop; history/statistics remain disabled on Android.

`PFStart(dataDir, migrationsDir, email, password)` and `PFStop()` return allocated
UTF-8 JSON strings. Call `PFFree(pointer)` after reading each result. Retain the
library until process exit; never unload an active Go runtime. Stop HTTP requests
before clearing PocketBase's database connections. A fresh random superuser
password is supplied for every start and never exposed to QML or persisted in
preferences. The PocketBase admin UI and public static-file server are omitted.
Only the fixed application migrations are loaded, not arbitrary JavaScript hooks.

Build all architectures from the project root:

```
python scripts/build_android_pocketbase.py --architecture all --ndk /path/to/android-ndk-r28c
```

The normal `scripts/build_android.py` wrapper invokes this automatically. The
helper downloads a checksummed Go 1.27.4 compiler if that version is not on PATH.
Go verifies module downloads against `go.sum`; builds use `-mod=readonly`.
Generated libraries, headers, notices and hashes go under
`build/android-pocketbase/<ABI>/`. The packaging hook requires the matching
library and copies it into `lib/<ABI>/libpornfetch_pocketbase.so`. Linker alignment
is 16 KiB. No native binaries are downloaded or executed from app data on Android.

`legal/` contains these bridge sources, module manifests, dependency notices,
source URLs and the Go license. It is included as APK assets/pocketbase-legal.
PocketBase and its dependencies retain their upstream licenses. The bridge is
covered by the repository's root LICENSE.

For host integration checks, run `go build -buildmode=c-shared -o /tmp/pb.so .`
here and set `PORN_FETCH_TEST_POCKETBASE_LIBRARY=/tmp/pb.so` for
`src.tests.integration.test_android_pocketbase`. Native compilation and host
checks do not establish device behavior; validate rebuilt APK startup and
pause/reopen/resume separately on Android.
