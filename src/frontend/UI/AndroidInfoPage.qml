import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    id: root
    padding: 8

    ScrollView {
        anchors.fill: parent
        contentWidth: availableWidth
        clip: true
        ColumnLayout {
            width: parent.width
            spacing: 12
            Label { text: qsTr("Porn Fetch"); font.pixelSize: 28; font.bold: true }
            Label { text: qsTr("Version %1").arg(Qt.application.version) }
            Label {
                Layout.fillWidth: true
                text: qsTr("Copyright © 2023–2026 Johannes Habel (EchterAlsFake)")
                wrapMode: Text.Wrap
            }
            Label { text: qsTr("Application license"); font.bold: true }
            Label {
                Layout.fillWidth: true
                text: qsTr("Porn Fetch Source-Available License 1.0. See the full license for terms.")
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
            Label { text: qsTr("Credits"); font.bold: true }
            Label {
                Layout.fillWidth: true
                text: qsTr("Thanks to Egsagon for the original PHUB API and to all contributors and translators.")
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
