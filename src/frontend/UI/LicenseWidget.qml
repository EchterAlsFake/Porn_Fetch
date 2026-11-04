// License management panel with explicit colours for every control state.
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material
import QtQuick.Layouts 1.15
import QtQuick.Dialogs

Item {
    id: root
    implicitWidth: 460
    implicitHeight: card.implicitHeight + 48

    readonly property bool dark: appSettings.dark_mode || appSettings.high_contrast
    readonly property color bgBase: appSettings.high_contrast ? "#000000" : dark ? "#1f1f21" : "#f5f6f8"
    readonly property color bgCard: appSettings.high_contrast ? "#000000" : dark ? "#262628" : "#ffffff"
    readonly property color bgInput: appSettings.high_contrast ? "#000000" : dark ? "#303136" : "#f3f4f7"
    readonly property color border: appSettings.high_contrast ? "#ffffff" : dark ? "#666976" : "#858b98"
    readonly property color textPri: dark ? "#f3f3f5" : "#202431"
    readonly property color textSec: appSettings.high_contrast ? "#ffffff" : dark ? "#c2c4cc" : "#565e70"
    readonly property color accent: appSettings.high_contrast ? "#ffff00" : "#2563eb"
    readonly property color accentGlow: appSettings.high_contrast ? "#ffff00" : dark ? "#9cc0ff" : "#1d4ed8"
    readonly property color success: appSettings.high_contrast ? "#ffffff" : dark ? "#4ade80" : "#15803d"
    readonly property color danger: appSettings.high_contrast ? "#ffffff" : dark ? "#ff676f" : "#b91c1c"
    Material.theme: root.dark ? Material.Dark : Material.Light
    Material.foreground: root.textPri
    Material.background: root.bgCard
    Material.accent: root.accent

    component LicenseActionButton: Button {
        id: action
        implicitHeight: Math.max(48, contentItem.implicitHeight + topPadding + bottomPadding)
        contentItem: Label {
            text: action.text
            font: action.font
            color: action.enabled ? root.textPri : root.textSec
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            wrapMode: Text.Wrap
        }
        background: Rectangle {
            radius: 12
            color: action.enabled && (action.down || action.hovered)
                   ? (root.dark ? "#454853" : "#e0e4ec") : root.bgInput
            border.width: action.activeFocus ? 2 : 1
            border.color: action.activeFocus ? root.accentGlow : root.border
        }
    }

    // ── The bridge is injected via rootContext().setContextProperty() ─
    // Do NOT declare `property QtObject bridge` here — it would shadow
    // the context property and stay null.
    readonly property bool hasValidBridge: Boolean(typeof bridge !== "undefined" && bridge && bridge.isValid)
    readonly property bool isBridgeBusy: Boolean(typeof bridge !== "undefined" && bridge && bridge.busy)

    property string feedback: ""

    // ── Import feedback ─────────────────────────────────────────────
    Connections {
        target: (typeof bridge !== "undefined" && bridge) ? bridge : null
        ignoreUnknownSignals: true
        function onImportFinished(ok, msg) {
            root.feedback = typeof noticeCenter !== "undefined" ? noticeCenter.safe_text(msg)
                            : (ok ? qsTr("License imported.") : qsTr("License import failed. Check your device clock and try again."))
            if (!ok && bridge.state !== "clock_mismatch" && bridge.state !== "clock_invalid") {
                root.feedback += "\n\n" + qsTr("Check your device date, time and time zone, enable automatic time synchronization, then try again.")
            }
        }
        function onFirstActivation() {
            activationDialog.open()
        }
    }

    Connections {
        target: appSettings
        function onAnonymousModeChanged() { root.feedback = "" }
    }

    // ── Native file dialog (lives in QML, avoids QWidgets conflicts) ─
    FileDialog {
        id: fileDialog
        title: qsTr("Select license file")
        nameFilters: [qsTr("All files (*)"), qsTr("License files (*.license *.lic *.json)")]
        onAccepted: {
            console.log("[LicenseWidget] FileDialog accepted, selectedFile:", fileDialog.selectedFile)
            console.log("[LicenseWidget] bridge:", bridge)
            if (typeof bridge !== "undefined" && bridge) {
                bridge.installFromPath(fileDialog.selectedFile.toString())
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
                                          : root.border
        border.width: 1

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
                running: !appSettings.reduced_motion

                loops: Animation.Infinite
                NumberAnimation { to: 0.6;  duration: appSettings.reduced_motion ? 0 : 1800; easing.type: Easing.InOutSine }
                NumberAnimation { to: 0.15; duration: appSettings.reduced_motion ? 0 : 1800; easing.type: Easing.InOutSine }
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
                    Behavior on border.color { ColorAnimation { duration: appSettings.reduced_motion ? 0 : 400 } }
                    scale: 1.0
                    Behavior on scale { NumberAnimation { duration: appSettings.reduced_motion ? 0 : 300; easing.type: Easing.OutBack } }

                    Text {
                        anchors.centerIn: parent
                        text: root.hasValidBridge ? "✓" : "✕"
                        font.pixelSize: 32 * appSettings.font_size / 12
                        font.weight: Font.Bold
                        color: root.hasValidBridge ? success : danger
                        Behavior on color { ColorAnimation { duration: appSettings.reduced_motion ? 0 : 350 } }
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
                    font.pixelSize: 20 * appSettings.font_size / 12
                    font.weight: Font.DemiBold
                    font.letterSpacing: 0.4
                    color: textPri

                    Behavior on text {
                        SequentialAnimation {
                            NumberAnimation { target: headingFade; property: "opacity"; to: 0; duration: appSettings.reduced_motion ? 0 : 120 }
                            PropertyAction  {}
                            NumberAnimation { target: headingFade; property: "opacity"; to: 1; duration: appSettings.reduced_motion ? 0 : 200 }
                        }
                    }
                    id: headingFade
                }

                Text {
                    Layout.alignment: Qt.AlignHCenter
                    text: (typeof bridge !== "undefined" && bridge && bridge.reason) ? String(bridge.reason) : ""
                    font.pixelSize: 13 * appSettings.font_size / 12
                    color: textSec
                    horizontalAlignment: Text.AlignHCenter
                    wrapMode: Text.WordWrap
                    Layout.maximumWidth: card.width - 60
                }

                TextField {
                    id: pastedLicense
                    objectName: "pastedLicenseInput"
                    Layout.fillWidth: true
                    color: root.textPri
                    placeholderTextColor: root.textSec
                    selectionColor: root.accent
                    selectedTextColor: appSettings.high_contrast ? "#000000" : "#ffffff"
                    background: Rectangle {
                        radius: 8
                        color: root.bgInput
                        border.width: pastedLicense.activeFocus ? 2 : 1
                        border.color: pastedLicense.activeFocus ? root.accentGlow : root.border
                    }
                    Accessible.name: placeholderText
                    placeholderText: qsTr("Paste signed license key or license JSON")
                    echoMode: TextInput.Password
                    enabled: !root.isBridgeBusy
                }
                LicenseActionButton {
                    objectName: "activatePastedLicenseButton"
                    Layout.fillWidth: true
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
                            text: qsTr("Premium version entitlement ends:")
                            font.pixelSize: 12 * appSettings.font_size / 12
                            font.weight: Font.DemiBold
                            color: textSec
                        }
                        Text {
                            Layout.fillWidth: true
                            text: (typeof bridge !== "undefined" && bridge && bridge.licenseExpiresAt) ? bridge.licenseExpiresAt : qsTr("Lifetime / Never")
                            font.pixelSize: 12 * appSettings.font_size / 12
                            font.weight: Font.Bold
                            color: success
                            horizontalAlignment: Text.AlignRight
                            ToolTip.visible: expiryMa.containsMouse
                            ToolTip.text: qsTr("Premium features are covered in releases for 1 year after first activation. App updates are free for everyone.")
                            MouseArea {
                                id: expiryMa
                                anchors.fill: parent
                                hoverEnabled: true
                            }
                        }

                        Text {
                            text: qsTr("Machine Limit:")
                            font.pixelSize: 12 * appSettings.font_size / 12
                            font.weight: Font.DemiBold
                            color: textSec
                        }
                        Text {
                            Layout.fillWidth: true
                            text: qsTr("10 Devices")
                            font.pixelSize: 12 * appSettings.font_size / 12
                            font.weight: Font.Medium
                            color: textPri
                            horizontalAlignment: Text.AlignRight
                            ToolTip.visible: limitMa.containsMouse
                            ToolTip.text: qsTr("Up to 10 active machines per license simultaneously")
                            MouseArea {
                                id: limitMa
                                anchors.fill: parent
                                hoverEnabled: true
                            }
                        }

                        Text {
                            text: qsTr("Offline Permit Expires:")
                            font.pixelSize: 12 * appSettings.font_size / 12
                            font.weight: Font.DemiBold
                            color: textSec
                        }
                        Text {
                            Layout.fillWidth: true
                            text: (typeof bridge !== "undefined" && bridge && bridge.nextCheckAt) ? bridge.nextCheckAt : "—"
                            font.pixelSize: 12 * appSettings.font_size / 12
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
                        font.pixelSize: 13 * appSettings.font_size / 12
                    }
                    Text {
                        text: qsTr("How do premium entitlement & 10-machine limits work?")
                        font.pixelSize: 12 * appSettings.font_size / 12
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
                LicenseActionButton {
                    objectName: "refreshLicenseButton"
                    Layout.fillWidth: true
                    text: qsTr("Refresh")
                    enabled: (typeof bridge !== "undefined" && bridge) && !root.isBridgeBusy
                    ToolTip.visible: hovered
                    ToolTip.text: qsTr("Re-verifies license and renews the 7-day offline check-in permit")
                    onClicked: bridge.refresh()
                }
                LicenseActionButton {
                    objectName: "deactivateLicenseButton"
                    Layout.fillWidth: true
                    text: qsTr("Deactivate")
                    enabled: root.hasValidBridge && !root.isBridgeBusy
                    ToolTip.visible: hovered
                    ToolTip.text: qsTr("Unlinks this device to free up 1 of your 10 machine seats")
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

            TextArea {
                Layout.fillWidth: true
                visible: text !== ""
                text: root.feedback
                textFormat: Text.PlainText
                readOnly: true
                selectByMouse: true
                wrapMode: Text.Wrap
                background: null
                color: root.textPri
                Accessible.name: qsTr("License import result")
            }

            // ── Import button ──────────────────────────────────────
            Rectangle {
                id: importBtn
                activeFocusOnTab: true
                enabled: !root.isBridgeBusy
                Accessible.role: Accessible.Button
                Accessible.name: bridge && bridge.isValid ? qsTr("Replace license") : qsTr("Import license")
                Accessible.onPressAction: fileDialog.open()
                Keys.onSpacePressed: fileDialog.open()
                Keys.onReturnPressed: fileDialog.open()
                border.width: activeFocus ? 2 : 0
                border.color: "white"
                Layout.fillWidth: true
                height: 48
                radius: 12
                color: importMa.containsMouse
                       ? Qt.lighter(accent, 1.12)
                       : accent

                Behavior on color { ColorAnimation { duration: appSettings.reduced_motion ? 0 : 180 } }

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
                    text: bridge && bridge.isValid ? qsTr("Replace license…") : qsTr("Import license…")
                    font.pixelSize: 14 * appSettings.font_size / 12
                    font.weight: Font.DemiBold
                    color: appSettings.high_contrast ? "#000000" : "white"
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
                Behavior on scale { NumberAnimation { duration: appSettings.reduced_motion ? 0 : 100 } }
            }
        }
    }

    Dialog {
        id: activationDialog
        parent: root.Overlay.overlay ? root.Overlay.overlay : root
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
                        font.pixelSize: 20 * appSettings.font_size / 12
                    }

                    Text {
                        Layout.fillWidth: true
                        text: qsTr("License & Activation Guide")
                        font.pixelSize: 15 * appSettings.font_size / 12
                        font.bold: true
                        color: textPri
                    }

                    ToolButton {
                        text: "✕"
                        font.pixelSize: 14 * appSettings.font_size / 12
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
                            Text { text: "📅"; font.pixelSize: 15 * appSettings.font_size / 12 }
                            Text {
                                text: qsTr("Premium Version Entitlement & Free App Updates")
                                font.pixelSize: 14 * appSettings.font_size / 12
                                font.bold: true
                                color: textPri
                            }
                        }

                        Text {
                            Layout.fillWidth: true
                            wrapMode: Text.WordWrap
                            font.pixelSize: 12 * appSettings.font_size / 12
                            lineHeight: 1.25
                            color: textSec
                            textFormat: Text.RichText
                            text: qsTr("• <b>Premium version entitlement ends:</b> The release deadline for licensed premium features. App updates are free for everyone, including without a license. A <b>Permanent License</b> provides perpetual premium access to versions released during the <b>first year after activation</b>. After 1 year, you may continue using premium features in every version released during your active year forever without paying again. Installing a newer version is free; premium access still follows your license entitlement.<br><br>• <b>Offline Permit:</b> Porn Fetch checks the licensing server at every startup. If the server is unavailable, a previously valid license remains usable until its 7-day offline permit expires. A server rejection takes effect immediately.")
                        }
                    }

                    Rectangle { Layout.fillWidth: true; height: 1; color: border; opacity: 0.6 }

                    // Section 2: Refresh Button
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 6

                        RowLayout {
                            spacing: 8
                            Text { text: "🔄"; font.pixelSize: 15 * appSettings.font_size / 12 }
                            Text {
                                text: qsTr("The \"Refresh\" Button")
                                font.pixelSize: 14 * appSettings.font_size / 12
                                font.bold: true
                                color: textPri
                            }
                        }

                        Text {
                            Layout.fillWidth: true
                            wrapMode: Text.WordWrap
                            font.pixelSize: 12 * appSettings.font_size / 12
                            lineHeight: 1.25
                            color: textSec
                            textFormat: Text.RichText
                            text: qsTr("Clicking <b>Refresh</b> manually connects to the licensing server to re-validate your license and extends your 7-day offline check-in period immediately.")
                        }
                    }

                    Rectangle { Layout.fillWidth: true; height: 1; color: border; opacity: 0.6 }

                    // Section 3: Deactivate & 10-Machine Limit
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 6

                        RowLayout {
                            spacing: 8
                            Text { text: "💻"; font.pixelSize: 15 * appSettings.font_size / 12 }
                            Text {
                                text: qsTr("The \"Deactivate\" Button & 10-Machine Limit")
                                font.pixelSize: 14 * appSettings.font_size / 12
                                font.bold: true
                                color: textPri
                            }
                        }

                        Text {
                            Layout.fillWidth: true
                            wrapMode: Text.WordWrap
                            font.pixelSize: 12 * appSettings.font_size / 12
                            lineHeight: 1.25
                            color: textSec
                            textFormat: Text.RichText
                            text: qsTr("Each license includes a <b>10-machine limit</b> (up to 10 active devices simultaneously). Clicking <b>Deactivate</b> unlinks this device from Keygen on the server, <b>freeing up a seat out of your 10-machine limit</b> so you can activate and use Porn Fetch on another computer or after reinstalling your OS.")
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
                    text: qsTr("Got It")
                    highlighted: true
                    onClicked: activationDialog.close()
                }
            }
        }
    }
}
