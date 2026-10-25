package org.kivy.android;

/** Private file bridge between Qt Python and Android's user-confirmed installer. */
public final class PornFetchPlatform {
    private static android.os.FileObserver observer;

    public static void install(android.app.Activity activity) {
        try {
            org.json.JSONObject info = new org.json.JSONObject();
            info.put("package", activity.getPackageName());
            String[] abis = android.os.Process.is64Bit()
                    ? android.os.Build.SUPPORTED_64_BIT_ABIS : android.os.Build.SUPPORTED_32_BIT_ABIS;
            info.put("abi", abis[0]);
            info.put("nativeLibraryDir", activity.getApplicationInfo().nativeLibraryDir);
            write(activity, "pornfetch-platform.json", info);
        } catch (Exception error) {
            result(activity, "error", "Could not read Android application identity.");
        }
        observer = new android.os.FileObserver(activity.getFilesDir().getAbsolutePath(),
                android.os.FileObserver.MOVED_TO | android.os.FileObserver.CLOSE_WRITE) {
            @Override public void onEvent(int event, String path) {
                if ("install-update.json".equals(path)) {
                    activity.runOnUiThread(() -> requestInstall(activity));
                }
            }
        };
        observer.startWatching();
    }

    private static void write(android.app.Activity activity, String name, org.json.JSONObject value)
            throws Exception {
        android.util.AtomicFile file = new android.util.AtomicFile(new java.io.File(activity.getFilesDir(), name));
        java.io.FileOutputStream output = file.startWrite();
        try {
            output.write(value.toString().getBytes(java.nio.charset.StandardCharsets.UTF_8));
            file.finishWrite(output);
        } catch (Exception error) {
            file.failWrite(output);
            throw error;
        }
    }

    private static void result(android.app.Activity activity, String state, String message) {
        try {
            org.json.JSONObject value = new org.json.JSONObject();
            value.put("state", state);
            value.put("message", message);
            write(activity, "install-result.json", value);
        } catch (Exception ignored) {
            android.util.Log.w("PornFetchUpdate", "Could not report install status");
        }
    }

    private static void requestInstall(android.app.Activity activity) {
        java.io.File request = new java.io.File(activity.getFilesDir(), "install-update.json");
        if (!request.exists()) return;
        try {
            String text = new String(java.nio.file.Files.readAllBytes(request.toPath()),
                    java.nio.charset.StandardCharsets.UTF_8);
            request.delete();
            org.json.JSONObject command = new org.json.JSONObject(text);
            java.io.File apk = new java.io.File(activity.getFilesDir(), "pornfetch-update.apk");
            android.content.pm.PackageManager manager = activity.getPackageManager();
            int flags = android.content.pm.PackageManager.GET_SIGNING_CERTIFICATES;
            android.content.pm.PackageInfo installed = manager.getPackageInfo(activity.getPackageName(), flags);
            android.content.pm.PackageInfo update = manager.getPackageArchiveInfo(apk.getAbsolutePath(), flags);
            if (update == null || !activity.getPackageName().equals(update.packageName)
                    || !command.getString("version").equals(update.versionName)
                    || update.getLongVersionCode() <= installed.getLongVersionCode()) {
                throw new SecurityException("The APK package or version does not match the verified update.");
            }
            android.content.pm.Signature[] oldSigners = installed.signingInfo.getApkContentsSigners();
            android.content.pm.Signature[] newSigners = update.signingInfo.getApkContentsSigners();
            if (oldSigners.length != 1 || newSigners.length != 1 || !oldSigners[0].equals(newSigners[0])) {
                throw new SecurityException("The APK signing identity does not match this installation.");
            }
            try (java.util.zip.ZipFile archive = new java.util.zip.ZipFile(apk)) {
                String prefix = "lib/" + command.getString("abi") + "/";
                boolean compatible = java.util.Collections.list(archive.entries()).stream()
                        .anyMatch(entry -> entry.getName().startsWith(prefix));
                if (!compatible) throw new SecurityException("The APK has the wrong architecture.");
            }
            if (!manager.canRequestPackageInstalls()) {
                activity.startActivity(new android.content.Intent(
                        android.provider.Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,
                        android.net.Uri.parse("package:" + activity.getPackageName())));
                result(activity, "permission", "Allow installs from Porn Fetch, then select Install update again.");
                return;
            }
            android.net.Uri uri = android.net.Uri.parse("content://" + activity.getPackageName() + ".updates/update.apk");
            android.content.Intent intent = new android.content.Intent(android.content.Intent.ACTION_INSTALL_PACKAGE);
            intent.setDataAndType(uri, "application/vnd.android.package-archive");
            intent.addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION);
            activity.startActivity(intent);
            result(activity, "confirmation", "Confirm the update in Android's installer. Cancelling keeps the current version.");
        } catch (Exception error) {
            request.delete();
            result(activity, "error", error.getMessage() == null ? "Android could not open the update." : error.getMessage());
        }
    }
}
