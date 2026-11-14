import QtQuick
import QtQuick.Controls

// A narrow, touch-only edge recognizer leaves ordinary content gestures alone.
Item {
    id: root
    property bool fromRight: true
    property color accentColor: systemPalette.highlight
    readonly property real distance: swipe.activeTranslation.x * (fromRight ? -1 : 1)
    readonly property real threshold: Math.min(96, parent.width * 0.25)
    signal backRequested()
    SystemPalette { id: systemPalette }
    width: 24

    DragHandler {
        id: swipe
        target: null
        acceptedDevices: PointerDevice.TouchScreen
        yAxis.enabled: false
        onGrabChanged: function(transition, point) {
            if (transition === PointerDevice.UngrabExclusive
                    && root.distance >= root.threshold
                    && Math.abs(centroid.position.y - centroid.pressPosition.y) < root.distance / 2)
                root.backRequested()
        }
    }

    Rectangle {
        visible: swipe.active && root.distance > 0
        width: 40
        height: 40
        radius: 20
        x: root.fromRight ? -Math.min(root.distance, 64) : Math.min(root.distance, 64)
        y: Math.max(0, Math.min(root.height - height, swipe.centroid.position.y - height / 2))
        color: root.accentColor
        opacity: Math.min(1, root.distance / root.threshold)
        Label {
            anchors.centerIn: parent
            text: "←"
            color: palette.highlightedText
            font.pixelSize: 24
        }
    }
}
