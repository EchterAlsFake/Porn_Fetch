pragma ComponentBehavior: Bound

import QtQuick

// The caller supplies activity; this visual never captures input.
Item {
    id: edge
    property bool active: false
    property bool animated: true
    property bool animationAllowed: true
    property color accentColor: "#6366f1"
    property real strength: 1
    property real glowWidth: 7.5
    property real lineWidth: 1
    property int pulseDuration: 2000
    property real cornerRadius: 0
    property var outline: ({})
    readonly property bool hasOutline: outline && outline.width > 0 && outline.height > 0
                                       && outline.corners && outline.corners.length === 4
    onOutlineChanged: outlineCanvas.requestPaint()
    onAccentColorChanged: outlineCanvas.requestPaint()
    onGlowWidthChanged: outlineCanvas.requestPaint()
    onLineWidthChanged: outlineCanvas.requestPaint()
    property real pulse: 0.35
    property bool showing: false

    clip: true
    opacity: showing ? 1 : 0
    visible: enabled && opacity > 0

    Behavior on opacity {
        NumberAnimation { duration: 240; easing.type: Easing.InOutSine }
    }

    onActiveChanged: {
        activationDelay.stop()
        if (active)
            activationDelay.start()
        else
            showing = false
    }
    Component.onCompleted: {
        if (active)
            activationDelay.start()
    }

    Timer {
        id: activationDelay
        interval: 280
        onTriggered: edge.showing = edge.active
    }

    SequentialAnimation on pulse {
        running: edge.animated && edge.animationAllowed && edge.visible
        loops: Animation.Infinite
        NumberAnimation {
            to: 1
            duration: edge.pulseDuration / 2
            easing.type: Easing.InOutSine
        }
        NumberAnimation {
            to: 0.35
            duration: edge.pulseDuration / 2
            easing.type: Easing.InOutSine
        }
    }

    // Keep 100–85% of the glow across the first 62.5%, then taper quickly
    // across the remaining width. Leave the halo translucent so nearby text
    // remains readable, even at the peak of the pulse.
    function glowOpacity(position: real): real {
        if (position <= 0.625)
            return 1 - 0.15 * position / 0.625
        const tail = (position - 0.625) / 0.375
        return 0.85 * Math.pow(Math.max(0, 1 - tail), 2)
    }

    Item {
        anchors.fill: parent
        opacity: Math.min(1, edge.strength * (edge.animated ? edge.pulse : 0.75))

        // Adjacent one-pixel strokes give a smooth profile in both themes.
        // Only opacity animates; no per-frame Canvas painting or blur textures.
        Repeater {
            model: edge.hasOutline ? 0 : Math.ceil(edge.glowWidth)
            Rectangle {
                required property int index
                anchors.fill: parent
                anchors.margins: index
                radius: Math.max(0, edge.cornerRadius - index)
                color: "transparent"
                border.width: 1
                border.color: edge.accentColor
                opacity: 0.65 * edge.glowOpacity(index / edge.glowWidth)
            }
        }

        Rectangle {
            anchors.fill: parent
            visible: !edge.hasOutline
            radius: edge.cornerRadius
            color: "transparent"
            border.width: edge.lineWidth
            border.color: edge.accentColor
        }

        Canvas {
            id: outlineCanvas
            anchors.fill: parent
            visible: edge.hasOutline
            onWidthChanged: requestPaint()
            onHeightChanged: requestPaint()
            onVisibleChanged: requestPaint()
            // Only geometry/color changes repaint; the parent animates opacity.
            onPaint: {
                var ctx = getContext("2d")
                ctx.reset()
                if (!edge.hasOutline || width <= 0 || height <= 0) return
                var sx = width / edge.outline.width
                var sy = height / edge.outline.height
                var scale = Math.min(sx, sy)
                var corners = edge.outline.corners.map(function(c) {
                    return { x: c.x * sx, y: c.y * sy, r: c.radius * scale }
                })
                function stroke(inset, opacity, thickness) {
                    ctx.beginPath()
                    for (var i = 0; i < 4; i++) {
                        var c = corners[i]
                        var r = Math.max(0, c.r - inset)
                        // Square fallback corners move inward with each stroke.
                        var x = c.r > 0 ? c.x : c.x + (i === 0 || i === 3 ? inset : -inset)
                        var y = c.r > 0 ? c.y : c.y + (i < 2 ? inset : -inset)
                        var angle = Math.PI + i * Math.PI / 2
                        var startX = x + r * Math.cos(angle)
                        var startY = y + r * Math.sin(angle)
                        if (i === 0) ctx.moveTo(startX, startY)
                        else ctx.lineTo(startX, startY)
                        if (r > 0) ctx.arc(x, y, r, angle, angle + Math.PI / 2)
                    }
                    ctx.closePath()
                    ctx.strokeStyle = edge.accentColor
                    ctx.globalAlpha = opacity
                    ctx.lineWidth = thickness
                    ctx.stroke()
                }
                for (var layer = 0; layer < Math.ceil(edge.glowWidth); layer++)
                    stroke(layer + 0.5, 0.65 * edge.glowOpacity(layer / edge.glowWidth), 1)
                stroke(edge.lineWidth / 2, 1, edge.lineWidth)
            }
        }
    }
}
