import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    id: root
    padding: 12
    readonly property color pageColor: appSettings.dark_mode ? "#101319" : "#f7f8fc"
    readonly property color cardColor: appSettings.dark_mode ? "#1b202a" : "#ffffff"
    readonly property color textColor: appSettings.dark_mode ? "#f0f2f8" : "#202431"
    readonly property color mutedColor: appSettings.dark_mode ? "#aeb6c5" : "#616b7d"
    background: Rectangle { color: root.pageColor }

    ScrollView {
        anchors.fill: parent
        contentWidth: availableWidth
        clip: true
        ColumnLayout {
            width: parent.width
            spacing: 12
            Label { text: qsTr("Porn Fetch"); color: root.textColor; font.pixelSize: 28; font.bold: true }
            Label { text: qsTr("Version %1").arg(Qt.application.version); color: root.mutedColor }
            Label {
                Layout.fillWidth: true
                text: qsTr("Copyright © 2023–2026 Johannes Habel (EchterAlsFake)")
                color: root.mutedColor
                wrapMode: Text.Wrap
            }
            Label { text: qsTr("Application license"); color: root.textColor; font.bold: true; font.pixelSize: 18 }
            Label {
                Layout.fillWidth: true
                text: qsTr("Porn Fetch Source-Available License 1.0. See the full license for terms.")
                color: root.mutedColor
                wrapMode: Text.Wrap
            }
            Button {
                Layout.fillWidth: true
                text: qsTr("Show application license")
                onClicked: { legalDialog.showNotices = false; legalDialog.open() }
            }
            Button {
                Layout.fillWidth: true
                text: qsTr("Show third-party notices")
                onClicked: { legalDialog.showNotices = true; legalDialog.open() }
            }
            Label { text: qsTr("Credits"); color: root.textColor; font.bold: true; font.pixelSize: 18 }
            Label {
                Layout.fillWidth: true
                text: qsTr("Thanks to Egsagon for the original PHUB API and to all contributors and translators.")
                color: root.mutedColor
                wrapMode: Text.Wrap
            }
        }
    }

    Dialog {
        id: legalDialog
        property bool showNotices: false
        parent: Overlay.overlay
        anchors.centerIn: parent
        width: Math.min(root.width - 24, 700)
        height: Math.min(root.height - 24, 650)
        title: showNotices ? qsTr("Third-party notices") : qsTr("Application license")
        standardButtons: Dialog.Close
        modal: true
        contentItem: ScrollView {
            TextArea {
                readOnly: true
                wrapMode: TextArea.Wrap
                text: legalDialog.showNotices ? thirdPartyNoticesText : applicationLicenseText
            }
        }
    }
}
