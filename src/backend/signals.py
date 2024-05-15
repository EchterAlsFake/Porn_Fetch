from PySide6.QtCore import QObject, Signal


class Signals(QObject):
    """Signals for the Download class"""
    # Progress Signals
    progress_single = Signal(int)
    completed = Signal()
    progress = Signal(int, int)
    progress_hqporner = Signal(int, int)
    progress_eporner = Signal(int, int)
    progress_xnxx = Signal(int, int)
    progress_xvideos = Signal(int, int)
    total_progress = Signal(int, int)
    progress_video = Signal(object)
    ffmpeg_progress = Signal(int, int)

    # Setup
    signal_setup_update = Signal(bool)
    signal_setup_internet = Signal(bool)

    # Ranges
    start_undefined_range = Signal()
    stop_undefined_range = Signal()
    data = Signal(list)

    # Other (I don't remember)
    text_data = Signal(list)

    # URL Thread
    url_iterators = Signal(list, list, list)

    # Operations
    finished = Signal()
    clear_signal = Signal()
    get_total = Signal(str, str)

    # Errors
    error_signal = Signal(str)