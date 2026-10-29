import QtQuick
import QtQuick.Controls

Dialog {
    id: dialog
    property alias message: messageLabel.text
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
    onAboutToShow: measureText()

    contentItem: SmoothScrollView {
        id: messageScroll
        objectName: "messageScroll"
        clip: true
        // Reserve the scrollbar gutter so wrapping does not change its visibility
        // and feed back into the dialog's preferred height.
        rightPadding: ScrollBar.vertical.width + 6
        implicitWidth: dialog.availableWidth
        implicitHeight: dialog.preferredTextHeight

        Label {
            id: messageLabel
            objectName: "messageLabel"
            width: Math.max(1, dialog.availableWidth - messageScroll.leftPadding - messageScroll.rightPadding)
            font: dialog.font
            textFormat: Text.PlainText
            wrapMode: Text.Wrap
            // Defer measurement until wrapping has settled, avoiding a sizing
            // cycle between the popup, its viewport and the wrapped label.
            onImplicitHeightChanged: Qt.callLater(dialog.measureText)
        }
    }
}
