package org.kivy.android;

/** Export completed downloads through MediaStore on devices without a picker. */
public final class PornFetchStorage {
    private static android.os.FileObserver observer;
    private static final java.util.concurrent.ExecutorService worker =
            java.util.concurrent.Executors.newSingleThreadExecutor();
    private static final String LOCATION = android.os.Environment.DIRECTORY_DOWNLOADS + "/Porn Fetch/";

    public static void install(android.app.Activity activity) {
        java.io.File directory = new java.io.File(activity.getFilesDir(), "storage-requests");
        directory.mkdirs();
        if (observer != null) observer.stopWatching();
        observer = new android.os.FileObserver(directory.getAbsolutePath(),
                android.os.FileObserver.MOVED_TO | android.os.FileObserver.CLOSE_WRITE) {
            @Override public void onEvent(int event, String path) {
                if (path != null && path.endsWith(".request.json")) {
                    worker.execute(() -> export(activity, new java.io.File(directory, path)));
                }
            }
        };
        observer.startWatching();
        try {
            org.json.JSONObject capabilities = new org.json.JSONObject();
            capabilities.put("sharedDownloads", android.os.Build.VERSION.SDK_INT >= 29
                    && activity.getPackageManager().resolveContentProvider("media", 0) != null);
            write(new java.io.File(activity.getFilesDir(), "storage-capabilities.json"), capabilities);
        } catch (Exception error) {
            android.util.Log.w("PornFetchStorage", "Could not publish storage capabilities", error);
        }
    }

    private static void write(java.io.File path, org.json.JSONObject value) throws Exception {
        android.util.AtomicFile file = new android.util.AtomicFile(path);
        java.io.FileOutputStream output = file.startWrite();
        try {
            output.write(value.toString().getBytes(java.nio.charset.StandardCharsets.UTF_8));
            file.finishWrite(output);
        } catch (Exception error) {
            file.failWrite(output);
            throw error;
        }
    }

    private static void export(android.app.Activity activity, java.io.File request) {
        if (!request.isFile()) return;
        android.content.ContentResolver resolver = activity.getContentResolver();
        android.net.Uri destination = null;
        boolean published = false;
        org.json.JSONObject result = new org.json.JSONObject();
        try {
            if (android.os.Build.VERSION.SDK_INT < 29) {
                throw new java.io.IOException("Shared Downloads requires Android 10 or newer.");
            }
            org.json.JSONObject command = new org.json.JSONObject(new String(
                    java.nio.file.Files.readAllBytes(request.toPath()), java.nio.charset.StandardCharsets.UTF_8));
            java.io.File source = new java.io.File(command.getString("source")).getCanonicalFile();
            if (!source.isFile()) throw new java.io.IOException("The completed download is missing.");
            android.net.Uri collection = android.provider.MediaStore.Downloads.getContentUri(
                    android.provider.MediaStore.VOLUME_EXTERNAL_PRIMARY);
            if (command.optBoolean("skipExisting")) {
                String selection = "_display_name = ? AND relative_path = ? AND owner_package_name = ? AND is_pending = 0";
                try (android.database.Cursor cursor = resolver.query(collection, new String[]{"_id"},
                        selection, new String[]{source.getName(), LOCATION, activity.getPackageName()}, null)) {
                    if (cursor != null && cursor.moveToFirst()) {
                        result.put("ok", true);
                        result.put("uri", android.content.ContentUris.withAppendedId(collection, cursor.getLong(0)));
                        result.put("skipped", true);
                        return;
                    }
                }
            }
            android.content.ContentValues values = new android.content.ContentValues();
            values.put(android.provider.MediaStore.MediaColumns.DISPLAY_NAME, source.getName());
            values.put(android.provider.MediaStore.MediaColumns.RELATIVE_PATH, LOCATION);
            String mime = java.net.URLConnection.guessContentTypeFromName(source.getName());
            values.put(android.provider.MediaStore.MediaColumns.MIME_TYPE,
                    mime == null ? "application/octet-stream" : mime);
            values.put(android.provider.MediaStore.MediaColumns.IS_PENDING, 1);
            destination = resolver.insert(collection, values);
            if (destination == null) throw new java.io.IOException("Android could not create the shared download.");
            try (java.io.InputStream input = new java.io.FileInputStream(source);
                 java.io.OutputStream output = resolver.openOutputStream(destination, "w")) {
                if (output == null) throw new java.io.IOException("Android could not open the shared download.");
                byte[] buffer = new byte[1024 * 1024];
                int count;
                while ((count = input.read(buffer)) != -1) {
                    if (!request.exists()) throw new java.io.IOException("Export cancelled.");
                    output.write(buffer, 0, count);
                }
            }
            if (!request.exists()) throw new java.io.IOException("Export cancelled.");
            values.clear();
            values.put(android.provider.MediaStore.MediaColumns.IS_PENDING, 0);
            if (resolver.update(destination, values, null, null) != 1) {
                throw new java.io.IOException("Android could not publish the shared download.");
            }
            published = true;
            result.put("ok", true);
            result.put("uri", destination.toString());
        } catch (Exception error) {
            try {
                result.put("ok", false);
                result.put("error", error.getMessage());
            } catch (org.json.JSONException ignored) { }
        } finally {
            if (destination != null && !published) {
                try { resolver.delete(destination, null, null); }
                catch (Exception error) { android.util.Log.w("PornFetchStorage", "Could not remove incomplete export", error); }
            }
            try {
                write(new java.io.File(request.getParentFile(),
                        request.getName().replace(".request.json", ".result.json")), result);
            } catch (Exception error) {
                android.util.Log.w("PornFetchStorage", "Could not report export result", error);
            }
            request.delete();
        }
    }
}
