# pornfetch_info_widget.py
# Drop-in QWidget for a QStackedWidget: native layout, no QTextBrowser.

from __future__ import annotations

# Works with PySide6 / PyQt6 / PyQt5
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QDesktopServices
from PySide6.QtWidgets import (
    QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QSizePolicy, QGridLayout, QApplication
)


def _label(
    text: str,
    *,
    bold: bool = False,
    size_pt: float | None = None,
    color: str | None = None,
    rich: bool = True,
    selectable: bool = True,
) -> QLabel:
    lab = QLabel()
    lab.setWordWrap(True)
    lab.setTextFormat(Qt.TextFormat.RichText if rich else Qt.TextFormat.PlainText)
    lab.setText(text)
    if selectable:
        lab.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
            | Qt.TextInteractionFlag.LinksAccessibleByMouse
        )
    else:
        lab.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)

    lab.setOpenExternalLinks(False)  # we handle via linkActivated for consistency

    f = lab.font()
    if bold:
        f.setWeight(QFont.Weight.DemiBold if hasattr(QFont, "Weight") else QFont.DemiBold)
    if size_pt is not None:
        f.setPointSizeF(size_pt)
    lab.setFont(f)

    if color:
        lab.setStyleSheet(f"color: {color};")

    lab.linkActivated.connect(lambda url: QDesktopServices.openUrl(QUrl(url)))
    return lab


class _Card(QFrame):
    def __init__(self, object_name: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(14, 14, 14, 14)
        self._layout.setSpacing(10)

    @property
    def layout_(self) -> QVBoxLayout:
        return self._layout


class _Section(QFrame):
    def __init__(self, title: str, object_name: str = "SectionCard", parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setFrameShape(QFrame.Shape.NoFrame)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Title bar
        bar = QFrame()
        bar.setObjectName("SectionTitleBar")
        bar_l = QVBoxLayout(bar)
        bar_l.setContentsMargins(12, 10, 12, 10)
        bar_l.addWidget(_label(title, bold=True, size_pt=12.0, rich=False, selectable=False))
        outer.addWidget(bar)

        # Body
        body = QWidget()
        body_l = QVBoxLayout(body)
        body_l.setContentsMargins(12, 10, 12, 12)
        body_l.setSpacing(8)
        outer.addWidget(body)

        self.body_layout = body_l


class PornFetchInfoWidget(QWidget):
    """
    A scrollable "info page" widget suitable for embedding in a QStackedWidget.

    Usage:
        page = PornFetchInfoWidget()
        stacked.addWidget(page)
    """

    def __init__(self, parent: QWidget | None = None, ui = None, initialize_porn_fetch = None):
        super().__init__(parent)

        self.setObjectName("PornFetchInfoRoot")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        root.addWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)

        layout = QVBoxLayout(content)
        layout.setSpacing(12)

        # Main container card (white)
        main = _Card("MainCard")
        layout.addWidget(main)

        # Header (dark)
        header = _Card("HeaderCard")
        header.layout_.setContentsMargins(14, 14, 14, 14)
        header.layout_.setSpacing(6)
        header.layout_.addWidget(_label("Welcome", bold=True, size_pt=16.0, color="#ffffff", rich=False, selectable=False))
        header.layout_.addWidget(
            _label(
                "Please read the information below carefully. It explains the basics of "
                "<b>Porn Fetch</b>, paid features, data collection, supported features, and legal aspects.",
                color="#ffffff",
            )
        )
        main.layout_.addWidget(header)

        # Important callout
        important = _Card("CalloutImportant")
        important.layout_.setContentsMargins(12, 10, 12, 10)
        important.layout_.setSpacing(6)
        important.layout_.addWidget(_label("Important", bold=True, color="#1d4ed8", rich=False, selectable=False))
        important.layout_.addWidget(
            _label(
                "The following information is <b>very important</b>, so please read through it. "
                "After reading, select your options below."
            )
        )
        main.layout_.addWidget(important)

        # --- 1) Data Collection ---
        s1 = _Section("1) Data Collection")
        s1.body_layout.addWidget(_label("<b>Porn Fetch does NOT send any data to third-party services</b> unless you explicitly agree to it."))
        s1.body_layout.addWidget(
            _label(
                "Porn Fetch includes an <b>optional automatic error reporting</b> feature. "
                "If enabled, errors are sent to my own server (running 24/7 at home on Arch Linux)."
            )
        )
        s1.body_layout.addWidget(_label("<b>Error logs include:</b>", rich=True))
        s1.body_layout.addWidget(self._bullets([
            "Python traceback",
            "Timestamp",
            "Porn Fetch version",
        ]))
        s1.body_layout.addWidget(
            _label(
                "You can also send feedback directly using the same scheme. This is <b>completely optional</b> and "
                "has <b>no effect</b> on how you can use Porn Fetch. Sent error/feedback messages are deleted from my "
                "server with each new version release."
            )
        )
        main.layout_.addWidget(s1)

        # --- 2) Paid Features ---
        s2 = _Section("2) Paid Features", object_name="SectionCardPaid")
        s2.body_layout.addWidget(_label("Some features of Porn Fetch are <b>paid-only</b>, including:"))
        s2.body_layout.addWidget(self._bullets([
            "<b>1080p+</b> resolution for video downloading",
            "<b>Simultaneous / parallel</b> downloads",
            "<b>Proxy</b> support",
        ]))
        s2.body_layout.addSpacing(6)
        s2.body_layout.addWidget(_label("<b>How to get a license</b>", rich=True))

        s2.body_layout.addWidget(self._kv_table([
            ("Website", '<a href="https://echteralsfake.me"><b>https://echteralsfake.me</b></a>'),
            ("Cost", "<b>5€</b> (one-time purchase)"),
            ("Includes", "Unlimited activations, valid forever, offline activation"),
        ]))

        s2.body_layout.addWidget(
            _label(
                "Alternatively, you can contribute <b>code</b> or <b>translations</b> to Porn Fetch to get a license. "
                "You can also run Porn Fetch from source to unlock everything."
            )
        )
        main.layout_.addWidget(s2)

        # --- 3) Is it legal? ---
        s3 = _Section("3) Is it legal?")
        s3.body_layout.addWidget(
            _label(
                "Generally, <b>yes</b>—in terms of the law and DMCA it is legal, unless you download copyrighted content "
                "<b>and redistribute it</b> or use it commercially. If you only use the content for private purposes this is typically fine."
            )
        )

        warning = _Card("CalloutWarning")
        warning.layout_.setContentsMargins(12, 10, 12, 10)
        warning.layout_.setSpacing(6)
        warning.layout_.addWidget(_label("Terms of Service notice", bold=True, color="#9a3412", rich=False, selectable=False))
        warning.layout_.addWidget(
            _label(
                "Web scraping and automation may still violate website Terms of Service. Sites can ban accounts, block IPs, "
                "or (in rare cases) take legal action if you disrupt their services. This is <b>very unlikely</b> unless "
                "you download extreme volumes (e.g., 1000+ videos/day)."
            )
        )
        s3.body_layout.addWidget(warning)
        main.layout_.addWidget(s3)

        # --- 4) Supported Features ---
        s4 = _Section("4) Supported Features")
        s4.body_layout.addWidget(_label("Porn Fetch in general supports:"))
        s4.body_layout.addWidget(self._bullets([
            "Downloading videos",
            "Downloading model / channel / creator accounts",
            "Downloading playlists",
            "Searching on websites",
            "(Sometimes) specific website functions",
        ], rich=False))
        s4.body_layout.addWidget(
            _label(
                "For info dedicated to the actually supported sites, please click on the <b>Supported Websites</b> button "
                "after you have continued with this dialog."
            )
        )
        main.layout_.addWidget(s4)

        # --- 5) How it works ---
        s5 = _Section("5) How it works")
        s5.body_layout.addWidget(
            _label(
                "Porn Fetch uses <b>web scraping</b> to fetch videos and extract useful information from their HTML / JavaScript. "
                "That means Porn Fetch mimics your browser. This works great in most cases, but if the website changes something "
                "then it breaks functionality and I need to make an update."
            )
        )
        s5.body_layout.addWidget(
            _label(
                "Porn Fetch explicitly ONLY works for the given supported list of websites. This is <b>NOT</b> a yt-dlp wrapper! "
                "After fetching a video the HLS URL that contains the segments is extracted and those are downloaded to your PC "
                "and converted into one file."
            )
        )

        note = _Card("CalloutNote")
        note.layout_.setContentsMargins(12, 10, 12, 10)
        note.layout_.setSpacing(6)
        note.layout_.addWidget(_label("Note", bold=True, rich=False, selectable=False))
        note.layout_.addWidget(
            _label(
                "Porn Fetch is in no way a perfect software. Don't expect everything to work here all the time — "
                "I am working on this in my absolute free time after school."
            )
        )
        s5.body_layout.addWidget(note)
        main.layout_.addWidget(s5)

        # Footer
        footer = _label("Thanks for taking the time to read this.", rich=False, selectable=False)
        footer.setStyleSheet("color:#6b7280; font-size:9.5pt;")
        main.layout_.addWidget(footer)

        # Let main card stop stretching weirdly
        layout.addStretch(1)

        self._apply_styles()

    def _bullets(self, items: list[str], rich: bool = True) -> QWidget:
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(4)
        for it in items:
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(8)
            dot = _label("•", rich=False, selectable=False)
            dot.setStyleSheet("color:#e5e7eb;")
            dot.setFixedWidth(12)
            txt = _label(it, rich=rich)
            row.addWidget(dot, 0)
            row.addWidget(txt, 1)
            l.addLayout(row)
        return w

    def _kv_table(self, rows: list[tuple[str, str]]) -> QWidget:
        frame = QFrame()
        frame.setObjectName("KVTable")
        grid = QGridLayout(frame)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)

        for r, (k, v) in enumerate(rows):
            k_lab = _label(k, rich=False, selectable=False)
            k_lab.setObjectName("KVKey")
            v_lab = _label(v, rich=True)
            v_lab.setObjectName("KVValue")

            grid.addWidget(k_lab, r, 0)
            grid.addWidget(v_lab, r, 1)

        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        return frame

    def _apply_styles(self) -> None:
        self.setStyleSheet("""
        QWidget#PornFetchInfoRoot {
            background: transparent;
        }

        QScrollArea {
            background: transparent;
        }

        /* Outer card */
        QFrame#MainCard {
            background: #0b1220;
            border: 1px solid #334155;
            border-radius: 14px;
        }

        /* Top header */
        QFrame#HeaderCard {
            background: #020617;
            border: 1px solid #0f172a;
            border-radius: 12px;
        }

        /* Callouts */
        QFrame#CalloutImportant {
            background: #0b1b3a;
            border: 1px solid #1d4ed8;
            border-left: 6px solid #3b82f6;
            border-radius: 12px;
        }

        QFrame#CalloutWarning {
            background: #2a1405;
            border: 1px solid #f97316;
            border-left: 6px solid #fb923c;
            border-radius: 12px;
        }

        QFrame#CalloutNote {
            background: #0f172a;
            border: 1px solid #334155;
            border-left: 6px solid #94a3b8;
            border-radius: 12px;
        }

        /* Sections */
        QFrame#SectionCard, QFrame#SectionCardPaid {
            background: #0b1220;
            border: 1px solid #334155;
            border-radius: 12px;
        }

        QFrame#SectionCardPaid {
            border: 1px solid #7c5e12; /* warm border */
        }

        QFrame#SectionTitleBar {
            background: #111827;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
        }

        /* Paid section title bar */
        QFrame#SectionCardPaid QFrame#SectionTitleBar {
            background: #1b1407;
        }

        /* KV table */
        QFrame#KVTable {
            border: 1px solid #334155;
            border-radius: 10px;
            background: #0b1220;
        }
        QLabel#KVKey {
            background: #111827;
            color: #94a3b8;
            padding: 8px 10px;
            border-right: 1px solid #334155;
        }
        QLabel#KVValue {
            padding: 8px 10px;
            color: #e5e7eb;
        }

        /* Default text */
        QLabel {
            color: #e5e7eb;
        }
        """)


# --- Minimal demo (optional) ---
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = PornFetchInfoWidget()
    w.resize(820, 720)
    w.show()
    sys.exit(app.exec())
