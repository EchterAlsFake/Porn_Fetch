from PySide6.QtGui import QFontMetrics
from PySide6.QtCore import Qt, QObject, QEvent, QTimer
from PySide6.QtWidgets import QAbstractScrollArea, QApplication, QStyle

POPUP_PAD = 6          # must match QComboBoxPrivateContainer padding in QSS
ITEM_PAD_X = 8         # must match your item padding left/right (6px 8px -> 8)
EXTRA_TEXT_GAP = 10    # small safety cushion

def _longest_item_width_px(combo):
    fm = QFontMetrics(combo.font())
    style = combo.style()

    max_text = 0
    icon_w = 0

    for i in range(combo.count()):
        text = combo.itemText(i) or ""
        max_text = max(max_text, fm.horizontalAdvance(text))

        icon = combo.itemIcon(i)
        if not icon.isNull():
            icon_w = max(icon_w, combo.iconSize().width())

    # If items are checkable, reserve indicator space (safe to always add a little)
    indicator = style.pixelMetric(QStyle.PixelMetric.PM_IndicatorWidth, None, combo)
    indicator_spacing = 6

    # text + optional icon + indicator + paddings + small cushion
    w = max_text
    if icon_w:
        w += icon_w + 6  # icon-text spacing
    w += indicator + indicator_spacing
    w += ITEM_PAD_X * 2
    w += EXTRA_TEXT_GAP

    return w

def fit_combo_popup(combo):
    view = combo.view()
    rows = combo.count()
    if rows == 0:
        return

    visible = min(rows, combo.maxVisibleItems())

    view.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
    view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    view.setTextElideMode(Qt.TextElideMode.ElideNone)  # important: don't elide while sizing
    view.doItemsLayout()

    # ----- WIDTH (from model text) -----
    w = _longest_item_width_px(combo)

    # add view frame + popup padding
    w += view.frameWidth() * 2
    w += POPUP_PAD * 2

    # add scrollbar width if it will show
    if rows > visible:
        w += view.verticalScrollBar().sizeHint().width()

    # never smaller than the combobox itself
    w = max(w, combo.width())

    # optionally cap to screen so it doesn't get forced smaller by Qt
    screen = combo.screen() or QApplication.primaryScreen()
    if screen:
        max_w = screen.availableGeometry().width() - 20
        w = min(w, max_w)

    # ----- HEIGHT (only what’s needed) -----
    h = 0
    for i in range(visible):
        h += view.sizeHintForRow(i)
    h += max(0, visible - 1) * view.spacing()
    h += view.frameWidth() * 2
    h += POPUP_PAD * 2

    # size the popup window (container), not just the view
    popup = view.window()  # QComboBoxPrivateContainer
    popup.setFixedSize(int(w), int(h))


class ComboPopupFitter(QObject):
    def eventFilter(self, obj, event):
        if event.type() in (QEvent.Type.MouseButtonPress, QEvent.Type.KeyPress):
            # run right AFTER Qt opens the popup and applies layouts
            QTimer.singleShot(0, lambda o=obj: fit_combo_popup(o))
        return super().eventFilter(obj, event)