import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    id: root
    padding: 8
    readonly property color pageColor: appSettings.high_contrast ? Theme.background : appSettings.dark_mode ? "#101319" : Theme.lightShade("#f7f8fc")
    readonly property color cardColor: appSettings.high_contrast ? Theme.background : appSettings.dark_mode ? "#1b202a" : Theme.lightShade("#ffffff")
    readonly property color textColor: appSettings.high_contrast ? Theme.ink : appSettings.dark_mode ? "#f0f2f8" : "#202431"
    readonly property color mutedColor: appSettings.high_contrast ? Theme.ink : appSettings.dark_mode ? "#aeb6c5" : "#616b7d"
    background: Rectangle { color: root.pageColor }

    ScrollView {
        anchors.fill: parent
        contentWidth: availableWidth
        clip: true
        ColumnLayout {
            width: parent.width
            spacing: 12
            AppButton {
                text: qsTr("Help translate")
                Layout.fillWidth: true
                implicitHeight: Math.max(48, contentItem.implicitHeight + topPadding + bottomPadding)
                onClicked: Qt.openUrlExternally(appSettings.translation_help_url)
            }
            Label { text: qsTr("Porn Fetch"); color: root.textColor; font.pixelSize: 28 * appSettings.font_size / 12; font.bold: true }
            Label { text: qsTr("Version %1").arg(Qt.application.version); color: root.mutedColor }
            Label {
                Layout.fillWidth: true
                text: qsTr("Copyright © 2023-2026 Johannes Habel (EchterAlsFake)")
                color: root.mutedColor
                wrapMode: Text.Wrap
            }
            Label { text: qsTr("Application license"); color: root.textColor; font.bold: true; font.pixelSize: 18 * appSettings.font_size / 12 }
            Label {
                Layout.fillWidth: true
                text: qsTr("Porn Fetch Source-Available License 1.0. See the full license for terms.")
                color: root.mutedColor
                wrapMode: Text.Wrap
            }
            AppButton {
                Layout.fillWidth: true
                text: qsTr("Show application license")
                onClicked: { legalDialog.showNotices = false; legalDialog.open() }
            }
            AppButton {
                Layout.fillWidth: true
                text: qsTr("Show third-party notices")
                onClicked: { legalDialog.showNotices = true; legalDialog.open() }
            }
            Label { text: qsTr("Credits"); color: root.textColor; font.bold: true; font.pixelSize: 18 * appSettings.font_size / 12 }
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
        ContrastPopupBackground { popup: legalDialog }
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
