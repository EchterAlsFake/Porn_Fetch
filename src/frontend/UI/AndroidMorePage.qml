import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    id: root
    signal openPage(int index)
    padding: 12
    readonly property color pageColor: appSettings.dark_mode ? "#101319" : "#f7f8fc"
    readonly property color cardColor: appSettings.dark_mode ? "#1b202a" : "#ffffff"
    readonly property color textColor: appSettings.dark_mode ? "#f0f2f8" : "#202431"
    readonly property color mutedColor: appSettings.dark_mode ? "#aeb6c5" : "#616b7d"
    background: Rectangle { color: root.pageColor }

    ColumnLayout {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        spacing: 12
        Item { Layout.preferredHeight: 4 }
        ItemDelegate {
            Layout.fillWidth: true
            Layout.preferredHeight: 88
            onClicked: root.openPage(4)
            background: Rectangle { color: root.cardColor; radius: 20 }
            contentItem: RowLayout {
                spacing: 16
                Image {
                    source: "qrc:/images/graphics/logo.png"
                    Layout.preferredWidth: 48
                    Layout.preferredHeight: 48
                    fillMode: Image.PreserveAspectFit
                }
                ColumnLayout {
                    Layout.fillWidth: true
                    Label { text: qsTr("About Porn Fetch"); color: root.textColor; font.bold: true }
                    Label { text: qsTr("Version, licenses and credits"); color: root.mutedColor }
                }
                Label { text: "›"; color: root.mutedColor; font.pixelSize: 26 }
            }
        }
        ItemDelegate {
            Layout.fillWidth: true
            Layout.preferredHeight: 88
            onClicked: root.openPage(5)
            background: Rectangle { color: root.cardColor; radius: 20 }
            contentItem: RowLayout {
                spacing: 16
                Image {
                    source: "qrc:/images/graphics/information.svg"
                    Layout.preferredWidth: 40
                    Layout.preferredHeight: 40
                    fillMode: Image.PreserveAspectFit
                }
                ColumnLayout {
                    Layout.fillWidth: true
                    Label { text: qsTr("Supported websites"); color: root.textColor; font.bold: true }
                    Label { text: qsTr("See where downloads work"); color: root.mutedColor }
                }
                Label { text: "›"; color: root.mutedColor; font.pixelSize: 26 }
            }
        }
    }
}
