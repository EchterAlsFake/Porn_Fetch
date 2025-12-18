# pornfetch_info_dialog.py
# Refactored info widget (PySide6): higher-contrast dark theme with violet accents,
# orange reserved for legal/disclaimer callouts, improved readability, and tighter layout.

from __future__ import annotations

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

# --- Typography (pt) ---
BASE_PT = 11.0
SMALL_PT = 10.0
HERO_PT = 18.0
SECTION_TITLE_PT = 12.5
CALLOUT_TITLE_PT = 12.0
LICENSE_PT = 12.5


def _open_url(url: str) -> None:
    QDesktopServices.openUrl(QUrl(url))


def _label(
    text: str,
    *,
    bold: bool = False,
    size_pt: float | None = None,
    color: str | None = None,
    rich: bool = True,
    selectable: bool = True,
    object_name: str | None = None,
) -> QLabel:
    """Create a QLabel with sane defaults (word-wrap, selectable text, link handling)."""
    lab = QLabel()
    if object_name:
        lab.setObjectName(object_name)

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

    lab.setOpenExternalLinks(False)  # open via linkActivated so it works everywhere consistently
    lab.linkActivated.connect(_open_url)

    f = lab.font()
    f.setPointSizeF(size_pt if size_pt is not None else BASE_PT)
    if bold:
        f.setWeight(QFont.Weight.DemiBold if hasattr(QFont, "Weight") else QFont.DemiBold)
    lab.setFont(f)

    if color:
        lab.setStyleSheet(f"color: {color};")
    return lab


class _Card(QFrame):
    """A rounded container with tight but comfortable padding."""

    def __init__(self, object_name: str, *, padding: int = 10, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

        l = QVBoxLayout(self)
        l.setContentsMargins(padding, padding, padding, padding)
        l.setSpacing(8)
        self._layout = l

    @property
    def layout_(self) -> QVBoxLayout:
        return self._layout


class _Section(QFrame):
    """Section with a title bar and body; keeps spacing tight to avoid wasted room."""

    def __init__(self, title: str, *, object_name: str = "SectionCard", parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName(object_name)
        self.setFrameShape(QFrame.Shape.NoFrame)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        bar = QFrame()
        bar.setObjectName("SectionTitleBar")
        bar_l = QHBoxLayout(bar)
        bar_l.setContentsMargins(10, 8, 10, 8)
        bar_l.setSpacing(8)
        bar_l.addWidget(_label(title, bold=True, size_pt=SECTION_TITLE_PT, rich=False, selectable=False), 1)
        outer.addWidget(bar)

        body = QWidget()
        body_l = QVBoxLayout(body)
        body_l.setContentsMargins(10, 8, 10, 10)
        body_l.setSpacing(9)
        outer.addWidget(body)

        self.body_layout = body_l


class PornFetchInfoWidget(QWidget):
    """
    A scrollable "info page" widget suitable for embedding in a QStackedWidget.

    Usage:
        page = PornFetchInfoWidget()
        stacked.addWidget(page)
    """

    def __init__(self, parent: QWidget | None = None, ui=None, initialize_porn_fetch=None):
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
        content.setObjectName("Content")
        scroll.setWidget(content)

        layout = QVBoxLayout(content)
        layout.setContentsMargins(8, 8, 8, 8)  # tight outer padding (no wasted margins)
        layout.setSpacing(10)

        # --- Header ---
        header = _Card("HeaderCard", padding=12)
        header.layout_.setSpacing(6)
        header.layout_.addWidget(_label("Welcome", bold=True, size_pt=HERO_PT, rich=False, selectable=False))

        header.layout_.addWidget(
            _label(
                "<div style='line-height:140%'>"
                "Please read the information below carefully. It explains the basics of "
                "<b>Porn Fetch</b>, paid features, data collection, supported features, and legal aspects."
                "</div>"
            )
        )
        layout.addWidget(header)

        # --- Important callout ---
        important = _Card("CalloutImportant", padding=10)
        important.layout_.setSpacing(6)
        important.layout_.addWidget(_label("Important", bold=True, size_pt=CALLOUT_TITLE_PT, color="#C4B5FD", rich=False, selectable=False))
        important.layout_.addWidget(
            _label(
                "<div style='line-height:145%'>"
                "The following information is <b>very important</b>, so please read through it. "
                "After reading, select your options below."
                "</div>"
            )
        )
        layout.addWidget(important)

        # --- 1) Data Collection ---
        s1 = _Section("1) Data Collection")
        s1.body_layout.addWidget(
            _label(
                "<div style='line-height:145%'>"
                "<b>Porn Fetch does NOT send any data to third-party services</b> unless you explicitly agree to it."
                "</div>"
            )
        )
        s1.body_layout.addWidget(
            _label(
                "<div style='line-height:145%'>"
                "Porn Fetch includes an <b>optional automatic error reporting</b> feature. "
                "If enabled, errors are sent to my own server (running 24/7 at home on Arch Linux)."
                "</div>"
            )
        )
        s1.body_layout.addWidget(_label("<b>Error logs include:</b>"))
        s1.body_layout.addWidget(self._bullets(["Python traceback", "Timestamp", "Porn Fetch version"]))
        s1.body_layout.addWidget(
            _label(
                "<div style='line-height:145%'>"
                "You can also send feedback directly using the same scheme. This is <b>completely optional</b> and "
                "has <b>no effect</b> on how you can use Porn Fetch. Sent error/feedback messages are deleted from my "
                "server with each new version release."
                "</div>"
            )
        )
        layout.addWidget(s1)

        # --- 2) Paid Features ---
        s2 = _Section("2) Paid Features", object_name="SectionCardPaid")
        s2.body_layout.addWidget(_label("Some features of Porn Fetch are <b>paid-only</b>, including:"))
        s2.body_layout.addWidget(
            self._bullets(
                [
                    "<b>1080p+</b> resolution for video downloading",
                    "<b>Simultaneous / parallel</b> downloads",
                    "<b>Proxy</b> support",
                ]
            )
        )
        s2.body_layout.addSpacing(2)

        # License callout (focus area)
        s2.body_layout.addWidget(self._license_callout())
        s2.body_layout.addWidget(
            _label(
                "<div style='line-height:145%'>"
                "Alternatively, you can contribute <b>code</b> or <b>translations</b> to Porn Fetch to get a license. "
                "You can also run Porn Fetch from source to unlock everything."
                "</div>"
            )
        )
        layout.addWidget(s2)

        # --- 3) Is it legal? ---
        s3 = _Section("3) Is it legal?")
        s3.body_layout.addWidget(
            _label(
                "<div style='line-height:145%'>"
                "Generally, <b>yes</b>—in terms of the law and DMCA it is legal, unless you download copyrighted content "
                "<b>and redistribute it</b> or use it commercially. If you only use the content for private purposes this is typically fine."
                "</div>"
            )
        )

        warning = _Card("CalloutWarning", padding=10)
        warning.layout_.setSpacing(6)
        warning.layout_.addWidget(
            _label("Terms of Service notice", bold=True, size_pt=CALLOUT_TITLE_PT, color="#FDBA74", rich=False, selectable=False)
        )
        warning.layout_.addWidget(
            _label(
                "<div style='line-height:150%'>"
                "Web scraping and automation may still violate website Terms of Service. Sites can ban accounts, block IPs, "
                "or (in rare cases) take legal action if you disrupt their services. This is <b>very unlikely</b> unless "
                "you download extreme volumes (e.g., 1000+ videos/day)."
                "</div>"
            )
        )
        s3.body_layout.addWidget(warning)
        layout.addWidget(s3)

        # --- 4) Supported Features ---
        s4 = _Section("4) Supported Features")
        s4.body_layout.addWidget(_label("Porn Fetch in general supports:"))
        s4.body_layout.addWidget(
            self._bullets(
                [
                    "Downloading videos",
                    "Downloading model / channel / creator accounts",
                    "Downloading playlists",
                    "Searching on websites",
                    "(Sometimes) specific website functions",
                ],
                rich=False,
            )
        )
        s4.body_layout.addWidget(
            _label(
                "<div style='line-height:145%'>"
                "For info dedicated to the actually supported sites, please click on the <b>Supported Websites</b> button "
                "after you have continued with this dialog."
                "</div>"
            )
        )
        layout.addWidget(s4)

        # --- 5) How it works ---
        s5 = _Section("5) How it works")
        s5.body_layout.addWidget(
            _label(
                "<div style='line-height:145%'>"
                "Porn Fetch uses <b>web scraping</b> to fetch videos and extract useful information from their HTML / JavaScript. "
                "That means Porn Fetch mimics your browser. This works great in most cases, but if the website changes something "
                "then it breaks functionality and I need to make an update."
                "</div>"
            )
        )
        s5.body_layout.addWidget(
            _label(
                "<div style='line-height:145%'>"
                "Porn Fetch explicitly ONLY works for the given supported list of websites. This is <b>NOT</b> a yt-dlp wrapper! "
                "After fetching a video the HLS URL that contains the segments is extracted and those are downloaded to your PC "
                "and converted into one file."
                "</div>"
            )
        )

        note = _Card("CalloutNote", padding=10)
        note.layout_.setSpacing(6)
        note.layout_.addWidget(_label("Note", bold=True, size_pt=CALLOUT_TITLE_PT, color="#E5E7EB", rich=False, selectable=False))
        note.layout_.addWidget(
            _label(
                "<div style='line-height:150%'>"
                "Porn Fetch is in no way a perfect software. Don't expect everything to work here all the time — "
                "I am working on this in my absolute free time after school."
                "</div>"
            )
        )
        s5.body_layout.addWidget(note)
        layout.addWidget(s5)

        footer = _label("Thanks for taking the time to read this.", rich=False, selectable=False, object_name="Footer")
        layout.addWidget(footer)

        self._apply_styles()

    # --- UI helpers ---

    def _bullets(self, items: list[str], *, rich: bool = True) -> QWidget:
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(6)

        for it in items:
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(8)

            dot = _label("•", rich=False, selectable=False, object_name="BulletDot")
            dot.setFixedWidth(14)

            txt = _label(f"<div style='line-height:140%'>{it}</div>" if rich else it, rich=rich)
            row.addWidget(dot, 0)
            row.addWidget(txt, 1)
            l.addLayout(row)

        return w

    def _license_callout(self) -> QWidget:
        card = _Card("LicenseCallout", padding=12)
        card.layout_.setSpacing(8)

        card.layout_.addWidget(
            _label("How to get a license", bold=True, size_pt=LICENSE_PT, rich=False, selectable=False)
        )

        # Build link with inline style to guarantee color + underline, regardless of platform theme.
        website = (
            '<a href="https://echteralsfake.me" '
            'style="color:#C4B5FD; text-decoration: underline; font-weight: 700;">'
            "https://echteralsfake.me"
            "</a>"
        )

        card.layout_.addWidget(
            _label(
                "<div style='line-height:150%'>"
                "<b>One-time purchase:</b> <span style='opacity:0.95'>5€</span> — "
                "unlimited activations, valid forever, offline activation."
                "</div>"
            )
        )

        card.layout_.addWidget(self._kv_table([
            ("Website", website),
            ("Cost", "<b>5€</b> (one-time purchase)"),
            ("Includes", "Unlimited activations, valid forever, offline activation"),
        ]))

        card.layout_.addWidget(
            _label(
                "<div style='line-height:150%'>"
                "If the link doesn't open, copy it and open it manually."
                "</div>",
                size_pt=SMALL_PT,
                object_name="SubtleHint",
            )
        )
        return card

    def _kv_table(self, rows: list[tuple[str, str]]) -> QWidget:
        frame = QFrame()
        frame.setObjectName("KVTable")

        grid = QGridLayout(frame)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)

        for r, (k, v) in enumerate(rows):
            k_lab = _label(k, rich=False, selectable=False, object_name="KVKey")
            v_lab = _label(v, rich=True, object_name="KVValue")
            v_lab.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
                | Qt.TextInteractionFlag.LinksAccessibleByMouse
            )
            v_lab.setOpenExternalLinks(False)
            v_lab.linkActivated.connect(_open_url)

            grid.addWidget(k_lab, r, 0)
            grid.addWidget(v_lab, r, 1)

        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        return frame

    # --- Theme ---

    def _apply_styles(self) -> None:
        # Palette targets:
        # - Violet/purple for primary accents
        # - Orange reserved for legal/disclaimer warnings
        self.setStyleSheet(r"""
        QWidget#PornFetchInfoRoot {
            background: #05040B;
            color: #F5F3FF;
            font-size: 11pt;
        }

        QScrollArea, QWidget#Content {
            background: transparent;
        }

        /* Common cards */
        QFrame#HeaderCard,
        QFrame#CalloutImportant,
        QFrame#CalloutNote,
        QFrame#CalloutWarning,
        QFrame#SectionCard,
        QFrame#SectionCardPaid,
        QFrame#LicenseCallout {
            border-radius: 14px;
        }

        /* Header: high contrast with subtle violet glow */
        QFrame#HeaderCard {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                        stop:0 #14062A, stop:1 #080B1A);
            border: 1px solid #6D28D9;
        }

        /* Important: violet accent */
        QFrame#CalloutImportant {
            background: #0E0A1D;
            border: 1px solid #8B5CF6;
            border-left: 6px solid #A78BFA;
        }

        /* Note: neutral */
        QFrame#CalloutNote {
            background: #0B1020;
            border: 1px solid #2A3558;
            border-left: 6px solid #A1A1AA;
        }

        /* Warning / legal disclaimer: ORANGE only */
        QFrame#CalloutWarning {
            background: #241206;
            border: 1px solid #FB923C;
            border-left: 6px solid #F97316;
        }

        /* Sections */
        QFrame#SectionCard {
            background: #090A14;
            border: 1px solid #2D2A45;
        }
        QFrame#SectionCardPaid {
            background: #090A14;
            border: 1px solid #8B5CF6;
        }

        QFrame#SectionTitleBar {
            background: #0D0B1A;
            border-top-left-radius: 14px;
            border-top-right-radius: 14px;
            border-bottom: 1px solid #2D2A45;
        }
        QFrame#SectionCardPaid QFrame#SectionTitleBar {
            background: #120828;
            border-bottom: 1px solid #6D28D9;
        }

        /* License focus area */
        QFrame#LicenseCallout {
            background: #120828;
            border: 1px solid #A78BFA;
            border-left: 6px solid #8B5CF6;
        }

        /* KV table in license */
        QFrame#KVTable {
            border: 1px solid #3B2E66;
            border-radius: 12px;
            background: #0B0A14;
        }
        QLabel#KVKey {
            background: #0E0B1E;
            color: #DDD6FE;
            padding: 10px 10px;
            border-right: 1px solid #3B2E66;
            font-weight: 600;
        }
        QLabel#KVValue {
            padding: 10px 10px;
            color: #F5F3FF;
        }

        /* Link color for rich text inside labels (best effort). Inline CSS in HTML ensures consistency. */
        QLabel#KVValue a { color: #C4B5FD; text-decoration: underline; }

        /* Bullets */
        QLabel#BulletDot {
            color: #A78BFA;
            font-size: 12pt;
        }

        /* Subtle hint text */
        QLabel#SubtleHint {
            color: #C7C3E6;
        }

        /* Footer */
        QLabel#Footer {
            color: #A1A1AA;
            font-size: 10pt;
            padding-top: 2px;
            padding-bottom: 4px;
        }

        /* Default label color (kept very bright for readability) */
        QLabel {
            color: #F5F3FF;
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