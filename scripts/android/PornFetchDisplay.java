package org.kivy.android;

/** Publishes Android's window-relative screen outline for the Qt overlay.
 * Geometry changes rarely; an atomic private file bridges Java and PySide without
 * a second JNI runtime. Qt watches the directory, so no polling is necessary.
 */
public final class PornFetchDisplay {
    private static String lastGeometry = "";

    public static void install(android.app.Activity activity) {
        android.view.View decor = activity.getWindow().getDecorView();
        decor.getViewTreeObserver().addOnGlobalLayoutListener(() -> publish(activity));
        decor.post(() -> publish(activity));
    }

    private static void publish(android.app.Activity activity) {
        android.view.View content = activity.findViewById(android.R.id.content);
        if (content == null || content.getWidth() == 0 || content.getHeight() == 0) return;
        android.util.AtomicFile file = new android.util.AtomicFile(
                new java.io.File(activity.getFilesDir(), "display-outline.json"));
        java.io.FileOutputStream output = null;
        try {
            int[] location = new int[2];
            content.getLocationInWindow(location);
            org.json.JSONObject geometry = new org.json.JSONObject();
            geometry.put("width", content.getWidth());
            geometry.put("height", content.getHeight());
            org.json.JSONArray corners = new org.json.JSONArray();
            android.view.WindowInsets insets = activity.getWindow().getDecorView().getRootWindowInsets();
            // Android positions: top-left, top-right, bottom-right, bottom-left.
            for (int position = 0; position < 4; position++) {
                int radius = 0;
                int x = (position == 1 || position == 2) ? content.getWidth() : 0;
                int y = position >= 2 ? content.getHeight() : 0;
                if (android.os.Build.VERSION.SDK_INT >= 31 && insets != null) {
                    android.view.RoundedCorner corner = insets.getRoundedCorner(position);
                    if (corner != null) {
                        radius = corner.getRadius();
                        x = corner.getCenter().x - location[0];
                        y = corner.getCenter().y - location[1];
                    }
                }
                org.json.JSONObject corner = new org.json.JSONObject();
                corner.put("x", x);
                corner.put("y", y);
                corner.put("radius", radius);
                corners.put(corner);
            }
            geometry.put("corners", corners);
            String serialized = geometry.toString();
            if (serialized.equals(lastGeometry)) return;
            output = file.startWrite();
            output.write(serialized.getBytes(java.nio.charset.StandardCharsets.UTF_8));
            file.finishWrite(output);
            lastGeometry = serialized;
        } catch (Exception error) {
            if (output != null) file.failWrite(output);
            android.util.Log.w("PornFetchDisplay", "Cannot publish screen outline", error);
        }
    }
}
