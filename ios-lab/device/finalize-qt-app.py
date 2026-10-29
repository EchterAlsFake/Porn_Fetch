"""Complete the iOS metadata normally supplied by an Xcode build, then sign."""
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys

device = Path(__file__).resolve().parent
app = Path(sys.argv[1]).resolve()
# The upstream copy phase includes CPython's large test suite and desktop-only
# tools. Match the lean stdlib already verified by the native module probe.
for stdlib in (app / "python/lib").glob("python3.*"):
    for name in ("test", "tests", "idlelib", "tkinter", "ensurepip", "turtledemo"):
        shutil.rmtree(stdlib / name, ignore_errors=True)
    for cache in stdlib.rglob("__pycache__"):
        shutil.rmtree(cache)
info_path = app / "Info.plist"
info = plistlib.loads(info_path.read_bytes())
info.update(CFBundleDisplayName=app.stem, MinimumOSVersion="15.0",
            CFBundleSupportedPlatforms=["iPhoneOS"], UIDeviceFamily=[1, 2], UILaunchScreen={})
info["UIApplicationSceneManifest"] = {
    "UIApplicationSupportsMultipleScenes": False,
    "UISceneConfigurations": {
        "UIWindowSceneSessionRoleApplication": [{
            "UISceneConfigurationName": "Default Configuration",
            "UISceneDelegateClassName": "QIOSWindowSceneDelegate",
        }],
    },
}
info.pop("UILaunchStoryboardName", None)
if app.stem == "PornFetch":
    info["UIFileSharingEnabled"] = True
    info["LSSupportsOpeningDocumentsInPlace"] = True
info_path.write_bytes(plistlib.dumps(info))
for framework in (app / "Frameworks").glob("*.framework"):
    framework_info = plistlib.loads((framework / "Info.plist").read_bytes())
    subprocess.run([str(device / "tools/ldid"), "-S",
                    str(framework / framework_info["CFBundleExecutable"])], check=True)
subprocess.run([str(device / "tools/ldid"), "-S" + str(device / "qt-app.entitlements.plist"),
                str(app / info["CFBundleExecutable"])], check=True)
subprocess.run(["tar", "-cf", str(device / "artifacts" / (app.stem + ".tar")),
                "-C", str(app.parent), app.name], check=True)
