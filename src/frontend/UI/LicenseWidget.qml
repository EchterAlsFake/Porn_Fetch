// LicenseWidget.qml — Hyper-modern license panel
// Matches the Porn Fetch dark theme (#1f1f21 base, #3b82f6 accent)
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs
import Qt5Compat.GraphicalEffects

Item {
    id: root
    implicitWidth: 460
    implicitHeight: card.implicitHeight + 48

    // ── Colour tokens ──────────────────────────────────────────────
    readonly property color bgBase:     "#1f1f21"
    readonly property color bgCard:     "#262628"
    readonly property color bgInput:    "#2a2b2e"
    readonly property color border:     "#333437"
    readonly property color textPri:    "#EAEAEA"
    readonly property color textSec:    "#9B9CA1"
    readonly property color accent:     "#3b82f6"
    readonly property color accentGlow: "#5b9bff"
    readonly property color success:    "#22c55e"
    readonly property color danger:     "#ef4444"

    // ── The bridge is injected via rootContext().setContextProperty() ─
    // Do NOT declare `property QtObject bridge` here — it would shadow
    // the context property and stay null.

    // ── Toast feedback ─────────────────────────────────────────────
    Connections {
        target: bridge
        function onImportFinished(ok, msg) {
            toast.isSuccess = ok
            toast.text      = msg
            toastAnim.restart()
        }
    }

    // ── Native file dialog (lives in QML, avoids QWidgets conflicts) ─
    FileDialog {
        id: fileDialog
        title: "Select license file"
        nameFilters: ["License files (*.license)", "All files (*)"]
        onAccepted: {
            console.log("[LicenseWidget] FileDialog accepted, selectedFile:", fileDialog.selectedFile)
            console.log("[LicenseWidget] bridge:", bridge)
            if (bridge) {
                bridge.installFromPath(fileDialog.selectedFile)
            } else {
                console.log("[LicenseWidget] ERROR: bridge is null!")
            }
        }
    }

    // ── Background fill ────────────────────────────────────────────
    Rectangle { anchors.fill: parent; color: bgBase }

    // ─── CARD ──────────────────────────────────────────────────────
    Rectangle {
        id: card
        anchors.centerIn: parent
        width: Math.min(root.width - 48, 420)
        implicitHeight: col.implicitHeight + 64
        radius: 20
        color: bgCard
        border.color: bridge && bridge.isValid ? Qt.rgba(success.r, success.g, success.b, 0.35)
                                               : Qt.rgba(border.r, border.g, border.b, 1)
        border.width: 1

        // subtle inner shadow
        layer.enabled: true
        layer.effect: DropShadow {
            transparentBorder: true
            radius: 32; samples: 65
            color: bridge && bridge.isValid ? Qt.rgba(success.r, success.g, success.b, 0.10)
                                            : Qt.rgba(0, 0, 0, 0.55)
            verticalOffset: 8
        }

        // ── Animated glow ring when valid ──────────────────────────
        Rectangle {
            id: glowRing
            anchors.fill: parent
            anchors.margins: -2
            radius: parent.radius + 2
            color: "transparent"
            border.width: 2
            border.color: bridge && bridge.isValid
                          ? Qt.rgba(success.r, success.g, success.b, glowRing.pulse)
                          : "transparent"
            property real pulse: 0.0
            visible: bridge && bridge.isValid

            SequentialAnimation on pulse {
                loops: Animation.Infinite
                NumberAnimation { to: 0.6;  duration: 1800; easing.type: Easing.InOutSine }
                NumberAnimation { to: 0.15; duration: 1800; easing.type: Easing.InOutSine }
            }
        }

        ColumnLayout {
            id: col
            anchors {
                fill: parent
                margins: 32
            }
            spacing: 24

            // ── Status icon + heading ──────────────────────────────
            ColumnLayout {
                Layout.alignment: Qt.AlignHCenter
                spacing: 12

                // Animated status badge
                Rectangle {
                    id: badge
                    Layout.alignment: Qt.AlignHCenter
                    width: 72; height: 72
                    radius: 36
                    color: bridge && bridge.isValid
                           ? Qt.rgba(success.r, success.g, success.b, 0.12)
                           : Qt.rgba(danger.r, danger.g, danger.b, 0.10)
                    border.width: 1.5
                    border.color: bridge && bridge.isValid
                                  ? Qt.rgba(success.r, success.g, success.b, 0.30)
                                  : Qt.rgba(danger.r, danger.g, danger.b, 0.25)

                    // scale-pop on change
                    Behavior on border.color { ColorAnimation { duration: 400 } }
                    scale: 1.0
                    Behavior on scale { NumberAnimation { duration: 300; easing.type: Easing.OutBack } }

                    Text {
                        anchors.centerIn: parent
                        text: bridge && bridge.isValid ? "✓" : "✕"
                        font.pixelSize: 32
                        font.weight: Font.Bold
                        color: bridge && bridge.isValid ? success : danger
                        Behavior on color { ColorAnimation { duration: 350 } }
                    }

                    // trigger pop on status change
                    Connections {
                        target: bridge
                        function onStatusChanged() { badge.scale = 0.85; badge.scale = 1.0 }
                    }
                }

                Text {
                    Layout.alignment: Qt.AlignHCenter
                    text: bridge && bridge.isValid ? "License Active" : "No Valid License"
                    font.pixelSize: 20
                    font.weight: Font.DemiBold
                    font.letterSpacing: 0.4
                    color: textPri

                    Behavior on text {
                        SequentialAnimation {
                            NumberAnimation { target: headingFade; property: "opacity"; to: 0; duration: 120 }
                            PropertyAction  {}
                            NumberAnimation { target: headingFade; property: "opacity"; to: 1; duration: 200 }
                        }
                    }
                    id: headingFade
                }

                Text {
                    Layout.alignment: Qt.AlignHCenter
                    text: bridge ? bridge.reason : ""
                    font.pixelSize: 13
                    color: textSec
                    horizontalAlignment: Text.AlignHCenter
                    wrapMode: Text.WordWrap
                    Layout.maximumWidth: card.width - 80
                }
            }

            // ── Separator ──────────────────────────────────────────
            Rectangle {
                Layout.fillWidth: true
                height: 1
                color: border
                opacity: 0.6
            }

            // ── License key display (when valid) ───────────────────
            Rectangle {
                Layout.fillWidth: true
                visible: bridge && bridge.isValid && bridge.licenseKey !== ""
                height: visible ? keyCol.implicitHeight + 24 : 0
                radius: 12
                color: bgInput
                border.color: border
                border.width: 1

                Behavior on height { NumberAnimation { duration: 250; easing.type: Easing.OutCubic } }

                ColumnLayout {
                    id: keyCol
                    anchors {
                        fill: parent
                        margins: 12
                    }
                    spacing: 6

                    Text {
                        text: "LICENSE KEY"
                        font.pixelSize: 10
                        font.weight: Font.Bold
                        font.letterSpacing: 1.6
                        color: textSec
                    }

                    Text {
                        text: bridge ? bridge.licenseKey : ""
                        font.pixelSize: 13
                        font.family: "monospace"
                        color: accent
                        wrapMode: Text.WrapAnywhere
                        Layout.fillWidth: true
                    }
                }
            }

            // ── Feature pills (when valid) ─────────────────────────
            Flow {
                Layout.fillWidth: true
                spacing: 8
                visible: bridge && bridge.isValid && bridge.features.length > 0

                Repeater {
                    model: bridge ? bridge.features : []

                    Rectangle {
                        width: pillText.implicitWidth + 20
                        height: 28
                        radius: 14
                        color: Qt.rgba(accent.r, accent.g, accent.b, 0.12)
                        border.width: 1
                        border.color: Qt.rgba(accent.r, accent.g, accent.b, 0.30)

                        Text {
                            id: pillText
                            anchors.centerIn: parent
                            text: modelData
                            font.pixelSize: 12
                            font.weight: Font.Medium
                            color: accentGlow
                        }

                        // appear animation
                        scale: 0
                        Component.onCompleted: scale = 1
                        Behavior on scale { NumberAnimation { duration: 300; easing.type: Easing.OutBack } }
                    }
                }
            }

            // ── Import button ──────────────────────────────────────
            Rectangle {
                id: importBtn
                Layout.fillWidth: true
                height: 44
                radius: 12
                color: importMa.containsMouse
                       ? Qt.lighter(accent, 1.12)
                       : accent

                Behavior on color { ColorAnimation { duration: 180 } }

                // subtle shimmer overlay
                Rectangle {
                    anchors.fill: parent
                    radius: parent.radius
                    gradient: Gradient {
                        orientation: Gradient.Horizontal
                        GradientStop { position: 0.0; color: Qt.rgba(1,1,1, 0.06) }
                        GradientStop { position: 0.5; color: "transparent" }
                        GradientStop { position: 1.0; color: Qt.rgba(1,1,1, 0.03) }
                    }
                }

                Text {
                    anchors.centerIn: parent
                    text: bridge && bridge.isValid ? "↻  Replace License…" : "⬆  Import License…"
                    font.pixelSize: 14
                    font.weight: Font.DemiBold
                    color: "white"
                }

                MouseArea {
                    id: importMa
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: fileDialog.open()
                }

                // press effect
                scale: importMa.pressed ? 0.97 : 1.0
                Behavior on scale { NumberAnimation { duration: 100 } }
            }
        }
    }

    // ─── TOAST NOTIFICATION ────────────────────────────────────────
    Rectangle {
        id: toast
        property bool isSuccess: true
        property string text: ""
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 24
        width: toastText.implicitWidth + 40
        height: 40
        radius: 20
        color: isSuccess ? Qt.rgba(success.r, success.g, success.b, 0.18)
                         : Qt.rgba(danger.r, danger.g, danger.b, 0.18)
        border.width: 1
        border.color: isSuccess ? Qt.rgba(success.r, success.g, success.b, 0.40)
                                : Qt.rgba(danger.r, danger.g, danger.b, 0.40)
        opacity: 0
        visible: opacity > 0

        Text {
            id: toastText
            anchors.centerIn: parent
            text: (toast.isSuccess ? "✓  " : "✕  ") + toast.text
            font.pixelSize: 13
            font.weight: Font.Medium
            color: toast.isSuccess ? success : danger
        }

        SequentialAnimation {
            id: toastAnim
            NumberAnimation { target: toast; property: "opacity"; to: 1; duration: 200; easing.type: Easing.OutCubic }
            PauseAnimation  { duration: 3000 }
            NumberAnimation { target: toast; property: "opacity"; to: 0; duration: 600; easing.type: Easing.InCubic }
        }
    }
}
