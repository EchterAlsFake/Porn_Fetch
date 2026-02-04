from PySide6.QtGui import QFontMetrics
from PySide6.QtCore import Qt, QObject, QEvent, QTimer
from PySide6.QtWidgets import QAbstractScrollArea, QApplication, QStyle, QComboBox, QListView

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


FREE_MAX_HEIGHT = 720                 # your free ceiling
LOCKED_LABELS = {"best", "half", "worst"}  # match your current “0..2 locked” behavior


def make_quality_combobox(
    available_heights: list[int],
    preferred_quality: str | int,
    has_license: bool
) -> QComboBox:
    """
    Creates a row combobox:
      - fills it with Worst/Half/Best + concrete heights (e.g. 360p, 720p...)
      - disables locked entries if no license
      - selects preferred quality (fallback to nearest available that respects license)
    """
    combo = QComboBox()
    combo.setView(QListView())  # you said this fixed styling -> keep it
    combo.setProperty("pfRole", "quality")  # optional: lets you target in QSS if you want

    # Normalize & sort heights (worst->best)
    heights = sorted({int(h) for h in (available_heights or []) if h is not None})

    # 1) Add auto labels first (same as settings)
    combo.addItem("Best", "best")
    combo.addItem("Half", "half")
    combo.addItem("Worst", "worst")

    # 2) Add numeric heights (I usually show best first, but keep whatever you prefer)
    for h in reversed(heights):  # best -> worst
        combo.addItem(f"{h}p", h)

    # 3) Apply license restrictions (disable items by userData)
    apply_license_state_quality_combo(combo, has_license)

    # 4) Pick default selection based on preferred quality, respecting license + availability
    selected_value = _choose_default_quality_value(
        preferred_quality=preferred_quality,
        heights=heights,
        has_license=has_license
    )
    _set_combo_to_value_first_enabled(combo, selected_value)

    return combo


def apply_license_state_quality_combo(combo: QComboBox, has_license: bool) -> None:
    """
    Disable items that require license:
      - labels in LOCKED_LABELS
      - numeric heights > FREE_MAX_HEIGHT
    """
    model = combo.model()
    for i in range(combo.count()):
        val = combo.itemData(i)

        needs_license = False
        if isinstance(val, str) and val.lower() in LOCKED_LABELS:
            needs_license = True
        elif isinstance(val, int) and val > FREE_MAX_HEIGHT:
            needs_license = True

        enabled = has_license or (not needs_license)
        item = model.item(i)
        if item:
            flags = item.flags()
            if enabled:
                item.setFlags(flags | Qt.ItemFlag.ItemIsEnabled)
            else:
                item.setFlags(flags & ~Qt.ItemFlag.ItemIsEnabled)

    # If current selection is disabled, move to first enabled
    cur_item = model.item(combo.currentIndex())
    if cur_item and not (cur_item.flags() & Qt.ItemFlag.ItemIsEnabled):
        for i in range(combo.count()):
            it = model.item(i)
            if it and (it.flags() & Qt.ItemFlag.ItemIsEnabled):
                combo.setCurrentIndex(i)
                break



def _set_combo_to_value_first_enabled(combo: QComboBox, desired_value):
    # Try exact match
    idx = combo.findData(desired_value)
    if idx != -1:
        item = combo.model().item(idx)
        if item and (item.flags() & Qt.ItemFlag.ItemIsEnabled):
            combo.setCurrentIndex(idx)
            return

    # Otherwise pick first enabled
    for i in range(combo.count()):
        it = combo.model().item(i)
        if it and (it.flags() & Qt.ItemFlag.ItemIsEnabled):
            combo.setCurrentIndex(i)
            return

def _choose_default_quality_value(preferred_quality, heights: list[int], has_license: bool):
    # If unlicensed, force preference down to 720 (same behavior you already have)
    if not has_license:
        if isinstance(preferred_quality, str) and preferred_quality.lower() in LOCKED_LABELS:
            preferred_quality = FREE_MAX_HEIGHT
        if isinstance(preferred_quality, int) and preferred_quality > FREE_MAX_HEIGHT:
            preferred_quality = FREE_MAX_HEIGHT

    # If preference is a label and allowed, keep it (it may pick best/half/worst later)
    if isinstance(preferred_quality, str):
        q = preferred_quality.strip().lower()
        if q in {"best", "half", "worst"}:
            return q

    # Numeric preference: choose closest available height (prefer <= target)
    try:
        target = int(preferred_quality)
    except Exception:
        target = FREE_MAX_HEIGHT

    if not heights:
        return target

    # highest <= target else closest
    below = [h for h in heights if h <= target]
    if below:
        return below[-1]
    return min(heights, key=lambda h: (abs(h - target), -h))
