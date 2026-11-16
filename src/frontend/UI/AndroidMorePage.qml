import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    id: root
    signal openPage(int index)
    signal openActivity()
    padding: 8
    readonly property color pageColor: appSettings.high_contrast ? Theme.background : appSettings.dark_mode ? "#101319" : Theme.lightShade("#f7f8fc")
    readonly property color cardColor: appSettings.high_contrast ? Theme.background : appSettings.dark_mode ? "#1b202a" : Theme.lightShade("#ffffff")
    readonly property color textColor: appSettings.high_contrast ? Theme.ink : appSettings.dark_mode ? "#f0f2f8" : "#202431"
    readonly property color mutedColor: appSettings.high_contrast ? Theme.ink : appSettings.dark_mode ? "#aeb6c5" : "#616b7d"
    background: Rectangle { color: root.pageColor }

    ColumnLayout {
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        spacing: 8
        AppButton {
            id: creatorsButton
            KeyNavigation.down: activityButton
            Layout.fillWidth: true
            text: qsTr("Creators")
            icon.source: "qrc:/images/graphics/creators.svg"
            icon.color: Theme.ink
            onClicked: root.openPage(7)
        }
        AppButton {
            id: activityButton
            KeyNavigation.up: creatorsButton
            KeyNavigation.down: aboutEntry
            Layout.fillWidth: true
            text: qsTr("Recent activity")
            onClicked: root.openActivity()
        }
        ItemDelegate {
            id: aboutEntry
            KeyNavigation.up: activityButton
            KeyNavigation.down: websitesEntry
            Layout.fillWidth: true
            Layout.preferredHeight: 88
            onClicked: root.openPage(3)
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
                Label { text: "›"; color: root.mutedColor; font.pixelSize: 26 * appSettings.font_size / 12 }
            }
        }
        ItemDelegate {
            id: websitesEntry
            KeyNavigation.up: aboutEntry
            Layout.fillWidth: true
            Layout.preferredHeight: 88
            onClicked: root.openPage(4)
            Keys.onReturnPressed: root.openPage(4)
            Keys.onEnterPressed: root.openPage(4)
            Keys.onSelectPressed: root.openPage(4)
            background: Rectangle {
                color: root.cardColor
                radius: 20
                border.width: parent.visualFocus ? 3 : 0
                border.color: Theme.accent
            }
            contentItem: RowLayout {
                spacing: 16
                Image {
                    source: "qrc:/images/graphics/information.png"
                    Layout.preferredWidth: 40
                    Layout.preferredHeight: 40
                    fillMode: Image.PreserveAspectFit
                }
                ColumnLayout {
                    Layout.fillWidth: true
                    Label { text: qsTr("Supported websites"); color: root.textColor; font.bold: true }
                    Label { text: qsTr("Explore websites and supported links"); color: root.mutedColor; wrapMode: Text.WordWrap; Layout.fillWidth: true }
                }
                Label { text: "›"; color: root.mutedColor; font.pixelSize: 26 * appSettings.font_size / 12 }
            }
        }
    }
}
