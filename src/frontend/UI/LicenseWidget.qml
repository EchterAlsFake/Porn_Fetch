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
    readonly property bool hasValidBridge: Boolean(typeof bridge !== "undefined" && bridge && bridge.isValid)
    readonly property bool isBridgeBusy: Boolean(typeof bridge !== "undefined" && bridge && bridge.busy)

    // ── Toast feedback ─────────────────────────────────────────────
    Connections {
        target: (typeof bridge !== "undefined" && bridge) ? bridge : null
        ignoreUnknownSignals: true
        function onImportFinished(ok, msg) {
            toast.isSuccess = ok
            toast.text      = msg
            toastAnim.restart()
        }
        function onFirstActivation() {
            activationDialog.open()
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
            if (typeof bridge !== "undefined" && bridge) {
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
        border.color: root.hasValidBridge ? Qt.rgba(success.r, success.g, success.b, 0.35)
                                          : Qt.rgba(border.r, border.g, border.b, 1)
        border.width: 1

        // subtle inner shadow
        layer.enabled: true
        layer.effect: DropShadow {
            transparentBorder: true
            radius: 32; samples: 65
            color: root.hasValidBridge ? Qt.rgba(success.r, success.g, success.b, 0.10)
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
            border.color: root.hasValidBridge
                          ? Qt.rgba(success.r, success.g, success.b, glowRing.pulse)
                          : "transparent"
            property real pulse: 0.0
            visible: root.hasValidBridge

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
                    color: root.hasValidBridge
                           ? Qt.rgba(success.r, success.g, success.b, 0.12)
                           : Qt.rgba(danger.r, danger.g, danger.b, 0.10)
                    border.width: 1.5
                    border.color: root.hasValidBridge
                                  ? Qt.rgba(success.r, success.g, success.b, 0.30)
                                  : Qt.rgba(danger.r, danger.g, danger.b, 0.25)

                    // scale-pop on change
                    Behavior on border.color { ColorAnimation { duration: 400 } }
                    scale: 1.0
                    Behavior on scale { NumberAnimation { duration: 300; easing.type: Easing.OutBack } }

                    Text {
                        anchors.centerIn: parent
                        text: root.hasValidBridge ? "✓" : "✕"
                        font.pixelSize: 32
                        font.weight: Font.Bold
                        color: root.hasValidBridge ? success : danger
                        Behavior on color { ColorAnimation { duration: 350 } }
                    }

                    // trigger pop on status change
                    Connections {
                        target: (typeof bridge !== "undefined" && bridge) ? bridge : null
                        ignoreUnknownSignals: true
                        function onStatusChanged() { badge.scale = 0.85; badge.scale = 1.0 }
                    }
                }

                Text {
                    Layout.alignment: Qt.AlignHCenter
                    text: root.hasValidBridge ? "License Active" : "No Valid License"
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
                    text: (typeof bridge !== "undefined" && bridge && bridge.reason) ? String(bridge.reason) : ""
                    font.pixelSize: 13
                    color: textSec
                    horizontalAlignment: Text.AlignHCenter
                    wrapMode: Text.WordWrap
                    Layout.maximumWidth: card.width - 60
                }

                TextField {
                    id: pastedLicense
                    Layout.fillWidth: true
                    placeholderText: qsTr("Paste signed license key or license JSON")
                    echoMode: TextInput.Password
                    enabled: !root.isBridgeBusy
                }
                Button {
                    text: qsTr("Activate pasted license")
                    enabled: !root.isBridgeBusy && pastedLicense.text.length > 0
                    onClicked: {
                        bridge.installFromText(pastedLicense.text)
                        pastedLicense.clear()
                    }
                }

                // Two expiry dates card
                Rectangle {
                    Layout.fillWidth: true
                    implicitHeight: expiryGrid.implicitHeight + 20
                    radius: 12
                    color: bgInput
                    border.color: border
                    border.width: 1
                    visible: root.hasValidBridge

                    GridLayout {
                        id: expiryGrid
                        anchors.fill: parent
                        anchors.margins: 10
                        columns: 2
                        rowSpacing: 8
                        columnSpacing: 12

                        Text {
                            text: "Update entitlement ends:"
                            font.pixelSize: 12
                            font.weight: Font.DemiBold
                            color: textSec
                        }
                        Text {
                            Layout.fillWidth: true
                            text: (typeof bridge !== "undefined" && bridge && bridge.licenseExpiresAt) ? bridge.licenseExpiresAt : "Lifetime / Never"
                            font.pixelSize: 12
                            font.weight: Font.Bold
                            color: success
                            horizontalAlignment: Text.AlignRight
                            ToolTip.visible: expiryMa.containsMouse
                            ToolTip.text: "Permanent license: valid for current release + updates for 1 year after first activation"
                            MouseArea {
                                id: expiryMa
                                anchors.fill: parent
                                hoverEnabled: true
                            }
                        }

                        Text {
                            text: "Machine Limit:"
                            font.pixelSize: 12
                            font.weight: Font.DemiBold
                            color: textSec
                        }
                        Text {
                            Layout.fillWidth: true
                            text: "10 Devices"
                            font.pixelSize: 12
                            font.weight: Font.Medium
                            color: textPri
                            horizontalAlignment: Text.AlignRight
                            ToolTip.visible: limitMa.containsMouse
                            ToolTip.text: "Up to 10 active machines per license simultaneously"
                            MouseArea {
                                id: limitMa
                                anchors.fill: parent
                                hoverEnabled: true
                            }
                        }

                        Text {
                            text: "Offline Permit Expires:"
                            font.pixelSize: 12
                            font.weight: Font.DemiBold
                            color: textSec
                        }
                        Text {
                            Layout.fillWidth: true
                            text: (typeof bridge !== "undefined" && bridge && bridge.nextCheckAt) ? bridge.nextCheckAt : "—"
                            font.pixelSize: 12
                            font.weight: Font.Medium
                            color: textPri
                            horizontalAlignment: Text.AlignRight
                        }
                    }
                }

                // Info link
                RowLayout {
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 6
                    visible: root.hasValidBridge

                    Text {
                        text: "ℹ️"
                        font.pixelSize: 13
                    }
                    Text {
                        text: "How do expiry, 1-yr updates & 10-machine limits work?"
                        font.pixelSize: 12
                        font.underline: helpMa.containsMouse
                        color: helpMa.containsMouse ? accentGlow : accent

                        MouseArea {
                            id: helpMa
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: activationDialog.open()
                        }
                    }
                }
            }

            RowLayout {
                Layout.fillWidth: true
                Button {
                    Layout.fillWidth: true
                    text: "Refresh"
                    enabled: (typeof bridge !== "undefined" && bridge) && !root.isBridgeBusy
                    ToolTip.visible: hovered
                    ToolTip.text: "Re-verifies license and renews the 7-day offline check-in permit"
                    onClicked: bridge.refresh()
                }
                Button {
                    Layout.fillWidth: true
                    text: "Deactivate"
                    enabled: root.hasValidBridge && !root.isBridgeBusy
                    ToolTip.visible: hovered
                    ToolTip.text: "Unlinks this device to free up 1 of your 10 machine seats"
                    onClicked: bridge.deactivate()
                }
            }

            // ── Separator ──────────────────────────────────────────
            Rectangle {
                Layout.fillWidth: true
                height: 1
                color: border
                opacity: 0.6
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
                    enabled: (typeof bridge !== "undefined" && bridge) && !root.isBridgeBusy
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

    // ─── ACTIVATION & LICENSE INFO DIALOG ──────────────────────────
    Dialog {
        id: activationDialog
        parent: Overlay.overlay ? Overlay.overlay : root
        anchors.centerIn: parent
        width: Math.min(parent ? parent.width - 32 : 460, 460)
        modal: true
        padding: 0
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

        background: Rectangle {
            radius: 16
            color: bgCard
            border.color: Qt.rgba(accent.r, accent.g, accent.b, 0.45)
            border.width: 1

            layer.enabled: true
            layer.effect: DropShadow {
                transparentBorder: true
                radius: 24; samples: 49
                color: Qt.rgba(0, 0, 0, 0.7)
                verticalOffset: 6
            }
        }

        contentItem: ColumnLayout {
            spacing: 0

            // Header
            Rectangle {
                Layout.fillWidth: true
                implicitHeight: 54
                color: Qt.rgba(accent.r, accent.g, accent.b, 0.14)
                radius: 16

                Rectangle {
                    anchors.bottom: parent.bottom
                    anchors.left: parent.left
                    anchors.right: parent.right
                    height: 16
                    color: parent.color
                }

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 20
                    anchors.rightMargin: 16
                    spacing: 10

                    Text {
                        text: "🔑"
                        font.pixelSize: 20
                    }

                    Text {
                        Layout.fillWidth: true
                        text: "License & Activation Guide"
                        font.pixelSize: 15
                        font.bold: true
                        color: textPri
                    }

                    ToolButton {
                        text: "✕"
                        font.pixelSize: 14
                        contentItem: Text {
                            text: parent.text
                            font: parent.font
                            color: textSec
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        background: Rectangle { color: "transparent" }
                        onClicked: activationDialog.close()
                    }
                }
            }

            // Body
            ScrollView {
                Layout.fillWidth: true
                Layout.preferredHeight: Math.min(dlgCol.implicitHeight, 350)
                clip: true
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
                ScrollBar.vertical.policy: ScrollBar.AsNeeded

                ColumnLayout {
                    id: dlgCol
                    width: activationDialog.width - 32
                    x: 16
                    spacing: 14

                    Item { implicitHeight: 4 }

                    // Section 1: Expiry vs Check-in
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 6

                        RowLayout {
                            spacing: 8
                            Text { text: "📅"; font.pixelSize: 15 }
                            Text {
                                text: "Update Entitlement & 1-Year Updates"
                                font.pixelSize: 14
                                font.bold: true
                                color: textPri
                            }
                        }

                        Text {
                            Layout.fillWidth: true
                            wrapMode: Text.WordWrap
                            font.pixelSize: 12
                            lineHeight: 1.25
                            color: textSec
                            textFormat: Text.RichText
                            text: "• <b>Update entitlement ends:</b> The deadline for receiving new releases. A <b>Permanent License</b> provides perpetual access to the versions released during your entitlement and includes all subsequent updates and releases for <b>1 year after first activation</b>. After 1 year, you may continue using every version released during your active year forever without paying again.<br><br>• <b>Offline Permit:</b> Porn Fetch checks the licensing server at every startup. If the server is unavailable, a previously valid license remains usable until its 7-day offline permit expires. A server rejection takes effect immediately."
                        }
                    }

                    Rectangle { Layout.fillWidth: true; height: 1; color: border; opacity: 0.6 }

                    // Section 2: Refresh Button
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 6

                        RowLayout {
                            spacing: 8
                            Text { text: "🔄"; font.pixelSize: 15 }
                            Text {
                                text: "The \"Refresh\" Button"
                                font.pixelSize: 14
                                font.bold: true
                                color: textPri
                            }
                        }

                        Text {
                            Layout.fillWidth: true
                            wrapMode: Text.WordWrap
                            font.pixelSize: 12
                            lineHeight: 1.25
                            color: textSec
                            textFormat: Text.RichText
                            text: "Clicking <b>Refresh</b> manually connects to the licensing server to re-validate your license and extends your 7-day offline check-in period immediately."
                        }
                    }

                    Rectangle { Layout.fillWidth: true; height: 1; color: border; opacity: 0.6 }

                    // Section 3: Deactivate & 10-Machine Limit
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 6

                        RowLayout {
                            spacing: 8
                            Text { text: "💻"; font.pixelSize: 15 }
                            Text {
                                text: "The \"Deactivate\" Button & 10-Machine Limit"
                                font.pixelSize: 14
                                font.bold: true
                                color: textPri
                            }
                        }

                        Text {
                            Layout.fillWidth: true
                            wrapMode: Text.WordWrap
                            font.pixelSize: 12
                            lineHeight: 1.25
                            color: textSec
                            textFormat: Text.RichText
                            text: "Each license includes a <b>10-machine limit</b> (up to 10 active devices simultaneously). Clicking <b>Deactivate</b> unlinks this device from Keygen on the server, <b>freeing up a seat out of your 10-machine limit</b> so you can activate and use Porn Fetch on another computer or after reinstalling your OS."
                        }
                    }

                    Item { implicitHeight: 8 }
                }
            }

            // Footer
            Rectangle {
                Layout.fillWidth: true
                implicitHeight: 52
                color: bgBase
                radius: 16

                Rectangle {
                    anchors.top: parent.top
                    anchors.left: parent.left
                    anchors.right: parent.right
                    height: 16
                    color: parent.color
                }

                Button {
                    anchors.centerIn: parent
                    implicitWidth: 140
                    implicitHeight: 34
                    text: "Got It"
                    highlighted: true
                    onClicked: activationDialog.close()
                }
            }
        }
    }
}
