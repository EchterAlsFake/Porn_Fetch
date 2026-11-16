package org.kivy.android;

/** Loaded only on AAOS, using its optional public android.car shared library. */
public final class PornFetchCarService implements AutoCloseable {
    private final android.app.Activity activity;
    private android.car.Car car;
    private android.car.drivingstate.CarUxRestrictionsManager manager;
    private boolean closed;

    public PornFetchCarService(android.app.Activity activity) {
        this.activity = activity;
        if (android.os.Build.VERSION.SDK_INT >= 29) {
            car = android.car.Car.createCar(activity, null, android.car.Car.CAR_WAIT_TIMEOUT_DO_NOT_WAIT,
                    (connected, ready) -> {
                        if (closed) { connected.disconnect(); return; }
                        car = connected;
                        if (ready) connect();
                        else {
                            manager = null;
                            PornFetchAutomotive.restrictions(activity, false, true);
                        }
                    });
        } else {
            car = android.car.Car.createCar(activity, new android.content.ServiceConnection() {
                @Override public void onServiceConnected(android.content.ComponentName name, android.os.IBinder service) { connect(); }
                @Override public void onServiceDisconnected(android.content.ComponentName name) {
                    manager = null;
                    PornFetchAutomotive.restrictions(activity, false, true);
                }
            });
            car.connect();
        }
    }

    private void connect() {
        try {
            manager = (android.car.drivingstate.CarUxRestrictionsManager)
                    car.getCarManager(android.car.Car.CAR_UX_RESTRICTION_SERVICE);
            if (manager == null) throw new IllegalStateException("Vehicle UX restriction service unavailable");
            manager.registerListener(restrictions -> update(restrictions));
            update(manager.getCurrentCarUxRestrictions());
        } catch (RuntimeException error) {
            PornFetchAutomotive.restrictions(activity, false, true);
            android.util.Log.w("PornFetchAutomotive", "Could not read vehicle restrictions", error);
        }
    }

    private void update(android.car.drivingstate.CarUxRestrictions restrictions) {
        if (!closed) PornFetchAutomotive.restrictions(activity, restrictions != null,
                restrictions == null || restrictions.isRequiresDistractionOptimization());
    }

    @Override public void close() {
        closed = true;
        try {
            if (manager != null) manager.unregisterListener();
        } finally {
            if (car != null) car.disconnect();
        }
    }
}
