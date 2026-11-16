.pragma library

function move(item, forward) {
    var next = item.nextItemInFocusChain(forward)
    for (var count = 0; next && count < 300; ++count) {
        if (next.activeFocusOnTab && next.visible && next.enabled) {
            next.forceActiveFocus(Qt.TabFocusReason)
            return
        }
        next = next.nextItemInFocusChain(forward)
    }
}
