import QtQuick
import QtQuick.Controls

Dialog {
    id: dialog
    ContrastPopupBackground { popup: dialog }
    property alias message: messageLabel.text
    property var previousFocus: null
    property real preferredTextHeight: 0
    parent: Overlay.overlay
    anchors.centerIn: parent
    width: Math.min(560, (parent ? parent.width : 592) - 32)
    height: Math.min(implicitHeight, (parent ? parent.height : 600) - 32)
    focus: true
    standardButtons: Dialog.Ok
    closePolicy: Popup.CloseOnEscape

    function measureText() {
        preferredTextHeight = messageLabel.implicitHeight
    }
    onAboutToShow: {
        previousFocus = dialog.parent && dialog.parent.Window.window ? dialog.parent.Window.window.activeFocusItem : null
        measureText()
    }
    onClosed: {
        var item = previousFocus
        Qt.callLater(function() {
            if (item) {
                // Qt may already have restored focus with OtherFocusReason.
                // Re-enter it so the keyboard focus indicator remains visible.
                item.focus = false
                item.forceActiveFocus(Qt.TabFocusReason)
            }
        })
    }
    onOpened: messageLabel.forceActiveFocus()

    footer: DialogButtonBox {
        standardButtons: dialog.standardButtons
        onAccepted: dialog.accept()
        onRejected: dialog.reject()
        AppButton {
            id: copyButton
            property bool copied: false
            text: copied ? qsTr("Copied") : qsTr("Copy text")
            Accessible.name: qsTr("Copy text")
            implicitHeight: 48
            DialogButtonBox.buttonRole: DialogButtonBox.HelpRole
            onClicked: {
                messageLabel.selectAll()
                messageLabel.copy()
                messageLabel.deselect()
                copied = true
                copiedTimer.restart()
                messageLabel.Accessible.announce(qsTr("Copied to clipboard."), Accessible.Polite)
            }
            Timer { id: copiedTimer; interval: 3000; onTriggered: copyButton.copied = false }
        }
    }

    contentItem: SmoothScrollView {
        id: messageScroll
        objectName: "messageScroll"
        clip: true
        contentWidth: availableWidth
        ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
        // Reserve the scrollbar gutter so wrapping does not change its visibility
        // and feed back into the dialog's preferred height.
        rightPadding: ScrollBar.vertical.width + 6
        implicitWidth: dialog.availableWidth
        implicitHeight: dialog.preferredTextHeight

        TextArea {
            id: messageLabel
            objectName: "messageLabel"
            width: Math.max(1, dialog.availableWidth - messageScroll.leftPadding - messageScroll.rightPadding)
            font: dialog.font
            padding: 0
            background: null
            readOnly: true
            selectByMouse: true
            Accessible.name: dialog.title
            textFormat: Text.PlainText
            wrapMode: Text.Wrap
            // Defer measurement until wrapping has settled, avoiding a sizing
            // cycle between the popup, its viewport and the wrapped label.
            onImplicitHeightChanged: Qt.callLater(dialog.measureText)
        }
    }
}
