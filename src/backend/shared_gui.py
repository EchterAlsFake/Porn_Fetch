import os
from pathlib import Path

os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Material")
os.environ.setdefault("QT_QUICK_CONTROLS_MATERIAL_THEME", "Dark")

from PySide6.QtGui import  QGuiApplication
from PySide6.QtQml import QQmlEngine, QQmlComponent
from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtCore import Signal, QObject, QCoreApplication, QUrl, QEventLoop, QThread, Qt, QMetaObject, Slot

_qml_engine = None
_dispatcher = None


def _get_qml_engine():
    global _qml_engine
    if _qml_engine is None:
        _qml_engine = QQmlEngine()
    return _qml_engine


class _PopupDispatcher(QObject):
    @Slot(str, str)
    def show_popup_slot(self, text: str, title: str):
        _show_qml_popup_impl(text, title)


def _get_dispatcher():
    global _dispatcher
    if _dispatcher is None:
        _dispatcher = _PopupDispatcher()
        app = QCoreApplication.instance()
        if app:
            _dispatcher.moveToThread(app.thread())
    return _dispatcher


def _fallback_popup(text: str, title: str):
    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setText(text)
    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.exec()


def _show_qml_popup_impl(text: str, title: str):
    app = QApplication.instance()
    if not app:
        return

    qml_file = Path(__file__).parent.parent / "frontend" / "UI" / "MessageBox.qml"
    if not qml_file.exists():
        _fallback_popup(text, title)
        return

    engine = _get_qml_engine()
    component = QQmlComponent(engine, QUrl.fromLocalFile(str(qml_file.resolve())))

    if component.isError():
        print(f"[shared_gui] QML Error loading MessageBox.qml: {component.errors()}")
        _fallback_popup(text, title)
        return

    obj = component.create()
    if not obj:
        _fallback_popup(text, title)
        return

    obj.setProperty("dialogTitle", str(title))
    obj.setProperty("messageText", str(text))

    # Center on active window or primary screen
    active_win = app.activeWindow()
    dw = obj.property("width") or 440
    dh = obj.property("height") or 220

    if active_win and active_win.isVisible():
        geo = active_win.geometry()
        cx = geo.x() + (geo.width() - dw) // 2
        cy = geo.y() + (geo.height() - dh) // 2
        obj.setProperty("x", max(0, cx))
        obj.setProperty("y", max(0, cy))
    else:
        screen = QGuiApplication.primaryScreen()
        if screen:
            geo = screen.geometry()
            cx = geo.x() + (geo.width() - dw) // 2
            cy = geo.y() + (geo.height() - dh) // 2
            obj.setProperty("x", max(0, cx))
            obj.setProperty("y", max(0, cy))

    loop = QEventLoop()
    obj.closed.connect(loop.quit)
    obj.show()
    obj.raise_()
    obj.requestActivate()
    loop.exec()
    obj.deleteLater()


def ui_popup(text, title="Notice"):
    """A styled QML UI popup for small messages and notifications to the user."""
    if text is None:
        text = ""
    else:
        text = str(text)

    if title is None or not isinstance(title, str):
        title = "Notice"

    app = QApplication.instance()
    if not app:
        print(f"[{title}] {text}")
        return

    if QThread.currentThread() == app.thread():
        _show_qml_popup_impl(text, title)
    else:
        dispatcher = _get_dispatcher()
        QMetaObject.invokeMethod(
            dispatcher,
            "show_popup_slot",
            Qt.ConnectionType.BlockingQueuedConnection,
            text,
            title
        )


def reset_pornfetch():
    # TODO
    ui_popup(QCoreApplication.translate("main", "Done! Please restart.", None))


def show_error(message):
    ui_popup(text=message, title="Error")


class Signals(QObject):
    """Signals for the Download class"""
    # Progress Signal
    total_progress = Signal(int) # Sets the current value for the progressbar
    total_progress_range = Signal(int) # Sets the maximum for the total progressbar
    progress_add_to_tree_widget = Signal(int, int)  # Tracks the number of videos
    # loaded and processed into the tree widget
    progress_video_range = Signal(int, int)         # video_id, total
    progress_video = Signal(int, int, int)          # video_id, pos, total
    progress_remux = Signal(int, int, int)          # video_id, pos, total   <-- NEW
    download_completed = Signal(int, dict)                # video_id

    error_signal = Signal(object)
    login_result = Signal(object)

    # Animations
    start_undefined_range = Signal()  # Starts the loading animation progressbar
    stop_undefined_range = Signal()  # Stops the loading animation progressbar

    # Operations / Reportings
    install_finished = Signal(object)  # Reports if the Porn Fetch installation was finished
    uninstall_finished = Signal(object)  # Reports if the Porn Fetch uninstallation was finished
    internet_check = Signal(object)  # Reports if the internet checks were successful
    update_check = Signal(bool, dict)
    result = Signal(dict)  # Reports the result of the internet checks if something went wrong
    clear_tree_widget_signal = Signal()  # A signal to clear the tree widget
    text_data_to_tree_widget = Signal(int)  # Sends the text data in the form of a dictionary to the main class
    progress_send_video = Signal(object,
                                 object)  # Sends the selected video objects from the tree widget to the main class
    tree_widget_finished = Signal()
    # to download them
    url_iterators = Signal(object, object)  # Sends the processed URLs from the file to Porn Fetch



def on_checkbox_clicked(checked: bool):
    if checked:
        debug_mode_warning()


def debug_mode_warning():
    text = QCoreApplication.translate("main",
"""
Debug mode is only intended for developing with Porn Fetch or for very specific error traceback. It will print a lot of things,
that are going on into your Terminal and will save VERY detailed log files that can contain sensitive information.

If you are using only the GUI this will not affect your user experience, but may slow down your system.""")
    ui_popup(text)


def available_title_formatting_options():
    text = QCoreApplication.translate("main",
"""
The following options are supported:

$title (The video Title) 
$video_id
$author
$length
$tags
$publish_date
$publish_dt
$video

Notice: Not every video supports all options. If something is not supported,
it will be skipped. 

The $publish_dt option supports a literal datetime object e.g.,: 
${publish_dt:%Y-%m-%d} → 2025-10-27

Same goes for length:
${length:0.0f}min → 12min

The $video references the literal video object class in the code, which allows
you to tweak it further e.g., for PornHub you can do:
${video.author.name}

Please note, that this is intended for advanced users. I will not show general
examples or ways to use all this. Please ask ChatGPT if you need further information.
""")
    ui_popup(text)
