import QtQuick
import QtQuick.Controls

ScrollView {
    id: control
    contentWidth: availableWidth
    rightPadding: ScrollBar.vertical.visible ? ScrollBar.vertical.width + 6 : 0

    property alias wheelStep: wheelHandler.wheelStep
    property alias wheelAnimationDuration: wheelHandler.animationDuration

    SmoothWheelHandler {
        id: wheelHandler
        flickable: control.contentItem
    }

    ScrollBar.vertical: ScrollBar {
        parent: control
        anchors.top: control.top
        anchors.bottom: control.bottom
        anchors.right: control.right
        orientation: Qt.Vertical
        policy: ScrollBar.AsNeeded
        active: size < 1.0 || hovered || pressed || wheelHandler.scrolling
    }
}
