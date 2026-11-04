package org.kivy.android;

/** Private, opt-in notification commands from the Qt frontend. */
public final class PornFetchNotifications {
    private static final String CHANNEL = "download-results";
    private static android.os.FileObserver observer;

    public static void install(android.app.Activity activity) {
        if (observer != null) observer.stopWatching();
        observer = new android.os.FileObserver(activity.getFilesDir().getAbsolutePath(),
                android.os.FileObserver.MOVED_TO | android.os.FileObserver.CLOSE_WRITE) {
            @Override public void onEvent(int event, String path) {
                if ("notifications-request.json".equals(path)) {
                    activity.runOnUiThread(() -> consume(activity));
                }
            }
        };
        observer.startWatching();
        activity.getWindow().getDecorView().getViewTreeObserver()
                .addOnWindowFocusChangeListener(focused -> { if (focused) publishStatus(activity); });
        consume(activity);
        publishStatus(activity);
    }

    private static void publishStatus(android.app.Activity activity) {
        try {
            android.app.NotificationManager manager = activity.getSystemService(android.app.NotificationManager.class);
            android.app.NotificationChannel channel = manager.getNotificationChannel(CHANNEL);
            boolean allowed = manager.areNotificationsEnabled()
                    && (channel == null || channel.getImportance() != android.app.NotificationManager.IMPORTANCE_NONE);
            org.json.JSONObject status = new org.json.JSONObject();
            status.put("state", allowed ? "allowed" : "denied");
            android.util.AtomicFile file = new android.util.AtomicFile(
                    new java.io.File(activity.getFilesDir(), "notifications-state.json"));
            java.io.FileOutputStream output = file.startWrite();
            try {
                output.write(status.toString().getBytes(java.nio.charset.StandardCharsets.UTF_8));
                file.finishWrite(output);
            } catch (Exception error) {
                file.failWrite(output);
            }
        } catch (Exception ignored) {
            android.util.Log.w("PornFetchNotifications", "Cannot read notification settings");
        }
    }

    private static void consume(android.app.Activity activity) {
        java.io.File path = new java.io.File(activity.getFilesDir(), "notifications-request.json");
        if (!path.isFile()) return;
        try {
            org.json.JSONObject command = new org.json.JSONObject(new String(
                    java.nio.file.Files.readAllBytes(path.toPath()), java.nio.charset.StandardCharsets.UTF_8));
            path.delete();
            android.app.NotificationManager manager = activity.getSystemService(android.app.NotificationManager.class);
            String action = command.getString("action");
            if ("enable".equals(action)) {
                android.app.NotificationChannel channel = new android.app.NotificationChannel(
                        CHANNEL, command.optString("title", "Downloads"), android.app.NotificationManager.IMPORTANCE_DEFAULT);
                channel.setSound(null, null);
                channel.enableVibration(false);
                channel.setLockscreenVisibility(android.app.Notification.VISIBILITY_SECRET);
                manager.createNotificationChannel(channel);
                android.content.SharedPreferences preferences = activity.getPreferences(0);
                if (android.os.Build.VERSION.SDK_INT >= 33
                        && activity.checkSelfPermission("android.permission.POST_NOTIFICATIONS")
                            != android.content.pm.PackageManager.PERMISSION_GRANTED
                        && !preferences.getBoolean("notifications-requested", false)) {
                    preferences.edit().putBoolean("notifications-requested", true).apply();
                    activity.requestPermissions(new String[]{"android.permission.POST_NOTIFICATIONS"}, 3310);
                }
            } else if ("settings".equals(action)) {
                activity.startActivity(new android.content.Intent(android.provider.Settings.ACTION_APP_NOTIFICATION_SETTINGS)
                        .putExtra(android.provider.Settings.EXTRA_APP_PACKAGE, activity.getPackageName()));
            } else if ("disable".equals(action)) {
                manager.cancel(3310);
            } else if ("notify".equals(action) && manager.areNotificationsEnabled()) {
                android.content.Intent intent = activity.getPackageManager().getLaunchIntentForPackage(activity.getPackageName());
                if (intent == null) return;
                intent.addFlags(android.content.Intent.FLAG_ACTIVITY_SINGLE_TOP | android.content.Intent.FLAG_ACTIVITY_CLEAR_TOP);
                android.app.PendingIntent open = android.app.PendingIntent.getActivity(activity, 3310, intent,
                        android.app.PendingIntent.FLAG_UPDATE_CURRENT | android.app.PendingIntent.FLAG_IMMUTABLE);
                android.app.Notification notification = new android.app.Notification.Builder(activity, CHANNEL)
                        .setSmallIcon(android.R.drawable.stat_sys_download_done)
                        .setContentTitle(command.optString("title", "Downloads"))
                        .setContentText(command.getString("message"))
                        .setStyle(new android.app.Notification.BigTextStyle().bigText(command.getString("message")))
                        .setVisibility(android.app.Notification.VISIBILITY_SECRET)
                        .setContentIntent(open).setAutoCancel(true).setOnlyAlertOnce(true).build();
                manager.notify(3310, notification);
            }
        } catch (Exception ignored) {
            path.delete();
            android.util.Log.w("PornFetchNotifications", "Notification command unavailable");
        }
        publishStatus(activity);
    }
}
