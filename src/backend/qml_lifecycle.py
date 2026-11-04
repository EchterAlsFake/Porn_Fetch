"""Destroy the QML interface before its Python context objects disappear."""
from PySide6.QtQml import QQmlApplicationEngine
from shiboken6 import delete, isValid


def destroy_qml_engine(engine: QQmlApplicationEngine) -> None:
    """Call after async shutdown, while context-property owners are still alive.

    Assigning None is insufficient: Qt adapters can retain the engine through
    Python reference cycles. Delete windows first so engine-owned backend
    objects cannot disappear underneath their QML bindings.
    """
    if not isValid(engine):
        return
    for root in engine.rootObjects():
        if isValid(root):
            delete(root)
    delete(engine)
