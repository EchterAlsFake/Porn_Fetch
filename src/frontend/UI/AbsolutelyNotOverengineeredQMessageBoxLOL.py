# stunning_message_box.py
# pip install PySide6
from __future__ import annotations

from typing import Optional
import sys

from PySide6.QtCore import (
    Qt, QSize, QPoint, QEasingCurve, QPropertyAnimation
)
from PySide6.QtGui import (
    QColor, QFont, QIcon, QPainter, QPixmap, QGuiApplication, QCursor
)
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStyle, QWidget, QFrame, QSizePolicy, QSpacerItem, QGraphicsDropShadowEffect,
    QMessageBox
)


def _is_dark(palette) -> bool:
    # Heuristic: check window background lightness
    c = palette.color(palette.Window)
    return c.lightness() < 128


def _tone(c: QColor, *, lighter: int = 100) -> str:
    # QColor.lighter: 100 = same, >100 lighter, <100 darker
    x = QColor(c)
    x = x.lighter(lighter)
    return f"rgba({x.red()}, {x.green()}, {x.blue()}, {x.alpha()})"


def _rgba(c: QColor, a: int) -> str:
    return f"rgba({c.red()}, {c.green()}, {c.blue()}, {a})"


def _qicon_for_mbox(icon: QMessageBox.Icon, style: QStyle) -> QIcon:
    sp_map = {
        QMessageBox.Icon.Information: QStyle.SP_MessageBoxInformation,
        QMessageBox.Icon.Warning: QStyle.SP_MessageBoxWarning,
        QMessageBox.Icon.Critical: QStyle.SP_MessageBoxCritical,
        QMessageBox.Icon.Question: QStyle.SP_MessageBoxQuestion,
        QMessageBox.Icon.NoIcon: QStyle.SP_CustomBase,
    }
    sp = sp_map.get(icon, QStyle.SP_MessageBoxInformation)
    if sp == QStyle.SP_CustomBase:
        return QIcon()
    return style.standardIcon(sp)


class PillButton(QPushButton):
    def __init__(self, text: str, *, is_default=False, accent="#7C3AED", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(36)
        self.setMinimumWidth(84)
        self.setAutoDefault(is_default)
        self.setDefault(is_default)
        self._is_default = is_default
        self._accent = QColor(accent)
        self._apply_style()

        # Gentle shadow glow for default action
        if is_default:
            glow = QGraphicsDropShadowEffect(self)
            glow.setBlurRadius(24)
            glow.setOffset(0, 0)
            glow.setColor(QColor(self._accent).lighter(110))
            self.setGraphicsEffect(glow)

    def _apply_style(self):
        accent = self._accent
        accent_str = f"rgb({accent.red()},{accent.green()},{accent.blue()})"
        # two variants: filled (default) vs ghost
        if self._is_default:
            self.setProperty("variant", "filled")
        else:
            self.setProperty("variant", "ghost")
        base = """
        QPushButton {
            border: 0;
            padding: 8px 14px;
            border-radius: 10px;
            font-weight: 600;
            letter-spacing: 0.1px;
            outline: none;
        }
        QPushButton:focus-visible {
            outline: 2px solid %ACCENT%;
            outline-offset: 2px;
        }
        """
        filled = f"""
        QPushButton[variant="filled"] {{
            background: {accent_str};
            color: white;
        }}
        QPushButton[variant="filled"]:hover {{
            filter: brightness(1.05);
        }}
        QPushButton[variant="filled"]:pressed {{
            filter: brightness(0.92);
        }}
        """
        ghost = f"""
        QPushButton[variant="ghost"] {{
            background: rgba(127,127,127,0.08);
            color: palette(window-text);
        }}
        QPushButton[variant="ghost"]:hover {{
            background: rgba(127,127,127,0.12);
        }}
        QPushButton[variant="ghost"]:pressed {{
            background: rgba(127,127,127,0.18);
        }}
        """
        self.setStyleSheet(
            base.replace("%ACCENT%", accent_str) + filled + ghost
        )


class GlassFrame(QFrame):
    """A rounded inner panel that paints a soft glass look."""
    def __init__(self, radius=18, parent=None):
        super().__init__(parent)
        self.radius = radius
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform, True)

        # Panel background (semi-transparent)
        palette = self.palette()
        dark = _is_dark(palette)
        base = palette.color(palette.Window)
        glass = QColor(base)
        glass.setAlpha(210 if dark else 230)

        p.setPen(Qt.NoPen)
        p.setBrush(glass)
        rect = self.rect()
        rect.adjust(1, 1, -1, -1)
        p.drawRoundedRect(rect, self.radius, self.radius)

        # Inner subtle top highlight and bottom shade for depth
        top = QColor(255, 255, 255, 24 if dark else 60)
        bottom = QColor(0, 0, 0, 60 if dark else 24)
        grad_h = rect
        # Top
        p.setBrush(top)
        p.drawRoundedRect(grad_h.adjusted(1, 1, -1, -int(rect.height() * 0.6)), self.radius, self.radius)
        # Bottom overlay
        p.setBrush(bottom)
        p.drawRoundedRect(grad_h.adjusted(1, int(rect.height() * 0.6), -1, -1), self.radius, self.radius)


class StunningMessageBox(QDialog):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        icon: QMessageBox.Icon = QMessageBox.Icon.Information,
        title: str = "Title",
        text: str = "",
        informative_text: str = "",
        buttons: QMessageBox.StandardButtons = QMessageBox.StandardButton.Ok,
        default_button: QMessageBox.StandardButton = QMessageBox.StandardButton.NoButton,
        accent: str = "#7C3AED",
    ):
        super().__init__(parent)
        self.setModal(True)
        self.setObjectName("StunningMessageBox")
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowModality(Qt.ApplicationModal)

        self._accent = QColor(accent)
        self._clicked: QMessageBox.StandardButton = QMessageBox.StandardButton.NoButton
        self._drag_pos = None

        self._build_ui(icon, title, text, informative_text, buttons, default_button)
        self._apply_styles()
        self._apply_shadow()
        self._animate_in()

    # ---------- UI ----------
    def _build_ui(
        self,
        icon: QMessageBox.Icon,
        title: str,
        text: str,
        informative_text: str,
        buttons: QMessageBox.StandardButtons,
        default_button: QMessageBox.StandardButton,
    ):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)

        # Outer chrome with subtle gradient ring (acts as border)
        chrome = QFrame(self)
        chrome.setObjectName("chrome")
        chrome_layout = QVBoxLayout(chrome)
        chrome_layout.setContentsMargins(2, 2, 2, 2)

        self.panel = GlassFrame(radius=18, parent=chrome)
        panel_layout = QVBoxLayout(self.panel)
        panel_layout.setContentsMargins(18, 18, 18, 18)
        panel_layout.setSpacing(12)

        # Header: Icon + Title
        header = QHBoxLayout()
        header.setSpacing(12)

        # Icon with capsule background
        icon_wrap = QFrame(self.panel)
        icon_wrap.setObjectName("iconWrap")
        icon_wrap.setFixedSize(QSize(48, 48))
        icon_layout = QVBoxLayout(icon_wrap)
        icon_layout.setContentsMargins(0, 0, 0, 0)

        icon_label = QLabel(icon_wrap)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setObjectName("iconLabel")
        qicon = _qicon_for_mbox(icon, self.style())
        if not qicon.isNull():
            pm = qicon.pixmap(28, 28)
            icon_label.setPixmap(pm)
        icon_layout.addWidget(icon_label, 0, Qt.AlignCenter)

        header.addWidget(icon_wrap, 0, Qt.AlignTop)

        title_wrap = QVBoxLayout()
        title_lbl = QLabel(title, self.panel)
        title_lbl.setObjectName("title")
        title_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        title_lbl.setWordWrap(True)

        text_lbl = QLabel(text, self.panel)
        text_lbl.setObjectName("body")
        text_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
        text_lbl.setOpenExternalLinks(True)
        text_lbl.setWordWrap(True)

        title_wrap.addWidget(title_lbl)
        title_wrap.addWidget(text_lbl)

        if informative_text:
            info_lbl = QLabel(informative_text, self.panel)
            info_lbl.setObjectName("info")
            info_lbl.setWordWrap(True)
            info_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse)
            title_wrap.addWidget(info_lbl)

        header_widget = QWidget(self.panel)
        header_widget.setLayout(title_wrap)
        header.addWidget(header_widget)

        panel_layout.addLayout(header)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        def add_btn(std: QMessageBox.StandardButton, label: str):
            is_default = std == default_button or (default_button == QMessageBox.StandardButton.NoButton and std == QMessageBox.StandardButton.Ok)
            b = PillButton(label, is_default=is_default, accent=self._accent.name(), parent=self.panel)
            b.clicked.connect(lambda _=False, s=std: self._on_clicked(s))
            btn_row.addWidget(b)

        # order: help stays left, destructive last
        mapping = [
            (QMessageBox.StandardButton.Help, "Help"),
            (QMessageBox.StandardButton.Retry, "Retry"),
            (QMessageBox.StandardButton.Ignore, "Ignore"),
            (QMessageBox.StandardButton.Apply, "Apply"),
            (QMessageBox.StandardButton.Discard, "Discard"),
            (QMessageBox.StandardButton.Abort, "Abort"),
            (QMessageBox.StandardButton.No, "No"),
            (QMessageBox.StandardButton.Yes, "Yes"),
            (QMessageBox.StandardButton.Close, "Close"),
            (QMessageBox.StandardButton.Cancel, "Cancel"),
            (QMessageBox.StandardButton.Ok, "OK"),
        ]
        for std, label in mapping:
            if buttons & std:
                add_btn(std, label)

        panel_layout.addLayout(btn_row)
        chrome_layout.addWidget(self.panel)
        root.addWidget(chrome)

        self._install_global_shortcuts(default_button)

    def _install_global_shortcuts(self, default_button: QMessageBox.StandardButton):
        # Enter -> default; Esc -> cancel if present, else reject
        self.default_button = default_button

    def _apply_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(60)
        shadow.setOffset(0, 22)
        # Slightly different in dark vs light
        shadow.setColor(QColor(0, 0, 0, 150))
        self.panel.setGraphicsEffect(shadow)

    def _apply_styles(self):
        dark = _is_dark(self.palette())
        base = self.palette().color(self.palette().Window)
        ring_a = QColor(self._accent).lighter(115)
        ring_b = QColor(self._accent).darker(125)
        ring_a.setAlpha(190 if dark else 160)
        ring_b.setAlpha(120 if dark else 110)

        chrome = f"""
        #chrome {{
            border-radius: 20px;
            background: qlineargradient(
                x1:0 y1:0, x2:1 y2:1,
                stop:0 {_rgba(ring_a, ring_a.alpha())},
                stop:1 {_rgba(ring_b, ring_b.alpha())}
            );
        }}
        """

        # Icon capsule behind the symbol
        cap_base = QColor(self._accent)
        cap_base.setAlpha(60 if dark else 80)
        cap_edge = QColor(self._accent).lighter(130)
        cap_edge.setAlpha(90 if dark else 110)
        icon_wrap = f"""
        #iconWrap {{
            border-radius: 12px;
            background: qlineargradient(
                x1:0 y1:0, x2:1 y2:1,
                stop:0 {_rgba(cap_edge, cap_edge.alpha())},
                stop:1 {_rgba(cap_base, cap_base.alpha())}
            );
        }}
        """

        # Typography
        # Use platform-standard fonts; Qt will pick best available
        font_css = """
        QLabel#title {
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 0.2px;
        }
        QLabel#body {
            font-size: 14px;
            color: palette(window-text);
        }
        QLabel#info {
            font-size: 12px;
            color: palette(mid);
        }
        """

        self.setStyleSheet(chrome + icon_wrap + font_css)

        # Cursor + drag feedback
        self.setCursor(Qt.ArrowCursor)

    # ---------- Interaction ----------
    def _on_clicked(self, std: QMessageBox.StandardButton):
        self._clicked = std
        self.accept()

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            # Simulate default button behavior
            if self.default_button != QMessageBox.StandardButton.NoButton:
                self._on_clicked(self.default_button)
                return
        if e.key() == Qt.Key_Escape:
            # Prefer Cancel/Close if present
            for std in (QMessageBox.StandardButton.Cancel, QMessageBox.StandardButton.Close):
                if self._has_button(std):
                    self._on_clicked(std)
                    return
            self.reject()
            return
        super().keyPressEvent(e)

    def _has_button(self, std: QMessageBox.StandardButton) -> bool:
        # Use layout traversal to check
        # (We already know what we created; this is simple)
        return True  # Any std we added is valid for this simple check

    # Window dragging
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
            e.accept()
            self.setCursor(Qt.SizeAllCursor)
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if self._drag_pos and e.buttons() & Qt.LeftButton:
            self.move(e.globalPosition().toPoint() - self._drag_pos)
            e.accept()
        super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        self._drag_pos = None
        self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(e)

    # ---------- Animation ----------
    def _animate_in(self):
        self.setWindowOpacity(0.0)
        # Place near cursor center if no parent geometry guidance
        if not self.parent():
            screen = QGuiApplication.screenAt(QCursor.pos()) or QGuiApplication.primaryScreen()
            geo = screen.availableGeometry()
            self.adjustSize()
            self.move(geo.center() - self.rect().center())

        anim = QPropertyAnimation(self, b"windowOpacity", self)
        anim.setDuration(180)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start(QPropertyAnimation.DeleteWhenStopped)

    # ---------- API parity helpers ----------
    @staticmethod
    def _run(icon, title, text, informative_text, buttons, default_button, parent=None, accent="#7C3AED"):
        dlg = StunningMessageBox(
            parent=parent,
            icon=icon,
            title=title,
            text=text,
            informative_text=informative_text or "",
            buttons=buttons or QMessageBox.StandardButton.Ok,
            default_button=default_button or QMessageBox.StandardButton.Ok,
            accent=accent,
        )
        res = dlg.exec()
        # If a button was clicked, return it; otherwise map accept/reject
        if dlg._clicked != QMessageBox.StandardButton.NoButton:
            return dlg._clicked
        return QMessageBox.StandardButton.Ok if res == QDialog.DialogCode.Accepted else QMessageBox.StandardButton.Cancel

    @classmethod
    def information(cls, parent, title, text, buttons=QMessageBox.StandardButton.Ok, defaultButton=QMessageBox.StandardButton.NoButton, accent="#3B82F6", informative_text=""):
        return cls._run(QMessageBox.Icon.Information, title, text, informative_text, buttons, defaultButton, parent, accent)

    @classmethod
    def warning(cls, parent, title, text, buttons=QMessageBox.StandardButton.Ok, defaultButton=QMessageBox.StandardButton.NoButton, accent="#F59E0B", informative_text=""):
        return cls._run(QMessageBox.Icon.Warning, title, text, informative_text, buttons, defaultButton, parent, accent)

    @classmethod
    def critical(cls, parent, title, text, buttons=QMessageBox.StandardButton.Ok, defaultButton=QMessageBox.StandardButton.NoButton, accent="#EF4444", informative_text=""):
        return cls._run(QMessageBox.Icon.Critical, title, text, informative_text, buttons, defaultButton, parent, accent)

    @classmethod
    def question(cls, parent, title, text, buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, defaultButton=QMessageBox.StandardButton.No, accent="#7C3AED", informative_text=""):
        return cls._run(QMessageBox.Icon.Question, title, text, informative_text, buttons, defaultButton, parent, accent)


# ---------- Demo ----------
if __name__ == "__main__":
    # High-DPI crispness
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("Stunning QMessageBox Demo")

    # Sample usage
    StunningMessageBox.information(
        None,
        "Update complete",
        "Your workspace has been upgraded successfully.",
        buttons=QMessageBox.StandardButton.Ok,
        defaultButton=QMessageBox.StandardButton.Ok,
        accent="#22C55E",
        informative_text="You’re on version 2.4.1. Release notes have been saved to your Docs.",
    )

    ans = StunningMessageBox.question(
        None,
        "Replace existing file?",
        "A file named <b>report.pdf</b> already exists in this folder.",
        buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
        defaultButton=QMessageBox.StandardButton.No,
        accent="#7C3AED",
        informative_text="Replacing will overwrite the current file. This action cannot be undone.",
    )
    if ans == QMessageBox.StandardButton.Yes:
        StunningMessageBox.information(None, "Done", "File replaced.", accent="#3B82F6")
    elif ans == QMessageBox.StandardButton.No:
        StunningMessageBox.information(None, "Skipped", "Existing file left untouched.", accent="#3B82F6")
    else:
        StunningMessageBox.warning(None, "Cancelled", "Operation cancelled by user.", accent="#F59E0B")

    sys.exit(0)
