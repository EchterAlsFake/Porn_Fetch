import QtQuick

WheelHandler {
    id: control

    required property var flickable
    property real wheelStep: 240
    property real minimumWheelMovement: 12
    property int animationDuration: 160
    property real destinationY: 0
    readonly property bool scrolling: active || scrollAnimation.running
    property var scrollAnimation: NumberAnimation {
        target: control.flickable
        property: "contentY"
        duration: control.animationDuration
        easing.type: Easing.OutCubic
    }

    target: null
    blocking: true

    // QtWayland can classify a physical mouse wheel as a touchpad.
    acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad

    function minimumY() {
        return flickable ? flickable.originY : 0
    }

    function maximumY() {
        if (!flickable)
            return 0
        var minimum = minimumY()
        return Math.max(minimum,
                        minimum + flickable.contentHeight - flickable.height)
    }

    function clampY(value) {
        return Math.max(minimumY(), Math.min(maximumY(), value))
    }

    onWheel: function(event) {
        if (!flickable || maximumY() <= minimumY()) {
            event.accepted = false
            return
        }

        var device = control.point.device
        var usePixelDelta = device
                && device.type === PointerDevice.TouchPad
                && event.pixelDelta.y !== 0
        var delta = usePixelDelta
                ? event.pixelDelta.y
                : event.angleDelta.y / 120 * control.wheelStep

        if (delta === 0) {
            event.accepted = false
            return
        }
        if (!usePixelDelta
                && Math.abs(delta) < control.minimumWheelMovement)
            delta = delta < 0
                    ? -control.minimumWheelMovement
                    : control.minimumWheelMovement

        var startingPoint = scrollAnimation.running
                ? control.destinationY
                : flickable.contentY
        control.destinationY = clampY(startingPoint - delta)

        scrollAnimation.stop()
        scrollAnimation.from = flickable.contentY
        scrollAnimation.to = control.destinationY
        scrollAnimation.start()
        event.accepted = true
    }
}
