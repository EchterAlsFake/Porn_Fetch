package org.kivy.android;

/** Optional car policy and input bridge. Phones and TVs keep their native input paths. */
public final class PornFetchAutomotive implements android.app.Application.ActivityLifecycleCallbacks {
    private static PornFetchAutomotive current;
    private final android.app.Activity activity;
    private final boolean automotive;
    private final boolean carMode;
    private boolean foreground;
    private boolean controllerNavigation;
    private boolean restricted;
    private boolean restrictionsKnown;
    private float remainingRotation;
    private int pauseGeneration;
    private AutoCloseable carService;

    private PornFetchAutomotive(android.app.Activity activity) {
        this.activity = activity;
        automotive = activity.getPackageManager().hasSystemFeature("android.hardware.type.automotive");
        carMode = automotive || (activity.getResources().getConfiguration().uiMode
                & android.content.res.Configuration.UI_MODE_TYPE_MASK)
                == android.content.res.Configuration.UI_MODE_TYPE_CAR;
    }

    public static void install(android.app.Activity activity) {
        if (current != null) current.close();
        current = new PornFetchAutomotive(activity);
        activity.getApplication().registerActivityLifecycleCallbacks(current);
        current.publish();
        if (current.automotive) {
            try {
                // Isolate android.car references: that optional shared library is absent on phones.
                current.carService = (AutoCloseable) Class.forName("org.kivy.android.PornFetchCarService")
                        .getConstructor(android.app.Activity.class).newInstance(activity);
            } catch (ReflectiveOperationException | LinkageError error) {
                // Ordinary, non-distraction-optimized activities are still blocked by AAOS itself.
                android.util.Log.w("PornFetchAutomotive", "Vehicle restriction API unavailable; using system activity restrictions", error);
            }
        }
    }

    static void restrictions(android.app.Activity activity, boolean known, boolean restricted) {
        activity.runOnUiThread(() -> {
            if (current == null || current.activity != activity) return;
            current.restrictionsKnown = known;
            current.restricted = restricted;
            current.publish();
        });
    }

    private void publish() {
        try {
            org.json.JSONObject value = new org.json.JSONObject();
            value.put("automotive", automotive);
            value.put("carMode", carMode);
            value.put("systemNavigation", automotive && activity.getPackageManager()
                    .hasSystemFeature("android.software.car.display_compatibility"));
            value.put("controllerNavigation", controllerNavigation);
            value.put("foreground", foreground);
            value.put("pauseGeneration", pauseGeneration);
            value.put("restrictionsKnown", restrictionsKnown);
            value.put("restricted", restricted);
            android.util.AtomicFile file = new android.util.AtomicFile(
                    new java.io.File(activity.getFilesDir(), "automotive-state.json"));
            java.io.FileOutputStream output = file.startWrite();
            try {
                output.write(value.toString().getBytes(java.nio.charset.StandardCharsets.UTF_8));
                file.finishWrite(output);
            } catch (Exception error) { file.failWrite(output); throw error; }
        } catch (Exception error) { android.util.Log.w("PornFetchAutomotive", "Could not publish vehicle state", error); }
    }

    public static boolean onGenericMotion(android.app.Activity activity, android.view.MotionEvent event) {
        if (current == null || current.activity != activity
                || event.getActionMasked() != android.view.MotionEvent.ACTION_SCROLL
                || !event.isFromSource(android.view.InputDevice.SOURCE_ROTARY_ENCODER)) return false;
        if (!current.foreground || !activity.hasWindowFocus()) return false;
        float rotation = event.getAxisValue(android.view.MotionEvent.AXIS_SCROLL);
        if (rotation == 0) rotation = event.getAxisValue(android.view.MotionEvent.AXIS_VSCROLL);
        if (rotation == 0) rotation = event.getAxisValue(android.view.MotionEvent.AXIS_HSCROLL);
        if (!Float.isFinite(rotation) || rotation == 0) return false;
        current.useController();
        // Focus the restricted screen's exit action without operating the hidden page.
        if (current.restricted) return true;
        current.remainingRotation += rotation;
        int steps = (int) current.remainingRotation;
        current.remainingRotation -= steps;
        // F11/F12 are private rotary commands to the QML navigator. Mouse wheels,
        // media/volume keys and the system keyboard are never translated.
        int key = steps > 0 ? android.view.KeyEvent.KEYCODE_F12 : android.view.KeyEvent.KEYCODE_F11;
        for (int i = 0; i < Math.min(64, Math.abs(steps)); ++i) sendKey(activity, key);
        return true;
    }

    private void useController() {
        if (!controllerNavigation) { controllerNavigation = true; publish(); }
    }

    private static void sendKey(android.app.Activity activity, int key) {
        long time = android.os.SystemClock.uptimeMillis();
        activity.dispatchKeyEvent(new android.view.KeyEvent(time, time, android.view.KeyEvent.ACTION_DOWN, key, 0));
        activity.dispatchKeyEvent(new android.view.KeyEvent(time, time, android.view.KeyEvent.ACTION_UP, key, 0));
    }

    public static boolean onKey(android.app.Activity activity, android.view.KeyEvent event) {
        if (current == null || current.activity != activity) return false;
        int key = event.getKeyCode();
        int translated;
        switch (key) {
            case android.view.KeyEvent.KEYCODE_SYSTEM_NAVIGATION_UP: translated = android.view.KeyEvent.KEYCODE_DPAD_UP; break;
            case android.view.KeyEvent.KEYCODE_SYSTEM_NAVIGATION_DOWN: translated = android.view.KeyEvent.KEYCODE_DPAD_DOWN; break;
            case android.view.KeyEvent.KEYCODE_SYSTEM_NAVIGATION_LEFT: translated = android.view.KeyEvent.KEYCODE_DPAD_LEFT; break;
            case android.view.KeyEvent.KEYCODE_SYSTEM_NAVIGATION_RIGHT: translated = android.view.KeyEvent.KEYCODE_DPAD_RIGHT; break;
            default:
                if (key >= android.view.KeyEvent.KEYCODE_DPAD_UP && key <= android.view.KeyEvent.KEYCODE_DPAD_CENTER)
                    current.useController();
                return false;
        }
        current.useController();
        activity.dispatchKeyEvent(new android.view.KeyEvent(event.getDownTime(), event.getEventTime(),
                event.getAction(), translated, event.getRepeatCount(), event.getMetaState(),
                event.getDeviceId(), event.getScanCode(), event.getFlags(), event.getSource()));
        return true;
    }

    public static void onTouch(android.app.Activity activity, android.view.MotionEvent event) {
        if (current != null && current.activity == activity
                && event.getActionMasked() == android.view.MotionEvent.ACTION_DOWN && current.controllerNavigation) {
            current.controllerNavigation = false;
            current.publish();
        }
    }

    private void close() {
        activity.getApplication().unregisterActivityLifecycleCallbacks(this);
        if (carService != null) {
            try { carService.close(); }
            catch (Exception error) { android.util.Log.w("PornFetchAutomotive", "Could not close vehicle service", error); }
        }
    }

    @Override public void onActivityResumed(android.app.Activity value) {
        if (value == activity) { foreground = true; publish(); }
    }
    @Override public void onActivityPaused(android.app.Activity value) {
        if (value == activity) { foreground = false; ++pauseGeneration; remainingRotation = 0; publish(); }
    }
    @Override public void onActivityDestroyed(android.app.Activity value) {
        if (value == activity) { close(); if (current == this) current = null; }
    }
    @Override public void onActivityCreated(android.app.Activity value, android.os.Bundle state) { }
    @Override public void onActivityStarted(android.app.Activity value) { }
    @Override public void onActivityStopped(android.app.Activity value) { }
    @Override public void onActivitySaveInstanceState(android.app.Activity value, android.os.Bundle state) { }
}
