package org.kivy.android;

/** Serves only the already-verified APK to the Android package installer. */
public final class PornFetchUpdateProvider extends android.content.ContentProvider {
    @Override public boolean onCreate() { return true; }
    private void check(android.net.Uri uri) {
        if (!"/update.apk".equals(uri.getPath())) throw new SecurityException("Unknown update URI");
    }
    @Override public String getType(android.net.Uri uri) {
        check(uri);
        return "application/vnd.android.package-archive";
    }
    @Override public android.os.ParcelFileDescriptor openFile(android.net.Uri uri, String mode)
            throws java.io.FileNotFoundException {
        check(uri);
        if (!"r".equals(mode)) throw new SecurityException("Read-only update URI");
        return android.os.ParcelFileDescriptor.open(new java.io.File(getContext().getFilesDir(),
                "pornfetch-update.apk"), android.os.ParcelFileDescriptor.MODE_READ_ONLY);
    }
    @Override public android.database.Cursor query(android.net.Uri uri, String[] projection,
            String selection, String[] args, String sortOrder) {
        check(uri);
        android.database.MatrixCursor cursor = new android.database.MatrixCursor(
                new String[]{"_display_name", "_size"});
        cursor.addRow(new Object[]{"PornFetch-update.apk",
                new java.io.File(getContext().getFilesDir(), "pornfetch-update.apk").length()});
        return cursor;
    }
    @Override public android.net.Uri insert(android.net.Uri uri, android.content.ContentValues values) {
        throw new SecurityException("Read-only");
    }
    @Override public int delete(android.net.Uri uri, String selection, String[] args) {
        throw new SecurityException("Read-only");
    }
    @Override public int update(android.net.Uri uri, android.content.ContentValues values, String selection, String[] args) {
        throw new SecurityException("Read-only");
    }
}
