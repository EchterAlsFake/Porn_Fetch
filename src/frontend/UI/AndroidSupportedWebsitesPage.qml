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
            spacing: 8
            Repeater {
                model: [
                    { category: qsTr("Videos"), sites: "PornHub, HQporner, Eporner, xnxx, xvideos, missav, Xhamster, Spankbang, YouPorn" },
                    { category: qsTr("Searching"), sites: "PornHub, HQporner, Eporner, xnxx, xvideos, missav, Xhamster, Spankbang" },
                    { category: qsTr("Models and creators"), sites: "PornHub, HQporner, xnxx, Xhamster, Spankbang" },
                    { category: qsTr("Channels"), sites: "PornHub, Xhamster, Spankbang" },
                    { category: qsTr("Playlists"), sites: "PornHub, xvideos, youporn" },
                    { category: qsTr("Shorts"), sites: "Xhamster" },
                    { category: qsTr("Account login"), sites: "PornHub, XHamster, XVideos" }
                ]
                delegate: Frame {
                    required property var modelData
                    Layout.fillWidth: true
                    padding: 16
                    background: Rectangle { color: root.cardColor; radius: 18 }
                    contentItem: ColumnLayout {
                        Label { text: modelData.category; color: root.textColor; font.bold: true; font.pixelSize: 17 }
                        Label { Layout.fillWidth: true; text: modelData.sites; color: root.mutedColor; wrapMode: Text.Wrap }
                    }
                }
            }
        }
    }
}
