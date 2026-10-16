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
            model: Math.ceil(edge.glowWidth)
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
            radius: edge.cornerRadius
            color: "transparent"
            border.width: edge.lineWidth
            border.color: edge.accentColor
        }
    }
}
