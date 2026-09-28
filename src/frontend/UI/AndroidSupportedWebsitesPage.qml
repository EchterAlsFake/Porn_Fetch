import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Pane {
    padding: 8
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
                    contentItem: ColumnLayout {
                        Label { text: modelData.category; font.bold: true }
                        Label { Layout.fillWidth: true; text: modelData.sites; wrapMode: Text.Wrap }
                    }
                }
            }
        }
    }
}
