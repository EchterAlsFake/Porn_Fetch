import QtQuick
import QtQuick.Controls
import QtQuick.Templates as T

// A fallback for keys left unhandled by native controls and page-specific paths.
// Keep text editing, sliders, spin boxes and open combo boxes in charge of their keys.
Item {
    id: remote
    required property var targetWindow
    signal navigationKeyRequested(int key)
    property bool automaticFocus: false
    property bool suspended: false
    property var lastFocus: null
    property var lastScope: null
    property var returnFocus: []
    property var activePopup: null
    property var closingPopup: null
    property var closingFocus: null
    property var editingItem: null
    property bool editorBackHeld: false
    readonly property var overlay: targetWindow.Overlay.overlay
    parent: overlay
    anchors.fill: parent
    z: 10000

    function usable(item) {
        return item && item.visible && item.enabled && item.width > 0 && item.height > 0
    }

    function flickable(item) {
        return item && typeof item.contentY === "number" && item.contentItem
            && typeof item.contentHeight === "number"
    }

    function adjustable(item) { return item instanceof T.Slider || item instanceof T.SpinBox }

    function textEditor(item) { return item instanceof T.TextField || item instanceof T.TextArea }

    function controlFor(item) {
        // Editable SpinBox controls give focus to an internal TextInput. Treat
        // that editor as part of the SpinBox for form navigation and outlining.
        for (var ancestor = item; ancestor; ancestor = ancestor.parent) {
            if (adjustable(ancestor) || textEditor(ancestor) || ancestor instanceof T.ComboBox
                || ancestor instanceof T.AbstractButton) return ancestor
        }
        return item
    }

    function scopeFor(item) {
        var child = item
        while (child && child.parent && child.parent !== overlay) child = child.parent
        return child && child.parent === overlay && child !== remote ? child : targetWindow.contentItem
    }

    function controls(scope) {
        var result = []
        function visit(item) {
            if (!usable(item) || item === remote) return
            // Scroll bars and internal editor handles are operated through their control.
            if (item instanceof T.ScrollBar) return
            var before = result.length
            if (item.activeFocusOnTab) result.push(item)
            if (adjustable(item) || textEditor(item) || item instanceof T.ComboBox) return
            for (var i = 0; i < item.children.length; ++i) visit(item.children[i])
            // A read-only list or document still needs a remote scrolling target.
            if (result.length === before && flickable(item) && item.contentHeight > item.height)
                result.push(item)
        }
        visit(scope)
        return result
    }

    function reveal(item) {
        if (!usable(item)) return
        for (var ancestor = item.parent; ancestor; ancestor = ancestor.parent) {
            if (!flickable(ancestor)) continue
            var point = item.mapToItem(ancestor.contentItem, 0, 0)
            var top = ancestor.contentY
            if (point.y < top) top = point.y - 8
            else if (point.y + item.height > top + ancestor.height)
                top = point.y + Math.min(item.height, ancestor.height) - ancestor.height + 8
            ancestor.contentY = Math.max(ancestor.originY || 0,
                Math.min(top, (ancestor.originY || 0) + Math.max(0, ancestor.contentHeight - ancestor.height)))
        }
    }

    function focusControl(item, reason) {
        if (!usable(item)) return
        item.forceActiveFocus(reason === undefined ? Qt.TabFocusReason : reason)
        reveal(item)
    }

    function center(item, scope) {
        for (var ancestor = item.parent; ancestor; ancestor = ancestor.parent) {
            if (flickable(ancestor) && item.height > ancestor.height) {
                var point = item.mapToItem(ancestor, item.width / 2, 0)
                return ancestor.mapToItem(scope, point.x,
                    (Math.max(0, point.y) + Math.min(ancestor.height, point.y + item.height)) / 2)
            }
        }
        return item.mapToItem(scope, item.width / 2, item.height / 2)
    }

    function visibleHeight(item) {
        for (var ancestor = item.parent; ancestor; ancestor = ancestor.parent)
            if (flickable(ancestor)) return Math.min(item.height, ancestor.height)
        return item.height
    }

    function updateFocus() {
        if (suspended || closingPopup) return
        var item = controlFor(targetWindow.activeFocusItem)
        if (editingItem !== item) editingItem = null
        var scope = scopeFor(item)
        if (lastScope && scope !== lastScope) {
            var saved = returnFocus.length ? returnFocus[returnFocus.length - 1] : null
            if (saved && scope === saved.scope) {
                returnFocus = returnFocus.slice(0, -1)
                lastScope = scope
                if (usable(saved.item)) { focusControl(saved.item); return }
            } else if (scope !== targetWindow.contentItem) {
                returnFocus = returnFocus.concat([{scope: lastScope, item: lastFocus,
                    reason: lastFocus ? lastFocus.focusReason : Qt.OtherFocusReason}])
            }
        }
        lastScope = scope
        activePopup = scope !== targetWindow.contentItem ? popupFor(scope, targetWindow.contentItem) : null
        if (item && (item.activeFocusOnTab || flickable(item))) {
            lastFocus = item
            reveal(item)
        } else if (automaticFocus && usable(scope)) {
            var items = controls(scope)
            if (items.length) focusControl(items[0])
        }
    }

    function move(key) {
        var current = controlFor(targetWindow.activeFocusItem)
        var scope = scopeFor(current)
        var items = controls(scope)
        if (!items.length) return false
        if (!current || items.indexOf(current) < 0) { focusControl(items[0]); return true }
        var vertical = key === Qt.Key_Up || key === Qt.Key_Down
        var positive = key === Qt.Key_Down || key === Qt.Key_Right
        var from = center(current, scope)
        var best = null
        var score = Infinity
        var scroll = flickable(current) ? current : current.parent
        while (scroll && !flickable(scroll)) scroll = scroll.parent
        function inside(item, ancestor) {
            for (; item; item = item.parent) if (item === ancestor) return true
            return false
        }
        var scrollingCandidate = null
        var scrollingScore = Infinity
        for (var i = 0; i < items.length; ++i) {
            var candidate = items[i]
            if (candidate === current) continue
            var to = center(candidate, scope)
            var along = vertical ? to.y - from.y : to.x - from.x
            var across = Math.abs(vertical ? to.x - from.x : to.y - from.y)
            if ((positive ? along : -along) <= 1) continue
            // Prefer controls in the same row/column, then the nearest neighbor.
            var beam = vertical ? (current.width + candidate.width) / 2 : (visibleHeight(current) + visibleHeight(candidate)) / 2
            var cost = Math.abs(along) + across * 0.25 + (across > beam ? 10000 : 0)
            if (cost < score) { score = cost; best = candidate }
            if (scroll && inside(candidate, scroll) && cost < scrollingScore) {
                scrollingScore = cost
                scrollingCandidate = candidate
            }
        }
        // Lists create delegates lazily. Scroll to instantiate the next rows before
        // allowing Down/Up to leave the list for a header or navigation rail.
        if (vertical && scroll) {
            if (scrollingCandidate) best = scrollingCandidate
            else {
                var previousY = scroll.contentY
                var origin = scroll.originY || 0
                scroll.contentY = Math.max(origin, Math.min(origin + Math.max(0, scroll.contentHeight - scroll.height),
                    previousY + (positive ? 1 : -1) * scroll.height * 0.7))
                if (Math.abs(previousY - scroll.contentY) > 1) {
                    Qt.callLater(function() {
                        var visible = controls(scroll).filter(function(control) {
                            var point = control.mapToItem(scroll, 0, 0)
                            return point.y >= 0 && point.y + control.height <= scroll.height
                        })
                        if (visible.length) focusControl(visible[positive ? 0 : visible.length - 1])
                    })
                    return true
                }
            }
        }
        if (best) { focusControl(best); return true }
        return false
    }

    function rotate(direction) {
        if (suspended) return false
        var current = controlFor(targetWindow.activeFocusItem)
        if (current instanceof T.ComboBox && current.popup.visible) {
            // Qt can keep focus on the ComboBox while its popup is open. Use
            // native highlight/selection rather than navigating the page beneath it.
            navigationKeyRequested(direction > 0 ? Qt.Key_Down : Qt.Key_Up)
            return true
        }
        if (editingItem === current) {
            if (adjustable(current)) {
                var previous = current.value
                if (direction > 0) current.increase()
                else current.decrease()
                if (current.value !== previous) {
                    if (current instanceof T.Slider) current.moved()
                    else current.valueModified()
                }
            }
            // The vehicle's IME owns rotary text entry; do not move out of its field.
            return true
        }
        if (textEditor(current) && current.readOnly) {
            var reader = current.parent
            while (reader && !flickable(reader)) reader = reader.parent
            if (reader) {
                var previousY = reader.contentY
                var origin = reader.originY || 0
                reader.contentY = Math.max(origin, Math.min(origin + Math.max(0, reader.contentHeight - reader.height),
                    previousY + direction * 72))
                if (Math.abs(reader.contentY - previousY) > 1) return true
            }
        }
        var items = controls(scopeFor(current))
        if (!items.length) return false
        var index = items.indexOf(current)
        var next = index < 0 ? items[0] : items[index + direction]
        var scroll = current ? current.parent : null
        while (scroll && !flickable(scroll)) scroll = scroll.parent
        if (scroll) {
            var ancestor = next
            while (ancestor && ancestor !== scroll) ancestor = ancestor.parent
            if (!ancestor && (direction > 0 ? !scroll.atYEnd : !scroll.atYBeginning))
                return move(direction > 0 ? Qt.Key_Down : Qt.Key_Up)
        }
        if (next) focusControl(next)
        return true
    }

    function popupFor(scope, item) {
        if (!item || item === remote) return null
        if (item instanceof T.Popup) {
            if (scopeFor(item.contentItem) === scope) return item
            return popupFor(scope, item.contentItem)
        }
        var objects = item.data || item.children || []
        for (var i = 0; i < objects.length; ++i) {
            var found = popupFor(scope, objects[i])
            if (found) return found
        }
        return null
    }

    function released(event) {
        if (suspended || event.key !== Qt.Key_Back) return
        var scope = scopeFor(targetWindow.activeFocusItem)
        if (scope === targetWindow.contentItem) return
        // Android Back and desktop Escape must obey the same popup close policy.
        var popup = popupFor(scope, targetWindow.contentItem)
        event.accepted = true
        if (!event.isAutoRepeat && popup && (popup.closePolicy & T.Popup.CloseOnEscape)) {
            if (popup instanceof T.Dialog) popup.reject()
            else popup.close()
        }
    }

    function pressed(event) {
        if (suspended || event.modifiers & (Qt.ControlModifier | Qt.AltModifier | Qt.MetaModifier)) return
        if (event.key === Qt.Key_F11 || event.key === Qt.Key_F12) {
            event.accepted = rotate(event.key === Qt.Key_F11 ? 1 : -1)
        } else if ([Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right].indexOf(event.key) >= 0) {
            event.accepted = move(event.key)
        } else if ([Qt.Key_Return, Qt.Key_Enter, Qt.Key_Select].indexOf(event.key) >= 0) {
            var item = targetWindow.activeFocusItem
            if (item instanceof T.ComboBox) {
                item.popup.open()
                event.accepted = true
            } else if (item instanceof T.AbstractButton) {
                if (!event.isAutoRepeat) item.click()
                event.accepted = true
            } else if (item && typeof item.readOnly === "boolean" && !item.readOnly) {
                Qt.inputMethod.show()
                event.accepted = true
            }
        }
    }

    function editorPressed(event) {
        if (suspended || event.modifiers & (Qt.ControlModifier | Qt.AltModifier | Qt.MetaModifier)) return
        var item = controlFor(targetWindow.activeFocusItem)
        if (item.readOnly) {
            if (event.key === Qt.Key_Up || event.key === Qt.Key_Down) {
                var scroll = item.parent
                while (scroll && !flickable(scroll)) scroll = scroll.parent
                if (scroll) {
                    var previous = scroll.contentY
                    var origin = scroll.originY || 0
                    scroll.contentY = Math.max(origin, Math.min(origin + Math.max(0, scroll.contentHeight - scroll.height),
                        previous + (event.key === Qt.Key_Up ? -72 : 72)))
                    if (Math.abs(scroll.contentY - previous) > 1) { event.accepted = true; return }
                }
            }
            if ([Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right, Qt.Key_Select, Qt.Key_Enter, Qt.Key_Return].indexOf(event.key) >= 0) {
                move(event.key === Qt.Key_Select || event.key === Qt.Key_Enter || event.key === Qt.Key_Return ? Qt.Key_Right : event.key)
                event.accepted = true
            }
            return
        }
        if (event.key === Qt.Key_Back || event.key === Qt.Key_Escape) {
            if (editingItem === item) {
                editingItem = null
                editorBackHeld = true
                if (textEditor(item) || (item instanceof T.SpinBox && item.editable)) Qt.inputMethod.hide()
                event.accepted = true
            }
        } else if (editingItem !== item) {
            if ([Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right].indexOf(event.key) >= 0) {
                // Before center activation, a remote traverses fields rather than
                // moving an invisible text cursor or getting trapped in a TextArea.
                move(event.key)
                event.accepted = true
            } else if ([Qt.Key_Return, Qt.Key_Enter, Qt.Key_Select].indexOf(event.key) >= 0) {
                editingItem = item
                if (textEditor(item) || (item instanceof T.SpinBox && item.editable)) Qt.inputMethod.show()
                event.accepted = true
            } else if (event.text.length) editingItem = item
        }
    }

    Connections {
        target: remote.targetWindow.contentItem.Keys
        function onPressed(event) { remote.pressed(event) }
    }
    Connections {
        target: remote.overlay.Keys
        function onPressed(event) { remote.pressed(event) }
    }
    Connections {
        target: remote.scopeFor(remote.targetWindow.activeFocusItem) !== remote.targetWindow.contentItem
            ? remote.scopeFor(remote.targetWindow.activeFocusItem).Keys : null
        function onPressed(event) { remote.pressed(event) }
        function onReleased(event) { remote.released(event) }
    }
    Connections {
        target: remote.targetWindow
        function onActiveFocusItemChanged() {
            if (remote.targetWindow.activeFocusItem && remote.targetWindow.activeFocusItem.activeFocusOnTab)
                remote.updateFocus()
            else Qt.callLater(remote.updateFocus)
        }
    }
    Connections {
        target: remote.automaticFocus && remote.targetWindow.activeFocusItem
            && (remote.textEditor(remote.targetWindow.activeFocusItem) || remote.adjustable(remote.controlFor(remote.targetWindow.activeFocusItem)))
            ? remote.targetWindow.activeFocusItem.Keys : null
        function onPressed(event) { remote.editorPressed(event) }
        function onReleased(event) {
            if (remote.editorBackHeld && (event.key === Qt.Key_Back || event.key === Qt.Key_Escape)) {
                remote.editorBackHeld = false
                event.accepted = true
            }
        }
    }
    Connections {
        target: remote.activePopup
        function onAboutToHide() {
            remote.closingPopup = remote.activePopup
            remote.closingFocus = remote.returnFocus.length ? remote.returnFocus[remote.returnFocus.length - 1] : null
        }
    }
    Connections {
        target: remote.closingPopup
        function onClosed() {
            var saved = remote.closingFocus
            remote.closingPopup = null
            remote.closingFocus = null
            if (saved) {
                remote.returnFocus = remote.returnFocus.slice(0, -1)
                remote.lastScope = saved.scope
                remote.lastFocus = saved.item
                if (remote.usable(saved.item)) remote.focusControl(saved.item, remote.automaticFocus ? Qt.TabFocusReason : saved.reason)
            }
            Qt.callLater(remote.updateFocus)
        }
    }
    onSuspendedChanged: if (!suspended && automaticFocus) Qt.callLater(updateFocus)
    onAutomaticFocusChanged: if (automaticFocus && !suspended) Qt.callLater(updateFocus)

    // Independent of a control's custom background, including delegates and drawers.
    Rectangle {
        id: outline
        objectName: "remoteFocusOutline"
        readonly property var item: remote.controlFor(remote.targetWindow.activeFocusItem)
        parent: item || remote
        visible: !remote.suspended && remote.usable(item) && (item.activeFocusOnTab || remote.flickable(item))
            && (remote.automaticFocus || item.focusReason === Qt.TabFocusReason || item.focusReason === Qt.BacktabFocusReason
                || item.focusReason === Qt.ShortcutFocusReason)
        anchors.fill: parent
        z: 10000
        radius: 6
        color: "transparent"
        border.width: 3
        border.color: Theme.accent
    }

    Label {
        readonly property var item: remote.controlFor(remote.targetWindow.activeFocusItem)
        visible: !remote.suspended && remote.automaticFocus && remote.usable(item)
            && (remote.textEditor(item) && !item.readOnly || remote.adjustable(item))
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 24
        width: Math.min(implicitWidth, parent.width - 48)
        padding: 12
        wrapMode: Text.WordWrap
        horizontalAlignment: Text.AlignHCenter
        color: Theme.ink
        text: remote.adjustable(item)
            ? (remote.editingItem === item ? qsTr("Use the arrows to adjust. Press Back when finished.") : qsTr("Press center to adjust. Use the arrows to move between controls."))
            : (remote.editingItem === item ? qsTr("Press Back to finish editing.") : qsTr("Press center to edit. Use the arrows to move between controls."))
        background: Rectangle { color: Theme.surface; border.color: Theme.outline; radius: 8 }
    }
}
